# Phase 0: Research and Technical Investigation

**Feature**: Full-Stack Web Todo Application
**Branch**: `002-fullstack-web-app`
**Date**: 2026-01-07

## Research Objectives

This document captures technical investigations, best practices, and architecture decisions to inform the implementation plan for transforming the CLI todo application into a production-ready full-stack web application.

## 1. Frontend Stack Research (Next.js 16 + TypeScript)

### 1.1 Next.js 16 App Router Architecture

**Investigation**: Next.js 16 with App Router provides:
- **Server Components by default**: Reduces client-side JavaScript bundle size
- **Route Handlers**: Native API routes in `app/api/` for BFF patterns (not used; direct FastAPI calls preferred)
- **Server Actions**: Form handling with progressive enhancement
- **Streaming SSR**: Faster initial page loads with Suspense boundaries
- **Layouts and Templates**: Shared UI patterns across routes

**Decision for this project**:
- Use **Client Components** for interactive todo CRUD UI (marked with `"use client"`)
- Leverage **Server Components** for static marketing pages (landing, about)
- Implement **API client abstraction** (`lib/api.ts`) to call FastAPI backend
- Use **React Query** or **SWR** for data fetching, caching, and optimistic updates
- Avoid Next.js API routes (Route Handlers) to maintain clean frontend/backend separation

**References**:
- Next.js 16 App Router documentation
- Server Components vs Client Components patterns
- Best practices for external API integration

### 1.2 Better Auth JWT Integration

**Investigation**: Better Auth is a modern authentication library for Next.js:
- **JWT-based authentication**: Stateless, scalable, API-friendly
- **Symmetric signing**: Uses shared secret (HS256) for signing/verification
- **Token storage**: Supports HTTP-only cookies (XSS protection) or localStorage (convenience)
- **Token refresh**: Automatic refresh flow when access token expires
- **Session persistence**: Validates JWT on page load to maintain session

**Decision for this project**:
- Use **Better Auth client SDK** in Next.js for login/register forms
- Store JWT in **HTTP-only cookies** (preferred) or localStorage (fallback)
- Extract JWT from cookies/storage and send as `Authorization: Bearer <token>` to FastAPI
- Implement **automatic logout** on 401 Unauthorized responses
- Better Auth handles JWT signing; FastAPI validates with shared secret

**Security considerations**:
- Shared secret MUST be loaded from environment variables (Vercel: `JWT_SECRET`, Render: `JWT_SECRET`)
- Secrets rotation requires simultaneous deployment to both platforms
- HTTPS enforcement prevents MITM attacks on JWT transmission
- Token expiration set to 24 hours (configurable via environment variable)

**References**:
- Better Auth documentation and examples
- JWT best practices (OWASP guidelines)
- Next.js authentication patterns

### 1.3 Tailwind CSS Responsive Design

**Investigation**: Tailwind CSS provides utility-first styling:
- **Responsive breakpoints**: `sm:`, `md:`, `lg:`, `xl:`, `2xl:` modifiers
- **Mobile-first design**: Default styles for small screens, scale up
- **Dark mode support**: `dark:` modifier (future enhancement)
- **Component libraries**: shadcn/ui, Headless UI for accessible components

**Decision for this project**:
- Use **Tailwind utility classes** for all styling (no custom CSS files)
- Implement **mobile-first responsive design**: 320px (mobile) → 768px (tablet) → 1920px (desktop)
- Use **Headless UI** or **Radix UI** for accessible modal dialogs and form controls
- Focus on **WCAG 2.1 AA compliance**: color contrast, keyboard navigation, ARIA labels

**Layout breakpoints**:
- Mobile (320px-767px): Single column, stacked todos, hamburger menu
- Tablet (768px-1023px): Two-column grid, expanded todos
- Desktop (1024px+): Three-column layout, sidebar navigation

**References**:
- Tailwind CSS responsive design documentation
- WCAG 2.1 accessibility guidelines
- shadcn/ui component library

### 1.4 Playwright E2E Testing Strategy

**Investigation**: Playwright provides cross-browser E2E testing:
- **Multi-browser support**: Chromium, Firefox, WebKit
- **Parallel execution**: Faster test runs with workers
- **Trace recording**: Visual debugging of test failures
- **Network interception**: Mock API responses for isolated tests
- **Accessibility testing**: Integrated axe-core for a11y audits

