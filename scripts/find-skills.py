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


def validate_skill(skill_path: str) -> tuple[bool, dict]:
    """
    Validate a skill using npx claude-skills-cli validate.

    Args:
        skill_path: Full path to the skill directory

    Returns:
        Tuple of (validation_passed, validation_data)
        validation_data contains errors, warnings, and other info
    """
    try:
        # Run validation using claude-skills-cli with JSON output
        result = subprocess.run(
            ["npx", "claude-skills-cli", "validate", skill_path, "--format", "json"],
            capture_output=True,
            text=True,
            timeout=30,
        )

        if result.returncode == 0:
            return True, {}

        # Parse JSON output for failed validation
        try:
            validation_data = json.loads(result.stdout)
            return False, validation_data
        except json.JSONDecodeError:
            # Fallback if JSON parsing fails
            return False, {
                "errors": [{"message": "Failed to parse validation output"}],
                "warnings": [],
                "stdout": result.stdout,
                "stderr": result.stderr,
            }

    except subprocess.TimeoutExpired:
        return False, {"errors": [{"message": "Validation timeout"}], "warnings": []}
    except Exception as e:
        return False, {"errors": [{"message": f"Error: {e}"}], "warnings": []}


def doctor_skill(skill_path: str) -> tuple[bool, str]:
    """
    Run doctor on a skill using npx claude-skills-cli doctor.

    Args:
        skill_path: Full path to the skill directory

    Returns:
        Tuple of (success, output)
    """
    try:
        # Run doctor using claude-skills-cli
        result = subprocess.run(
            ["npx", "claude-skills-cli", "doctor", skill_path],
            capture_output=True,
            text=True,
            timeout=60,  # Doctor might take longer
        )

        return result.returncode == 0, result.stdout

    except subprocess.TimeoutExpired:
        return False, "Doctor operation timed out"
    except Exception as e:
        return False, f"Error running doctor: {e}"


def main():
    parser = argparse.ArgumentParser(
        description="Find all skill directories in plugins"
    )
    parser.add_argument(
        "--plugins-dir",
        default="./plugins",
        help="Path to plugins directory (default: ./plugins)",
    )
    parser.add_argument(
        "--validate", action="store_true", help="Run validation on each found skill"
    )
    parser.add_argument(
        "--validate-only",
        action="store_true",
        help="Only run validation, don't list skills",
    )
    parser.add_argument(
        "--doctor", action="store_true", help="Run doctor on each found skill"
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

            validation_passed, validation_data = validate_skill(skill_path)

            if validation_passed:
                print("✓ PASSED")
                validation_results.append(
                    {**skill, "validation": "passed", "validation_data": {}}
                )
            else:
                print("✗ FAILED")
                validation_results.append(
                    {
                        **skill,
                        "validation": "failed",
                        "validation_data": validation_data,
                    }
                )

        # Show summary
        passed = sum(1 for r in validation_results if r["validation"] == "passed")
        failed = len(validation_results) - passed

        print(f"\nValidation Summary:")
        print(f"  Passed: {passed}")
        print(f"  Failed: {failed}")
        print(f"  Total:  {len(validation_results)}")

        # Show detailed errors for failed skills
        if failed > 0:
            print(f"\nFailed Skills Details:")
            for result in validation_results:
                if result["validation"] == "failed":
                    print(f"\n❌ {result['plugin']}/{result['skill']}:")
                    validation_data = result.get("validation_data", {})

                    errors = validation_data.get("errors", [])
                    warnings = validation_data.get("warnings", [])

                    if errors:
                        print("  Errors:")
                        for error in errors:
                            if isinstance(error, dict):
                                print(f"    • {error.get('message', str(error))}")
                            else:
                                print(f"    • {error}")

                    if warnings:
                        print("  Warnings:")
                        for warning in warnings:
                            if isinstance(warning, dict):
                                print(f"    • {warning.get('message', str(warning))}")
                            else:
                                print(f"    • {warning}")

        if args.validate_only:
            return

    if args.doctor:
        if not skills:
            print("No skill directories found to doctor")
            return

        print(f"Running doctor on {len(skills)} skill directories...\n")

        for skill in skills:
            skill_path = skill["full_path"]
            print(f"Doctor: {skill['plugin']}/{skill['skill']}")
            print("-" * 50)

            success, output = doctor_skill(skill_path)
            print(output)

            if not success:
                print("❌ Doctor operation failed")
            else:
                print("✓ Doctor completed")

            print("\n" + "=" * 60 + "\n")
        return

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
