#!/usr/bin/env python3
"""
Dynamically builds marketplace.json and README.md based on plugins directory contents.

This script scans the plugins directory, extracts metadata from plugin files,
and generates a marketplace configuration and documentation.
"""

import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional
from datetime import datetime, timezone


# ============================================================================
# Data Classes
# ============================================================================


@dataclass
class ComponentInfo:
    """Information about a plugin component."""

    name: str
    description: str


@dataclass
class PluginComponents:
    """All components within a plugin."""

    commands: List[ComponentInfo]
    agents: List[ComponentInfo]
    skills: List[ComponentInfo]
    hooks: List[ComponentInfo]
    mcp_servers: List[ComponentInfo]

    def __init__(self):
        self.commands = []
        self.agents = []
        self.skills = []
        self.hooks = []
        self.mcp_servers = []

    def get_counts(self) -> Dict[str, int]:
        """Get count of each component type."""
        return {
            "commands": len(self.commands),
            "agents": len(self.agents),
            "skills": len(self.skills),
            "hooks": len(self.hooks),
            "mcp_servers": len(self.mcp_servers),
        }


@dataclass
class PluginInfo:
    """Plugin metadata and information."""

    name: str
    key: str
    description: str
    source: str
    components: PluginComponents


# ============================================================================
# Text Extraction and Processing
# ============================================================================


class TextExtractor:
    """Handles extraction of text content from various file formats."""

    DEFAULT_PLUGIN_DESC = "Specialized tools for enhanced development workflows"
    DEFAULT_COMPONENT_DESC = "No description available"
    MAX_PLUGIN_DESC_LENGTH = 200
    MAX_COMPONENT_DESC_LENGTH = 150

    @staticmethod
    def extract_plugin_description(plugin_dir: Path) -> str:
        """Extract description from plugin README.md - text between first and second heading."""
        readme_path = plugin_dir / "README.md"

        if not readme_path.exists():
            return TextExtractor.DEFAULT_PLUGIN_DESC

        try:
            content = readme_path.read_text(encoding="utf-8")
            lines = content.split("\n")

            description_lines = []
            in_description = False
            heading_count = 0

            for line in lines:
                line = line.strip()

                # Track headings to find description boundaries
                if line.startswith("#"):
                    heading_count += 1
                    if heading_count == 1:
                        in_description = True
                        continue
                    elif heading_count == 2:
                        break

                # Collect description text
                if in_description and line and not line.startswith("#"):
                    description_lines.append(line)

            if description_lines:
                description = " ".join(description_lines)
                return TextExtractor._clean_and_truncate(
                    description, TextExtractor.MAX_PLUGIN_DESC_LENGTH
                )

        except (FileNotFoundError, UnicodeDecodeError) as e:
            print(f"Warning: Could not read {readme_path}: {e}")

        return TextExtractor.DEFAULT_PLUGIN_DESC

    @staticmethod
    def extract_component_description(file_path: Path) -> str:
        """Extract description from component file (YAML frontmatter or first paragraph)."""
        if not file_path.exists():
            return TextExtractor.DEFAULT_COMPONENT_DESC

        try:
            content = file_path.read_text(encoding="utf-8")
            lines = content.split("\n")

            # Try YAML frontmatter first
            if lines and lines[0].strip() == "---":
                yaml_desc = TextExtractor._extract_from_yaml(lines[1:])
                if yaml_desc:
                    return yaml_desc

            # Fallback to first paragraph
            return TextExtractor._extract_first_paragraph(lines)

        except (FileNotFoundError, UnicodeDecodeError) as e:
            print(f"Warning: Could not read {file_path}: {e}")

        return TextExtractor.DEFAULT_COMPONENT_DESC

    @staticmethod
    def _extract_from_yaml(lines: List[str]) -> Optional[str]:
        """Extract description from YAML frontmatter."""
        for line in lines:
            if line.strip() == "---":
                break

            if line.strip().startswith("description:"):
                match = re.match(r"description:\s*(.+)", line.strip())
                if match:
                    description = match.group(1).strip()
                    # Remove quotes
                    description = description.strip("\"'")
                    return TextExtractor._clean_and_truncate(
                        description, TextExtractor.MAX_COMPONENT_DESC_LENGTH
                    )
        return None

    @staticmethod
    def _extract_first_paragraph(lines: List[str]) -> str:
        """Extract first paragraph after heading."""
        description_lines = []
        started = False

        for line in lines:
            line = line.strip()

            if not line or line.startswith("#"):
                if line.startswith("#") and started:
                    break
                continue

            if not started:
                started = True

            description_lines.append(line)
            if len(description_lines) >= 3:
                break

        if description_lines:
            description = " ".join(description_lines)
            return TextExtractor._clean_and_truncate(
                description, TextExtractor.MAX_COMPONENT_DESC_LENGTH
            )

        return TextExtractor.DEFAULT_COMPONENT_DESC

    @staticmethod
    def _clean_and_truncate(text: str, max_length: int) -> str:
        """Clean up whitespace and truncate text to maximum length."""
        text = re.sub(r"\s+", " ", text).strip()
        if len(text) > max_length:
            return text[: max_length - 3] + "..."
        return text


