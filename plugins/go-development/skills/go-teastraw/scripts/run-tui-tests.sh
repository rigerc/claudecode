#!/bin/bash

# Run TUI Tests Script for Teastraw Testing
# This script provides a comprehensive testing suite for TUI applications

set -e

# Default values
VERBOSE=false
UPDATE_GOLDEN=false
COVERAGE=false
INTEGRATION=false
SPECIFIC_TEST=""
TERMINAL_SIZES="80x24"
PARALLEL=false

# Help function
show_help() {
    cat << EOF
Usage: $0 [OPTIONS]

Run TUI tests with various configurations and options.

OPTIONS:
    -v, --verbose      Run tests with verbose output
    -u, --update       Update golden files instead of running tests
    -c, --coverage     Generate test coverage report
    -i, --integration  Include integration tests
    -t, --test TEST    Run specific test function
    -s, --sizes SIZE   Test with multiple terminal sizes (e.g., "80x24,120x40,40x12")
    -p, --parallel     Run tests in parallel
    -h, --help         Show this help message

EXAMPLES:
    $0                                    # Run basic TUI tests
    $0 -v -c                             # Run with verbose output and coverage
    $0 -u                                # Update golden files
    $0 -t TestNavigation                 # Run specific test
    $0 -s "80x24,120x40"                 # Test with multiple terminal sizes
    $0 -i -p                             # Run integration tests in parallel

ENVIRONMENT VARIABLES:
    TEST_TIMEOUT    - Timeout for test operations (default: 30s)
    NO_COLOR        - Disable color output (set to 1)
    TERM            - Terminal type (default: xterm-256color)

EOF
}

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        -v|--verbose)
            VERBOSE=true
            shift
            ;;
        -u|--update)
            UPDATE_GOLDEN=true
            shift
            ;;
        -c|--coverage)
            COVERAGE=true
            shift
            ;;
        -i|--integration)
            INTEGRATION=true
            shift
            ;;
        -t|--test)
            SPECIFIC_TEST="$2"
            shift 2
            ;;
        -s|--sizes)
            TERMINAL_SIZES="$2"
            shift 2
            ;;
        -p|--parallel)
            PARALLEL=true
            shift
            ;;
        -h|--help)
            show_help
            exit 0
            ;;
        *)
            echo "Unknown option: $1"
            show_help
            exit 1
            ;;
    esac
done

# Check if we're in a Go project
if [ ! -f "go.mod" ]; then
    echo "Error: No go.mod file found. Please run this script from the root of a Go project."
    exit 1
fi

# Set environment variables for consistent testing
export TEST_MODE=1
export NO_COLOR=1
export TERM=xterm-256color

# Timeout from environment or default
TEST_TIMEOUT=${TEST_TIMEOUT:-30s}

echo "=== Teastraw TUI Test Runner ==="
echo "Configuration:"
echo "  Verbose: $VERBOSE"
echo "  Update Golden: $UPDATE_GOLDEN"
echo "  Coverage: $COVERAGE"
echo "  Integration: $INTEGRATION"
echo "  Specific Test: $SPECIFIC_TEST"
echo "  Terminal Sizes: $TERMINAL_SIZES"
echo "  Parallel: $PARALLEL"
echo "  Test Timeout: $TEST_TIMEOUT"
echo ""

# Build the test command
TEST_CMD="go test"
TEST_FLAGS=""

if [ "$VERBOSE" = true ]; then
    TEST_FLAGS="$TEST_FLAGS -v"
fi

if [ "$UPDATE_GOLDEN" = true ]; then
    TEST_FLAGS="$TEST_FLAGS -update"
fi

if [ "$COVERAGE" = true ]; then
    TEST_FLAGS="$TEST_FLAGS -coverprofile=coverage.out -covermode=atomic"
fi

if [ "$PARALLEL" = true ]; then
    TEST_FLAGS="$TEST_FLAGS -parallel"
    # Use number of CPU cores for parallel execution
    TEST_FLAGS="$TEST_FLAGS $(nproc)"
fi

if [ -n "$SPECIFIC_TEST" ]; then
    TEST_FLAGS="$TEST_FLAGS -run $SPECIFIC_TEST"
fi

# Add timeout for all tests
TEST_FLAGS="$TEST_FLAGS -timeout $TEST_TIMEOUT"

# Function to run tests for a specific terminal size
run_tests_for_size() {
    local size=$1
    local width=${size%x*}
    local height=${size#*x}

    echo "--- Testing with terminal size: ${width}x${height} ---"

    # Set terminal size environment variables
    export COLUMNS=$width
    export LINES=$height

    # Determine which test directories to run
    TEST_DIRS="./tests/tui"
    if [ "$INTEGRATION" = true ]; then
        TEST_DIRS="$TEST_DIRS ./tests/integration"
    fi

    # Check for root test files
    if ls *_test.go 1> /dev/null 2>&1; then
        TEST_DIRS="$TEST_DIRS ."
    fi

    # Run the tests
    echo "Running: $TEST_CMD $TEST_FLAGS $TEST_DIRS"
    if eval "$TEST_CMD $TEST_FLAGS $TEST_DIRS"; then
        echo "✓ Tests passed for size ${width}x${height}"
        return 0
    else
        echo "✗ Tests failed for size ${width}x${height}"
        return 1
    fi
}

# Main test execution
FAILED_SIZES=()

if [ "$UPDATE_GOLDEN" = true ]; then
    echo "Updating golden files..."
    # For updating, just run once with default size
    if ! run_tests_for_size "80x24"; then
        echo "Failed to update golden files"
        exit 1
    fi
else
    # Run tests for each specified terminal size
    IFS=',' read -ra SIZES <<< "$TERMINAL_SIZES"
    for size in "${SIZES[@]}"; do
        size=$(echo "$size" | xargs) # Trim whitespace
        if ! run_tests_for_size "$size"; then
            FAILED_SIZES+=("$size")
        fi
        echo ""
    done
fi

# Coverage report
if [ "$COVERAGE" = true ] && [ -f "coverage.out" ]; then
    echo "=== Coverage Report ==="
    go tool cover -html=coverage.out -o coverage.html
    go tool cover -func=coverage.out | tail -1
    echo "Coverage report saved to coverage.html"
fi

# Summary
echo "=== Test Summary ==="
if [ "$UPDATE_GOLDEN" = true ]; then
    echo "✓ Golden files updated successfully"
elif [ ${#FAILED_SIZES[@]} -eq 0 ]; then
    echo "✓ All tests passed for all terminal sizes"
else
    echo "✗ Tests failed for the following terminal sizes: ${FAILED_SIZES[*]}"
    exit 1
fi

# Additional useful information
echo ""
echo "Useful commands:"
echo "  - View golden files: ls -la testdata/*.golden"
echo "  - Update specific golden: go test -run TestName -update"
echo "  - Run single test: go test -run TestName -v"
echo "  - View coverage: open coverage.html"

if [ "$VERBOSE" = true ]; then
    echo ""
    echo "Test artifacts:"
    if [ -f "coverage.out" ]; then
        echo "  - Coverage data: coverage.out"
    fi
    if [ -f "coverage.html" ]; then
        echo "  - Coverage report: coverage.html"
    fi
    if [ -d "testdata" ]; then
        echo "  - Golden files: $(find testdata -name "*.golden" | wc -l) files"
    fi
fi