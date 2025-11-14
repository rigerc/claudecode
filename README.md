# Claude Extensions Plugin Collection

A curated collection of specialized plugins for Claude Code, organized by functionality to provide focused tools for specific development tasks.

## Overview

- **12 Specialized Plugins**
- **11 Custom Commands**
- **10 Expert Agents**
- **23 Specialized Skills**
- **2 Hooks**
- **0 MCP Servers**

## Plugin Details

### [Markdowntaskmanager](./plugins/MarkdownTaskManager/)
Kanban task management system using local Markdown files with comprehensive task lifecycle management

**Skills** (1):
- **markdown-task-manager**: Use to manage Kanban tasks using local Markdown files. Handles task creation, tracking, archival, and reporting.

**Hooks** (1):
- **SessionStart_0**: Hook for SessionStart

**Install**: `MarkdownTaskManager@rigerc-claude`

### [Bash Scripting](./plugins/bash-scripting/)
Expert tools for Bash scripting, automation, and testing with bats-core framework

**Agents** (1):
- **bash-scripting-expert**: Expert Bash scripting developer specializing in best practices, code review, optimization, and modern Bash patterns. Provides professional guidance...

**Skills** (1):
- **bats-tester**: Use when creating tests for bash scripts using bats-core. Provides expertise in test writing, setup, and best practices.

**Install**: `bash-scripting@rigerc-claude`

### [Claude Code Development](./plugins/claude-code-development/)
Tools for developing and extending Claude Code with custom agents, commands, skills, and hooks. Skill-creator is adapted from claude-skills-cli.

**Commands** (5):
- `create-agent`: Create a new Claude Code agent or sub-agent using the working-with-claude-code skill
- `create-command`: Create a new Claude Code slash command using the slash-command-creator skill
- `create-hook`: Create a new Claude Code hook using the working-with-claude-code skill
- `create-skill`: Create a new Claude Code Skill using the skill-creator skill
- `validate-all-skills`: Validate all agent skills using claude-skills-cli

**Agents** (4):
- **context-manager**: Use PROACTIVELY when you need to manage context across multiple agents and long-running tasks, especially for projects exceeding 10k tokens. MUST B...
- **marketplace-dev**: Use PROACTIVELY when working with Claude Code marketplace repository. Expert in adding/modifying plugins, hooks, commands, agents, and skills. MUST...
- **mcp-expert**: Model Context Protocol (MCP) integration specialist for the cli-tool components system. Use PROACTIVELY for MCP server configurations, protocol spe...
- **meta-agent**: Generates a new, complete Claude Code sub-agent configuration file from a user's description. Use this to create new agents. Use this Proactively w...

**Skills** (6):
- **claude-skills-cli**: Create and manage Claude Agent Skills with progressive disclosure validation. Use for building and validating skill structure and activation.
- **developing-claude-code-plugins**: Use when working on Claude Code plugins. Provides streamlined workflows, patterns, and examples for the complete lifecycle.
- **plugin-creator**: Use when creating or developing Claude Code plugins. Scaffolds structure, adds components, sets up development environments, and provides guidance ...
- **skill-creator**: Use when creating or updating Claude Code skills that extend capabilities with specialized knowledge and workflows.
- **slash-commands-creator**: Create and review Claude Code slash commands. Use when creating `/...` commands, reviewing syntax, or standardizing command definitions with proper...
- **working-with-claude-code**: Use when working with Claude Code CLI or any feature. Provides comprehensive official documentation for all aspects of Claude Code.

**Install**: `claude-code-development@rigerc-claude`

### [Code Quality](./plugins/code-quality/)
Code review, refactoring, and quality analysis tools for improving code maintainability and security

**Commands** (2):
- `code-review`: Comprehensive code quality review with security, performance, and architecture analysis
- `refactor-code`: Intelligently refactor and improve code quality

**Agents** (1):
- **code-reviewer**: Expert code review specialist for quality, security, and maintainability. Use PROACTIVELY after writing or modifying code to ensure high developmen...

**Install**: `code-quality@rigerc-claude`

### [Documentation Generation](./plugins/documentation-generation/)
Comprehensive tools for generating API documentation, technical docs, and project documentation

**Commands** (1):
- `create-documentation`: Command for using the generate-documentation skill

