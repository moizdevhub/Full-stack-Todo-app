# Implementation Plan: Full-Stack Web Todo Application

**Branch**: `002-fullstack-web-app` | **Date**: 2026-01-08 | **Spec**: spec.md
**Input**: Feature specification from `/specs/002-fullstack-web-app/spec.md`

## Summary

Transform the CLI Todo App into a production-ready full-stack web application with Next.js frontend, FastAPI backend, Neon PostgreSQL database, Better Auth JWT authentication, comprehensive testing (80%+ coverage + Playwright E2E), and multi-phase deployment to Vercel and Render. The application will provide secure user authentication, complete CRUD operations for todos with data isolation, responsive UI, and performance optimization.

## Technical Context

**Language/Version**: Python 3.11+ for backend, TypeScript/JavaScript for Next.js frontend
**Primary Dependencies**: Next.js 14+, FastAPI 0.100+, Better Auth, SQLModel, Neon PostgreSQL, Playwright, pytest
**Storage**: Neon PostgreSQL (serverless PostgreSQL) with SQLModel ORM
**Testing**: pytest with 80%+ coverage, Playwright for E2E testing, mypy for Python type checking, TypeScript strict mode
**Target Platform**: Web application (Vercel frontend, Render backend)
**Project Type**: Web (frontend + backend)
**Performance Goals**: <500ms p95 API response time, <3s initial page load on 3G, 60fps UI rendering
**Constraints**: <200ms p95 for 1000+ concurrent users, JWT-based auth, data isolation between users
**Scale/Scope**: 1000+ concurrent users, 1000+ todos per user, zero-downtime deployments

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- Authentication & Authorization: JWT validation at all network boundaries (Section VIII.1)
- Data Segregation: All queries filtered by authenticated user UUID (Section VIII.2)
- Secrets Management: Secrets only in environment variables (Section VIII.3)
- API Stability: Versioned API routes with backward compatibility (Section VIII.4)
- Code Quality: TypeScript strict mode, Python type hints with mypy strict, 80%+ test coverage
- Database Hygiene: Alembic migrations with both upgrade() and downgrade() functions
- Testing Gates: All tests must pass in CI/CD before deployment

## Project Structure

### Documentation (this feature)

```text
specs/002-fullstack-web-app/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
backend/
├── main.py
├── requirements.txt
├── alembic/
│   ├── versions/
│   ├── env.py
│   └── script.py.mako
├── src/
│   ├── models/
│   │   ├── user.py
│   │   └── todo.py
│   ├── services/
│   │   ├── auth.py
│   │   └── todo_service.py
│   ├── api/
│   │   ├── auth.py
│   │   └── todos.py
│   └── database/
│       └── session.py
└── tests/
    ├── unit/
    ├── integration/
    └── conftest.py

frontend/
├── package.json
├── tsconfig.json
├── next.config.js
├── src/
│   ├── app/
│   │   ├── (auth)/
│   │   │   ├── login/
│   │   │   └── register/
│   │   ├── dashboard/
│   │   ├── api/
│   │   └── layout.tsx
│   ├── components/
│   │   ├── auth/
│   │   ├── todos/
│   │   └── ui/
│   ├── hooks/
│   ├── services/
│   └── types/
├── public/
└── tests/
    └── e2e/
        └── todo.spec.ts

docker-compose.yml
README.md
CLAUDE.md
```

**Structure Decision**: Web application with separate backend (FastAPI) and frontend (Next.js) directories following Option 2 structure. This allows independent deployment to Render (backend) and Vercel (frontend) while maintaining clear separation of concerns.

## Phase 1: Backend Development

### 1.1 Set up FastAPI Project
- Initialize FastAPI project with uv package management
- Configure dependencies in pyproject.toml
- Set up project structure with models, services, and API layers
- Implement Python type hints and mypy configuration

### 1.2 Implement SQLModel Database Models
- Create User model with UUID, email, hashed password, timestamps
- Create Todo model with UUID, user_id (foreign key), title, description, status, timestamps
- Define relationships between User and Todo models
- Implement proper indexing on user_id and created_at columns

### 1.3 Configure Neon PostgreSQL and Alembic Migrations
- Set up Neon PostgreSQL connection with connection pooling
- Configure Alembic for database schema migrations
- Create initial migration with both upgrade() and downgrade() functions
- Implement automatic migration execution during deployment

