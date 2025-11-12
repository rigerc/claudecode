#!/usr/bin/env python3
"""
Initialize a new Claude Code plugin with proper structure.

Usage:
    python init_plugin.py <plugin-name> [--path <output-directory>]

Examples:
    python init_plugin.py my-awesome-plugin --path ~/plugins
    python init_plugin.py my-plugin

Marketplace:
    By default, creates .dev-marketplace/ for immediate local testing.
"""

import argparse
import json
import sys
from pathlib import Path


def create_plugin_manifest(plugin_name: str, description: str = "") -> dict:
    """Create a basic plugin.json manifest with comprehensive component registration."""
    manifest = {
        "name": plugin_name,
        "version": "0.1.0",
        "description": description or f"A Claude Code plugin for {plugin_name}",
        "author": {
            "name": "Plugin Author",
            "email": "author@example.com"
        },
        "repository": "",
        "license": "MIT",
        # Register all components (arrays support multiple items; single strings also valid)
        "skills": ["./skills/example-skill/SKILL.md"],
        "commands": ["./commands/example.md"],
        "agents": ["./agents/example-agent.md"],
        "hooks": ["./hooks/hooks.json"]
    }

    # Note: Component fields accept either string or array format:
    #   Single: "commands": "./commands/example.md"
    #   Multiple: "commands": ["./commands/cmd1.md", "./commands/cmd2.md"]
    # Arrays used here for consistency and easier addition of components

    return manifest


def get_template_path(template_name: str) -> Path:
    """Get the path to a template file in the assets directory."""
    # Get the directory where this script is located
    script_dir = Path(__file__).parent
    # Navigate to the assets directory (../assets/)
    assets_dir = script_dir.parent / "assets"
    return assets_dir / template_name


def load_template(template_name: str) -> str:
    """Load a template file from the assets directory."""
    template_path = get_template_path(template_name)
    if not template_path.exists():
        print(f"⚠️  Warning: Template not found: {template_path}")
        return ""
    with open(template_path, 'r') as f:
        return f.read()


def write_template_file(template_name: str, output_path: Path, description: str, plugin_dir: Path) -> None:
    """Write a template file and print success message."""
    template = load_template(template_name)
    with open(output_path, 'w') as f:
        f.write(template)
    print(f"✅ Created {description}: {output_path.relative_to(plugin_dir)}")


def init_plugin(plugin_name: str, output_path: Path) -> None:
    """Initialize a new plugin with standard directory structure."""

    # Validate plugin name (kebab-case)
    if not all(c.islower() or c.isdigit() or c == '-' for c in plugin_name):
        print(f"❌ Error: Plugin name must be in kebab-case (lowercase with hyphens)")
        sys.exit(1)

    # Create plugin directory
    plugin_dir = output_path / plugin_name
    if plugin_dir.exists():
        print(f"❌ Error: Directory already exists: {plugin_dir}")
        sys.exit(1)

    print(f"🚀 Initializing plugin: {plugin_name}")
    print(f"   Location: {plugin_dir}\n")

    # Create standard directory structure (per official docs)
    dirs_to_create = [
        plugin_dir / ".claude-plugin",
        plugin_dir / "commands",
        plugin_dir / "agents",
        plugin_dir / "skills" / "example-skill",
        plugin_dir / "hooks",
    ]

    for dir_path in dirs_to_create:
        dir_path.mkdir(parents=True, exist_ok=True)
        print(f"✅ Created directory: {dir_path.relative_to(plugin_dir)}")

    # Create plugin.json manifest
    manifest_path = plugin_dir / ".claude-plugin" / "plugin.json"
    manifest = create_plugin_manifest(plugin_name)
    with open(manifest_path, 'w') as f:
        json.dump(manifest, f, indent=2)
    print(f"✅ Created manifest: .claude-plugin/plugin.json")

    # Create example components from templates
    write_template_file("command-template.md", plugin_dir / "commands" / "example.md", "example command", plugin_dir)
    write_template_file("agent-template.md", plugin_dir / "agents" / "example-agent.md", "example agent", plugin_dir)
    write_template_file("skill-template.md", plugin_dir / "skills" / "example-skill" / "SKILL.md", "example skill", plugin_dir)
    write_template_file("hooks-template.json", plugin_dir / "hooks" / "hooks.json", "hooks configuration", plugin_dir)

    # Create README
    readme_path = plugin_dir / "README.md"
    with open(readme_path, 'w') as f:
        f.write(f"# {plugin_name}\n\n{manifest['description']}\n\n## Installation\n\nTBD\n\n## Usage\n\nTBD\n")
    print(f"✅ Created README.md")

    # Create local development marketplace
    marketplace_dir = plugin_dir / ".dev-marketplace" / ".claude-plugin"
    marketplace_dir.mkdir(parents=True, exist_ok=True)

    marketplace_config = {
        "name": "local-dev",
        "owner": {
            "name": manifest["author"]["name"] or "Plugin Author"
        },
        "plugins": [
            {
                "name": plugin_name,
                "source": "./../../"
            }
        ]
    }

    marketplace_path = marketplace_dir / "marketplace.json"
    with open(marketplace_path, 'w') as f:
        json.dump(marketplace_config, f, indent=2)
    print(f"✅ Created local marketplace: .dev-marketplace/.claude-plugin/marketplace.json")

    # Create MCP server configuration
    mcp_template = load_template("mcp-template.json")
    mcp_path = plugin_dir / ".mcp.json"
    with open(mcp_path, 'w') as f:
        f.write(mcp_template)
    print(f"✅ Created MCP configuration: .mcp.json")

    print(f"\n✅ Plugin '{plugin_name}' initialized successfully at {plugin_dir}")

    print("\nNext steps:")
    print("1. Delete unused component directories and update plugin.json accordingly")
    print("2. Edit .claude-plugin/plugin.json to customize metadata and components")
    print("3. Customize remaining components with your actual functionality")
    print("4. See .mcp.json for additional MCP server configuration examples")
    print("5. Run 'claude plugin validate' to verify the plugin structure")

    print("\n📦 Local marketplace created! Install with:")
    print(f"   claude plugin marketplace add {plugin_dir.absolute()}/.dev-marketplace/.claude-plugin/marketplace.json")
    print(f"   claude plugin install {plugin_name}@local-dev")


def main():
    parser = argparse.ArgumentParser(
        description="Initialize a new Claude Code plugin"
    )
    parser.add_argument(
        "plugin_name",
        help="Name of the plugin (kebab-case format)"
    )
    parser.add_argument(
        "--path",
        type=Path,
        default=Path.cwd(),
        help="Output directory for the plugin (default: current directory)"
    )

    args = parser.parse_args()

    # Ensure output path exists
    args.path.mkdir(parents=True, exist_ok=True)

    init_plugin(args.plugin_name, args.path)


if __name__ == "__main__":
    main()
