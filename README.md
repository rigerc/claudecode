# Claude Code Extensions

> **⚡ Auto-generated marketplace from .claude directory**
> *Last updated: Automatically generated on change*

A curated collection of Claude Code extensions that enhance your development workflow.

## 📊 Extension Statistics

- **Commands**: 10
- **Skills**: 6
- **Agents**: 11
- **Hooks**: 0
- **Total Extensions**: 27

## 🚀 Quick Start

Extensions are automatically discovered from your `.claude` directory. To add new extensions:

1. **Add Commands**: Place `.md` files in `.claude/commands/`
2. **Add Skills**: Create directories with `SKILL.md` in `.claude/skills/`
3. **Add Agents**: Place `.md` files in `.claude/agents/`
4. **Add Hooks**: Place `.md` files in `.claude/hooks/`

## 📦 Available Extensions

### 🔧 Development Toolkit
Essential tools for creating, reviewing, and managing code.

**Commands**:
- `code-review`: ---
- `create-agent`: ---
- `create-command`: ---
- `create-documentation`: ---
- `create-hook`: ---
- `create-skill-from-documentation`: ---
- `create-skill`: ---
- `feature-brainstorm`: ---
- `refactor-code`: # Intelligently Refactor and Improve Code Quality

### 🤖 Specialist Agents
Domain-specific expert agents for specialized tasks.

**Agents**:
- `bash-scripting-expert`: ---
- `chezmoi`: ---
- `claude-optimizer`: ---
- `code-reviewer`: ---
- `context-manager`: ---
- `golang-pro`: ---
- `mcp-expert`: ---
- `meta-agent`: ---
- `readme-writer`: ---
- `researcher`: ---
- `technical-docs-writer`: ---

### 📚 Documentation Tools
Tools for generating and managing documentation.

**Skills & Commands**:
- `api-docs-generator`: ---
- `generate-documentation`: ---

### 🛠️ Quality & Testing Tools
Tools for testing, validation, and quality assurance.

**Skills**:
- `bats-tester`: ---

### 🎵 Specialized Tools
Domain-specific tools for particular workflows.

**Skills**:
- `beets`: ---
- `developing-claude-code-plugins`: ---
- `working-with-claude-code`: ---

## 🔧 Automation

This marketplace is **automatically generated** from your `.claude` directory:

```bash
# Regenerate marketplace (run after adding new extensions)
python3 scripts/generate-marketplace.py

# The script will:
# 1. ✅ Discover all extensions in .claude/
# 2. ✅ Categorize them automatically
# 3. ✅ Update marketplace.json
# 4. ✅ Update this README
```

## 📁 Directory Structure

```
.claude/
├── commands/          # Slash commands (.md files)
├── skills/            # Agent skills (directories with SKILL.md)
├── agents/            # Subagents (.md files)
├── hooks/             # Event hooks (.md files)
└── marketplace.json   # Auto-generated

scripts/
└── generate-marketplace.py  # This generator
```

## 🎯 Adding New Extensions

### Commands
Create `.claude/commands/my-command.md`:
```markdown
# My Command

Description of what this command does...

## Usage
/my-command [args]
```

### Skills
Create `.claude/skills/my-skill/SKILL.md`:
```markdown
# My Skill

Description of when and how to use this skill...
```

### Agents
Create `.claude/agents/my-agent.md`:
```markdown
# My Agent

Description of this specialized agent...
```

### Hooks
Create `.claude/hooks/my-hook.md`:
```markdown
# My Hook

Description of when this hook triggers...
```

After adding extensions, just run:
```bash
python3 scripts/generate-marketplace.py
```

And your marketplace is updated automatically! 🎉

---

**Generated with ❤️ by automation - No manual maintenance required!**
