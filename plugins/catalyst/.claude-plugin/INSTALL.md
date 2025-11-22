# Catalyst Plugin Installation Guide

## Prerequisites

- Claude Code installed and configured
- Git for version control (recommended)
- Terminal/shell access

## Installation Options

### Option 1: Full Plugin Installation (Recommended)

Install the complete Catalyst toolkit with all components:

```bash
# From local development directory
cd /path/to/claudecode
claude plugin install catalyst@local-dev

# Or from marketplace (once published)
claude plugin install catalyst
```

### Option 2: Individual Component Installation

Copy specific components to your existing project:

```bash
# Copy specific agents
cp catalyst/agents/code-refactor-master.md .claude/agents/
cp catalyst/agents/documentation-architect.md .claude/agents/

# Copy skills with customization
cp -r catalyst/skills/backend-dev-guidelines .claude/skills/
cp catalyst/skill-rules.json .claude/skills/

# Copy hooks
cp catalyst/hooks/skill-activation-prompt.sh .claude/hooks/
cp catalyst/hooks/post-tool-use-tracker.sh .claude/hooks/
chmod +x .claude/hooks/*.sh
```

## Post-Installation Setup

### 1. Configure Skills (Required for Auto-Activation)

Skills need to know your project structure to auto-activate:

```bash
# Edit skill rules
nano .claude/skills/skill-rules.json
```

**Example configuration for a typical project:**

```json
{
  "skills": {
    "backend-dev-guidelines": {
      "type": "domain",
      "enforcement": "suggest",
      "priority": "medium",
      "promptTriggers": {
        "keywords": ["backend", "api", "route", "controller", "service"]
      },
      "fileTriggers": {
        "pathPatterns": [
          "src/api/**/*.ts",
          "backend/**/*.ts",
          "services/*/src/**/*.ts"
        ],
        "contentPatterns": ["express", "prisma", "controller"]
      }
    },
    "frontend-dev-guidelines": {
      "type": "guardrail",
      "enforcement": "block",
      "priority": "high",
      "promptTriggers": {
        "keywords": ["react", "component", "frontend", "ui", "mui"]
      },
      "fileTriggers": {
        "pathPatterns": [
          "src/**/*.tsx",
          "frontend/src/**/*.tsx",
          "apps/web/**/*.tsx"
        ],
        "contentPatterns": ["React", "MUI", "useSuspenseQuery"]
      }
    }
  }
}
```

### 2. Install Rust Hooks (Recommended for Performance)

Essential hooks use Rust implementation for optimal performance:

```bash
cd .claude/hooks/
# Find RustHooks directory (should be included with plugin)
cd RustHooks/
./install.sh
# This installs binaries to ~/.claude-hooks/bin/
```

### 3. Configure Claude Code Settings

Add to your `.claude/settings.json` (plugin should do this automatically):

```json
{
  "enableAllProjectMcpServers": true,
  "enabledMcpjsonServers": [
    "mysql",
    "sequential-thinking",
    "playwright"
  ],
  "permissions": {
    "allow": [
      "Edit:*",
      "Write:*",
      "MultiEdit:*",
      "NotebookEdit:*",
      "Bash:*"
    ],
    "defaultMode": "acceptEdits"
  },
  "hooks": {
    "UserPromptSubmit": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/skill-activation-prompt.sh"
          }
        ]
      }
    ],
    "PostToolUse": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/post-tool-use-tracker.sh"
          }
        ]
      }
    ]
  }
}
```

## Verification

### 1. Check Plugin Installation

```bash
# Verify plugin is loaded
claude plugin list

# Should show:
# catalyst (local-dev) - Comprehensive development toolkit...
```

### 2. Test Skill Activation

```bash
# Create a test backend file
echo "import express from 'express';" > test-api.ts

# Start Claude and test
claude
# Type: "Create a new API route for user management"
# Should see skill suggestion for backend-dev-guidelines
```

### 3. Test Agent Usage

```bash
claude
# Type: "Use the code-refactor-master agent to refactor the authentication module"
# Should launch the refactor agent
```

