#!/usr/bin/env python3
"""
Chezmoi Template Validator

A Python script to validate Chezmoi template syntax and check for common issues.
This script helps identify template problems before applying changes.
"""

import sys
import os
import re
import argparse
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple
import json
import yaml

try:
    from textwrap import dedent
except ImportError:
    def dedent(text):
        """Fallback dedent function"""
        lines = text.splitlines()
        if not lines:
            return text
        # Find minimum indentation
        min_indent = min(len(line) - len(line.lstrip()) for line in lines if line.strip())
        if min_indent == 0:
            return text
        return '\n'.join(line[min_indent:] if line.strip() else '' for line in lines)

class TemplateValidator:
    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self.errors = []
        self.warnings = []

    def log_error(self, message: str, line_num: Optional[int] = None):
        """Log an error"""
        if line_num:
            message = f"Line {line_num}: {message}"
        self.errors.append(message)

    def log_warning(self, message: str, line_num: Optional[int] = None):
        """Log a warning"""
        if line_num:
            message = f"Line {line_num}: {message}"
        self.warnings.append(message)

    def log_info(self, message: str):
        """Log info if verbose mode is enabled"""
        if self.verbose:
            print(f"[INFO] {message}")

    def validate_template_file(self, file_path: Path) -> bool:
        """Validate a single template file"""
        self.log_info(f"Validating {file_path}")

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            self.log_error(f"Could not read file: {e}")
            return False

        return self.validate_template_content(content, file_path)

    def validate_template_content(self, content: str, file_path: Optional[Path] = None) -> bool:
        """Validate template content"""
        lines = content.split('\n')
        is_valid = True

        # Check for basic Go template syntax
        stack = []
        in_template = False
        template_start_line = None

        for line_num, line in enumerate(lines, 1):
            # Find template delimiters
            for match in re.finditer(r'{{[^}]*}}', line):
                template_content = match.group()[2:-2].strip()

                # Check for unclosed template
                if not template_content.endswith('}}'):
                    self.log_error(f"Unclosed template: {match.group()}", line_num)
                    is_valid = False

                # Check for common syntax errors
                if template_content.startswith('end ') and not stack:
                    self.log_error(f"Unexpected {{% end %}} - no matching block", line_num)
                    is_valid = False
                elif template_content.startswith(('if ', 'range ', 'with ')) and not template_content.endswith(' end'):
                    stack.append((template_content.split()[0], line_num))
                elif template_content.startswith('end ') and stack:
                    stack.pop()
                elif template_content == 'else' and not stack:
                    self.log_error(f"Unexpected {{% else %}} - no matching if block", line_num)
                    is_valid = False

            # Check for template directives
            if 'chezmoi:template:' in line:
                self.validate_template_directive(line, line_num)

        # Check for unclosed blocks
        if stack:
            for block_type, start_line in stack:
                self.log_error(f"Unclosed {block_type} block starting at line {start_line}")
                is_valid = False

        # Check for common issues
        self.check_common_issues(content, lines)

        return is_valid

    def validate_template_directive(self, line: str, line_num: int):
        """Validate chezmoi template directive"""
        try:
            # Parse directive
            directive_match = re.search(r'chezmoi:template:([^:]*)', line)
            if directive_match:
                options = directive_match.group(1)
                self.log_info(f"Found template directive: {options}")

                # Check for known options
                known_options = ['left-delimiter', 'right-delimiter']
                for option in known_options:
                    if option in options:
                        self.log_info(f"  - {option}: found")
        except Exception as e:
            self.log_warning(f"Could not parse template directive: {e}", line_num)

    def check_common_issues(self, content: str, lines: List[str]):
        """Check for common template issues"""
        # Check for undefined variables (common ones)
        defined_vars = set()
        used_vars = set()

        # Extract defined and used variables
        for line_num, line in enumerate(lines, 1):
            # Variable assignments
            assign_matches = re.findall(r'{{\s*\$([a-zA-Z_][a-zA-Z0-9_]*)\s*:=', line)
            for var in assign_matches:
                defined_vars.add(var)

            # Variable usage
            usage_matches = re.findall(r'{{\s*\.?([a-zA-Z_][a-zA-Z0-9_.]*)\s*}}', line)
            for var in usage_matches:
                # Skip function calls and known variables
                if '.' in var and not var.startswith('.chezmoi'):
                    continue
                if var in ['chezmoi', 'true', 'false', 'nil']:
                    continue
                used_vars.add(var)

        # Check for variables used but not defined
        for var in used_vars:
            if var not in defined_vars and not var.startswith('chezmoi'):
                self.log_warning(f"Variable '{var}' may not be defined in data file")

    def validate_data_file(self, file_path: Path) -> bool:
        """Validate a data file (YAML or JSON)"""
        self.log_info(f"Validating data file {file_path}")

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                if file_path.suffix.lower() in ['.yaml', '.yml']:
                    yaml.safe_load(f)
                elif file_path.suffix.lower() == '.json':
                    json.load(f)
                else:
                    self.log_warning(f"Unknown data file format: {file_path.suffix}")
                    return False

            self.log_info(f"Data file {file_path} is valid")
            return True
        except yaml.YAMLError as e:
            self.log_error(f"YAML syntax error in {file_path}: {e}")
            return False
        except json.JSONDecodeError as e:
            self.log_error(f"JSON syntax error in {file_path}: {e}")
            return False
        except Exception as e:
            self.log_error(f"Error reading data file {file_path}: {e}")
            return False

    def validate_chezmoi_config(self, file_path: Path) -> bool:
        """Validate chezmoi configuration file"""
        self.log_info(f"Validating chezmoi config {file_path}")

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Parse based on file extension
            if file_path.suffix.lower() == '.toml':
                # Basic TOML validation (simple check)
                if content.strip() and not content.strip().startswith('#'):
                    self.log_info("TOML config file found (basic validation only)")
            elif file_path.suffix.lower() in ['.yaml', '.yml']:
                yaml.safe_load(content)
            elif file_path.suffix.lower() == '.json':
                json.loads(content)

            # Check for common configuration issues
            if 'encryption' in content.lower():
                self.log_info("Encryption configuration found")

            if 'password' in content.lower() or 'key' in content.lower():
                self.log_warning("Configuration may contain sensitive information")

            return True
        except Exception as e:
            self.log_error(f"Error validating config file {file_path}: {e}")
            return False

    def find_template_files(self, directory: Path) -> List[Path]:
        """Find all template files in directory"""
        template_files = []

        for file_path in directory.rglob('*'):
            if file_path.is_file():
                # Check if it's a template file
                if (file_path.name.endswith('.tmpl') or
                    'template' in file_path.name.lower() or
                    file_path.name.startswith('dot_') or
                    file_path.name.startswith('executable_') or
                    file_path.name.startswith('private_') or
                    file_path.name.startswith('encrypted_')):
                    template_files.append(file_path)

        return template_files

    def find_data_files(self, directory: Path) -> List[Path]:
        """Find all data files in directory"""
        data_files = []

        for file_path in directory.rglob('*'):
            if file_path.is_file() and file_path.name in ['.chezmoidata.yaml', '.chezmoidata.yml', '.chezmoidata.json']:
                data_files.append(file_path)

        return data_files

    def find_config_files(self, directory: Path) -> List[Path]:
        """Find all configuration files"""
        config_files = []
        config_dir = Path.home() / '.config' / 'chezmoi'

        # Check both the source directory and config directory
        for search_dir in [directory, config_dir]:
            if search_dir.exists():
                for file_path in search_dir.rglob('*'):
                    if file_path.is_file() and file_path.name.startswith('chezmoi.'):
                        config_files.append(file_path)

        return config_files

    def validate_directory(self, directory: Path) -> bool:
        """Validate all chezmoi files in directory"""
        if not directory.exists():
            self.log_error(f"Directory does not exist: {directory}")
            return False

        self.log_info(f"Validating chezmoi files in {directory}")

        all_valid = True

        # Find and validate template files
        template_files = self.find_template_files(directory)
        if template_files:
            self.log_info(f"Found {len(template_files)} template files")
            for file_path in template_files:
                if not self.validate_template_file(file_path):
                    all_valid = False
        else:
            self.log_warning("No template files found")

        # Find and validate data files
        data_files = self.find_data_files(directory)
        for file_path in data_files:
            if not self.validate_data_file(file_path):
                all_valid = False

        # Find and validate config files
        config_files = self.find_config_files(directory)
        for file_path in config_files:
            if not self.validate_chezmoi_config(file_path):
                all_valid = False

        return all_valid

    def print_results(self):
        """Print validation results"""
        print("\n" + "="*50)
        print("CHEZMOI TEMPLATE VALIDATION RESULTS")
        print("="*50)

        if self.errors:
            print(f"\n{len(self.errors)} ERROR(S) FOUND:")
            for error in self.errors:
                print(f"  ❌ {error}")

        if self.warnings:
            print(f"\n{len(self.warnings)} WARNING(S) FOUND:")
            for warning in self.warnings:
                print(f"  ⚠️  {warning}")

        if not self.errors and not self.warnings:
            print("\n✅ All files passed validation!")

        print(f"\nSUMMARY:")
        print(f"  Errors: {len(self.errors)}")
        print(f"  Warnings: {len(self.warnings)}")

        if self.errors:
            print(f"  Status: FAILED")
            return False
        else:
            print(f"  Status: PASSED")
            return True


