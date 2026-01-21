from uuid import UUID, uuid4
from datetime import datetime
from sqlmodel import Field, SQLModel, Relationship
from typing import Optional, TYPE_CHECKING, List

if TYPE_CHECKING:
    from .todo import Todo
    from .tag import Tag


class User(SQLModel, table=True):
    """User account entity for authentication and todo ownership.

    Attributes:
        id: Unique user identifier (UUID v4)
        email: User email address (unique, indexed, used for login)
        hashed_password: Argon2 hashed password (never plaintext)
        created_at: Account creation timestamp (UTC)
        todos: Relationship to user's todos (lazy-loaded)
    """
    __tablename__ = "users"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    email: str = Field(max_length=255, unique=True, index=True, nullable=False)
    hashed_password: str = Field(max_length=255, nullable=False)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)

    # Relationships
    todos: List["Todo"] = Relationship(back_populates="user", cascade_delete=True)
    tags: List["Tag"] = Relationship(back_populates="user", cascade_delete=True)


class UserCreate(SQLModel):
    """Schema for user registration request.

    Attributes:
        email: User email address (validated at application level)
        password: Plaintext password (will be hashed before storage)
    """
    email: str = Field(max_length=255)
    password: str = Field(min_length=8)


class UserRead(SQLModel):
    """Schema for user data in API responses (excludes hashed_password).

    Attributes:
        id: Unique user identifier
        email: User email address
        created_at: Account creation timestamp
    """
    id: UUID
    email: str
    created_at: datetime


class UserLogin(SQLModel):
    """Schema for user login request.

    Attributes:
        email: User email address
        password: Plaintext password (verified against hashed_password)
    """
    email: str
    password: str