# ============================================================================
# Component Discovery
# ============================================================================


class ComponentDiscovery:
    """Discovers and catalogs plugin components."""

    @staticmethod
    def discover_all(plugin_dir: Path) -> PluginComponents:
        """Discover all components in a plugin directory."""
        components = PluginComponents()

        components.commands = ComponentDiscovery._discover_commands(plugin_dir)
        components.agents = ComponentDiscovery._discover_agents(plugin_dir)
        components.skills = ComponentDiscovery._discover_skills(plugin_dir)
        components.hooks = ComponentDiscovery._discover_hooks(plugin_dir)
        components.mcp_servers = ComponentDiscovery._discover_mcp_servers(plugin_dir)

        return components

    @staticmethod
    def _discover_commands(plugin_dir: Path) -> List[ComponentInfo]:
        """Discover command components."""
        commands_dir = plugin_dir / "commands"
        if not commands_dir.exists():
            return []

        return [
            ComponentInfo(
                name=cmd_file.stem,
                description=TextExtractor.extract_component_description(cmd_file),
            )
            for cmd_file in sorted(commands_dir.glob("*.md"))
        ]

    @staticmethod
    def _discover_agents(plugin_dir: Path) -> List[ComponentInfo]:
        """Discover agent components."""
        agents_dir = plugin_dir / "agents"
        if not agents_dir.exists():
            return []

        return [
            ComponentInfo(
                name=agent_file.stem,
                description=TextExtractor.extract_component_description(agent_file),
            )
            for agent_file in sorted(agents_dir.glob("*.md"))
        ]

    @staticmethod
    def _discover_skills(plugin_dir: Path) -> List[ComponentInfo]:
        """Discover skill components."""
        skills_dir = plugin_dir / "skills"
        if not skills_dir.exists():
            return []

        skills = []
        for skill_dir in sorted(skills_dir.iterdir()):
            skill_file = skill_dir / "SKILL.md"
            if skill_dir.is_dir() and skill_file.exists():
                skills.append(
                    ComponentInfo(
                        name=skill_dir.name,
                        description=TextExtractor.extract_component_description(
                            skill_file
                        ),
                    )
                )
        return skills

    @staticmethod
    def _discover_hooks(plugin_dir: Path) -> List[ComponentInfo]:
        """Discover hook components."""
        hooks_dir = plugin_dir / "hooks"
        if not hooks_dir.exists():
            return []

        hooks_json = hooks_dir / "hooks.json"
        if hooks_json.exists():
            return ComponentDiscovery._parse_hooks_json(hooks_json)

        # Fallback to markdown files
        return [
            ComponentInfo(
                name=hook_file.stem,
                description=TextExtractor.extract_component_description(hook_file),
            )
            for hook_file in sorted(hooks_dir.glob("*.md"))
        ]

    @staticmethod
    def _parse_hooks_json(hooks_json: Path) -> List[ComponentInfo]:
        """Parse hooks from hooks.json file."""
        try:
            with open(hooks_json, "r", encoding="utf-8") as f:
                hooks_data = json.load(f)

            hooks = []
            if isinstance(hooks_data, dict) and "hooks" in hooks_data:
                hooks_section = hooks_data["hooks"]
                if isinstance(hooks_section, dict):
                    for hook_event, hook_configs in hooks_section.items():
                        if isinstance(hook_configs, list):
                            for i, hook_config in enumerate(hook_configs):
                                if isinstance(hook_config, dict):
                                    hooks.append(
                                        ComponentInfo(
                                            name=f"{hook_event}_{i}",
                                            description=hook_config.get(
                                                "description", f"Hook for {hook_event}"
                                            ),
                                        )
                                    )
                elif isinstance(hooks_section, list):
                    for hook in hooks_section:
                        if isinstance(hook, dict):
                            hooks.append(
                                ComponentInfo(
                                    name=hook.get("name", "Unknown"),
                                    description=hook.get(
                                        "description", "No description"
                                    ),
                                )
                            )
            elif isinstance(hooks_data, list):
                for hook in hooks_data:
                    hooks.append(
                        ComponentInfo(
                            name=hook.get("name", "Unknown"),
                            description=hook.get("description", "No description"),
                        )
                    )
            return hooks

        except (json.JSONDecodeError, FileNotFoundError):
            return []

    @staticmethod
    def _discover_mcp_servers(plugin_dir: Path) -> List[ComponentInfo]:
        """Discover MCP server components."""
        mcp_dir = plugin_dir / "mcp_servers"
        if not mcp_dir.exists():
            return []

        mcp_servers = []
        for mcp_file in sorted(mcp_dir.glob("*.json")):
            try:
                with open(mcp_file, "r", encoding="utf-8") as f:
                    mcp_data = json.load(f)
                    mcp_servers.append(
                        ComponentInfo(
                            name=mcp_file.stem,
                            description=mcp_data.get(
                                "description", "No description available"
                            ),
                        )
                    )
            except (json.JSONDecodeError, FileNotFoundError):
                mcp_servers.append(
                    ComponentInfo(name=mcp_file.stem, description="Configuration file")
                )

        return mcp_servers