**Decision for this project**:
- Write **E2E tests in TypeScript** in `frontend/e2e/` directory
- Test **critical user flows**: registration → login → create todo → complete todo → delete todo → logout
- Use **Page Object Model (POM)**: Separate page interactions from test logic
- Run tests against **local dev environment** (localhost) and **staging environment** (Vercel preview)
- Integrate with **CI/CD pipeline**: Block merges on E2E test failures

**Test coverage**:
- Authentication: Register, login, logout, session persistence
- Todo CRUD: Create, read, update, delete, status toggle
- Filtering/Sorting: Filter by status, sort by creation date
- Error handling: Invalid inputs, network failures, expired tokens
- Accessibility: Keyboard navigation, screen reader announcements

**References**:
- Playwright documentation and examples
- Page Object Model pattern
- E2E testing best practices

## 2. Backend Stack Research (FastAPI + Python)

### 2.1 FastAPI Architecture and Middleware

**Investigation**: FastAPI provides high-performance async API development:
- **Async/await support**: Non-blocking I/O for database queries
- **Pydantic v2 validation**: Automatic request/response validation
- **OpenAPI generation**: Auto-generated API documentation at `/docs`
- **Dependency injection**: Reusable dependencies for auth, database sessions
- **Middleware system**: CORS, JWT validation, request logging

**Decision for this project**:
- Use **FastAPI 0.115+** with Pydantic v2 for type safety and validation
- Implement **JWT middleware** using `fastapi.security.HTTPBearer` dependency
- Structure code with **domain-driven design**: `api/` (routes), `services/` (business logic), `models/` (database entities)
- Use **async route handlers** for all endpoints (database I/O is async)
- Enable **CORS middleware** allowing requests from Vercel frontend domain

**Middleware stack** (execution order):
1. CORS middleware (allow Vercel domain)
2. Request logging middleware (log all requests with user ID)
3. JWT validation middleware (extract and validate token)
4. Rate limiting middleware (100 requests/minute per user)
5. Error handling middleware (transform exceptions to standardized JSON errors)

**References**:
- FastAPI documentation and best practices
- FastAPI security and authentication patterns
- Async Python performance optimization

### 2.2 SQLModel ORM and Type Safety

**Investigation**: SQLModel combines SQLAlchemy and Pydantic:
- **Type-safe queries**: Python type hints for database queries
- **Pydantic validation**: Automatic validation of database models
- **Relationship management**: Foreign keys and joins
- **Session management**: Async session support with context managers
- **Migration compatibility**: Works seamlessly with Alembic

**Decision for this project**:
- Define **SQLModel classes** for `User` and `Todo` entities
- Use **async session** for all database queries
- Implement **relationship definitions**: `User.todos` (one-to-many), `Todo.user` (many-to-one)
- Separate **database models** (SQLModel) from **API schemas** (Pydantic)
- Enforce **user_id filtering** at query level (all queries include `WHERE user_id = ?`)

**Model structure**:
```python
# models/user.py
class User(SQLModel, table=True):
    id: UUID
    email: str (unique, indexed)
    hashed_password: str
    created_at: datetime

# models/todo.py
class Todo(SQLModel, table=True):
    id: UUID
    user_id: UUID (foreign key to User, indexed)
    title: str (max 500 chars)
    description: str | None (max 5000 chars)
    completed: bool (default False)
    created_at: datetime (indexed)
    updated_at: datetime
```

**References**:
- SQLModel documentation and examples
- SQLAlchemy async patterns
- Type-safe database query patterns

### 2.3 Alembic Migrations with Neon PostgreSQL

**Investigation**: Alembic provides database version control:
- **Migration scripts**: Replayable `upgrade()` and `downgrade()` functions
- **Auto-generation**: Detect schema changes and generate migrations
- **Neon compatibility**: Works with Neon's serverless PostgreSQL
- **Connection pooling**: Manages concurrent connections

**Decision for this project**:
- Use **Alembic 1.13+** for all schema migrations
- Store migrations in `backend/alembic/versions/` directory
- Naming convention: `YYYYMMDD_HHMM_descriptive_name.py` (e.g., `20260107_1430_create_users_and_todos.py`)
- Run migrations **automatically on Render deployment** via startup script
- Test migrations on **Neon branch databases** before production deployment

