# Claude Code Development

Tools for developing and extending Claude Code with custom agents, commands, skills, and hooks. Skill-creator is adapted from claude-skills-cli.

## Overview

This plugin provides the following components:

## Commands (5)

### `create-agent`
Create a new Claude Code agent or sub-agent using the working-with-claude-code skill

### `create-command`
Create a new Claude Code slash command using the slash-command-creator skill

### `create-hook`
Create a new Claude Code hook using the working-with-claude-code skill

### `create-skill`
Create a new Claude Code Skill using the skill-creator skill

### `validate-all-skills`
Validate all agent skills using claude-skills-cli

## Agents (1)

### marketplace-dev
Use PROACTIVELY when working with Claude Code marketplace repository. Expert in adding/modifying plugins, hooks, commands, agents, and skills. MUST...

## Skills (4)

### claude-skills-cli
Create and manage Claude Agent Skills with progressive disclosure validation. Use for building and validating skill structure and activation.

### plugin-creator
Use when creating or developing Claude Code plugins. Scaffolds structure, adds components, sets up development environments, and provides guidance ...

### skill-creator
Use when creating or updating Claude Code skills that extend capabilities with specialized knowledge and workflows.

### slash-commands-creator
Create and review Claude Code slash commands. Use when creating `/...` commands, reviewing syntax, or standardizing command definitions with proper...


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
