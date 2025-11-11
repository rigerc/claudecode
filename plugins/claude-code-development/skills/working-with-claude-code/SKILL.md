---
name: working-with-claude-code
description: Use when working with Claude Code CLI, plugins, hooks, MCP servers, skills, configuration, or any Claude Code feature - provides comprehensive official documentation for all aspects of Claude Code
allowed-tools:
  - Read
  - Grep
  - Bash
  - WebFetch
  - Write
---

# Working with Claude Code

## Overview

This skill provides complete, authoritative documentation for Claude Code directly from docs.claude.com. Instead of guessing about configuration paths, API structures, or feature capabilities, read the official docs stored in this skill's references directory.

## When to Use

Use this skill when:
- Creating or configuring Claude Code plugins
- Setting up MCP servers
- Working with hooks (pre-commit, session-start, etc.)
- Writing or testing skills
- Configuring Claude Code settings
- Troubleshooting Claude Code issues
- Understanding CLI commands
- Setting up integrations (VS Code, JetBrains, etc.)
- Configuring networking, security, or enterprise features

## Quick Reference

| Task | Read This File |
|------|---------------|
| Create a plugin | `plugins.md` then `plugins-reference.md` |
| Set up MCP server | `mcp.md` |
| Configure hooks | `hooks.md` then `hooks-guide.md` |
| Write a skill | `skills.md` |
| CLI commands | `cli-reference.md` |
| Troubleshoot issues | `troubleshooting.md` |
| General setup | `setup.md` or `quickstart.md` |
| Configuration options | `settings.md` |

## Documentation Organization

All documentation is stored as individual markdown files in `references/`. Use the Read tool to access specific documentation:

```
references/
├── overview.md              # Claude Code introduction
├── quickstart.md           # Getting started guide
├── setup.md                # Installation and setup
├── plugins.md              # Plugin development
├── plugins-reference.md    # Plugin API reference
├── plugin-marketplaces.md  # Plugin marketplaces
├── skills.md               # Skill creation
├── mcp.md                  # MCP server integration
├── hooks.md                # Hooks overview
├── hooks-guide.md          # Hooks implementation guide
├── slash-commands.md       # Slash command reference
├── sub-agents.md           # Subagent usage
├── settings.md             # Configuration reference
├── cli-reference.md        # CLI command reference
├── common-workflows.md     # Common usage patterns
├── interactive-mode.md     # Interactive mode guide
├── headless.md             # Headless mode guide
├── output-styles.md        # Output customization
├── statusline.md           # Status line configuration
├── memory.md               # Memory and context management
├── checkpointing.md        # Checkpointing feature
├── analytics.md            # Usage analytics
├── costs.md                # Cost tracking
├── monitoring-usage.md     # Usage monitoring
├── data-usage.md           # Data usage policies
├── security.md             # Security features
├── iam.md                  # IAM integration
├── network-config.md       # Network configuration
├── terminal-config.md      # Terminal configuration
├── model-config.md         # Model configuration
├── llm-gateway.md          # LLM gateway setup
├── amazon-bedrock.md       # AWS Bedrock integration
├── google-vertex-ai.md     # Google Vertex AI integration
├── vs-code.md              # VS Code integration
├── jetbrains.md            # JetBrains integration
├── devcontainer.md         # Dev container support
├── github-actions.md       # GitHub Actions integration
├── gitlab-ci-cd.md         # GitLab CI/CD integration
├── third-party-integrations.md  # Other integrations
├── legal-and-compliance.md # Legal information
├── troubleshooting.md      # Troubleshooting guide
└── migration-guide.md      # Migration guide
```

## Workflow

### For Specific Questions

1. Identify the relevant documentation file from the list above
2. Use Read tool to load: `./references/filename.md`
3. Find the answer in the official documentation
4. Apply the solution

**Example:**
```
User: "How do I create a Claude Code plugin?"
→ Read ./references/plugins.md
→ Follow the official plugin creation steps
```

### For Broad Topics

When exploring a topic, start with the overview document, then drill into specific files:

