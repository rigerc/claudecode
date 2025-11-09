#!/usr/bin/env bats

# Complex Bats Test Template
# Use this template for advanced testing scenarios with setup/teardown

# Global variables for test environment
TEST_TEMP_DIR=""
TEST_CONFIG_FILE=""
TEST_DATA_FILE=""

setup_file() {
    # This runs once before all tests in this file
    # Use for expensive setup operations

    # Load helper libraries
    load 'test_helper/bats-support/load'
    load 'test_helper/bats-assert/load'
    load 'test_helper/bats-file/load'  # if using bats-file

    # Get test directory
    DIR="$( cd "$( dirname "$BATS_TEST_FILENAME" )" >/dev/null 2>&1 && pwd )"
    PATH="$DIR/../src:$PATH"

    # Create temporary directory for tests
    TEST_TEMP_DIR=$(mktemp -d)
    export TEST_TEMP_DIR

    # Create test configuration
    TEST_CONFIG_FILE="$TEST_TEMP_DIR/test.conf"
    cat > "$TEST_CONFIG_FILE" << EOF
# Test configuration
test_mode=true
debug_level=1
EOF
    export TEST_CONFIG_FILE

    # Create test data
    TEST_DATA_FILE="$TEST_TEMP_DIR/test_data.txt"
    echo "test data line 1" > "$TEST_DATA_FILE"
    echo "test data line 2" >> "$TEST_DATA_FILE"
    export TEST_DATA_FILE
}

teardown_file() {
    # This runs once after all tests in this file
    # Clean up expensive setup
    if [[ -n "$TEST_TEMP_DIR" && -d "$TEST_TEMP_DIR" ]]; then
        rm -rf "$TEST_TEMP_DIR"
    fi
}

setup() {
    # This runs before each individual test
    # Create test-specific temporary files if needed
    CURRENT_TEST_TEMP=$(mktemp)
    export CURRENT_TEST_TEMP
}

teardown() {
    # This runs after each individual test
    # Clean up test-specific files
    if [[ -n "$CURRENT_TEST_TEMP" && -f "$CURRENT_TEST_TEMP" ]]; then
        rm -f "$CURRENT_TEST_TEMP"
    fi
}

@test "script works with configuration file" {
    run your_script.sh --config "$TEST_CONFIG_FILE"
    assert_success
    assert_output --partial "Configuration loaded"
}

@test "script processes data correctly" {
    run your_script.sh --input "$TEST_DATA_FILE"
    assert_success
    assert_output --partial "Processing complete"
}

@test "script handles invalid configuration" {
    run your_script.sh --config "/nonexistent/config"
    assert_failure
    assert_output --partial "Configuration not found"
}

@test "script creates output files" {
    output_file="$TEST_TEMP_DIR/output.txt"
    run your_script.sh --output "$output_file"
    assert_success
    assert_file_exists "$output_file"
}

@test "script handles multiple test runs" {
    # First run
    run your_script.sh --mode test
    assert_success

    # Second run (should not fail due to leftover state)
    run your_script.sh --mode test
    assert_success

    # Verify no conflicting output
    refute_output --partial "error"
}