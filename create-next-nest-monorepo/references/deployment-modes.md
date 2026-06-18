# Deployment Modes

The generated monorepo should support two deployment modes.

## Mode A: Separate Frontend and Backend Services

Use this as the default production recommendation.

Best fit:

- Next.js SSR, Server Components with dynamic rendering, Server Actions, ISR, image optimization, middleware, or route handlers.
- Deployments to Vercel, containers, Kubernetes, or separate web/API services.
- Independent frontend/backend scaling.

Build flow:

```bash
pnpm --filter frontend build
pnpm --filter backend build
```

Runtime:

```bash
pnpm --filter frontend start
pnpm --filter backend start
```

Rules:

- Frontend calls backend through an environment variable such as `NEXT_PUBLIC_API_BASE_URL`.
- Backend runs on its own `PORT`.
- Backend global prefix remains `api`, and Swagger stays at `/api/docs`.

## Mode B: Nest Backend Serves Static Next Export

Use this only when the frontend is compatible with static export.

Best fit:

- A single deployable server/container is required.
- Frontend routes can be generated to static HTML/CSS/JS.
- API is served by Nest under `/api`.

Required frontend config:

```ts
// apps/frontend/next.config.ts
import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  output: process.env.NEXT_OUTPUT === "export" ? "export" : undefined,
  transpilePackages: ["@repo/shared"]
};

export default nextConfig;
```

Build flow:

```bash
NEXT_OUTPUT=export pnpm --filter frontend build
pnpm --filter backend build
```

Deployment packaging:

- Copy `apps/frontend/out/**` into the backend runtime image.
- Point `ServeStaticModule.rootPath` at that copied directory.
- Set `SERVE_FRONTEND=true` in the backend environment.

Runtime:

```bash
SERVE_FRONTEND=true pnpm --filter backend start
```

Rules:

- Use `app.setGlobalPrefix("api")` in Nest.
- Configure `ServeStaticModule` with `exclude: ["/api*"]`.
- Keep health and docs under the API prefix: `/api/health`, `/api/docs`.
- Do not use this mode for SSR-only Next features.

## Unsupported Claim to Avoid

Do not say "Nest can serve a Next.js App Router app" without qualification. Nest can serve static files. A normal Next.js production app may require a Next runtime, not just static middleware.