# ============================================================================
# Plugin Management
# ============================================================================


class PluginManager:
    """Manages plugin discovery and metadata extraction."""

    MARKETPLACE_NAME = "rigerc-claude"

    @staticmethod
    def get_plugin_name_from_json(plugin_dir: Path) -> str:
        """Get plugin name from .claude-plugin/plugin.json, fallback to directory name."""
        plugin_json_path = plugin_dir / ".claude-plugin" / "plugin.json"

        if plugin_json_path.exists():
            try:
                with open(plugin_json_path, "r", encoding="utf-8") as f:
                    plugin_data = json.load(f)
                    return plugin_data.get("name", plugin_dir.name)
            except (json.JSONDecodeError, FileNotFoundError):
                pass

        return plugin_dir.name

    @staticmethod
    def format_plugin_name(plugin_name: str) -> str:
        """Convert plugin name to proper title format."""
        # Handle camelCase
        name = re.sub(r"(?<!^)(?=[A-Z])", " ", plugin_name)
        # Replace hyphens with spaces
        name = name.replace("-", " ")
        # Title case
        return " ".join(name.split()).title()

    @staticmethod
    def generate_anchor(plugin_name: str) -> str:
        """Generate URL-safe anchor from plugin name."""
        return plugin_name.lower().replace(" ", "-")

    @staticmethod
    def extract_plugin_info(plugin_dir: Path) -> PluginInfo:
        """Extract complete plugin information."""
        plugin_json_name = PluginManager.get_plugin_name_from_json(plugin_dir)
        plugin_name = PluginManager.format_plugin_name(plugin_json_name)
        plugin_key = plugin_dir.name

        # Try to get description from plugin.json first
        description = PluginManager._get_description_from_json(plugin_dir)
        if not description:
            description = TextExtractor.extract_plugin_description(plugin_dir)

        # Discover all components
        components = ComponentDiscovery.discover_all(plugin_dir)

        return PluginInfo(
            name=plugin_name,
            key=plugin_key,
            description=description,
            source=f"./plugins/{plugin_key}",
            components=components,
        )

    @staticmethod
    def _get_description_from_json(plugin_dir: Path) -> Optional[str]:
        """Get description from plugin.json if available."""
        plugin_json_path = plugin_dir / ".claude-plugin" / "plugin.json"

        if plugin_json_path.exists():
            try:
                with open(plugin_json_path, "r", encoding="utf-8") as f:
                    plugin_data = json.load(f)
                    return plugin_data.get("description")
            except (json.JSONDecodeError, FileNotFoundError):
                pass

        return None

    @staticmethod
    def discover_plugins(plugins_dir: Path) -> List[PluginInfo]:
        """Discover all valid plugins in the plugins directory."""
        if not plugins_dir.exists():
            print(f"Warning: Plugins directory {plugins_dir} does not exist")
            return []

        plugins = []
        for plugin_dir in plugins_dir.iterdir():
            if not plugin_dir.is_dir() or plugin_dir.name.startswith("."):
                continue

            # Check if it's a valid plugin
            plugin_json = plugin_dir / ".claude-plugin" / "plugin.json"
            readme = plugin_dir / "README.md"

            if plugin_json.exists() or readme.exists():
                try:
                    plugin_info = PluginManager.extract_plugin_info(plugin_dir)
                    plugins.append(plugin_info)
                    print(f"✓ Discovered plugin: {plugin_info.name}")
                except Exception as e:
                    print(f"✗ Error processing plugin {plugin_dir.name}: {e}")

        # Sort by name
        plugins.sort(key=lambda x: x.name)
        return plugins


