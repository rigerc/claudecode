---
name: bash-scripting
description: This skill should be used when users need to write or edit bash scripts. It provides templates, guidelines, style checking, and best practices for creating maintainable bash shell scripts (*.sh files).
---

# Bash Scripting

## Overview

This skill enables writing and editing bash scripts following Google Shell Style Guide and reviewing/refactoring existing scripts. It provides automated style checking, script templates, and comprehensive best practices for creating maintainable shell scripts.

## Quick Start

### Writing New Scripts

Use the template generator to create properly structured bash scripts:

```bash
# Basic script template
python3 scripts/generate_template.py basic my-script "Process input files"

# Full-featured main script
python3 scripts/generate_template.py main data-processor "Process CSV data files"

# Function library
python3 scripts/generate_template.py function utils "Utility functions"
```

### Reviewing Existing Scripts

Check existing scripts for style violations:

```bash
# Check a specific file
python3 scripts/style_checker.py script.sh

# Check script from stdin
cat script.sh | python3 scripts/style_checker.py
```

## Core Capabilities

### 1. Script Creation Workflow

Follow this workflow for creating new bash scripts:

#### Step 1: Choose Template Type
- **Basic**: Simple scripts with minimal structure
- **Main**: Full-featured scripts with argument parsing, logging, and error handling
- **Function**: Function libraries for sourcing
- **Utility**: Scripts with common utility patterns

#### Step 2: Generate Template
```bash
# Generate main script template
python3 scripts/generate_template.py main backup-script "Backup utility script"

# This creates: backup-script.sh (executable)
```

#### Step 3: Customize for Your Use Case
- Update the description and version
- Modify argument parsing for your specific needs
- Add your core logic in the designated sections
- Test with `./script.sh --help`

#### Step 4: Style Check
```bash
python3 scripts/style_checker.py backup-script.sh
```

### 2. Script Review Workflow

Use this workflow for reviewing existing bash scripts:

#### Step 1: Initial Analysis
Run the style checker to identify violations:
```bash
python3 scripts/style_checker.py script.sh
```

#### Step 2: Address Critical Errors
Focus on these priority issues:
- Use `$(command)` instead of backticks
- Add proper variable quoting: `"${var}"`
- Fix indentation (use 2 spaces, no tabs)
- Add `set -euo pipefail` at script start

#### Step 3: Improve Structure
- Add function organization
- Implement proper error handling
- Add argument parsing for main scripts
- Include help documentation

#### Step 4: Final Validation
```bash
# Re-check after fixes
python3 scripts/style_checker.py script.sh

# Test script functionality
./script.sh --help
./script.sh --dry-run [test-args]
```

## Google Shell Style Guide Rules

### File Structure

#### Shebang and Permissions
```bash
#!/bin/bash  # Always use bash, not sh
chmod +x script.sh  # Make executable
```

#### File Extensions
- Use `.sh` for executables with build rules
- No extension for scripts in PATH
- Never use SUID/SGID on shell scripts

### Code Formatting

#### Indentation
```bash
# ✅ Correct: 2 spaces
if [[ -f "$file" ]]; then
  process_file "$file"
fi

# ❌ Wrong: tabs or inconsistent spacing
if [[ -f "$file" ]]; then
	process_file "$file"
fi
```

#### Line Length
- Maximum 80 characters per line
- Use line continuation for long commands:
```bash
long_command --option1 value1 \
             --option2 value2 \
             input_file
```

#### Control Flow
```bash
# ✅ Correct: if and then on same line
if [[ condition ]]; then
  action
fi

# ❌ Wrong: if and then on separate lines
if [[ condition ]]
then
  action
fi
```

### Variable Usage

#### Always Quote Variables
```bash
# ✅ Correct: Always quoted
filename="$1"
output_dir="${filename%.*}_processed"
echo "Processing: ${filename}"

# ❌ Wrong: Unquoted variables
filename=$1
echo $filename
```

#### Variable Naming
```bash
# ✅ Correct: Lowercase for variables, uppercase for constants
readonly SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
readonly MAX_RETRIES=5

local temp_file="${1:-default_value}"

# ❌ Wrong: Inconsistent naming
TempDir="/tmp"
max_retries=5
```

#### Arrays for Lists
```bash
# ✅ Correct: Use arrays for multiple values
files=("file1.txt" "file2.txt" "file3.txt")
for file in "${files[@]}"; do
  process_file "$file"
done

# ❌ Wrong: Space-separated strings for lists
files="file1.txt file2.txt file3.txt"
for file in $files; do  # This breaks with spaces in filenames
  process_file "$file"
done
```

### Command Usage

#### Command Substitution
```bash
# ✅ Correct: Use $(command)
current_dir="$(pwd)"
file_count="$(ls -1 *.txt | wc -l)"

# ❌ Wrong: Use backticks
current_dir=\`pwd\`
file_count=\`ls -1 *.txt | wc -l\`
```

#### Test Statements
```bash
# ✅ Correct: Use [[ ]] for tests
if [[ -f "$filename" && -r "$filename" ]]; then
  process_file "$filename"
fi

# ❌ Wrong: Use [ ] for complex tests
if [ -f "$filename" -a -r "$filename" ]; then
  process_file "$filename"
fi
```

