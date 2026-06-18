# Scaffold Guide

Use this guide to generate a starter monorepo. Verify current CLI flags before running commands in a fresh project.

## Root Workspace

Create the repo and initialize pnpm:

```bash
mkdir my-monorepo
cd my-monorepo
pnpm init
```

Create `pnpm-workspace.yaml`:

```yaml
packages:
  - "apps/*"
  - "packages/*"
```

Create root `package.json` shape:

```json
{
  "name": "my-monorepo",
  "private": true,
  "packageManager": "pnpm@latest",
  "scripts": {
    "dev": "turbo run dev",
    "build": "turbo run build",
    "lint": "turbo run lint",
    "typecheck": "turbo run typecheck",
    "format": "prettier --write .",
    "deploy:backend-static": "pnpm build && pnpm --filter backend build:with-frontend"
  },
  "devDependencies": {
    "prettier": "latest",
    "turbo": "latest",
    "typescript": "latest"
  }
}
```

Create `turbo.json` with the current `tasks` key:

```json
{
  "$schema": "https://turbo.build/schema.json",
  "tasks": {
    "build": {
      "dependsOn": ["^build"],
      "outputs": ["dist/**", ".next/**", "!.next/cache/**", "out/**"]
    },
    "lint": {
      "dependsOn": ["^lint"]
    },
    "typecheck": {
      "dependsOn": ["^typecheck"]
    },
    "dev": {
      "cache": false,
      "persistent": true
    }
  }
}
```

## Shared TypeScript Config

Create `packages/ts-config/package.json`:

```json
{
  "name": "@repo/ts-config",
  "version": "0.0.0",
  "private": true,
  "exports": {
    "./base": "./base.json",
    "./next": "./next.json",
    "./nest": "./nest.json"
  }
}
```

Create `packages/ts-config/base.json`:

```json
{
  "compilerOptions": {
    "target": "ES2022",
    "lib": ["ES2022"],
    "strict": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true,
    "esModuleInterop": true,
    "moduleResolution": "Bundler",
    "resolveJsonModule": true,
    "isolatedModules": true
  }
}
```

Create `packages/ts-config/next.json`:

```json
{
  "extends": "./base.json",
  "compilerOptions": {
    "jsx": "preserve",
    "allowJs": true,
    "noEmit": true,
    "incremental": true,
    "plugins": [{ "name": "next" }]
  }
}
```

Create `packages/ts-config/nest.json`:

```json
{
  "extends": "./base.json",
  "compilerOptions": {
    "module": "NodeNext",
    "moduleResolution": "NodeNext",
    "declaration": true,
    "sourceMap": true,
    "outDir": "./dist",
    "removeComments": true,
    "emitDecoratorMetadata": true,
    "experimentalDecorators": true,
    "allowSyntheticDefaultImports": true
  }
}
```

## Shared Package

Create `packages/shared/package.json`:

```json
{
  "name": "@repo/shared",
  "version": "0.0.0",
  "private": true,
  "type": "module",
  "exports": {
    ".": "./src/index.ts"
  },
  "scripts": {
    "typecheck": "tsc --noEmit"
  },
  "devDependencies": {
    "@repo/ts-config": "workspace:*",
    "typescript": "latest"
  },
  "dependencies": {
    "zod": "latest"
  }
}
```

Create `packages/shared/tsconfig.json`:

```json
{
  "extends": "@repo/ts-config/base",
  "compilerOptions": {
    "noEmit": true
  },
  "include": ["src"]
}
```

Create `packages/shared/src/index.ts`:

```ts
import { z } from "zod";

export const userSchema = z.object({
  id: z.string(),
  name: z.string(),
  email: z.string().email()
});

export type User = z.infer<typeof userSchema>;

export type ApiResponse<T> = {
  data: T;
  error: string | null;
};
```

## Frontend: Next.js + shadcn/ui

Create the frontend with current official defaults:

```bash
pnpm create next-app@latest apps/frontend --yes
```

From `apps/frontend`, initialize shadcn/ui:

```bash
cd apps/frontend
pnpm dlx shadcn@latest init
pnpm dlx shadcn@latest add button
cd ../..
```

Update `apps/frontend/package.json`:

```json
{
  "name": "frontend",
  "private": true,
  "scripts": {
    "dev": "next dev --port 3000",
    "build": "next build",
    "build:static": "NEXT_OUTPUT=export next build",
    "lint": "next lint",
    "typecheck": "tsc --noEmit"
  },
  "dependencies": {
    "@repo/shared": "workspace:*"
  },
  "devDependencies": {
    "@repo/ts-config": "workspace:*"
  }
}
```