# ============================================================================
# Version Management
# ============================================================================


class VersionManager:
    """Manages marketplace version numbering."""

    DEFAULT_VERSION = "1.0.0"

    @staticmethod
    def get_current_version(marketplace_file: Path) -> str:
        """Get current version from existing marketplace file."""
        if marketplace_file.exists():
            try:
                with open(marketplace_file, "r", encoding="utf-8") as f:
                    marketplace = json.load(f)
                    return marketplace.get("metadata", {}).get(
                        "version", VersionManager.DEFAULT_VERSION
                    )
            except (json.JSONDecodeError, FileNotFoundError):
                pass
        return VersionManager.DEFAULT_VERSION

    @staticmethod
    def increment_version(version: str) -> str:
        """Increment patch version (x.y.z -> x.y.z+1)."""
        try:
            parts = version.split(".")
            if len(parts) == 3:
                major, minor, patch = map(int, parts)
                return f"{major}.{minor}.{patch + 1}"
        except (ValueError, IndexError):
            pass
        return "1.0.1"


# ============================================================================
# Generators
# ============================================================================


class MarketplaceGenerator:
    """Generates marketplace.json configuration."""

    @staticmethod
    def generate(plugins: List[PluginInfo], marketplace_file: Path) -> Dict[str, Any]:
        """Generate marketplace.json structure."""
        current_version = VersionManager.get_current_version(marketplace_file)
        new_version = VersionManager.increment_version(current_version)

        print(f"Version: {current_version} -> {new_version}")

        return {
            "name": PluginManager.MARKETPLACE_NAME,
            "owner": {"name": "rigerc's Claude personal marketplace"},
            "metadata": {
                "version": new_version,
                "description": "A curated collection of specialized plugins for Claude Code, "
                "organized by functionality to provide focused tools for specific development tasks.",
                "lastUpdated": datetime.now(timezone.utc)
                .isoformat()
                .replace("+00:00", "Z"),
            },
            "plugins": [
                {
                    "name": plugin.key,
                    "source": plugin.source,
                    "description": plugin.description,
                }
                for plugin in plugins
            ],
        }


