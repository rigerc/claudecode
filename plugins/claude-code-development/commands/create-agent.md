---
description: Create a new Claude Code agent or sub-agent using the working-with-claude-code skill
argument-hint: [agent-name] "[agent-description]"
allowed-tools: Read, Write, Bash
---

# Create a new Agent/Sub-agent

This command helps you create a new Claude Code agent or sub-agent using the official documentation from the working-with-claude-code skill.

## Agent Details:
- **Name**: $1
- **Description**: $ARGUMENTS

I'll help you create a new agent/sub-agent called "$1" with the description "$ARGUMENTS". First, let me reference the official documentation to ensure we follow best practices.

Use the working-with-claude-code skill to understand how to create agents/sub-agents properly, then create the agent configuration.

The process should be:
1. Use the working-with-claude-code skill to get agent creation guidance
2. Ask whether they want a project-level agent (`.claude/agents/`) or personal agent (`~/.claude/agents/`)
3. Create the agent file with proper YAML frontmatter (name, description, tools, model) including the provided description
4. Write the system prompt with clear instructions and expertise definition
5. Include specific guidance on when Claude should use this agent
6. Verify the agent configuration is correct

Ask the user about what tools the agent should have access to and when it should be invoked, then create the agent accordingly with the provided description.