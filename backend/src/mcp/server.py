"""FastMCP server for stateless task operations."""

import os
from datetime import datetime
from typing import Any, Dict, List, Literal, Optional

from mcp.server import Server
from mcp.server.stdio import stdio_server
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from ..models.task import Task
from ..services.database import async_session_maker


# Initialize MCP server
server = Server("todo-mcp-server")


async def get_db_session() -> AsyncSession:
    """Get database session for MCP tools."""
    return async_session_maker()


@server.tool()
async def add_task(
    user_id: str, title: str, description: Optional[str] = None
) -> Dict[str, Any]:
    """
    Create a new task for the user.

    Args:
        user_id: User UUID from JWT sub claim (required for data isolation)
        title: Task title or description (1-200 characters)
        description: Optional additional details about the task (max 2000 characters)

    Returns:
        Dict containing task_id, title, description, completed, and created_at

    Raises:
        ValueError: If title is empty or too long
    """
    # Validate inputs
    if not title or not title.strip():
        raise ValueError("Task title cannot be empty")

    if len(title) > 200:
        raise ValueError("Task title must be 200 characters or less")

    if description and len(description) > 2000:
        raise ValueError("Task description must be 2000 characters or less")

    # Create task in database
    async with await get_db_session() as session:
        task = Task(
            user_id=user_id,
            title=title.strip(),
            description=description.strip() if description else None,
        )
        session.add(task)
        await session.commit()
        await session.refresh(task)

        return {
            "task_id": task.id,
            "title": task.title,
            "description": task.description,
            "completed": task.completed,
            "created_at": task.created_at.isoformat(),
        }


@server.tool()
async def list_tasks(
    user_id: str, status: Literal["all", "pending", "completed"] = "all"
) -> Dict[str, Any]:
    """
    Retrieve tasks for the user with optional filtering by completion status.

    Args:
        user_id: User UUID from JWT sub claim (required for data isolation)
        status: Filter tasks by completion status (all, pending, or completed)

    Returns:
        Dict containing tasks list, total count, and status_filter applied
    """
    async with await get_db_session() as session:
        # Build query with user_id filter
        query = select(Task).where(Task.user_id == user_id)

        # Apply status filter
        if status == "pending":
            query = query.where(Task.completed == False)
        elif status == "completed":
            query = query.where(Task.completed == True)

        # Order by creation date (newest first)
        query = query.order_by(Task.created_at.desc())

        # Execute query
        result = await session.execute(query)
        tasks = result.scalars().all()

        # Format response
        return {
            "tasks": [
                {
                    "task_id": task.id,
                    "title": task.title,
                    "description": task.description,
                    "completed": task.completed,
                    "created_at": task.created_at.isoformat(),
                    "updated_at": task.updated_at.isoformat(),
                }
                for task in tasks
            ],
            "total": len(tasks),
            "status_filter": status,
        }


@server.tool()
async def complete_task(user_id: str, task_id: int) -> Dict[str, Any]:
    """
    Mark a task as completed.

    Args:
        user_id: User UUID from JWT sub claim (required for data isolation)
        task_id: ID of the task to mark as completed

    Returns:
        Dict containing task_id, title, completed status, and updated_at

    Raises:
        ValueError: If task not found or does not belong to user
    """
    async with await get_db_session() as session:
        # Fetch task with ownership verification
        task = await session.get(Task, task_id)

        if not task or task.user_id != user_id:
            raise ValueError("Task not found or does not belong to user")

        # Mark as completed
        task.completed = True
        task.updated_at = datetime.utcnow()

        await session.commit()
        await session.refresh(task)

        return {
            "task_id": task.id,
            "title": task.title,
            "completed": task.completed,
            "updated_at": task.updated_at.isoformat(),
        }


@server.tool()
async def delete_task(user_id: str, task_id: int) -> Dict[str, Any]:
    """
    Permanently delete a task.

    Args:
        user_id: User UUID from JWT sub claim (required for data isolation)
        task_id: ID of the task to delete

    Returns:
        Dict containing task_id and deleted status

    Raises:
        ValueError: If task not found or does not belong to user
    """
    async with await get_db_session() as session:
        # Fetch task with ownership verification
        task = await session.get(Task, task_id)

        if not task or task.user_id != user_id:
            raise ValueError("Task not found or does not belong to user")

        # Delete task
        await session.delete(task)
        await session.commit()

        return {"task_id": task_id, "deleted": True}


@server.tool()
async def update_task(
    user_id: str,
    task_id: int,
    title: Optional[str] = None,
    description: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Update an existing task's title or description.

    Args:
        user_id: User UUID from JWT sub claim (required for data isolation)
        task_id: ID of the task to update
        title: New task title (optional)
        description: New task description (optional, null to clear)

    Returns:
        Dict containing task_id, title, description, completed, and updated_at

    Raises:
        ValueError: If task not found, does not belong to user, or no fields provided
    """
    # Validate at least one field is provided
    if title is None and description is None:
        raise ValueError("At least one field (title or description) must be provided")

    async with await get_db_session() as session:
        # Fetch task with ownership verification
        task = await session.get(Task, task_id)

        if not task or task.user_id != user_id:
            raise ValueError("Task not found or does not belong to user")

        # Update fields
        if title is not None:
            if not title.strip():
                raise ValueError("Task title cannot be empty")
            if len(title) > 200:
                raise ValueError("Task title must be 200 characters or less")
            task.title = title.strip()

        if description is not None:
            if description and len(description) > 2000:
                raise ValueError("Task description must be 2000 characters or less")
            task.description = description.strip() if description else None

        task.updated_at = datetime.utcnow()

        await session.commit()
        await session.refresh(task)

        return {
            "task_id": task.id,
            "title": task.title,
            "description": task.description,
            "completed": task.completed,
            "updated_at": task.updated_at.isoformat(),
        }


# Server entry point
async def run_mcp_server():
    """Run the MCP server."""
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream)
