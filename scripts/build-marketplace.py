#!/usr/bin/env python3
"""
Dynamically builds marketplace.json and README.md based on plugins directory contents.
"""

import json
import os
import re
from pathlib import Path
from typing import Dict, List, Any
from datetime import datetime, timezone

def extract_plugin_description(plugin_dir: Path) -> str:
    """Extract description from plugin README.md - text after first heading and before second heading."""
    readme_path = plugin_dir / "README.md"

    if not readme_path.exists():
        return "Specialized tools for enhanced development workflows"

    try:
        with open(readme_path, 'r', encoding='utf-8') as f:
            readme_content = f.read()
            lines = readme_content.split('\n')

            description_lines = []
            in_description = False
            heading_count = 0

            for line in lines:
                line = line.strip()

                # Count headings to find boundaries
                if line.startswith('#'):
                    heading_count += 1
                    if heading_count == 1:
                        # Skip the first heading, start collecting after this
                        in_description = True
                        continue
                    elif heading_count == 2:
                        # Stop at second heading
                        break

                # Collect description text between first and second headings
                if in_description and line:
                    if not line.startswith('#'):
                        description_lines.append(line)
                elif in_description and not line and description_lines:
                    # Stop if we hit an empty line after collecting some content
                    continue

            if description_lines:
                description = ' '.join(description_lines)
                # Clean up and limit length
                description = re.sub(r'\s+', ' ', description).strip()
                if len(description) > 200:
                    description = description[:197] + "..."
                return description

    except (FileNotFoundError, UnicodeDecodeError) as e:
        print(f"Warning: Could not read {readme_path}: {e}")

    return "Specialized tools for enhanced development workflows"

def extract_plugin_info(plugin_dir: Path) -> Dict[str, Any]:
    """Extract plugin information from plugin directory."""
    plugin_name = plugin_dir.name
    plugin_json_path = plugin_dir / ".claude-plugin" / "plugin.json"
    readme_path = plugin_dir / "README.md"

    # Default plugin info with relative path
    plugin_info = {
        "name": plugin_name,
        "source": f"./plugins/{plugin_name}",
        "description": f"Plugin: {plugin_name.replace('-', ' ').title()}"
    }

    # Load from plugin.json if exists
    if plugin_json_path.exists():
        try:
            with open(plugin_json_path, 'r', encoding='utf-8') as f:
                plugin_data = json.load(f)
                plugin_info["description"] = plugin_data.get("description", plugin_info["description"])
        except (json.JSONDecodeError, FileNotFoundError) as e:
            print(f"Warning: Could not parse {plugin_json_path}: {e}")

    # Extract description from README.md (text after first heading and before second heading)
    plugin_info["description"] = extract_plugin_description(plugin_dir)

    # Truncate long descriptions
    if len(plugin_info["description"]) > 200:
        plugin_info["description"] = plugin_info["description"][:197] + "..."

    return plugin_info

def count_components(plugin_dir: Path) -> Dict[str, int]:
    """Count commands, agents, and skills in plugin directory."""
    counts = {"commands": 0, "agents": 0, "skills": 0}

    for component_type in counts.keys():
        component_dir = plugin_dir / component_type
        if component_dir.exists():
            if component_type == "skills":
                # Count skill directories (each contains SKILL.md)
                counts[component_type] = len([d for d in component_dir.iterdir()
                                             if d.is_dir() and (d / "SKILL.md").exists()])
            else:
                # Count markdown files
                counts[component_type] = len([f for f in component_dir.glob("*.md")])

    return counts

def get_current_version(marketplace_file: Path) -> str:
    """Get current version from existing marketplace file or return initial version."""
    if marketplace_file.exists():
        try:
            with open(marketplace_file, 'r', encoding='utf-8') as f:
                marketplace = json.load(f)
                current_version = marketplace.get("metadata", {}).get("version", "1.0.0")
                return current_version
        except (json.JSONDecodeError, FileNotFoundError):
            pass
    return "1.0.0"

