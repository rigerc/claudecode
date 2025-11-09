#!/usr/bin/env python3
"""
Comprehensive validation script for Claude Code plugins and marketplace configuration.
Based on official Claude Code plugin marketplace specifications.
"""

import json
import os
import re
import sys
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from urllib.parse import urlparse
import argparse

class ValidationError:
    def __init__(self, file_path: str, message: str, severity: str = "error"):
        self.file_path = file_path
        self.message = message
        self.severity = severity  # "error", "warning", "info"

    def __str__(self):
        return f"[{self.severity.upper()}] {self.file_path}: {self.message}"

def validate_plugin_name(name: str) -> List[ValidationError]:
    """Validate plugin name follows kebab-case convention."""
    errors = []

    if not name:
        errors.append(ValidationError("", "Plugin name is required"))
        return errors

    # Check kebab-case (lowercase, hyphens, no spaces)
    if not re.match(r'^[a-z0-9-]+$', name):
        errors.append(ValidationError(
            "",
            f"Plugin name '{name}' must be kebab-case (lowercase, hyphens, numbers only)"
        ))

    # Check for consecutive hyphens
    if '--' in name:
        errors.append(ValidationError(
            "",
            f"Plugin name '{name}' should not contain consecutive hyphens"
        ))

    # Check for leading/trailing hyphens
    if name.startswith('-') or name.endswith('-'):
        errors.append(ValidationError(
            "",
            f"Plugin name '{name}' should not start or end with hyphens"
        ))

    return errors

def validate_plugin_manifest(plugin_dir: Path) -> List[ValidationError]:
    """Validate plugin.json according to official schema."""
    errors = []
    manifest_path = plugin_dir / ".claude-plugin" / "plugin.json"

    if not manifest_path.exists():
        errors.append(ValidationError(
            str(manifest_path),
            "plugin.json is required"
        ))
        return errors

    try:
        with open(manifest_path, 'r', encoding='utf-8') as f:
            manifest = json.load(f)
    except json.JSONDecodeError as e:
        errors.append(ValidationError(
            str(manifest_path),
            f"Invalid JSON: {e}"
        ))
        return errors

    # Required fields
    required_fields = ["name"]
    for field in required_fields:
        if field not in manifest:
            errors.append(ValidationError(
                str(manifest_path),
                f"Required field '{field}' is missing"
            ))

    # Validate name if present
    if "name" in manifest:
        errors.extend(validate_plugin_name(manifest["name"]))

    # Optional fields with validation
    string_fields = ["version", "description", "homepage", "repository", "license"]
    for field in string_fields:
        if field in manifest and not isinstance(manifest[field], str):
            errors.append(ValidationError(
                str(manifest_path),
                f"Field '{field}' must be a string"
            ))

    # Validate author object
    if "author" in manifest:
        author = manifest["author"]
        if not isinstance(author, dict):
            errors.append(ValidationError(
                str(manifest_path),
                "Field 'author' must be an object"
            ))
        else:
            if "name" in author and not isinstance(author["name"], str):
                errors.append(ValidationError(
                    str(manifest_path),
                    "Author name must be a string"
                ))

    # Validate keywords
    if "keywords" in manifest:
        keywords = manifest["keywords"]
        if not isinstance(keywords, list):
            errors.append(ValidationError(
                str(manifest_path),
                "Field 'keywords' must be an array"
            ))
        elif not all(isinstance(k, str) for k in keywords):
            errors.append(ValidationError(
                str(manifest_path),
                "All keywords must be strings"
            ))

    # Validate component paths
    component_fields = ["commands", "agents", "hooks", "mcpServers"]
    for field in component_fields:
        if field in manifest:
            value = manifest[field]
            if field in ["commands", "agents"]:
                # Can be string or array of strings
                if isinstance(value, str):
                    if not value.strip():
                        errors.append(ValidationError(
                            str(manifest_path),
                            f"Field '{field}' cannot be empty string"
                        ))
                elif isinstance(value, list):
                    if not all(isinstance(item, str) for item in value):
                        errors.append(ValidationError(
                            str(manifest_path),
                            f"Field '{field}' array must contain only strings"
                        ))
                else:
                    errors.append(ValidationError(
                        str(manifest_path),
                        f"Field '{field}' must be a string or array of strings"
                    ))
            elif field in ["hooks", "mcpServers"]:
                # Must be object
                if not isinstance(value, dict):
                    errors.append(ValidationError(
                        str(manifest_path),
                        f"Field '{field}' must be an object"
                    ))

    return errors

