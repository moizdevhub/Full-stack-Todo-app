"""Context reconstruction service for stateless architecture."""

from typing import Dict, List

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from ..models.conversation import Conversation
from ..models.message import Message


async def get_conversation_history(
    session: AsyncSession, user_id: str, conversation_id: int
) -> List[Dict[str, str]]:
    """
    Reconstruct conversation context from database.

    Args:
        session: Database session
        user_id: User UUID from JWT sub claim
        conversation_id: Conversation ID to retrieve

    Returns:
        List of messages in format [{"role": "user", "content": "..."}, ...]

    Raises:
        HTTPException: 401 if conversation doesn't exist or doesn't belong to user
    """
    # Verify conversation ownership
    conversation = await session.get(Conversation, conversation_id)

    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")

    if conversation.user_id != user_id:
        raise HTTPException(
            status_code=401, detail="Unauthorized: Conversation does not belong to user"
        )

    # Fetch messages in chronological order
    query = (
        select(Message)
        .where(Message.conversation_id == conversation_id)
        .order_by(Message.created_at)
    )

    result = await session.execute(query)
    messages = result.scalars().all()

    # Format messages for agent
    return [{"role": msg.role, "content": msg.content} for msg in messages]


async def verify_conversation_ownership(
    session: AsyncSession, user_id: str, conversation_id: int
) -> Conversation:
    """
    Verify that a conversation belongs to the authenticated user.

    Args:
        session: Database session
        user_id: User UUID from JWT sub claim
        conversation_id: Conversation ID to verify

    Returns:
        Conversation: The verified conversation

    Raises:
        HTTPException: 401 if conversation doesn't exist or doesn't belong to user
    """
    conversation = await session.get(Conversation, conversation_id)

    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")

    if conversation.user_id != user_id:
        raise HTTPException(
            status_code=401, detail="Unauthorized: Conversation does not belong to user"
        )

    return conversation


async def create_conversation(session: AsyncSession, user_id: str) -> Conversation:
    """
    Create a new conversation for the user.

    Args:
        session: Database session
        user_id: User UUID from JWT sub claim

    Returns:
        Conversation: The newly created conversation
    """
    conversation = Conversation(user_id=user_id)
    session.add(conversation)
    await session.commit()
    await session.refresh(conversation)
    return conversation


async def save_message(
    session: AsyncSession, conversation_id: int, user_id: str, role: str, content: str
) -> Message:
    """
    Save a message to the database.

    Args:
        session: Database session
        conversation_id: Conversation ID
        user_id: User UUID from JWT sub claim
        role: Message role ("user" or "assistant")
        content: Message content

    Returns:
        Message: The saved message
    """
    message = Message(
        user_id=user_id, conversation_id=conversation_id, role=role, content=content
    )
    session.add(message)
    await session.commit()
    await session.refresh(message)
    return message


async def update_conversation_timestamp(session: AsyncSession, conversation_id: int) -> None:
    """
    Update conversation's updated_at timestamp.

    Args:
        session: Database session
        conversation_id: Conversation ID to update
    """
    from datetime import datetime

    conversation = await session.get(Conversation, conversation_id)
    if conversation:
        conversation.updated_at = datetime.utcnow()
        await session.commit()
