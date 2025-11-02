#!/usr/bin/env python3
"""
Bats Test Template Generator

Generates bats test file templates based on script analysis and user requirements.
"""

import argparse
import os
import re
import sys
from pathlib import Path
from typing import List, Dict, Optional, Tuple

class TestTemplateGenerator:
    """Generates bats test file templates."""

    def __init__(self):
        self.script_functions = []
        self.script_options = []
        self.script_dependencies = []

    def analyze_script(self, script_path: str) -> None:
        """Analyze a bash script to extract testable components."""
        try:
            with open(script_path, 'r') as f:
                content = f.read()

            # Extract function definitions
            self.script_functions = self._extract_functions(content)

            # Extract command line options
            self.script_options = self._extract_options(content)

            # Extract dependencies
            self.script_dependencies = self._extract_dependencies(content)

        except FileNotFoundError:
            print(f"Warning: Script file not found: {script_path}")
        except Exception as e:
            print(f"Error analyzing script: {e}")

    def _extract_functions(self, content: str) -> List[str]:
        """Extract function names from bash script."""
        # Match function definitions: function_name() { or function function_name {
        patterns = [
            r'^(\w+)\(\s*\)\s*{',
            r'^function\s+(\w+)\s*{',
            r'^(\w+)\s*\(\s*\)\s*$'
        ]

        functions = []
        for line in content.split('\n'):
            line = line.strip()
            if line.startswith('#') or not line:
                continue

            for pattern in patterns:
                match = re.match(pattern, line)
                if match and not match.group(1).startswith('_'):
                    functions.append(match.group(1))
                    break

        return functions

    def _extract_options(self, content: str) -> List[Dict[str, str]]:
        """Extract command line options from bash script."""
        options = []

        # Look for case statements in argument parsing
        arg_parse_blocks = re.findall(r'while\s+\[\[?\s*\$#.*?\n\s*done', content, re.DOTALL)

        for block in arg_parse_blocks:
            # Find case statements within argument parsing
            case_matches = re.findall(r'case\s+\$1.*?esac', block, re.DOTALL)

            for case_block in case_matches:
                # Extract option patterns
                option_matches = re.findall(r'\s*(-[a-zA-Z]|--[a-zA-Z-]+)\)', case_block)
                for opt in option_matches:
                    options.append({
                        'option': opt,
                        'has_argument': '--' in opt or opt in ['-f', '-o', '-i']
                    })

        return options

    def _extract_dependencies(self, content: str) -> List[str]:
        """Extract external command dependencies from script."""
        dependencies = []

        # Look for external commands
        patterns = [
            r'\b(\w+)\s+',  # Command calls
            r'command\s+-v\s+(\w+)',  # Command checks
            r'which\s+(\w+)',  # Which checks
            r'type\s+(\w+)',  # Type checks
        ]

        for pattern in patterns:
            matches = re.findall(pattern, content)
            dependencies.extend(matches)

        # Filter out bash built-ins and common utilities
        built_ins = {
            'echo', 'printf', 'read', 'cd', 'pwd', 'ls', 'cat', 'grep', 'sed', 'awk',
            'if', 'then', 'else', 'fi', 'for', 'while', 'do', 'done', 'case', 'esac',
            'function', 'return', 'exit', 'local', 'export', 'unset', 'set', 'shift'
        }

        dependencies = list(set(dependencies) - built_ins)
        return sorted(dependencies)

    def generate_basic_template(self, script_name: str, script_path: str) -> str:
        """Generate a basic test template."""
        template = f'''#!/usr/bin/env bats

# Tests for {script_name}

setup() {{
    # Load helper libraries
    load 'test_helper/bats-support/load'
    load 'test_helper/bats-assert/load'

    # Get the directory containing this test file
    DIR="$( cd "$( dirname "$BATS_TEST_FILENAME" )" >/dev/null 2>&1 && pwd )"

    # Add src directory to PATH so scripts can be called without relative paths
    PATH="$DIR/../src:$PATH"
}}

@test "script shows help with --help" {{
    run {script_name}.sh --help
    assert_success
    assert_output --partial "Usage:"
}}

@test "script shows version with --version" {{
    run {script_name}.sh --version
    assert_success
    assert_output --regexp "[0-9]+\\.[0-9]+\\.[0-9]+"
}}

@test "script runs without arguments" {{
    run {script_name}.sh
    # Adjust expectation based on script behavior
    # assert_success  # Uncomment if script should succeed
    # assert_failure  # Uncomment if script should fail
}}

@test "script fails with unknown option" {{
    run {script_name}.sh --unknown-option
    assert_failure
    assert_output --partial "Unknown option" -- "Invalid option" -- "unrecognized"
}}
'''
        return template

    def generate_function_tests(self, script_name: str) -> str:
        """Generate test cases for script functions."""
        if not self.script_functions:
            return ""

        tests = ["\n# Function-specific tests"]
        for func in self.script_functions:
            tests.append(f'''
@test "function {func} works correctly" {{
    # TODO: Add specific test for {func} function
    # This may require sourcing the script and calling the function directly
    skip "Function testing not implemented yet"
}}''')

        return '\n'.join(tests)

    def generate_option_tests(self, script_name: str) -> str:
        """Generate test cases for command line options."""
        if not self.script_options:
            return ""

        tests = ["\n# Option-specific tests"]
        for opt_info in self.script_options:
            option = opt_info['option']
            tests.append(f'''
@test "option {option} is handled correctly" {{
    run {script_name}.sh {option}
    # TODO: Add specific assertions for {option} behavior
    skip "Option testing not implemented yet"
}}''')

        return '\n'.join(tests)

    def generate_dependency_tests(self, script_name: str) -> str:
        """Generate test cases for dependencies."""
        if not self.script_dependencies:
            return ""

        tests = ["\n# Dependency tests"]
        for dep in self.script_dependencies:
            tests.append(f'''
@test "required dependency {dep} is available" {{
    if ! command -v {dep} &> /dev/null; then
        skip "{dep} is not available"
    fi
    run {script_name}.sh --help  # Test that script can run when dependency exists
    assert_success
}}''')

        return '\n'.join(tests)

    def generate_error_case_tests(self, script_name: str) -> str:
        """Generate error case tests."""
        return f'''

# Error case tests
@test "script handles missing input gracefully" {{
    run {script_name}.sh /nonexistent/input
    # Adjust expectation based on script behavior
    assert_failure
    assert_output --partial "not found" -- "No such file" -- "cannot access"
}}

@test "script handles permission denied gracefully" {{
    # Create a file without read permissions
    test_file=$(mktemp)
    chmod 000 "$test_file"
    run {script_name}.sh "$test_file"
    assert_failure
    assert_output --partial "Permission denied" -- "cannot open"
    rm -f "$test_file"
}}

@test "script handles empty input gracefully" {{
    empty_file=$(mktemp)
    run {script_name}.sh "$empty_file"
    # Adjust expectation based on script behavior
    # assert_success  # Uncomment if script should handle empty input
    # assert_failure  # Uncomment if script should fail on empty input
    rm -f "$empty_file"
}}
'''

    def generate_integration_tests(self, script_name: str) -> str:
        """Generate integration test template."""
        return f'''

# Integration tests
@test "script integrates with standard Unix tools" {{
    # Test piping input
    echo "test input" | run {script_name}.sh
    assert_success

    # Test output redirection
    output_file=$(mktemp)
    run {script_name}.sh > "$output_file"
    assert_success
    test -s "$output_file"  # Check that output file is not empty
    rm -f "$output_file"
}}

@test "script works in different directories" {{
    original_dir=$(pwd)
    test_dir=$(mktemp -d)
    cd "$test_dir"

    run "$original_dir/src/{script_name}.sh" --help
    assert_success

    cd "$original_dir"
    rm -rf "$test_dir"
}}
'''

    def generate_complete_template(self, script_name: str, script_path: str,
                                 include_functions: bool = False,
                                 include_options: bool = False,
                                 include_dependencies: bool = False,
                                 include_errors: bool = True,
                                 include_integration: bool = False) -> str:
        """Generate a complete test template."""

        # Analyze the script first
        self.analyze_script(script_path)

        # Start with basic template
        template = self.generate_basic_template(script_name, script_path)

        # Add optional sections
        if include_functions:
            template += self.generate_function_tests(script_name)

        if include_options:
            template += self.generate_option_tests(script_name)

        if include_dependencies:
            template += self.generate_dependency_tests(script_name)

        if include_errors:
            template += self.generate_error_case_tests(script_name)

        if include_integration:
            template += self.generate_integration_tests(script_name)

        return template