### 1.4 Implement JWT Authentication with Better Auth
- Set up Better Auth for JWT token management
- Create authentication middleware for FastAPI
- Implement user registration with email validation and password hashing (bcrypt)
- Implement login, logout, and token refresh functionality
- Create protected routes with JWT validation

### 1.5 Develop API Endpoints with Row-Level Security
- Create RESTful API endpoints following convention: `/api/v1/todos`
- Implement POST /api/v1/todos - Create new todo
- Implement GET /api/v1/todos - Retrieve user's todos with filtering and sorting
- Implement PUT /api/v1/todos/{id} - Update todo
- Implement PATCH /api/v1/todos/{id}/status - Update todo status
- Implement DELETE /api/v1/todos/{id} - Delete todo
- Implement health check endpoint at `/api/health`
- Enforce row-level security by validating user_id on all queries

### 1.6 Implement Data Validation and Security
- Validate all input fields (title max 500 chars, description max 5000 chars)
- Implement XSS prevention by sanitizing user inputs
- Use parameterized queries through SQLModel to prevent SQL injection
- Implement proper error handling with standardized JSON responses
- Return appropriate HTTP status codes (400, 401, 403, 404, 500)

### 1.7 Set up Testing Framework
- Configure pytest for backend testing
- Implement unit tests for models and services
- Create integration tests for API endpoints
- Achieve minimum 80% code coverage using pytest-cov
- Set up CI/CD pipeline to run tests before deployment

## Phase 2: Frontend Development

### 2.1 Set up Next.js 14+ Project with TypeScript
- Initialize Next.js project with App Router
- Configure TypeScript strict mode
- Set up Tailwind CSS for styling
- Implement proper project structure with components, hooks, and services

### 2.2 Implement Authentication UI and State Management
- Create login and registration forms with validation
- Implement JWT token handling with secure storage
- Create authentication context for global state management
- Implement protected routes and session persistence
- Handle token expiration and refresh automatically

### 2.3 Develop Todo CRUD UI Components
- Create TodoList component to display todos with filtering and sorting
- Create TodoForm component for creating and editing todos
- Create TodoItem component with status toggle and delete functionality
- Implement empty state and loading indicators
- Add confirmation modal for todo deletion

### 2.4 Implement Responsive and Accessible UI
- Create responsive layout for mobile, tablet, and desktop
- Implement keyboard navigation with proper focus indicators
- Add ARIA labels and roles for screen reader support
- Ensure WCAG 2.1 AA compliance with proper color contrast
- Implement virtual scrolling for large todo lists

### 2.5 Integrate with Backend API
- Create API service layer for HTTP requests
- Implement error handling and user feedback
- Add optimistic UI updates for better user experience
- Implement proper loading states and error boundaries
- Handle network failures gracefully

### 2.6 Implement Frontend Testing
- Set up Playwright for E2E testing
- Create tests covering all user flows: registration, login, CRUD operations, logout
- Implement UI component testing
- Set up CI/CD pipeline for automated testing

## Phase 3: Performance and Security Optimization

### 3.1 Database Performance Optimization
- Review and optimize database indexes
- Implement efficient queries with proper filtering
- Set up connection pooling for concurrent requests
- Optimize query performance for large todo lists (1000+ items)

### 3.2 API Performance Optimization
- Implement caching strategies where appropriate
- Optimize API response times for p95 <500ms
- Set up rate limiting (100 requests per minute per user)
- Implement proper CORS configuration for Vercel frontend

### 3.3 Security Hardening
- Implement CSRF protection for state-changing operations
- Ensure all secrets are loaded from environment variables only
- Validate JWT tokens on every request
- Implement proper input sanitization to prevent XSS and SQL injection
- Set up error logging with full context for debugging

## Phase 4: Deployment and Monitoring

### 4.1 Set up CI/CD Pipeline
- Configure GitHub Actions for automated testing
- Set up automatic deployments on Git push to main branch
- Implement deployment validation and rollback mechanisms
- Block deployments on test failures

### 4.2 Deploy to Production
- Deploy Next.js frontend to Vercel with automatic deployments
- Deploy FastAPI backend to Render with automatic deployments
- Configure environment variables for both platforms
- Set up custom domains and SSL certificates

