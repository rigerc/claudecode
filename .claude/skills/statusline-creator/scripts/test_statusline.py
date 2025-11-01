#!/usr/bin/env python3
"""
Test and preview statusline configurations.
Validates format, renders preview with sample data, and checks for common issues.
"""

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path


class StatuslineValidator:
    """Validate and test statusline configurations."""

    # ANSI color codes for validation
    ANSI_PATTERNS = {
        'reset': r'\x1b\[0m',
        'bold': r'\x1b\[1m',
        'color': r'\x1b\[\d+m',
        'rgb': r'\x1b\[38;2;\d+;\d+;\d+m',
    }

    def __init__(self, config_path: str = None):
        """Initialize with optional config file path."""
        self.config_path = Path(config_path) if config_path else None
        self.errors = []
        self.warnings = []

    def load_config(self) -> dict:
        """Load statusline configuration from Claude Code settings."""
        if self.config_path and self.config_path.exists():
            with open(self.config_path) as f:
                return json.load(f)

        # Try default Claude Code settings location
        default_path = Path.home() / ".claude" / "settings.json"
        if default_path.exists():
            with open(default_path) as f:
                settings = json.load(f)
                return settings.get("statusline", {})

        return {}

    def validate_format(self, statusline: str) -> bool:
        """Validate statusline format and structure."""
        if not statusline:
            self.errors.append("Statusline is empty")
            return False

        # Check for balanced ANSI codes
        if statusline.count('\x1b[') > statusline.count('m'):
            self.warnings.append("Potentially unbalanced ANSI escape codes")

        # Check length (recommended < 200 chars for readability)
        visible_length = len(re.sub(r'\x1b\[[0-9;]*m', '', statusline))
        if visible_length > 200:
            self.warnings.append(f"Statusline is very long ({visible_length} chars visible)")

        # Check for shell command substitution patterns
        if '`' in statusline or '$(' in statusline:
            self.warnings.append("Contains shell command substitution - ensure proper escaping")

        return len(self.errors) == 0

    def render_preview(self, statusline: str, sample_data: dict = None) -> str:
        """Render statusline with sample or real data."""
        if sample_data is None:
            sample_data = {
                'git_branch': 'main',
                'git_status': '✓',
                'pwd': '~/workspace/project',
                'time': '14:23:45',
                'user': 'developer',
                'host': 'machine',
                'load': '1.23',
            }

        # Replace common placeholders
        rendered = statusline
        for key, value in sample_data.items():
            rendered = rendered.replace(f'{{{key}}}', str(value))
            rendered = rendered.replace(f'${{{key}}}', str(value))

        return rendered

    def test_with_scripts(self, skill_dir: Path) -> dict:
        """Test statusline with actual script data."""
        scripts_dir = skill_dir / "scripts"
        data = {}

        # Test git info script
        git_script = scripts_dir / "get_git_info.sh"
        if git_script.exists():
            try:
                result = subprocess.run(
                    ["bash", str(git_script), "--format", "statusline"],
                    capture_output=True,
                    text=True,
                    timeout=5
                )
                if result.returncode == 0:
                    data['git_info'] = result.stdout.strip()
            except Exception as e:
                self.warnings.append(f"Could not run git info script: {e}")

        # Test system info script
        sys_script = scripts_dir / "get_system_info.sh"
        if sys_script.exists():
            try:
                result = subprocess.run(
                    ["bash", str(sys_script), "--format", "statusline"],
                    capture_output=True,
                    text=True,
                    timeout=5
                )
                if result.returncode == 0:
                    data['sys_info'] = result.stdout.strip()
            except Exception as e:
                self.warnings.append(f"Could not run system info script: {e}")

        return data

    def report(self) -> str:
        """Generate validation report."""
        lines = []

        if self.errors:
            lines.append("❌ ERRORS:")
            for error in self.errors:
                lines.append(f"  • {error}")

        if self.warnings:
            lines.append("⚠️  WARNINGS:")
            for warning in self.warnings:
                lines.append(f"  • {warning}")

        if not self.errors and not self.warnings:
            lines.append("✅ No issues found")

        return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Test and preview statusline configurations"
    )
    parser.add_argument(
        "statusline",
        nargs="?",
        help="Statusline string to test (or use --config)"
    )
    parser.add_argument(
        "--config",
        help="Path to settings.json file"
    )
    parser.add_argument(
        "--skill-dir",
        help="Path to statusline-creator skill directory"
    )
    parser.add_argument(
        "--preview",
        action="store_true",
        help="Show preview with sample data"
    )
    parser.add_argument(
        "--live",
        action="store_true",
        help="Show preview with live script data"
    )

    args = parser.parse_args()

    validator = StatuslineValidator(args.config)

    # Get statusline to test
    statusline = args.statusline
    if not statusline and args.config:
        config = validator.load_config()
        statusline = config.get("format", "")

    if not statusline:
        print("Error: No statusline provided", file=sys.stderr)
        parser.print_help()
        sys.exit(1)

    # Validate
    print("🔍 Validating statusline...\n")
    is_valid = validator.validate_format(statusline)

    # Show preview
    if args.preview or args.live:
        print("👁️  Preview:\n")
        if args.live and args.skill_dir:
            skill_path = Path(args.skill_dir)
            data = validator.test_with_scripts(skill_path)
            if data:
                # Create sample data with live values
                sample = {
                    'git_branch': data.get('git_info', 'main'),
                    'pwd': subprocess.run(
                        ["pwd"], capture_output=True, text=True
                    ).stdout.strip().replace(str(Path.home()), '~'),
                    'time': subprocess.run(
                        ["date", "+%H:%M:%S"], capture_output=True, text=True
                    ).stdout.strip(),
                }
                preview = validator.render_preview(statusline, sample)
            else:
                preview = validator.render_preview(statusline)
        else:
            preview = validator.render_preview(statusline)

        print(f"  {preview}")
        print()

    # Show report
    print(validator.report())

    sys.exit(0 if is_valid else 1)


if __name__ == "__main__":
    main()