def validate_plugin_structure(plugin_dir: Path) -> List[ValidationError]:
    """Validate plugin directory structure and component files."""
    errors = []

    if not plugin_dir.is_dir():
        errors.append(ValidationError(
            str(plugin_dir),
            "Plugin directory does not exist"
        ))
        return errors

    # Check for .claude-plugin directory
    claude_plugin_dir = plugin_dir / ".claude-plugin"
    if not claude_plugin_dir.exists():
        errors.append(ValidationError(
            str(claude_plugin_dir),
            ".claude-plugin directory is required"
        ))

    # Validate component directories and files
    component_dirs = ["commands", "agents", "skills", "hooks"]

    for component in component_dirs:
        component_path = plugin_dir / component
        if component_path.exists():
            if component == "skills":
                # Skills should contain directories with SKILL.md
                for skill_dir in component_path.iterdir():
                    if skill_dir.is_dir():
                        skill_md = skill_dir / "SKILL.md"
                        if not skill_md.exists():
                            errors.append(ValidationError(
                                str(skill_md),
                                f"Skill directory '{skill_dir.name}' must contain SKILL.md"
                            ))
            else:
                # Commands, agents, hooks should contain .md files
                md_files = list(component_path.glob("*.md"))
                if not md_files:
                    errors.append(ValidationError(
                        str(component_path),
                        f"{component.title()} directory exists but contains no .md files"
                    ))

    # Check for README.md
    readme_path = plugin_dir / "README.md"
    if not readme_path.exists():
        errors.append(ValidationError(
            str(readme_path),
            "README.md is recommended for better plugin discovery"
        ), "warning")

    return errors

def validate_marketplace_json(marketplace_path: Path) -> List[ValidationError]:
    """Validate marketplace.json according to official specifications."""
    errors = []

    if not marketplace_path.exists():
        errors.append(ValidationError(
            str(marketplace_path),
            "marketplace.json does not exist"
        ))
        return errors

    try:
        with open(marketplace_path, 'r', encoding='utf-8') as f:
            marketplace = json.load(f)
    except json.JSONDecodeError as e:
        errors.append(ValidationError(
            str(marketplace_path),
            f"Invalid JSON: {e}"
        ))
        return errors

    # Required fields
    required_fields = ["name", "owner", "plugins"]
    for field in required_fields:
        if field not in marketplace:
            errors.append(ValidationError(
                str(marketplace_path),
                f"Required field '{field}' is missing"
            ))

    # Validate marketplace name
    if "name" in marketplace:
        name_errors = validate_plugin_name(marketplace["name"])
        for error in name_errors:
            error.file_path = str(marketplace_path)
            error.message = error.message.replace("Plugin name", "Marketplace name")
        errors.extend(name_errors)

    # Validate owner
    if "owner" in marketplace:
        owner = marketplace["owner"]
        if not isinstance(owner, dict):
            errors.append(ValidationError(
                str(marketplace_path),
                "Field 'owner' must be an object"
            ))
        else:
            if "name" not in owner:
                errors.append(ValidationError(
                    str(marketplace_path),
                    "Owner must have a 'name' field"
                ))
            elif not isinstance(owner["name"], str):
                errors.append(ValidationError(
                    str(marketplace_path),
                    "Owner name must be a string"
                ))

    # Validate plugins array
    if "plugins" in marketplace:
        plugins = marketplace["plugins"]
        if not isinstance(plugins, list):
            errors.append(ValidationError(
                str(marketplace_path),
                "Field 'plugins' must be an array"
            ))
        else:
            for i, plugin in enumerate(plugins):
                plugin_errors = validate_marketplace_plugin_entry(plugin, marketplace_path, i)
                errors.extend(plugin_errors)

    # Validate optional metadata
    if "metadata" in marketplace:
        metadata = marketplace["metadata"]
        if not isinstance(metadata, dict):
            errors.append(ValidationError(
                str(marketplace_path),
                "Field 'metadata' must be an object"
            ))
        else:
            metadata_string_fields = ["description", "version", "pluginRoot"]
            for field in metadata_string_fields:
                if field in metadata and not isinstance(metadata[field], str):
                    errors.append(ValidationError(
                        str(marketplace_path),
                        f"Metadata field '{field}' must be a string"
                    ))

    return errors