def increment_version(version: str) -> str:
    """Increment patch version (x.y.z -> x.y.z+1)."""
    try:
        parts = version.split('.')
        if len(parts) == 3:
            major, minor, patch = map(int, parts)
            return f"{major}.{minor}.{patch + 1}"
    except (ValueError, IndexError):
        pass
    # Fallback to new version if parsing fails
    return "1.0.1"

def build_marketplace_json(plugins_dir: Path, marketplace_file: Path) -> Dict[str, Any]:
    """Build marketplace.json from plugins directory with version management."""
    plugins = []

    if not plugins_dir.exists():
        print(f"Warning: Plugins directory {plugins_dir} does not exist")
        return {}

    for plugin_dir in plugins_dir.iterdir():
        if plugin_dir.is_dir() and not plugin_dir.name.startswith('.'):
            # Check if it's a valid plugin (has .claude-plugin/plugin.json or README.md)
            plugin_json = plugin_dir / ".claude-plugin" / "plugin.json"
            readme = plugin_dir / "README.md"

            if plugin_json.exists() or readme.exists():
                plugin_info = extract_plugin_info(plugin_dir)
                plugins.append(plugin_info)
                print(f"Added plugin: {plugin_info['name']}")

    # Sort plugins by name
    plugins.sort(key=lambda x: x["name"])

    # Get current version and increment
    current_version = get_current_version(marketplace_file)
    new_version = increment_version(current_version)

    print(f"Version: {current_version} -> {new_version}")

    marketplace = {
        "name": "rigerc-claude",
        "owner": {
            "name": "rigerc's Claude personal marketplace"
        },
        "metadata": {
            "version": new_version,
            "description": "A curated collection of specialized plugins for Claude Code, organized by functionality to provide focused tools for specific development tasks.",
            "lastUpdated": datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')
        },
        "plugins": plugins
    }

    return marketplace

def generate_plugin_table(plugin_dirs: List[Path]) -> str:
    """Generate markdown table of plugins."""
    table_lines = [
        "| Plugin | Commands | Agents | Skills | Focus |",
        "|--------|----------|---------|---------|-------|"
    ]

    for plugin_dir in sorted(plugin_dirs, key=lambda x: x.name):
        if plugin_dir.is_dir() and not plugin_dir.name.startswith('.'):
            plugin_name = plugin_dir.name.replace('-', ' ').title()
            counts = count_components(plugin_dir)

            # Determine focus based on plugin content
            focus = "General"
            if "claude-code" in plugin_dir.name:
                focus = "Extending Claude Code"
            elif "bash" in plugin_dir.name:
                focus = "Shell automation"
            elif "documentation" in plugin_dir.name or "docs" in plugin_dir.name:
                focus = "Technical writing"
            elif "code-quality" in plugin_dir.name or "review" in plugin_dir.name:
                focus = "Code review"
            elif "go" in plugin_dir.name or "golang" in plugin_dir.name:
                focus = "Go programming"
            elif "music" in plugin_dir.name or "beets" in plugin_dir.name:
                focus = "Beets tool"
            elif "productivity" in plugin_dir.name:
                focus = "Workflow enhancement"

            table_lines.append(
                f"| **{plugin_name}** | {counts['commands']} | {counts['agents']} | "
                f"{counts['skills']} | {focus} |"
            )

    return '\n'.join(table_lines)

def generate_plugin_list(plugin_dirs: List[Path]) -> str:
    """Generate detailed plugin list with installation commands."""
    list_items = []

    for plugin_dir in sorted(plugin_dirs, key=lambda x: x.name):
        if plugin_dir.is_dir() and not plugin_dir.name.startswith('.'):
            plugin_name = plugin_dir.name.replace('-', ' ').title()
            plugin_key = plugin_dir.name

            # Extract description from README.md
            description = extract_plugin_description(plugin_dir)

            list_items.append(f"### {plugin_name}\n{description}\n")
            list_items.append(f"**Install**: `{plugin_key}@rigerc-claude`\n")

    return '\n'.join(list_items)