- **Extending Claude Code**: Start with `plugins.md`, `skills.md`, or `mcp.md`
- **Configuration**: Start with `settings.md` or `setup.md`
- **Integrations**: Check relevant integration file (vs-code.md, github-actions.md, etc.)
- **Troubleshooting**: Start with `troubleshooting.md`

### For Uncertain Topics

Use Grep tool to search across all documentation:

```bash
pattern: "search term"
path: ./references/
```

## Updating Documentation

The skill includes `scripts/update_docs.js` to fetch the latest documentation from docs.claude.com.

Run when:
- Documentation seems outdated
- New Claude Code features are released
- Official docs have been updated

```bash
node ./scripts/update_docs.js
```

The script:
1. Fetches llms.txt from docs.claude.com
2. Extracts all Claude Code documentation URLs
3. Downloads each page to `references/`
4. Reports success/failures

## Common Patterns

### Plugin Development

Read `plugins.md` for overview, then `plugins-reference.md` for API details.

### MCP Server Setup

Read `mcp.md` for configuration format and examples.

### Hook Configuration

Read `hooks.md` for overview, then `hooks-guide.md` for implementation details.

### Skill Creation

Read `skills.md` for the complete skill authoring guide.

## Troubleshooting

### Documentation Access Issues

**Problem**: Cannot find specific documentation
- **Solution**: Use Grep tool to search across all reference files
- **Command**: Search for keywords in `references/` directory
- **Alternative**: Check `troubleshooting.md` for common issues

**Problem**: Documentation seems outdated
- **Solution**: Run the update script to fetch latest docs
- **Command**: `node ./scripts/update_docs.js`
- **Verify**: Check timestamps in reference files

**Problem**: Reference files missing or corrupted
- **Solution**: Re-download documentation using the update script
- **Check**: Verify all files listed in Documentation Organization exist
- **Recovery**: Reinstall the skill if files are persistently missing

### Search and Navigation Issues

**Problem**: Search results are too broad
- **Solution**: Use more specific search terms and file filters
- **Example**: Search `"plugin.json"` instead of `"plugin"`
- **Pattern**: Use quotes for exact phrases, include file extensions

**Problem**: Cannot locate relevant section in long documents
- **Solution**: Use section-specific searches with headers
- **Pattern**: Search `"## Configuration"` for configuration sections
- **Alternative**: Scan document headers first, then search within sections

### Update Script Issues

**Problem**: Update script fails to run
- **Cause**: Node.js not installed or script permissions missing
- **Solution**: Install Node.js and ensure script is executable
- **Alternative**: Manually download documentation from docs.claude.com

**Problem**: Update reports network errors
- **Cause**: Network connectivity issues or firewall blocking
- **Solution**: Check internet connection and proxy settings
- **Alternative**: Update during different network conditions

**Problem**: Partial documentation update
- **Cause**: Some docs failed to download or parse
- **Solution**: Review update script output for failed files
- **Recovery**: Run update script again or manually fix missing files

### Integration Issues

**Problem**: Documentation references features not available in current version
- **Cause**: Documentation ahead of installed Claude Code version
- **Solution**: Check Claude Code version and update if needed
- **Reference**: Read `migration-guide.md` for version differences

**Problem**: Examples in documentation don't work
- **Cause**: Examples may need adaptation for specific environment
- **Solution**: Check configuration requirements and dependencies
- **Debug**: Use `troubleshooting.md` for example-specific issues

### Common Documentation Workflows

**Finding Configuration Options**
1. Start with `settings.md` for overview
2. Search specific option name across all files
3. Check integration-specific docs (vs-code.md, etc.)
4. Review `troubleshooting.md` for configuration issues

**Resolving Plugin Development Issues**
1. Read `plugins.md` for fundamentals
2. Check `plugins-reference.md` for API details
3. Search `troubleshooting.md` for common problems
4. Review `common-workflows.md` for patterns

**Setting Up Integrations**
1. Read specific integration file (vs-code.md, github-actions.md)
2. Check `network-config.md` for connectivity issues
3. Review `security.md` for authentication requirements
4. Consult `troubleshooting.md` for integration problems

### Performance Tips

