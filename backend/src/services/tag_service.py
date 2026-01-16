from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from uuid import UUID
from typing import Optional, List

from ..models.tag import Tag, TagCreate, TagUpdate


class TagService:
    """Service for handling tag CRUD operations with row-level security."""

    async def create_tag(
        self,
        session: AsyncSession,
        user_id: UUID,
        tag_data: TagCreate
    ) -> Tag:
        """Create a new tag for the authenticated user."""
        new_tag = Tag(
            user_id=user_id,
            name=tag_data.name.strip(),
            color=tag_data.color or "#3B82F6",
        )

        session.add(new_tag)
        await session.commit()
        await session.refresh(new_tag)

        return new_tag

    async def get_user_tags(
        self,
        session: AsyncSession,
        user_id: UUID
    ) -> List[Tag]:
        """Get all tags for the authenticated user."""
        result = await session.execute(
            select(Tag).where(Tag.user_id == user_id).order_by(Tag.name)
        )
        return list(result.scalars().all())

    async def get_tag_by_id(
        self,
        session: AsyncSession,
        user_id: UUID,
        tag_id: UUID
    ) -> Optional[Tag]:
        """Get a specific tag by ID with row-level security."""
        result = await session.execute(
            select(Tag).where(
                Tag.id == tag_id,
                Tag.user_id == user_id
            )
        )
        return result.scalar_one_or_none()

    async def update_tag(
        self,
        session: AsyncSession,
        user_id: UUID,
        tag_id: UUID,
        tag_data: TagUpdate
    ) -> Optional[Tag]:
        """Update a tag with row-level security."""
        tag = await self.get_tag_by_id(session, user_id, tag_id)
        if not tag:
            return None

        if tag_data.name is not None:
            tag.name = tag_data.name.strip()

        if tag_data.color is not None:
            tag.color = tag_data.color

        session.add(tag)
        await session.commit()
        await session.refresh(tag)

        return tag

    async def delete_tag(
        self,
        session: AsyncSession,
        user_id: UUID,
        tag_id: UUID
    ) -> bool:
        """Delete a tag with row-level security."""
        tag = await self.get_tag_by_id(session, user_id, tag_id)
        if not tag:
            return False

        await session.delete(tag)
        await session.commit()

        return True


# Create singleton instance
tag_service = TagService()