class ReadmeGenerator:
    """Generates README.md documentation."""

    @staticmethod
    def generate_main_readme(plugins: List[PluginInfo]) -> str:
        """Generate main README.md for the marketplace."""
        toc = ReadmeGenerator._generate_toc(plugins)
        plugin_details = ReadmeGenerator._generate_plugin_details(plugins)
        summary = ReadmeGenerator._generate_summary(plugins)

        return f"""# Claude Extensions Plugin Collection

A curated collection of specialized plugins for Claude Code, organized by functionality to provide focused tools for specific development tasks.

## Table of Contents

- [🚀 Installation](#installation)
  - [Add Marketplace](#add-marketplace)
  - [Install Individual Plugins](#install-individual-plugins)
  - [Browse Available Plugins](#browse-available-plugins)
- [🔌 Plugin Details](#plugin-details)
{toc}
- [📁 Plugin Structure](#plugin-structure)
- [🛠️ Development](#️development)
  - [Building](#building)
  - [Plugin Categories](#plugin-categories)
- [📄 License](#license)

## Collection Summary

{summary}

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
/plugin install claude-code-development@{PluginManager.MARKETPLACE_NAME}
/plugin install bash-scripting@{PluginManager.MARKETPLACE_NAME}
/plugin install documentation-generation@{PluginManager.MARKETPLACE_NAME}
```

### Browse Available Plugins

```bash
/plugin
# Select "Browse Plugins" from {PluginManager.MARKETPLACE_NAME} marketplace
# Install desired plugins
```

---

## 🔌 Plugin Details

{plugin_details}

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

    @staticmethod
    def _generate_toc(plugins: List[PluginInfo]) -> str:
        """Generate table of contents for plugins."""
        lines = []
        for plugin in plugins:
            anchor = PluginManager.generate_anchor(plugin.name)
            lines.append(f"  - [{plugin.name}](#{anchor})")
        return "\n".join(lines)

    @staticmethod
    def _generate_summary(plugins: List[PluginInfo]) -> str:
        """Generate collection summary statistics."""
        total_commands = sum(len(p.components.commands) for p in plugins)
        total_agents = sum(len(p.components.agents) for p in plugins)
        total_skills = sum(len(p.components.skills) for p in plugins)
        total_hooks = sum(len(p.components.hooks) for p in plugins)
        total_mcp = sum(len(p.components.mcp_servers) for p in plugins)

        return f"""- **{len(plugins)} Specialized Plugins**
- **{total_commands} Custom Commands**
- **{total_agents} Expert Agents**
- **{total_skills} Specialized Skills**
- **{total_hooks} Hooks**
- **{total_mcp} MCP Servers**"""

    @staticmethod
    def _generate_plugin_details(plugins: List[PluginInfo]) -> str:
        """Generate detailed plugin information section."""
        lines = []

        for i, plugin in enumerate(plugins):
            if i > 0:
                lines.append("---\n")

            lines.append(f"### {plugin.name}\n")
            lines.append(f"{plugin.description}\n")
            lines.append(
                f"**📦 Install**: `/plugin install {plugin.key}@{PluginManager.MARKETPLACE_NAME}`\n"
            )

            # Add component details
            components = plugin.components

            if components.commands:
                lines.append(f"\n**Commands** ({len(components.commands)}):")
                for cmd in components.commands:
                    lines.append(f"- `{cmd.name}`: {cmd.description}")
                lines.append("")

            if components.agents:
                lines.append(f"\n**Agents** ({len(components.agents)}):")
                for agent in components.agents:
                    lines.append(f"- **{agent.name}**: {agent.description}")
                lines.append("")

            if components.skills:
                lines.append(f"\n**Skills** ({len(components.skills)}):")
                for skill in components.skills:
                    lines.append(f"- **{skill.name}**: {skill.description}")
                lines.append("")

            if components.hooks:
                lines.append(f"\n**Hooks** ({len(components.hooks)}):")
                for hook in components.hooks:
                    lines.append(f"- **{hook.name}**: {hook.description}")
                lines.append("")

            if components.mcp_servers:
                lines.append(f"\n**MCP Servers** ({len(components.mcp_servers)}):")
                for mcp in components.mcp_servers:
                    lines.append(f"- **{mcp.name}**: {mcp.description}")
                lines.append("")

        return "\n".join(lines)

    @staticmethod
    def generate_plugin_readme(plugin: PluginInfo) -> str:
        """Generate individual plugin README."""
        components = plugin.components

        # Build component sections
        sections = []

        if components.commands:
            sections.append(f"## Commands ({len(components.commands)})\n")
            for cmd in components.commands:
                sections.append(f"### `{cmd.name}`\n{cmd.description}\n")

        if components.agents:
            sections.append(f"## Agents ({len(components.agents)})\n")
            for agent in components.agents:
                sections.append(f"### {agent.name}\n{agent.description}\n")

        if components.skills:
            sections.append(f"## Skills ({len(components.skills)})\n")
            for skill in components.skills:
                sections.append(f"### {skill.name}\n{skill.description}\n")

        if components.hooks:
            sections.append(f"## Hooks ({len(components.hooks)})\n")
            for hook in components.hooks:
                sections.append(f"### {hook.name}\n{hook.description}\n")

        if components.mcp_servers:
            sections.append(f"## MCP Servers ({len(components.mcp_servers)})\n")
            for mcp in components.mcp_servers:
                sections.append(f"### {mcp.name}\n{mcp.description}\n")

        component_section = (
            "\n".join(sections) if sections else "No components defined.\n"
        )

        return f"""# {plugin.name}