**Large Documentation Sets**
- Use targeted searches instead of browsing entire files
- Cache frequently accessed sections locally
- Use specific file paths when known

**Efficient Search Patterns**
- Start broad, then refine with specific terms
- Use multiple search terms for complex topics
- Combine search with direct file navigation

## Examples

### Example 1: Setting Up a New Plugin

**User Request**: "How do I create a Claude Code plugin?"

**Workflow**:
1. Start with overview documentation
2. Read detailed plugin reference
3. Check common patterns and examples
4. Troubleshoot any issues

**Commands**:
```bash
# Read plugin fundamentals
Read file="./references/plugins.md"

# Get API reference details
Read file="./references/plugins-reference.md"

# Search for specific examples
Grep pattern="example" path="./references/plugins.md"
```

### Example 2: Configuring MCP Server

**User Request**: "I need to set up an MCP server for my database"

**Workflow**:
1. Read MCP integration documentation
2. Search for database-specific examples
3. Check configuration requirements
4. Review security considerations

**Commands**:
```bash
# Get MCP server setup guide
Read file="./references/mcp.md"

# Search for database examples
Grep pattern="database" path="./references/mcp.md"

# Check security requirements
Read file="./references/security.md"
```

### Example 3: Troubleshooting Hook Issues

**User Request**: "My pre-commit hook isn't working"

**Workflow**:
1. Review hooks documentation
2. Search for common hook issues
3. Check troubleshooting guide
4. Look at configuration examples

**Commands**:
```bash
# Read hooks overview
Read file="./references/hooks.md"

# Get implementation details
Read file="./references/hooks-guide.md"

# Search for hook issues
Grep pattern="pre-commit" path="./references/troubleshooting.md"
```

### Example 4: Setting Up VS Code Integration

**User Request**: "How do I integrate Claude Code with VS Code?"

**Workflow**:
1. Read VS Code integration documentation
2. Check configuration requirements
3. Review common workflows
4. Troubleshoot connection issues

**Commands**:
```bash
# Get VS Code integration guide
Read file="./references/vs-code.md"

# Check configuration requirements
Grep pattern="configuration" path="./references/vs-code.md"

# Review networking setup
Read file="./references/network-config.md"
```

### Example 5: Finding Configuration Options

**User Request**: "What settings are available for memory management?"

**Workflow**:
1. Search across all documentation for memory-related settings
2. Review configuration reference
3. Check specific memory documentation
4. Look for performance optimization tips

**Commands**:
```bash
# Search for memory configuration
Grep pattern="memory" path="./references/settings.md"

# Read memory management documentation
Read file="./references/memory.md"

# Search for performance tips
Grep pattern="performance" path="./references/"
```

### Example 6: Resolving Version Compatibility

**User Request**: "Some features aren't working after updating Claude Code"

**Workflow**:
1. Check current version documentation
2. Review migration guide
3. Search for breaking changes
4. Find alternative approaches

**Commands**:
```bash
# Check migration guide
Read file="./references/migration-guide.md"

# Search for breaking changes
Grep pattern="breaking" path="./references/migration-guide.md"

# Review troubleshooting for version issues
Grep pattern="version" path="./references/troubleshooting.md"
```

### Example 7: Advanced CLI Usage

**User Request**: "How do I use Claude Code in headless mode for automation?"

**Workflow**:
1. Read headless mode documentation
2. Check CLI reference for automation options
3. Review common automation workflows
4. Look for enterprise integration patterns

**Commands**:
```bash
# Get headless mode guide
Read file="./references/headless.md"

# Check CLI commands
Read file="./references/cli-reference.md"

# Search for automation examples
Grep pattern="automation" path="./references/"
```

## What This Skill Does NOT Do

- This skill provides **documentation access**, not procedural guidance
- For workflows on **how to build** plugins/skills, use the `extending-claude-code` skill (when available)
- This skill is a **reference library**, not a tutorial

## Red Flags

If you find yourself:
- Guessing about configuration file locations → Read `settings.md`
- Speculating about API structures → Read relevant reference doc
- Unsure about hook names → Read `hooks.md`
- Making assumptions about features → Search the docs first

**Always consult the official documentation before guessing.**