**Migration workflow**:
1. Modify SQLModel classes
2. Run `alembic revision --autogenerate -m "description"`
3. Review generated migration for correctness
4. Test migration on local PostgreSQL or Neon branch
5. Commit migration file to Git
6. Deploy to Render (migrations run automatically)

**Neon-specific considerations**:
- Use **Neon's connection string** with SSL required
- Enable **connection pooling** (PgBouncer or SQLAlchemy pool)
- Use **Neon branches** for preview deployments (staging, testing)
- Monitor **connection limits** (Neon free tier: 100 connections)

**References**:
- Alembic documentation and best practices
- Neon PostgreSQL documentation
- Database migration strategies

### 2.4 pytest and Coverage Requirements

**Investigation**: pytest provides powerful testing capabilities:
- **Fixtures**: Reusable test dependencies (database, client, auth tokens)
- **Async support**: `pytest-asyncio` for testing async code
- **Coverage reporting**: `pytest-cov` for line coverage metrics
- **Parameterization**: Test multiple inputs with `@pytest.mark.parametrize`
- **Mocking**: `unittest.mock` for external dependencies

**Decision for this project**:
- Achieve **minimum 80% line coverage** for backend code
- Write **unit tests** for services, utilities, validators
- Write **integration tests** for API endpoints with real database (test DB)
- Use **pytest fixtures** for test database, authenticated client, sample data
- Run tests in **CI/CD pipeline** and block merges on failures

**Test structure**:
```
backend/tests/
├── conftest.py (fixtures: test_db, client, auth_token)
├── unit/
│   ├── test_services.py
│   ├── test_validators.py
│   └── test_utils.py
└── integration/
    ├── test_auth_endpoints.py
    ├── test_todo_endpoints.py
    └── test_edge_cases.py
```

**Coverage exclusions**:
- Migration scripts (Alembic versions)
- Configuration files (settings.py)
- Entry point scripts (main.py)
- Development-only code (debug routes)

**References**:
- pytest documentation and examples
- pytest-asyncio for async testing
- pytest-cov for coverage reporting

## 3. Database Design (Neon PostgreSQL)

### 3.1 Schema Design and Normalization

**Investigation**: PostgreSQL best practices for multi-tenant applications:
- **UUID primary keys**: Globally unique, not sequential (prevents enumeration attacks)
- **Indexed foreign keys**: Fast joins on `user_id`
- **Timestamps**: Track creation and modification times
- **Data types**: Use appropriate types (VARCHAR vs TEXT, BOOLEAN vs INT)

**Decision for this project**:
- Use **UUID v4** for all primary keys (not auto-increment integers)
- Create **indexes** on: `users.email`, `todos.user_id`, `todos.created_at`
- Use **ON DELETE CASCADE** for `todos.user_id` foreign key (delete todos when user deleted)
- Store **timestamps in UTC** (converted to local time on frontend)
- Use **VARCHAR(500)** for titles, **TEXT** for descriptions

**Schema**:
```sql
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_users_email ON users(email);

CREATE TABLE todos (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    title VARCHAR(500) NOT NULL,
    description TEXT,
    completed BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_todos_user_id ON todos(user_id);
CREATE INDEX idx_todos_created_at ON todos(created_at);
```

**References**:
- PostgreSQL UUID generation
- Database indexing strategies
- Multi-tenant database design

### 3.2 Performance Optimization

**Investigation**: Query optimization for todo list application:
- **Row-level filtering**: All queries filtered by `user_id` from JWT
- **Pagination**: Limit results to 100 todos per page (future enhancement)
- **Connection pooling**: Reuse database connections
- **Query caching**: Cache frequent queries (e.g., todo count)

**Decision for this project**:
- Enforce **user_id filtering** at application level (SQLModel queries)
- Add **composite index** on `(user_id, created_at)` for sorted queries
- Use **connection pooling** (SQLAlchemy default pool size: 20)
- Implement **query timeout** (5 seconds max per query)
- Monitor **slow query log** on Neon dashboard

