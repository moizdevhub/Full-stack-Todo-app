<!--
SYNC IMPACT REPORT
==================
Version Change: 1.0.0 → 2.0.0 (Production Standards Added)
Rationale: MAJOR - Added new mandatory security and quality principles (Section VIII) that fundamentally change requirements for production deployments beyond Phase I

Modified Principles:
- None (existing principles unchanged)

Added Sections:
- VIII. Production Standards (NON-NEGOTIABLE for production deployments)
  - AuthN/AuthZ (JWT validation at all network boundaries)
  - Data Segregation (user-scoped queries)
  - Secret Management (environment-only secrets)
  - API Stability (versioning and backward compatibility)
  - Error Contract (standardized JSON error responses)
  - Type Safety (TypeScript strict + Python mypy)
  - UV Package Manager (explicit requirement)
  - DB Migration Hygiene (Alembic migrations)
  - Testing Gates (80%+ coverage requirement)

Removed Sections:
- None

Templates Requiring Updates:
✅ .specify/memory/constitution.md (this file)
✅ .specify/templates/spec-template.md (aligned - already requires functional requirements)
✅ .specify/templates/plan-template.md (aligned - Constitution Check section validates compliance)
✅ .specify/templates/tasks-template.md (aligned - supports security and testing tasks)
⚠ CLAUDE.md (review for production security guidance)

Follow-up TODOs:
- When transitioning to production web stack (Next.js + FastAPI + Neon), all Section VIII principles become MANDATORY
- Consider creating production-specific templates in future phases
- Update CLAUDE.md to reference Section VIII for production deployments
-->

# Todo Console App Constitution

**Project**: Todo Console App (In-Memory Python → Future Production Stack)
**Phase**: Hackathon Phase I (future: production web application)
**Stack**: UV, Python 3.13+, Claude Code, Spec-Kit Plus
**Future Stack**: Next.js (TypeScript) + FastAPI (Python) + Neon (PostgreSQL)
**Infrastructure**: GitHub MCP Server

## Core Principles

### I. Agentic Development (NON-NEGOTIABLE)

All development MUST be performed by AI agents. Human role is limited to:
- Providing requirements and feature descriptions
- Reviewing and approving specs, plans, and implementations
- Making architectural decisions when prompted by agents
- Testing final deliverables

**Enforcement**:
- Zero vibe code writing permitted
- All code generation goes through agent workflow
- Human edits to code are violations unless fixing critical bugs
- Agent logs MUST be preserved in PHR (Prompt History Records)

**Rationale**: Ensures consistent, documented, reproducible development process
optimized for hackathon speed while maintaining quality and traceability.

### II. Spec-Driven Development (NON-NEGOTIABLE)

Every feature MUST begin with a specification. The mandatory workflow is:

1. **Spec** (`/sp.specify`) - Define WHAT and WHY (no HOW)
2. **Plan** (`/sp.plan`) - Architect HOW to implement
3. **Tasks** (`/sp.tasks`) - Break down into testable units
4. **Implement** (`/sp.implement`) - Execute task-by-task

**Enforcement**:
- No implementation without approved spec
- No plan without completed spec
- No tasks without approved plan
- No code without task breakdown
- Each stage produces artifacts in `specs/<feature>/`

**Rationale**: Prevents scope creep, ensures clarity before coding, enables
parallel work, creates documentation automatically, facilitates review.

### III. AI-First Approach

All development activities MUST use AI agents and tools:

**Agent Types** (located in `.claude/agents/`):
- `spec-writer` - Creates and refines specifications
- `architecture-planner` - Designs implementation plans
- `implementation-executor` - Writes production code
- `code-quality-validator` - Reviews code quality
- `test-case-designer` - Designs comprehensive test cases
- `documentation-maintainer` - Maintains all documentation

**Agent Invocation**:
- Agents are invoked via Claude Code Task tool
- Each agent has specific expertise and tools
- Agents communicate via handoffs (defined in agent frontmatter)
- Agent execution produces PHR for traceability

**Rationale**: Specialized agents ensure expert-level work in each domain,
handoffs create clear accountability, automation enables hackathon speed.

### IV. GitHub MCP Integration (MANDATORY)

ALL Git operations MUST go through the GitHub MCP Server. Direct git CLI
usage is PROHIBITED.

**MCP-Required Operations**:
- Creating branches (feature branches: `<number>-<feature-name>`)
- All commits (with conventional commit messages)
- Creating pull requests (with generated summaries)
- Managing issues (feature tracking)
- Setting milestones (phase tracking)
- Checking repository status
- Viewing commit history and diffs

