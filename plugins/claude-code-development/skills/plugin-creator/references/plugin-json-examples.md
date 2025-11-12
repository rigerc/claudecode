# Plugin.json Examples

Quick reference for plugin manifest structure.

## Field Format Notes

Component registration fields (`commands`, `agents`, `skills`, `hooks`, `mcpServers`) accept flexible formats:

**Single string** (one component):
```json
"commands": "./commands/example.md"
```

**Array** (one or more components):
```json
"commands": ["./commands/cmd1.md", "./commands/cmd2.md"]
```

**Note:** The initialization script generates arrays for consistency, but single strings are valid for one-component registrations.

## Full Plugin.json Examples

### Minimal Plugin (Commands Only)

```json
{
  "name": "json-formatter",
  "version": "1.0.0",
  "description": "JSON formatting and validation tools",
  "author": {
    "name": "Developer Name",
    "email": "dev@example.com"
  },
  "repository": "https://github.com/username/json-formatter",
  "license": "MIT",
  "commands": [
    "./commands/format-json.md",
    "./commands/validate-json.md",
    "./commands/minify-json.md"
  ]
}
```

### Standard Plugin (Commands + Agents)

```json
{
  "name": "aws-deploy-tools",
  "version": "2.1.0",
  "description": "AWS deployment automation with specialized agents",
  "author": {
    "name": "DevOps Team"
  },
  "repository": "https://github.com/company/aws-deploy-tools",
  "license": "Apache-2.0",
  "commands": [
    "./commands/deploy.md",
    "./commands/rollback.md",
    "./commands/status.md"
  ],
  "agents": [
    "./agents/aws-specialist.md",
    "./agents/security-reviewer.md"
  ],
  "mcpServers": "./.mcp.json"
}
```

### Advanced Plugin (All Components)

```json
{
  "name": "python-dev-toolkit",
  "version": "3.0.0",
  "description": "Complete Python development environment with testing, formatting, and deployment",
  "author": {
    "name": "Python Guild",
    "url": "https://python-guild.dev"
  },
  "repository": "https://github.com/python-guild/dev-toolkit",
  "license": "MIT",
  "commands": [
    "./commands/test.md",
    "./commands/format.md",
    "./commands/lint.md",
    "./commands/deploy.md"
  ],
  "agents": [
    "./agents/testing-specialist.md",
    "./agents/code-quality-reviewer.md"
  ],
  "skills": [
    "./skills/pytest-runner/SKILL.md",
    "./skills/ci-cd-helper/SKILL.md"
  ],
  "hooks": "./hooks/hooks.json",
  "mcpServers": "./.mcp.json"
}
```
