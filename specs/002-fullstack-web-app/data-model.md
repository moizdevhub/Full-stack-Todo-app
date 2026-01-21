# Data Model and Database Schema

**Feature**: Full-Stack Web Todo Application
**Branch**: `002-fullstack-web-app`
**Date**: 2026-01-07
**Database**: Neon PostgreSQL

## Overview

This document defines the database schema, entity models, and data relationships for the full-stack web todo application. The schema supports multi-user authentication with row-level data isolation as required by Constitution Section VIII.2.

## Entity-Relationship Diagram

```
┌─────────────────────────────────┐
│          User                    │
│─────────────────────────────────│
│ id: UUID (PK)                   │
│ email: VARCHAR(255) UNIQUE      │
│ hashed_password: VARCHAR(255)   │
│ created_at: TIMESTAMP           │
└─────────────────────────────────┘
              │ 1
              │
              │ owns
              │
              │ *
┌─────────────────────────────────┐
│          Todo                    │
│─────────────────────────────────│
│ id: UUID (PK)                   │
│ user_id: UUID (FK → User)       │
│ title: VARCHAR(500) NOT NULL    │
│ description: TEXT                │
│ completed: BOOLEAN              │
│ created_at: TIMESTAMP           │
│ updated_at: TIMESTAMP           │
└─────────────────────────────────┘
```

**Relationship**: One User has many Todos (1:N)
**Cascade**: DELETE User → CASCADE DELETE all associated Todos

## Database Schema

### Table: `users`

Stores authenticated user accounts.

```sql
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

-- Indexes for performance
CREATE UNIQUE INDEX idx_users_email ON users(email);

-- Comments for documentation
COMMENT ON TABLE users IS 'Authenticated user accounts for the todo application';
COMMENT ON COLUMN users.id IS 'Unique user identifier (UUID v4)';
COMMENT ON COLUMN users.email IS 'User email address (unique, used for login)';
COMMENT ON COLUMN users.hashed_password IS 'Argon2 hashed password (never plaintext)';
COMMENT ON COLUMN users.created_at IS 'Account creation timestamp (UTC)';
```

**Constraints**:
- `id`: PRIMARY KEY, UUID v4, auto-generated via `gen_random_uuid()`
- `email`: UNIQUE, NOT NULL, indexed for fast login lookups
- `hashed_password`: NOT NULL, stored using Argon2 hashing algorithm
- `created_at`: NOT NULL, defaults to current timestamp (UTC)

**Validation Rules** (enforced at application level):
- Email: Valid email format (RFC 5322 regex)
- Email: Maximum 255 characters
- Password (plaintext, before hashing): Minimum 8 characters, at least one uppercase, one lowercase, one number

**Security Notes**:
- Passwords are NEVER stored in plaintext
- Password hashing uses Argon2 with time_cost=2, memory_cost=512MB, parallelism=2
- Email uniqueness prevents duplicate account creation
- No soft deletes (hard delete only)

---

### Table: `todos`

Stores todo items with user ownership.

```sql
CREATE TABLE todos (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    title VARCHAR(500) NOT NULL,
    description TEXT,
    completed BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);

-- Indexes for performance
CREATE INDEX idx_todos_user_id ON todos(user_id);
CREATE INDEX idx_todos_created_at ON todos(created_at);
CREATE INDEX idx_todos_user_created ON todos(user_id, created_at DESC);

-- Comments for documentation
COMMENT ON TABLE todos IS 'Todo items owned by users with row-level isolation';
COMMENT ON COLUMN todos.id IS 'Unique todo identifier (UUID v4)';
COMMENT ON COLUMN todos.user_id IS 'Foreign key to users table (owner of this todo)';
COMMENT ON COLUMN todos.title IS 'Todo title (required, max 500 characters)';
COMMENT ON COLUMN todos.description IS 'Optional detailed description (max 5000 characters)';
COMMENT ON COLUMN todos.completed IS 'Completion status (false = incomplete, true = complete)';
COMMENT ON COLUMN todos.created_at IS 'Todo creation timestamp (UTC)';
COMMENT ON COLUMN todos.updated_at IS 'Last update timestamp (UTC, auto-updated)';
```