def main():
    """Main function."""
    parser = argparse.ArgumentParser(
        description='Generate Bats test file templates',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  %(prog)s -s myscript.sh                    # Basic template
  %(prog)s -s myscript.sh -a                # Complete template with all sections
  %(prog)s -s myscript.sh -f -o -e          # Template with functions, options, and error cases
  %(prog)s -s myscript.sh -o my_test.bats   # Output to specific file
        '''
    )

    parser.add_argument('-s', '--script', required=True,
                       help='Path to the bash script to create tests for')
    parser.add_argument('-n', '--name',
                       help='Name for the script (defaults to script filename without extension)')
    parser.add_argument('-o', '--output',
                       help='Output test file path (default: script_name_test.bats)')
    parser.add_argument('-a', '--all', action='store_true',
                       help='Include all optional test sections')
    parser.add_argument('-f', '--functions', action='store_true',
                       help='Include function tests')
    parser.add_argument('--options', action='store_true',
                       help='Include option tests')
    parser.add_argument('-d', '--dependencies', action='store_true',
                       help='Include dependency tests')
    parser.add_argument('-e', '--errors', action='store_true', default=True,
                       help='Include error case tests (default)')
    parser.add_argument('-i', '--integration', action='store_true',
                       help='Include integration tests')
    parser.add_argument('--dry-run', action='store_true',
                       help='Show what would be generated without creating files')

    args = parser.parse_args()

    # Validate script path
    script_path = Path(args.script)
    if not script_path.exists():
        print(f"Error: Script file not found: {script_path}", file=sys.stderr)
        sys.exit(1)

    # Determine script name
    if args.name:
        script_name = args.name
    else:
        script_name = script_path.stem
        if script_name.endswith('.sh'):
            script_name = script_name[:-3]

    # Determine output file
    if args.output:
        output_file = Path(args.output)
    else:
        output_file = Path(f"{script_name}_test.bats")

    # Generate template
    generator = TestTemplateGenerator()

    # Set flags for optional sections
    include_functions = args.all or args.functions
    include_options = args.all or args.options
    include_dependencies = args.all or args.dependencies
    include_errors = args.all or args.errors
    include_integration = args.all or args.integration

    template = generator.generate_complete_template(
        script_name=script_name,
        script_path=str(script_path),
        include_functions=include_functions,
        include_options=include_options,
        include_dependencies=include_dependencies,
        include_errors=include_errors,
        include_integration=include_integration
    )

    # Output template
    if args.dry_run:
        print(f"Would generate test file: {output_file}")
        print("=" * 50)
        print(template)
    else:
        try:
            # Create output directory if it doesn't exist
            output_file.parent.mkdir(parents=True, exist_ok=True)

            with open(output_file, 'w') as f:
                f.write(template)

            # Make file executable
            os.chmod(output_file, 0o755)

            print(f"Generated test file: {output_file}")
            print(f"Script analyzed: {script_path}")

            if generator.script_functions:
                print(f"Functions found: {', '.join(generator.script_functions)}")
            if generator.script_options:
                options = [opt['option'] for opt in generator.script_options]
                print(f"Options found: {', '.join(options)}")
            if generator.script_dependencies:
                print(f"Dependencies found: {', '.join(generator.script_dependencies)}")

            print(f"\nNext steps:")
            print(f"1. Review and customize the generated test file: {output_file}")
            print(f"2. Run tests: ./test/bats/bin/bats {output_file}")
            print(f"3. Update TODO comments with specific test assertions")

        except Exception as e:
            print(f"Error writing test file: {e}", file=sys.stderr)
            sys.exit(1)

if __name__ == '__main__':
    main()