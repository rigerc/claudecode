#!/usr/bin/env bats

# Basic Bats Test Template
# Use this template for simple script testing scenarios

setup() {
    # Load helper libraries
    load 'test_helper/bats-support/load'
    load 'test_helper/bats-assert/load'

    # Get the directory containing this test file
    DIR="$( cd "$( dirname "$BATS_TEST_FILENAME" )" >/dev/null 2>&1 && pwd )"

    # Add src directory to PATH so scripts can be called without relative paths
    PATH="$DIR/../src:$PATH"
}

teardown() {
    # Clean up any temporary files created during tests
    # Add cleanup commands here as needed
    :
}

@test "script runs successfully" {
    run your_script.sh
    assert_success
}

@test "script produces expected output" {
    run your_script.sh
    assert_output --partial "expected message"
}

@test "script handles missing arguments" {
    run your_script.sh
    assert_failure
    assert_output --partial "Usage:"
}