**Performance targets**:
- GET /todos: p95 < 200ms (with 1000 todos)
- POST /todos: p95 < 150ms
- PUT /todos/:id: p95 < 150ms
- DELETE /todos/:id: p95 < 100ms

**References**:
- PostgreSQL query optimization
- Database connection pooling
- Performance monitoring strategies

## 4. Authentication and Authorization

### 4.1 JWT Token Structure

**Investigation**: JWT token payload design:
- **Standard claims**: `sub` (user ID), `iat` (issued at), `exp` (expiration)
- **Custom claims**: `email` (for display), `role` (future: admin/user)
- **Token lifespan**: 24 hours (balance security and user convenience)
- **Signing algorithm**: HS256 (symmetric secret) for simplicity

**Decision for this project**:
```json
{
  "sub": "550e8400-e29b-41d4-a716-446655440000",
  "email": "user@example.com",
  "iat": 1735632000,
  "exp": 1735718400
}
```

- Use **sub claim** for user UUID (validated on every request)
- Store **email** in token for UI display (avoid extra database query)
- Set **exp** to 24 hours from issue time
- Sign with **HS256** using shared secret from environment variable

**Token refresh strategy**:
- Issue new token when current token has < 2 hours remaining
- Transparent refresh via frontend API client (no user action required)
- Logout on refresh failure (forces re-authentication)

**References**:
- JWT.io documentation
- JWT best practices (OWASP)
- Token refresh patterns

### 4.2 Password Hashing

**Investigation**: Secure password storage:
- **bcrypt**: Industry standard, adaptive cost factor (future-proof)
- **argon2**: Modern, winner of Password Hashing Competition
- **scrypt**: Memory-hard, resistant to hardware attacks

**Decision for this project**:
- Use **argon2** via `passlib` library (recommended for new projects)
- Configure **cost parameters**: time_cost=2, memory_cost=512MB, parallelism=2
- Verify password on login using constant-time comparison
- Never log or transmit plaintext passwords

**Implementation**:
```python
from passlib.hash import argon2

# Registration
hashed = argon2.hash("user_password")

# Login
is_valid = argon2.verify("user_password", hashed)
```

**References**:
- passlib documentation
- OWASP password storage guidelines
- Argon2 parameter recommendations

## 5. Deployment and DevOps

### 5.1 Vercel Frontend Deployment

**Investigation**: Vercel deployment for Next.js:
- **Automatic deployments**: Triggered by Git push to main branch
- **Preview deployments**: Created for pull requests
- **Environment variables**: Managed via Vercel dashboard
- **Edge network**: Global CDN for fast page loads
- **Build caching**: Faster deployments with incremental builds

**Decision for this project**:
- Deploy **production build** to Vercel on merge to main
- Create **preview deployments** for all PRs (automated testing)
- Set environment variables: `NEXT_PUBLIC_API_URL` (FastAPI backend URL), `JWT_SECRET` (shared secret)
- Enable **automatic HTTPS** (Vercel default)
- Configure **custom domain** (optional future enhancement)

**Build configuration** (vercel.json):
```json
{
  "framework": "nextjs",
  "buildCommand": "npm run build",
  "outputDirectory": ".next",
  "installCommand": "npm install"
}
```

**References**:
- Vercel deployment documentation
- Next.js deployment best practices
- Environment variable management

### 5.2 Render Backend Deployment

**Investigation**: Render deployment for FastAPI:
- **Automatic deployments**: Triggered by Git push to main branch
- **Environment variables**: Managed via Render dashboard
- **Health checks**: Monitor `/api/health` endpoint
- **Auto-scaling**: Scale based on CPU/memory usage (paid plans)
- **Zero-downtime deployments**: Rolling updates with health checks

**Decision for this project**:
- Deploy **FastAPI backend** as Render Web Service
- Set environment variables: `DATABASE_URL` (Neon connection string), `JWT_SECRET` (shared secret), `CORS_ORIGINS` (Vercel domain)
- Configure **health check endpoint**: `/api/health` returns 200 OK
- Run **Alembic migrations** on startup via `render-build.sh` script
- Use **UV package manager** for dependency installation

