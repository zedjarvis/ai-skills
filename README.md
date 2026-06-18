# AI Skills

Reusable Agent Skills for AI-assisted software development.

Each skill lives in its own top-level folder and contains a required `SKILL.md` file plus optional `references/`, `scripts/`, and `assets/` directories. The repository is organized this way so agents can load only the skill they need without pulling unrelated context into a working session.

## Skills

| Skill | Purpose |
| --- | --- |
| `create-skills` | Create, update, research, and validate new Agent Skills in this repository. |
| `create-next-nest-monorepo` | Scaffold or review a pnpm/Turborepo full-stack TypeScript monorepo with Next.js, shadcn/ui, NestJS, Swagger, Terminus, and shared packages. |
| `write-readable-typescript` | Write and review TypeScript for clear names, small functions, focused files, and maintainable structure. |

## Repository Rules

- Keep one skill per folder.
- Name each skill folder with lowercase hyphen-case.
- Match the folder name exactly in `SKILL.md` frontmatter `name`.
- Keep `SKILL.md` concise and operational.
- Put detailed source notes or examples in `references/`.
- Put deterministic helpers in `scripts/`.
- Browse and cite verifiable sources before creating non-trivial skills.

See [AGENTS.md](AGENTS.md) for the full agent operating instructions.

## Validate Skills

Run the local validator against any skill folder:

```bash
create-skills/scripts/validate_skill.py create-skills
create-skills/scripts/validate_skill.py create-next-nest-monorepo
create-skills/scripts/validate_skill.py write-readable-typescript
```

## Useful Scripts

Validate a generated Next/Nest monorepo:

```bash
create-next-nest-monorepo/scripts/validate_monorepo.py /path/to/generated/repo
```

Scan TypeScript/JavaScript code for long files and approximate long functions:

```bash
write-readable-typescript/scripts/check_code_shape.py /path/to/project
```

## Source Standard

Skills in this repository should not be generated from memory alone when current documentation exists. Use official docs, standards, maintainer guides, reputable engineering posts, or research papers, then translate that evidence into practical instructions.
