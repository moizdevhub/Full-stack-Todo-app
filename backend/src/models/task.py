"""Task SQLModel for todo items."""

from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel


class Task(SQLModel, table=True):
    """Task model representing a todo item belonging to a specific user."""

    __tablename__ = "tasks"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(index=True, nullable=False, description="User UUID from JWT sub claim")
    title: str = Field(max_length=200, nullable=False, description="Task title/description")
    description: Optional[str] = Field(
        default=None, max_length=2000, description="Additional task details"
    )
    completed: bool = Field(default=False, description="Task completion status")
    created_at: datetime = Field(
        default_factory=datetime.utcnow, description="Timestamp when task was created"
    )
    updated_at: datetime = Field(
        default_factory=datetime.utcnow, description="Timestamp when task was last modified"
    )

    class Config:
        """Pydantic configuration."""

        json_schema_extra = {
            "example": {
                "user_id": "550e8400-e29b-41d4-a716-446655440000",
                "title": "Buy groceries",
                "description": "Milk, eggs, bread",
                "completed": False,
            }
        }
