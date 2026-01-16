from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlmodel import select, or_, func
from uuid import UUID
from datetime import datetime
from typing import Optional

from ..models.todo import Todo, TodoCreate, TodoUpdate


class TodoService:
    """Service for handling todo CRUD operations with row-level security."""

    async def create_todo(
        self,
        session: AsyncSession,
        user_id: UUID,
        todo_data: TodoCreate
    ) -> Todo:
        """Create a new todo for the authenticated user.

        Args:
            session: Database session
            user_id: Authenticated user's UUID
            todo_data: Todo creation data

        Returns:
            Created todo
        """
        new_todo = Todo(
            user_id=user_id,
            title=todo_data.title.strip(),
            description=todo_data.description.strip() if todo_data.description else None,
            priority=todo_data.priority or "medium",
            due_date=todo_data.due_date,
        )

        session.add(new_todo)
        await session.commit()
        await session.refresh(new_todo, ["tags"])

        # Associate tags if provided
        if todo_data.tag_ids:
            from ..models.tag import Tag
            # Fetch tags that belong to the user
            result = await session.execute(
                select(Tag).where(
                    Tag.id.in_(todo_data.tag_ids),
                    Tag.user_id == user_id
                )
            )
            tags = result.scalars().all()
            new_todo.tags = list(tags)
            await session.commit()
            await session.refresh(new_todo, ["tags"])

        return new_todo

    async def get_user_todos(
        self,
        session: AsyncSession,
        user_id: UUID,
        completed: Optional[bool] = None,
        sort_order: str = "desc",
        search: Optional[str] = None,
        page: int = 1,
        page_size: int = 50
    ) -> tuple[list[Todo], int]:
        """Get todos for the authenticated user with filtering, search, and pagination.

        Args:
            session: Database session
            user_id: Authenticated user's UUID
            completed: Optional filter by completion status
            sort_order: Sort order for created_at ("asc" or "desc")
            search: Optional search query for title and description
            page: Page number (1-indexed)
            page_size: Number of items per page

        Returns:
            Tuple of (list of todos, total count)
        """
        # Base query with eager loading of tags
        query = select(Todo).where(Todo.user_id == user_id).options(selectinload(Todo.tags))

        # Apply completion filter if provided
        if completed is not None:
            query = query.where(Todo.completed == completed)

        # Apply search filter if provided
        if search and search.strip():
            search_term = f"%{search.strip()}%"
            query = query.where(
                or_(
                    Todo.title.ilike(search_term),
                    Todo.description.ilike(search_term)
                )
            )

        # Get total count before pagination
        count_query = select(func.count()).select_from(query.subquery())
        total_result = await session.execute(count_query)
        total_count = total_result.scalar_one()

        # Apply sorting
        if sort_order == "asc":
            query = query.order_by(Todo.created_at.asc())
        else:
            query = query.order_by(Todo.created_at.desc())

        # Apply pagination
        offset = (page - 1) * page_size
        query = query.offset(offset).limit(page_size)

        result = await session.execute(query)
        todos = result.scalars().all()

        return list(todos), total_count

    async def get_todo_by_id(
        self,
        session: AsyncSession,
        user_id: UUID,
        todo_id: UUID
    ) -> Optional[Todo]:
        """Get a specific todo by ID with row-level security.

        Args:
            session: Database session
            user_id: Authenticated user's UUID
            todo_id: Todo UUID to retrieve

        Returns:
            Todo if found and belongs to user, None otherwise
        """
        result = await session.execute(
            select(Todo)
            .where(
                Todo.id == todo_id,
                Todo.user_id == user_id
            )
            .options(selectinload(Todo.tags))
        )
        return result.scalar_one_or_none()

    async def update_todo(
        self,
        session: AsyncSession,
        user_id: UUID,
        todo_id: UUID,
        todo_data: TodoUpdate
    ) -> Optional[Todo]:
        """Update a todo with row-level security.

        Args:
            session: Database session
            user_id: Authenticated user's UUID
            todo_id: Todo UUID to update
            todo_data: Todo update data

        Returns:
            Updated todo if found and belongs to user, None otherwise
        """
        # Fetch todo with row-level security
        todo = await self.get_todo_by_id(session, user_id, todo_id)
        if not todo:
            return None

        # Update fields if provided
        if todo_data.title is not None:
            todo.title = todo_data.title.strip()

        if todo_data.description is not None:
            todo.description = todo_data.description.strip() if todo_data.description else None

        if todo_data.completed is not None:
            todo.completed = todo_data.completed

        if todo_data.priority is not None:
            todo.priority = todo_data.priority

        if todo_data.due_date is not None:
            todo.due_date = todo_data.due_date

        # Update tags if provided
        if todo_data.tag_ids is not None:
            from ..models.tag import Tag
            # Fetch tags that belong to the user
            result = await session.execute(
                select(Tag).where(
                    Tag.id.in_(todo_data.tag_ids),
                    Tag.user_id == user_id
                )
            )
            tags = result.scalars().all()
            todo.tags = list(tags)

        # Update timestamp
        todo.updated_at = datetime.utcnow()

        session.add(todo)
        await session.commit()
        await session.refresh(todo, ["tags"])

        return todo

    async def delete_todo(
        self,
        session: AsyncSession,
        user_id: UUID,
        todo_id: UUID
    ) -> bool:
        """Delete a todo with row-level security.

        Args:
            session: Database session
            user_id: Authenticated user's UUID
            todo_id: Todo UUID to delete

        Returns:
            True if deleted, False if not found or doesn't belong to user
        """
        # Fetch todo with row-level security
        todo = await self.get_todo_by_id(session, user_id, todo_id)
        if not todo:
            return False

        await session.delete(todo)
        await session.commit()

        return True


# Create singleton instance
todo_service = TodoService()
