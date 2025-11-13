#!/bin/bash

# Go Package Explorer Script
# This script helps explore Go packages using go doc with various options

set -e

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Print colored output
print_header() {
    echo -e "${BLUE}=== $1 ===${NC}"
}

print_section() {
    echo -e "${CYAN}--- $1 ---${NC}"
}

print_info() {
    echo -e "${GREEN}ℹ $1${NC}"
}

print_command() {
    echo -e "${PURPLE}> $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

# Show help
show_help() {
    cat << EOF
Go Package Explorer Script

USAGE:
    $0 [PACKAGE] [OPTIONS]

PACKAGES:
    PACKAGE              Go package import path (e.g., fmt, encoding/json)

OPTIONS:
    -a, --all           Show all documentation (equivalent to -all)
    -s, --short         Show one-line summaries only
    -u, --unexported    Include unexported symbols
    -c, --case-sensitive  Use case-sensitive matching
    -src, --source      Show source code
    -cmd, --command     Include command symbols
    -f, --filter PATTERN   Filter output with grep pattern
    -o, --output FILE   Save output to file
    -w, --web           Start HTTP server for web browsing
    -p, --port PORT     Port for HTTP server (default: 6060)
    -v, --verbose       Verbose output
    -h, --help          Show this help

EXAMPLES:
    $0 fmt                              # Basic package documentation
    $0 encoding/json --all              # Complete JSON package documentation
    $0 net/http --short --filter "func.*Client"  # Filter HTTP client functions
    $0 time --unexported               # Include unexported time symbols
    $0 context --web                   # Start web server for context package
    $0 --help                          # Show help

FEATURES:
    - Package overview with structure analysis
    - Function and type exploration
    - Method discovery
    - Source code viewing
    - HTTP server integration
    - Output filtering and saving

EOF
}

# Validate package exists
validate_package() {
    local package=$1
    if ! go list "$package" > /dev/null 2>&1; then
        print_error "Package '$package' not found"
        print_info "Try 'go list $package' to verify package exists"
        return 1
    fi
    return 0
}

# Get package directory
get_package_dir() {
    local package=$1
    go list -f '{{.Dir}}' "$package" 2>/dev/null || ""
}

# Show package overview
show_overview() {
    local package=$1
    local flags=$2

    print_header "Package Overview: $package"

    # Basic package info
    print_section "Basic Information"
    local pkg_dir=$(get_package_dir "$package")
    print_info "Import path: $package"
    print_info "Directory: $pkg_dir"

    # Show package documentation
    print_section "Package Documentation"
    print_command "go doc $flags $package"
    go doc $flags "$package"
    echo
}

# Show all symbols
show_symbols() {
    local package=$1
    local flags=$2
    local filter=$3

    print_header "Package Symbols: $package"

    local cmd="go doc -all $flags $package"

    if [ -n "$filter" ]; then
        cmd="$cmd | grep -E '$filter'"
        print_command "$cmd"
        eval "$cmd"
    else
        print_command "$cmd"
        go doc -all $flags "$package"
    fi
    echo
}

# Show functions only
show_functions() {
    local package=$1
    local flags=$2
    local filter=$3

    print_header "Functions: $package"

    local cmd="go doc -all $flags $package | grep -E '^[[:space:]]*func'"

    if [ -n "$filter" ]; then
        cmd="$cmd | grep -E '$filter'"
    fi

    print_command "$cmd"
    eval "$cmd"
    echo
}

# Show types only
show_types() {
    local package=$1
    local flags=$2
    local filter=$3

    print_header "Types: $package"

    local cmd="go doc -all $flags $package | grep -E '^[[:space:]]*type'"

    if [ -n "$filter" ]; then
        cmd="$cmd | grep -E '$filter'"
    fi

    print_command "$cmd"
    eval "$cmd"
    echo
}

# Show methods for types
show_methods() {
    local package=$1
    local flags=$2
    local filter=$3

    print_header "Methods: $package"

    # Get all types first
    local types=$(go doc -all "$package" | grep -E '^[[:space:]]*type' | sed 's/^[[:space:]]*type[[:space:]]*\([^[:space:]]*\).*/\1/')

    for type in $types; do
        if [ -n "$filter" ]; then
            if ! echo "$type" | grep -E "$filter" > /dev/null; then
                continue
            fi
        fi

        print_section "Type: $type"
        local cmd="go doc -all $flags $package.$type"
        print_command "$cmd"
        eval "$cmd"
        echo
    done
}

# Show variables and constants
show_variables() {
    local package=$1
    local flags=$2
    local filter=$3

    print_header "Variables and Constants: $package"

    local cmd="go doc -all $flags $package | grep -E '^[[:space:]]*(var|const)'"

    if [ -n "$filter" ]; then
        cmd="$cmd | grep -E '$filter'"
    fi

    print_command "$cmd"
    eval "$cmd"
    echo
}

# Show source code
show_source() {
    local package=$1
    local symbol=$2

    print_header "Source Code"

    if [ -n "$symbol" ]; then
        print_section "Source for $package.$symbol"
        print_command "go doc -src $package.$symbol"
        go doc -src "$package.$symbol"
    else
        print_section "Package Files"
        local pkg_dir=$(get_package_dir "$package")
        if [ -n "$pkg_dir" ]; then
            print_info "Files in $(basename "$pkg_dir"):"
            find "$pkg_dir" -name "*.go" -exec basename {} \; | sort
            echo

            print_info "Main files:"
            find "$pkg_dir" -name "*.go" -not -name "*_test.go" | head -5
        fi
    fi
}

# Start HTTP server
start_web_server() {
    local package=$1
    local port=$2

    print_header "Starting HTTP Documentation Server"

    local pkg_dir=$(get_package_dir "$package")
    if [ -n "$pkg_dir" ]; then
        cd "$pkg_dir"
        print_info "Working directory: $pkg_dir"
    fi

    local url="http://localhost:$port"
    print_info "Starting server on $url"

    print_command "go doc -http=:$port"
    go doc -http=":$port"
}

# Analyze package structure
analyze_structure() {
    local package=$1

    print_header "Package Structure Analysis"

    # Get basic info
    local pkg_dir=$(get_package_dir "$package")
    print_section "Basic Statistics"

    if [ -n "$pkg_dir" ]; then
        print_info "Directory: $pkg_dir"

        # Count Go files
        local go_files=$(find "$pkg_dir" -name "*.go" | wc -l)
        print_info "Go files: $go_files"

        # Count test files
        local test_files=$(find "$pkg_dir" -name "*_test.go" | wc -l)
        print_info "Test files: $test_files"

        # Count exported symbols
        local exported=$(go doc -all "$package" | grep -E '^[[:space:]]*(func|type|var|const)' | grep -v -E '^[[:space:]]*[a-z]' | wc -l)
        print_info "Exported symbols: $exported"

        echo

        # Show file structure
        print_section "File Structure"
        find "$pkg_dir" -name "*.go" | sort | while read -r file; do
            local basename=$(basename "$file")
            local rel_path=$(echo "$file" | sed "s|$pkg_dir/||")
            print_info "$rel_path"
        done
    fi

    echo
}

# Save output to file
save_output() {
    local package=$1
    local output_file=$2
    local flags=$3

    print_header "Saving Documentation to File"

    print_command "go doc -all $flags $package > $output_file"
    go doc -all $flags "$package" > "$output_file"

    print_info "Documentation saved to: $output_file"
    local file_size=$(wc -l < "$output_file")
    print_info "Lines: $file_size"
}

# Main exploration function
explore_package() {
    local package=$1
    shift

    # Default options
    local flags=""
    local filter=""
    local output_file=""
    local start_web=false
    local port=6060
    local show_src=false
    local symbol=""
    local verbose=false

    # Parse options
    while [[ $# -gt 0 ]]; do
        case $1 in
            -a|--all)
                flags="$flags -all"
                shift
                ;;
            -s|--short)
                flags="$flags -short"
                shift
                ;;
            -u|--unexported)
                flags="$flags -u"
                shift
                ;;
            -c|--case-sensitive)
                flags="$flags -c"
                shift
                ;;
            -src|--source)
                show_src=true
                shift
                ;;
            -cmd|--command)
                flags="$flags -cmd"
                shift
                ;;
            -f|--filter)
                filter="$2"
                shift 2
                ;;
            -o|--output)
                output_file="$2"
                shift 2
                ;;
            -w|--web)
                start_web=true
                shift
                ;;
            -p|--port)
                port="$2"
                shift 2
                ;;
            -v|--verbose)
                verbose=true
                shift
                ;;
            *)
                if [[ "$1" != -* ]]; then
                    # Assume it's a symbol for source viewing
                    symbol="$1"
                fi
                shift
                ;;
        esac
    done

    # Validate package
    if ! validate_package "$package"; then
        return 1
    fi

    if [ "$verbose" = true ]; then
        print_info "Exploring package: $package"
        print_info "Flags: $flags"
        print_info "Filter: $filter"
        print_info "Output file: $output_file"
        print_info "Start web: $start_web"
        print_info "Port: $port"
    fi

    # If output file specified, save and exit
    if [ -n "$output_file" ]; then
        save_output "$package" "$output_file" "$flags"
        return 0
    fi

    # If web server requested, start and exit
    if [ "$start_web" = true ]; then
        start_web_server "$package" "$port"
        return 0
    fi

    # If source viewing requested
    if [ "$show_src" = true ]; then
        show_source "$package" "$symbol"
        return 0
    fi

    # Regular exploration
    show_overview "$package" "$flags"
    analyze_structure "$package"
    show_functions "$package" "$flags" "$filter"
    show_types "$package" "$flags" "$filter"
    show_variables "$package" "$flags" "$filter"
    show_methods "$package" "$flags" "$filter"
}

# Parse command line arguments
if [[ $# -eq 0 ]]; then
    show_help
    exit 0
fi

case "${1:-}" in
    -h|--help)
        show_help
        exit 0
        ;;
    *)
        explore_package "$@"
        ;;
esac