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

def extract_better_description(content: str, file_type: str, name: str) -> str:
    """Extract better description from markdown content"""
    lines = content.split('\n')

    # Skip YAML frontmatter if present
    start_idx = 0
    if lines and lines[0].startswith('---'):
        for i, line in enumerate(lines[1:], 1):
            if line.strip() == '---':
                start_idx = i + 1
                break

    # Skip empty lines and title lines
    description_lines = []
    for i, line in enumerate(lines[start_idx:], start_idx):
        line = line.strip()

        # Skip title lines (lines that start with #)
        if line.startswith('#'):
            continue

        # Skip empty lines
        if not line:
            continue

        # Skip lines that look like YAML or metadata
        if any(skip in line.lower() for skip in ['---', '===', 'name:', 'description:', 'tools:', 'use proactively', 'must be used', 'allowed-tools:', 'color:']):
            continue

        # Skip lines that are clearly field names
        if line.endswith(':') and len(line) < 50:
            continue

        # Skip very short lines that are likely field names
        if len(line) < 10:
            continue

        description_lines.append(line)

        # Take first meaningful line
        if len(description_lines) >= 1 and len(description_lines[0]) > 20:
            break
        elif len(description_lines) >= 2:
            break

    if description_lines:
        description = ' '.join(description_lines[:1])
        # Clean up common patterns
        description = description.replace('Use PROACTIVELY when', '').replace('Use when', '')
        description = description.replace('MUST BE USED for', '').strip()
        # Remove leading bullets/asterisks and clean up
        description = description.lstrip('*- ').strip()
        # Remove any trailing special characters
        description = description.rstrip('.:;')

        if len(description) > 10:
            return description

    # Fallback descriptions based on file type and name
    fallback_descriptions = {
        'commands': {
            'create-agent': 'Create specialized Claude agents for specific tasks',
            'create-command': 'Create custom slash commands for your workflow',
            'create-skill': 'Create new skills for Claude to use autonomously',
            'create-hook': 'Create event hooks for automation workflows',
            'code-review': 'Automated code review with confidence scoring and best practices',
            'feature-brainstorm': 'Brainstorm feature ideas and improvements for your projects',
            'refactor-code': 'Intelligent code refactoring suggestions and improvements',
            'create-documentation': 'Generate documentation from code and examples',
            'create-skill-from-documentation': 'Create skills from existing documentation'
        },
        'skills': {
            'api-docs-generator': 'Generate comprehensive API documentation from code and specs',
            'generate-documentation': 'Complete documentation creation for projects and features',
            'bats-tester': 'Bash script testing framework with BATS automation',
            'developing-claude-code-plugins': 'Tools for developing Claude Code extensions',
            'working-with-claude-code': 'Claude Code best practices and workflow guidance',
            'beets': 'Music library management, organization, and metadata automation'
        },
        'agents': {
            'bash-scripting-expert': 'Shell scripting automation, security, and best practices',
            'chezmoi': 'Dotfile management system for configuration synchronization',
            'claude-optimizer': 'Optimize Claude Code performance and settings',
            'code-reviewer': 'Comprehensive code analysis, security, and quality review',
            'context-manager': 'Conversation context and memory management for long sessions',
            'golang-pro': 'Go development expert with concurrency and best practices',
            'mcp-expert': 'MCP (Model Context Protocol) server development and integration',
            'meta-agent': 'Create new Claude Code sub-agents automatically',
            'readme-writer': 'Professional README and documentation generation',
            'researcher': 'Research and information gathering from documentation and APIs',
            'technical-docs-writer': 'Technical documentation, API docs, and user guides'
        }
    }

    return fallback_descriptions.get(file_type, {}).get(name, f"{file_type.title()} extension for {name}")

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
                description = extract_better_description(content, "commands", cmd_name)
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
                        description = extract_better_description(content, "skills", skill_dir.name)
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
                description = extract_better_description(content, "agents", agent_name)
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
                description = extract_better_description(content, "hooks", hook_name)
            extensions["hooks"].append({
                "name": hook_name,
                "description": description,
                "path": str(hook_file.relative_to(base_path))
            })

    return extensions