**Constraints**:
- `id`: PRIMARY KEY, UUID v4, auto-generated via `gen_random_uuid()`
- `user_id`: FOREIGN KEY REFERENCES users(id) ON DELETE CASCADE, NOT NULL, indexed
- `title`: NOT NULL, VARCHAR(500) (enforces max length)
- `description`: TEXT (nullable, no max length in schema but enforced at app level as 5000 chars)
- `completed`: NOT NULL, defaults to FALSE
- `created_at`: NOT NULL, defaults to current timestamp (UTC)
- `updated_at`: NOT NULL, defaults to current timestamp (UTC), auto-updated on modification

**Validation Rules** (enforced at application level):
- Title: Required, non-empty after trimming whitespace
- Title: Maximum 500 characters
- Description: Optional, maximum 5000 characters
- user_id: Must reference an existing user UUID

**Security Notes**:
- **Row-Level Security**: ALL queries MUST filter by `user_id` from authenticated JWT (Constitution VIII.2)
- ON DELETE CASCADE: Deleting a user automatically deletes all their todos (prevents orphaned records)
- No user can access another user's todos (enforced at application level, not database triggers)

**Indexing Strategy**:
- `idx_todos_user_id`: Fast filtering by user (all queries filtered by user_id)
- `idx_todos_created_at`: Fast sorting by creation date
- `idx_todos_user_created`: Composite index for combined user filtering + date sorting (optimal for default list view)

---

## SQLModel Entity Definitions

### Backend: `models/user.py`

```python
from uuid import UUID, uuid4
from datetime import datetime
from sqlmodel import Field, SQLModel, Relationship
from typing import Optional


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
    todos: list["Todo"] = Relationship(back_populates="user", cascade_delete=True)

    class Config:
        json_schema_extra = {
            "example": {
                "id": "550e8400-e29b-41d4-a716-446655440000",
                "email": "user@example.com",
                "created_at": "2026-01-07T12:34:56.789Z"
            }
        }


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
```

---

### Backend: `models/todo.py`

```python
from uuid import UUID, uuid4
from datetime import datetime
from sqlmodel import Field, SQLModel, Relationship
from typing import Optional


class Todo(SQLModel, table=True):
    """Todo item entity with user ownership and completion tracking.

    Attributes:
        id: Unique todo identifier (UUID v4)
        user_id: Foreign key to users table (owner of this todo)
        title: Todo title (required, max 500 characters)
        description: Optional detailed description (max 5000 characters)
        completed: Completion status (false = incomplete, true = complete)
        created_at: Todo creation timestamp (UTC)
        updated_at: Last update timestamp (UTC)
        user: Relationship to owning user (lazy-loaded)
    """
    __tablename__ = "todos"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: UUID = Field(foreign_key="users.id", nullable=False, index=True)
    title: str = Field(max_length=500, nullable=False)
    description: Optional[str] = Field(default=None, max_length=5000)
    completed: bool = Field(default=False, nullable=False)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)

    # Relationships
    user: User = Relationship(back_populates="todos")

    class Config:
        json_schema_extra = {
            "example": {
                "id": "660e8400-e29b-41d4-a716-446655440001",
                "user_id": "550e8400-e29b-41d4-a716-446655440000",
                "title": "Finish implementation plan",
                "description": "Complete data-model.md, contracts/, and quickstart.md",
                "completed": false,
                "created_at": "2026-01-07T12:34:56.789Z",
                "updated_at": "2026-01-07T12:34:56.789Z"
            }
        }


class TodoCreate(SQLModel):
    """Schema for todo creation request (user_id from JWT, not request body).

    Attributes:
        title: Todo title (required, max 500 characters)
        description: Optional detailed description (max 5000 characters)
    """
    title: str = Field(min_length=1, max_length=500)
    description: Optional[str] = Field(default=None, max_length=5000)


class TodoUpdate(SQLModel):
    """Schema for todo update request (partial updates allowed).

    Attributes:
        title: Optional new title (max 500 characters)
        description: Optional new description (max 5000 characters)
        completed: Optional new completion status
    """
    title: Optional[str] = Field(default=None, min_length=1, max_length=500)
    description: Optional[str] = Field(default=None, max_length=5000)
    completed: Optional[bool] = Field(default=None)


class TodoRead(SQLModel):
    """Schema for todo data in API responses.

    Attributes:
        id: Unique todo identifier
        user_id: Owner's user identifier
        title: Todo title
        description: Optional description
        completed: Completion status
        created_at: Creation timestamp
        updated_at: Last update timestamp
    """
    id: UUID
    user_id: UUID
    title: str
    description: Optional[str]
    completed: bool
    created_at: datetime
    updated_at: datetime
```

