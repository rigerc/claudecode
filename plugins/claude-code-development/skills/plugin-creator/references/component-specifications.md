# Component Specifications

Complete reference for Claude Code plugin components: plugin manifest, commands, agents, skills, hooks, and MCP servers.

## 0. Plugin Manifest (plugin.json)

### Location

```
.claude-plugin/plugin.json
```

### Required Field

```json
{
  "name": "plugin-name"
}
```

**`name`** - Plugin identifier in kebab-case (lowercase with hyphens). Example: `"deployment-tools"`

### Optional Metadata

```json
{
  "name": "my-plugin",
  "version": "1.0.0",
  "description": "Brief plugin description",
  "author": {
    "name": "Author Name",
    "email": "author@example.com"
  },
  "repository": "https://github.com/author/my-plugin",
  "license": "MIT",
  "keywords": ["tag1", "tag2"]
}
```

**Fields:**
- `version` - Semantic versioning (MAJOR.MINOR.PATCH)
- `description` - Displayed in marketplace listings
- `author` - Name, email (optional), url (optional)
- `repository` - Source code URL
- `license` - License identifier (MIT, Apache-2.0, etc.)
- `keywords` - Discovery tags for searching

### Component Paths

Specify custom locations (supplements default directories):

```json
{
  "commands": ["./custom/commands/"],
  "agents": "./custom/agents/",
  "hooks": "./config/hooks.json",
  "mcpServers": "./mcp-config.json"
}
```

**Rules:**
- Custom paths supplement defaults, don't replace them
- All paths must be relative to plugin root, starting with `./`
- Use `${CLAUDE_PLUGIN_ROOT}` in scripts for absolute plugin path

### Validation

```bash
claude plugin validate /path/to/plugin
```

## 1. Slash Commands

User-invoked operations via `/command-name`.

### Location

```
commands/          # Default
```

Custom paths in plugin.json: `"commands": ["./custom/commands/"]`

### Structure

```markdown
---
name: command-name
description: Brief description
---

# Command Name

Instructions for Claude when this command is invoked.

## Usage

- `/command-name` - Basic usage
- `/command-name arg1 arg2` - With arguments

## Implementation

Step-by-step execution instructions.
```

### Example

```markdown
---
name: deploy
description: Deploy application to production
---

# Deploy Command

1. Check current branch is main
2. Run test suite (unless --skip-tests)
3. Build production bundle
4. Deploy to server
5. Verify success
```

## 2. Agents

Specialized subagents for automatic task delegation.

### Location

```
agents/          # Default
```

Custom paths in plugin.json: `"agents": ["./custom/agents/"]`

### Structure

```markdown
---
description: Agent specialty for delegation matching
capabilities:
  - Capability 1
  - Capability 2
---

# Agent Name

Role, expertise, and use cases.

## Instructions

How this agent operates and what it accesses.
```

### Delegation Logic

Claude delegates automatically by matching task context to agent description and capabilities.

### Example

```markdown
---
description: AWS infrastructure deployment and management
capabilities:
  - Deploy CloudFormation stacks
  - Manage EC2 instances
  - Configure security groups
---

# AWS Deployment Agent

1. Verify AWS credentials before operations
2. Use CloudFormation for infrastructure changes
3. Follow AWS security best practices
4. Provide deployment status updates
```

## 3. Skills

Reusable capabilities with bundled resources using progressive loading.

### Structure

```
skills/
└── skill-name/
    ├── SKILL.md           # Required
    ├── scripts/           # Optional executables
    ├── references/        # Optional documentation
    └── assets/            # Optional templates
```

### SKILL.md Format

```markdown
---
name: skill-identifier
description: What this skill does and when to use it
allowed-tools: [Read, Write, Bash]  # Optional
---

# Skill Name

Overview and usage instructions.

## Resources

- scripts/ - Utility scripts
- references/ - Technical documentation
- assets/ - Output templates
```

**Frontmatter:**
- `name` (required) - Identifier (lowercase, numbers, hyphens; max 64 chars)
- `description` (required) - When to use (max 1024 chars)
- `allowed-tools` (optional) - Tool restrictions

### Progressive Loading

1. **Metadata** - Always loaded (name + description)
2. **SKILL.md** - Loaded when skill activates
3. **Bundled resources** - Loaded on demand as referenced

## 4. Hooks

Event handlers executing automatically on lifecycle events.

### Location

```
hooks/hooks.json     # Default
```

Custom path in plugin.json: `"hooks": "./config/hooks.json"`

### Structure

```json
{
  "hooks": {
    "EventName": [
      {
        "matcher": "ToolPattern",
        "hooks": [
          {
            "type": "command",
            "command": "shell_command"
          }
        ]
      }
    ]
  }
}
```

### Events

- **PreToolUse** - Before tool calls (can block)
- **PostToolUse** - After tool completion
- **UserPromptSubmit** - On user prompt submission
- **SessionStart** - Session start/resume
- **SessionEnd** - Session end
- **Stop** - After Claude finishes responding
- **SubagentStop** - After subagent completion
- **Notification** - On Claude Code notifications

### Matchers

- Specific tool: `"Bash"`, `"Edit"`, `"Write"`
- All tools: `"*"`

### Example

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "echo 'Command executed' >> log.txt"
          }
        ]
      }
    ]
  }
}
```

### Use Cases

- Code formatting after edits
- Command logging and audit trails
- File validation
- Custom notifications

## 5. MCP Servers

Model Context Protocol servers providing additional tools and resources.

### Location

```
.mcp.json           # Default (plugin root) - Recommended
```

Or inline in plugin.json: `"mcpServers": { ... }`

**Recommendation:** Use `.mcp.json` for cleaner separation of concerns. This keeps the plugin manifest focused on metadata and component registration while isolating MCP server configuration. Inline configuration in `plugin.json` is possible but better suited for very simple cases with a single server.

### Structure

```json
{
  "server-name": {
    "command": "${CLAUDE_PLUGIN_ROOT}/servers/executable",
    "args": ["--option", "value"],
    "env": {
      "API_KEY": "${API_KEY}",
      "CONFIG": "${CLAUDE_PLUGIN_ROOT}/config.json"
    }
  }
}
```

**Fields:**
- `command` (required) - Server executable path
- `args` (optional) - Command-line arguments
- `env` (optional) - Environment variables

**Variable Expansion:**
- `${CLAUDE_PLUGIN_ROOT}` - Plugin root directory
- `${VAR}` - Environment variable value
- `${VAR:-default}` - Default if variable unset

### Lifecycle

- Servers start when plugin enabled
- Restart Claude Code to apply changes
- Tools appear alongside built-in tools
- View with `/mcp` command

### Example

```json
{
  "database-tools": {
    "command": "${CLAUDE_PLUGIN_ROOT}/servers/db-server",
    "args": ["--config", "${CLAUDE_PLUGIN_ROOT}/config.json"],
    "env": {
      "DB_URL": "${DB_URL}",
      "LOG_LEVEL": "info"
    }
  }
}
```
