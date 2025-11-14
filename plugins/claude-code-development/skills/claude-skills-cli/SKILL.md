---
name: claude-skills-cli
description: Create and manage Claude Agent Skills with progressive disclosure validation. Use for building and validating skill structure and activation.
allowed-tools: Bash, Write, Read, Edit, Glob
---

# Claude Skills CLI

Expert assistance for creating, validating, and managing Claude Agent Skills using the claude-skills-cli tool with progressive disclosure validation.

## When to Use

- Creating Claude Agent Skills with proper structure
- Validating skill format and progressive disclosure compliance
- Setting up reliable skill activation with hooks
- Managing skill locations (project/personal/plugin)

## Quick Start

```bash
# Create and validate skill
npx claude-skills-cli init --name my-skill --description "Brief description with trigger keywords"
# Or create at specific path:
npx claude-skills-cli init --path .claude/skills/my-skill --description "Brief description with trigger keywords"
npx claude-skills-cli validate .claude/skills/my-skill

# Add activation hook and fix issues
npx claude-skills-cli add-hook --project
npx claude-skills-cli doctor .claude/skills/my-skill
```

## References

See `references/` for detailed documentation:
- `detailed-guide.md` - Complete workflows and best practices
- `validation-rules.md` - Progressive disclosure constraints
- `command-examples.md` - Real-world CLI usage
- `progressive-disclosure.md` - Architecture details
