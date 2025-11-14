# Documentation Generation

Comprehensive tools for generating API documentation, technical docs, and project documentation

## Overview

This plugin provides the following components:

## Commands (1)

### `create-documentation`
--- description: Command for using the generate-documentation skill argument-hint: "description"

## Agents (3)

### readme-writer
--- name: readme-writer description: Use PROACTIVELY when you need to create or improve README documentation for open source projects, libraries, o...

### researcher
--- name: researcher description: Use PROACTIVELY to research documentation, APIs, frameworks, and best practices. MUST BE USED when user mentions:...

### technical-docs-writer
--- name: technical-docs-writer description: Use PROACTIVELY when you need to create user-facing documentation for a product or feature, including ...

## Skills (2)

### api-docs-generator
--- name: api-docs-generator description: Use to generate API documentation from OpenAPI specs, docstrings, or comments. Supports multiple source f...

### generate-documentation
--- name: generate-documentation description: Use to generate project documentation. Researches with context7 and saves to docs/ directory.

## Installation

Install this plugin from the rigerc-claude marketplace:

```bash
/plugin install documentation-generation@rigerc-claude
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