def validate_marketplace_plugin_entry(plugin: Dict[str, Any], marketplace_path: Path, index: int) -> List[ValidationError]:
    """Validate individual plugin entry in marketplace.json."""
    errors = []
    plugin_context = f"plugins[{index}]"

    # Required fields
    if "name" not in plugin:
        errors.append(ValidationError(
            str(marketplace_path),
            f"{plugin_context}: Plugin name is required"
        ))
        return errors

    # Validate plugin name
    name_errors = validate_plugin_name(plugin["name"])
    for error in name_errors:
        error.file_path = f"{str(marketplace_path)} ({plugin_context})"
        errors.extend(name_errors)

    # Validate source
    if "source" not in plugin:
        errors.append(ValidationError(
            str(marketplace_path),
            f"{plugin_context} ({plugin.get('name', 'unknown')}): Source is required"
        ))
    else:
        source = plugin["source"]
        if isinstance(source, str):
            # Relative path source
            if not source.strip():
                errors.append(ValidationError(
                    str(marketplace_path),
                    f"{plugin_context} ({plugin['name']}): Source cannot be empty string"
                ))
        elif isinstance(source, dict):
            # Object source (github, git, etc.)
            if "source" not in source:
                errors.append(ValidationError(
                    str(marketplace_path),
                    f"{plugin_context} ({plugin['name']}): Source object must specify 'source' type"
                ))
            else:
                source_type = source["source"]
                if source_type == "github":
                    if "repo" not in source:
                        errors.append(ValidationError(
                            str(marketplace_path),
                            f"{plugin_context} ({plugin['name']}): GitHub source must specify 'repo'"
                        ))
                elif source_type == "url":
                    if "url" not in source:
                        errors.append(ValidationError(
                            str(marketplace_path),
                            f"{plugin_context} ({plugin['name']}): URL source must specify 'url'"
                        ))
                    else:
                        # Validate URL format
                        url = source["url"]
                        try:
                            parsed = urlparse(url)
                            if not parsed.scheme or not parsed.netloc:
                                errors.append(ValidationError(
                                    str(marketplace_path),
                                    f"{plugin_context} ({plugin['name']}): Invalid URL format"
                                ))
                        except:
                            errors.append(ValidationError(
                                str(marketplace_path),
                                f"{plugin_context} ({plugin['name']}): Invalid URL format"
                            ))
        else:
            errors.append(ValidationError(
                str(marketplace_path),
                f"{plugin_context} ({plugin['name']}): Source must be string or object"
            ))

    # Validate optional fields (same as plugin manifest)
    string_fields = ["version", "description", "homepage", "repository", "license", "category"]
    for field in string_fields:
        if field in plugin and not isinstance(plugin[field], str):
            errors.append(ValidationError(
                str(marketplace_path),
                f"{plugin_context} ({plugin['name']}): Field '{field}' must be a string"
            ))

    # Validate tags
    if "tags" in plugin:
        tags = plugin["tags"]
        if not isinstance(tags, list):
            errors.append(ValidationError(
                str(marketplace_path),
                f"{plugin_context} ({plugin['name']}): Field 'tags' must be an array"
            ))
        elif not all(isinstance(tag, str) for tag in tags):
            errors.append(ValidationError(
                str(marketplace_path),
                f"{plugin_context} ({plugin['name']}): All tags must be strings"
            ))

    # Validate strict field
    if "strict" in plugin and not isinstance(plugin["strict"], bool):
        errors.append(ValidationError(
            str(marketplace_path),
            f"{plugin_context} ({plugin['name']}): Field 'strict' must be a boolean"
        ))

    return errors

def validate_plugin_sources(marketplace_path: Path, plugins_dir: Path) -> List[ValidationError]:
    """Validate that all plugin sources in marketplace actually exist."""
    errors = []

    if not marketplace_path.exists():
        return errors

    try:
        with open(marketplace_path, 'r', encoding='utf-8') as f:
            marketplace = json.load(f)

        if "plugins" not in marketplace:
            return errors

        for plugin in marketplace["plugins"]:
            plugin_name = plugin.get("name", "unknown")
            source = plugin.get("source", "")

            if isinstance(source, str) and source.startswith("./"):
                # Relative path - check if it exists locally
                plugin_path = plugins_dir.parent / source
                if not plugin_path.exists():
                    errors.append(ValidationError(
                        str(marketplace_path),
                        f"Plugin '{plugin_name}' source path does not exist: {source}"
                    ))
                elif not (plugin_path / ".claude-plugin" / "plugin.json").exists():
                    errors.append(ValidationError(
                        str(marketplace_path),
                        f"Plugin '{plugin_name}' missing plugin.json at: {source}"
                    ))
            elif isinstance(source, dict):
                # GitHub or other structured source
                source_type = source.get("source", "")
                if source_type == "github":
                    # For GitHub sources, validate the repository format
                    repo = source.get("repo", "")
                    if not repo:
                        errors.append(ValidationError(
                            str(marketplace_path),
                            f"Plugin '{plugin_name}' GitHub source missing 'repo' field"
                        ))
                    elif "/" not in repo:
                        errors.append(ValidationError(
                            str(marketplace_path),
                            f"Plugin '{plugin_name}' GitHub repo format should be 'owner/repo', got: {repo}"
                        ))

                    # If plugins_dir exists locally, validate the path exists
                    if plugins_dir.exists():
                        path = source.get("path", "")
                        if path:
                            plugin_path = plugins_dir / path.split("/")[-1]
                            if not plugin_path.exists():
                                errors.append(ValidationError(
                                    str(marketplace_path),
                                    f"Plugin '{plugin_name}' local path '{path}' not found for validation",
                                    "warning"
                                ))
                            elif not (plugin_path / ".claude-plugin" / "plugin.json").exists():
                                errors.append(ValidationError(
                                    str(marketplace_path),
                                    f"Plugin '{plugin_name}' missing plugin.json in local path: {path}",
                                    "warning"
                                ))

                elif source_type == "url":
                    # URL source - validate URL format
                    url = source.get("url", "")
                    if not url:
                        errors.append(ValidationError(
                            str(marketplace_path),
                            f"Plugin '{plugin_name}' URL source missing 'url' field"
                        ))
                    else:
                        try:
                            from urllib.parse import urlparse
                            parsed = urlparse(url)
                            if not parsed.scheme or not parsed.netloc:
                                errors.append(ValidationError(
                                    str(marketplace_path),
                                    f"Plugin '{plugin_name}' invalid URL format: {url}"
                                ))
                        except:
                            errors.append(ValidationError(
                                str(marketplace_path),
                                f"Plugin '{plugin_name}' invalid URL format: {url}"
                            ))

    except (json.JSONDecodeError, KeyError):
        # JSON errors are handled elsewhere
        pass

    return errors

