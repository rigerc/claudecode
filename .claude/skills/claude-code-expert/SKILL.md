---
name: claude-code-expert
description: This skill provides comprehensive expertise in Claude Code - Anthropic's AI-powered terminal coding assistant. Use this skill when users need help with Claude Code installation, configuration, slash commands, permission management, hook systems, plugin development, MCP integration, or advanced workflow optimization. This skill covers all aspects from basic usage to enterprise deployment and custom automation.
---

# Claude Code Expert

## Overview

This skill transforms Claude into a Claude Code specialist capable of expert-level guidance on Anthropic's AI coding assistant. It provides comprehensive knowledge covering installation, configuration, customization, workflow optimization, and advanced integration patterns for development teams. Before proceeding to implementation, research using Context7 (`anthropics/claude-code`).

## Core Capabilities

### 1. Installation and Setup

Guide users through complete Claude Code deployment across different environments:

```bash
# Standard installation
npm install -g @anthropic-ai/claude-code

# Environment setup for different providers
export ANTHROPIC_API_KEY=sk-ant-...
export OPENAI_API_KEY=sk-...
export AWS_REGION=us-west-2
export GOOGLE_APPLICATION_CREDENTIALS=/path/to/creds.json

# Launch with specific configuration
claude --settings /path/to/settings.json
claude --model claude-sonnet-4
claude --permission-mode acceptEdits
```

**Setup validation:**
- Run `/doctor` to diagnose configuration issues
- Verify API key authentication with `/usage`
- Test permission system with safe commands
- Validate MCP server connections

### 2. Permission System Configuration

Implement granular security controls for enterprise environments:

```json
{
  "permissions": {
    "allowedTools": [
      "Read(**/*.{js,ts,jsx,tsx,json,md})",
      "Edit(**/*.{js,ts,jsx,tsx})",
      "Bash(git:*)",
      "Bash(npm:*)",
      "Bash(python:*)",
      "Bash(node:*)"
    ],
    "deniedTools": [
      "Edit(/config/secrets.json)",
      "Edit(/prod/**)",
      "Bash(rm -rf:*)",
      "Bash(sudo:*)"
    ]
  },
  "permissionMode": "ask"
}
```

**Permission patterns:**
- Use glob patterns for file access control
- Implement command whitelisting for bash operations
- Set up environment-specific permission modes
- Configure audit logging for security compliance

### 3. Custom Slash Commands

Create powerful workflow automation commands:

**Basic command structure:**
```markdown
# .claude/commands/deploy.md
---
allowed-tools: Bash(npm:*), Bash(git:*), Edit(**/package.json)
description: Build, test, and deploy application to production
---

## Deployment Workflow

1. Run test suite with `npm run test`
2. Build application with `npm run build`
3. If tests pass, deploy to production
4. Create git tag with version number
5. Update deployment status
```

**Advanced command patterns:**
- Multi-step deployment pipelines
- Automated code review workflows
- Database migration automation
- Security scanning integration

### 4. Hook System Implementation

Set up validation and automation hooks:

**Pre-execution validation:**
```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "python3 /path/to/security-validator.py"
          }
        ]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "Edit",
        "hooks": [
          {
            "type": "command",
            "command": "npm run lint && npm run type-check"
          }
        ]
      }
    ]
  }
}
```

**Hook implementations:**
- Security vulnerability scanners
- Code quality validators
- Performance impact analyzers
- Compliance checkers

### 5. MCP Server Integration

Integrate external services via Model Context Protocol:

**GitHub MCP server:**
```json
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@anthropic-ai/mcp-server-github"],
      "oauth": {
        "clientId": "your-client-id",
        "clientSecret": "your-client-secret",
        "scopes": ["repo", "issues", "pull_requests"]
      }
    },
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "/allowed/path"]
    }
  }
}
```

**MCP usage patterns:**
- Enable `@github` for repository management
- Use `@filesystem` for controlled file access
- Integrate with custom APIs via MCP servers
- Combine multiple MCP services for complex workflows

### 6. Plugin Development

Create and manage custom plugins:

**Plugin structure:**
```
my-plugin/
├── .claude-plugin/
│   └── plugin.json
├── commands/
│   ├── deploy.md
│   └── security-scan.md
├── agents/
│   └── code-reviewer.md
└── hooks/
    └── validation.json
```

**Plugin configuration:**
```json
{
  "name": "enterprise-tools",
  "version": "1.0.0",
  "description": "Enterprise development automation tools",
  "commands": ["deploy", "security-scan", "compliance-check"],
  "agents": ["code-reviewer", "security-analyst"],
  "hooks": ["pre-commit", "pre-deploy"]
}
```

### 7. Advanced Workflow Optimization

Implement sophisticated development patterns:

**Git workflow automation:**
```bash
# Intelligent commit generation
claude "Commit these changes and create a PR with proper template"

# Automated branch management
claude "Create feature branch from develop, implement user auth, and submit for review"
```

**Code review automation:**
- Automated PR creation with templates
- Intelligent commit message generation
- Code quality analysis integration
- Security vulnerability scanning

**Testing workflows:**
- Automated test suite execution
- Coverage analysis and reporting
- Performance benchmarking
- Integration test management

### 8. Enterprise Deployment

Configure Claude Code for team environments:

**Team configuration sharing:**
```json
{
  "extraKnownMarketplaces": [
    {
      "name": "company-plugins",
      "url": "https://github.com/company/claude-plugins"
    }
  ],
  "sharedSettings": {
    "permissions": "company-wide-permissions.json",
    "hooks": "company-hooks.json",
    "mcpServers": "company-mcp-servers.json"
  }
}
```

**Multi-provider setup:**
- Configure Anthropic, OpenAI, AWS Bedrock, Google Vertex
- Implement cost optimization strategies
- Set up usage monitoring and alerting
- Configure model selection policies

### 9. Troubleshooting and Debugging

Resolve common Claude Code issues:

**Diagnostic procedures:**
```bash
# System health check
claude /doctor

# Debug mode for troubleshooting
claude --debug

# Log analysis
tail -f ~/.claude/debug.log

# Permission validation
claude --validate-permissions
```

**Common issues and solutions:**
- OAuth token expiration and renewal
- Path resolution across operating systems
- Hook execution failures
- MCP server connectivity problems
- Plugin loading errors

### 10. Performance Optimization

Optimize Claude Code for efficiency:

**Context management:**
```bash
# Monitor context usage
/context

# Strategic directory inclusion
/add-dir src/core

# Memory optimization
/memory
```

**Cost optimization:**
- Model selection strategies
- Token usage monitoring
- Caching implementation
- Batch operation processing

## Usage Guidelines

**When to use this skill:**
- Setting up Claude Code for new development environments
- Configuring enterprise-grade security and permissions
- Creating custom automation workflows
- Integrating external services via MCP servers
- Developing custom plugins and slash commands
- Troubleshooting deployment and configuration issues
- Optimizing performance and cost efficiency

**Expert workflow patterns:**
1. **Assessment**: Evaluate user's current setup and requirements
2. **Configuration**: Implement appropriate security and permission controls
3. **Automation**: Create custom workflows for repetitive tasks
4. **Integration**: Connect external services and APIs
5. **Validation**: Test configuration and troubleshoot issues
6. **Optimization**: Refine for performance and cost efficiency

This skill enables comprehensive Claude Code expertise from basic setup to enterprise deployment, ensuring secure, efficient, and powerful AI-assisted development workflows.