#### Error Handling
```bash
# ✅ Correct: Check return values
if ! cp "$source" "$destination"; then
  echo "Error: Failed to copy file" >&2
  exit 1
fi

# ✅ Correct: Use set -euo pipefail
set -euo pipefail  # Exit on error, undefined vars, pipe failures
```

### Functions

#### Function Definition and Naming
```bash
# ✅ Correct: lowercase_with_underscores
process_file() {
  local filename="${1:-}"
  local output_dir="${2:-output}"

  if [[ -z "$filename" ]]; then
    echo "Error: filename required" >&2
    return 1
  fi

  # Function logic here
}

# ❌ Wrong: camelCase or inconsistent naming
processFile() {
  # ...
}
```

#### Local Variables
```bash
# ✅ Correct: Use local for function variables
calculate_sum() {
  local num1="${1:-0}"
  local num2="${2:-0}"
  local result=$((num1 + num2))
  echo "$result"
}

# ❌ Wrong: Global variables in functions
total=0
calculate_sum() {
  num1="${1:-0}"
  num2="${2:-0}"
  total=$((num1 + num2))  # Modifies global variable
}
```

## Common Patterns and Examples

### Argument Parsing
```bash
#!/bin/bash
set -euo pipefail

readonly SCRIPT_NAME="$(basename "${BASH_SOURCE[0]}")"
VERBOSE=false
DRY_RUN=false

show_usage() {
  cat << EOF
Usage: $SCRIPT_NAME [OPTIONS] <input>

Options:
  -h, --help     Show this help message
  -v, --verbose  Enable verbose output
  -n, --dry-run  Show what would be done without executing

Examples:
  $SCRIPT_NAME --verbose input.txt
  $SCRIPT_NAME --dry-run input.txt
EOF
}

parse_arguments() {
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
      -*)
        echo "Error: Unknown option $1" >&2
        show_usage
        exit 1
        ;;
      *)
        break
        ;;
    esac
  done
}
```

### Logging Functions
```bash
# Color output
readonly RED='\033[0;31m'
readonly GREEN='\033[0;32m'
readonly YELLOW='\033[1;33m'
readonly NC='\033[0m'  # No Color

log_info() {
  local message="${1:-}"
  echo -e "${GREEN}[INFO]${NC} $message"
}

log_warn() {
  local message="${1:-}"
  echo -e "${YELLOW}[WARN]${NC} $message" >&2
}

log_error() {
  local message="${1:-}"
  echo -e "${RED}[ERROR]${NC} $message" >&2
}
```

### File Processing
```bash
process_files() {
  local directory="${1:-.}"
  local pattern="${2:-*.txt}"

  # Use find with proper handling of special characters
  while IFS= read -r -d '' file; do
    log_info "Processing: $file"

    if [[ "$DRY_RUN" == "true" ]]; then
      log_info "DRY RUN: Would process $file"
    else
      process_single_file "$file"
    fi
  done < <(find "$directory" -name "$pattern" -type f -print0)
}

process_single_file() {
  local file="${1:-}"

  if [[ ! -f "$file" ]]; then
    log_error "File not found: $file"
    return 1
  fi

  if [[ ! -r "$file" ]]; then
    log_error "Cannot read file: $file"
    return 1
  fi

  # Processing logic here
  cp "$file" "${file}.backup"
}
```

## Resources

### scripts/

The `scripts/` directory contains executable tools for bash script development:

#### `style_checker.py`
Automated style checker that validates bash scripts against Google Shell Style Guide rules:
- Checks line length (80 char limit)
- Validates 2-space indentation
- Ensures proper variable quoting
- Detects backticks (recommends $(command))
- Validates test statements (suggests [[ ]] over [ ])
- Checks function naming conventions

**Usage:**
```bash
# Check specific file
python3 scripts/style_checker.py script.sh

# Check from stdin
cat script.sh | python3 scripts/style_checker.py

# Check multiple files
for script in *.sh; do
  echo "Checking $script:"
  python3 scripts/style_checker.py "$script"
  echo
done
```

#### `generate_template.py`
Template generator that creates bash scripts following best practices:
- **basic**: Simple script with basic structure
- **main**: Full-featured script with argument parsing, logging, error handling
- **function**: Function library template for sourcing
- **utility**: Script with common utility patterns

**Usage:**
```bash
# Generate basic script
python3 scripts/generate_template.py basic my-script "Description here"

# Generate main script (recommended for most use cases)
python3 scripts/generate_template.py main data-processor "Process data files"

# Generate function library
python3 scripts/generate_template.py function utils "Utility functions"

# Output to stdout instead of file
python3 scripts/generate_template.py main test-script --stdout
```

### references/

### assets/

The `assets/` directory contains templates and example files that can be used as starting points or copied into user projects.

---

**Key Usage Patterns:**
- "Create a bash script that..." → Use `generate_template.py` then customize
- "Review this bash script" → Use `style_checker.py` then address violations
- "Fix style issues in this script" → Run checker, prioritize errors, apply fixes systematically
- "Convert this script to follow Google style guide" → Systematic refactoring using this skill's rules

**When NOT to use this skill:**
- For non-bash shell scripts (use appropriate language-specific skills)
- For simple one-liners that don't need full script structure
- When the user specifically wants to violate style guidelines for compatibility reasons