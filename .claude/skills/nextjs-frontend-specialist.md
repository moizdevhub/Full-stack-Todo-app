---
name: "nextjs-frontend-specialist"
description: "Engineer production-grade, Lighthouse-100, TypeScript-strict React applications using Next.js. Use when the user needs to build high-performance UI, implement accessible components, or architect App Router solutions."
version: "1.0.0"
---

# Next.js Frontend Specialist Skill

## When to Use This Skill

- User needs to build or refactor a Next.js application using the **App Router**.
- User requires **Lighthouse-100** performance and SEO optimization.
- User needs **TypeScript-strict** type definitions and Zod validation.
- User mentions **Tailwind CSS**, Radix UI, or Shadcn for accessible UI components.
- User requires secure **Auth flows** (e.g., Better-Auth) with SSR and JWT.

## How This Skill Works

1.  **Strict Architecture**: Default to Server Components (RSC) to minimize client-side JS; use 'use client' only at the leaf nodes.
2.  **Type-First Development**: Define Zod schemas for all API responses and component props before writing logic.
3.  **A11y Integration**: Implement `aria-*` attributes and keyboard navigation as the component is being built, not after.
4.  **Performance Optimization**: Use `next/image` for layout stability, dynamic imports for heavy libraries, and edge runtimes for low-latency middleware.
5.  **Fail-Fast Logic**: Configure CI/CD patterns where any lint error or type mismatch prevents the build.

## Output Format

Provide:
- **Component Code**: Clean, modular TSX using Tailwind CSS.
- **Type Definitions**: Exported interfaces or Zod schemas.
- **Performance Notes**: Explanation of bundle size impact and caching strategy (ISR/SSG/SSR).
- **Accessibility Report**: Brief list of keyboard shortcuts and ARIA roles implemented.

## Quality Criteria

A project is "Production-Grade" when:
- **Bundle Size**: Zero unused JavaScript; FCP < 1.5s.
- **Type Safety**: No `any` types; `strict: true` in `tsconfig.json`.
- **Accessibility**: axe-core score is 0; 100% keyboard navigable.
- **Runtime**: Error boundaries and suspense fallbacks are implemented for "loud" failure handling.

## Example

**Input**: "Build a 'User Profile' card for a dashboard. Needs to show name, email, and a 'Settings' button. Use Next.js 15 App Router and Tailwind."

**Output**:
- **Implementation**: A Server Component for data fetching with a Client Component for the interactive button.
- **Code**: 
  ```typescript
  // types/user.ts
  export const UserSchema = z.object({ name: z.string(), email: z.string().email() });
  
  // components/ProfileCard.tsx
  import { UserSchema } from "@/types/user";
  // ... Accessible, type-safe implementation using Tailwind