---
name: plugin-creator
description: This skill should be used when creating, scaffolding, or developing Claude Code plugins. Use when users request to create a new plugin, add components to a plugin (skills, commands, agents, hooks, MCP servers), set up plugin development environments, or need guidance on plugin structure and best practices.
---

# Plugin Creator

## Purpose

This skill guides the creation of Claude Code plugins - modular packages that extend Claude Code with custom slash commands, specialized agents, reusable skills, event hooks, and external service integrations. Use this skill to build plugins ranging from simple utilities to complex development toolkits.

## When to Use This Skill

Apply this skill when the user wants to:
- Create a new Claude Code plugin from scratch
- Add components to an existing plugin (commands, agents, skills, hooks, MCP servers)
- Set up a plugin development environment
- Understand plugin structure and best practices
- Test or distribute a plugin

Common usage patterns:
- "Create a plugin with /deploy and /rollback commands"
- "Build a Python development toolkit plugin"
- "Add a code formatter hook to my existing plugin"
- "Create a plugin that integrates with the GitHub API"
- "Help me scaffold a new Claude Code plugin"

## How to Use This Skill

### Development Workflow

Follow the core development workflow:

1. **Understanding** - Gather 2-3 concrete examples of how the plugin will be used
2. **Planning** - Determine which components are needed (commands, agents, skills, hooks, MCP servers)
3. **Implementation** - Execute `python scripts/init_plugin.py <plugin-name>` to scaffold the structure
4. **Customization** - Customize generated components, remove unused ones, update metadata
5. **Testing** - Install via local marketplace, validate, and iterate

For detailed procedures (Phases 0-5), example scenarios, and distribution guidance, consult `references/development-workflow.md`.

**Component Types:**
- **Commands** - User-invoked operations (`/deploy`, `/test`)
- **Skills** - Reusable workflows with bundled resources
- **Agents** - Automatic delegation to specialized tasks
- **Hooks** - Automatic responses to events
- **MCP servers** - External service integration

Consult `references/component-specifications.md` for detailed component guidance.

### Iteration and Refinement

After initial implementation, improve the plugin through systematic iteration:

1. **Test activation** - Verify commands appear in `/help`, agents in `/agents`, skills activate on matching descriptions
2. **Gather feedback** - Have users test realistic scenarios and report issues
3. **Refine components** - Update component files based on testing results
4. **Validate changes** - Run `claude plugin validate` after each modification
5. **Reinstall and retest** - Use uninstall/install cycle to test changes:
   ```bash
   claude plugin uninstall <plugin-name>
   claude plugin install <plugin-name>@local-dev
   ```
6. **Monitor conflicts** - Ensure commands/skills do not conflict with other plugins
7. **Document improvements** - Track changes for version history

For detailed iteration procedures, consult `references/development-workflow.md` Phase 3.

### Using Bundled Resources

This skill provides scripts, references, and templates to streamline plugin development:

**scripts/init_plugin.py**
Execute this script directly via Bash to scaffold a new plugin. Do not load into context for typical usage.

```bash
python scripts/init_plugin.py <plugin-name> [--path <output-dir>]
```

Creates complete plugin structure with all component directories, plugin.json manifest, example files, local .dev-marketplace for testing, and README template. Requires Python 3.6+ (standard library only).

Load into context only when customization of initialization behavior is needed (e.g., modifying scaffold logic, changing default structure).

**references/component-specifications.md**
- Load for detailed specs on all component types
- Includes plugin manifest schema
- Reference when implementing commands, agents, skills, hooks, or MCP servers

**references/plugin-json-examples.md**
- Load for plugin.json structure reference (minimal, standard, advanced configurations)
- Quick lookup when scaffolding or updating manifest
- Grep patterns for targeted loading:
  - "Minimal Plugin" | "Standard Plugin" | "Advanced Plugin" - configuration examples

**references/component-examples.md**
- Load for real-world component implementations
- Shows complete working examples for commands, agents, skills, hooks, and MCP servers
- Grep patterns for targeted loading:
  - "/deploy" | "AWS Deployment" | "Testing Workflow" - specific component examples
  - "Command:" | "Agent:" | "Skill:" | "Hook:" | "MCP:" - component type sections

**references/pattern-library.md**
- Load for advanced implementation patterns and edge cases
- Covers CRUD patterns, progressive loading, hook chains, tool restrictions, custom paths
- Grep patterns for targeted loading:
  - "CRUD Plugin" | "Progressive Loading" | "Hook Chain" - implementation patterns
  - "Monorepo" | "Non-Standard" | "Component-Specific Testing" - advanced topics

**references/development-workflow.md**
- Load for testing, validation, and distribution procedures
- Follow when setting up local development or preparing to publish
- Grep patterns for targeted loading:
  - "Phase 0" | "Phase 1" | "Phase 2" | "Phase 3" | "Phase 4" | "Phase 5" - development phases
  - "Single Command Plugin" | "Multi-Component" | "Event-Driven" - example scenarios
  - "Best Practices" | "Useful Commands" - quick reference

**references/troubleshooting.md**
- Load when encountering validation errors or structural issues
- Contains common problems and actionable solutions

**references/marketplace-guide.md**
- Load only when ready to distribute the plugin
- Covers marketplace creation, git setup, and publishing

**assets/ templates**
- Copy as starting points when creating components
- `command-template.md` - Slash command structure
- `agent-template.md` - Agent structure
- `skill-template.md` - Skill structure
- `hooks-template.json` - Hook configuration
- `mcp-template.json` - MCP server definitions
- `marketplace-template.json` - Marketplace structure

Templates are minimal, copy-ready files (not loaded into context).

### Language and Style

Write all plugin content using:
- Imperative/infinitive form (verb-first instructions)
- Objective, instructional tone
- Third-person in YAML frontmatter descriptions
- Clear, actionable guidance

Avoid second-person language ("you should") - instead use "To accomplish X, do Y" format.

### Additional Resources

For canonical, up-to-date documentation, see [official Claude Code documentation](https://code.claude.com/docs/en/plugins-reference).

Throughout the development process, ask clarifying questions to understand user needs. Focus on the most important questions first to avoid overwhelming the user.
