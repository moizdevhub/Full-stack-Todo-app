from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from typing import Optional
import math

from ..models.todo import Todo, TodoCreate, TodoUpdate, TodoRead, TodoListResponse
from ..services.todo_service import todo_service
from ..middleware.auth import get_current_user_id
from ..database.session import get_session

router = APIRouter(prefix="/todos", tags=["Todos"])


def serialize_todo(todo: Todo) -> TodoRead:
    """Serialize a Todo object to TodoRead, handling tags relationship."""
    return TodoRead(
        id=todo.id,
        user_id=todo.user_id,
        title=todo.title,
        description=todo.description,
        completed=todo.completed,
        priority=todo.priority,
        due_date=todo.due_date,
        created_at=todo.created_at,
        updated_at=todo.updated_at,
        tags=[{"id": str(tag.id), "name": tag.name, "color": tag.color} for tag in todo.tags] if todo.tags else []
    )


@router.post("", response_model=TodoRead, status_code=status.HTTP_201_CREATED)
async def create_todo(
    todo_data: TodoCreate,
    user_id: UUID = Depends(get_current_user_id),
    session: AsyncSession = Depends(get_session)
):
    """Create a new todo for the authenticated user.

    Args:
        todo_data: Todo creation data
        user_id: Authenticated user's UUID (from JWT)
        session: Database session

    Returns:
        Created todo
    """
    todo = await todo_service.create_todo(session, user_id, todo_data)
    return serialize_todo(todo)


@router.get("", response_model=TodoListResponse)
async def get_todos(
    completed: Optional[bool] = None,
    sort_order: str = "desc",
    search: Optional[str] = Query(None, max_length=500),
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=100),
    user_id: UUID = Depends(get_current_user_id),
    session: AsyncSession = Depends(get_session)
):
    """Get todos for the authenticated user with search and pagination.

    Args:
        completed: Optional filter by completion status
        sort_order: Sort order for created_at ("asc" or "desc")
        search: Optional search query for title and description
        page: Page number (1-indexed, default: 1)
        page_size: Number of items per page (default: 50, max: 100)
        user_id: Authenticated user's UUID (from JWT)
        session: Database session

    Returns:
        Paginated list of todos with metadata
    """
    todos, total_count = await todo_service.get_user_todos(
        session, user_id, completed, sort_order, search, page, page_size
    )

    total_pages = math.ceil(total_count / page_size) if total_count > 0 else 1

    return TodoListResponse(
        todos=[serialize_todo(todo) for todo in todos],
        total=total_count,
        page=page,
        page_size=page_size,
        total_pages=total_pages
    )


@router.get("/{todo_id}", response_model=TodoRead)
async def get_todo(
    todo_id: UUID,
    user_id: UUID = Depends(get_current_user_id),
    session: AsyncSession = Depends(get_session)
):
    """Get a specific todo by ID.

    Args:
        todo_id: Todo UUID
        user_id: Authenticated user's UUID (from JWT)
        session: Database session

    Returns:
        Todo if found

    Raises:
        HTTPException: If todo not found or doesn't belong to user
    """
    todo = await todo_service.get_todo_by_id(session, user_id, todo_id)
    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found"
        )
    return serialize_todo(todo)


@router.put("/{todo_id}", response_model=TodoRead)
async def update_todo(
    todo_id: UUID,
    todo_data: TodoUpdate,
    user_id: UUID = Depends(get_current_user_id),
    session: AsyncSession = Depends(get_session)
):
    """Update a todo.

    Args:
        todo_id: Todo UUID
        todo_data: Todo update data
        user_id: Authenticated user's UUID (from JWT)
        session: Database session

    Returns:
        Updated todo

    Raises:
        HTTPException: If todo not found or doesn't belong to user
    """
    todo = await todo_service.update_todo(session, user_id, todo_id, todo_data)
    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found"
        )
    return serialize_todo(todo)


@router.patch("/{todo_id}/status", response_model=TodoRead)
async def update_todo_status(
    todo_id: UUID,
    completed: bool,
    user_id: UUID = Depends(get_current_user_id),
    session: AsyncSession = Depends(get_session)
):
    """Update todo completion status.

    Args:
        todo_id: Todo UUID
        completed: New completion status
        user_id: Authenticated user's UUID (from JWT)
        session: Database session

    Returns:
        Updated todo

    Raises:
        HTTPException: If todo not found or doesn't belong to user
    """
    todo_data = TodoUpdate(completed=completed)
    todo = await todo_service.update_todo(session, user_id, todo_id, todo_data)
    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found"
        )
    return serialize_todo(todo)


@router.delete("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(
    todo_id: UUID,
    user_id: UUID = Depends(get_current_user_id),
    session: AsyncSession = Depends(get_session)
):
    """Delete a todo.

    Args:
        todo_id: Todo UUID
        user_id: Authenticated user's UUID (from JWT)
        session: Database session

    Raises:
        HTTPException: If todo not found or doesn't belong to user
    """
    deleted = await todo_service.delete_todo(session, user_id, todo_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found"
        )
