# Documentation Generation

Comprehensive tools for generating API documentation, technical docs, and project documentation

## Overview

This plugin provides the following components:

## Commands (1)

### `create-documentation`
Command for using the generate-documentation skill

## Agents (3)

### readme-writer
Use PROACTIVELY when you need to create or improve README documentation for open source projects, libraries, or developer tools. MUST BE USED for a...

### researcher
Use PROACTIVELY to research documentation, APIs, frameworks, and best practices. MUST BE USED when user mentions: "documentation for", "how does X ...

### technical-docs-writer
Use PROACTIVELY when you need to create user-facing documentation for a product or feature, including API documentation, getting started guides, tu...

## Skills (3)

### api-docs-generator
Use to generate API documentation from OpenAPI specs, docstrings, or comments. Supports multiple source formats.

### generate-documentation
Use to generate project documentation. Researches with context7 and saves to docs/ directory.

### library-researcher
Use for researching libraries and frameworks. Provides documentation and best practices via Context7.


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