**Render configuration** (render.yaml):
```yaml
services:
  - type: web
    name: todo-api
    runtime: python
    buildCommand: uv sync && alembic upgrade head
    startCommand: uvicorn main:app --host 0.0.0.0 --port $PORT
    envVars:
      - key: DATABASE_URL
        sync: false
      - key: JWT_SECRET
        sync: false
      - key: CORS_ORIGINS
        value: https://todo-app.vercel.app
```

**References**:
- Render deployment documentation
- FastAPI production deployment
- Zero-downtime deployment strategies

### 5.3 CI/CD Pipeline

**Investigation**: GitHub Actions for CI/CD:
- **Automated testing**: Run tests on every push and PR
- **Type checking**: Run `tsc` and `mypy` to catch type errors
- **Linting**: Run ESLint (frontend) and Ruff (backend)
- **Coverage reporting**: Upload coverage to Codecov
- **Deployment**: Automatic deployment on merge to main

**Decision for this project**:
- Create **GitHub Actions workflows** in `.github/workflows/`
- Run **frontend tests** (Playwright E2E) and **backend tests** (pytest)
- Block **PR merges** on test failures or coverage drops below 80%
- Run **type checkers** (TypeScript strict, mypy strict)
- Deploy **automatically** to Vercel and Render on merge to main

**Workflow structure**:
```yaml
# .github/workflows/test.yml
name: Test and Deploy

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  frontend-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
      - run: npm install
      - run: npm run type-check
      - run: npm run lint
      - run: npx playwright test

  backend-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
      - run: uv sync
      - run: mypy --strict src/
      - run: pytest --cov=src --cov-report=xml
      - run: uv run coverage report --fail-under=80
```

**References**:
- GitHub Actions documentation
- CI/CD best practices
- Coverage reporting with Codecov

## 6. Security Considerations

### 6.1 OWASP Top 10 Mitigation

**Investigation**: Common web application vulnerabilities:
1. **Broken Access Control**: Validate user_id on every request
2. **Cryptographic Failures**: Use HTTPS, hash passwords, secure JWT secrets
3. **Injection**: Use parameterized queries (SQLModel ORM)
4. **Insecure Design**: Implement rate limiting, input validation
5. **Security Misconfiguration**: No debug mode in production, secure CORS
6. **Vulnerable Components**: Regular dependency updates via Dependabot
7. **Authentication Failures**: Strong password policy, JWT expiration
8. **Data Integrity Failures**: Validate all inputs with Pydantic
9. **Logging Failures**: Log all security events (auth failures, data access)
10. **SSRF**: No user-controlled URLs (N/A for this app)

**Decision for this project**:
- Implement **row-level security**: All queries filtered by authenticated user_id
- Enforce **HTTPS** on Vercel and Render (automatic)
- Use **parameterized queries** exclusively (SQLModel ORM)
- Validate **all inputs** with Pydantic schemas
- Implement **rate limiting**: 100 requests/minute per user
- Enable **dependency scanning** via Dependabot and Snyk
- Log **security events**: failed logins, token validation failures, unauthorized access attempts

**References**:
- OWASP Top 10 2021
- Web application security best practices
- FastAPI security guidelines

### 6.2 XSS and CSRF Protection

**Investigation**: Cross-site scripting and CSRF attacks:
- **XSS**: Inject malicious JavaScript into pages
- **CSRF**: Trick users into performing unwanted actions

**Decision for this project**:
- **XSS prevention**: React automatically escapes HTML (JSX), validate and sanitize user inputs on backend
- **CSRF prevention**: Use JWT tokens in Authorization header (not cookies), implement SameSite cookie attribute if using cookies
- **Content Security Policy (CSP)**: Set headers to restrict inline scripts (future enhancement)

**Implementation**:
- Backend: Validate and sanitize all user inputs (titles, descriptions)
- Frontend: Never use `dangerouslySetInnerHTML` without sanitization
- HTTP headers: Set `X-Content-Type-Options: nosniff`, `X-Frame-Options: DENY`

**References**:
- OWASP XSS prevention cheat sheet
- OWASP CSRF prevention cheat sheet
- Content Security Policy guide

## 7. Testing Strategy

### 7.1 Test Pyramid

**Investigation**: Balance between unit, integration, and E2E tests:
- **Unit tests (70%)**: Fast, isolated, test individual functions/classes
- **Integration tests (20%)**: Test API endpoints with real database
- **E2E tests (10%)**: Test user flows in real browser

