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
        with open(readme_path, "r", encoding="utf-8") as f:
            readme_content = f.read()
            lines = readme_content.split("\n")

            description_lines = []
            in_description = False
            heading_count = 0

            for line in lines:
                line = line.strip()

                # Count headings to find boundaries
                if line.startswith("#"):
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
                    if not line.startswith("#"):
                        description_lines.append(line)
                elif in_description and not line and description_lines:
                    # Stop if we hit an empty line after collecting some content
                    continue

            if description_lines:
                description = " ".join(description_lines)
                # Clean up and limit length
                description = re.sub(r"\s+", " ", description).strip()
                if len(description) > 200:
                    description = description[:197] + "..."
                return description

    except (FileNotFoundError, UnicodeDecodeError) as e:
        print(f"Warning: Could not read {readme_path}: {e}")

    return "Specialized tools for enhanced development workflows"


def extract_component_description(file_path: Path) -> str:
    """Extract description from component file (from YAML frontmatter or first paragraph)."""
    if not file_path.exists():
        return "No description available"

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
            lines = content.split("\n")

            # First try to extract description from YAML frontmatter
            if lines and len(lines) > 0 and lines[0].strip() == "---":
                in_yaml = True
                yaml_lines = []

                for line in lines[1:]:  # Skip the first ---
                    line_stripped = line.strip()
                    if line_stripped == "---":
                        break  # End of YAML frontmatter
                    yaml_lines.append(line)

                # Parse YAML lines to find description
                for yaml_line in yaml_lines:
                    if yaml_line.strip().startswith("description:"):
                        # Extract description after "description:"
                        desc_match = re.match(r"description:\s*(.+)", yaml_line.strip())
                        if desc_match:
                            description = desc_match.group(1).strip()
                            # Remove quotes if present
                            if description.startswith('"') and description.endswith(
                                '"'
                            ):
                                description = description[1:-1]
                            elif description.startswith("'") and description.endswith(
                                "'"
                            ):
                                description = description[1:-1]

                            # Clean up and limit length
                            description = re.sub(r"\s+", " ", description).strip()
                            if len(description) > 150:
                                description = description[:147] + "..."
                            return description

            # Fallback: extract first paragraph after heading
            description_lines = []
            in_description = False

            for line in lines:
                line = line.strip()

                # Skip empty lines and headings
                if not line or line.startswith("#"):
                    if line.startswith("#") and in_description:
                        break  # Stop at next heading
                    continue

                # Start collecting description after first heading/empty line
                if not in_description:
                    in_description = True

                if in_description:
                    description_lines.append(line)
                    if len(description_lines) >= 3:  # Limit to first few lines
                        break

            if description_lines:
                description = " ".join(description_lines)
                description = re.sub(r"\s+", " ", description).strip()
                if len(description) > 150:
                    description = description[:147] + "..."
                return description

    except (FileNotFoundError, UnicodeDecodeError) as e:
        print(f"Warning: Could not read {file_path}: {e}")

    return "No description available"