def categorize_extensions(extensions: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Create a single plugin that contains all extensions"""

    plugin = {
        "name": "claudecode-extensions",
        "description": "A comprehensive collection of Claude Code extensions including commands, skills, and agents for enhanced development workflow",
        "version": "1.0.0",
        "author": {
            "name": "Rigert"
        },
        "category": "Development",
        "keywords": ["extensions", "claude-code", "development", "productivity"],
        "homepage": "https://github.com/rigerc/claudecode",
        "repository": "https://github.com/rigerc/claudecode",
        "license": "MIT",
        "source": "./.claude",
        "commands": [f"./.claude/{cmd['path']}" for cmd in extensions["commands"]],
        "agents": [f"./.claude/{agent['path']}" for agent in extensions["agents"]],
        "skills": [f"./.claude/{skill['path']}" for skill in extensions["skills"]],
        "tags": ["extensions", "automation", "tools"],
        "strict": False
    }

    return [plugin]

def generate_marketplace_json(plugins: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Generate the marketplace.json configuration"""
    return {
        "name": "claudecode-marketplace",
        "owner": {
            "name": "Rigert"
        },
        "plugins": plugins
    }

def generate_readme(extensions: Dict[str, Any], plugins: List[Dict[str, Any]]) -> str:
    """Generate an automated README"""
    total_commands = len(extensions["commands"])
    total_skills = len(extensions["skills"])
    total_agents = len(extensions["agents"])
    total_hooks = len(extensions["hooks"])

    # Get development commands
    dev_commands = [cmd for cmd in extensions["commands"]
                   if any(keyword in cmd["name"].lower()
                         for keyword in ["create", "code", "refactor", "brainstorm", "documentation"])]

    # Get documentation skills
    doc_skills = [skill for skill in extensions["skills"]
                  if any(keyword in skill["name"].lower()
                        for keyword in ["api", "docs", "documentation", "readme"])]

    # Get quality/testing skills
    quality_skills = [skill for skill in extensions["skills"]
                     if skill not in doc_skills and skill["name"] not in ["beets"]]

    # Get specialized tools
    specialized_skills = [skill for skill in extensions["skills"]
                          if skill["name"] in ["beets"]]

    readme = f"""# Claude Code Extension Marketplace

> A curated collection of Claude Code extensions to enhance your development workflow

## 🚀 Quick Installation

Install this marketplace in Claude Code:

```bash
/plugin marketplace add rigerc/claudecode
```

Then install the extensions:

```bash
/plugin install claudecode-extensions
```

## 📦 Available Extensions

### 🔧 Development Tools
Commands for creating, reviewing, and managing code:

{chr(10).join(f"- **`{cmd['name']}`** - {cmd['description']}" for cmd in dev_commands)}

### 🤖 Specialist Agents
Domain-specific expert agents:

{chr(10).join(f"- **`{agent['name']}`** - {agent['description']}" for agent in extensions['agents'])}

### 📚 Documentation Tools
Generate and manage documentation:

{chr(10).join(f"- **`{skill['name']}`** - {skill['description']}" for skill in doc_skills)}

### 🛠️ Testing & Quality
Tools for testing, validation, and quality assurance:

{chr(10).join(f"- **`{skill['name']}`** - {skill['description']}" for skill in quality_skills)}

### 🎵 Specialized Tools
Domain-specific utilities:

{chr(10).join(f"- **`{skill['name']}`** - {skill['description']}" for skill in specialized_skills)}

## 📊 Statistics

- **{total_commands + total_skills + total_agents + total_hooks} Extensions**: {total_commands} commands, {total_skills} skills, {total_agents} agents
- **5 Categories**: Development, Agents, Documentation, Testing, Tools
- **Auto-updated**: Extensions are maintained and updated automatically

## 🔍 Usage Examples

After installation, extensions are immediately available:

```bash
# Create a new specialized agent
/create-agent

# Review your current code changes
/code-review

# Brainstorm new features for your project
/feature-brainstorm

# Generate comprehensive documentation
/generate-documentation api

# Refactor code for better performance
/refactor-code src/main.py
```

## ⚙️ Configuration

Most extensions work out-of-the-box. Some may need additional setup:

- **API Keys**: For external services and integrations
- **Git Access**: For repository-based operations
- **MCP Servers**: For protocol integrations
- **Development Tools**: For building and testing workflows

## 🤝 Contributing

Found an issue or have a suggestion?

- 🐛 [Report Issues](https://github.com/rigerc/claudecode/issues)
- 💡 [Request Features](https://github.com/rigerc/claudecode/discussions)
- 🔧 [Submit Pull Requests](https://github.com/rigerc/claudecode/pulls)

## 📄 License

MIT License - see [LICENSE](LICENSE) for details.

---

*Last updated: Automatically generated*
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