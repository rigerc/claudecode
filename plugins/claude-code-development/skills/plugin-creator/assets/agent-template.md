---
description: Specialized agent for [specific domain/task]. Delegates when [trigger conditions].
---

# Agent Name

Specialized agent for [specific task type or domain].

## When to Delegate

Claude delegates automatically when:
- [Specific pattern or requirement]
- [Specific task type]
- [Specific context]

## Capabilities

1. [Capability 1]
2. [Capability 2]
3. [Capability 3]

## Instructions

When delegated to this agent:

1. **Analyze request** - Understand requirements and scope
2. **Execute task** - Perform specialized work
3. **Report results** - Provide clear summary and findings

## Optional Frontmatter Fields

```yaml
description: What agent does and when to delegate (required)
tools: Read, Grep, Bash  # Restrict available tools
model: sonnet  # Options: sonnet, haiku, opus, inherit
```

## Best Practices

- **Single responsibility** - Focus on one specific task type
- **Minimal tools** - Only tools needed for the job
- **Clear triggers** - Specific delegation conditions in description
- **Efficient model** - Use haiku for simple tasks, sonnet for balanced, opus for complex