---

## TypeScript Type Definitions

### Frontend: `types/user.ts`

```typescript
/**
 * User entity type (matches backend UserRead schema)
 */
export interface User {
  id: string; // UUID
  email: string;
  created_at: string; // ISO 8601 timestamp
}

/**
 * User registration request payload
 */
export interface UserCreateRequest {
  email: string;
  password: string; // Plaintext (sent over HTTPS, hashed on backend)
}

/**
 * User login request payload
 */
export interface UserLoginRequest {
  email: string;
  password: string;
}

/**
 * Authentication response (JWT token + user data)
 */
export interface AuthResponse {
  access_token: string; // JWT token
  token_type: "bearer";
  user: User;
}
```

---

### Frontend: `types/todo.ts`

```typescript
/**
 * Todo entity type (matches backend TodoRead schema)
 */
export interface Todo {
  id: string; // UUID
  user_id: string; // UUID
  title: string;
  description: string | null;
  completed: boolean;
  created_at: string; // ISO 8601 timestamp
  updated_at: string; // ISO 8601 timestamp
}

/**
 * Todo creation request payload
 */
export interface TodoCreateRequest {
  title: string;
  description?: string | null;
}

/**
 * Todo update request payload (partial updates allowed)
 */
export interface TodoUpdateRequest {
  title?: string;
  description?: string | null;
  completed?: boolean;
}

/**
 * Todo list response
 */
export interface TodoListResponse {
  todos: Todo[];
  total: number;
}
```

---

## Data Validation Rules

### Email Validation

**Frontend Validation**:
```typescript
const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
const isValidEmail = (email: string): boolean => emailRegex.test(email);
```

**Backend Validation** (Pydantic):
```python
from pydantic import EmailStr

class UserCreate(SQLModel):
    email: EmailStr  # Automatic email validation
    password: str
```

**Rules**:
- Must match RFC 5322 email format
- Maximum 255 characters
- Case-insensitive for uniqueness check

---

### Password Validation

**Frontend Validation**:
```typescript
const passwordRegex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{8,}$/;
const isValidPassword = (password: string): boolean => passwordRegex.test(password);
```

**Backend Validation** (custom validator):
```python
import re

def validate_password(password: str) -> None:
    """Validate password meets security requirements."""
    if len(password) < 8:
        raise ValueError("Password must be at least 8 characters")
    if not re.search(r"[a-z]", password):
        raise ValueError("Password must contain at least one lowercase letter")
    if not re.search(r"[A-Z]", password):
        raise ValueError("Password must contain at least one uppercase letter")
    if not re.search(r"\d", password):
        raise ValueError("Password must contain at least one number")
```

**Rules**:
- Minimum 8 characters
- At least one lowercase letter (a-z)
- At least one uppercase letter (A-Z)
- At least one digit (0-9)
- No maximum length (hashed on backend)

---

### Todo Title Validation

**Frontend Validation**:
```typescript
const isValidTitle = (title: string): boolean => {
  const trimmed = title.trim();
  return trimmed.length > 0 && trimmed.length <= 500;
};
```

**Backend Validation** (Pydantic):
```python
from pydantic import field_validator

class TodoCreate(SQLModel):
    title: str = Field(min_length=1, max_length=500)

    @field_validator("title")
    def validate_title(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Title cannot be empty or whitespace only")
        return v.strip()
```

**Rules**:
- Required (not nullable)
- Minimum 1 character (after trimming whitespace)
- Maximum 500 characters
- Automatically trimmed of leading/trailing whitespace

---

### Todo Description Validation

**Frontend Validation**:
```typescript
const isValidDescription = (description: string | null): boolean => {
  if (description === null || description === "") return true;
  return description.length <= 5000;
};
```

**Backend Validation** (Pydantic):
```python
from typing import Optional

class TodoCreate(SQLModel):
    description: Optional[str] = Field(default=None, max_length=5000)
```

**Rules**:
- Optional (nullable)
- Maximum 5000 characters if provided
- Stored as TEXT in database (no hard limit at DB level)
- Empty string converted to NULL

---

## Data Migration Strategy

### Initial Schema Migration

**Migration File**: `backend/alembic/versions/20260107_1430_create_users_and_todos.py`

