#!/usr/bin/env python3
"""
Find all skill directories in the plugins directory.

Skill directories are defined as directories in any plugin's skills/
subdirectory that contain a SKILL.md file.
"""

import os
import json
import argparse
import subprocess
import sys
from pathlib import Path
from typing import List, Dict, Any


def find_skill_directories(plugins_dir: str = "./plugins") -> List[Dict[str, Any]]:
    """
    Find all skill directories in the plugins directory.

    Args:
        plugins_dir: Path to the plugins directory

    Returns:
        List of dictionaries containing skill information
    """
    plugins_path = Path(plugins_dir)
    skills = []

    if not plugins_path.exists():
        print(f"Error: Plugins directory '{plugins_dir}' not found")
        return skills

    # Iterate through all plugin directories
    for plugin_dir in plugins_path.iterdir():
        if not plugin_dir.is_dir():
            continue

        # Look for skills subdirectory
        skills_dir = plugin_dir / "skills"
        if not skills_dir.exists() or not skills_dir.is_dir():
            continue

        # Find all directories in skills/ that contain SKILL.md
        for skill_dir in skills_dir.iterdir():
            if not skill_dir.is_dir():
                continue

            skill_md = skill_dir / "SKILL.md"
            if skill_md.exists() and skill_md.is_file():
                # Get relative path from project root
                try:
                    rel_path = str(skill_dir.relative_to(Path.cwd()))
                except ValueError:
                    # Fallback to relative path from plugins directory
                    rel_path = str(skill_dir.relative_to(plugins_path.parent))

                skill_info = {
                    "plugin": plugin_dir.name,
                    "skill": skill_dir.name,
                    "path": rel_path,
                    "full_path": str(skill_dir.absolute()),
                    "skill_md": str(skill_md.absolute()),
                }

                skills.append(skill_info)

    return skills


def validate_skill(skill_path: str) -> bool:
    """
    Validate a skill using npx claude-skills-cli validate.

    Args:
        skill_path: Full path to the skill directory

    Returns:
        True if validation passed, False otherwise
    """
    try:
        # Run validation using claude-skills-cli
        result = subprocess.run(
            ["npx", "claude-skills-cli", "validate", skill_path, "--strict"],
            capture_output=True,
            text=True,
            timeout=30,
        )

        return result.returncode == 0

    except subprocess.TimeoutExpired:
        print(f"Validation timeout for {skill_path}")
        return False
    except Exception as e:
        print(f"Error validating {skill_path}: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(
        description="Find all skill directories in plugins"
    )
    parser.add_argument(
        "--plugins-dir",
        default="./plugins",
        help="Path to plugins directory (default: ./plugins)",
    )
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    parser.add_argument(
        "--count", action="store_true", help="Only show the count of skills found"
    )
    parser.add_argument(
        "--validate", action="store_true", help="Run validation on each found skill"
    )
    parser.add_argument(
        "--validate-only",
        action="store_true",
        help="Only run validation, don't list skills",
    )

    args = parser.parse_args()

    skills = find_skill_directories(args.plugins_dir)

    if args.validate or args.validate_only:
        if not skills:
            print("No skill directories found to validate")
            return

        print(f"Validating {len(skills)} skill directories...\n")

        validation_results = []
        for skill in skills:
            skill_path = skill["full_path"]
            print(f"Validating: {skill['plugin']}/{skill['skill']}", end=" ... ")

            if validate_skill(skill_path):
                print("✓ PASSED")
                validation_results.append({**skill, "validation": "passed"})
            else:
                print("✗ FAILED")
                validation_results.append({**skill, "validation": "failed"})

        # Show summary
        passed = sum(1 for r in validation_results if r["validation"] == "passed")
        failed = len(validation_results) - passed

        print(f"\nValidation Summary:")
        print(f"  Passed: {passed}")
        print(f"  Failed: {failed}")
        print(f"  Total:  {len(validation_results)}")

        if args.validate_only:
            return

    if args.count:
        print(len(skills))
        return

    if args.json:
        if args.validate:
            # Include validation results in JSON output
            validation_results = []  # Initialize in case validation wasn't run
            print(json.dumps(validation_results, indent=2))
        else:
            print(json.dumps(skills, indent=2))
    else:
        if not skills:
            print("No skill directories found")
            return

        print(f"Found {len(skills)} skill directories:\n")
        for skill in skills:
            print(f"Plugin: {skill['plugin']}")
            print(f"  Skill: {skill['skill']}")
            print(f"  Path: {skill['path']}")
            print()


if __name__ == "__main__":
    main()