**Decision for this project**:
- **Backend unit tests**: Test services, validators, utilities (target: 80%+ coverage)
- **Backend integration tests**: Test API endpoints with test database (all CRUD operations)
- **Frontend E2E tests**: Test critical user flows with Playwright (registration, login, CRUD, logout)
- **Frontend component tests**: Test React components with React Testing Library (future enhancement)

**Test distribution** (target):
- Backend unit tests: ~150 tests (70% of backend tests)
- Backend integration tests: ~40 tests (20% of backend tests)
- Frontend E2E tests: ~20 tests (10% of all tests)

**References**:
- Test pyramid pattern
- Testing best practices
- Playwright vs Cypress comparison

### 7.2 Load Testing

**Investigation**: Verify performance under high concurrency:
- **k6**: Modern load testing tool with JavaScript-based test scripts
- **Locust**: Python-based load testing framework
- **Apache JMeter**: Java-based load testing tool

**Decision for this project**:
- Use **k6** for load testing (aligns with modern JavaScript tooling)
- Test **API endpoints** under 1000 concurrent users
- Verify **p95 latency** < 500ms for all CRUD operations
- Test **database connection pooling** under high load
- Run **load tests** before production launch

**Load test scenarios**:
1. **Ramp-up test**: Gradually increase from 0 to 1000 users over 10 minutes
2. **Stress test**: Sudden spike to 1000 users, maintain for 5 minutes
3. **Endurance test**: 100 concurrent users for 1 hour (detect memory leaks)
4. **Spike test**: 100 users → 1000 users → 100 users (test auto-scaling)

**References**:
- k6 documentation and examples
- Load testing best practices
- Performance benchmarking strategies

## 8. Monitoring and Observability

### 8.1 Logging Strategy

**Investigation**: Structured logging for production applications:
- **Python**: structlog or loguru for structured JSON logs
- **Next.js**: pino or winston for server-side logging
- **Log aggregation**: Send logs to centralized service (Datadog, Sentry, LogRocket)

**Decision for this project**:
- Use **Python logging** with JSON formatter for FastAPI
- Log **request metadata**: user_id, request_id, endpoint, method, status_code, duration
- Log **security events**: auth failures, unauthorized access, rate limit exceeded
- Log **errors** with full stack traces and context
- Send logs to **Render logs** (built-in) or **external service** (future enhancement)

**Log levels**:
- DEBUG: Development only (disable in production)
- INFO: Normal operations (user login, todo created)
- WARNING: Recoverable errors (rate limit approaching, slow query)
- ERROR: Unrecoverable errors (database connection failed, invalid JWT)
- CRITICAL: System failures (database down, service unavailable)

**References**:
- Structured logging best practices
- Python logging configuration
- FastAPI logging patterns

### 8.2 Error Monitoring

**Investigation**: Real-time error tracking and alerting:
- **Sentry**: Error tracking with stack traces, user context, release tracking
- **Datadog**: Full-stack monitoring (logs, metrics, traces, errors)
- **Rollbar**: Error tracking with deployment tracking

**Decision for this project**:
- Use **Sentry** for error monitoring (free tier sufficient for MVP)
- Track **frontend errors**: Unhandled exceptions, API failures, console errors
- Track **backend errors**: Unhandled exceptions, validation errors, database errors
- Configure **error alerts**: Notify via Slack/email on critical errors
- Tag errors with **release version** and **environment** (production, staging)

**Sentry integration**:
- Frontend: Install `@sentry/nextjs`, configure in `sentry.client.config.js`
- Backend: Install `sentry-sdk`, configure in FastAPI app initialization
- Environment variables: `SENTRY_DSN` (Data Source Name)

**References**:
- Sentry documentation and setup
- Error monitoring best practices
- Alerting strategies

## 9. Phase-Based Development Strategy

### 9.1 Phase Breakdown

**Phase 1: Frontend Foundation (Next.jsFrontendArchitect + Next.jsFrontendSpecialist)**
- Scaffold Next.js 16 project with TypeScript strict mode and Tailwind CSS
- Implement Better Auth JWT authentication (login, register, logout)
- Create 6 CRUD views: Dashboard, Create Todo, Edit Todo, Todo List, Todo Detail, Login/Register
- Write Playwright E2E tests for all user flows
- Commit with Git tag: `phase-frontend`

