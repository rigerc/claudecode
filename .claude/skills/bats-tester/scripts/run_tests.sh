#!/usr/bin/env bash

# Bats Test Runner Script
# Enhanced test runner with additional features and reporting

set -euo pipefail

# Default values
TEST_DIR="test"
BATS_PATH=""
JOBS=""
FORMATTER="pretty"
TIMING=false
VERBOSE=false
FILTER=""
COVERAGE=false
REPORT_DIR=""
CLEAN_TEMP=true
STOP_ON_FAILURE=false

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Logging functions
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
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

log_debug() {
    if [[ "$VERBOSE" == "true" ]]; then
        echo -e "${PURPLE}[DEBUG]${NC} $1"
    fi
}

# Print usage
usage() {
    cat << EOF
Usage: $(basename "$0") [OPTIONS] [TEST_FILES...]

Enhanced Bats test runner with additional features.

Arguments:
    TEST_FILES    Specific test files to run (default: all tests in test directory)

Options:
    -d, --test-dir DIR      Test directory (default: test)
    -b, --bats-path DIR     Path to bats executable (default: test/bats/bin/bats)
    -j, --jobs N            Number of parallel jobs (default: CPU cores)
    -f, --formatter FORMAT  Output format: pretty, tap, junit (default: pretty)
    -t, --timing            Show timing information
    -v, --verbose           Enable verbose output
    -k, --filter PATTERN    Run tests matching pattern
    -c, --coverage          Generate coverage report (requires kcov)
    -r, --report-dir DIR    Directory for test reports (default: test_reports)
    --no-clean              Don't clean temporary files after tests
    --stop-on-failure       Stop on first test failure
    -h, --help              Show this help message

Examples:
    $(basename "$0")                           # Run all tests
    $(basename "$0") test/unit_test.bats       # Run specific test file
    $(basename "$0") --jobs 4 --timing         # Run with 4 parallel jobs and timing
    $(basename "$0") --formatter junit --report-dir reports/  # JUnit XML output
    $(basename "$0") --filter "integration"    # Run tests matching pattern
    $(basename "$0") --coverage                # Generate coverage report

EOF
}

