---
name: library-researcher
description: Use for researching libraries and frameworks. Provides documentation and best practices via Context7.
allowed-tools:
  - Read
  - Write
  - Edit
  - Grep
  - WebFetch
  - WebSearch
  - mcp__context7__resolve-library-id
  - mcp__context7__get-library-docs
---

# Library Researcher

Expert assistance for researching software libraries, frameworks, APIs, and development tools using the Context7 documentation system.

## When to Use This Skill

Use this skill when you need help with:

- Understanding how to use a specific library or framework
- Comparing different libraries for the same purpose
- Finding documentation, examples, and best practices
- Researching API specifications and usage patterns
- Understanding integration requirements and dependencies
- Finding alternative tools or libraries for specific needs

## Quick Start

```bash
# 1. Resolve library name to Context7 ID
mcp__context7__resolve-library-id "react"

# 2. Get comprehensive documentation
mcp__context7__get-library-docs "/facebook/react" "getting-started,hooks"

# 3. Research and provide recommendations
```

## Available Resources

See `references/` for comprehensive documentation:

- **research_workflow.md**: Complete research process and usage patterns
- **templates.md**: Analysis and comparison templates for common scenarios
- **advanced_techniques.md**: Context7 advanced usage and integration examples
- **best_practices.md**: Research quality guidelines and efficiency tips
- **troubleshooting.md**: Common issues, debugging, and getting help
