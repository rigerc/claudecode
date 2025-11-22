# Catalyst Plugin

Comprehensive development toolkit for Claude Code featuring specialized agents, auto-activating skills, productivity commands, and automation hooks.

## Overview

Catalyst transforms your Claude Code experience with:

- **10 Specialized Agents** for autonomous complex tasks
- **7 Domain-Specific Skills** with auto-activation
- **3 Productivity Commands** for common workflows
- **9 Automation Hooks** for seamless integration
- **Pre-configured Settings** for optimal development

## 🚀 Quick Start

### Installation

```bash
# Install from local development
claude plugin install catalyst@local-dev

# Or install from marketplace (once published)
claude plugin install catalyst
```

### Verify Installation

```bash
# Check plugin is loaded
claude plugin list

# Test skill activation
echo "Creating a new API route" | claude
```

## 📋 Components

### Agents (10)

Autonomous specialists for complex multi-step tasks:

| Agent | Purpose | Integration |
|-------|---------|-------------|
| `code-architecture-reviewer` | Review architectural decisions | ✅ Ready to use |
| `code-refactor-master` | Plan and execute refactoring | ✅ Ready to use |
| `documentation-architect` | Create comprehensive docs | ✅ Ready to use |
| `frontend-error-fixer` | Debug frontend issues | ⚠️ May need screenshot paths |
| `plan-reviewer` | Validate development plans | ✅ Ready to use |
| `refactor-planner` | Create refactoring strategies | ✅ Ready to use |
| `web-research-specialist` | Research technical issues | ✅ Ready to use |
| `auth-route-tester` | Test authenticated endpoints | ⚠️ Requires JWT setup |
| `auth-route-debugger` | Debug authentication | ⚠️ Requires JWT setup |
| `auto-error-resolver` | Fix TypeScript errors | ⚠️ May need path updates |

**Usage:** Ask Claude to "Use the [agent-name] agent to [task]"

### Skills (7)

Auto-activating domain knowledge bases:

| Skill | Domain | Auto-Activation |
|-------|--------|-----------------|
| `skill-developer` | Creating Claude skills | Skill development keywords |
| `backend-dev-guidelines` | Node.js/Express/TypeScript | Backend file patterns |
| `frontend-dev-guidelines` | React/TypeScript/MUI v7 | Frontend file patterns |
| `route-tester` | API route testing | Auth/route keywords |
| `error-tracking` | Sentry monitoring | Error/monitoring keywords |
| `rust-developer` | Rust development patterns | Rust file patterns |
| `svelte-skill` | Svelte development | Svelte file patterns |

**Customization Required:** Update `skill-rules.json` path patterns for your project structure.

### Commands (3)

Productivity-boosting slash commands:

- `/dev-docs` - Generate development documentation
- `/dev-docs-update` - Update existing docs
- `/route-research-for-testing` - Research routes for testing

### Hooks (9)

Automation and integration hooks:

**Essential Hooks (Recommended for all users):**
- `skill-activation-prompt` - Auto-suggests relevant skills
- `post-tool-use-tracker` - Tracks file changes for context

**Optional Hooks (Require customization):**
- `cargo-check-stop` - Rust compilation checks
- `tsc-check` - TypeScript compilation checks
- `trigger-build-resolver` - Auto-launch error resolution
- Plus performance monitoring and validation hooks

## ⚙️ Configuration

### Skill Activation Setup

1. **Install Rust hooks (one-time):**
   ```bash
   cd .claude/hooks/RustHooks
   ./install.sh
   ```

2. **Update path patterns in `skill-rules.json`:**
   ```json
   {
     "skills": {
       "backend-dev-guidelines": {
         "fileTriggers": {
           "pathPatterns": ["src/api/**/*.ts"]  // Your backend paths
         }
       },
       "frontend-dev-guidelines": {
         "fileTriggers": {
           "pathPatterns": ["src/**/*.tsx"]  // Your frontend paths
         }
       }
     }
   }
   ```

### Authentication Setup (Optional)

For `auth-route-tester` and `auth-route-debugger` agents:
1. Ensure you use JWT cookie-based authentication
2. Update service URLs in agent files
3. Test with your authentication setup

## 🔧 Development

### Project Structure

```
catalyst/
├── .claude-plugin/
│   ├── plugin.json          # Plugin manifest
│   └── README.md            # This file
├── agents/                  # Specialized agents (10)
├── commands/                # Slash commands (3)
├── skills/                  # Domain skills (7)
├── hooks/                   # Automation hooks (9)
└── settings.json            # Default configuration
```

### Testing Changes

```bash
# Install local development version
claude plugin install catalyst@local-dev

# Test components
claude agent list
claude skill list
claude | grep "Available Commands"

# Validate plugin structure
claude plugin validate
```

### Component Integration

**Adding to Existing Projects:**

1. **Copy individual components:**
   ```bash
   # Copy specific agent
   cp catalyst/agents/code-refactor-master.md .claude/agents/

   # Copy skill with customization
   cp -r catalyst/skills/backend-dev-guidelines .claude/skills/
   # Update pathPatterns in skill-rules.json
   ```

2. **Install full plugin:**
   ```bash
   claude plugin install catalyst@local-dev
   ```

## 📚 Usage Examples

### Agent Usage
```bash
# Review architecture
"Use the code-architecture-reviewer agent to review the new user management system"

# Refactor code
"Use the code-refactor-master agent to refactor the authentication module"

# Debug frontend
"Use the frontend-error-fixer agent to debug this React error"
```

### Skill Activation
```bash
# Backend development - auto-activates backend-dev-guidelines
"Create a new API route for user profile management"

# Frontend development - auto-activates frontend-dev-guidelines
"Build a React component for data display with MUI v7"

# Svelte development - auto-activates svelte-skill
"Create a Svelte component with form validation"
```

### Command Usage
```bash
# Generate documentation
/dev-docs

# Update documentation
/dev-docs-update

# Research routes for testing
/route-research-for-testing user-authentication
```

## 🚦 Getting Started Workflow

1. **Install plugin:** `claude plugin install catalyst@local-dev`
2. **Configure skills:** Update `skill-rules.json` path patterns
3. **Test activation:** Edit a file and watch skills auto-activate
4. **Explore agents:** Try different agents for your tasks
5. **Customize hooks:** Add optional hooks based on your needs

## 🤝 Contributing

### Adding New Components

**New Agent:**
1. Create `.md` file in `agents/`
2. Follow existing agent structure
3. Add to README.md agents list

**New Skill:**
1. Create directory in `skills/`
2. Add `SKILL.md` and resource files
3. Update `skill-rules.json`
4. Add to README.md skills list

**New Command:**
1. Create `.md` file in `commands/`
2. Follow slash command format
3. Add to README.md commands list

**New Hook:**
1. Create script in `hooks/`
2. Update `plugin.json` hooks section
3. Add to README.md hooks list

### Validation

```bash
# Validate plugin structure
claude plugin validate

# Test all components
claude agent test
claude skill test
```

## 📄 License

MIT License - see LICENSE file for details.

## 🔗 Related Resources

- [Claude Code Documentation](https://docs.anthropic.com/claude-code)
- [Plugin Development Guide](https://docs.anthropic.com/claude-code/plugins)
- [Skill Development](https://docs.anthropic.com/claude-code/skills)

---

**Catalyst** - Supercharge your Claude Code development workflow with specialized agents, intelligent skills, and automation hooks.