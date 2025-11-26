# Claude Extensions Plugin Collection

A curated collection of specialized plugins for Claude Code, organized by functionality to provide focused tools for specific development tasks.

## Table of Contents

- 🚀 [Installation](#-installation)
  - [Add Marketplace](#add-marketplace)
  - [Install Individual Plugins](#install-individual-plugins)
  - [Browse Available Plugins](#browse-available-plugins)
- 🔌 [Plugin Details](#-plugin-details)
  - [Bash Scripting](#bash-scripting)
  - [Claude Code Development](#claude-code-development)
  - [Code Quality](#code-quality)
  - [Documentation Generation](#documentation-generation)
  - [Flatban](#flatban)
  - [Frontend Skills](#frontend-skills)
  - [Go Development](#go-development)
  - [Home Assistant](#home-assistant)
  - [Markdown Task Manager](#markdown-task-manager)
  - [Marketplace Updater](#marketplace-updater)
  - [Music Management](#music-management)
  - [Productivity Tools](#productivity-tools)
- 📁 [Plugin Structure](#-plugin-structure)
- 🛠️ [Development](#-development)
  - [Building](#building)
  - [Plugin Categories](#plugin-categories)
- 📄 [License](#-license)

## Collection Summary

- **12 Specialized Plugins**
- **13 Custom Commands**
- **7 Expert Agents**
- **39 Specialized Skills**
- **3 Hooks**
- **0 MCP Servers**

---

## 🚀 Installation

### Add Marketplace

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

---

## 🔌 Plugin Details

### Bash Scripting

Expert tools for Bash scripting, automation, and testing with bats-core framework

**📦 Install**: `/plugin install bash-scripting@rigerc-claude`


**Agents** (1):
- **bash-scripting-expert**: Expert Bash scripting developer specializing in best practices, code review, optimization, and modern Bash patterns. Provides professional guidance...


**Skills** (7):
- **argc-bash**: Use when creating Bash CLIs with argc framework. Provides expertise in argc comment tags, parameter types, dynamic values, nested subcommands, and ...
- **bats-tester**: Use when creating tests for bash scripts using bats-core. Provides expertise in test writing, setup, and best practices.
- **curl**: Use for expert guidance on curl HTTP requests, API testing, file transfers, shell automation, and network debugging
- **fish-plugins**: Use when creating Fish shell plugins, functions, completions, or managing Fish shell configurations
- **fish-shell**: Use when working with Fish Shell for interactive usage, scripting, configuration, automation, and intelligent completions
- **gum**: Use when working with charmbracelet/gum for creating interactive, glamorous shell scripts. Provides expertise in gum commands for input, selection,...
- **jq**: Use for JSON processing with jq command in bash scripts, data filtering, transformation, and API response parsing

---

### Claude Code Development

Tools for developing and extending Claude Code with custom agents, commands, skills, and hooks. Skill-creator is adapted from claude-skills-cli.

**📦 Install**: `/plugin install claude-code-development@rigerc-claude`


**Commands** (7):
- `create-agent`: Create a new Claude Code agent or sub-agent using the working-with-claude-code skill
- `create-command`: Create a new Claude Code slash command using the slash-command-creator skill
- `create-hook`: Create a new Claude Code hook using the working-with-claude-code skill
- `create-skill`: Create a new Claude Code Skill using the skill-creator skill
- `rule2hook`: You are an expert at converting natural language project rules into Claude Code hook configurations. Your task is to analyze the given rules and ge...
- `split-references`: Find SKILL.MD files with detailed-guide.md references and split long reference files into multiple focused files
- `validate-all-skills`: Validate all agent skills using claude-skills-cli


**Agents** (1):
- **claude-dev**: Use PROACTIVELY when working with Claude Code plugins, components, skills, agents, commands, or hooks. Expert in using claude-code-development skil...


**Skills** (5):
- **agent-creator**: Use when creating or updating Claude Code subagents. Provides expertise in agent configuration, system prompts, and workflow design.
- **claude-skills-cli**: Create and manage Claude Agent Skills with progressive disclosure validation. Use for building and validating skill structure and activation.
- **plugin-creator**: Use when creating or developing Claude Code plugins. Scaffolds structure, adds components, sets up development environments, and provides guidance ...
- **skill-creator**: Use when creating or updating Claude Code skills that extend capabilities with specialized knowledge and workflows.
- **slash-commands-creator**: Create and review Claude Code slash commands. Use when creating `/...` commands, reviewing syntax, or standardizing command definitions with proper...


**Hooks** (1):
- **PreToolUse_0**: Hook for PreToolUse

---

### Code Quality

Code review, refactoring, and quality analysis tools for improving code maintainability and security

**📦 Install**: `/plugin install code-quality@rigerc-claude`


**Commands** (2):
- `code-review`: Comprehensive code quality review with security, performance, and architecture analysis
- `refactor-code`: Intelligently refactor and improve code quality


**Agents** (1):
- **code-reviewer**: Expert code review specialist for quality, security, and maintainability. Use PROACTIVELY after writing or modifying code to ensure high developmen...

---

### Documentation Generation

Comprehensive tools for generating API documentation, technical docs, and project documentation

**📦 Install**: `/plugin install documentation-generation@rigerc-claude`


**Commands** (1):
- `create-documentation`: Command for using the generate-documentation skill


**Agents** (3):
- **readme-writer**: Use PROACTIVELY when you need to create or improve README documentation for open source projects, libraries, or developer tools. MUST BE USED for a...
- **researcher**: Use PROACTIVELY to research documentation, APIs, frameworks, and best practices. MUST BE USED when user mentions: "documentation for", "how does X ...
- **technical-docs-writer**: Use PROACTIVELY when you need to create user-facing documentation for a product or feature, including API documentation, getting started guides, tu...


**Skills** (3):
- **api-docs-generator**: Use to generate API documentation from OpenAPI specs, docstrings, or comments. Supports multiple source formats.
- **generate-documentation**: Use to generate project documentation. Researches with context7 and saves to docs/ directory.
- **library-researcher**: Use for researching libraries and frameworks. Provides documentation and best practices via Context7.

---

### Flatban

A Claude Code plugin that enables integration with [Flatban](https://github.com/gelform/flatban) - a filesystem-based Kanban project management system designed for AI-assisted development.

**📦 Install**: `/plugin install Flatban@rigerc-claude`


**Commands** (1):
- `flatban`: Create or update Flatban tasks with AI assistance

---

### Frontend Skills

Skills for frontend development

**📦 Install**: `/plugin install frontend-skills@rigerc-claude`


**Skills** (1):
- **shadcn-svelte**: Use when building Svelte/SvelteKit applications with shadcn-svelte components, need form integration, theme customization, or accessibility pattern...

---

### Go Development

Specialized tools for Go development with goroutines, channels, interfaces, and idiomatic patterns

**📦 Install**: `/plugin install go-development@rigerc-claude`


**Agents** (1):
- **golang-pro**: Write idiomatic Go code with goroutines, channels, and interfaces. Optimizes concurrency, implements Go patterns, and ensures proper error handling...


**Skills** (20):
- **anthropic-sdk-go**: Use when integrating the official Anthropic Go SDK for Claude. Covers API clients, messages, streaming, function calling, files, and beta features ...
- **charmlog**: Use for beautiful, minimal, and colorful logging in Go applications with Charmbracelet Log
- **fyne**: Use when developing cross-platform GUI applications in Go using the Fyne toolkit for desktop, mobile, and web applications.
- **go-bubbles-skill**: Use when working with the Bubbles component library for BubbleTea applications in Go. Provides expertise in components and styling.
- **go-bubbletea-skill**: Use when building terminal UIs with the BubbleTea framework in Go. Provides expertise in Model-View-Update pattern and TUI best practices.
- **go-doc**: Use when working with Go's `go doc` command. Access package docs, explore APIs, and manage HTTP documentation servers.
- **go-env-parser**: Use when working with github.com/caarlos0/env for parsing environment variables into Go structs. Covers struct tags, custom parsers, envFile/envExp...
- **go-hass-anything**: Use when developing Go applications for Home Assistant integration via MQTT using the go-hass-anything framework. Expert guidance for creating sens...
- **go-koanf**: Use when implementing Go configuration management with Koanf. Load from files, env vars, flags with hot-reloading and type-safe unmarshalling.
- **go-openai**: Use when working with the go-openai library for OpenAI API integration in Go. Provides expertise in chat, embeddings, and more.
- **go-openrouter**: Use when working with the OpenRouter Go client library for AI model integration. Provides expertise in chat completions, streaming, function callin...
- **go-pond**: Use when implementing concurrent Go applications with Pond worker pool library for high-performance task management and goroutine control
- **go-syscall**: Use when working with Go syscalls, low-level system programming, and Windows APIs using syscall and golang.org/x/sys packages
- **go-teastraw**: Use when creating end-to-end tests for TUI applications in Go using Teastraw. Expertise in testing compiled TUI binaries, simulating user interacti...
- **go-urfave-cli-v3**: Use when building Go CLI applications with urfave/cli v3. Provides code generation, templates, migration tools, and reference documentation for com...
- **go-wails3**: Use for Wails 3 desktop app development with Go backend and web frontend. Expert guidance on project setup, event system, menus, themes, and cross-...
- **gopsutil**: Use when implementing system monitoring, performance analysis, or DevOps applications requiring cross-platform system metrics in Go.
- **media-winrt-go**: Use when implementing Windows media player integration - SystemMediaTransportControls for media playback control on Windows
- **xsys-windows**: Use when working with Windows system programming, Windows APIs, and Windows-specific functionality using golang.org/x/sys/windows package
- **zerolog**: Use when implementing high-performance zero-allocation JSON logging with Zerolog in Go applications

---

### Home Assistant

Home Assistant development tools and automation skills for creating add-ons, integrations, and smart home workflows

**📦 Install**: `/plugin install home-assistant@rigerc-claude`


**Skills** (1):
- **ha-addon**: Use when working on Home Assistant add-ons. Expert in Docker, YAML config, security, and HA API integration.

---

### Markdown Task Manager

Kanban task management system using local Markdown files with comprehensive task lifecycle management

**📦 Install**: `/plugin install MarkdownTaskManager@rigerc-claude`


**Skills** (1):
- **markdown-task-manager**: Use to manage Kanban tasks using local Markdown files. Handles task creation, tracking, archival, and reporting.


**Hooks** (1):
- **SessionStart_0**: Hook for SessionStart

---

### Marketplace Updater

Automatic marketplace metadata updater that checks for updates on Claude Code startup

**📦 Install**: `/plugin install marketplace-updater@rigerc-claude`


**Hooks** (1):
- **SessionStart_0**: Hook for SessionStart

---

### Music Management

Comprehensive music library management system guidance using the beets music organization tool

**📦 Install**: `/plugin install music-management@rigerc-claude`


**Skills** (1):
- **beets**: Use when working with beets music library management. Provides expertise in setup, importing, metadata, and plugin development.

---

### Productivity Tools

Productivity enhancement tools including feature brainstorming and dotfile management

**📦 Install**: `/plugin install productivity-tools@rigerc-claude`


**Commands** (2):
- `enhance-prompt`: Enhance prompt with full repository context and codebase analysis
- `feature-brainstorm`: Analyze the current project and suggest improvements to features or new features that are in line with the project's goals. The suggestions should ...


---

## 📁 Plugin Structure

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

---

## 🛠️ Development

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

— **Development Tools** — For extending Claude Code and development workflows
— **Language Specific** — Targeted tools for specific programming languages  
— **Documentation** — Comprehensive documentation generation and writing tools
— **Quality & Review** — Code analysis, review, and improvement tools
— **Productivity** — General productivity enhancement tools
— **Specialized** — Domain-specific tools for particular use cases

---

## 📄 License

All plugins in this collection are licensed under MIT License.

---

*This README is automatically generated. Do not edit manually - run `python scripts/build-marketplace.py` to update.*
