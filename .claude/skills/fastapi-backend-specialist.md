---
name: "fastapi-backend-specialist"
description: "Architect high-performance, uv-powered, async Python APIs. Use when the user needs to build JWT-secured backends, SQLModel/SQLAlchemy schemas, or high-concurrency endpoints with 100% test coverage."
version: "1.0.0"
---

# FastAPI Backend Specialist Skill

## When to Use This Skill

- User needs to design a scalable, **async-first** Python backend.
- User requires a migration from legacy Python managers (pip/poetry) to **uv**.
- User needs to implement **JWT-based authentication** or OAuth2 scopes.
- User is defining database architectures using **SQLModel** or SQLAlchemy 2.x.
- User demands high performance (p95 < 200ms) and comprehensive **Pytest** suites.

## How This Skill Works

1.  **Strict Typing**: Every function signature must have Python 3.12+ type hints; Pydantic models are mandatory for all I/O.
2.  **Async Enforcement**: Audit all database and network calls to ensure no blocking code (`time.sleep`, synchronous requests) hits the event loop.
3.  **Secure Middleware**: Implement JWT decoding and permission checks at the dependency or middleware level before hitting the route logic.
4.  **Database Integrity**: Use Alembic for versioned migrations and implement Row-Level Security (RLS) within SQL queries.
5.  **Test-Driven Development**: Every endpoint must be accompanied by a Pytest unit test, an integration test, and a performance benchmark.

## Output Format

Provide:
- **API Implementation**: Async FastAPI routes with typed dependencies.
- **Data Models**: Pydantic schemas (Request/Response) and SQLModel entities.
- **Testing Suite**: Pytest snippets covering success and edge cases (401, 422).
- **Performance Spec**: Estimated RPS and memory footprint for the proposed solution.

## Quality Criteria

An API is "Production-Ready" when:
- **Coverage**: 100% Pytest coverage reported.
- **Speed**: p95 response time is < 200ms under simulated load.
- **Security**: 401/403 errors are handled gracefully; no sensitive data leaks in 5xx errors.
- **Efficiency**: Dependency management is handled via `uv` for lightning-fast builds.

## Example

**Input**: "Create a POST endpoint to register a user. Use SQLModel, asyncpg, and hash passwords with Passlib."

**Output**:
- **Pydantic Schema**: `UserCreate` with email validation.
- **Logic**: Async function hashing the password before database insertion.
- **Security**: Dependency-based password validation and unique constraint handling.
- **Test**: A test case ensuring the password is never returned in the JSON response.