```python
"""Create users and todos tables

Revision ID: 001_initial_schema
Revises:
Create Date: 2026-01-07 14:30:00.000000
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID

# revision identifiers, used by Alembic.
revision = '001_initial_schema'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create users table
    op.create_table(
        'users',
        sa.Column('id', UUID(as_uuid=True), primary_key=True, server_default=sa.text('gen_random_uuid()')),
        sa.Column('email', sa.String(255), nullable=False, unique=True),
        sa.Column('hashed_password', sa.String(255), nullable=False),
        sa.Column('created_at', sa.TIMESTAMP, nullable=False, server_default=sa.func.now())
    )
    op.create_index('idx_users_email', 'users', ['email'], unique=True)

    # Create todos table
    op.create_table(
        'todos',
        sa.Column('id', UUID(as_uuid=True), primary_key=True, server_default=sa.text('gen_random_uuid()')),
        sa.Column('user_id', UUID(as_uuid=True), nullable=False),
        sa.Column('title', sa.String(500), nullable=False),
        sa.Column('description', sa.Text, nullable=True),
        sa.Column('completed', sa.Boolean, nullable=False, server_default=sa.false()),
        sa.Column('created_at', sa.TIMESTAMP, nullable=False, server_default=sa.func.now()),
        sa.Column('updated_at', sa.TIMESTAMP, nullable=False, server_default=sa.func.now()),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE')
    )
    op.create_index('idx_todos_user_id', 'todos', ['user_id'])
    op.create_index('idx_todos_created_at', 'todos', ['created_at'])
    op.create_index('idx_todos_user_created', 'todos', ['user_id', 'created_at'], postgresql_ops={'created_at': 'DESC'})


def downgrade() -> None:
    op.drop_index('idx_todos_user_created', table_name='todos')
    op.drop_index('idx_todos_created_at', table_name='todos')
    op.drop_index('idx_todos_user_id', table_name='todos')
    op.drop_table('todos')

    op.drop_index('idx_users_email', table_name='users')
    op.drop_table('users')
```

**Migration Execution**:
```bash
# Local testing
alembic upgrade head

# Render deployment (automatic via render-build.sh)
uv sync && alembic upgrade head

# Rollback if needed
alembic downgrade -1
```

---

### Future Schema Migrations

**Guidelines for future migrations** (Constitution VIII.8):
- All migrations MUST be idempotent (safe to run multiple times)
- All migrations MUST include both `upgrade()` and `downgrade()` functions
- All migrations MUST be tested on Neon branch databases before production
- Migration naming: `YYYYMMDD_HHMM_descriptive_name.py`
- Use `alembic revision --autogenerate` to detect schema changes
- Always review auto-generated migrations for correctness

**Potential future migrations**:
- Add `updated_at` trigger for automatic timestamp updates
- Add `deleted_at` column for soft deletes (if required)
- Add `priority` column for todo prioritization (if required)
- Add `due_date` column for deadline tracking (if required)
- Add full-text search index on `title` and `description` (if required)

---

## Query Patterns and Performance

### Row-Level Security Enforcement (Constitution VIII.2)

**ALL queries MUST filter by authenticated user_id**:

```python
# CORRECT: Filtered by user_id from JWT
async def get_user_todos(db: AsyncSession, user_id: UUID) -> list[Todo]:
    result = await db.execute(
        select(Todo).where(Todo.user_id == user_id).order_by(Todo.created_at.desc())
    )
    return result.scalars().all()

# INCORRECT: No user_id filter (security violation)
async def get_all_todos(db: AsyncSession) -> list[Todo]:
    result = await db.execute(select(Todo))
    return result.scalars().all()
```

**Enforcement mechanisms**:
- JWT middleware extracts `user_id` from token `sub` claim
- All service functions accept `user_id: UUID` parameter
- All queries include `.where(Todo.user_id == user_id)`
- Code review checklist validates user_id filtering
- Integration tests verify cross-user data isolation

---

### Optimized Query Patterns

**1. List todos (default view: newest first)**:
```python
# Uses idx_todos_user_created composite index
result = await db.execute(
    select(Todo)
    .where(Todo.user_id == user_id)
    .order_by(Todo.created_at.desc())
)
todos = result.scalars().all()
```

**2. Filter by completion status**:
```python
# Filtered by user_id + completed status
result = await db.execute(
    select(Todo)
    .where(Todo.user_id == user_id, Todo.completed == False)
    .order_by(Todo.created_at.desc())
)
incomplete_todos = result.scalars().all()
```

