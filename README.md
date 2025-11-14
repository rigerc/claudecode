# Claude Extensions Plugin Collection

A curated collection of specialized plugins for Claude Code, organized by functionality to provide focused tools for specific development tasks.

## Overview

- **12 Specialized Plugins**
- **11 Custom Commands**
- **10 Expert Agents**
- **23 Specialized Skills**
- **2 Hooks**
- **0 MCP Servers**

## Available Plugins

| Plugin | Commands | Agents | Skills | Hooks | MCP | Focus |
|--------|----------|---------|---------|-------|-----|-------|
| **Markdowntaskmanager** | 0 | 0 | 1 | 1 | 0 | General |
| **Bash Scripting** | 0 | 1 | 1 | 0 | 0 | Shell automation |
| **Claude Code Development** | 5 | 4 | 6 | 0 | 0 | Extending Claude Code |
| **Code Quality** | 2 | 1 | 0 | 0 | 0 | Code review |
| **Documentation Generation** | 1 | 3 | 2 | 0 | 0 | Technical writing |
| **Flatban** | 1 | 0 | 0 | 0 | 0 | General |
| **Go Development** | 0 | 1 | 10 | 0 | 0 | Go programming |
| **Home Assistant** | 0 | 0 | 1 | 0 | 0 | General |
| **Library Researcher** | 0 | 0 | 1 | 0 | 0 | General |
| **Marketplace Updater** | 0 | 0 | 0 | 1 | 0 | General |
| **Music Management** | 0 | 0 | 1 | 0 | 0 | Beets tool |
| **Productivity Tools** | 2 | 0 | 0 | 0 | 0 | Workflow enhancement |

## Plugin Details

### Markdowntaskmanager
A comprehensive AI-driven task management system that brings discipline and transparency to your development workflow. This plugin implements a Kanban-style task management system using local Markd...

**Components**: 1 skills, 1 hooks

**Install**: `MarkdownTaskManager@rigerc-claude`

### Bash Scripting
Expert tools for Bash scripting, automation, and testing with bats-core framework.

**Components**: 1 agents, 1 skills

**Install**: `bash-scripting@rigerc-claude`

### Claude Code Development
Tools for developing and extending Claude Code with custom agents, commands, skills, and hooks.

**Components**: 5 commands, 4 agents, 6 skills

**Install**: `claude-code-development@rigerc-claude`

### Code Quality
Code review, refactoring, and quality analysis tools for improving code maintainability and security.

**Components**: 2 commands, 1 agents

**Install**: `code-quality@rigerc-claude`

### Documentation Generation
Comprehensive tools for generating API documentation, technical docs, and project documentation.

**Components**: 1 commands, 3 agents, 2 skills

**Install**: `documentation-generation@rigerc-claude`

### Flatban
A Claude Code plugin that enables integration with [Flatban](https://github.com/gelform/flatban) - a filesystem-based Kanban project management system designed for AI-assisted development.

**Components**: 1 commands

**Install**: `flatban@rigerc-claude`

### Go Development
Specialized tools for Go development with goroutines, channels, interfaces, and idiomatic patterns.

**Components**: 1 agents, 10 skills

**Install**: `go-development@rigerc-claude`

### Home Assistant
A comprehensive Claude Code plugin for Home Assistant development, providing tools and skills for creating add-ons, integrations, and smart home automation workflows.

**Components**: 1 skills

**Install**: `home-assistant@rigerc-claude`

### Library Researcher
**Advanced library research and documentation analysis plugin for Claude Code** The Library Researcher plugin provides powerful tools for researching, analyzing, and documenting software libraries,...

**Components**: 1 skills

**Install**: `library-researcher@rigerc-claude`

### Marketplace Updater
Automatically checks if repositories in `~/.claude/plugins/` are up to date and informs you when updates are available.

**Components**: 1 hooks

**Install**: `marketplace-updater@rigerc-claude`

### Music Management
Comprehensive music library management system guidance using the beets music organization tool.

**Components**: 1 skills

**Install**: `music-management@rigerc-claude`

### Productivity Tools
Productivity enhancement tools including feature brainstorming, prompt enhancement, and dotfile management.

**Components**: 2 commands

**Install**: `productivity-tools@rigerc-claude`


## Installation

### Add the Marketplace

First, add this collection to your Claude Code marketplaces:

```bash
/plugin marketplace add rigerc/claudecode
```

### Install Individual Plugins

Install only the plugins you need:

```bash
# Example installations
/plugin install claude-code-development@rigerc-claude
/plugin install bash-scripting@rigerc-claude
/plugin install documentation-generation@rigerc-claude
```

### Browse Available Plugins

```bash
/plugin
# Select "Browse Plugins" from rigerc-claude marketplace
# Install desired plugins
```

## Plugin Structure

Each plugin follows the standard Claude Code plugin structure:

```
plugin-name/
├── .claude-plugin/
│   └── plugin.json          # Plugin metadata
├── commands/                 # Custom slash commands (optional)
├── agents/                   # Custom agents (optional)
├── skills/                   # Agent Skills (optional)
├── hooks/                    # Git hooks (optional)
├── mcp_servers/              # MCP server configurations (optional)
└── README.md                 # Plugin documentation
```

## Development

This collection is automatically generated from the `plugins/` directory. When adding or modifying plugins:

1. Create/modify plugin directories in `plugins/`
2. Run the build script: `python scripts/build-marketplace.py`
3. Commit the generated `.claude-plugin/marketplace.json` and `README.md`

### Building

```bash
# Build marketplace and README
python scripts/build-marketplace.py

# The script will:
# - Scan plugins/ directory
# - Generate .claude-plugin/marketplace.json
# - Update this README.md
# - Generate individual plugin READMEs
```

### Plugin Categories

- **Development Tools**: For extending Claude Code and development workflows
- **Language Specific**: Targeted tools for specific programming languages
- **Documentation**: Comprehensive documentation generation and writing tools
- **Quality & Review**: Code analysis, review, and improvement tools
- **Productivity**: General productivity enhancement tools
- **Specialized**: Domain-specific tools for particular use cases

## License

All plugins in this collection are licensed under MIT License.

---

*This README is automatically generated. Do not edit manually - run `python scripts/build-marketplace.py` to update.*
