---
name: "fullstack-integration-specialist"
description: "Diagnose and resolve cross-layer friction between Next.js and FastAPI. Use when the user needs to sync JWT auth, debug CORS issues, manage cookie-based sessions, or implement SSR token forwarding."
version: "1.0.0"
---

# Full-Stack Integration Specialist Skill

## When to Use This Skill

- User is struggling with **CORS** pre-flight errors or credential mismatches.
- User needs to sync **Better-Auth** (Next.js) with a **FastAPI** backend.
- User is implementing **SSR (Server-Side Rendering)** and needs to forward tokens to an external API.
- User reports "Session Expired" loops or **JWT clock-skew** issues.
- User needs to implement **distributed tracing** (Trace-ID) from frontend to DB.

## How This Skill Works

1.  **Auth Synchronization**: Ensure JWT `iss` (issuer), `aud` (audience), and `secret_key` are byte-for-byte identical between Next.js and FastAPI.
2.  **Cookie Strategy**: Default to `httpOnly`, `Secure`, `SameSite=Lax` cookies for browser sessions to mitigate CSRF without losing functionality.
3.  **CORS Hardening**: Never use wildcards (`*`) with `Allow-Credentials`. Use specific origin lists and ensure pre-flight `OPTIONS` requests return `204 No Content` instantly.
4.  **Token Forwarding**: In `getServerSideProps` or Server Actions, extract the cookie/header and inject it into the outgoing `fetch` request to the FastAPI backend.
5.  **Observability**: Inject a `X-Trace-ID` in the Next.js middleware and ensure FastAPI logs include this ID for cross-service debugging.

## Output Format

Provide:
- **Environment Config**: Unified `.env` structure for both services.
- **Middleware Logic**: TypeScript/Python snippets for auth interceptors.
- **CORS Config**: FastAPI `CORSMiddleware` settings matched with Next.js headers.
- **Troubleshooting Checklist**: Step-by-step verification for JWT/Cookie failures.

## Quality Criteria

Integration is "Seamless" when:
- **Latency**: Authentication middleware adds < 10ms to the request chain.
- **Security**: Zero "silent fall-throughs"; a 401 from API triggers an immediate, clean UI redirect.
- **Consistency**: Environment variables are managed through a single source of truth (e.g., Doppler, Vercel).
- **Compatibility**: Auth flow works across Safari (strict ITP), iOS WebViews, and desktop browsers.

## Example

**Input**: "My Next.js app on Vercel is getting a CORS error when calling my FastAPI backend on Render. I'm using cookies for auth."

**Output**:
- **Diagnosis**: Credentials enabled on fetch but `Access-Control-Allow-Origin` set to `*`.
- **FastAPI Fix**: 
  ```python
  app.add_middleware(CORSMiddleware, allow_origins=["[https://your-app.vercel.app](https://your-app.vercel.app)"], allow_credentials=True)