def validate_all(plugins_dir: Path, marketplace_path: Path) -> List[ValidationError]:
    """Run comprehensive validation on all plugins and marketplace."""
    all_errors = []

    print("🔍 Running comprehensive validation...")

    # Validate marketplace.json
    print("  Validating marketplace.json...")
    all_errors.extend(validate_marketplace_json(marketplace_path))

    # Validate plugin sources in marketplace
    print("  Validating plugin sources...")
    all_errors.extend(validate_plugin_sources(marketplace_path, plugins_dir))

    # Validate individual plugins
    if plugins_dir.exists():
        plugin_dirs = [d for d in plugins_dir.iterdir()
                      if d.is_dir() and not d.name.startswith('.')]

        print(f"  Validating {len(plugin_dirs)} plugin directories...")

        for plugin_dir in plugin_dirs:
            print(f"    Validating plugin: {plugin_dir.name}")
            all_errors.extend(validate_plugin_structure(plugin_dir))
            all_errors.extend(validate_plugin_manifest(plugin_dir))
    else:
        all_errors.append(ValidationError(
            str(plugins_dir),
            "Plugins directory does not exist"
        ))

    return all_errors

def main():
    parser = argparse.ArgumentParser(description="Validate Claude Code plugins and marketplace")
    parser.add_argument("--plugins-dir", default="plugins", help="Plugins directory path")
    parser.add_argument("--marketplace", default=".claude-plugin/marketplace.json",
                       help="Marketplace JSON file path")
    parser.add_argument("--strict", action="store_true",
                       help="Treat warnings as errors")
    parser.add_argument("--format", choices=["text", "json"], default="text",
                       help="Output format")

    args = parser.parse_args()

    plugins_dir = Path(args.plugins_dir)
    marketplace_path = Path(args.marketplace)

    errors = validate_all(plugins_dir, marketplace_path)

    if args.format == "json":
        error_data = []
        for error in errors:
            error_data.append({
                "file": error.file_path,
                "message": error.message,
                "severity": error.severity
            })
        print(json.dumps(error_data, indent=2))
    else:
        if errors:
            print("\n❌ Validation Issues Found:")
            print("=" * 50)

            # Group errors by severity
            error_count = len([e for e in errors if e.severity == "error"])
            warning_count = len([e for e in errors if e.severity == "warning"])
            info_count = len([e for e in errors if e.severity == "info"])

            # Print errors first
            for error in sorted(errors, key=lambda e: (e.severity, e.file_path)):
                severity_symbol = {
                    "error": "❌",
                    "warning": "⚠️",
                    "info": "ℹ️"
                }.get(error.severity, "❓")

                print(f"{severity_symbol} {error}")

            print("\n" + "=" * 50)
            print(f"Summary: {error_count} errors, {warning_count} warnings, {info_count} info")

            if args.strict:
                exit(1)
            elif error_count > 0:
                exit(1)
            else:
                print("⚠️  Warnings found (use --strict to treat as errors)")
        else:
            print("✅ All validations passed!")
            print("🎉 Plugins and marketplace are ready for distribution!")

    return 0

if __name__ == "__main__":
    sys.exit(main())