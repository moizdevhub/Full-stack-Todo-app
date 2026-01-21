# Quickstart Guide: Full-Stack Web Todo Application

**Feature**: Full-Stack Web Todo Application
**Branch**: `002-fullstack-web-app`
**Date**: 2026-01-07
**Target Audience**: Developers setting up the project for local development

---

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Repository Setup](#repository-setup)
3. [Backend Setup (FastAPI)](#backend-setup-fastapi)
4. [Database Setup (Neon PostgreSQL)](#database-setup-neon-postgresql)
5. [Frontend Setup (Next.js)](#frontend-setup-nextjs)
6. [Running the Application](#running-the-application)
7. [Testing](#testing)
8. [Deployment](#deployment)
9. [Troubleshooting](#troubleshooting)

---

## Prerequisites

Ensure the following tools are installed on your development machine:

### Required Tools

| Tool | Version | Purpose | Installation |
|------|---------|---------|--------------|
| **Node.js** | 20.x or 22.x | Next.js runtime | https://nodejs.org/ |
| **npm** | 10.x | Frontend package manager | Included with Node.js |
| **Python** | 3.13+ | FastAPI runtime | https://www.python.org/ |
| **UV** | Latest | Python package manager | https://docs.astral.sh/uv/ |
| **Git** | 2.40+ | Version control | https://git-scm.com/ |
| **PostgreSQL** | 15+ (optional) | Local database testing | https://www.postgresql.org/ |

### Optional Tools

- **Docker**: For containerized local development (alternative to local PostgreSQL)
- **Postman/Insomnia**: For API testing and debugging
- **VS Code**: Recommended IDE with extensions (ESLint, Prettier, Pylance, mypy)

### Verify Installation

```bash
# Check Node.js and npm
node --version  # Should be v20.x or v22.x
npm --version   # Should be v10.x

# Check Python and UV
python --version  # Should be 3.13+
uv --version      # Should be latest

# Check Git
git --version  # Should be 2.40+
```

---

## Repository Setup

### 1. Clone the Repository

```bash
# Clone from GitHub
git clone https://github.com/your-org/todo-console-app.git
cd todo-console-app

# Checkout the feature branch
git checkout 002-fullstack-web-app
```

### 2. Project Structure

After setup, your project will have this structure:

```
todo-console-app/
├── backend/                 # FastAPI backend
│   ├── alembic/            # Database migrations
│   ├── src/
│   │   ├── api/            # API route handlers
│   │   ├── models/         # SQLModel entities
│   │   ├── services/       # Business logic
│   │   ├── middleware/     # JWT auth middleware
│   │   └── main.py         # FastAPI app entry point
│   ├── tests/              # pytest tests
│   ├── pyproject.toml      # UV dependencies
│   └── .env                # Backend environment variables (create this)
├── frontend/                # Next.js frontend
│   ├── src/
│   │   ├── app/            # Next.js App Router pages
│   │   ├── components/     # React components
│   │   ├── lib/            # API client, utilities
│   │   └── types/          # TypeScript type definitions
│   ├── e2e/                # Playwright E2E tests
│   ├── public/             # Static assets
│   ├── package.json        # npm dependencies
│   └── .env.local          # Frontend environment variables (create this)
├── specs/                   # Feature specifications
│   └── 002-fullstack-web-app/
│       ├── spec.md
│       ├── plan.md
│       ├── data-model.md
│       ├── quickstart.md   # This file
│       └── contracts/
│           └── api.openapi.yaml
└── README.md
```

---

## Backend Setup (FastAPI)

### 1. Navigate to Backend Directory

```bash
cd backend
```

### 2. Install Dependencies with UV

```bash
# Create virtual environment and install dependencies
uv sync

# Activate virtual environment
# Windows (Git Bash/WSL)
source .venv/Scripts/activate  # Git Bash
# or
.venv\Scripts\activate.bat     # Windows CMD

# Linux/macOS
source .venv/bin/activate
```

### 3. Create Environment Variables File

Create `backend/.env` with the following content:

```env
# Database Configuration
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/todo_app
# For Neon PostgreSQL (production):
# DATABASE_URL=postgresql+asyncpg://username:password@ep-xxx.us-east-2.aws.neon.tech/todo_db?sslmode=require

# JWT Configuration
JWT_SECRET=your-super-secret-jwt-signing-key-change-this-in-production
JWT_ALGORITHM=HS256
JWT_EXPIRATION_HOURS=24

# CORS Configuration
CORS_ORIGINS=http://localhost:3000,https://todo-app.vercel.app

# Environment
ENVIRONMENT=development  # or "production"

# Logging
LOG_LEVEL=INFO
```

**IMPORTANT SECURITY NOTES**:
- NEVER commit `.env` files to Git (already in `.gitignore`)
- Generate a strong JWT secret: `python -c "import secrets; print(secrets.token_urlsafe(32))"`
- Use different secrets for development and production

### 4. Verify Dependencies Installation

```bash
# Check installed packages
uv pip list

# Expected packages (partial list):
# - fastapi
# - uvicorn
# - sqlmodel
# - alembic
# - asyncpg
# - passlib
# - python-jose
# - pydantic
# - pytest
# - pytest-cov
# - pytest-asyncio
```

---

## Database Setup (Neon PostgreSQL)

### Option A: Local PostgreSQL (Development)

#### 1. Install PostgreSQL

```bash
# Ubuntu/Debian
sudo apt-get install postgresql postgresql-contrib

# macOS (Homebrew)
brew install postgresql@15
brew services start postgresql@15

# Windows
# Download installer from https://www.postgresql.org/download/windows/
```

#### 2. Create Database and User

```bash
# Connect to PostgreSQL
psql -U postgres

# Create database and user
CREATE DATABASE todo_app;
CREATE USER todo_user WITH PASSWORD 'secure_password';
GRANT ALL PRIVILEGES ON DATABASE todo_app TO todo_user;
\q
```

#### 3. Update `.env` with Local Database URL

```env
DATABASE_URL=postgresql+asyncpg://todo_user:secure_password@localhost:5432/todo_app
```

### Option B: Neon PostgreSQL (Cloud Development/Production)

#### 1. Create Neon Account

- Visit https://neon.tech
- Sign up for free account (no credit card required for free tier)

#### 2. Create Project and Database

- Create new project: "todo-app"
- Note the connection string (format: `postgresql://username:password@ep-xxx.region.aws.neon.tech/dbname`)
- Enable connection pooling (recommended for production)

#### 3. Update `.env` with Neon URL

```env
DATABASE_URL=postgresql+asyncpg://username:password@ep-xxx.us-east-2.aws.neon.tech/todo_db?sslmode=require
```

### 4. Run Database Migrations

```bash
# Ensure you're in backend/ directory and virtual environment is active

# Run migrations to create tables
alembic upgrade head

# Verify tables were created
# For local PostgreSQL:
psql -U todo_user -d todo_app -c "\dt"

# For Neon PostgreSQL:
# Use Neon web console to view tables
```

**Expected tables after migration**:
- `users` (id, email, hashed_password, created_at)
- `todos` (id, user_id, title, description, completed, created_at, updated_at)
- `alembic_version` (version tracking)

### 5. (Optional) Seed Development Data

```bash
# Run seed script (if available)
python scripts/seed_dev_data.py

# This creates:
# - Demo user: demo@example.com / DemoPassword123
# - Sample todos for testing
```

---

## Frontend Setup (Next.js)

### 1. Navigate to Frontend Directory

```bash
cd ../frontend  # From backend/ directory
# or
cd frontend     # From repository root
```

### 2. Install Dependencies with npm

```bash
# Install all dependencies
npm install

# This installs:
# - next, react, react-dom
# - typescript, @types/react, @types/node
# - tailwindcss, postcss, autoprefixer
# - better-auth (JWT authentication)
# - @playwright/test (E2E testing)
# - axios or fetch for API calls
```

### 3. Create Environment Variables File

Create `frontend/.env.local` with the following content:

```env
# API Configuration
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1

# For production:
# NEXT_PUBLIC_API_URL=https://todo-api.onrender.com/api/v1

# JWT Configuration (must match backend)
NEXT_PUBLIC_JWT_SECRET=your-super-secret-jwt-signing-key-change-this-in-production

# Environment
NEXT_PUBLIC_ENVIRONMENT=development
```

**IMPORTANT**:
- Use `NEXT_PUBLIC_` prefix for client-side accessible variables
- Never expose sensitive secrets via `NEXT_PUBLIC_` variables
- The JWT secret here is ONLY for token verification, not signing (handled by backend)

### 4. Verify Installation

```bash
# Check installed packages
npm list --depth=0

# Check TypeScript configuration
npx tsc --version  # Should be 5.x

# Verify Next.js is working
npm run dev -- --help
```

---

## Running the Application

### Start Backend (Terminal 1)

```bash
# Navigate to backend directory
cd backend

# Activate virtual environment (if not already active)
source .venv/Scripts/activate  # Git Bash/WSL
# or
.venv\Scripts\activate.bat     # Windows CMD

# Start FastAPI with auto-reload
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000

# Backend will be available at:
# - API: http://localhost:8000/api/v1
# - Docs: http://localhost:8000/docs (Swagger UI)
# - ReDoc: http://localhost:8000/redoc
```

**Expected output**:
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [12345] using WatchFiles
INFO:     Started server process [12346]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

### Start Frontend (Terminal 2)

```bash
# Navigate to frontend directory
cd frontend

# Start Next.js development server
npm run dev

# Frontend will be available at:
# - http://localhost:3000
```

**Expected output**:
```
▲ Next.js 16.0.0
- Local:        http://localhost:3000
- Environments: .env.local

✓ Ready in 1.2s
```

### Verify Everything Works

1. **Open browser to http://localhost:3000**
   - Should see the todo app landing page
   - Registration/login forms should be visible

2. **Test API directly**:
   ```bash
   # Health check
   curl http://localhost:8000/api/health
   # Expected: {"status":"ok","timestamp":"2026-01-07T12:34:56.789Z","version":"1.0.0"}

   # OpenAPI docs
   # Open http://localhost:8000/docs in browser
   # Should see interactive Swagger UI
   ```

3. **Register a test user**:
   - Use frontend UI or curl:
   ```bash
   curl -X POST http://localhost:8000/api/v1/auth/register \
     -H "Content-Type: application/json" \
     -d '{"email":"test@example.com","password":"TestPassword123"}'
   # Expected: {"access_token":"<JWT>","token_type":"bearer","user":{...}}
   ```

---

## Testing

### Backend Tests (pytest)

```bash
# Navigate to backend directory
cd backend

# Run all tests with coverage
pytest --cov=src --cov-report=term-missing --cov-report=html

# Run specific test file
pytest tests/unit/test_services.py

# Run with verbose output
pytest -v

# Run only integration tests
pytest tests/integration/

# Generate coverage report
pytest --cov=src --cov-report=html
# Open htmlcov/index.html in browser
```

**Expected output** (example):
```
========================= test session starts =========================
collected 42 items

tests/unit/test_models.py ........                              [ 19%]
tests/unit/test_services.py ............                        [ 47%]
tests/integration/test_auth_endpoints.py ......                 [ 61%]
tests/integration/test_todo_endpoints.py ..............          [100%]

---------- coverage: platform win32, python 3.13.0 ----------
Name                       Stmts   Miss  Cover   Missing
--------------------------------------------------------
src/main.py                   45      2    96%   78-79
src/models/user.py            32      0   100%
src/models/todo.py            42      1    98%   67
src/services/auth.py          67      3    96%   45, 89-90
src/services/todo.py          89      4    95%   102-105
--------------------------------------------------------
TOTAL                        275     10    96%

========================= 42 passed in 3.45s =========================
```

### Frontend E2E Tests (Playwright)

```bash
# Navigate to frontend directory
cd frontend

# Install Playwright browsers (first time only)
npx playwright install

# Run all E2E tests (headless mode)
npx playwright test

# Run tests with UI (headed mode)
npx playwright test --headed

# Run specific test file
npx playwright test e2e/auth.spec.ts

# Show test report
npx playwright show-report

# Debug tests
npx playwright test --debug
```

**Expected output** (example):
```
Running 15 tests using 3 workers

  ✓ [chromium] › auth.spec.ts:3:5 › user can register (2.1s)
  ✓ [chromium] › auth.spec.ts:15:5 › user can login (1.8s)
  ✓ [chromium] › todo-crud.spec.ts:3:5 › user can create todo (2.5s)
  ✓ [chromium] › todo-crud.spec.ts:18:5 › user can complete todo (1.9s)
  ✓ [chromium] › todo-crud.spec.ts:30:5 › user can delete todo (2.1s)
  ...

  15 passed (18.7s)
```

### Type Checking

```bash
# Backend (mypy)
cd backend
mypy src/ --strict
# Expected: Success: no issues found in X source files

# Frontend (TypeScript)
cd frontend
npm run type-check
# or
npx tsc --noEmit
# Expected: no errors
```

### Linting

```bash
# Backend (Ruff)
cd backend
ruff check src/
# Expected: All checks passed!

# Frontend (ESLint)
cd frontend
npm run lint
# Expected: ✓ No ESLint warnings or errors
```

---

## Deployment

### Backend Deployment (Render)

#### 1. Create Render Account
- Visit https://render.com
- Sign up with GitHub account

#### 2. Create New Web Service
- Click "New +" → "Web Service"
- Connect GitHub repository
- Select `002-fullstack-web-app` branch
- **Build Command**: `uv sync && alembic upgrade head`
- **Start Command**: `uvicorn src.main:app --host 0.0.0.0 --port $PORT`
- **Environment Variables**:
  - `DATABASE_URL`: (Neon connection string)
  - `JWT_SECRET`: (strong random secret)
  - `CORS_ORIGINS`: `https://your-app.vercel.app`

#### 3. Deploy
- Click "Create Web Service"
- Wait for deployment (2-5 minutes)
- Note the service URL: `https://todo-api.onrender.com`

### Frontend Deployment (Vercel)

#### 1. Create Vercel Account
- Visit https://vercel.com
- Sign up with GitHub account

#### 2. Import Project
- Click "New Project"
- Import GitHub repository
- Select `002-fullstack-web-app` branch
- **Framework Preset**: Next.js
- **Root Directory**: `frontend`
- **Environment Variables**:
  - `NEXT_PUBLIC_API_URL`: `https://todo-api.onrender.com/api/v1`
  - `NEXT_PUBLIC_JWT_SECRET`: (same as backend JWT_SECRET)

#### 3. Deploy
- Click "Deploy"
- Wait for deployment (1-3 minutes)
- Visit your live site: `https://your-app.vercel.app`

### Verify Production Deployment

1. **Health Check**:
   ```bash
   curl https://todo-api.onrender.com/api/health
   ```

2. **Frontend Live**:
   - Visit `https://your-app.vercel.app`
   - Register a new user
   - Create a todo
   - Verify CRUD operations work

3. **Monitor Logs**:
   - Render: View logs in Render dashboard
   - Vercel: View logs in Vercel dashboard
   - Neon: View queries in Neon dashboard

---

## Troubleshooting

### Common Issues

#### Issue: Backend fails to start with "ModuleNotFoundError"

**Solution**:
```bash
# Reinstall dependencies
cd backend
uv sync --reinstall

# Verify virtual environment is activated
which python  # Should point to .venv/bin/python
```

#### Issue: Database connection fails with "Connection refused"

**Solution**:
```bash
# Check PostgreSQL is running
sudo systemctl status postgresql  # Linux
brew services list                # macOS

# Verify connection string in .env
echo $DATABASE_URL

# Test connection manually
psql -d $DATABASE_URL  # or use Neon web console
```

#### Issue: Frontend API calls fail with CORS errors

**Solution**:
```bash
# Check CORS_ORIGINS in backend/.env includes frontend URL
CORS_ORIGINS=http://localhost:3000

# Restart backend after changing .env
```

#### Issue: Alembic migration fails with "Target database is not up to date"

**Solution**:
```bash
# Check current migration version
alembic current

# Rollback if needed
alembic downgrade -1

# Re-run migration
alembic upgrade head

# If stuck, stamp the version manually
alembic stamp head
```

#### Issue: JWT token validation fails

**Solution**:
```bash
# Verify JWT_SECRET matches between frontend and backend
# Check .env and .env.local files

# Decode JWT to inspect claims (use jwt.io)
# Verify 'sub' claim contains valid user UUID
```

#### Issue: Playwright tests fail with "browserType.launch: Executable doesn't exist"

**Solution**:
```bash
# Reinstall Playwright browsers
npx playwright install

# For specific browser
npx playwright install chromium
```

#### Issue: TypeScript errors after npm install

**Solution**:
```bash
# Delete node_modules and reinstall
rm -rf node_modules package-lock.json
npm install

# Clear Next.js cache
rm -rf .next
npm run dev
```

---

## Development Workflow

### Daily Development

1. **Start both servers**:
   ```bash
   # Terminal 1: Backend
   cd backend && uvicorn src.main:app --reload

   # Terminal 2: Frontend
   cd frontend && npm run dev
   ```

2. **Make changes**:
   - Edit backend code in `backend/src/`
   - Edit frontend code in `frontend/src/`
   - Auto-reload occurs on file save

3. **Run tests frequently**:
   ```bash
   # Backend tests
   cd backend && pytest

   # Frontend type check
   cd frontend && npm run type-check
   ```

4. **Commit changes** (via GitHub MCP Server):
   ```bash
   # Use sp.git.commit_pr skill for git operations
   # See CLAUDE.md for workflow
   ```

### Database Migrations

When modifying SQLModel classes:

```bash
# 1. Update SQLModel class (e.g., add column to Todo model)

# 2. Generate migration
cd backend
alembic revision --autogenerate -m "Add priority column to todos"

# 3. Review generated migration in alembic/versions/

# 4. Test migration on local database
alembic upgrade head

# 5. Verify with database query
psql -d todo_app -c "SELECT * FROM todos LIMIT 1;"

# 6. Commit migration file to Git
```

---

## Additional Resources

### Documentation

- **FastAPI**: https://fastapi.tiangolo.com/
- **Next.js**: https://nextjs.org/docs
- **SQLModel**: https://sqlmodel.tiangolo.com/
- **Alembic**: https://alembic.sqlalchemy.org/
- **Playwright**: https://playwright.dev/
- **Neon PostgreSQL**: https://neon.tech/docs
- **Better Auth**: https://www.better-auth.com/docs

### Project-Specific Docs

- **Specification**: `specs/002-fullstack-web-app/spec.md`
- **Implementation Plan**: `specs/002-fullstack-web-app/plan.md`
- **Data Model**: `specs/002-fullstack-web-app/data-model.md`
- **API Contract**: `specs/002-fullstack-web-app/contracts/api.openapi.yaml`
- **Constitution**: `.specify/memory/constitution.md`

### Support

- **Issues**: Report bugs via GitHub Issues
- **Questions**: Ask in project Slack/Discord channel
- **Code Review**: Create PR and request review from team

---

**Last Updated**: 2026-01-07
**Maintained By**: Architecture Planning Team

**Next Steps**: After completing this quickstart, proceed to Phase 1 implementation (Next.js frontend scaffolding).
