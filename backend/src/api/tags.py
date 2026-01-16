from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from ..models.tag import Tag, TagCreate, TagUpdate, TagRead
from ..services.tag_service import tag_service
from ..middleware.auth import get_current_user_id
from ..database.session import get_session

router = APIRouter(prefix="/tags", tags=["Tags"])


@router.post("", response_model=TagRead, status_code=status.HTTP_201_CREATED)
async def create_tag(
    tag_data: TagCreate,
    user_id: UUID = Depends(get_current_user_id),
    session: AsyncSession = Depends(get_session)
):
    """Create a new tag for the authenticated user."""
    tag = await tag_service.create_tag(session, user_id, tag_data)
    return TagRead.from_orm(tag)


@router.get("", response_model=list[TagRead])
async def get_tags(
    user_id: UUID = Depends(get_current_user_id),
    session: AsyncSession = Depends(get_session)
):
    """Get all tags for the authenticated user."""
    tags = await tag_service.get_user_tags(session, user_id)
    return [TagRead.from_orm(tag) for tag in tags]


@router.get("/{tag_id}", response_model=TagRead)
async def get_tag(
    tag_id: UUID,
    user_id: UUID = Depends(get_current_user_id),
    session: AsyncSession = Depends(get_session)
):
    """Get a specific tag by ID."""
    tag = await tag_service.get_tag_by_id(session, user_id, tag_id)
    if not tag:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tag not found"
        )
    return TagRead.from_orm(tag)


@router.put("/{tag_id}", response_model=TagRead)
async def update_tag(
    tag_id: UUID,
    tag_data: TagUpdate,
    user_id: UUID = Depends(get_current_user_id),
    session: AsyncSession = Depends(get_session)
):
    """Update a tag."""
    tag = await tag_service.update_tag(session, user_id, tag_id, tag_data)
    if not tag:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tag not found"
        )
    return TagRead.from_orm(tag)


@router.delete("/{tag_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_tag(
    tag_id: UUID,
    user_id: UUID = Depends(get_current_user_id),
    session: AsyncSession = Depends(get_session)
):
    """Delete a tag."""
    deleted = await tag_service.delete_tag(session, user_id, tag_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tag not found"
        )
