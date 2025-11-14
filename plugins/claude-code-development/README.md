# Claude Code Development

Tools for developing and extending Claude Code with custom agents, commands, skills, and hooks. Skill-creator is adapted from claude-skills-cli.

## Overview

This plugin provides the following components:

## Commands (5)

### `create-agent`
--- description: Create a new Claude Code agent or sub-agent using the working-with-claude-code skill argument-hint: [agent-name] "[agent-descripti...

### `create-command`
--- description: Create a new Claude Code slash command using the slash-command-creator skill argument-hint: [command-name] "[command-description]"

### `create-hook`
--- description: Create a new Claude Code hook using the working-with-claude-code skill argument-hint: [hook-event] "[hook-purpose]"

### `create-skill`
--- description: Create a new Claude Code Skill using the skill-creator skill argument-hint: [skill-name] "[skill-description]"

### `validate-all-skills`
--- description: Validate all agent skills using claude-skills-cli allowed-tools: Bash, Read, Grep, Glob, TodoWrite

## Agents (4)

### context-manager
--- name: context-manager description: Use PROACTIVELY when you need to manage context across multiple agents and long-running tasks, especially fo...

### marketplace-dev
--- name: marketplace-dev description: Use PROACTIVELY when working with Claude Code marketplace repository. Expert in adding/modifying plugins, ho...

### mcp-expert
--- name: mcp-expert description: Model Context Protocol (MCP) integration specialist for the cli-tool components system. Use PROACTIVELY for MCP s...

### meta-agent
--- name: meta-agent description: Generates a new, complete Claude Code sub-agent configuration file from a user's description. Use this to create ...

## Skills (6)

### claude-skills-cli
--- name: claude-skills-cli description: Create and manage Claude Agent Skills with progressive disclosure validation. Use for building and validat...

### developing-claude-code-plugins
--- name: developing-claude-code-plugins description: Use when working on Claude Code plugins. Provides streamlined workflows, patterns, and exampl...

### plugin-creator
--- name: plugin-creator description: Use when creating or developing Claude Code plugins. Scaffolds structure, adds components, sets up developmen...

### skill-creator
--- name: skill-creator description: Use when creating or updating Claude Code skills that extend capabilities with specialized knowledge and workf...

### slash-commands-creator
--- name: slash-commands-creator description: Create and review Claude Code slash commands. Use when creating `/...` commands, reviewing syntax, or...

### working-with-claude-code
--- name: working-with-claude-code description: Use when working with Claude Code CLI or any feature. Provides comprehensive official documentation...

## Installation

Install this plugin from the rigerc-claude marketplace:

```bash
/plugin install claude-code-development@rigerc-claude
```

## Usage

After installation, the components provided by this plugin will be available in your Claude Code environment.

- **Commands** can be used with slash commands (e.g., `/command-name`)
- **Agents** provide specialized expertise for specific tasks
- **Skills** enhance agent capabilities for particular domains
- **Hooks** automate workflows and git operations
- **MCP Servers** provide external tool integrations

## Development

This plugin is part of the rigerc-claude marketplace collection. For development details, see the main repository.

---

*This README is automatically generated. Do not edit manually - run `python scripts/build-marketplace.py` to update.*