def list_plugin_components(plugin_dir: Path) -> Dict[str, List[Dict[str, str]]]:
    """List all components with their descriptions for a plugin."""
    components = {
        "commands": [],
        "agents": [],
        "skills": [],
        "hooks": [],
        "mcp_servers": [],
    }

    # List commands
    commands_dir = plugin_dir / "commands"
    if commands_dir.exists():
        for cmd_file in sorted(commands_dir.glob("*.md")):
            name = cmd_file.stem
            description = extract_component_description(cmd_file)
            components["commands"].append({"name": name, "description": description})

    # List agents
    agents_dir = plugin_dir / "agents"
    if agents_dir.exists():
        for agent_file in sorted(agents_dir.glob("*.md")):
            name = agent_file.stem
            description = extract_component_description(agent_file)
            components["agents"].append({"name": name, "description": description})

    # List skills
    skills_dir = plugin_dir / "skills"
    if skills_dir.exists():
        for skill_dir in sorted(skills_dir.iterdir()):
            if skill_dir.is_dir() and (skill_dir / "SKILL.md").exists():
                name = skill_dir.name
                description = extract_component_description(skill_dir / "SKILL.md")
                components["skills"].append({"name": name, "description": description})

    # List hooks
    hooks_dir = plugin_dir / "hooks"
    if hooks_dir.exists():
        hooks_json = hooks_dir / "hooks.json"
        if hooks_json.exists():
            try:
                with open(hooks_json, "r", encoding="utf-8") as f:
                    hooks_data = json.load(f)
                    if isinstance(hooks_data, dict) and "hooks" in hooks_data:
                        hooks_section = hooks_data["hooks"]
                        if isinstance(hooks_section, dict):
                            for hook_event, hook_configs in hooks_section.items():
                                if isinstance(hook_configs, list):
                                    for i, hook_config in enumerate(hook_configs):
                                        if isinstance(hook_config, dict):
                                            name = f"{hook_event}_{i}"
                                            description = hook_config.get(
                                                "description", f"Hook for {hook_event}"
                                            )
                                            components["hooks"].append(
                                                {
                                                    "name": name,
                                                    "description": description,
                                                }
                                            )
                        elif isinstance(hooks_section, list):
                            for hook in hooks_section:
                                if isinstance(hook, dict):
                                    name = hook.get("name", "Unknown")
                                    description = hook.get(
                                        "description", "No description"
                                    )
                                    components["hooks"].append(
                                        {"name": name, "description": description}
                                    )
                    elif isinstance(hooks_data, list):
                        for hook in hooks_data:
                            name = hook.get("name", "Unknown")
                            description = hook.get("description", "No description")
                            components["hooks"].append(
                                {"name": name, "description": description}
                            )
            except (json.JSONDecodeError, FileNotFoundError):
                # Fallback to markdown files
                for hook_file in sorted(hooks_dir.glob("*.md")):
                    name = hook_file.stem
                    description = extract_component_description(hook_file)
                    components["hooks"].append(
                        {"name": name, "description": description}
                    )
        else:
            # Fallback to markdown files
            for hook_file in sorted(hooks_dir.glob("*.md")):
                name = hook_file.stem
                description = extract_component_description(hook_file)
                components["hooks"].append({"name": name, "description": description})

    # List MCP servers
    mcp_dir = plugin_dir / "mcp_servers"
    if mcp_dir.exists():
        for mcp_file in sorted(mcp_dir.glob("*.json")):
            name = mcp_file.stem
            try:
                with open(mcp_file, "r", encoding="utf-8") as f:
                    mcp_data = json.load(f)
                    description = mcp_data.get(
                        "description", "No description available"
                    )
                    components["mcp_servers"].append(
                        {"name": name, "description": description}
                    )
            except (json.JSONDecodeError, FileNotFoundError):
                components["mcp_servers"].append(
                    {"name": name, "description": "Configuration file"}
                )

    return components


def generate_plugin_readme(plugin_dir: Path) -> str:
    """Generate README.md for a specific plugin."""
    plugin_name = plugin_dir.name.replace("-", " ").title()
    plugin_key = plugin_dir.name

    # Extract description from plugin.json first, then fallback to README extraction
    plugin_json_path = plugin_dir / ".claude-plugin" / "plugin.json"
    description = ""

    if plugin_json_path.exists():
        try:
            with open(plugin_json_path, "r", encoding="utf-8") as f:
                plugin_data = json.load(f)
                description = plugin_data.get("description", "")
        except (json.JSONDecodeError, FileNotFoundError):
            pass

    # Fallback to extracting from README if no description in plugin.json
    if not description:
        description = extract_plugin_description(plugin_dir)

    # Get component counts and details
    counts = count_components(plugin_dir)
    components = list_plugin_components(plugin_dir)

    readme = f"""# {plugin_name}

{description}

## Overview

This plugin provides the following components:

"""

    # Add component sections
    if components["commands"]:
        readme += f"## Commands ({len(components['commands'])})\n\n"
        for cmd in components["commands"]:
            readme += f"### `{cmd['name']}`\n{cmd['description']}\n\n"

    if components["agents"]:
        readme += f"## Agents ({len(components['agents'])})\n\n"
        for agent in components["agents"]:
            readme += f"### {agent['name']}\n{agent['description']}\n\n"

    if components["skills"]:
        readme += f"## Skills ({len(components['skills'])})\n\n"
        for skill in components["skills"]:
            readme += f"### {skill['name']}\n{skill['description']}\n\n"

    if components["hooks"]:
        readme += f"## Hooks ({len(components['hooks'])})\n\n"
        for hook in components["hooks"]:
            readme += f"### {hook['name']}\n{hook['description']}\n\n"

    if components["mcp_servers"]:
        readme += f"## MCP Servers ({len(components['mcp_servers'])})\n\n"
        for mcp in components["mcp_servers"]:
            readme += f"### {mcp['name']}\n{mcp['description']}\n\n"

    readme += f"""## Installation

Install this plugin from the rigerc-claude marketplace:

```bash
/plugin install {plugin_key}@rigerc-claude
```

## Usage

After installation, the components provided by this plugin will be available in your Claude Code environment.

- **Commands** can be used with slash commands (e.g., `/command-name`)
- **Agents** provide specialized expertise for specific tasks
- **Skills** enhance agent capabilities for particular domains
- **Hooks** automate workflows and git operations
- **MCP Servers** provide external tool integrations

## Development

This plugin is part of the rigerc-claude marketplace collection. For development details, see the main repository.

---

*This README is automatically generated. Do not edit manually - run `python scripts/build-marketplace.py` to update.*
"""

    return readme


