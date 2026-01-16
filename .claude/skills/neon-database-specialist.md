---
name: "neon-database-specialist"
description: "Architect and manage serverless Postgres workflows with Neon. Use when the user needs to implement database branching, serverless connection pooling, or optimized SQL schemas for edge environments."
version: "1.0.0"
---

# Neon Database Specialist Skill

## When to Use This Skill

- User needs to set up **branching workflows** (Git-like DB environments per PR).
- User requires **scale-to-zero** configuration to optimize costs.
- User is implementing **serverless functions** or Edge runtimes requiring the Neon Serverless Driver.
- User needs to tune **Postgres performance** using `pg_stat_statements`.
- User requires **PII masking** or secure row-level security (RLS) policies.

## How This Skill Works

1.  **Instant Branching**: Treat the database like code. Create copy-on-write branches for every feature branch to prevent environment pollution.
2.  **Connection Optimization**: Default to the Neon Serverless Driver for WebSockets over HTTP/1.1 or use the pooled connection string (port 5432) for long-lived apps.
3.  **Compute Tuning**: Set the Compute Unit (CU) floor to minimize cold starts while ensuring the database scales to zero during idle hours.
4.  **Index-First Design**: Audit every `WHERE` clause in your JWT-isolated queries to ensure they are backed by an index.
5.  **Data Portability**: Maintain vanilla SQL compatibility and automate nightly logical dumps to S3 to avoid vendor lock-in.

## Output Format

Provide:
- **Connection Logic**: Optimized connection strings or driver initialization code.
- **SQL Schema**: Clean DDL with appropriate indexing and RLS policies.
- **Branching Workflow**: CLI commands or GitHub Action snippets for branching.
- **Cost/Performance Estimate**: Predicted CU usage and cold-start mitigations.

## Quality Criteria

A database setup is "Spec-Ready" when:
- **Efficiency**: Scale-to-zero is active with a defined `suspend_timeout`.
- **Latency**: Queries utilize the Neon Edge proxy to reduce round-trip times.
- **Security**: Database branches used in CI are anonymized or scoped to specific schemas.
- **Scalability**: Autoscale ceilings are set to prevent runaway costs during traffic spikes.

## Example

**Input**: "Configure a Neon DB for a Vercel Edge function. We need a branching strategy for our 'staging' and 'production' environments."

**Output**:
- **Strategy**: Utilize `neon-cli` to branch `main` into `staging` with a 24-hour TTL.
- **Code**: 
  ```typescript
  import { neon } from '@neondatabase/serverless';
  const sql = neon(process.env.DATABASE_URL);
  // Implementation of an edge-optimized query...