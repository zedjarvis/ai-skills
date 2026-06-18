# Skill Repository Instructions

This repository is a skills library. Each skill must live in its own top-level folder named after the skill, using lowercase hyphen-case.

## Repository Shape

Use this layout:

```text
skill-name/
  SKILL.md
  scripts/      # optional executable helpers
  references/   # optional focused docs loaded only when needed
  assets/       # optional templates or static files used in outputs
```

Rules:

- Keep one skill per folder.
- Name the folder exactly the same as the `name` field in `SKILL.md`.
- Use only lowercase letters, numbers, and hyphens in skill names.
- Do not create broad catch-all skills. Prefer one focused skill that does one job well.
- Do not add extra documentation files such as `README.md`, `CHANGELOG.md`, or `QUICK_REFERENCE.md` inside skills unless the user explicitly asks.

## Required Skill Format

Every skill must contain a `SKILL.md` file with YAML frontmatter followed by Markdown instructions:

```markdown
---
name: skill-name
description: Clear description of what the skill does and when to use it. Include trigger words and realistic user intents.
---

# Skill Name

Follow these steps...
```

Frontmatter requirements:

- `name` is required, must match the folder name, and must be 1-64 characters.
- `description` is required, must be non-empty, and should stay under 1024 characters.
- Do not add optional frontmatter fields unless they are useful for this specific skill.

## Skill Creation Standard

When creating or updating a skill:

1. Clarify the job the skill should do with concrete examples from the user or the codebase.
2. Browse the web for current, verifiable best practices for the skill's subject unless the user explicitly forbids browsing.
3. Prefer primary or authoritative sources: official documentation, standards, vendor docs, maintainers' guides, research papers, reputable engineering posts, and established security or accessibility guidance.
4. Record the sources used inside `references/sources.md` when web research materially shaped the skill.
5. Convert the research into practical instructions. Avoid vague lines like "follow best practices" unless the specific practices are listed.
6. Keep `SKILL.md` concise. Put detailed framework notes, API references, or source summaries in focused files under `references/`.
7. Add scripts only when deterministic execution is better than rewriting code each time.
8. Validate the skill before finishing.

## Quality Bar

Skills should be easy to read and useful in real work:

- Write imperative instructions.
- Include defaults, decision rules, and gotchas.
- Use checklists for workflows with multiple steps.
- Use examples only when they remove ambiguity.
- Prefer real commands and exact file paths over abstract advice.
- Make validation explicit: lint, typecheck, tests, manual review, eval cases, or source verification as appropriate.
- Include human checkpoints for destructive operations, credential handling, production changes, purchases, or irreversible actions.

## Research Expectations

Do not generate AI-slop skills from memory alone. For every non-trivial skill, gather current source material first.

Minimum source standard:

- At least one official source for the main tool, framework, platform, or domain.
- At least one implementation-quality source when available, such as an engineering guide, standard, security guideline, or maintainer recommendation.
- For fast-changing topics, use current docs and record the access date.

Treat source material as evidence, not filler. The final skill should explain what to do, not summarize the internet.

## Agent Skills References

This repository follows the Agent Skills format:

- Overview: https://agentskills.io/home
- Specification: https://agentskills.io/specification
- Quickstart: https://agentskills.io/skill-creation/quickstart
- Best practices: https://agentskills.io/skill-creation/best-practices
- Optimizing descriptions: https://agentskills.io/skill-creation/optimizing-descriptions
- Evaluating skills: https://agentskills.io/skill-creation/evaluating-skills
- Using scripts: https://agentskills.io/skill-creation/using-scripts
- Adding skills support: https://agentskills.io/client-implementation/adding-skills-support

## Current Starter Skill

Use `create-skills/` when the user wants to create, improve, evaluate, or organize skills in this repository.
