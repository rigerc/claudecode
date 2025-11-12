# Implementation Patterns

Advanced patterns for complex plugin structures.

## Common Implementation Patterns

### Multi-Command CRUD Plugin

Plugin with create, read, update, delete operations:

**Structure:**
```
crud-plugin/
├── .claude-plugin/plugin.json
├── commands/
│   ├── create.md
│   ├── read.md
│   ├── update.md
│   └── delete.md
└── README.md
```

**Pattern:** Each command follows consistent structure:
1. Validate input parameters
2. Call shared logic (via agent or script)
3. Handle errors uniformly
4. Report results in consistent format

### Progressive Loading Skill

Skill with large reference documentation:

**Structure:**
```
api-skill/
├── SKILL.md (brief, <500 words)
├── scripts/
│   └── api_client.py
├── references/
│   ├── api-endpoints.md (5000 words)
│   ├── authentication.md (2000 words)
│   └── error-codes.md (3000 words)
└── assets/
    └── request-templates/
```

**Pattern in SKILL.md:**
```markdown
**references/api-endpoints.md**
Load for complete API endpoint documentation.
Search for "POST /users" for user creation endpoints.
Search for "GET /data" for data retrieval endpoints.

**references/authentication.md**
Load when setting up authentication or debugging auth errors.

**references/error-codes.md**
Load when debugging API errors. Search for error code number.
```

### Hook Chain Pattern

Multiple validations in sequence:

**hooks/hooks.json:**
```json
{
  "PostToolUse": {
    "Edit": [
      {
        "description": "Stage 1: Syntax validation",
        "command": "python hooks/validate_syntax.py \"${file_path}\"",
        "continueOnError": false
      },
      {
        "description": "Stage 2: Code formatting",
        "command": "black \"${file_path}\"",
        "continueOnError": true
      },
      {
        "description": "Stage 3: Security scan",
        "command": "bandit -r \"${file_path}\"",
        "continueOnError": true
      }
    ]
  }
}
```

**Pattern:**
- Critical validations: `continueOnError: false`
- Enhancement operations: `continueOnError: true`
- Execute in logical order (validate before format before scan)

### Tool Restriction Pattern

Agent with limited tool access for security:

**agents/restricted-executor.md:**
```markdown
---
name: restricted-executor
description: Executes user-provided code in restricted environment. Only has access to Read and Bash tools, cannot modify files or access sensitive commands.
---

# Restricted Executor

Agent for executing untrusted code with minimal permissions.

## Tool Access

Allowed tools:
- Read (for viewing files)
- Bash (restricted to safe commands only)

Blocked tools:
- Edit, Write (cannot modify filesystem)
- WebFetch (cannot make external requests)
- All MCP tools (no external service access)

## Use Cases

- Running user-submitted scripts for analysis
- Executing code in sandboxed environment
- Testing potentially unsafe operations
- Learning environments

## Safety Measures

1. All Bash commands are prefixed with `timeout 30s` to prevent infinite loops
2. No access to environment variables or credentials
3. Runs in isolated directory with limited permissions
4. All output is sanitized before display
```

## Custom Path Configurations

### Non-Standard Component Locations

**plugin.json with custom paths:**
```json
{
  "name": "custom-layout-plugin",
  "version": "1.0.0",
  "description": "Plugin with non-standard directory structure",
  "commands": [
    "./src/cli/commands/deploy.md",
    "./src/cli/commands/test.md"
  ],
  "agents": [
    "./src/agents/deployment-agent.md"
  ],
  "skills": [
    "./lib/skills/testing-skill/SKILL.md"
  ],
  "hooks": "./config/hooks.json",
  "mcpServers": "./config/mcp-servers.json"
}
```

### Monorepo Pattern

Multiple plugins in one repository:

**Repository structure:**
```
plugins-monorepo/
├── python-tools/
│   └── .claude-plugin/plugin.json
├── javascript-tools/
│   └── .claude-plugin/plugin.json
├── deployment-tools/
│   └── .claude-plugin/plugin.json
└── .dev-marketplace/
    └── .claude-plugin/marketplace.json
```

**Marketplace configuration:**
```json
{
  "name": "dev-tools-suite",
  "description": "Complete development toolkit collection",
  "plugins": [
    {
      "name": "python-tools",
      "version": "1.0.0",
      "description": "Python development tools",
      "path": "../python-tools"
    },
    {
      "name": "javascript-tools",
      "version": "1.0.0",
      "description": "JavaScript development tools",
      "path": "../javascript-tools"
    },
    {
      "name": "deployment-tools",
      "version": "2.0.0",
      "description": "Deployment automation tools",
      "path": "../deployment-tools"
    }
  ]
}
```

## Testing Patterns

### Component-Specific Testing

Test each component type systematically:

**Commands:**
```bash
# List all commands
/help

# Test each command with minimal args
/command-name

# Test with various arguments
/command-name arg1 arg2 --flag

# Test error cases
/command-name invalid-input
```

**Agents:**
```bash
# List agents
/agents

# Trigger via natural delegation
"Deploy to AWS using the deployment agent"

# Verify agent activates
# Check agent has correct tool access
# Confirm agent completes task
```

**Skills:**
```bash
# Trigger via usage pattern
"Use the testing skill to run pytest"

# Verify skill loads
# Check bundled resources are accessible
# Confirm workflow completes
```

**Hooks:**
```bash
# Trigger event
# Edit a file (for PostToolUse Edit hook)

# Verify hook executes
# Check output/side effects
# Confirm continueOnError behavior
```

**MCP Servers:**
```bash
# List MCP servers
/mcp

# Verify server started
# Use MCP-provided tools
# Check error handling
```
