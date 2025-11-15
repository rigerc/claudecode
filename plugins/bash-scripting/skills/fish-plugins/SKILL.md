---
name: fish-plugins
description: Use when creating Fish shell plugins, functions, completions, or managing Fish shell configurations
version: 1.0.0
author: Claude Code
---

# Fish Shell Plugins

Expert Fish shell plugin development with progressive disclosure guidance.

## Quick Start
Create Fish functions, completions, and configuration. Use `fish-plugin create <name>` to scaffold.

## Commands
- `fish-plugin create <name>` - Create new plugin scaffold
- `fish-plugin completion <command>` - Generate completions
- `fish-plugin validate` - Check plugin structure
- `fish-plugin install <name>` - Install from template

## Examples
```fish
fish-plugin create my-tool      # Creates plugin structure
fish-plugin completion docker   # Generate docker completions
```

## What I Need
Plugin name, command description, desired functionality.

## Reference
`references/fish-guide.md` - Complete Fish shell documentation
`references/templates.md` - Plugin templates and examples
`scripts/fish-plugin` - Plugin management CLI tool