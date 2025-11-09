---
description: Create a new Claude Code hook using the working-with-claude-code skill
argument-hint: [hook-event] "[hook-purpose]"
allowed-tools: Read, Write, Bash
---

# Create a new Hook

This command helps you create a new Claude Code hook using the official documentation from the working-with-claude-code skill.

## Hook Details:
- **Event**: $1
- **Purpose**: $ARGUMENTS

I'll help you create a new hook for the "$1" event with the purpose "$ARGUMENTS". First, let me reference the official documentation to ensure we follow best practices.

Use the working-with-claude-code skill to understand how to create hooks properly, then create the hook configuration.

The process should be:
1. Use the working-with-claude-code skill to get hook creation guidance
2. Understand the specific hook event ($1) and its input/output format
3. Ask whether they want to modify project settings (`.claude/settings.json`) or user settings (`~/.claude/settings.json`)
4. Create or update the settings file with the hook configuration
5. Include proper matcher patterns for tool-based hooks
6. Create any hook scripts if needed
7. Verify the hook configuration is correct

Ask the user about which tools/events the hook should match and whether they need a custom script, then create the hook accordingly based on the stated purpose.