#!/usr/bin/env python3
"""
Automated Marketplace Generator for Claude Code

This script automatically generates the marketplace configuration and documentation
from the existing .claude directory structure, eliminating manual maintenance.
"""

import os
import json
import glob
from pathlib import Path
from typing import Dict, List, Any

def discover_extensions() -> Dict[str, Any]:
    """Discover all extensions in the .claude directory"""
    base_path = Path(".claude")
    extensions = {
        "commands": [],
        "skills": [],
        "agents": [],
        "hooks": []
    }

    # Discover commands
    commands_path = base_path / "commands"
    if commands_path.exists():
        for cmd_file in commands_path.glob("*.md"):
            cmd_name = cmd_file.stem
            with open(cmd_file, 'r', encoding='utf-8') as f:
                content = f.read()
                # Extract first line as description
                description = content.split('\n')[0].strip() if content else ""
            extensions["commands"].append({
                "name": cmd_name,
                "description": description,
                "path": str(cmd_file.relative_to(base_path))
            })

    # Discover skills
    skills_path = base_path / "skills"
    if skills_path.exists():
        for skill_dir in skills_path.iterdir():
            if skill_dir.is_dir():
                skill_file = skill_dir / "SKILL.md"
                if skill_file.exists():
                    with open(skill_file, 'r', encoding='utf-8') as f:
                        content = f.read()
                        description = content.split('\n')[0].strip() if content else ""
                    extensions["skills"].append({
                        "name": skill_dir.name,
                        "description": description,
                        "path": str(skill_dir.relative_to(base_path))
                    })

    # Discover agents
    agents_path = base_path / "agents"
    if agents_path.exists():
        for agent_file in agents_path.glob("*.md"):
            agent_name = agent_file.stem
            with open(agent_file, 'r', encoding='utf-8') as f:
                content = f.read()
                description = content.split('\n')[0].strip() if content else ""
            extensions["agents"].append({
                "name": agent_name,
                "description": description,
                "path": str(agent_file.relative_to(base_path))
            })

    # Discover hooks
    hooks_path = base_path / "hooks"
    if hooks_path.exists():
        for hook_file in hooks_path.glob("*.md"):
            hook_name = hook_file.stem
            with open(hook_file, 'r', encoding='utf-8') as f:
                content = f.read()
                description = content.split('\n')[0].strip() if content else ""
            extensions["hooks"].append({
                "name": hook_name,
                "description": description,
                "path": str(hook_file.relative_to(base_path))
            })

    return extensions

