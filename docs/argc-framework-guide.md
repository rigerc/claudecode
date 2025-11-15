# Argc Bash Framework: Complete Guide

Argc is a powerful Bash framework that simplifies building full-featured command-line interfaces and project automation scripts. It allows you to define CLI parameters through comment tags, automatically handling argument parsing, validation, usage text generation, and variable mapping.

## Table of Contents

- [Installation](#installation)
- [Quick Start](#quick-start)
- [Core Concepts](#core-concepts)
- [Parameter Types](#parameter-types)
- [Advanced Features](#advanced-features)
- [Command Runner (Argcfile.sh)](#command-runner-argcfilesh)
- [Best Practices](#best-practices)
- [Real-World Examples](#real-world-examples)
- [Integration and Tooling](#integration-and-tooling)

## Installation

### Installing Argc

```bash
# Install via curl (recommended)
curl -sSL https://github.com/sigoden/argc/releases/latest/download/argc-v0.9.2-x86_64-unknown-linux-musl.tar.gz | tar -xz
sudo mv argc /usr/local/bin/

# Or via cargo
cargo install argc

# Verify installation
argc --version
```

### Shell Completion Setup

```bash
# Add to ~/.bashrc
source <(argc --argc-completions bash argc)

# Add to ~/.zshrc
source <(argc --argc-completions zsh argc)

# Add to ~/.config/fish/config.fish
argc --argc-completions fish argc | source
```

## Quick Start

### Basic CLI Script

Create a simple file transfer CLI:

```bash
#!/usr/bin/env bash
# @describe A file transfer CLI
# @meta version 1.0.0

# @cmd Upload a file to server
# @alias u
# @flag -f --force              Override existing file
# @option -t --timeout <SEC>    Timeout in seconds
# @arg target!                  File to upload
upload() {
    echo "Uploading: $argc_target"
    echo "Force mode: $argc_force"
    echo "Timeout: $argc_timeout"
}

# @cmd Download a file from server
# @alias d
# @flag -f --force              Override existing file
# @option -t --tries <NUM>      Number of retry attempts
# @arg source!                  URL to download from
# @arg target                   Save file to (optional)
download() {
    echo "Downloading from: $argc_source"
    echo "Save to: ${argc_target:-current directory}"
    echo "Retries: ${argc_tries:-3}"
}

eval "$(argc --argc-eval "$0" "$@")"
```

**Usage:**

```bash
# Make executable
chmod +x transfer.sh

# Upload with options
./transfer.sh upload --force --timeout 30 /path/to/file.txt

# Download with alias
./transfer.sh d -f --tries 5 https://example.com/file.txt

# Get help
./transfer.sh --help
```

## Core Concepts

### 1. Comment-Based Configuration

Argc uses special comment tags to define CLI structure:

```bash
# @describe     Script description
# @cmd          Define a command
# @arg          Define positional argument
# @option       Define optional parameter with flag
# @flag         Define boolean flag
# @alias        Command alias
# @env          Environment variable
# @meta         Metadata and configuration
```

### 2. Variable Naming Pattern

All parameters become available as `$argc_<name>` variables:

```bash
# @arg file!
# @option --timeout <SEC>
# @flag --verbose

# Access in your function:
echo "File: $argc_file"           # Required argument
echo "Timeout: $argc_timeout"     # Option value
echo "Verbose: $argc_verbose"     # Flag (1 or 0)
```

### 3. The Magic Line

Every Argc script needs this evaluation line at the end:

```bash
eval "$(argc --argc-eval "$0" "$@")"
```

This line parses arguments, sets up variables, and calls the appropriate command function.

## Parameter Types

### Arguments (Positional Parameters)

```bash
# @arg val                      Optional single value
# @arg vals*                    Multiple values (zero or more)
# @arg required!                Required single value
# @arg multi+                   Required multiple values (one or more)
# @arg withdefault=production   Default value
# @arg env[dev|staging|prod]    Choices
# @arg mode[=fast|slow]         Choices with default
# @arg file <PATH>              Value notation hint
```

**Usage Examples:**

```bash
./script.sh cmd myfile.txt                 # Single argument
./script.sh cmd file1.txt file2.txt         # Multiple arguments (*)
./script.sh cmd --file /etc/config          # Option notation
./script.sh cmd production                  # Choices
```

### Options (Flags with Values)

```bash
# @option --simple              Basic option
# @option -s --short            Option with short flag
# @option --req!                Required option
# @option --multi*              Multi-occurrence
# @option --list*,              Multi-occurrence, comma-separated
# @option --pair <KEY> <VAL>    Two-value option
# @option --default=value       Default value
# @option --choice[a|b|c]       Choices
```

**Usage Examples:**

```bash
./script.sh cmd --simple value
./script.sh cmd -s value                  # Short flag
./script.sh cmd --multi x --multi y       # Multiple occurrences
./script.sh cmd --list a,b,c              # Comma-separated
./script.sh cmd --pair key val            # Key-value pairs
```

### Flags (Boolean Options)

```bash
# @flag -v --verbose            Enable verbose output
# @flag -d --debug*             Debug level (can repeat)
# @meta combine-shorts          Allow combined short flags
```

**Usage Examples:**

```bash
./script.sh cmd -v              # Single flag
./script.sh cmd -vvv            # Repeated flag (counter)
./script.sh cmd -vd             # Combined flags (with combine-shorts)
```

### Environment Variables

```bash
# Global env vars (top of script)
# @env API_URL!                         API endpoint (required)
# @env API_KEY                          API key (optional)
# @env RETRY_COUNT=3                    Retry attempts (default)
# @env LOG_LEVEL[debug|info|warn]       Log level (choices)
# @env ENV[=dev|staging|prod]           Environment (choices with default)

# Command-specific env vars
# @cmd Start server
# @env PORT=8080                        Server port (command-specific)
start() {
    echo "API URL: $API_URL"
    echo "Port: $PORT"
}
```

**Usage with .env file:**

```bash
# .env file
API_URL=https://api.example.com
LOG_LEVEL=debug

# Script automatically loads .env if @meta dotenv is specified
./script.sh start
```

## Advanced Features

### Dynamic Values and Validation

Use functions to provide dynamic defaults, choices, and validation:

```bash
#!/usr/bin/env bash
# @describe CLI with dynamic values

# Function to provide default value
_default_env() {
    echo "staging"
}

# Function to provide choices dynamically
_list_branches() {
    git branch --format='%(refname:short)' 2>/dev/null || echo "main"
}

# Function to provide file completions
_list_configs() {
    find config/ -name "*.yml" 2>/dev/null
}

# @cmd Deploy application
# @option -e --env=`_default_env`           Environment (dynamic default)
# @option -b --branch[`_list_branches`]     Git branch (dynamic choices)
# @option -c --config[`_list_configs`]      Config file (dynamic choices)
# @arg services+[api|web|worker]            Services to deploy
deploy() {
    echo "Environment: $argc_env"
    echo "Branch: ${argc_branch:-current}"
    echo "Config: $argc_config"
    echo "Services: ${argc_services[@]}"
}

eval "$(argc --argc-eval "$0" "$@")"
```

### Nested Subcommands

Create complex CLI structures with nested commands:

```bash
#!/usr/bin/env bash
# @describe Container management CLI

# @cmd Manage builders
builder() { :; }

# @cmd List builders
builder::ls() {
    echo "Listing all builders..."
}

# @cmd Remove builder
# @arg name!    Builder name
builder::rm() {
    echo "Removing builder: $argc_name"
}

# @cmd Image tools
builder::imagetools() { :; }

# @cmd Create image
# @option -t --tag+    Image tags
# @arg source!         Source image
builder::imagetools::create() {
    echo "Creating image from: $argc_source"
    echo "Tags: ${argc_tag[@]}"
}

eval "$(argc --argc-eval "$0" "$@")"
```

**Usage:**

```bash
./container.sh builder ls
./container.sh builder rm my-builder
./container.sh builder imagetools create --tag v1.0 source:image
```

### Hooks and Lifecycle

Add pre/post execution hooks:

```bash
#!/usr/bin/env bash
# @describe CLI with hooks

# Called before command execution
_argc_before() {
    echo "[BEFORE] Command: $argc__fn"
    # Validate prerequisites
    if [[ ! -f "./config.yml" ]]; then
        echo "Error: config.yml not found" >&2
        exit 1
    fi
}

# Called after command execution
_argc_after() {
    local exit_code=$?
    echo "[AFTER] Command completed with exit code: $exit_code"
    # Cleanup
    rm -f /tmp/temp-files-*
    return $exit_code
}

# @cmd Process data
# @arg input!    Input file
process() {
    echo "Processing: $argc_input"
}

eval "$(argc --argc-eval "$0" "$@")"
```

## Command Runner (Argcfile.sh)

Argc doubles as a command runner similar to Make or npm scripts. Create an `Argcfile.sh` in your project root:

```bash
#!/usr/bin/env bash
# Argcfile.sh - Project task automation

set -e

# @meta dotenv
# @meta require-tools node,npm,docker

# @cmd Install dependencies
# @flag -f --force    Force clean install
install() {
    if [[ "$argc_force" -eq 1 ]]; then
        rm -rf node_modules
    fi
    npm install
}

# @cmd Build the project
# @option -m --mode[dev|prod]    Build mode
# @flag --watch                  Watch mode
build() {
    install  # Dependency on install command
    echo "Building in ${argc_mode:-dev} mode..."
    if [[ "$argc_watch" -eq 1 ]]; then
        npm run build -- --watch
    else
        npm run build
    fi
}

# @cmd Run tests
# @option --coverage[lcov|html]    Generate coverage report
# @arg pattern*                    Test file patterns
test() {
    echo "Running tests: ${argc_pattern[@]:-all}"
    if [[ -n "$argc_coverage" ]]; then
        npm test -- --coverage --coverageReporters="$argc_coverage"
    else
        npm test -- ${argc_pattern[@]}
    fi
}

# @cmd Start development server
# @option -p --port=3000    Server port
# @meta default-subcommand
dev() {
    build --mode dev
    echo "Starting dev server on port $argc_port..."
    npm run dev -- --port "$argc_port"
}

eval "$(argc --argc-eval "$0" "$@")"
```

### Using Argcfile.sh

```bash
# Create Argcfile.sh quickly
argc --argc-create build test deploy

# Run commands from anywhere in project
argc                    # Shows available commands
argc install            # Install dependencies
argc build --mode prod  # Build for production
argc test --coverage html '*.test.js'

# Default subcommand (dev is marked as default)
argc                    # Runs dev command
argc --port 4000        # Start dev server on port 4000
```

## Best Practices

### 1. Script Organization

```bash
#!/usr/bin/env bash
# @describe Well-structured CLI tool
# @meta version 1.0.0
# @meta author Your Name

set -euo pipefail  # Bash strict mode

# Global environment variables
# @env CONFIG_DIR=${HOME}/.config/myapp    Config directory
# @env LOG_LEVEL[debug|info|warn]=info     Log level with default

# Utility functions
_log() {
    local level=$1
    shift
    echo "[$level] $*" >&2
}

# Command implementations
# @cmd Initialize configuration
# @arg path=${HOME}/.config/myapp    Config path
init() {
    _log "INFO" "Initializing config at: $argc_path"
    mkdir -p "$argc_path"
}

# @cmd Process data
# @arg input!                    Input file
# @flag -v --verbose             Verbose output
# @option -o --output <FILE>     Output file
process() {
    local input_file="$argc_input"
    local output_file="${argc_output:-${input_file}.processed}"

    if [[ "$argc_verbose" -eq 1 ]]; then
        _log "INFO" "Processing $input_file -> $output_file"
    fi

    # Main processing logic
    cp "$input_file" "$output_file"
}

eval "$(argc --argc-eval "$0" "$@")"
```

### 2. Error Handling and Validation

```bash
#!/usr/bin/env bash
# @describe Robust CLI with validation

# @cmd Deploy application
# @arg env[staging|production]!    Environment
# @option -v --version=latest      Version to deploy
# @flag --skip-tests               Skip test execution
deploy() {
    local env="$argc_env"
    local version="$argc_version"

    # Validate environment
    case "$env" in
        staging|production)
            _log "INFO" "Deploying to $env"
            ;;
        *)
            echo "Error: Invalid environment: $env" >&2
            exit 1
            ;;
    esac

    # Check prerequisites
    if [[ "$env" == "production" && "$argc_skip_tests" -eq 1 ]]; then
        echo "Error: Cannot skip tests for production deployment" >&2
        exit 1
    fi

    # Version validation
    if [[ "$version" != "latest" ]] && ! git rev-parse --verify "$version" >/dev/null 2>&1; then
        echo "Error: Invalid version: $version" >&2
        exit 1
    fi

    echo "Deploying version $version to $env"
}

eval "$(argc --argc-eval "$0" "$@")"
```

### 3. Configuration Management

```bash
#!/usr/bin/env bash
# @describe CLI with configuration management

# @meta dotenv  # Load .env file automatically

# Global configuration
# @env API_BASE_URL=https://api.example.com    API base URL
# @env TIMEOUT=30                             Request timeout
# @env CACHE_DIR=${HOME}/.cache/myapp         Cache directory

# Load user config if exists
if [[ -f "${HOME}/.config/myapp/config" ]]; then
    source "${HOME}/.config/myapp/config"
fi

# @cmd Configure application
# @option --api-url <URL>     API base URL
# @option --timeout <SEC>     Request timeout
# @flag --reset               Reset to defaults
configure() {
    local config_dir="${HOME}/.config/myapp"
    local config_file="$config_dir/config"

    if [[ "$argc_reset" -eq 1 ]]; then
        rm -f "$config_file"
        echo "Configuration reset to defaults"
        return
    fi

    mkdir -p "$config_dir"

    cat > "$config_file" <<EOF
# Generated configuration
API_BASE_URL="${argc_api_url:-$API_BASE_URL}"
TIMEOUT="${argc_timeout:-$TIMEOUT}"
CACHE_DIR="$CACHE_DIR"
EOF

    echo "Configuration saved to $config_file"
}

eval "$(argc --argc-eval "$0" "$@")"
```

## Real-World Examples

### Example 1: Database Management CLI

```bash
#!/usr/bin/env bash
# @describe Database management CLI
# @meta version 1.0.0

set -euo pipefail

# Environment variables
# @env DB_HOST=localhost     Database host
# @env DB_PORT=5432         Database port
# @env DB_USER!             Database username (required)
# @env DB_NAME!             Database name (required)

# Database connection helper
_db_connect() {
    PGPASSWORD="${DB_PASSWORD:-}" psql -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -d "$DB_NAME" "$@"
}

# @cmd Create database backup
# @option -o --output <FILE>     Output file (default: timestamped)
# @flag --compress               Compress backup
backup() {
    local timestamp=$(date +%Y%m%d_%H%M%S)
    local output_file="${argc_output:-backup_${DB_NAME}_${timestamp}.sql}"

    if [[ "$argc_compress" -eq 1 ]]; then
        output_file="${output_file}.gz"
        _db_connect --dump "$DB_NAME" | gzip > "$output_file"
    else
        _db_connect --dump "$DB_NAME" > "$output_file"
    fi

    echo "Backup created: $output_file"
}

# @cmd Run database migrations
# @arg direction[up|down]=up     Migration direction
# @option -v --version           Target version
migrate() {
    echo "Running migrations: $argc_direction"

    if [[ -n "$argc_version" ]]; then
        _db_connect -c "SELECT version FROM schema_migrations WHERE version = '$argc_version';"
    fi

    # Migration logic here
    echo "Migration completed"
}

# @cmd Execute SQL query
# @arg query!                    SQL query to execute
# @flag --format                 Format output
query() {
    if [[ "$argc_format" -eq 1 ]]; then
        _db_connect -c "$argc_query" | column -t
    else
        _db_connect -c "$argc_query"
    fi
}

eval "$(argc --argc-eval "$0" "$@")"
```

### Example 2: Project Development Tools

```bash
#!/usr/bin/env bash
# Argcfile.sh - Development automation

set -euo pipefail

# @meta dotenv
# @meta require-tools node,npm,docker,git

# @cmd Setup development environment
# @flag --full    Complete setup with all tools
setup() {
    echo "Setting up development environment..."

    # Install dependencies
    npm install

    if [[ "$argc_full" -eq 1 ]]; then
        # Setup pre-commit hooks
        npm run setup:pre-commit

        # Build Docker images
        docker-compose build

        # Initialize database
        npm run db:migrate

        # Load seed data
        npm run db:seed
    fi

    echo "Development environment ready!"
}

# @cmd Run development server
# @option -p --port=3000     Server port
# @option -e --env=dev       Environment
# @flag --debug              Debug mode
# @meta default-subcommand
dev() {
    local port="$argc_port"
    local env="$argc_env"

    echo "Starting development server on port $port (env: $env)"

    if [[ "$argc_debug" -eq 1 ]]; then
        export DEBUG=*
    fi

    NODE_ENV="$env" PORT="$port" npm run dev
}

# @cmd Run tests
# @option -c --coverage      Generate coverage
# @option -w --watch         Watch mode
# @arg pattern*              Test pattern
test() {
    local test_cmd="npm test"

    if [[ -n "$argc_pattern" ]]; then
        test_cmd="$test_cmd -- ${argc_pattern[*]}"
    fi

    if [[ "$argc_coverage" -eq 1 ]]; then
        test_cmd="$test_cmd -- --coverage"
    fi

    if [[ "$argc_watch" -eq 1 ]]; then
        test_cmd="$test_cmd -- --watch"
    fi

    eval "$test_cmd"
}

# @cmd Build application
# @option -m --mode[dev|prod]=prod     Build mode
# @flag --analyze                      Bundle analysis
build() {
    local mode="$argc_mode"

    echo "Building application for $mode environment..."

    if [[ "$mode" == "prod" ]]; then
        npm run build:prod
    else
        npm run build:dev
    fi

    if [[ "$argc_analyze" -eq 1 ]]; then
        npm run analyze
    fi
}

# @cmd Deployment utilities
deploy() { :; }

# @cmd Deploy to staging
# @flag --skip-tests       Skip test execution
deploy::staging() {
    if [[ "$argc_skip_tests" -ne 1 ]]; then
        test --coverage
    fi

    build --mode prod

    echo "Deploying to staging..."
    # Deployment logic here
}

# @cmd Deploy to production
# @flag --dry-run          Simulate deployment
# @arg version!            Version to deploy
deploy::production() {
    local version="$argc_version"

    echo "Deploying version $version to production..."

    if [[ "$argc_dry_run" -eq 1 ]]; then
        echo "DRY RUN: Would deploy $version"
        return
    fi

    # Production deployment logic
    echo "Deployed $version to production!"
}

eval "$(argc --argc-eval "$0" "$@")"
```

## Integration and Tooling

### Building Standalone Scripts

Create scripts that don't require the argc binary:

```bash
# Build standalone script
argc --argc-build ./myscript.sh ./dist/

# The output script contains all argc functionality
./dist/myscript.sh --help    # Works without argc installed
```

### Man Page Generation

```bash
# Generate man pages
argc --argc-mangen ./myscript.sh ./man/

# View generated man page
man ./man/myscript.1

# Install system-wide
argc --argc-mangen ./myscript.sh /usr/local/share/man/man1/
```

### Shell Completions

Generate completions for all major shells:

```bash
# Bash completion
source <(argc --argc-completions bash myscript.sh mytool)

# Zsh completion
source <(argc --argc-completions zsh myscript.sh mytool)

# Fish completion
argc --argc-completions fish myscript.sh mytool | source

# PowerShell completion
argc --argc-completions powershell myscript.sh mytool | Out-String | Invoke-Expression
```

### IDE Integration

Most modern editors support Argc through shell integration:

- **VS Code**: Use shellcheck and bash IDE extensions
- **Vim/Neovim**: Configure with shellcheck and completions
- **Emacs**: Use exec-path-from-shell and shell-script-mode

## Troubleshooting

### Common Issues

1. **"Command not found: argc"**
   - Ensure argc is in your PATH
   - Try `which argc` to verify location

2. **Permission denied**
   - Make script executable: `chmod +x script.sh`
   - Check shebang line: `#!/usr/bin/env bash`

3. **Variable not found**
   - Check parameter naming (must be `$argc_<name>`)
   - Verify parameter is defined in comments

4. **Environment variables not loading**
   - Add `# @meta dotenv` to enable .env loading
   - Check .env file location

### Debug Mode

Enable debug output to troubleshoot issues:

```bash
# Enable debug mode
set -x  # In your script

# Or use argc debug flag
argc --argc-debug ./script.sh cmd args
```

### Getting Help

- **GitHub Issues**: [sigoden/argc](https://github.com/sigoden/argc/issues)
- **Documentation**: [argc official docs](https://github.com/sigoden/argc)
- **Examples**: Check the argc repository for more examples

---

This guide provides a comprehensive overview of the Argc bash framework. Argc combines the simplicity of Bash with powerful CLI-building capabilities, making it an excellent choice for both simple scripts and complex command-line tools.