# Parse command line arguments
parse_args() {
    while [[ $# -gt 0 ]]; do
        case $1 in
            -d|--test-dir)
                TEST_DIR="$2"
                shift 2
                ;;
            -b|--bats-path)
                BATS_PATH="$2"
                shift 2
                ;;
            -j|--jobs)
                JOBS="$2"
                shift 2
                ;;
            -f|--formatter)
                FORMATTER="$2"
                shift 2
                ;;
            -t|--timing)
                TIMING=true
                shift
                ;;
            -v|--verbose)
                VERBOSE=true
                shift
                ;;
            -k|--filter)
                FILTER="$2"
                shift 2
                ;;
            -c|--coverage)
                COVERAGE=true
                shift
                ;;
            -r|--report-dir)
                REPORT_DIR="$2"
                shift 2
                ;;
            --no-clean)
                CLEAN_TEMP=false
                shift
                ;;
            --stop-on-failure)
                STOP_ON_FAILURE=true
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
                # Assume remaining arguments are test files
                break
                ;;
        esac
    done

    # Remaining arguments are test files
    if [[ $# -gt 0 ]]; then
        TEST_FILES=("$@")
    else
        TEST_FILES=()
    fi
}

# Detect bats executable
detect_bats() {
    if [[ -n "$BATS_PATH" ]]; then
        if [[ ! -f "$BATS_PATH" ]]; then
            log_error "Bats executable not found: $BATS_PATH"
            exit 1
        fi
        BATS_EXEC="$BATS_PATH"
    else
        # Try common locations
        local possible_paths=(
            "$TEST_DIR/bats/bin/bats"
            "test/bats/bin/bats"
            "./bats/bin/bats"
            "bats"
        )

        for path in "${possible_paths[@]}"; do
            if command -v "$path" &> /dev/null || [[ -f "$path" ]]; then
                BATS_EXEC="$path"
                break
            fi
        done

        if [[ -z "$BATS_EXEC" ]]; then
            log_error "Bats executable not found. Please install bats-core or specify path with --bats-path"
            exit 1
        fi
    fi

    log_debug "Using bats executable: $BATS_EXEC"
}

# Validate test directory and files
validate_tests() {
    if [[ ! -d "$TEST_DIR" ]]; then
        log_error "Test directory not found: $TEST_DIR"
        exit 1
    fi

    # If specific test files provided, validate them
    if [[ ${#TEST_FILES[@]} -gt 0 ]]; then
        for file in "${TEST_FILES[@]}"; do
            if [[ ! -f "$file" ]]; then
                log_error "Test file not found: $file"
                exit 1
            fi
        done
    fi

    log_debug "Test validation passed"
}

# Setup test environment
setup_test_env() {
    log_info "Setting up test environment"

    # Create report directory if specified
    if [[ -n "$REPORT_DIR" ]]; then
        mkdir -p "$REPORT_DIR"
        log_debug "Created report directory: $REPORT_DIR"
    fi

    # Check submodules if using standard layout
    if [[ -d "$TEST_DIR/bats" ]]; then
        if [[ ! -f "$TEST_DIR/bats/bin/bats" ]]; then
            log_warning "Bats submodule not initialized. Initializing..."
            (cd "$TEST_DIR" && git submodule update --init --recursive) || {
                log_error "Failed to initialize bats submodules"
                exit 1
            }
        fi
    fi

    # Check for helper libraries
    local helper_libs=("bats-support" "bats-assert")
    for lib in "${helper_libs[@]}"; do
        if [[ ! -d "$TEST_DIR/test_helper/$lib" ]]; then
            log_warning "Helper library not found: $lib"
        fi
    done

    log_debug "Test environment setup complete"
}

# Build bats command
build_bats_command() {
    local cmd=("$BATS_EXEC")

    # Add formatter option
    if [[ "$FORMATTER" != "pretty" ]]; then
        cmd+=(--formatter "$FORMATTER")
    fi

    # Add jobs option
    if [[ -n "$JOBS" ]]; then
        cmd+=(--jobs "$JOBS")
    else
        # Default to number of CPU cores
        if command -v nproc &> /dev/null; then
            local cpu_cores=$(nproc)
            cmd+=(--jobs "$cpu_cores")
        fi
    fi

    # Add timing option
    if [[ "$TIMING" == "true" ]]; then
        cmd+=(--timing)
    fi

    # Add filter option
    if [[ -n "$FILTER" ]]; then
        cmd+=(--filter "$FILTER")
    fi

    # Add output file for JUnit format
    if [[ "$FORMATTER" == "junit" && -n "$REPORT_DIR" ]]; then
        cmd+=(--report-formatter junit --output "$REPORT_DIR/junit.xml")
    fi

    # Add test files or directory
    if [[ ${#TEST_FILES[@]} -gt 0 ]]; then
        cmd+=("${TEST_FILES[@]}")
    else
        cmd+=("$TEST_DIR")
    fi

    echo "${cmd[@]}"
}

# Run coverage analysis
run_coverage() {
    if ! command -v kcov &> /dev/null; then
        log_error "kcov is required for coverage analysis. Install with: sudo apt-get install kcov"
        exit 1
    fi

    log_info "Running coverage analysis with kcov"

    local coverage_dir="${REPORT_DIR:-test_reports}/coverage"
    mkdir -p "$coverage_dir"

    # Build bats command without coverage-specific options
    local bats_cmd
    if [[ ${#TEST_FILES[@]} -gt 0 ]]; then
        bats_cmd=("$BATS_EXEC" "${TEST_FILES[@]}")
    else
        bats_cmd=("$BATS_EXEC" "$TEST_DIR")
    fi

    # Run with kcov
    kcov \
        --exclude-path=/usr,/lib \
        --include-pattern=*.sh \
        --merge \
        "$coverage_dir" \
        "${bats_cmd[@]}"

    log_success "Coverage report generated in $coverage_dir"
}

# Clean temporary files
cleanup_temp_files() {
    if [[ "$CLEAN_TEMP" == "true" ]]; then
        log_debug "Cleaning temporary files"
        find /tmp -name "bats-run-*" -type d -exec rm -rf {} + 2>/dev/null || true
        find /tmp -name "*.bats.tmp" -delete 2>/dev/null || true
    fi
}

# Print test summary
print_summary() {
    local exit_code=$1

    echo
    if [[ $exit_code -eq 0 ]]; then
        log_success "All tests passed!"
    else
        log_error "Some tests failed!"
    fi

    # Show report locations
    if [[ -n "$REPORT_DIR" ]]; then
        log_info "Test reports: $REPORT_DIR"
    fi

    if [[ "$COVERAGE" == "true" ]]; then
        local coverage_dir="${REPORT_DIR:-test_reports}/coverage"
        log_info "Coverage report: $coverage_dir/index.html"
    fi

    return $exit_code
}

# Main execution
main() {
    local start_time
    start_time=$(date +%s)

    parse_args "$@"
    detect_bats
    validate_tests
    setup_test_env
    cleanup_temp_files

    # Build bats command
    local bats_cmd
    bats_cmd=$(build_bats_command)

    log_info "Running tests..."
    log_debug "Command: $bats_cmd"

    # Run tests or coverage
    local exit_code=0
    if [[ "$COVERAGE" == "true" ]]; then
        run_coverage
        exit_code=$?
    else
        # Execute bats command
        if [[ "$STOP_ON_FAILURE" == "true" ]]; then
            # Run with set -e to stop on first failure
            set -e
            eval "$bats_cmd"
        else
            # Run normally and capture exit code
            eval "$bats_cmd"
            exit_code=$?
        fi
    fi

    # Calculate and show timing
    local end_time
    end_time=$(date +%s)
    local duration=$((end_time - start_time))

    if [[ "$TIMING" == "true" || "$VERBOSE" == "true" ]]; then
        log_info "Tests completed in ${duration}s"
    fi

    cleanup_temp_files
    print_summary $exit_code

    exit $exit_code
}

# Handle script interruption
trap 'log_warning "Test execution interrupted"; cleanup_temp_files; exit 130' INT TERM

# Run main function with all arguments
main "$@"