def categorize_extensions(extensions: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Automatically categorize extensions into logical plugins"""
    plugins = []

    # Plugin 1: Development Toolkit (commands for creating things)
    dev_commands = [cmd for cmd in extensions["commands"]
                   if any(keyword in cmd["name"].lower()
                         for keyword in ["create", "code", "refactor", "brainstorm", "documentation"])]

    if dev_commands:
        plugins.append({
            "name": "development-toolkit",
            "description": "Essential tools for creating, reviewing, and managing code and documentation",
            "version": "1.0.0",
            "author": "Rigert",
            "category": "Development",
            "keywords": ["development", "tools", "productivity"],
            "commands": [cmd["name"] for cmd in dev_commands],
            "tags": ["development", "tools", "automation"]
        })

    # Plugin 2: Specialist Agents (all agents)
    if extensions["agents"]:
        plugins.append({
            "name": "specialist-agents",
            "description": "Collection of specialized agents for domain-specific expertise",
            "version": "1.0.0",
            "author": "Rigert",
            "category": "Agents",
            "keywords": ["agents", "expertise", "specialization"],
            "agents": [agent["name"] for agent in extensions["agents"]],
            "tags": ["agents", "expertise", "automation"]
        })

    # Plugin 3: Documentation Tools (skills and commands for docs)
    doc_skills = [skill for skill in extensions["skills"]
                  if any(keyword in skill["name"].lower()
                        for keyword in ["api", "docs", "documentation", "readme"])]
    doc_commands = [cmd for cmd in extensions["commands"]
                   if "documentation" in cmd["name"].lower()]

    if doc_skills or doc_commands:
        plugins.append({
            "name": "documentation-tools",
            "description": "Comprehensive tools for generating and managing documentation",
            "version": "1.0.0",
            "author": "Rigert",
            "category": "Documentation",
            "keywords": ["documentation", "writing", "api"],
            "skills": [skill["name"] for skill in doc_skills],
            "commands": [cmd["name"] for cmd in doc_commands],
            "tags": ["documentation", "writing", "productivity"]
        })

    # Plugin 4: Testing & Quality (remaining skills)
    quality_skills = [skill for skill in extensions["skills"]
                     if skill not in doc_skills]

    if quality_skills:
        plugins.append({
            "name": "quality-tools",
            "description": "Tools for testing, validation, and code quality assurance",
            "version": "1.0.0",
            "author": "Rigert",
            "category": "Development",
            "keywords": ["testing", "quality", "validation"],
            "skills": [skill["name"] for skill in quality_skills],
            "tags": ["testing", "quality", "development"]
        })

    # Plugin 5: Specialized Tools (unique extensions)
    special_skills = [skill for skill in extensions["skills"]
                     if any(keyword in skill["name"].lower()
                           for keyword in ["beets", "media", "claude", "working"])]

    if special_skills:
        plugins.append({
            "name": "specialized-tools",
            "description": "Specialized tools for specific domains and workflows",
            "version": "1.0.0",
            "author": "Rigert",
            "category": "Tools",
            "keywords": ["specialized", "workflow", "automation"],
            "skills": [skill["name"] for skill in special_skills],
            "tags": ["tools", "specialization", "workflow"]
        })

    return plugins

def generate_marketplace_json(plugins: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Generate the marketplace.json configuration"""
    return {
        "name": "claudecode-marketplace",
        "version": "1.0.0",
        "description": "Automatically generated marketplace for Claude Code extensions",
        "autoGenerated": True,
        "generatedAt": str(Path.cwd()),
        "owner": {
            "name": "Rigert",
            "url": "https://github.com/rigerc"
        },
        "homepage": "https://github.com/rigerc/claudecode",
        "license": "MIT",
        "plugins": plugins,
        "installation": {
            "commands": {
                "install": "/plugin install <plugin-name>",
                "list": "/plugin list",
                "update": "/plugin update"
            }
        },
        "automation": {
            "regenerateCommand": "./scripts/generate-marketplace.py",
            "sourceDirectory": ".claude",
            "autoDiscovery": True
        }
    }

def generate_readme(extensions: Dict[str, Any], plugins: List[Dict[str, Any]]) -> str:
    """Generate an automated README"""
    total_commands = len(extensions["commands"])
    total_skills = len(extensions["skills"])
    total_agents = len(extensions["agents"])
    total_hooks = len(extensions["hooks"])

    readme = f"""# Claude Code Extensions

> **⚡ Auto-generated marketplace from .claude directory**
> *Last updated: Automatically generated on change*

A curated collection of Claude Code extensions that enhance your development workflow.

## 📊 Extension Statistics

- **Commands**: {total_commands}
- **Skills**: {total_skills}
- **Agents**: {total_agents}
- **Hooks**: {total_hooks}
- **Total Extensions**: {total_commands + total_skills + total_agents + total_hooks}

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
{chr(10).join(f"- `{cmd['name']}`: {cmd['description']}" for cmd in extensions['commands'] if any(k in cmd['name'].lower() for k in ['create', 'code', 'refactor', 'brainstorm']))}

### 🤖 Specialist Agents
Domain-specific expert agents for specialized tasks.

**Agents**:
{chr(10).join(f"- `{agent['name']}`: {agent['description']}" for agent in extensions['agents'])}

### 📚 Documentation Tools
Tools for generating and managing documentation.

**Skills & Commands**:
{chr(10).join(f"- `{skill['name']}`: {skill['description']}" for skill in extensions['skills'] if any(k in skill['name'].lower() for k in ['api', 'docs', 'documentation', 'readme']))}

### 🛠️ Quality & Testing Tools
Tools for testing, validation, and quality assurance.

**Skills**:
{chr(10).join(f"- `{skill['name']}`: {skill['description']}" for skill in extensions['skills'] if not any(k in skill['name'].lower() for k in ['api', 'docs', 'documentation', 'readme', 'beets', 'claude']))}

### 🎵 Specialized Tools
Domain-specific tools for particular workflows.

**Skills**:
{chr(10).join(f"- `{skill['name']}`: {skill['description']}" for skill in extensions['skills'] if any(k in skill['name'].lower() for k in ['beets', 'claude', 'working']))}

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
"""

    return readme

def main():
    """Main generation function"""
    print("🚀 Generating automated marketplace...")

    # Ensure .claude-plugin directory exists
    Path(".claude-plugin").mkdir(exist_ok=True)

    # Discover extensions
    print("📁 Discovering extensions...")
    extensions = discover_extensions()

    print(f"   Found {len(extensions['commands'])} commands")
    print(f"   Found {len(extensions['skills'])} skills")
    print(f"   Found {len(extensions['agents'])} agents")
    print(f"   Found {len(extensions['hooks'])} hooks")

    # Categorize into plugins
    print("🏷️  Categorizing extensions...")
    plugins = categorize_extensions(extensions)
    print(f"   Created {len(plugins)} plugin categories")

    # Generate marketplace.json
    print("📦 Generating marketplace.json...")
    marketplace_config = generate_marketplace_json(plugins)

    with open(".claude-plugin/marketplace.json", 'w', encoding='utf-8') as f:
        json.dump(marketplace_config, f, indent=2)

    # Generate README
    print("📚 Generating README.md...")
    readme_content = generate_readme(extensions, plugins)

    with open("README.md", 'w', encoding='utf-8') as f:
        f.write(readme_content)

    print("✅ Marketplace generation complete!")
    print()
    print("📋 Summary:")
    for plugin in plugins:
        components = []
        if plugin.get("commands"):
            components.append(f"{len(plugin['commands'])} commands")
        if plugin.get("skills"):
            components.append(f"{len(plugin['skills'])} skills")
        if plugin.get("agents"):
            components.append(f"{len(plugin['agents'])} agents")

        print(f"   {plugin['name']}: {', '.join(components)}")

    print()
    print("💡 Tip: Add new extensions to .claude/ and run this script again!")

if __name__ == "__main__":
    main()