def main():
    parser = argparse.ArgumentParser(
        description="Validate Chezmoi template files",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s                           # Validate default chezmoi source directory
  %(prog)s /path/to/dotfiles         # Validate specific directory
  %(prog)s --file template.tmpl      # Validate specific file
  %(prog)s --verbose                 # Show detailed output
        """
    )

    parser.add_argument(
        'path',
        nargs='?',
        default=Path.home() / '.local' / 'share' / 'chezmoi',
        help='Path to chezmoi source directory or file to validate'
    )

    parser.add_argument(
        '--file', '-f',
        action='store_true',
        help='Validate single file instead of directory'
    )

    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Show verbose output'
    )

    parser.add_argument(
        '--version',
        action='version',
        version='Chezmoi Template Validator 1.0.0'
    )

    args = parser.parse_args()

    # Create validator
    validator = TemplateValidator(verbose=args.verbose)

    # Validate
    target_path = Path(args.path)

    if args.file:
        # Validate single file
        if not target_path.exists():
            print(f"Error: File not found: {target_path}")
            sys.exit(1)

        if target_path.name.endswith(('.tmpl', '.yaml', '.yml', '.json', '.toml')):
            if target_path.name.endswith('.tmpl'):
                success = validator.validate_template_file(target_path)
            elif target_path.name.startswith('chezmoi.'):
                success = validator.validate_chezmoi_config(target_path)
            else:
                success = validator.validate_data_file(target_path)
        else:
            print(f"Error: Unsupported file type: {target_path}")
            sys.exit(1)
    else:
        # Validate directory
        success = validator.validate_directory(target_path)

    # Print results
    success = validator.print_results()

    # Exit with appropriate code
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()