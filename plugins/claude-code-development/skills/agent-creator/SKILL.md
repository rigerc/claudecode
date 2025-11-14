---
name: agent-creator
# IMPORTANT: Keep description on ONE line for Claude Code compatibility
# prettier-ignore
description: Use when creating or updating Claude Code subagents. Provides expertise in agent configuration, system prompts, and workflow design.
---

# Agent Creator

Expert in creating and managing Claude Code subagents with proper configuration, focused system prompts, and effective tool permissions.

## Quick Start

Create a subagent with this structure:

```markdown
---
name: your-agent-name
description: When to use this agent (include "PROACTIVELY" for auto-invocation)
tools: Read, Write, Edit, Bash  # Optional - omit to inherit all tools
model: sonnet  # Optional - sonnet/opus/haiku/inherit
---

[System prompt with specific instructions, best practices, and constraints]
```

## Core Principles

- **Focused purpose**: Single, clear responsibility per agent
- **Detailed prompts**: Include examples, constraints, and approach
- **Minimal tools**: Grant only necessary permissions
- **Proactive triggers**: Use "PROACTIVELY" or "MUST BE USED" in description

## Agent Creation Workflow

1. **Location**: Choose project (`.claude/agents/`) or user (`~/.claude/agents/`)
2. **Generate**: Recommended - use Claude to generate initial version, then customize
3. **Configure**: Set name, description, tools, and model
4. **Prompt**: Write detailed system prompt with role, capabilities, and process
5. **Test**: Invoke explicitly first: "Use the X agent to..."

## Reference Files

- [agent-structure.md](references/agent-structure.md) - File format and configuration
- [best-practices.md](references/best-practices.md) - Design patterns and tips
- [examples.md](references/examples.md) - Complete agent examples

## Notes

- Use `/agents` command for interactive management with tool selection UI
- Project agents override user agents when names conflict
- Agents use separate context windows from main conversation
