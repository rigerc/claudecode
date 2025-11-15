# Argc Parameter Syntax Quick Reference

Quick lookup for argc comment tags and parameter patterns.

## Comment Tags

| Tag | Purpose | Example |
|-----|---------|---------|
| `@describe` | Script/command description | `# @describe File transfer CLI` |
| `@cmd` | Define command | `# @cmd Upload file` |
| `@arg` | Positional argument | `# @arg file! <PATH>` |
| `@option` | Option with value | `# @option --timeout <SEC>` |
| `@flag` | Boolean flag | `# @flag -v --verbose` |
| `@alias` | Command alias | `# @alias u` |
| `@env` | Environment variable | `# @env API_KEY!` |
| `@meta` | Metadata/config | `# @meta version 1.0.0` |

## Argument Modifiers

| Syntax | Meaning | Example |
|--------|---------|---------|
| `val` | Optional single value | `# @arg file` |
| `val!` | Required single value | `# @arg file!` |
| `vals*` | Multiple values (0+) | `# @arg files*` |
| `vals+` | Multiple values (1+) | `# @arg files+` |
| `val=default` | Default value | `# @arg env=prod` |
| `val[a\|b\|c]` | Choices | `# @arg mode[fast\|slow]` |
| `val[=a\|b]` | Choices with default | `# @arg env[=dev\|prod]` |
| `val <NOTATION>` | Value notation hint | `# @arg file <PATH>` |

## Option Syntax

```bash
# Basic option
# @option --name

# With short flag
# @option -n --name

# Required option
# @option --name!

# Multiple occurrences
# @option --name*

# Comma-separated values
# @option --list*,

# Two-value option (key-value pairs)
# @option --pair <KEY> <VAL>

# With default
# @option --timeout=30

# With choices
# @option --level[debug|info|warn]

# Complete example
# @option -t --timeout=30 <SEC>    Request timeout in seconds
```

## Flag Syntax

```bash
# Basic flag
# @flag --verbose

# With short flag
# @flag -v --verbose

# Repeatable (counter)
# @flag -d --debug*

# Multiple short flags (requires @meta combine-shorts)
# @flag -v --verbose
# @flag -d --debug
# @meta combine-shorts
# Usage: script.sh -vd
```

## Environment Variables

```bash
# Optional env var
# @env API_URL

# Required env var
# @env API_KEY!

# With default value
# @env PORT=8080

# With choices
# @env LOG_LEVEL[debug|info|warn]

# With choices and default
# @env ENV[=dev|staging|prod]
```

## Dynamic Values

Use backticks to call functions for dynamic defaults or choices:

```bash
# Dynamic default value
_default_branch() { git branch --show-current; }
# @arg branch=`_default_branch`

# Dynamic choices
_list_configs() { find config/ -name "*.yml"; }
# @option --config[`_list_configs`]

# Dynamic choices for completion
_list_branches() { git branch --format='%(refname:short)'; }
# @option -b --branch[`_list_branches`]
```

## Nested Commands

Use `::` to create command hierarchies:

```bash
# @cmd Parent command
parent() { :; }

# @cmd Subcommand under parent
parent::sub() {
    echo "Nested command"
}

# @cmd Deeply nested
parent::sub::deep() {
    echo "Deep nesting"
}
```

**Usage:**
```bash
./script.sh parent sub
./script.sh parent sub deep
```

## Variable Access

All parameters are available as `$argc_<name>` variables:

```bash
# @arg file!
# @option --timeout <SEC>
# @flag -v --verbose

my_command() {
    echo "$argc_file"           # Required arg
    echo "$argc_timeout"        # Option value (empty if not provided)
    echo "$argc_verbose"        # Flag (1 if set, 0 if not)
}
```

### Arrays for Multiple Values

```bash
# @arg files+
# @option --tag*

deploy() {
    # Access array elements
    for file in "${argc_files[@]}"; do
        echo "File: $file"
    done

    # Array count
    echo "Number of tags: ${#argc_tag[@]}"

    # All values
    echo "Tags: ${argc_tag[*]}"
}
```

## Meta Directives

```bash
# @meta version 1.0.0              Version information
# @meta author "Your Name"         Author
# @meta dotenv                     Load .env file
# @meta combine-shorts             Allow -abc for -a -b -c
# @meta default-subcommand         Make command default
# @meta require-tools tool1,tool2  Check for required tools
```

## Hooks

```bash
# Called before any command
_argc_before() {
    echo "Before: $argc__fn"
    # Validation, setup, etc.
}

# Called after any command
_argc_after() {
    local exit_code=$?
    echo "After: exit $exit_code"
    # Cleanup, reporting, etc.
    return $exit_code
}
```

## Special Variables

| Variable | Description |
|----------|-------------|
| `$argc__fn` | Current command function name |
| `$argc__args` | All raw arguments |

## Complete Script Template

```bash
#!/usr/bin/env bash
# @describe My CLI tool
# @meta version 1.0.0
# @meta dotenv

set -euo pipefail

# Global env vars
# @env CONFIG_DIR=${HOME}/.config/myapp

# Utility functions
_log() { echo "[$1] ${*:2}" >&2; }

# @cmd Main command
# @arg input!                Input file
# @option -o --output        Output file
# @flag -v --verbose         Verbose mode
main() {
    [[ "$argc_verbose" -eq 1 ]] && _log "INFO" "Processing $argc_input"
    echo "Output: ${argc_output:-stdout}"
}

eval "$(argc --argc-eval "$0" "$@")"
```

## Common Patterns

### Optional with Default
```bash
# @arg env=production
# Access: ${argc_env}  # Always has value (arg or default)
```

### Required Validation
```bash
# @arg file!
# Argc automatically validates - no need for manual checks
```

### Choice Validation
```bash
# @arg mode[dev|staging|prod]
# Argc only accepts listed values
```

### Boolean Flags
```bash
# @flag --force
if [[ "$argc_force" -eq 1 ]]; then
    echo "Force mode enabled"
fi
```

### Repeatable Counter
```bash
# @flag -v --verbose*
# -v = 1, -vv = 2, -vvv = 3
case "$argc_verbose" in
    0) ;; # Silent
    1) echo "Verbose" ;;
    *) echo "Very verbose" ;;
esac
```

## Tips

1. **Always end with eval line**: `eval "$(argc --argc-eval "$0" "$@")"`
2. **Use long names for clarity**: `--timeout` better than `-t` alone
3. **Add descriptions**: They appear in `--help` output
4. **Validate early**: Let argc handle validation via `!` and `[choices]`
5. **Use functions for dynamic values**: More maintainable than hardcoded lists
6. **Test help output**: `./script.sh --help` should be clear and complete