### 4.3 Implement Monitoring and Health Checks
- Set up health check endpoint for monitoring
- Implement error logging and monitoring (e.g., Sentry)
- Configure performance monitoring
- Set up uptime monitoring and alerts

### 4.4 Zero-Downtime Deployment Strategy
- Implement rolling updates for zero-downtime deployments
- Set up automatic database migrations during deployment
- Configure proper health checks to validate deployments
- Implement automatic rollback on deployment failures

## Functional Requirements Implementation

### Authentication & Authorization (FR-001 to FR-008)
- User registration with email validation and password requirements
- JWT-based login with symmetric signing
- JWT validation on all endpoints
- User ID extraction from JWT for database queries
- 401 Unauthorized responses for invalid tokens
- Session persistence across page refreshes
- Data isolation between users

### Todo CRUD Operations (FR-009 to FR-020)
- Create todos with UUID, title, description, and status
- Retrieve user's todos with filtering and sorting
- Update todo details with validation
- Toggle todo status between complete/incomplete
- Delete todos with confirmation
- Proper error responses for non-existent or unauthorized access

### Data Validation & Integrity (FR-021 to FR-026)
- Input validation for all fields
- XSS prevention through input sanitization
- SQL injection prevention through ORM
- Foreign key constraints
- Email validation during registration
- Password hashing with bcrypt

### Error Handling (FR-027 to FR-030)
- Standardized JSON error responses
- No exposed stack traces in production
- Server-side error logging
- Appropriate HTTP status codes

### API Design (FR-031 to FR-035)
- RESTful API endpoints with versioning
- CORS configuration for Vercel frontend
- Rate limiting implementation
- Proper Content-Type headers

### Testing & Quality (FR-036 to FR-040)
- 80%+ backend code coverage
- Playwright E2E tests for all flows
- TypeScript strict mode
- Python type hints with mypy strict
- CI/CD test validation

### Database & Migrations (FR-041 to FR-044)
- Alembic migration system
- Proper indexing strategy
- Neon PostgreSQL connection pooling
- Idempotent migrations

### Security (FR-045 to FR-047)
- Environment variable management
- HTTPS enforcement
- CSRF protection

### Deployment (FR-048 to FR-052)
- Vercel frontend deployment
- Render backend deployment
- Health check endpoint
- Zero-downtime deployments
- Automatic migration execution

## Success Criteria Implementation

### Functional Success (SC-001 to SC-005)
- Complete authentication flow with JWT handling
- Full CRUD operations with data persistence
- Proper data isolation between users
- Form validation with clear error messages
- Filtering and sorting functionality

### Performance Success (SC-006 to SC-009)
- <3s initial page load on 3G
- <500ms p95 API response time under load
- Smooth rendering for 1000+ items
- Optimistic UI updates

### Security Success (SC-010 to SC-013)
- No hardcoded secrets
- JWT validation on all endpoints
- User data isolation
- XSS and SQL injection protection

### Testing Success (SC-014 to SC-017)
- 80%+ backend coverage
- Complete Playwright E2E test suite
- TypeScript strict mode compliance
- Python mypy strict compliance

### Deployment Success (SC-018 to SC-021)
- Automated CI/CD pipeline
- Working health checks
- Zero-downtime deployments
- Successful migration execution

### Accessibility Success (SC-022 to SC-024)
- WCAG 2.1 AA compliance
- Keyboard navigation support
- Screen reader compatibility

## Edge Cases to Address

- JWT token expiration during active session
- Concurrent edits to the same todo in multiple tabs
- Database connection loss during API requests
- High-volume todo creation (10,000+ todos)
- Network failures between frontend and backend
- Malformed JWT tokens
- XSS payload attempts in todo fields
- PostgreSQL connection limits
- Rapid button clicking
- SQL injection attempts
- Non-existent route handling
- Missing environment variables

## Complexity Tracking

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| Two separate projects | Frontend and backend require different deployment platforms and technologies | Single project would complicate deployment and tech stack management |
| JWT with Better Auth | Industry standard for stateless authentication | Session-based auth would require server-side session storage |
| SQLModel ORM | Type-safe database queries with Pydantic integration | Raw SQL would lack type safety and require more manual validation |
| Alembic migrations | Proper database schema version control | Manual schema management would be error-prone and difficult to maintain |
