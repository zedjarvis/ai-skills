---
name: create-next-nest-monorepo
description: Create production-ready TypeScript monorepos with pnpm workspaces, Turborepo, Next.js App Router frontend, shadcn/ui, NestJS backend, Swagger/OpenAPI, Terminus health checks, shared packages, and deployment modes for separate services or Nest-hosted static frontend builds. Use when the user asks to scaffold, review, fix, or document a Next.js + NestJS full-stack monorepo starter.
---

# Create Next Nest Monorepo

Use this skill to create a clean full-stack TypeScript monorepo for AI-assisted development.

## Default Architecture

Use this structure unless the user requests otherwise:

```text
repo-name/
  apps/
    frontend/      # Next.js App Router + shadcn/ui
    backend/       # NestJS API
  packages/
    shared/        # shared Zod schemas, API contracts, types
    ts-config/     # shared TypeScript configs
  package.json
  pnpm-workspace.yaml
  turbo.json
  AGENTS.md
```

Prefer:

- `pnpm` workspaces for package isolation and `workspace:*` dependencies.
- Turborepo for task orchestration and cacheable builds.
- `apps/*` for deployable apps and `packages/*` for shared libraries/tooling.
- `@repo/*` internal package names unless the user has an organization namespace.
- Shared contracts through `@repo/shared`, never cross-package relative imports.

## Workflow

1. Verify current docs before generating.
   - Check Next.js, shadcn/ui, NestJS, Turborepo, and pnpm docs if the task depends on current commands or versions.
   - Reject stale Turborepo examples that use `pipeline`; current config uses `tasks`.
   - Record sources in `references/sources.md` when creating a new skill, template, or repo guide.

2. Choose deployment mode.
   - Default development mode: run frontend and backend as separate dev servers through `turbo run dev`.
   - Default production mode: separate frontend and backend services unless the user explicitly wants one backend-hosted deployable.
   - Backend-hosted frontend mode: only serve the frontend from Nest when the frontend can be built as a static Next export. See [deployment-modes.md](references/deployment-modes.md).
   - Do not claim Nest can serve a normal SSR Next.js app by copying `.next/`; SSR Next needs a Next runtime/server or platform adapter.

3. Scaffold the repo.
   - Follow [scaffold-guide.md](references/scaffold-guide.md) for exact commands and file contents.
   - Use `pnpm create next-app@latest apps/frontend --yes` or the latest official equivalent.
   - Run `pnpm dlx shadcn@latest init` from `apps/frontend`.
   - Create the Nest backend in `apps/backend` using the Nest CLI or a manual Nest starter that matches current docs.
   - Add Swagger/OpenAPI setup in `apps/backend/src/main.ts`.
   - Add a Terminus health module and `/health` endpoint.
   - Add optional `@nestjs/serve-static` only for backend-hosted static frontend deployment mode.

4. Configure packages.
   - Create `packages/ts-config` with shared TypeScript configs.
   - Create `packages/shared` for Zod schemas, API contracts, DTO-like types, and shared constants.
   - Prefer Just-in-Time TypeScript package exports for simple internal type/schema packages.
   - Use compiled packages with `tsc` when runtime JavaScript must be consumed directly by Node, when package build output is deployed independently, or when consumers cannot transpile workspace TypeScript.

5. Configure orchestration.
   - Root scripts should usually include `dev`, `build`, `lint`, `typecheck`, and `format`.
   - `turbo.json` must use `tasks`, cache build outputs, and mark long-running dev tasks as `persistent`.
   - Add `dependsOn: ["^build"]` for build tasks that rely on internal packages.

6. Add AI-agent project instructions.
   - Create a root `AGENTS.md` in generated monorepos.
   - Include exact scripts, package-boundary rules, deployment modes, and validation commands.
   - Keep instructions concise and concrete.

7. Validate.
   - Run dependency install from the repo root.
   - Run `pnpm build`, `pnpm lint`, and `pnpm typecheck` when available.
   - Run `create-next-nest-monorepo/scripts/validate_monorepo.py <repo-path>` from this skills repository to catch missing structure.
   - Verify backend routes: `/api/health` or `/health` depending on the chosen global prefix, and Swagger docs at the configured docs route.

## Non-Negotiables

- Use `workspace:*` for internal dependencies.
- Keep frontend and backend dev servers separate.
- Prefix backend API routes, usually with `api`, to avoid static frontend route conflicts.
- Do not use cross-relative imports between apps and packages.
- Do not add a root `tsconfig.json` as the dumping ground for all package config; each package/app owns its config and can extend `@repo/ts-config`.
- Do not use stale `turbo.json` examples with `pipeline`.
- Do not serve SSR Next.js from Nest static middleware.

## When to Read References

- Read [scaffold-guide.md](references/scaffold-guide.md) when creating the actual monorepo.
- Read [deployment-modes.md](references/deployment-modes.md) before wiring production scripts or `@nestjs/serve-static`.
- Read [sources.md](references/sources.md) when updating this skill or checking why a rule exists.
