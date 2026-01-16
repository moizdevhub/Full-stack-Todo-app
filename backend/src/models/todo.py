from uuid import UUID, uuid4
from datetime import datetime, date
from sqlmodel import Field, SQLModel, Relationship
from typing import Optional, TYPE_CHECKING, List
from enum import Enum

if TYPE_CHECKING:
    from .user import User
    from .tag import Tag, TodoTag
else:
    # Import TodoTag for runtime use in Relationship
    from .tag import TodoTag


class Priority(str, Enum):
    """Priority levels for todos."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class Todo(SQLModel, table=True):
    """Todo item entity with user ownership and completion tracking.

    Attributes:
        id: Unique todo identifier (UUID v4)
        user_id: Foreign key to users table (owner of this todo)
        title: Todo title (required, max 500 characters)
        description: Optional detailed description (max 5000 characters)
        completed: Completion status (false = incomplete, true = complete)
        priority: Priority level (low, medium, high)
        due_date: Optional due date for the todo
        created_at: Todo creation timestamp (UTC)
        updated_at: Last update timestamp (UTC)
        user: Relationship to owning user (lazy-loaded)
        tags: Relationship to associated tags (many-to-many)
    """
    __tablename__ = "todos"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: UUID = Field(foreign_key="users.id", nullable=False, index=True)
    title: str = Field(max_length=500, nullable=False)
    description: Optional[str] = Field(default=None, max_length=5000)
    completed: bool = Field(default=False, nullable=False)
    priority: str = Field(default=Priority.MEDIUM.value, nullable=False)
    due_date: Optional[date] = Field(default=None)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)

    # Relationships
    user: "User" = Relationship(back_populates="todos")
    tags: List["Tag"] = Relationship(back_populates="todos", link_model=TodoTag)


class TodoCreate(SQLModel):
    """Schema for todo creation request (user_id from JWT, not request body).

    Attributes:
        title: Todo title (required, max 500 characters)
        description: Optional detailed description (max 5000 characters)
        priority: Priority level (low, medium, high)
        due_date: Optional due date
        tag_ids: Optional list of tag IDs to associate with this todo
    """
    title: str = Field(min_length=1, max_length=500)
    description: Optional[str] = Field(default=None, max_length=5000)
    priority: Optional[str] = Field(default=Priority.MEDIUM.value)
    due_date: Optional[date] = Field(default=None)
    tag_ids: Optional[List[UUID]] = Field(default=None)


class TodoUpdate(SQLModel):
    """Schema for todo update request (partial updates allowed).

    Attributes:
        title: Optional new title (max 500 characters)
        description: Optional new description (max 5000 characters)
        completed: Optional new completion status
        priority: Optional new priority level
        due_date: Optional new due date
        tag_ids: Optional list of tag IDs to replace existing tags
    """
    title: Optional[str] = Field(default=None, min_length=1, max_length=500)
    description: Optional[str] = Field(default=None, max_length=5000)
    completed: Optional[bool] = Field(default=None)
    priority: Optional[str] = Field(default=None)
    due_date: Optional[date] = Field(default=None)
    tag_ids: Optional[List[UUID]] = Field(default=None)


class TodoRead(SQLModel):
    """Schema for todo data in API responses.

    Attributes:
        id: Unique todo identifier
        user_id: Owner's user identifier
        title: Todo title
        description: Optional description
        completed: Completion status
        priority: Priority level
        due_date: Optional due date
        created_at: Creation timestamp
        updated_at: Last update timestamp
        tags: List of associated tags
    """
    id: UUID
    user_id: UUID
    title: str
    description: Optional[str]
    completed: bool
    priority: str
    due_date: Optional[date]
    created_at: datetime
    updated_at: datetime
    tags: Optional[List[dict]] = None  # Will be populated with tag data


class TodoListResponse(SQLModel):
    """Schema for paginated todo list response.

    Attributes:
        todos: List of todos for current page
        total: Total number of todos matching filters
        page: Current page number
        page_size: Number of items per page
        total_pages: Total number of pages
    """
    todos: list[TodoRead]
    total: int
    page: int
    page_size: int
    total_pages: int