def build_plugin_readmes(plugins_dir: Path) -> None:
    """Generate README.md for each plugin."""
    if not plugins_dir.exists():
        print(f"Warning: Plugins directory {plugins_dir} does not exist")
        return

    for plugin_dir in plugins_dir.iterdir():
        if plugin_dir.is_dir() and not plugin_dir.name.startswith("."):
            # Check if it's a valid plugin
            plugin_json = plugin_dir / ".claude-plugin" / "plugin.json"
            readme = plugin_dir / "README.md"

            if plugin_json.exists() or readme.exists():
                plugin_readme = generate_plugin_readme(plugin_dir)
                readme_path = plugin_dir / "README.md"

                with open(readme_path, "w", encoding="utf-8") as f:
                    f.write(plugin_readme)

                print(f"✅ Generated {readme_path}")


def extract_plugin_info(plugin_dir: Path) -> Dict[str, Any]:
    """Extract plugin information from plugin directory."""
    plugin_name = plugin_dir.name
    plugin_json_path = plugin_dir / ".claude-plugin" / "plugin.json"
    readme_path = plugin_dir / "README.md"

    # Default plugin info with relative path
    plugin_info = {
        "name": plugin_name,
        "source": f"./plugins/{plugin_name}",
        "description": f"Plugin: {plugin_name.replace('-', ' ').title()}",
    }

    # Load from plugin.json if exists
    if plugin_json_path.exists():
        try:
            with open(plugin_json_path, "r", encoding="utf-8") as f:
                plugin_data = json.load(f)
                plugin_info["description"] = plugin_data.get(
                    "description", plugin_info["description"]
                )
        except (json.JSONDecodeError, FileNotFoundError) as e:
            print(f"Warning: Could not parse {plugin_json_path}: {e}")

    # Extract description from README.md (text after first heading and before second heading)
    plugin_info["description"] = extract_plugin_description(plugin_dir)

    # Truncate long descriptions
    if len(plugin_info["description"]) > 200:
        plugin_info["description"] = plugin_info["description"][:197] + "..."

    return plugin_info


def count_components(plugin_dir: Path) -> Dict[str, int]:
    """Count commands, agents, skills, hooks, and MCP servers in plugin directory."""
    counts = {"commands": 0, "agents": 0, "skills": 0, "hooks": 0, "mcp_servers": 0}

    for component_type in counts.keys():
        component_dir = plugin_dir / component_type
        if component_dir.exists():
            if component_type == "skills":
                # Count skill directories (each contains SKILL.md)
                counts[component_type] = len(
                    [
                        d
                        for d in component_dir.iterdir()
                        if d.is_dir() and (d / "SKILL.md").exists()
                    ]
                )
            elif component_type == "hooks":
                # Count hooks.json files or markdown files in hooks directory
                hooks_json = component_dir / "hooks.json"
                if hooks_json.exists():
                    try:
                        with open(hooks_json, "r", encoding="utf-8") as f:
                            hooks_data = json.load(f)
                            # Count hooks in the JSON structure
                            if isinstance(hooks_data, dict):
                                counts[component_type] = len(
                                    hooks_data.get("hooks", [])
                                )
                            elif isinstance(hooks_data, list):
                                counts[component_type] = len(hooks_data)
                    except (json.JSONDecodeError, FileNotFoundError):
                        counts[component_type] = len(
                            [f for f in component_dir.glob("*.md")]
                        )
                else:
                    counts[component_type] = len(
                        [f for f in component_dir.glob("*.md")]
                    )
            elif component_type == "mcp_servers":
                # Count MCP server configurations
                counts[component_type] = len([f for f in component_dir.glob("*.json")])
            else:
                # Count markdown files for commands and agents
                counts[component_type] = len([f for f in component_dir.glob("*.md")])

    return counts