**Enforcement**:
- Agents MUST use MCP tools for all GitHub operations
- No `git` commands in Bash tool
- All commits include co-author attribution to Claude
- PR descriptions auto-generated from spec artifacts

**Rationale**: MCP provides structured, validated, auditable GitHub operations
with error handling and consistency enforcement.

### V. Test-Driven Development

Testing is MANDATORY for all features:

**Test Requirements**:
- Unit tests for all core functions (pytest)
- Integration tests for feature workflows
- Test coverage minimum: 80% for production code
- Tests MUST be written before implementation (Red-Green-Refactor)
- All tests MUST pass before PR approval

**Test Organization**:
- Unit tests: `tests/unit/`
- Integration tests: `tests/integration/`
- Test fixtures: `tests/fixtures/`
- Test utilities: `tests/utils/`

**Enforcement**:
- `test-case-designer` agent creates test specs
- Implementation executor writes tests first
- Code quality validator verifies coverage
- CI MUST run tests on all PRs (future)

**Rationale**: Ensures reliability, enables refactoring, documents behavior,
catches regressions, hackathon code remains maintainable.

### VI. Documentation Completeness

All artifacts MUST be documented:

**Required Documentation**:
- `README.md` - Project overview, setup, usage
- `CLAUDE.md` - AI development guidelines and project rules
- `specs/<feature>/spec.md` - Feature specifications
- `specs/<feature>/plan.md` - Implementation plans
- `specs/<feature>/tasks.md` - Task breakdowns
- `history/prompts/` - All PHRs (Prompt History Records)
- `history/adr/` - Architectural Decision Records
- Inline code comments for complex logic

**Standards**:
- Markdown for all documentation
- Follow template structures from `.specify/templates/`
- Clear, concise, technical writing
- No placeholder text in final deliverables
- Version and timestamp all artifacts

**Rationale**: Documentation enables team onboarding, preserves decisions,
supports maintenance, demonstrates hackathon process.

### VII. Simplicity and Pragmatism

Optimize for hackathon constraints:

