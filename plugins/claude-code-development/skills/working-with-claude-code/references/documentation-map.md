# Claude Code Documentation Map

Complete reference guide to all available documentation files organized by category.

## Core Development

### Plugins
- **plugins.md**: Plugin development guide - structure, lifecycle, best practices
- **plugins-reference.md**: Complete plugin API reference
- **plugin-marketplaces.md**: Publishing and distributing plugins

### Skills
- **skills.md**: Skill authoring guide - creation, validation, best practices

### MCP Servers
- **mcp.md**: MCP server integration - configuration, setup, usage

### Hooks
- **hooks.md**: Hooks overview - available hooks, use cases
- **hooks-guide.md**: Hook implementation guide - examples, patterns

### Commands & Agents
- **slash-commands.md**: Custom slash command reference
- **sub-agents.md**: Subagent usage and patterns

## Configuration & Setup

### Getting Started
- **overview.md**: Claude Code introduction and concepts
- **quickstart.md**: Quick start guide for new users
- **setup.md**: Detailed installation and setup instructions

### Configuration
- **settings.md**: Complete configuration reference - all available settings
- **cli-reference.md**: CLI command documentation
- **terminal-config.md**: Terminal configuration options
- **model-config.md**: Model selection and configuration

### Advanced Configuration
- **network-config.md**: Network and proxy configuration
- **security.md**: Security features and best practices
- **iam.md**: IAM integration for enterprise
- **llm-gateway.md**: LLM gateway setup

## Usage Modes

### Interactive
- **interactive-mode.md**: Interactive mode guide
- **common-workflows.md**: Common usage patterns and workflows

### Automation
- **headless.md**: Headless mode for automation and CI/CD

### UI Customization
- **output-styles.md**: Output format customization
- **statusline.md**: Status line configuration

## Memory & Context

- **memory.md**: Memory and context management
- **checkpointing.md**: Session checkpointing feature

## Monitoring & Analytics

- **analytics.md**: Usage analytics
- **costs.md**: Cost tracking and management
- **monitoring-usage.md**: Usage monitoring and limits
- **data-usage.md**: Data usage policies

## Integrations

### IDEs
- **vs-code.md**: Visual Studio Code integration
- **jetbrains.md**: JetBrains IDE integration

### CI/CD
- **github-actions.md**: GitHub Actions integration
- **gitlab-ci-cd.md**: GitLab CI/CD integration

### Development Environments
- **devcontainer.md**: Dev container support

### Cloud Providers
- **amazon-bedrock.md**: AWS Bedrock integration
- **google-vertex-ai.md**: Google Vertex AI integration

### Other
- **third-party-integrations.md**: Other integration options

## Web Platform
- **claude-code-on-the-web.md**: Using Claude Code in web browsers

## Support

- **troubleshooting.md**: Common issues and solutions
- **migration-guide.md**: Migrating between versions
- **legal-and-compliance.md**: Legal and compliance information

## Usage Patterns

### Finding Information

**By Task**:
1. Check this map for relevant files
2. Read the overview file for context
3. Dive into specific reference files
4. Search across all files with Grep if needed

**By Search**:
```bash
# Search across all documentation
Grep pattern="your-search-term" path="./references/"
```

### Common Workflows

**Plugin Development**:
`plugins.md` → `plugins-reference.md` → `common-workflows.md`

**MCP Setup**:
`mcp.md` → `security.md` → `troubleshooting.md`

**Hook Configuration**:
`hooks.md` → `hooks-guide.md` → `common-workflows.md`

**Integration Setup**:
`vs-code.md` OR `github-actions.md` → `network-config.md` → `troubleshooting.md`

**Troubleshooting**:
`troubleshooting.md` → relevant feature docs → `common-workflows.md`
