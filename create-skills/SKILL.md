---
name: create-skills
description: Create, update, organize, research, and validate Agent Skills in this repository. Use when the user asks to create a new skill, improve an existing skill, turn a workflow into a reusable skill, add scripts/references/assets to a skill, optimize skill descriptions, evaluate skill quality, or maintain a folder-based skills library.
---

# Create Skills

Use this skill to create practical Agent Skills that are grounded in verifiable sources and usable by future agents.

## Workflow

1. Understand the requested skill.
   - Identify the user goal, target users, trigger phrases, expected outputs, and likely edge cases.
   - Ask only when a missing answer would make the skill unsafe or mis-scoped.
   - Prefer a narrow skill over a broad one.

2. Research before writing.
   - Browse for current best practices unless the user explicitly forbids browsing.
   - Prefer official docs, standards, maintainer docs, security guidance, reputable engineering posts, and research papers.
   - For tool/framework skills, use the official documentation as the primary source.
   - For fast-changing domains, verify current versions, APIs, and dates.
   - Save material source links in `references/sources.md` for the skill when research materially shapes the instructions.

3. Design the skill folder.
   - Create a top-level folder named with lowercase hyphen-case.
   - Match the folder name exactly in `SKILL.md` frontmatter `name`.
   - Add only resource directories that the skill needs:
     - `references/` for focused domain notes, API details, source summaries, or examples.
     - `scripts/` for deterministic repeatable commands.
     - `assets/` for templates and static files used in outputs.

4. Write `SKILL.md`.
   - Keep the body concise and operational.
   - Put all trigger logic in the frontmatter `description`.
   - Describe what to do, what to avoid, and how to validate the result.
   - Use imperative instructions, concrete defaults, and short checklists.
   - Link to reference files with relative paths when extra detail is optional.

5. Add reusable resources when useful.
   - Add scripts when repeated code, parsing, generation, validation, or formatting must be reliable.
   - Scripts must support non-interactive use and a `--help` path when practical.
   - Prefer structured output for scripts that agents will parse.
   - Test scripts before finishing.

6. Validate the skill.
   - Run `create-skills/scripts/validate_skill.py <skill-folder>` when available.
   - Check that `name` matches the folder, the description is specific, and referenced files exist.
   - For complex skills, add 2-3 realistic eval prompts in `references/evals.md` or another focused reference file.
   - Use the skill on a realistic prompt when practical, then tighten weak instructions.

## Description Checklist

A good `description`:

- Says what the skill does.
- Says when to use it, using realistic trigger language.
- Mentions key file types, frameworks, platforms, domains, or workflows.
- Is specific enough to avoid false triggers.
- Avoids generic wording such as "helps with development" or "improves productivity."

## Source Checklist

Use `references/sources.md` with this format:

```markdown
# Sources

- Title: URL
  - Accessed: YYYY-MM-DD
  - Use: Short note on how this source shaped the skill.
```

Do not paste long copied content. Capture the implementation-relevant points in your own words.

## Validation Checklist

Before finishing a skill, confirm:

- The skill folder name is lowercase hyphen-case.
- `SKILL.md` exists.
- Frontmatter has `name` and `description`.
- `name` matches the folder.
- The description explains both capability and trigger conditions.
- Detailed source notes are in `references/`, not stuffed into `SKILL.md`.
- Scripts are executable or have clear interpreter commands.
- Any referenced files exist.
- The final answer reports created/changed files and validation performed.

## Gotchas

- Do not create a skill from generic AI memory when current source material is available.
- Do not overfill `SKILL.md`; use progressive disclosure through references.
- Do not make one mega-skill for unrelated workflows.
- Do not add placeholder directories or files.
- Do not include secrets, tokens, private keys, or live credentials in a skill.
