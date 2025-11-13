---
name: working-with-claude-code
description: Use when working with Claude Code CLI, plugins, hooks, MCP servers, skills, configuration, or any Claude Code feature - provides comprehensive official documentation for all aspects of Claude Code
allowed-tools:
  - Read
  - Grep
  - Bash
  - WebFetch
  - Write
---

# Working with Claude Code

Expert guidance for Claude Code CLI, providing comprehensive official documentation from docs.claude.com for all aspects of development and configuration.

## When to Use This Skill

Use this skill when you need help with:

- Creating or configuring Claude Code plugins, skills, hooks, or MCP servers
- Configuring Claude Code settings, CLI, or integrations (VS Code, JetBrains, CI/CD)
- Configuring networking, security, or enterprise features
- Troubleshooting Claude Code issues

## Quick Start

```bash
# Read plugin development guide
Read file="./references/plugins.md"

# Search across all documentation
Grep pattern="search-term" path="./references/"
```

## Available Resources

See `references/documentation-map.md` for complete listing of 45+ reference files organized by category.

Key files:
- `plugins.md`, `skills.md`, `mcp.md`, `hooks.md`: Core development
- `setup.md`, `settings.md`, `cli-reference.md`: Configuration
- `vs-code.md`, `github-actions.md`: Integrations
- `troubleshooting.md`: Common issues

## Workflow

1. Check `documentation-map.md` for relevant files
2. Read specific file: `./references/filename.md`
3. Apply solution from official documentation

For uncertain topics, search: `Grep pattern="term" path="./references/"`
