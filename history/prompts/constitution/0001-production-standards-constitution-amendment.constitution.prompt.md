---
id: 0001
title: Production Standards Constitution Amendment
stage: constitution
date: 2026-01-07
surface: agent
model: claude-sonnet-4-5
feature: none
branch: 001-todo-cli-phase-i
user: system
command: /sp.constitution
labels: ["constitution", "governance", "production", "security", "quality"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - .specify/memory/constitution.md
tests:
  - N/A (constitution amendment, no code changes)
---

## Prompt

/sp.constitution

AuthN / AuthZ

Every network boundary (Next.js ↔ FastAPI, FastAPI ↔ Neon) MUST validate the JWT issued by Better Auth before processing any request body, query string, or path parameter.

Data Segregation

Every SELECT / INSERT / UPDATE / DELETE MUST be filtered by the authenticated user UUID extracted from the JWT sub claim.

Secret Management

The symmetric secret used to sign and verify JWTs MUST exist only in:

• Vercel environment variables (Next.js)
• Render / Northflank / equivalent environment variables (FastAPI)

The literal value MUST never be committed to GitHub, logs, artifacts, or build outputs.

API Stability

Public endpoints MUST remain backward compatible for the lifetime of the current MAJOR version.
Breaking changes require a MAJOR version bump and a minimum 90-day deprecation window.

Error Contract

All 4xx and 5xx responses MUST return JSON:

{ "error": string, "code": string, "timestamp": iso8601 }


No stack traces may be exposed in production responses.

Type Safety

TypeScript strict mode MUST be enabled for all Next.js code.
Python type hints MUST pass mypy ≥ 1.0 for all FastAPI services.
UV package manager
All SQLModel columns MUST be fully typed.

DB Migration Hygiene

Every schema change MUST ship as an Alembic migration and MUST be replayable from scratch on a fresh Neon branch.

Testing Gates

FastAPI handler unit coverage MUST be ≥ 80 %.
End-to-end coverage MUST exist for core verbs (GET

## Response snapshot

Constitution updated to version 2.0.0 with new Section VIII: Production Standards.

**Version Change**: 1.0.0 → 2.0.0 (MAJOR)

**Rationale**: Added mandatory security and quality principles for production web application deployments (Next.js + FastAPI + Neon stack). Phase I hackathon CLI app remains exempt.

**New Section VIII includes**:
- 8.1 AuthN/AuthZ - JWT validation at all network boundaries
- 8.2 Data Segregation - User-scoped database queries
- 8.3 Secret Management - Environment-only secrets, no hardcoded values
- 8.4 API Stability - Versioning, backward compatibility, 90-day deprecation
- 8.5 Error Contract - Standardized JSON error responses
- 8.6 Type Safety - TypeScript strict mode + Python mypy --strict
- 8.7 UV Package Manager - Explicit Python dependency management requirement
- 8.8 DB Migration Hygiene - Alembic migrations, idempotent, replayable
- 8.9 Testing Gates - 80%+ coverage + E2E tests for core verbs

**Applicability**: Section VIII standards apply ONLY when deploying production web applications. Current Phase I CLI prototype is exempt.

**Enforcement**: When transitioning to production stack, code-quality-validator agent MUST verify compliance with ALL Section VIII standards before approving any PR.

**Template Alignment**: All existing templates (spec, plan, tasks) already aligned - no changes required.

## Outcome

- ✅ Impact: Constitution amended to v2.0.0 with production security and quality standards
- 🧪 Tests: N/A (governance document, no code changes)
- 📁 Files: .specify/memory/constitution.md updated with Section VIII
- 🔁 Next prompts: When transitioning to production stack, reference Section VIII for mandatory requirements
- 🧠 Reflection: MAJOR version bump justified - new principles fundamentally change production deployment requirements

## Evaluation notes (flywheel)

- Failure modes observed: None - amendment successfully integrated production standards while preserving Phase I exemption
- Graders run and results (PASS/FAIL): PASS - Constitution structure maintained, all placeholders filled, sync impact report complete
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): When implementing production features, validate Section VIII compliance in code-quality-validator agent
