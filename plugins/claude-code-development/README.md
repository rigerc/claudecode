# Claude Code Development

Tools for developing and extending Claude Code with custom agents, commands, skills, and hooks. Skill-creator is adapted from claude-skills-cli.

## Overview

This plugin provides the following components:

## Commands (7)

### `create-agent`
Create a new Claude Code agent or sub-agent using the working-with-claude-code skill

### `create-command`
Create a new Claude Code slash command using the slash-command-creator skill

### `create-hook`
Create a new Claude Code hook using the working-with-claude-code skill

### `create-skill`
Create a new Claude Code Skill using the skill-creator skill

### `rule2hook`
You are an expert at converting natural language project rules into Claude Code hook configurations. Your task is to analyze the given rules and ge...

### `split-references`
Find SKILL.MD files with detailed-guide.md references and split long reference files into multiple focused files

### `validate-all-skills`
Validate all agent skills using claude-skills-cli

## Agents (1)

### claude-dev
Use PROACTIVELY when working with Claude Code plugins, components, skills, agents, commands, or hooks. Expert in using claude-code-development skil...

## Skills (5)

### agent-creator
Use when creating or updating Claude Code subagents. Provides expertise in agent configuration, system prompts, and workflow design.

### claude-skills-cli
Create and manage Claude Agent Skills with progressive disclosure validation. Use for building and validating skill structure and activation.

### plugin-creator
Use when creating or developing Claude Code plugins. Scaffolds structure, adds components, sets up development environments, and provides guidance ...

### skill-creator
Use when creating or updating Claude Code skills that extend capabilities with specialized knowledge and workflows.

### slash-commands-creator
Create and review Claude Code slash commands. Use when creating `/...` commands, reviewing syntax, or standardizing command definitions with proper...

## Hooks (1)

### PreToolUse_0
Hook for PreToolUse


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
