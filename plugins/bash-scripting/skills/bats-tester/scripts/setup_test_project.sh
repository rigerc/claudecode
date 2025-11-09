#!/usr/bin/env bash

# Bats Test Project Setup Script
# Creates a new project directory with bats-core testing infrastructure

set -euo pipefail

# Default values
PROJECT_NAME=""
PROJECT_DIR="."
INIT_GIT=false
QUIET=false

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Logging functions
log_info() {
    if [[ "$QUIET" != "true" ]]; then
        echo -e "${BLUE}[INFO]${NC} $1"
    fi
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1" >&2
}

# Print usage
usage() {
    cat << EOF
Usage: $(basename "$0") [OPTIONS] PROJECT_NAME

Creates a new bash project with bats-core testing infrastructure.

Arguments:
    PROJECT_NAME    Name of the project to create

Options:
    -d, --dir DIR       Project directory (default: current directory)
    -g, --git           Initialize git repository
    -q, --quiet         Suppress informational output
    -h, --help          Show this help message

Examples:
    $(basename "$0") my-project
    $(basename "$0") --git --dir ~/projects my-project
    $(basename "$0") -q -g my-bash-tool

EOF
}

# Parse command line arguments
parse_args() {
    while [[ $# -gt 0 ]]; do
        case $1 in
            -d|--dir)
                PROJECT_DIR="$2"
                shift 2
                ;;
            -g|--git)
                INIT_GIT=true
                shift
                ;;
            -q|--quiet)
                QUIET=true
                shift
                ;;
            -h|--help)
                usage
                exit 0
                ;;
            -*)
                log_error "Unknown option: $1"
                usage
                exit 1
                ;;
            *)
                if [[ -z "$PROJECT_NAME" ]]; then
                    PROJECT_NAME="$1"
                else
                    log_error "Multiple project names provided: $PROJECT_NAME and $1"
                    usage
                    exit 1
                fi
                shift
                ;;
        esac
    done

    if [[ -z "$PROJECT_NAME" ]]; then
        log_error "Project name is required"
        usage
        exit 1
    fi

    # Validate project name
    if [[ ! "$PROJECT_NAME" =~ ^[a-zA-Z][a-zA-Z0-9_-]*$ ]]; then
        log_error "Invalid project name: $PROJECT_NAME"
        log_error "Project name must start with a letter and contain only letters, numbers, hyphens, and underscores"
        exit 1
    fi
}