def get_current_version(marketplace_file: Path) -> str:
    """Get current version from existing marketplace file or return initial version."""
    if marketplace_file.exists():
        try:
            with open(marketplace_file, "r", encoding="utf-8") as f:
                marketplace = json.load(f)
                current_version = marketplace.get("metadata", {}).get(
                    "version", "1.0.0"
                )
                return current_version
        except (json.JSONDecodeError, FileNotFoundError):
            pass
    return "1.0.0"


def increment_version(version: str) -> str:
    """Increment patch version (x.y.z -> x.y.z+1)."""
    try:
        parts = version.split(".")
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
        if plugin_dir.is_dir() and not plugin_dir.name.startswith("."):
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
        "owner": {"name": "rigerc's Claude personal marketplace"},
        "metadata": {
            "version": new_version,
            "description": "A curated collection of specialized plugins for Claude Code, organized by functionality to provide focused tools for specific development tasks.",
            "lastUpdated": datetime.now(timezone.utc)
            .isoformat()
            .replace("+00:00", "Z"),
        },
        "plugins": plugins,
    }

    return marketplace


def generate_plugin_list(plugin_dirs: List[Path]) -> str:
    """Generate detailed plugin list with installation commands."""
    list_items = []
    plugin_count = 0

    for plugin_dir in sorted(plugin_dirs, key=lambda x: x.name):
        if plugin_dir.is_dir() and not plugin_dir.name.startswith("."):
            plugin_count += 1
            plugin_name = plugin_dir.name.replace("-", " ").title()
            plugin_key = plugin_dir.name
            counts = count_components(plugin_dir)
            components = list_plugin_components(plugin_dir)

            # Extract description from README.md
            description = extract_plugin_description(plugin_dir)

            # Add horizontal rule between plugins (but not before first one)
            if plugin_count > 1:
                list_items.append("---\n")

            # Create anchor-friendly name (lowercase, replace spaces with hyphens)
            anchor = plugin_name.lower().replace(" ", "-")
            list_items.append(f"### {plugin_name} {{#{anchor}}}\n")
            list_items.append(f"{description}\n")

            # Add install command immediately after description
            list_items.append(f"**📦 Install**: `/plugin install {plugin_key}@rigerc-claude`\n")

            # Add detailed component information with better spacing
            if components["commands"]:
                list_items.append(f"\n**Commands** ({len(components['commands'])}):")
                for cmd in components["commands"]:
                    list_items.append(f"- `{cmd['name']}`: {cmd['description']}")
                list_items.append("")

            if components["agents"]:
                list_items.append(f"\n**Agents** ({len(components['agents'])}):")
                for agent in components["agents"]:
                    list_items.append(f"- **{agent['name']}**: {agent['description']}")
                list_items.append("")

            if components["skills"]:
                list_items.append(f"\n**Skills** ({len(components['skills'])}):")
                for skill in components["skills"]:
                    list_items.append(f"- **{skill['name']}**: {skill['description']}")
                list_items.append("")

            if components["hooks"]:
                list_items.append(f"\n**Hooks** ({len(components['hooks'])}):")
                for hook in components["hooks"]:
                    list_items.append(f"- **{hook['name']}**: {hook['description']}")
                list_items.append("")

            if components["mcp_servers"]:
                list_items.append(
                    f"\n**MCP Servers** ({len(components['mcp_servers'])}):"
                )
                for mcp in components["mcp_servers"]:
                    list_items.append(f"- **{mcp['name']}**: {mcp['description']}")
                list_items.append("")

    return "\n".join(list_items)


