from uuid import UUID, uuid4
from datetime import datetime
from sqlmodel import Field, SQLModel, Relationship
from typing import Optional, TYPE_CHECKING, List

if TYPE_CHECKING:
    from .user import User
    from .todo import Todo


class TodoTag(SQLModel, table=True):
    """Many-to-many relationship between todos and tags.

    Attributes:
        todo_id: Foreign key to todos table
        tag_id: Foreign key to tags table
        created_at: Relationship creation timestamp (UTC)
    """
    __tablename__ = "todo_tags"

    todo_id: UUID = Field(foreign_key="todos.id", primary_key=True)
    tag_id: UUID = Field(foreign_key="tags.id", primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)


class Tag(SQLModel, table=True):
    """Tag entity for categorizing todos.

    Attributes:
        id: Unique tag identifier (UUID v4)
        user_id: Foreign key to users table (owner of this tag)
        name: Tag name (required, max 50 characters)
        color: Hex color code for tag display (e.g., #FF5733)
        created_at: Tag creation timestamp (UTC)
    """
    __tablename__ = "tags"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: UUID = Field(foreign_key="users.id", nullable=False, index=True)
    name: str = Field(max_length=50, nullable=False)
    color: str = Field(max_length=7, default="#3B82F6")  # Default blue
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)

    # Relationships
    user: "User" = Relationship(back_populates="tags")
    todos: List["Todo"] = Relationship(back_populates="tags", link_model=TodoTag)


class TagCreate(SQLModel):
    """Schema for tag creation request.

    Attributes:
        name: Tag name (required, max 50 characters)
        color: Optional hex color code (defaults to blue)
    """
    name: str = Field(min_length=1, max_length=50)
    color: Optional[str] = Field(default="#3B82F6", max_length=7)


class TagUpdate(SQLModel):
    """Schema for tag update request.

    Attributes:
        name: Optional new tag name
        color: Optional new color
    """
    name: Optional[str] = Field(default=None, min_length=1, max_length=50)
    color: Optional[str] = Field(default=None, max_length=7)


class TagRead(SQLModel):
    """Schema for tag data in API responses.

    Attributes:
        id: Unique tag identifier
        user_id: Owner's user identifier
        name: Tag name
        color: Hex color code
        created_at: Creation timestamp
    """
    id: UUID
    user_id: UUID
    name: str
    color: str
    created_at: datetime
