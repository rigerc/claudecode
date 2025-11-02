#!/usr/bin/env bash

# Common Setup Functions for Bats Tests
# Source this file in your test files to reuse common setup patterns

# Standard setup function with helper libraries
standard_setup() {
    local project_root="${1:-$BATS_TEST_DIRNAME/..}"

    # Load helper libraries
    load 'test_helper/bats-support/load'
    load 'test_helper/bats-assert/load'

    # Add scripts to PATH
    PATH="$project_root/src:$PATH"

    # Export common variables
    export PROJECT_ROOT="$project_root"
    export TEST_TEMP_DIR=$(mktemp -d)
}

# Setup with file operations support
file_setup() {
    local project_root="${1:-$BATS_TEST_DIRNAME/..}"

    # Standard setup
    standard_setup "$project_root"

    # Load file operations helper
    load 'test_helper/bats-file/load'

    # Create common test files
    export TEST_FILE="$TEST_TEMP_DIR/test.txt"
    echo "test content" > "$TEST_FILE"
}

# Setup for network/service testing
service_setup() {
    local project_root="${1:-$BATS_TEST_DIRNAME/..}"

    # Standard setup
    standard_setup "$project_root"

    # Find available port for testing
    export TEST_PORT=$(python3 -c 'import socket; s=socket.socket(); s.bind(("",0)); print(s.getsockname()[1]); s.close()')

    # Export service-related variables
    export TEST_SERVICE_PID=""
    export TEST_SERVICE_URL="http://localhost:$TEST_PORT"
}

# Setup for database testing
database_setup() {
    local project_root="${1:-$BATS_TEST_DIRNAME/..}"

    # Standard setup
    standard_setup "$project_root"

    # Create temporary database
    export TEST_DB="$TEST_TEMP_DIR/test.db"

    # Skip tests if sqlite3 is not available
    if ! command -v sqlite3 &> /dev/null; then
        skip "sqlite3 is required for database tests"
    fi
}

# Common teardown function
standard_teardown() {
    # Clean up temporary directory
    if [[ -n "$TEST_TEMP_DIR" && -d "$TEST_TEMP_DIR" ]]; then
        rm -rf "$TEST_TEMP_DIR"
    fi

    # Stop any running services
    if [[ -n "$TEST_SERVICE_PID" ]]; then
        kill "$TEST_SERVICE_PID" 2>/dev/null || true
    fi
}

# Helper function to check if command exists
command_exists() {
    command -v "$1" &> /dev/null
}

# Helper function to create test data
create_test_data() {
    local file="$1"
    local content="$2"

    mkdir -p "$(dirname "$file")"
    echo "$content" > "$file"
}

# Helper function to wait for service to be ready
wait_for_service() {
    local url="$1"
    local max_attempts="${2:-30}"
    local attempt=1

    while [[ $attempt -le $max_attempts ]]; do
        if curl -s "$url" &> /dev/null; then
            return 0
        fi
        sleep 1
        ((attempt++))
    done

    return 1
}