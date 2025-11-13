---
name: plugin-creator
description: Use when creating or developing Claude Code plugins. Scaffolds structure, adds components, sets up development environments, and provides guidance on plugin architecture and best practices.
---

# Plugin Creator

Expert assistance for creating Claude Code plugins - modular packages that extend Claude Code with custom slash commands, specialized agents, reusable skills, event hooks, and external service integrations.

## When to Use This Skill

Use this skill when you need help with:

- Creating a new Claude Code plugin from scratch
- Adding components to an existing plugin (commands, agents, skills, hooks, MCP servers)
- Setting up plugin development environments
- Understanding plugin structure and best practices
- Testing, validating, or distributing plugins

## Quick Start

```bash
# Scaffold a new plugin
python scripts/init_plugin.py <plugin-name>

# Install for local testing
claude plugin install <plugin-name>@local-dev

# Validate plugin structure
claude plugin validate
```

## Development Workflow

1. **Understanding** - Gather 2-3 concrete examples of plugin usage
2. **Planning** - Determine needed components (commands, agents, skills, hooks, MCP servers)
3. **Implementation** - Execute `python scripts/init_plugin.py <plugin-name>` to scaffold
4. **Customization** - Customize components, remove unused ones, update metadata
5. **Testing** - Install via local marketplace, validate, and iterate

## Available Resources

See `references/` for comprehensive documentation:

- **component-specifications.md**: Detailed specs for all component types and plugin manifest schema
- **component-examples.md**: Real-world implementations for commands, agents, skills, hooks, and MCP servers
- **development-workflow.md**: Testing, validation, and distribution procedures (Phases 0-5)
- **pattern-library.md**: Advanced implementation patterns, CRUD patterns, progressive loading, hook chains
- **plugin-json-examples.md**: Plugin.json structure reference (minimal, standard, advanced)
- **troubleshooting.md**: Common validation errors and structural issues with solutions
- **marketplace-guide.md**: Distribution setup, marketplace creation, git setup, publishing

See `assets/` for component templates and `scripts/init_plugin.py` for scaffolding tool.
