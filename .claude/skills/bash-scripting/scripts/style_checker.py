#!/usr/bin/env python3
"""
Bash Script Style Checker
Validates bash scripts against Google Shell Style Guide rules.
"""

import re
import sys
import argparse
from pathlib import Path

class BashStyleChecker:
    def __init__(self):
        self.errors = []
        self.warnings = []
        self.line_number = 0

    def check_file(self, file_path):
        """Check a bash file for style violations."""
        try:
            content = Path(file_path).read_text()
            lines = content.split('\n')
            self.check_content(lines, file_path)
        except Exception as e:
            print(f"Error reading file {file_path}: {e}", file=sys.stderr)
            return False

        return len(self.errors) == 0

    def check_content(self, lines, file_path="stdin"):
        """Check content line by line."""
        self.line_number = 0
        in_multiline_comment = False

        for line in lines:
            self.line_number += 1
            stripped = line.rstrip()

            # Skip empty lines and comments
            if not stripped or stripped.strip().startswith('#'):
                continue

            # Check for style violations
            self.check_line_length(stripped)
            self.check_indentation(stripped)
            self.check_quoting(stripped)
            self.check_command_substitution(stripped)
            self.check_test_statements(stripped)
            self.check_variable_format(stripped)
            self.check_function_format(stripped)

    def check_line_length(self, line):
        """Check if line exceeds 80 characters."""
        if len(line) > 80:
            self.add_error(f"Line exceeds 80 characters ({len(line)} chars)")

    def check_indentation(self, line):
        """Check for proper 2-space indentation."""
        if line.startswith(' '):
            # Count leading spaces
            spaces = len(line) - len(line.lstrip(' '))
            if spaces % 2 != 0:
                self.add_error("Use 2-space indentation (multiple of 2)")
            if '\t' in line:
                self.add_error("Use spaces instead of tabs")

    def check_quoting(self, line):
        """Check for proper variable quoting."""
        # Look for unquoted $var or ${var}
        unquoted_vars = re.findall(r'\$[a-zA-Z_][a-zA-Z0-9_]*(?![})])', line)
        unquoted_braces = re.findall(r'\$\{[^}]+\}(?!"[^"]*")', line)

        for var in unquoted_vars:
            if not self.is_safely_quoted(line, var):
                self.add_warning(f'Unquoted variable: {var} - use "${{{var[1:]}}}"')

    def check_command_substitution(self, line):
        """Check for modern $(command) instead of backticks."""
        if '`' in line and not line.strip().startswith('#'):
            self.add_error("Use $(command) instead of backticks `")

    def check_test_statements(self, line):
        """Check for [[ ]] instead of [ ] for tests."""
        if '[ ' in line and not '[[' in line:
            # Check if it's a test statement
            if any(op in line for op in ['-eq', '-ne', '-lt', '-le', '-gt', '-ge', '=']):
                self.add_warning("Use [[ ]] instead of [ ] for tests")

    def check_variable_format(self, line):
        """Check variable naming conventions."""
        # Check for uppercase variables (should be constants)
        uppercase_vars = re.findall(r'\b[A-Z][A-Z0-9_]*\b', line)
        for var in uppercase_vars:
            if var not in ['PATH', 'HOME', 'USER', 'SHELL', 'PWD', 'OLDPWD']:
                self.add_warning(f"Variable '{var}' looks like a constant - consider lowercase")

    def check_function_format(self, line):
        """Check function naming and format."""
        # Function definition
        if line.strip().startswith('function ') or '(' in line and ')' in line:
            if 'function ' in line:
                func_name = line.split('function ')[1].split('(')[0].strip()
            else:
                func_name = line.split('(')[0].strip()

            if func_name:
                # Check naming convention
                if not re.match(r'^[a-z][a-z0-9_]*$', func_name):
                    self.add_error(f"Function name '{func_name}' should use lowercase_with_underscores")

    def is_safely_quoted(self, line, var):
        """Check if variable is safely quoted in context."""
        # Simple heuristic - check if variable is in quotes
        var_pos = line.find(var)
        before = line[:var_pos]
        after = line[var_pos + len(var):]

        # Count quotes before and after
        quotes_before = before.count('"')
        quotes_after = after.count('"')

        return quotes_before % 2 == 1 and quotes_after % 2 == 1

    def add_error(self, message):
        """Add an error message."""
        self.errors.append(f"Line {self.line_number}: {message}")

    def add_warning(self, message):
        """Add a warning message."""
        self.warnings.append(f"Line {self.line_number}: {message}")

    def print_results(self):
        """Print check results."""
        if self.errors:
            print("ERRORS:")
            for error in self.errors:
                print(f"  {error}")

        if self.warnings:
            print("WARNINGS:")
            for warning in self.warnings:
                print(f"  {warning}")

        if not self.errors and not self.warnings:
            print("✅ No style issues found!")
        else:
            print(f"\nFound {len(self.errors)} errors and {len(self.warnings)} warnings")

def main():
    parser = argparse.ArgumentParser(description='Check bash script style against Google Shell Style Guide')
    parser.add_argument('file', nargs='?', help='Bash script file to check (default: stdin)')
    parser.add_argument('--fix', action='store_true', help='Automatically fix some issues')

    args = parser.parse_args()

    checker = BashStyleChecker()

    if args.file:
        success = checker.check_file(args.file)
    else:
        # Read from stdin
        content = sys.stdin.read()
        lines = content.split('\n')
        checker.check_content(lines)
        success = len(checker.errors) == 0

    checker.print_results()

    if not success:
        sys.exit(1)

if __name__ == '__main__':
    main()