def build_readme(plugins_dir: Path) -> str:
    """Build README.md from plugins directory."""

    # Get plugin directories
    plugin_dirs = [
        d for d in plugins_dir.iterdir() if d.is_dir() and not d.name.startswith(".")
    ]

    # Generate TOC plugin links
    toc_plugin_links = []
    for plugin_dir in sorted(plugin_dirs, key=lambda x: x.name):
        if plugin_dir.is_dir() and not plugin_dir.name.startswith("."):
            plugin_name = plugin_dir.name.replace("-", " ").title()
            plugin_key = plugin_dir.name
            # Create anchor-friendly name (lowercase, replace spaces with hyphens)
            anchor = plugin_name.lower().replace(" ", "-")
            toc_plugin_links.append(f"  - [{plugin_name}](#{anchor})")

    # Count totals
    total_commands = sum(count_components(d)["commands"] for d in plugin_dirs)
    total_agents = sum(count_components(d)["agents"] for d in plugin_dirs)
    total_skills = sum(count_components(d)["skills"] for d in plugin_dirs)
    total_hooks = sum(count_components(d)["hooks"] for d in plugin_dirs)
    total_mcp_servers = sum(count_components(d)["mcp_servers"] for d in plugin_dirs)

    readme = f"""# Claude Extensions Plugin Collection

A curated collection of specialized plugins for Claude Code, organized by functionality to provide focused tools for specific development tasks.

## Table of Contents

- [🚀 Installation](#-installation)
  - [Add Marketplace](#add-marketplace)
  - [Install Individual Plugins](#install-individual-plugins)
  - [Browse Available Plugins](#browse-available-plugins)
- [🔌 Plugin Details](#-plugin-details)
{chr(10).join(toc_plugin_links)}
- [📁 Plugin Structure](#-plugin-structure)
- [🛠️ Development](#️-development)
  - [Building](#building)
  - [Plugin Categories](#plugin-categories)
- [📄 License](#-license)

## Collection Summary

- **{len(plugin_dirs)} Specialized Plugins**
- **{total_commands} Custom Commands**
- **{total_agents} Expert Agents**
- **{total_skills} Specialized Skills**
- **{total_hooks} Hooks**
- **{total_mcp_servers} MCP Servers**

---

## 🚀 Installation

### Add Marketplace

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

---

## 🔌 Plugin Details

{generate_plugin_list(plugin_dirs)}

---

## 📁 Plugin Structure

Each plugin follows the standard Claude Code plugin structure:

```
plugin-name/
├── .claude-plugin/
│   └── plugin.json          # Plugin metadata
├── commands/                 # Custom slash commands (optional)
├── agents/                   # Custom agents (optional)
├── skills/                   # Agent Skills (optional)
├── hooks/                    # Git hooks (optional)
├── mcp_servers/              # MCP server configurations (optional)
└── README.md                 # Plugin documentation
```

---

## 🛠️ Development

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
# - Generate individual plugin READMEs
```

### Plugin Categories

— **Development Tools** — For extending Claude Code and development workflows
— **Language Specific** — Targeted tools for specific programming languages  
— **Documentation** — Comprehensive documentation generation and writing tools
— **Quality & Review** — Code analysis, review, and improvement tools
— **Productivity** — General productivity enhancement tools
— **Specialized** — Domain-specific tools for particular use cases

---

## 📄 License

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

    with open(marketplace_file, "w", encoding="utf-8") as f:
        json.dump(marketplace, f, indent=2, ensure_ascii=False)

    print(f"✅ Generated {marketplace_file}")

    # Build README.md
    readme_content = build_readme(plugins_dir)
    readme_file = project_root / "README.md"

    with open(readme_file, "w", encoding="utf-8") as f:
        f.write(readme_content)

    print(f"✅ Generated {readme_file}")

    # Build individual plugin READMEs
    print("\nBuilding individual plugin READMEs...")
    build_plugin_readmes(plugins_dir)

    # Summary
    plugin_count = len(marketplace.get("plugins", []))
    print(f"\n📦 Built marketplace with {plugin_count} plugins")

    if plugin_count == 0:
        print("⚠️  No plugins found. Check the plugins/ directory structure.")


if __name__ == "__main__":
    main()