Use `transpilePackages` when importing raw TypeScript workspace packages from Next:

```ts
// apps/frontend/next.config.ts
import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  transpilePackages: ["@repo/shared"],
  output: process.env.NEXT_OUTPUT === "export" ? "export" : undefined
};

export default nextConfig;
```

Use shared contracts from the frontend:

```tsx
import type { User } from "@repo/shared";

const user: User = {
  id: "1",
  name: "Ada Lovelace",
  email: "ada@example.com"
};
```

## Backend: NestJS

Create the backend with Nest CLI or current official starter commands. In a pnpm monorepo, keep the Nest app under `apps/backend` and name the package `backend`.

Install backend dependencies:

```bash
pnpm --filter backend add @nestjs/swagger swagger-ui-express @nestjs/terminus @nestjs/serve-static
pnpm --filter backend add @repo/shared@workspace:*
pnpm --filter backend add -D @repo/ts-config@workspace:*
```

Use root-level dev orchestration, but keep backend scripts local:

```json
{
  "name": "backend",
  "private": true,
  "scripts": {
    "dev": "nest start --watch",
    "build": "nest build",
    "build:with-frontend": "pnpm --filter frontend build:static && nest build",
    "start": "node dist/main.js",
    "lint": "eslint .",
    "typecheck": "tsc --noEmit"
  },
  "dependencies": {
    "@repo/shared": "workspace:*"
  },
  "devDependencies": {
    "@repo/ts-config": "workspace:*"
  }
}
```

Configure Swagger and an API prefix in `apps/backend/src/main.ts`:

```ts
import { NestFactory } from "@nestjs/core";
import { DocumentBuilder, SwaggerModule } from "@nestjs/swagger";
import { AppModule } from "./app.module";

async function bootstrap() {
  const app = await NestFactory.create(AppModule);

  app.setGlobalPrefix("api", {
    exclude: process.env.SERVE_FRONTEND === "true" ? ["/"] : []
  });
  app.enableShutdownHooks();

  const config = new DocumentBuilder()
    .setTitle("Monorepo API")
    .setDescription("Backend API documentation")
    .setVersion("1.0.0")
    .build();
  const documentFactory = () => SwaggerModule.createDocument(app, config);
  SwaggerModule.setup("api/docs", app, documentFactory);

  await app.listen(process.env.PORT ?? 3001);
}

void bootstrap();
```

Create `apps/backend/src/health/health.module.ts`:

```ts
import { Module } from "@nestjs/common";
import { TerminusModule } from "@nestjs/terminus";
import { HealthController } from "./health.controller";

@Module({
  imports: [TerminusModule],
  controllers: [HealthController]
})
export class HealthModule {}
```

Create `apps/backend/src/health/health.controller.ts`:

```ts
import { Controller, Get } from "@nestjs/common";
import { HealthCheck, HealthCheckService, MemoryHealthIndicator } from "@nestjs/terminus";

@Controller("health")
export class HealthController {
  constructor(
    private readonly health: HealthCheckService,
    private readonly memory: MemoryHealthIndicator
  ) {}

  @Get()
  @HealthCheck()
  check() {
    return this.health.check([
      () => this.memory.checkHeap("memory_heap", 256 * 1024 * 1024)
    ]);
  }
}
```

Import `HealthModule` in `AppModule`.

## Backend-Hosted Static Frontend

Only add this when the user chooses backend-hosted deployment.

Install `@nestjs/serve-static`, then configure `ServeStaticModule` in `AppModule`:

```ts
import { Module } from "@nestjs/common";
import { ServeStaticModule } from "@nestjs/serve-static";
import { join } from "node:path";
import { HealthModule } from "./health/health.module";

const serveFrontend = process.env.SERVE_FRONTEND === "true";

@Module({
  imports: [
    ...(serveFrontend
      ? [
          ServeStaticModule.forRoot({
            rootPath: join(__dirname, "..", "..", "frontend"),
            exclude: ["/api*"]
          })
        ]
      : []),
    HealthModule
  ]
})
export class AppModule {}
```

Ensure the deployment build copies `apps/frontend/out` into the backend runtime image/path expected by `rootPath`. Do not point Nest at `.next` for SSR.

## Validation

Run these from the generated monorepo root:

```bash
pnpm install
pnpm typecheck
pnpm lint
pnpm build
pnpm dev
```

Check:

- Frontend dev server: `http://localhost:3000`
- Backend dev server: `http://localhost:3001`
- Swagger docs: `http://localhost:3001/api/docs`
- Health check: `http://localhost:3001/api/health`

From this skills repository, run:

```bash
create-next-nest-monorepo/scripts/validate_monorepo.py /path/to/generated/repo
```
