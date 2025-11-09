---
description: Create a new Claude Code slash command using the working-with-claude-code skill
argument-hint: [command-name] "[command-description]"
allowed-tools: Read, Write, Bash
---

# Create a new Slash Command

This command helps you create a new Claude Code slash command using the official documentation from the working-with-claude-code skill.

## Command Details:
- **Name**: /$1
- **Description**: $ARGUMENTS

I'll help you create a new slash command called "/$1" with the description "$ARGUMENTS". First, let me reference the official documentation to ensure we follow best practices.

Use the working-with-claude-code skill to understand how to create slash commands properly, then create the command file.

The process should be:
1. Use the working-with-claude-code skill to get slash command creation guidance
2. Ask whether they want a project-level command (`.claude/commands/`) or personal command (`~/.claude/commands/`)
3. Create the command file at the appropriate location
4. Include proper frontmatter with the provided description, allowed-tools, etc.
5. Add the command content with argument placeholders ($1, $2, $ARGUMENTS)
6. Verify the command structure is correct

Ask the user about the command's purpose and whether they need arguments, then create the command accordingly with the provided description.