def build_readme(plugins_dir: Path) -> str:
    """Build README.md from plugins directory."""

    # Get plugin directories
    plugin_dirs = [d for d in plugins_dir.iterdir()
                   if d.is_dir() and not d.name.startswith('.')]

    # Count totals
    total_commands = sum(count_components(d)["commands"] for d in plugin_dirs)
    total_agents = sum(count_components(d)["agents"] for d in plugin_dirs)
    total_skills = sum(count_components(d)["skills"] for d in plugin_dirs)

    readme = f"""# Claude Extensions Plugin Collection

A curated collection of specialized plugins for Claude Code, organized by functionality to provide focused tools for specific development tasks.

## Overview

- **{len(plugin_dirs)} Specialized Plugins**
- **{total_commands} Custom Commands**
- **{total_agents} Expert Agents**
- **{total_skills} Specialized Skills**

## Available Plugins

{generate_plugin_table(plugin_dirs)}

## Plugin Details

{generate_plugin_list(plugin_dirs)}

## Installation

### Add the Marketplace

First, add this collection to your Claude Code marketplaces:

```bash
/plugin marketplace add rigerc/claudecode
```

### Install Individual Plugins

Install only the plugins you need:

```bash
# Example installations
/plugin install claude-code-development@rigerc-claude
/plugin install bash-scripting@rigerc-claude
/plugin install documentation-generation@rigerc-claude
```

### Browse Available Plugins

```bash
/plugin
# Select "Browse Plugins" from rigerc-claude marketplace
# Install desired plugins
```

## Plugin Structure

Each plugin follows the standard Claude Code plugin structure:

```
plugin-name/
├── .claude-plugin/
│   └── plugin.json          # Plugin metadata
├── commands/                 # Custom slash commands (optional)
├── agents/                   # Custom agents (optional)
├── skills/                   # Agent Skills (optional)
└── README.md                 # Plugin documentation
```

## Development

This collection is automatically generated from the `plugins/` directory. When adding or modifying plugins:

1. Create/modify plugin directories in `plugins/`
2. Run the build script: `python scripts/build-marketplace.py`
3. Commit the generated `.claude-plugin/marketplace.json` and `README.md`

### Building

```bash
# Build marketplace and README
python scripts/build-marketplace.py

# The script will:
# - Scan plugins/ directory
# - Generate .claude-plugin/marketplace.json
# - Update this README.md
```

### Plugin Categories

- **Development Tools**: For extending Claude Code and development workflows
- **Language Specific**: Targeted tools for specific programming languages
- **Documentation**: Comprehensive documentation generation and writing tools
- **Quality & Review**: Code analysis, review, and improvement tools
- **Productivity**: General productivity enhancement tools
- **Specialized**: Domain-specific tools for particular use cases

## License

All plugins in this collection are licensed under MIT License.

---

*This README is automatically generated. Do not edit manually - run `python scripts/build-marketplace.py` to update.*
"""

    return readme

def main():
    """Main build function."""
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    plugins_dir = project_root / "plugins"
    marketplace_dir = project_root / ".claude-plugin"

    # Create directories if they don't exist
    marketplace_dir.mkdir(exist_ok=True)

    print("Building marketplace configuration and README...")

    # Build marketplace.json
    marketplace_file = marketplace_dir / "marketplace.json"
    marketplace = build_marketplace_json(plugins_dir, marketplace_file)

    with open(marketplace_file, 'w', encoding='utf-8') as f:
        json.dump(marketplace, f, indent=2, ensure_ascii=False)

    print(f"✅ Generated {marketplace_file}")

    # Build README.md
    readme_content = build_readme(plugins_dir)
    readme_file = project_root / "README.md"

    with open(readme_file, 'w', encoding='utf-8') as f:
        f.write(readme_content)

    print(f"✅ Generated {readme_file}")

    # Summary
    plugin_count = len(marketplace.get("plugins", []))
    print(f"\n📦 Built marketplace with {plugin_count} plugins")

    if plugin_count == 0:
        print("⚠️  No plugins found. Check the plugins/ directory structure.")

if __name__ == "__main__":
    main()