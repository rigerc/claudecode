---
description: Create a new Claude Code Skill using the skill-creator skill
argument-hint: [skill-name] "[skill-description]"
allowed-tools: Read, Write, Bash
---

# Create a new Skill

This command helps you create a new Claude Code Skill using the skill-creator skill.

## Skill Details:
- **Name**: $1
- **Description**: $ARGUMENTS

I'll help you create a new Skill called "$1" with the description "$ARGUMENTS". First, let me reference the official documentation to ensure we follow best practices.

Use the skill-creator skill to understand how to create Skills properly, then create the Skill directory structure and files.

The process should be:
1. Use the skill-creator skill to get Skill creation guidance
2. Create the Skill directory at `.claude/skills/$1/` (project) or `~/.claude/skills/$1/` (personal)
3. Create a proper SKILL.md file with YAML frontmatter including the provided description
4. Add any supporting files if needed
5. Verify the Skill structure is correct

Ask the user whether they want a project-level Skill (shared with team) or personal Skill (just for them), then create accordingly with the provided description.