**Phase 2: Backend Foundation (FastAPIBackendArchitect + FastAPIBackendSpecialist)**
- Scaffold FastAPI project with UV package manager
- Implement SQLModel entities (User, Todo) and Alembic migrations
- Create 6 API endpoints: POST /auth/register, POST /auth/login, GET /todos, POST /todos, PUT /todos/:id, DELETE /todos/:id
- Implement JWT middleware and row-level user filtering
- Write pytest unit and integration tests (80%+ coverage)
- Commit with Git tag: `phase-backend`

**Phase 3: Database Performance (DatabasePerformanceSpecialist)**
- Review database indexes and query performance
- Run k6 load tests to verify p95 < 200ms latency
- Optimize slow queries and add composite indexes if needed
- Push performance tuning PR

**Phase 4: Full-Stack Integration (FullStackIntegrationSpecialist)**
- Wire Next.js frontend to FastAPI backend
- Configure CORS headers for Vercel domain
- Implement token refresh logic on frontend
- Run full Playwright E2E tests against integrated stack
- Push integration PR

**Phase 5: Production Deployment (DevOpsInfrastructureEngineer)**
- Deploy Next.js frontend to Vercel with environment variables
- Deploy FastAPI backend to Render with environment variables
- Set up Neon PostgreSQL database with migrations
- Configure secrets rotation and monitoring
- Add README badges (build status, coverage, deployment status)
- Tag release: `v1.0.0`
- Record demo video

### 9.2 Agent Coordination

**Agent handoffs**:
1. **architecture-planner** creates plan.md → hands off to **implementation-executor**
2. **implementation-executor** completes Phase 1 (frontend) → hands off to **implementation-executor** (backend)
3. **implementation-executor** completes Phase 2 (backend) → hands off to **code-quality-validator**
4. **code-quality-validator** reviews code → hands off to **DatabasePerformanceSpecialist** agent
5. **DatabasePerformanceSpecialist** optimizes performance → hands off to **FullStackIntegrationSpecialist** agent
6. **FullStackIntegrationSpecialist** wires frontend/backend → hands off to **DevOpsInfrastructureEngineer** agent
7. **DevOpsInfrastructureEngineer** deploys to production → hands off to **documentation-maintainer**

**Parallelization opportunities**:
- Phase 1 (frontend) and Phase 2 (backend) can be developed in parallel (shared API contract)
- Playwright E2E tests can be written in parallel with backend development
- Load testing can start as soon as backend endpoints are functional

**References**:
- Agile development best practices
- Team coordination strategies
- Phased rollout patterns

## 10. Risks and Mitigations

### 10.1 Technical Risks

**Risk 1: Better Auth JWT integration complexity**
- **Likelihood**: Medium
- **Impact**: High (blocks authentication)
- **Mitigation**: Start with Better Auth quickstart example, test JWT flow early, have fallback plan (custom JWT implementation)

**Risk 2: Neon PostgreSQL connection limits on free tier**
- **Likelihood**: Medium
- **Impact**: Medium (performance degradation under load)
- **Mitigation**: Use connection pooling, monitor connection usage, upgrade to paid plan if needed

**Risk 3: Playwright E2E test flakiness**
- **Likelihood**: High
- **Impact**: Low (CI/CD delays)
- **Mitigation**: Use explicit waits, increase timeouts, retry failed tests, run in headed mode for debugging

**Risk 4: Cross-origin authentication issues (CORS, cookies)**
- **Likelihood**: Medium
- **Impact**: High (authentication breaks)
- **Mitigation**: Test CORS early, use Authorization header instead of cookies if needed, configure SameSite attributes

**Risk 5: Database migration failures in production**
- **Likelihood**: Low
- **Impact**: Critical (production downtime)
- **Mitigation**: Test migrations on Neon branch databases, implement automatic rollback on failure, have manual rollback procedure

### 10.2 Process Risks

**Risk 1: Scope creep (adding features not in spec)**
- **Likelihood**: Medium
- **Impact**: High (delays launch)
- **Mitigation**: Strict adherence to spec, mark enhancements as "future", defer non-critical features