**3. Get single todo by ID**:
```python
# Filtered by user_id + todo_id (prevents cross-user access)
result = await db.execute(
    select(Todo)
    .where(Todo.id == todo_id, Todo.user_id == user_id)
)
todo = result.scalar_one_or_none()
if not todo:
    raise HTTPException(status_code=404, detail="Todo not found")
```

**4. Count user's todos**:
```python
# Uses idx_todos_user_id index
result = await db.execute(
    select(func.count(Todo.id)).where(Todo.user_id == user_id)
)
count = result.scalar()
```

**Performance targets**:
- GET /todos: p95 < 200ms (with 1000 todos)
- POST /todos: p95 < 150ms
- PUT /todos/:id: p95 < 150ms
- DELETE /todos/:id: p95 < 100ms

---

## Sample Data

### Development Seed Data

**Users**:
```json
[
  {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "email": "demo@example.com",
    "hashed_password": "$argon2id$v=19$m=65536,t=2,p=2$...",
    "created_at": "2026-01-07T12:00:00Z"
  },
  {
    "id": "660e8400-e29b-41d4-a716-446655440001",
    "email": "test@example.com",
    "hashed_password": "$argon2id$v=19$m=65536,t=2,p=2$...",
    "created_at": "2026-01-07T12:05:00Z"
  }
]
```

**Todos**:
```json
[
  {
    "id": "770e8400-e29b-41d4-a716-446655440010",
    "user_id": "550e8400-e29b-41d4-a716-446655440000",
    "title": "Complete implementation plan",
    "description": "Finish data-model.md, contracts/, and quickstart.md",
    "completed": false,
    "created_at": "2026-01-07T12:30:00Z",
    "updated_at": "2026-01-07T12:30:00Z"
  },
  {
    "id": "880e8400-e29b-41d4-a716-446655440011",
    "user_id": "550e8400-e29b-41d4-a716-446655440000",
    "title": "Write Playwright E2E tests",
    "description": null,
    "completed": true,
    "created_at": "2026-01-07T12:35:00Z",
    "updated_at": "2026-01-07T13:00:00Z"
  }
]
```

**Seed script** (for development):
```python
# backend/scripts/seed_dev_data.py
import asyncio
from uuid import UUID
from datetime import datetime
from sqlmodel import select
from passlib.hash import argon2
from app.database import engine, get_session
from app.models import User, Todo

async def seed_dev_data():
    async with get_session() as db:
        # Create demo users
        demo_user = User(
            id=UUID("550e8400-e29b-41d4-a716-446655440000"),
            email="demo@example.com",
            hashed_password=argon2.hash("DemoPassword123"),
            created_at=datetime(2026, 1, 7, 12, 0, 0)
        )
        db.add(demo_user)

        # Create sample todos
        todo1 = Todo(
            id=UUID("770e8400-e29b-41d4-a716-446655440010"),
            user_id=demo_user.id,
            title="Complete implementation plan",
            description="Finish data-model.md, contracts/, and quickstart.md",
            completed=False,
            created_at=datetime(2026, 1, 7, 12, 30, 0),
            updated_at=datetime(2026, 1, 7, 12, 30, 0)
        )
        db.add(todo1)

        await db.commit()
        print("Dev data seeded successfully")

if __name__ == "__main__":
    asyncio.run(seed_dev_data())
```

---

## Summary

**Entities**:
- `User`: Authentication accounts with email/password
- `Todo`: Task items with user ownership and completion tracking

**Relationships**:
- User → Todos: One-to-Many (1:N) with CASCADE DELETE

**Security**:
- Row-level filtering by `user_id` from JWT (Constitution VIII.2)
- Password hashing with Argon2 (never plaintext)
- UUID primary keys (prevents enumeration attacks)

**Performance**:
- Composite index `(user_id, created_at)` for default list view
- Foreign key index on `user_id` for fast joins
- Connection pooling for concurrent requests

**Compliance**:
- Type safety: SQLModel + Pydantic for backend, TypeScript strict for frontend (Constitution VIII.6)
- Migration hygiene: Alembic with upgrade/downgrade functions (Constitution VIII.8)
- Validation: Pydantic schemas enforce data constraints (Constitution VIII.5)

**Next Steps**:
- Create `contracts/api.openapi.yaml` with OpenAPI specification
- Create `quickstart.md` with setup and development instructions
- Fill `plan.md` with complete implementation plan