{plugin.description}

## Overview

This plugin provides the following components:

{component_section}

## Installation

Install this plugin from the {PluginManager.MARKETPLACE_NAME} marketplace:

```bash
/plugin install {plugin.key}@{PluginManager.MARKETPLACE_NAME}
```

## Usage

After installation, the components provided by this plugin will be available in your Claude Code environment.

- **Commands** can be used with slash commands (e.g., `/command-name`)
- **Agents** provide specialized expertise for specific tasks
- **Skills** enhance agent capabilities for particular domains
- **Hooks** automate workflows and git operations
- **MCP Servers** provide external tool integrations

## Development

This plugin is part of the {PluginManager.MARKETPLACE_NAME} marketplace collection. For development details, see the main repository.

---

*This README is automatically generated. Do not edit manually - run `python scripts/build-marketplace.py` to update.*
"""


# ============================================================================
# Main Build Process
# ============================================================================


class MarketplaceBuilder:
    """Orchestrates the marketplace build process."""

    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.plugins_dir = project_root / "plugins"
        self.marketplace_dir = project_root / ".claude-plugin"
        self.marketplace_file = self.marketplace_dir / "marketplace.json"
        self.readme_file = project_root / "README.md"

    def build(self):
        """Execute the complete build process."""
        print("=" * 70)
        print("Building marketplace configuration and documentation")
        print("=" * 70)

        # Ensure directories exist
        self.marketplace_dir.mkdir(exist_ok=True)

        # Discover plugins
        print("\n📂 Discovering plugins...")
        plugins = PluginManager.discover_plugins(self.plugins_dir)

        if not plugins:
            print("⚠️  No plugins found. Check the plugins/ directory structure.")
            return

        print(f"\n✓ Found {len(plugins)} plugins")

        # Generate marketplace.json
        print("\n📄 Generating marketplace.json...")
        marketplace_data = MarketplaceGenerator.generate(plugins, self.marketplace_file)

        with open(self.marketplace_file, "w", encoding="utf-8") as f:
            json.dump(marketplace_data, f, indent=2, ensure_ascii=False)

        print(f"✓ Generated {self.marketplace_file}")

        # Generate main README
        print("\n📝 Generating main README.md...")
        readme_content = ReadmeGenerator.generate_main_readme(plugins)

        with open(self.readme_file, "w", encoding="utf-8") as f:
            f.write(readme_content)

        print(f"✓ Generated {self.readme_file}")

        # Generate individual plugin READMEs
        print("\n📚 Generating individual plugin READMEs...")
        self._build_plugin_readmes(plugins)

        # Summary
        print("\n" + "=" * 70)
        print(f"✅ Successfully built marketplace with {len(plugins)} plugins")
        print("=" * 70)

    def _content_would_change(self, file_path: Path, new_content: str) -> bool:
        """Check if writing new content would change the file."""
        if not file_path.exists():
            return True

        try:
            existing_content = file_path.read_text(encoding="utf-8")
            return existing_content != new_content
        except (FileNotFoundError, UnicodeDecodeError):
            return True

    def _build_plugin_readmes(self, plugins: List[PluginInfo]):
        """Generate README for each plugin, only if content would change."""
        for plugin in plugins:
            plugin_dir = self.plugins_dir / plugin.key
            readme_path = plugin_dir / "README.md"

            readme_content = ReadmeGenerator.generate_plugin_readme(plugin)

            if self._content_would_change(readme_path, readme_content):
                with open(readme_path, "w", encoding="utf-8") as f:
                    f.write(readme_content)
                print(f"  ✓ {readme_path}")
            else:
                print(f"  ⏭ {readme_path} (no changes)")


# ============================================================================
# Entry Point
# ============================================================================


def main():
    """Main entry point."""
    script_dir = Path(__file__).parent
    project_root = script_dir.parent

    builder = MarketplaceBuilder(project_root)
    builder.build()


if __name__ == "__main__":
    main()
