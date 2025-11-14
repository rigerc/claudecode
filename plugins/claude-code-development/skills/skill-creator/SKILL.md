---
name: skill-creator
description: Use when creating or updating Claude Code skills that extend capabilities with specialized knowledge and workflows.
license: Complete terms in LICENSE.txt
---

# Skill Creator

Create effective Claude Skills using progressive disclosure.

## Quick Start

1. Ask user location (Project/User/Project Plugin) via AskUserQuestion
2. Use `claude-skills-cli` skill to create & validate
3. Keep SKILL.md under 50 lines, move details to references/

## When to Create

- Repeating context across conversations
- Domain expertise needed repeatedly
- On request

## Progressive Disclosure

Three levels: **Metadata** (~27 tokens) → **SKILL.md** (<50 lines) →
**references/** (unlimited)

Keep Levels 1 & 2 lean. Move details to Level 3.

## Structure

```
my-skill/
├── SKILL.md       # Core instructions + metadata
├── references/    # Detailed docs (loaded as needed)
├── scripts/       # Executable operations
└── assets/        # Templates, images, files
```

## Workflow

**Location** (use AskUserQuestion): Project (`.claude/skills/`), User
(`~/.claude/skills/`), or Plugin (`plugins/<plugin>/skills/`)

**Validation**: Always use `claude-skills-cli` skill after creation.

**Packaging**: Optional - only for sharing/uploading.

## References

- [quick-start.md](references/quick-start.md) - First skill walkthrough
- [writing-guide.md](references/writing-guide.md) - Writing effective skills
- [development-process.md](references/development-process.md) - 7-step workflow
- [skill-examples.md](references/skill-examples.md) - Patterns & examples
- [cli-reference.md](references/cli-reference.md) - CLI tool usage
- [anthropic-resources.md](references/anthropic-resources.md) - Official docs