**Risk 2: Section VIII compliance gaps**
- **Likelihood**: Medium
- **Impact**: High (security vulnerabilities, deployment blocks)
- **Mitigation**: Create compliance checklist, review before each phase completion, automated pre-commit checks

**Risk 3: Inadequate testing coverage**
- **Likelihood**: Low
- **Impact**: High (bugs in production)
- **Mitigation**: Enforce 80% coverage threshold, block PRs on test failures, prioritize critical path testing

**Risk 4: Deployment configuration errors**
- **Likelihood**: Medium
- **Impact**: High (production downtime)
- **Mitigation**: Test deployments on staging environment, use infrastructure-as-code (Render YAML, Vercel JSON), document rollback procedure

## 11. Key Decisions Summary

| Decision | Option Chosen | Rationale |
|----------|---------------|-----------|
| Frontend Framework | Next.js 16 App Router | Modern React framework with SSR, optimal for SEO and performance |
| Styling | Tailwind CSS | Utility-first, fast development, responsive design patterns |
| Authentication | Better Auth (JWT) | Stateless, scalable, API-friendly, industry standard |
| Backend Framework | FastAPI | High performance, async support, automatic OpenAPI docs |
| ORM | SQLModel | Type-safe, Pydantic integration, Alembic compatibility |
| Database | Neon PostgreSQL | Serverless, scalable, branching for preview environments |
| Deployment (Frontend) | Vercel | Automatic Next.js deployments, global CDN, preview URLs |
| Deployment (Backend) | Render | Automatic Python deployments, health checks, environment management |
| E2E Testing | Playwright | Multi-browser, parallel execution, trace recording |
| Backend Testing | pytest + pytest-cov | Python standard, async support, coverage reporting |
| Load Testing | k6 | Modern, JavaScript-based, easy scripting |
| Error Monitoring | Sentry | Real-time error tracking, release tracking, free tier |
| Package Manager (Python) | UV | Fast, modern, reproducible builds (Constitution requirement) |
| Type Checking (Frontend) | TypeScript strict | Catch bugs at compile time (Constitution requirement) |
| Type Checking (Backend) | mypy --strict | Catch bugs at compile time (Constitution requirement) |
| Primary Keys | UUID v4 | Globally unique, prevents enumeration attacks |
| Password Hashing | Argon2 | Modern, secure, recommended by OWASP |
| API Versioning | `/api/v1/` prefix | Supports backward compatibility (Constitution requirement) |
| Error Format | Standardized JSON | Consistent client handling (Constitution requirement) |

## 12. Next Steps

1. **Phase 1: Design** (this research output)
   - Create `data-model.md` with entity schemas and relationships
   - Create `contracts/api.openapi.yaml` with OpenAPI specification
   - Create `quickstart.md` with setup and development instructions

2. **Fill plan.md** with complete implementation plan:
   - Scope and Dependencies
   - Key Decisions and Rationale
   - Interfaces and API Contracts
   - Non-Functional Requirements
   - Data Management and Migration
   - Operational Readiness
   - Risk Analysis
   - Validation Criteria
   - Project Structure

3. **Generate tasks.md** with phase-based task breakdown:
   - Phase 1: Frontend Foundation (Next.js + Better Auth + Tailwind + E2E)
   - Phase 2: Backend Foundation (FastAPI + SQLModel + Alembic + pytest)
   - Phase 3: Database Performance (indexes, k6 load testing)
   - Phase 4: Full-Stack Integration (CORS, token refresh, E2E)
   - Phase 5: Production Deployment (Vercel + Render + monitoring)

4. **Execute implementation** (`/sp.implement`):
   - Follow Red-Green-Refactor cycle for each task
   - Validate Section VIII compliance at each checkpoint
   - Create PHRs for all significant decisions
   - Run tests continuously (TDD approach)

5. **Deploy and monitor**:
   - Deploy to Vercel and Render
   - Configure monitoring and alerting
   - Run load tests and verify performance
   - Create demo video

---

**Research Complete**: All technical unknowns resolved, best practices identified, architecture decisions documented.

**Next Command**: Continue with Phase 1 design artifacts (data-model.md, contracts/, quickstart.md)
