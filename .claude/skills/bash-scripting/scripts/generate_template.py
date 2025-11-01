#!/usr/bin/env python3
"""
Bash Script Template Generator
Generates bash script templates following Google Shell Style Guide.
"""

import sys
import argparse
from pathlib import Path

class BashTemplateGenerator:
    def __init__(self):
        self.templates = {
            'basic': self.basic_template,
            'function': self.function_template,
            'utility': self.utility_template,
            'main': self.main_script_template
        }

    def generate(self, script_type, name, description=""):
        """Generate a bash script template."""
        if script_type not in self.templates:
            print(f"Error: Unknown template type '{script_type}'", file=sys.stderr)
            print(f"Available types: {', '.join(self.templates.keys())}", file=sys.stderr)
            return None

        template_func = self.templates[script_type]
        return template_func(name, description)

    def basic_template(self, name, description):
        """Generate basic bash script template."""
        return f'''#!/bin/bash
# {name}
# {description or "Basic bash script template"}
# Follows Google Shell Style Guide

set -euo pipefail  # Exit on error, undefined vars, pipe failures

# Constants
readonly SCRIPT_DIR="$(cd "$(dirname "${{BASH_SOURCE[0]}}")" && pwd)"
readonly SCRIPT_NAME="$(basename "${{BASH_SOURCE[0]}}")"

# Functions
main() {{
  echo "Hello from {{name}}"
  # Add your logic here
}}

# Run main function if script is executed directly
if [[ "${{BASH_SOURCE[0]}}" == "${{0}}" ]]; then
  main "$@"
fi
'''.replace('{{name}}', name)

    def function_template(self, name, description):
        """Generate function library template."""
        return f'''#!/bin/bash
# {name}
# {description or "Function library template"}
# Follows Google Shell Style Guide

# Source this file to use functions: source {name}.sh

# Constants
readonly LIB_VERSION="1.0.0"

# Functions
{{name}}_function() {{
  local arg1="${{1:-}}"
  local arg2="${{2:-}}"

  if [[ -z "${{arg1}}" ]]; then
    echo "Error: Missing required argument" >&2
    return 1
  fi

  echo "Function called with: ${{arg1}} ${{arg2}}"
}}

{{name}}_validate_input() {{
  local input="${{1:-}}"

  # Validate input format
  if [[ ! "${{input}}" =~ ^[a-zA-Z0-9_]+$ ]]; then
    echo "Error: Invalid input format" >&2
    return 1
  fi

  return 0
}}

# Export functions if sourced
if [[ "${{BASH_SOURCE[0]}}" != "${{0}}" ]]; then
  export -f {{name}}_function
  export -f {{name}}_validate_input
fi
'''.replace('{{name}}', name.replace('-', '_'))

    def utility_template(self, name, description):
        """Generate utility script template."""
        return f'''#!/bin/bash
# {name}
# {description or "Utility script template"}
# Follows Google Shell Style Guide

set -euo pipefail

# Constants
readonly SCRIPT_DIR="$(cd "$(dirname "${{BASH_SOURCE[0]}}")" && pwd)"
readonly LOG_FILE="/tmp/{{name}}.log"

# Utility functions
log_info() {{
  local message="${{1:-}}"
  echo "[INFO] $(date '+%Y-%m-%d %H:%M:%S') - ${{message}}" | tee -a "${{LOG_FILE}}"
}}

log_error() {{
  local message="${{1:-}}"
  echo "[ERROR] $(date '+%Y-%m-%d %H:%M:%S') - ${{message}}" >&2 | tee -a "${{LOG_FILE}}"
}}

show_usage() {{
  cat << EOF
Usage: ${{SCRIPT_NAME}} [OPTIONS] <arguments>

{{name}} - {description}

Options:
  -h, --help     Show this help message
  -v, --verbose  Enable verbose output
  -q, --quiet    Suppress non-error output

Examples:
  ${{SCRIPT_NAME}} --verbose input.txt
  ${{SCRIPT_NAME}} -q output.txt

EOF
}}

parse_arguments() {{
  while [[ $# -gt 0 ]]; do
    case $1 in
      -h|--help)
        show_usage
        exit 0
        ;;
      -v|--verbose)
        set -x
        shift
        ;;
      -q|--quiet)
        exec 1>/dev/null
        shift
        ;;
      *)
        log_error "Unknown option: $1"
        show_usage
        exit 1
        ;;
    esac
  done
}}

# Main logic
main() {{
  parse_arguments "$@"

  log_info "Starting {{name}}"

  # Add your utility logic here

  log_info "Completed successfully"
}}

# Execute main if script is run directly
if [[ "${{BASH_SOURCE[0]}}" == "${{0}}" ]]; then
  main "$@"
fi
'''.replace('{{name}}', name)

    def main_script_template(self, name, description):
        """Generate main executable script template."""
        return f'''#!/bin/bash
# {name}
# {description or "Main script template"}
# Follows Google Shell Style Guide

set -euo pipefail

# Script metadata
readonly SCRIPT_DIR="$(cd "$(dirname "${{BASH_SOURCE[0]}}")" && pwd)"
readonly SCRIPT_NAME="$(basename "${{BASH_SOURCE[0]}}")"
readonly VERSION="1.0.0"

# Default values
VERBOSE=false
DRY_RUN=false
OUTPUT_DIR="output"

# Color codes for output
readonly RED='\\033[0;31m'
readonly GREEN='\\033[0;32m'
readonly YELLOW='\\033[1;33m'
readonly NC='\\033[0m' # No Color

# Logging functions
print_info() {{
  local message="${{1:-}}"
  echo -e "${{GREEN}}[INFO]${{NC}} ${{message}}"
}}

print_warn() {{
  local message="${{1:-}}"
  echo -e "${{YELLOW}}[WARN]${{NC}} ${{message}}" >&2
}}

print_error() {{
  local message="${{1:-}}"
  echo -e "${{RED}}[ERROR]${{NC}} ${{message}}" >&2
}}

print_verbose() {{
  local message="${{1:-}}"
  if [[ "${{VERBOSE}}" == "true" ]]; then
    echo "[VERBOSE] ${{message}}"
  fi
}}

# Usage information
show_usage() {{
  cat << EOF
{{name}} v{{VERSION}}

{description}

USAGE:
    ${{SCRIPT_NAME}} [OPTIONS] <input>

OPTIONS:
    -h, --help          Show this help message
    -v, --verbose       Enable verbose output
    -n, --dry-run       Show what would be done without executing
    -o, --output DIR    Output directory (default: ${{OUTPUT_DIR}})
    --version           Show version information

EXAMPLES:
    ${{SCRIPT_NAME}} input.txt
    ${{SCRIPT_NAME}} --verbose --output ./results input.txt
    ${{SCRIPT_NAME}} --dry-run input.txt

EOF
}}

# Argument validation
validate_arguments() {{
  local input_file="${{1:-}}"

  if [[ -z "${{input_file}}" ]]; then
    print_error "Input file is required"
    show_usage
    exit 1
  fi

  if [[ ! -f "${{input_file}}" ]]; then
    print_error "Input file does not exist: ${{input_file}}"
    exit 1
  fi

  if [[ ! -r "${{input_file}}" ]]; then
    print_error "Cannot read input file: ${{input_file}}"
    exit 1
  fi
}}

# Core functionality
process_file() {{
  local input_file="${{1:-}}"
  local output_file="${{2:-}}"

  print_verbose "Processing file: ${{input_file}}"

  if [[ "${{DRY_RUN}}" == "true" ]]; then
    print_info "DRY RUN: Would process ${{input_file}} -> ${{output_file}}"
    return 0
  fi

  # Create output directory if needed
  mkdir -p "${{OUTPUT_DIR}}"

  # Add your processing logic here
  cp "${{input_file}}" "${{output_file}}"

  print_info "Processed: ${{input_file}} -> ${{output_file}}"
}}

# Parse command line arguments
parse_arguments() {{
  while [[ $# -gt 0 ]]; do
    case $1 in
      -h|--help)
        show_usage
        exit 0
        ;;
      -v|--verbose)
        VERBOSE=true
        shift
        ;;
      -n|--dry-run)
        DRY_RUN=true
        shift
        ;;
      -o|--output)
        OUTPUT_DIR="${{2:-}}"
        shift 2
        ;;
      --version)
        echo "${{SCRIPT_NAME}} version ${{VERSION}}"
        exit 0
        ;;
      -*)
        print_error "Unknown option: $1"
        show_usage
        exit 1
        ;;
      *)
        # Assume remaining arguments are input files
        break
        ;;
    esac
  done

  # Validate remaining arguments
  validate_arguments "$@"
}

# Main execution
main() {{
  local input_file="${{1:-}}"

  parse_arguments "$@"

  print_info "Starting {{name}}"
  print_verbose "Script directory: ${{SCRIPT_DIR}}"
  print_verbose "Output directory: ${{OUTPUT_DIR}}"

  # Generate output filename
  local filename=$(basename "${{input_file%.*}}")
  local extension="${{input_file##*.}}"
  local output_file="${{OUTPUT_DIR}}/${{filename}}_processed.${{extension}}"

  process_file "${{input_file}}" "${{output_file}}"

  print_info "Completed successfully"
}}

# Execute main function
if [[ "${{BASH_SOURCE[0]}}" == "${{0}}" ]]; then
  main "$@"
fi
'''.replace('{{name}}', name).replace('{{VERSION}}', "1.0.0")

def main():
    parser = argparse.ArgumentParser(description='Generate bash script templates following Google Shell Style Guide')
    parser.add_argument('type', choices=['basic', 'function', 'utility', 'main'],
                       help='Template type to generate')
    parser.add_argument('name', help='Name for the script (kebab-case recommended)')
    parser.add_argument('-d', '--description', help='Description of the script')
    parser.add_argument('-o', '--output', help='Output file (default: name.sh)')
    parser.add_argument('--stdout', action='store_true', help='Output to stdout instead of file')

    args = parser.parse_args()

    generator = BashTemplateGenerator()

    # Generate template
    template = generator.generate(args.type, args.name, args.description or f"{args.name} script")

    if not template:
        sys.exit(1)

    # Determine output
    if args.stdout:
        print(template)
    else:
        output_file = args.output or f"{args.name}.sh"
        Path(output_file).write_text(template)
        # Make executable
        Path(output_file).chmod(0o755)
        print(f"Generated template: {output_file}")
        print(f"Made executable: chmod +x {output_file}")

if __name__ == '__main__':
    main()