# Check dependencies
check_dependencies() {
    local missing_deps=()

    if ! command -v git &> /dev/null; then
        missing_deps+=("git")
    fi

    if [[ "$INIT_GIT" == "true" ]] && [[ ${#missing_deps[@]} -gt 0 ]]; then
        log_error "Missing required dependencies for git initialization: ${missing_deps[*]}"
        log_error "Install missing dependencies or run without --git flag"
        exit 1
    fi

    log_info "Dependencies check passed"
}

# Create project directory structure
create_directory_structure() {
    local project_path="$PROJECT_DIR/$PROJECT_NAME"

    log_info "Creating project directory: $project_path"

    if [[ -d "$project_path" ]]; then
        log_error "Directory already exists: $project_path"
        exit 1
    fi

    mkdir -p "$project_path"/{src,test/{test_helper,fixtures},docs}

    log_success "Directory structure created"
}

# Initialize git repository if requested
init_git_repo() {
    if [[ "$INIT_GIT" == "true" ]]; then
        log_info "Initializing git repository"
        cd "$PROJECT_DIR/$PROJECT_NAME"
        git init

        # Create .gitignore
        cat > .gitignore << 'EOF'
# Bats temporary files
/tmp/bats-*
*.bats.tmp

# Test artifacts
test_artifacts/
*.test.log

# OS-specific files
.DS_Store
Thumbs.db

# Editor files
.vscode/
.idea/
*.swp
*.swo
*~

# Backup files
*.bak
*.backup

EOF

        git add .gitignore
        git commit -m "Initial commit: Add .gitignore"

        log_success "Git repository initialized"
    fi
}

# Initialize bats submodules
init_bats_submodules() {
    log_info "Initializing bats-core submodules"
    cd "$PROJECT_DIR/$PROJECT_NAME"

    # Initialize git repository if needed for submodules
    if [[ "$INIT_GIT" != "true" ]]; then
        log_info "Initializing git repository for submodules"
        git init
        git add .
        git commit -m "Initial commit" 2>/dev/null || true
    fi

    # Add submodules
    git submodule add https://github.com/bats-core/bats-core.git test/bats
    git submodule add https://github.com/bats-core/bats-support.git test/test_helper/bats-support
    git submodule add https://github.com/bats-core/bats-assert.git test/test_helper/bats-assert

    # Initialize and update submodules
    git submodule update --init --recursive

    log_success "Bats submodules initialized"
}

# Create example files
create_example_files() {
    log_info "Creating example files"
    cd "$PROJECT_DIR/$PROJECT_NAME"

    # Create main script
    cat > "src/${PROJECT_NAME}.sh" << EOF
#!/usr/bin/env bash

# $PROJECT_NAME - Main script
# TODO: Add script description and usage

set -euo pipefail

# Script version
VERSION="0.1.0"

# Show usage information
show_usage() {
    cat << EOF
Usage: $(basename "\$0") [OPTIONS] [ARGUMENTS]

$PROJECT_NAME - TODO: Add script description

Options:
    -h, --help      Show this help message
    -v, --version   Show version information

Examples:
    \$(basename "\$0") --help
    \$(basename "\$0") example-argument

EOF
}

# Main function
main() {
    # Parse command line arguments
    while [[ \$# -gt 0 ]]; do
        case \$1 in
            -h|--help)
                show_usage
                exit 0
                ;;
            -v|--version)
                echo "\$VERSION"
                exit 0
                ;;
            -*)
                echo "Unknown option: \$1" >&2
                show_usage
                exit 1
                ;;
            *)
                echo "Unexpected argument: \$1" >&2
                show_usage
                exit 1
                ;;
        esac
        shift
    done

    # TODO: Add main script logic here
    echo "Hello from $PROJECT_NAME!"
}

# Run main function with all arguments
main "\$@"
EOF

    chmod +x "src/${PROJECT_NAME}.sh"

    # Create test file
    cat > "test/${PROJECT_NAME}_test.bats" << EOF
#!/usr/bin/env bats

# Tests for $PROJECT_NAME

setup() {
    # Load helper libraries
    load 'test_helper/bats-support/load'
    load 'test_helper/bats-assert/load'

    # Get the directory containing this test file
    DIR="\$( cd "\$( dirname "\$BATS_TEST_FILENAME" )" >/dev/null 2>&1 && pwd )"

    # Add src directory to PATH so scripts can be called without relative paths
    PATH="\$DIR/../src:\$PATH"
}

@test "script shows help with --help" {
    run ${PROJECT_NAME}.sh --help
    assert_success
    assert_output --partial "Usage:"
}

@test "script shows version with --version" {
    run ${PROJECT_NAME}.sh --version
    assert_success
    assert_output "0.1.0"
}

@test "script runs without arguments" {
    run ${PROJECT_NAME}.sh
    assert_success
    assert_output "Hello from $PROJECT_NAME!"
}

@test "script fails with unknown option" {
    run ${PROJECT_NAME}.sh --unknown-option
    assert_failure
    assert_output --partial "Unknown option"
}
EOF

    # Create Makefile
    cat > Makefile << 'EOF'
.PHONY: test test-unit test-integration test-setup test-clean

# Default target
all: test

# Run all tests
test:
	./test/bats/bin/bats test/

# Run tests with timing
test-timing:
	./test/bats/bin/bats --timing test/

# Run tests with parallel execution
test-parallel:
	./test/bats/bin/bats --jobs 4 test/

# Setup test environment
test-setup:
	chmod +x src/*.sh
	git submodule update --init --recursive

# Clean test artifacts
test-clean:
	rm -rf /tmp/bats-*
	find . -name "*.tmp" -delete
	find . -name "*.bats.tmp" -delete

# Install dependencies (if needed)
install-deps:
	@if command -v apt-get &> /dev/null; then \
		sudo apt-get update && sudo apt-get install -y git; \
	elif command -v yum &> /dev/null; then \
		sudo yum install -y git; \
	elif command -v brew &> /dev/null; then \
		brew install git; \
	else \
		echo "Please install git manually"; \
	fi

# Show project information
info:
	@echo "Project: $(shell basename $(shell pwd))"
	@echo "Test framework: Bats-Core"
	@echo "Test command: make test"
	@echo "Source directory: src/"
	@echo "Test directory: test/"
EOF

    # Create README
    cat > README.md << EOF
# $PROJECT_NAME

TODO: Add project description

## Requirements

- Bash 4.0+
- Git (for running tests)

## Installation

1. Clone this repository:
   \`\`\`bash
   git clone <repository-url>
   cd $PROJECT_NAME
   \`\`\`

2. Initialize test dependencies:
   \`\`\`bash
   make test-setup
   \`\`\`

3. Make scripts executable:
   \`\`\`bash
   chmod +x src/*.sh
   \`\`\`

## Usage

\`\`\`bash
# Show help
./src/${PROJECT_NAME}.sh --help

# Show version
./src/${PROJECT_NAME}.sh --version

# Run the script
./src/${PROJECT_NAME}.sh
\`\`\`

## Testing

Run all tests:
\`\`\`bash
make test
\`\`\`

Run tests with timing information:
\`\`\`bash
make test-timing
\`\`\`

Run tests in parallel:
\`\`\`bash
make test-parallel
\`\`\`

Clean test artifacts:
\`\`\`bash
make test-clean
\`\`\`

## Project Structure

\`\`\`
$PROJECT_NAME/
├── src/                    # Source scripts
│   └── ${PROJECT_NAME}.sh
├── test/                   # Test files
│   ├── bats/              # Bats-core (git submodule)
│   ├── test_helper/       # Bats helper libraries (git submodules)
│   │   ├── bats-support/
│   │   └── bats-assert/
│   └── ${PROJECT_NAME}_test.bats
├── docs/                   # Documentation
├── Makefile               # Build and test commands
└── README.md              # This file
\`\`\`

## Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure all tests pass
5. Submit a pull request

## License

TODO: Add license information
EOF

    log_success "Example files created"
}

# Create git commits if git was initialized
create_git_commits() {
    if [[ "$INIT_GIT" == "true" ]]; then
        log_info "Creating initial git commits"
        cd "$PROJECT_DIR/$PROJECT_NAME"

        git add .
        git commit -m "Add project files and examples"

        log_success "Initial git commits created"
    fi
}

# Print success message
print_success() {
    local project_path="$PROJECT_DIR/$PROJECT_NAME"

    echo
    log_success "Project '$PROJECT_NAME' created successfully!"
    echo
    echo "Project location: $project_path"
    echo
    echo "Next steps:"
    echo "  1. cd $project_path"
    echo "  2. make test-setup   # Initialize test dependencies"
    echo "  3. make test         # Run tests"
    echo "  4. ./src/${PROJECT_NAME}.sh --help  # See script usage"
    echo
    echo "Useful commands:"
    echo "  make test           # Run all tests"
    echo "  make test-timing    # Run tests with timing"
    echo "  make test-parallel  # Run tests in parallel"
    echo "  make test-clean     # Clean test artifacts"
    echo "  make info           # Show project information"
    echo
}

# Main execution
main() {
    parse_args "$@"
    check_dependencies
    create_directory_structure

    if [[ "$INIT_GIT" == "true" ]]; then
        init_git_repo
    fi

    init_bats_submodules
    create_example_files
    create_git_commits
    print_success
}

# Run main function with all arguments
main "$@"