**Agents** (3):
- **readme-writer**: Use PROACTIVELY when you need to create or improve README documentation for open source projects, libraries, or developer tools. MUST BE USED for a...
- **researcher**: Use PROACTIVELY to research documentation, APIs, frameworks, and best practices. MUST BE USED when user mentions: "documentation for", "how does X ...
- **technical-docs-writer**: Use PROACTIVELY when you need to create user-facing documentation for a product or feature, including API documentation, getting started guides, tu...

**Skills** (2):
- **api-docs-generator**: Use to generate API documentation from OpenAPI specs, docstrings, or comments. Supports multiple source formats.
- **generate-documentation**: Use to generate project documentation. Researches with context7 and saves to docs/ directory.

**Install**: `documentation-generation@rigerc-claude`

### [Flatban](./plugins/flatban/)
A Claude Code plugin that enables integration with [Flatban](https://github.com/gelform/flatban) - a filesystem-based Kanban project management system designed for AI-assisted development.

**Commands** (1):
- `flatban`: Create or update Flatban tasks with AI assistance

**Install**: `flatban@rigerc-claude`

### [Go Development](./plugins/go-development/)
Specialized tools for Go development with goroutines, channels, interfaces, and idiomatic patterns

**Agents** (1):
- **golang-pro**: Write idiomatic Go code with goroutines, channels, and interfaces. Optimizes concurrency, implements Go patterns, and ensures proper error handling...

**Skills** (10):
- **anthropic-sdk-go**: Use when integrating the official Anthropic Go SDK for Claude. Covers API clients, messages, streaming, function calling, files, and beta features ...
- **go-bubbles-skill**: Use when working with the Bubbles component library for BubbleTea applications in Go. Provides expertise in components and styling.
- **go-bubbletea-skill**: Use when building terminal UIs with the BubbleTea framework in Go. Provides expertise in Model-View-Update pattern and TUI best practices.
- **go-doc**: Use when working with Go's `go doc` command. Access package docs, explore APIs, and manage HTTP documentation servers.
- **go-env-parser**: Use when working with github.com/caarlos0/env for parsing environment variables into Go structs. Covers struct tags, custom parsers, envFile/envExp...
- **go-koanf**: Use when implementing Go configuration management with Koanf. Load from files, env vars, flags with hot-reloading and type-safe unmarshalling.
- **go-openai**: Use when working with the go-openai library for OpenAI API integration in Go. Provides expertise in chat, embeddings, and more.
- **go-openrouter**: Use when working with the OpenRouter Go client library for AI model integration. Provides expertise in chat completions, streaming, function callin...
- **go-teastraw**: Use when creating end-to-end tests for TUI applications in Go using Teastraw. Expertise in testing compiled TUI binaries, simulating user interacti...
- **go-urfave-cli-v3**: Use when building Go CLI applications with urfave/cli v3. Provides code generation, templates, migration tools, and reference documentation for com...

**Install**: `go-development@rigerc-claude`

### [Home Assistant](./plugins/home-assistant/)
Home Assistant development tools and automation skills for creating add-ons, integrations, and smart home workflows

**Skills** (1):
- **ha-addon**: Use when working on Home Assistant add-ons. Expert in Docker, YAML config, security, and HA API integration.

**Install**: `home-assistant@rigerc-claude`

### [Library Researcher](./plugins/library-researcher/)
Advanced library research skill using Context7 to analyze, compare, and document software libraries, frameworks, and development tools

**Skills** (1):
- **library-researcher**: Use for researching libraries and frameworks. Provides documentation and best practices via Context7.

**Install**: `library-researcher@rigerc-claude`

### [Marketplace Updater](./plugins/marketplace-updater/)
Automatic marketplace metadata updater that checks for updates on Claude Code startup

**Hooks** (1):
- **SessionStart_0**: Hook for SessionStart

**Install**: `marketplace-updater@rigerc-claude`

### [Music Management](./plugins/music-management/)
Comprehensive music library management system guidance using the beets music organization tool

**Skills** (1):
- **beets**: Use when working with beets music library management. Provides expertise in setup, importing, metadata, and plugin development.

**Install**: `music-management@rigerc-claude`

### [Productivity Tools](./plugins/productivity-tools/)
Productivity enhancement tools including feature brainstorming and dotfile management

**Commands** (2):
- `enhance-prompt`: Enhance prompt with full repository context and codebase analysis
- `feature-brainstorm`: Analyze the current project and suggest improvements to features or new features that are in line with the project's goals. The suggestions should ...

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