**Design Principles**:
- In-memory storage (no database setup overhead)
- Pure Python (minimal dependencies via UV)
- CLI-first interface (fastest to build and demo)
- Single repository (monorepo for speed)
- No over-engineering (YAGNI - You Ain't Gonna Need It)

**Technology Constraints**:
- Python 3.13+ only
- UV for dependency management
- Standard library preferred over external packages
- pytest for testing (minimal test framework)
- Rich library for CLI formatting (optional enhancement)

**Rationale**: Reduces setup time, eliminates deployment complexity, focuses
on core features, maximizes demo impact, enables rapid iteration.

### VIII. Production Standards (NON-NEGOTIABLE)

**Applicability**: These standards apply ONLY when deploying production web applications (Next.js + FastAPI + Neon stack). Phase I hackathon (CLI in-memory) is exempt.

**When Active**: Upon transition from CLI prototype to production web stack.

---

#### 8.1 Authentication & Authorization (AuthN/AuthZ)

Every network boundary (Next.js ↔ FastAPI, FastAPI ↔ Neon) MUST validate the JWT issued by Better Auth before processing any request body, query string, or path parameter.

**Enforcement**:
- All FastAPI endpoints MUST use `@require_auth` decorator or equivalent middleware
- JWT signature MUST be verified using the shared symmetric secret
- JWT claims (especially `sub` user UUID) MUST be extracted and validated
- Expired or malformed JWTs MUST return HTTP 401 Unauthorized
- Missing JWTs MUST return HTTP 401 Unauthorized

**Rationale**: Prevents unauthorized access, ensures every request is tied to an authenticated user, blocks token tampering.

---

#### 8.2 Data Segregation

Every SELECT / INSERT / UPDATE / DELETE MUST be filtered by the authenticated user UUID extracted from the JWT `sub` claim.

**Enforcement**:
- All database queries MUST include `WHERE user_id = <authenticated_user_uuid>`
- No global queries allowed (except admin endpoints with explicit authorization)
- ORM filters MUST automatically scope by user (e.g., SQLModel filters)
- Raw SQL queries MUST use parameterized user_id filtering

**Rationale**: Prevents data leaks between users, ensures multi-tenant data isolation, blocks privilege escalation attacks.

---

#### 8.3 Secret Management

The symmetric secret used to sign and verify JWTs MUST exist only in:
- Vercel environment variables (Next.js)
- Render / Northflank / equivalent environment variables (FastAPI)

**Enforcement**:
- The literal secret value MUST NEVER be committed to GitHub, logs, artifacts, or build outputs
- Secrets MUST be loaded via `os.environ` or equivalent at runtime
- `.env` files MUST be in `.gitignore`
- Pre-commit hooks MUST scan for hardcoded secrets
- Rotate secrets immediately if exposed

**Rationale**: Prevents credential leaks, enables secret rotation, protects against repository compromise.

---

#### 8.4 API Stability

Public endpoints MUST remain backward compatible for the lifetime of the current MAJOR version. Breaking changes require a MAJOR version bump and a minimum 90-day deprecation window.

**Enforcement**:
- Versioned API paths (e.g., `/api/v1/todos`, `/api/v2/todos`)
- No removing fields from response schemas in MINOR/PATCH versions
- No changing field types or semantics in MINOR/PATCH versions
- Deprecated endpoints MUST return `Deprecated: true` header + warning
- Breaking changes MUST be documented in CHANGELOG with migration guide

**Rationale**: Protects client integrations, enables gradual migrations, maintains trust with API consumers.

---

#### 8.5 Error Contract

All 4xx and 5xx responses MUST return JSON with the following structure:

```json
{
  "error": "Human-readable error message",
  "code": "MACHINE_READABLE_ERROR_CODE",
  "timestamp": "2025-01-07T12:34:56.789Z"
}
```

**Enforcement**:
- No stack traces exposed in production responses (log internally only)
- No HTML error pages for API endpoints
- Consistent error codes across all endpoints (e.g., `INVALID_TOKEN`, `USER_NOT_FOUND`)
- All exceptions MUST be caught and transformed to error contract format
- Error responses MUST use correct HTTP status codes (400, 401, 403, 404, 500, etc.)

**Rationale**: Enables client-side error handling, prevents information disclosure, provides actionable debugging info without security risks.

---

#### 8.6 Type Safety

TypeScript strict mode MUST be enabled for all Next.js code. Python type hints MUST pass mypy ≥ 1.0 for all FastAPI services.

**Enforcement**:
- **TypeScript**: `"strict": true` in `tsconfig.json`
- **Python**: `mypy --strict` MUST pass with zero errors
- All function signatures MUST have type annotations
- All SQLModel columns MUST be fully typed (no `Any` types)
- Pre-commit hooks MUST run type checkers
- CI MUST fail builds on type errors

**Rationale**: Catches bugs at compile time, enables IDE autocomplete, documents contracts, prevents runtime type errors.

---

#### 8.7 UV Package Manager

All Python dependency management MUST use UV package manager exclusively.

**Enforcement**:
- No `pip`, `poetry`, or `pipenv` commands allowed
- Dependencies declared in `pyproject.toml`
- Lock file (`uv.lock`) MUST be committed
- CI MUST use `uv sync` to install dependencies
- Virtual environments MUST be managed via `uv venv`

**Rationale**: Fast dependency resolution, reproducible builds, modern Python tooling, consistent with project standards.

---

#### 8.8 DB Migration Hygiene

Every schema change MUST ship as an Alembic migration and MUST be replayable from scratch on a fresh Neon branch.

**Enforcement**:
- All schema changes via `alembic revision --autogenerate`
- Migration files MUST be committed to repository
- Migration naming: `YYYYMMDD_HHMM_descriptive_name.py`
- Migrations MUST be idempotent (safe to run multiple times)
- Migrations MUST include both `upgrade()` and `downgrade()` functions
- Test migrations on fresh database before merging
- No direct `CREATE TABLE` / `ALTER TABLE` in application code

**Rationale**: Enables version-controlled schema evolution, supports rollbacks, ensures production/dev parity, prevents data loss.

---

#### 8.9 Testing Gates

FastAPI handler unit coverage MUST be ≥ 80%. End-to-end coverage MUST exist for core verbs (GET, POST, PUT, DELETE).

**Enforcement**:
- `pytest --cov` MUST report ≥ 80% coverage for `src/` directory
- CI MUST fail builds below 80% coverage threshold
- Critical paths (auth, payments, data mutations) MUST have integration tests
- E2E tests MUST cover happy path + primary error cases for each endpoint
- Coverage reports MUST be generated on every PR
- Uncovered code MUST be justified or tested before merge

**Rationale**: Maintains code quality, catches regressions, documents expected behavior, enables confident refactoring.

---

**Production Standards Enforcement**: When transitioning to production stack, the `code-quality-validator` agent MUST verify compliance with ALL Section VIII standards before approving any PR.

## Prohibited Actions

The following actions are VIOLATIONS of this constitution:

1. **Manual Code Writing** - All code MUST be generated by agents
2. **Skipping Specs** - No implementation without spec → plan → tasks
3. **Bypassing Agents** - Direct file edits instead of agent invocation
4. **Direct Git Commands** - MUST use GitHub MCP Server exclusively
5. **Untested Code** - No merges without passing tests and 80%+ coverage
6. **Undocumented Decisions** - Significant choices require ADRs
7. **Placeholder Text** - No TODO/TBD/FIXME in final deliverables
8. **Scope Creep** - Features not in spec are out of scope
9. **Production Violations** - When using production stack, all Section VIII standards MUST be followed

**Enforcement**: Code review by `code-quality-validator` agent checks
compliance. Violations require immediate remediation before PR approval.

## Required Workflow

Every feature follows this exact sequence:

### Phase 1: Specification
```
Human: /sp.specify <feature-description>
→ spec-writer agent creates specs/<N>-<name>/spec.md
→ Human reviews and approves (or requests clarifications via /sp.clarify)
```

### Phase 2: Planning
```
Human: /sp.plan
→ architecture-planner agent creates specs/<N>-<name>/plan.md
→ Identifies architecture decisions, creates ADRs if needed
→ Human reviews and approves
```

### Phase 3: Task Breakdown
```
Human: /sp.tasks
→ architecture-planner agent creates specs/<N>-<name>/tasks.md
→ Breaks plan into testable, ordered tasks
→ Human reviews task list
```

### Phase 4: Implementation
```
Human: /sp.implement
→ implementation-executor agent executes each task
→ Writes tests first (Red)
→ Implements functionality (Green)
→ Refactors if needed (Refactor)
→ Creates PHR for each task
```

### Phase 5: Quality Validation
```
Human: (automatic after implementation)
→ code-quality-validator agent reviews code
→ Checks: style, tests, coverage, documentation
→ For production deployments: validates Section VIII compliance
→ Reports issues or approves
```

### Phase 6: Git Workflow (via MCP)
```
Human: /sp.git.commit_pr
→ sp.git.commit_pr agent uses GitHub MCP to:
  - Stage changes
  - Create conventional commit
  - Push to feature branch
  - Create pull request with auto-generated description
→ Human reviews PR and merges
```

**Enforcement**: Each phase produces artifacts. Missing artifacts = incomplete
workflow = violation.

## Agent System Architecture

### Agent Location
All agents are defined in `.claude/agents/` as Markdown files with YAML
frontmatter.

### Agent Structure
```markdown
---
name: agent-name
description: What this agent does
tools: [Read, Write, Edit, Bash, Grep, Glob, etc.]
handoffs:
  - agent: next-agent-name
    prompt: Suggested next step
---

# Agent Instructions
[Detailed instructions for the agent...]
```

### Agent Invocation
Agents are invoked via Claude Code's Task tool:
```
Task(
  subagent_type="agent-name",
  prompt="Specific task for this agent",
  description="Short description"
)
```

### Agent Handoffs
Agents suggest next steps via handoff definitions. Handoffs appear in agent
output as actionable suggestions (e.g., "Run `/sp.plan` to create the plan").

### Agent Specialization
Each agent has a focused responsibility:
- **Input**: Specific context (spec, plan, code, etc.)
- **Process**: Domain expertise (specification, architecture, coding, etc.)
- **Output**: Artifact + handoff suggestion
- **Tools**: Minimal set needed for the job

**Rationale**: Single-responsibility agents are easier to maintain, debug,
and reason about. Handoffs create clear workflow.

## Skills System Architecture

### Skill Location
All skills are defined in `.claude/skills/` as Markdown files with YAML
frontmatter.

### Skill Structure
```markdown
---
description: What this skill does (shown in skill list)
handoffs:
  - label: Related action
    agent: agent-or-skill-name
    prompt: Suggested prompt
---

## User Input
$ARGUMENTS

## Task
[Instructions for executing this skill...]
```

### Available Skills
**Todo Management**:
- `/todo.add` - Add new todo with priority, due date, tags
- `/todo.list` - List/filter todos by status, priority, tags
- `/todo.complete` - Mark todo(s) as completed
- `/todo.delete` - Delete or archive todo(s)

**Development**:
- `/dev.run` - Run app in interactive/CLI/dev/server mode
- `/dev.test` - Run tests with coverage and filtering

**Spec-Driven Development** (from Spec-Kit Plus):
- `/sp.specify` - Create feature specification
- `/sp.clarify` - Clarify spec requirements
- `/sp.plan` - Create implementation plan
- `/sp.tasks` - Generate task breakdown
- `/sp.implement` - Execute implementation
- `/sp.adr` - Document architectural decisions
- `/sp.git.commit_pr` - Commit and create PR via MCP

### Skill Invocation
Skills are invoked by users typing `/<skill-name> [arguments]`

### Skill Design Principles
- **Single Purpose**: Each skill does one thing well
- **Discoverability**: Clear descriptions and handoffs
- **Flexibility**: Accept various argument formats
- **Validation**: Check inputs before execution
- **Feedback**: Clear success/error messages

**Rationale**: Skills provide user-friendly commands that orchestrate agents,
creating a streamlined development experience.

## GitHub MCP Integration

### MCP Server Setup
The GitHub MCP Server MUST be configured in Claude Code settings:
- Provides `github_*` tools (create_branch, create_pr, etc.)
- Authenticated with GitHub token
- Scoped to this repository

### MCP Workflow

**Branch Creation**:
```
github_create_branch(
  branch_name="<number>-<feature-name>",
  from_branch="master"
)
```

**Committing Changes**:
```
github_create_commit(
  message="feat: add todo list functionality\n\n🤖 Generated with Claude Code\n\nCo-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>",
  files=[...],
  branch="<number>-<feature-name>"
)
```

**Creating Pull Requests**:
```
github_create_pull_request(
  title="feat: add todo list functionality",
  body="[Auto-generated from spec and implementation]",
  base="master",
  head="<number>-<feature-name>"
)
```

**Issue Management**:
```
github_create_issue(
  title="Feature: <description>",
  body="[Spec summary]",
  labels=["feature", "phase-1"]
)
```

### Commit Message Format
Follow Conventional Commits:
```
<type>(<scope>): <description>

[optional body]

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
```

**Types**: feat, fix, docs, test, refactor, chore

**Rationale**: MCP ensures consistent, validated Git operations with proper
attribution and formatting.

## Quality Standards

### Code Quality
- **Readability**: Clear variable names, logical structure
- **Pythonic**: Follow PEP 8, use type hints (Python 3.13+)
- **Modularity**: Single-responsibility functions/classes
- **Error Handling**: Graceful failures with informative messages
- **No Dead Code**: Remove commented code, unused imports

### Testing Quality
- **Coverage**: Minimum 80% line coverage
- **Independence**: Tests don't depend on execution order
- **Clarity**: Test names describe what they verify
- **Fast**: Unit tests run in milliseconds
- **Assertions**: Use specific assertions (assertEqual vs assertTrue)

### Documentation Quality
- **Completeness**: All public functions have docstrings
- **Accuracy**: Docs match actual behavior
- **Examples**: Include usage examples where helpful
- **Up-to-date**: Updated with code changes

### Architecture Quality
- **Separation of Concerns**: Clear module boundaries
- **Dependency Direction**: High-level → low-level (no cycles)
- **Testability**: Easy to mock/stub dependencies
- **Simplicity**: Prefer simple solutions over clever ones

**Enforcement**: `code-quality-validator` agent checks these standards during
review phase.

## Deliverables & Success Criteria

### Required Deliverables

**Repository Structure**:
```
Todo-Console-App/
├── .claude/
│   ├── agents/           # All agent definitions
│   ├── skills/           # All skill definitions
│   └── commands/         # SDD workflow commands
├── .specify/
│   ├── memory/
│   │   └── constitution.md   # This file
│   ├── templates/        # Spec/plan/task templates
│   └── scripts/          # Automation scripts
├── specs/
│   ├── 1-<feature-1>/
│   │   ├── spec.md
│   │   ├── plan.md
│   │   └── tasks.md
│   └── [2-5 more features...]
├── history/
│   ├── prompts/          # All PHRs
│   │   ├── constitution/
│   │   ├── <feature-name>/
│   │   └── general/
│   └── adr/              # Architectural decisions
├── src/
│   ├── todo_app/         # Main application code
│   │   ├── __init__.py
│   │   ├── models.py     # Todo data models
│   │   ├── storage.py    # In-memory storage
│   │   ├── cli.py        # CLI interface
│   │   └── utils.py      # Utilities
│   └── __main__.py       # Entry point
├── tests/
│   ├── unit/             # Unit tests
│   ├── integration/      # Integration tests
│   ├── fixtures/         # Test data
│   └── conftest.py       # Pytest configuration
├── README.md             # Project overview
├── CLAUDE.md             # AI development guide
├── pyproject.toml        # UV project config
└── .gitignore
```

**Working Features** (All 5 MUST work):
1. **Add Todo** - Create todos with description, priority, due date, tags
2. **List Todos** - View all todos with filtering and sorting
3. **Complete Todo** - Mark todo(s) as done with timestamp
4. **Delete Todo** - Remove todo(s) with confirmation
5. **Interactive CLI** - REPL interface for all operations

**Documentation**:
- README with setup, usage, examples
- CLAUDE.md with development guidelines
- All specs, plans, tasks in specs/
- PHR for every significant agent interaction
- ADRs for architectural decisions

### Success Criteria

**Functional Success**:
- ✅ All 5 todo features implemented and working
- ✅ Interactive CLI accepts commands and shows output
- ✅ In-memory storage persists during session
- ✅ All tests pass with 80%+ coverage
- ✅ No runtime errors in happy path flows

**Process Success**:
- ✅ Full spec → plan → task → implement workflow for each feature
- ✅ Complete PHR history in history/prompts/
- ✅ All code generated by agents (zero manual coding)
- ✅ All Git operations via GitHub MCP
- ✅ Proper repository structure maintained

**Quality Success**:
- ✅ Code passes code-quality-validator review
- ✅ Documentation complete and accurate
- ✅ Clean git history with conventional commits
- ✅ No TODOs/FIXMEs in production code
- ✅ Professional README suitable for portfolio

**Hackathon Success**:
- ✅ Completed within hackathon timeframe
- ✅ Demonstrable working application
- ✅ Clear process documentation for judges
- ✅ Reproducible setup (README instructions work)
- ✅ Impressive AI-driven development showcase

**Production Success** (when applicable):
- ✅ All Section VIII standards verified and passing
- ✅ Zero security violations (AuthN/AuthZ, secrets, data segregation)
- ✅ Type safety verified (TypeScript strict + mypy --strict)
- ✅ API stability maintained (versioning, error contracts)
- ✅ Database migrations tested and replayable

**Rationale**: Clear, measurable criteria enable objective assessment and
ensure hackathon submission meets all requirements.

## Governance

### Constitutional Authority
This constitution is the SUPREME governance document for this project. In case
of conflict between this constitution and any other guidance (README,
CLAUDE.md, agent instructions, etc.), this constitution prevails.

### Amendment Process
1. Propose amendment with rationale
2. Document impact on existing artifacts
3. Update constitution with new version number
4. Propagate changes to dependent templates
5. Update CLAUDE.md if agent behavior changes
6. Create PHR documenting the amendment

**Version Bumping**:
- **MAJOR** (X.0.0): Remove/change core principles, workflow changes
- **MINOR** (0.X.0): Add new principles, expand sections
- **PATCH** (0.0.X): Clarifications, typos, non-semantic fixes

### Compliance Verification
Every agent invocation MUST verify constitutional compliance:
- Spec-writer: Ensures spec-first workflow
- Architecture-planner: Checks design principles + production standards (if applicable)
- Implementation-executor: Validates no manual coding + enforces type safety (Section VIII.6)
- Code-quality-validator: Enforces quality standards + Section VIII compliance (production only)
- sp.git.commit_pr: Ensures MCP-only Git operations

### Violation Response
If a violation is detected:
1. **Halt** - Stop current workflow
2. **Document** - Record violation in PHR
3. **Remediate** - Fix the violation
4. **Learn** - Update agent instructions to prevent recurrence
5. **Resume** - Continue workflow after fix

### Review Cadence
- **Per Feature**: Validate compliance during code quality review
- **Per Phase**: Review process adherence before phase completion
- **Post-Hackathon**: Retrospective on constitution effectiveness
- **Production Deployment**: Mandatory Section VIII audit before launch

**Rationale**: Strong governance ensures consistent, high-quality,
auditable development process throughout the hackathon.

---

**Version**: 2.0.0 | **Ratified**: 2025-12-30 | **Last Amended**: 2026-01-07