### 4. Test Commands

```bash
claude
# Type: /dev-docs
# Should show available documentation commands
```

## Customization Guide

### Backend Projects

Update `skill-rules.json` with your backend paths:

```json
{
  "skills": {
    "backend-dev-guidelines": {
      "fileTriggers": {
        "pathPatterns": [
          "YOUR_BACKEND_PATH/**/*.ts"
        ]
      }
    }
  }
}
```

### Frontend Projects

Update `skill-rules.json` with your frontend paths:

```json
{
  "skills": {
    "frontend-dev-guidelines": {
      "fileTriggers": {
        "pathPatterns": [
          "YOUR_FRONTEND_PATH/**/*.tsx"
        ]
      }
    }
  }
}
```

### Authentication Setup

For `auth-route-tester` and `auth-route-debugger` agents:

1. **Check authentication method:**
   ```bash
   # Verify you use JWT cookie-based auth
   grep -r "jwt.*cookie" src/ || echo "JWT cookie auth not found"
   ```

2. **Update service URLs in agent files:**
   ```bash
   # Edit agent files to match your service URLs
   nano .claude/agents/auth-route-tester.md
   nano .claude/agents/auth-route-debugger.md
   ```

### TypeScript Projects

For `auto-error-resolver` and `tsc-check` hook:

1. **Update project paths:**
   ```bash
   # Edit tsc-check.sh to match your service structure
   nano .claude/hooks/tsc-check.sh
   ```

2. **Configure TypeScript path patterns:**
   ```json
   {
     "skills": {
       "auto-error-resolver": {
         "fileTriggers": {
           "pathPatterns": ["src/**/*.ts", "src/**/*.tsx"]
         }
       }
     }
   }
   ```

## Troubleshooting

### Plugin Not Found

```bash
# Check plugin directory exists
ls -la .claude-plugin/

# Verify plugin.json format
cat .claude-plugin/plugin.json | jq .

# Reinstall plugin
claude plugin uninstall catalyst
claude plugin install catalyst@local-dev
```

### Skills Not Activating

```bash
# Check skill-rules.json exists
ls -la .claude/skills/skill-rules.json

# Validate JSON format
cat .claude/skills/skill-rules.json | jq .

# Test hook manually
./.claude/hooks/skill-activation-prompt.sh < test-input.txt
```

### Hooks Not Working

```bash
# Check hook permissions
ls -la .claude/hooks/*.sh

# Test hook manually
echo "test" | ./.claude/hooks/skill-activation-prompt.sh

# Check Rust hooks installed
ls -la ~/.claude-hooks/bin/
```

### Agents Not Found

```bash
# Check agent files exist
ls -la .claude/agents/*.md

# Test agent availability
claude agent list
```

### Performance Issues

```bash
# Check Rust hooks are being used
ps aux | grep skill-activation

# If using shell scripts, consider Rust installation:
cd .claude/hooks/RustHooks && ./install.sh
```

## Migration from Individual Components

If you were previously using individual Catalyst components:

1. **Backup existing configuration:**
   ```bash
   cp -r .claude .claude.backup
   ```

2. **Remove old components:**
   ```bash
   rm -rf .claude/agents/*
   rm -rf .claude/skills/*
   rm -rf .claude/hooks/*
   ```

3. **Install full plugin:**
   ```bash
   claude plugin install catalyst@local-dev
   ```

4. **Restore custom configurations:**
   ```bash
   # Merge any custom skill rules
   merge-config .claude.backup/skills/skill-rules.json .claude/skills/skill-rules.json
   ```

## Next Steps

1. **Explore Components**: Try different agents and skills
2. **Customize Configuration**: Adapt paths and patterns to your project
3. **Read Documentation**: Check `.claude-plugin/README.md` for detailed usage
4. **Provide Feedback**: Report issues or suggest improvements

## Support

For installation issues:

1. Check this guide first
2. Review `.claude-plugin/README.md` for component details
3. Test with individual components if full plugin has issues
4. Check Claude Code documentation for plugin troubleshooting

---

**Happy coding with Catalyst!** 🚀