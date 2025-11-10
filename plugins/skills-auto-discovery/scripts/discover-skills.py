#!/usr/bin/env python3
"""
Skills Auto-Discovery Script

Discovers all available skills from personal, project, and plugin sources
and injects them into session context via SessionStart hook.
"""

import json
import os
import sys
import time
from pathlib import Path
from typing import Dict, List, Any, Optional
import argparse

try:
    import yaml

    HAS_YAML = True
except ImportError:
    HAS_YAML = False


class SkillsDiscovery:
    def __init__(self):
        self.cache_dir = Path.home() / ".claude" / "cache"
        self.cache_file = self.cache_dir / "skills-discovery.json"
        self.cache_dir.mkdir(exist_ok=True)

    def discover_all_skills(self) -> Dict[str, Any]:
        """Discover skills from all sources."""
        skills = {
            "personal": self.scan_directory(Path.home() / ".claude" / "skills"),
            "project": self.scan_directory(Path(".claude") / "skills"),
            "plugins": self.scan_plugin_skills(),
        }

        # Remove empty categories
        skills = {k: v for k, v in skills.items() if v}

        return {
            "skills": skills,
            "total_count": sum(len(category) for category in skills.values()),
            "categories": list(skills.keys()),
        }

    def scan_directory(self, path: Path) -> List[Dict[str, Any]]:
        """Scan a directory for SKILL.md files and extract metadata."""
        if not path.exists():
            return []

        skills = []
        for skill_dir in path.iterdir():
            if not skill_dir.is_dir():
                continue

            skill_file = skill_dir / "SKILL.md"
            if skill_file.exists():
                skill_info = self.extract_skill_metadata(skill_file, skill_dir.name)
                if skill_info:
                    skills.append(skill_info)

        return sorted(skills, key=lambda x: x["name"])

    def scan_plugin_skills(self) -> Dict[str, List[Dict[str, Any]]]:
        """Scan installed plugins for skills."""
        installed_plugins_file = (
            Path.home() / ".claude" / "plugins" / "installed_plugins.json"
        )
        if not installed_plugins_file.exists():
            return {}

        try:
            with open(installed_plugins_file, "r") as f:
                installed_data = json.load(f)
        except (json.JSONDecodeError, IOError):
            return {}

        plugin_skills = {}
        plugins = installed_data.get("plugins", {})

        for plugin_key, plugin_info in plugins.items():
            install_path = Path(plugin_info.get("installPath", ""))
            if not install_path.exists():
                continue

            skills_dir = install_path / "skills"
            if not skills_dir.exists():
                continue

            skills = []
            for skill_dir in skills_dir.iterdir():
                if not skill_dir.is_dir():
                    continue

                skill_file = skill_dir / "SKILL.md"
                if skill_file.exists():
                    skill_info = self.extract_skill_metadata(skill_file, skill_dir.name)
                    if skill_info:
                        skills.append(skill_info)

            if skills:
                plugin_name = self.get_plugin_name(install_path)
                plugin_skills[plugin_name] = sorted(skills, key=lambda x: x["name"])

        return plugin_skills

    def get_plugin_name(self, plugin_dir: Path) -> str:
        """Get plugin name from plugin.json or directory name."""
        plugin_json = plugin_dir / ".claude-plugin" / "plugin.json"
        if plugin_json.exists():
            try:
                with open(plugin_json, "r") as f:
                    data = json.load(f)
                    return data.get("name", plugin_dir.name)
            except (json.JSONDecodeError, IOError):
                pass
        return plugin_dir.name

    def extract_skill_metadata(
        self, skill_file: Path, skill_name: str
    ) -> Optional[Dict[str, Any]]:
        """Extract metadata from SKILL.md file."""
        try:
            with open(skill_file, "r", encoding="utf-8") as f:
                content = f.read()

            # Extract YAML frontmatter
            if content.startswith("---") and HAS_YAML:
                try:
                    end_index = content.find("---", 3)
                    if end_index != -1:
                        frontmatter = content[3:end_index].strip()
                        metadata = yaml.safe_load(frontmatter)  # type: ignore

                        return {
                            "name": metadata.get("name", skill_name),
                            "description": metadata.get(
                                "description", "No description available"
                            ),
                            "allowed_tools": metadata.get("allowed-tools", []),
                            "source": str(skill_file.parent),
                            "skill_name": skill_name,
                        }
                except Exception:
                    pass

            # Fallback: use basic info
            return {
                "name": skill_name,
                "description": "No description available",
                "allowed_tools": [],
                "source": str(skill_file.parent),
                "skill_name": skill_name,
            }

        except (IOError, UnicodeDecodeError):
            return None

    def format_skills_overview(self, skills_data: Dict[str, Any]) -> str:
        """Format skills data into markdown overview."""
        output = ["## 🎯 Available Skills (Auto-Discovered)\n"]

        skills = skills_data["skills"]
        total_count = skills_data["total_count"]

        if not skills:
            output.append("No skills found. Skills will appear here once installed.")
            return "\n".join(output)

        # Personal Skills
        if "personal" in skills and skills["personal"]:
            output.append("### 📁 Personal Skills")
            for skill in skills["personal"]:
                output.append(f"- **{skill['name']}**: {skill['description']}")
                if skill["allowed_tools"]:
                    tools = ", ".join(skill["allowed_tools"])
                    output.append(f"  *Tools: {tools}*")
            output.append("")

        # Project Skills
        if "project" in skills and skills["project"]:
            output.append("### 📂 Project Skills")
            for skill in skills["project"]:
                output.append(f"- **{skill['name']}**: {skill['description']}")
                if skill["allowed_tools"]:
                    tools = ", ".join(skill["allowed_tools"])
                    output.append(f"  *Tools: {tools}*")
            output.append("")

        # Plugin Skills
        if "plugins" in skills and skills["plugins"]:
            output.append("### 🔌 Plugin Skills")
            for plugin_name, plugin_skills in skills["plugins"].items():
                output.append(f"#### {plugin_name}")
                for skill in plugin_skills:
                    output.append(f"- **{skill['name']}**: {skill['description']}")
                    if skill["allowed_tools"]:
                        tools = ", ".join(skill["allowed_tools"])
                        output.append(f"  *Tools: {tools}*")
                output.append("")

        # Summary
        categories = ", ".join(skills_data["categories"])
        output.append("---")
        output.append(f"*Found {total_count} skills across {categories} sources.*")
        output.append(
            "*Skills are model-invoked based on your requests and descriptions.*"
        )

        return "\n".join(output)

    def is_cache_valid(self) -> bool:
        """Check if cache is still valid."""
        if not self.cache_file.exists():
            return False

        try:
            with open(self.cache_file, "r") as f:
                cache_data = json.load(f)

            cache_time = cache_data.get("timestamp", 0)

            # Check if any skill directories are newer than cache
            sources_to_check = [
                Path.home() / ".claude" / "skills",
                Path(".claude") / "skills",
                Path.home() / ".claude" / "plugins",
            ]

            for source in sources_to_check:
                if source.exists():
                    for item in source.rglob("SKILL.md"):
                        if item.stat().st_mtime > cache_time:
                            return False

            return True

        except (json.JSONDecodeError, IOError):
            return False

    def load_from_cache(self) -> str:
        """Load skills overview from cache."""
        try:
            with open(self.cache_file, "r") as f:
                cache_data = json.load(f)
            return cache_data.get("overview", "")
        except (json.JSONDecodeError, IOError):
            return ""

    def save_to_cache(self, overview: str):
        """Save skills overview to cache."""
        try:
            cache_data = {"timestamp": time.time(), "overview": overview}
            with open(self.cache_file, "w") as f:
                json.dump(cache_data, f)
        except IOError:
            pass  # Cache save failure is not critical

    def discover_and_format(self, force_refresh: bool = False) -> str:
        """Main discovery method with caching."""
        if not force_refresh and self.is_cache_valid():
            return self.load_from_cache()

        skills_data = self.discover_all_skills()
        overview = self.format_skills_overview(skills_data)
        self.save_to_cache(overview)

        return overview


def main():
    parser = argparse.ArgumentParser(description="Discover Claude Code skills")
    parser.add_argument(
        "--force-refresh", action="store_true", help="Force refresh of skills cache"
    )
    parser.add_argument(
        "--test", action="store_true", help="Test discovery and output to stdout"
    )

    args = parser.parse_args()

    # Read hook input (not used for this script but required for hook compatibility)
    try:
        input_data = json.load(sys.stdin)
    except json.JSONDecodeError:
        input_data = {}

    discovery = SkillsDiscovery()
    overview = discovery.discover_and_format(force_refresh=args.force_refresh)

    if args.test:
        print(overview)
        sys.exit(0)

    # Output as JSON for hook
    output = {
        "systemMessage": f"The following skills have been auto-discovered and are available for use: {overview}",
        "hookSpecificOutput": {
            "hookEventName": "SessionStart",
            "additionalContext": overview,
        },
    }

    print(json.dumps(output))
    sys.exit(0)


if __name__ == "__main__":
    main()
