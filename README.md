# Claude Extensions Plugin Collection

A curated collection of specialized plugins for Claude Code, organized by functionality to provide focused tools for specific development tasks.

## Overview

- **11 Specialized Plugins**
- **9 Custom Commands**
- **11 Expert Agents**
- **8 Specialized Skills**

## Available Plugins

| Plugin | Commands | Agents | Skills | Focus |
|--------|----------|---------|---------|-------|
| **Markdowntaskmanager** | 0 | 0 | 1 | General |
| **Bash Scripting** | 0 | 1 | 1 | Shell automation |
| **Claude Code Development** | 5 | 4 | 2 | Extending Claude Code |
| **Code Quality** | 2 | 1 | 0 | Code review |
| **Documentation Generation** | 1 | 3 | 2 | Technical writing |
| **Go Development** | 0 | 1 | 0 | Go programming |
| **Home Assistant** | 0 | 0 | 1 | General |
| **Marketplace Updater** | 0 | 0 | 0 | General |
| **Music Management** | 0 | 0 | 1 | Beets tool |
| **Productivity Tools** | 1 | 1 | 0 | Workflow enhancement |
| **Skills Auto Discovery** | 0 | 0 | 0 | General |

## Plugin Details

### Markdowntaskmanager
Kanban task management system using local Markdown files with comprehensive task lifecycle management

**Install**: `MarkdownTaskManager@rigerc-claude`

### Bash Scripting
Expert tools for Bash scripting, automation, and testing with bats-core framework

**Install**: `bash-scripting@rigerc-claude`

### Claude Code Development
Tools for developing and extending Claude Code with custom agents, commands, skills, and hooks

**Install**: `claude-code-development@rigerc-claude`

### Code Quality
Code review, refactoring, and quality analysis tools for improving code maintainability and security

**Install**: `code-quality@rigerc-claude`

### Documentation Generation
Comprehensive tools for generating API documentation, technical docs, and project documentation

**Install**: `documentation-generation@rigerc-claude`

### Go Development
Specialized tools for Go development with goroutines, channels, interfaces, and idiomatic patterns

**Install**: `go-development@rigerc-claude`

### Home Assistant
Home Assistant development tools and automation skills for creating add-ons, integrations, and smart home workflows

**Install**: `home-assistant@rigerc-claude`

### Marketplace Updater
Automatic marketplace metadata updater that checks for updates on Claude Code startup

**Install**: `marketplace-updater@rigerc-claude`

### Music Management
Comprehensive music library management system guidance using the beets music organization tool

**Install**: `music-management@rigerc-claude`

### Productivity Tools
Productivity enhancement tools including feature brainstorming and dotfile management

**Install**: `productivity-tools@rigerc-claude`

### Skills Auto Discovery
Automatically discovers and injects all available skills into session context at startup

**Install**: `skills-auto-discovery@rigerc-claude`


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
