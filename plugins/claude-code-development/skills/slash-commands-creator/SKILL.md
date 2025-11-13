---
name: slash-commands-creator
description: Create and review Claude Code slash commands. Use when creating `/...` commands, reviewing syntax, or standardizing command definitions with proper argument handling and permissions.
trigger: Use when developers need to create `/...` commands, review slash command syntax, or maintain command standards.
author: n/a
---

# Slash Commands Creator

Expert assistance for creating, reviewing, and maintaining Claude Code custom slash commands based on official guidelines.

## When to Use This Skill

Use this skill when you need help with:

- Creating new `/...` slash commands
- Reviewing existing command syntax and structure
- Standardizing command definitions
- Implementing argument handling (`$ARGUMENTS`, `$1`, `$2`)
- Configuring `allowed-tools` permissions
- Choosing between project, personal, or plugin commands

## Quick Start

```markdown
---
description: Brief description of command purpose
---

Instructions for Claude to follow when command runs.
Use $ARGUMENTS for free-form input or $1, $2 for structured params.
```

See `references/examples.md` for complete examples with arguments, tools, and context handling.

## Available Resources

See `references/` for comprehensive documentation:

- **command-creation-workflow.md**: Step-by-step process for creating commands
- **examples.md**: Real-world command examples and patterns

For complete slash command syntax, see:
- `@plugins/claude-code-development/skills/working-with-claude-code/references/slash-commands.md`
