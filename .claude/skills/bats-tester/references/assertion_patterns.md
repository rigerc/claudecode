# Common Assertion Patterns

This document provides common assertion patterns for testing bash scripts with bats-core and helper libraries.

## Bats-Assert Assertions

### Output Assertions

#### `assert_output [expected]`
Assert that command output matches expected string.

**Usage:**
```bash
@test "script outputs exact message" {
    run script.sh
    assert_output "Hello, World!"
}
```

#### `assert_output --partial <substring>`
Assert that output contains expected substring.

**Usage:**
```bash
@test "script contains welcome message" {
    run script.sh
    assert_output --partial "Welcome"
}
```

#### `assert_output --regexp <pattern>`
Assert that output matches regular expression.

**Usage:**
```bash
@test "script outputs valid timestamp" {
    run script.sh
    assert_output --regexp '[0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2}'
}
```

#### `assert_output [line_number] <expected>`
Assert that specific line matches expected content.

**Usage:**
```bash
@test "script outputs correct header" {
    run script.sh
    assert_output 1 "Header Title"
}
```

#### `refute_output [expected]`
Assert that output does NOT match expected string.

**Usage:**
```bash
@test "script does not contain error message" {
    run script.sh
    refute_output "Error occurred"
}
```

#### `refute_output --partial <substring>`
Assert that output does NOT contain substring.

**Usage:**
```bash
@test "script does not contain debug info" {
    run script.sh
    refute_output --partial "DEBUG:"
}
```

### Exit Code Assertions

#### `assert_success`
Assert that command succeeded (exit code 0).

**Usage:**
```bash
@test "script executes successfully" {
    run script.sh
    assert_success
}
```

#### `assert_failure`
Assert that command failed (non-zero exit code).

**Usage:**
```bash
@test "script fails with invalid input" {
    run script.sh --invalid
    assert_failure
}
```

#### `assert_equal <actual> <expected>`
Assert that two values are equal.

**Usage:**
```bash
@test "script returns correct exit code" {
    run script.sh
    assert_equal "$status" 2
}
```

## Bats-Support Assertions

### Status Assertions

#### `assert_status_is <expected_status>`
Assert that command exited with specific status code.

**Usage:**
```bash
@test "script exits with status 1 on error" {
    run script.sh --error
    assert_status_is 1
}
```

#### `assert_status_success`
Alias for `assert_success`.

#### `assert_status_failure`
Alias for `assert_failure`.

### Line Assertions

#### `assert_line <line_number> <expected>`
Assert that specific line contains expected content.

**Usage:**
```bash
@test "script outputs specific line" {
    run script.sh
    assert_line 1 "Starting process..."
}
```

#### `assert_line_count <expected_count>`
Assert that output has specific number of lines.

**Usage:**
```bash
@test "script outputs exactly 3 lines" {
    run script.sh
    assert_line_count 3
}
```

## Common Test Patterns

### Testing Command Success/Failure

```bash
@test "command succeeds with valid input" {
    run command.sh --valid-input
    assert_success
    assert_output --partial "Operation completed"
}

@test "command fails with invalid input" {
    run command.sh --invalid-input
    assert_failure
    assert_output --partial "Invalid input"
}
```

### Testing File Operations

```bash
@test "script creates output file" {
    output_file="$BATS_TMPDIR/output.txt"
    run script.sh --output "$output_file"
    assert_success
    assert_file_exists "$output_file"
}

@test "script handles missing input file" {
    run script.sh --input "/nonexistent/file.txt"
    assert_failure
    assert_output --partial "File not found"
}
```

### Testing Script Arguments

```bash
@test "script shows help with --help" {
    run script.sh --help
    assert_success
    assert_output --partial "Usage:"
}

@test "script requires mandatory argument" {
    run script.sh
    assert_failure
    assert_output --partial "Missing required argument"
}
```

### Testing Configuration File Handling

```bash
@test "script loads configuration file" {
    config_file="$BATS_TMPDIR/config.conf"
    echo "setting=value" > "$config_file"
    run script.sh --config "$config_file"
    assert_success
    assert_output --partial "Configuration loaded"
}

@test "script handles missing configuration" {
    run script.sh --config "/nonexistent/config"
    assert_failure
    assert_output --partial "Configuration file not found"
}
```

### Testing Output Formats

```bash
@test "script outputs valid JSON" {
    run script.sh --format json
    assert_success

    # Verify output is valid JSON
    echo "$output" | jq . >/dev/null
    assert_success
}

@test "script outputs CSV format" {
    run script.sh --format csv
    assert_success
    assert_output --regexp "^[^,]+,[^,]+,[^,]+$"
}
```

### Testing Network Operations

```bash
@test "script connects to service" {
    run script.sh --host "localhost" --port 8080
    assert_success
    assert_output --partial "Connected to service"
}

@test "script handles connection failure" {
    run script.sh --host "nonexistent" --port 9999
    assert_failure
    assert_output --partial "Connection failed"
}
```

### Testing Database Operations

```bash
@test "script creates database table" {
    db_file="$BATS_TMPDIR/test.db"
    run script.sh --db "$db_file" --create-table
    assert_success

    # Verify table exists
    sqlite3 "$db_file" "SELECT name FROM sqlite_master WHERE type='table'" | grep -q "test_table"
    assert_success
}
```

### Testing Multiple Scenarios

```bash
@test "script handles multiple input formats" {
    # Test with file input
    input_file="$BATS_TMPDIR/input.txt"
    echo "test data" > "$input_file"
    run script.sh --input "$input_file"
    assert_success
    assert_output --partial "Processed file input"

    # Test with stdin input
    echo "test data" | run script.sh --input -
    assert_success
    assert_output --partial "Processed stdin input"
}
```

## Error Message Testing

### Testing Specific Error Messages

```bash
@test "script shows clear error for invalid option" {
    run script.sh --invalid-option
    assert_failure
    assert_output "Invalid option: --invalid-option"
    assert_output --partial "Use --help for usage information"
}
```

### Testing Error Code Specificity

```bash
@test "script returns different codes for different errors" {
    # Test missing file error
    run script.sh --input "/missing/file"
    assert_equal "$status" 2

    # Test permission error
    touch "$BATS_TMPDIR/readonly.txt"
    chmod 444 "$BATS_TMPDIR/readonly.txt"
    run script.sh --input "$BATS_TMPDIR/readonly.txt"
    assert_equal "$status" 3
}
```

## Performance Testing

### Timing Assertions

```bash
@test "script completes within time limit" {
    start_time=$(date +%s)
    run script.sh --large-input
    end_time=$(date +%s)

    duration=$((end_time - start_time))
    assert_success
    assert [ "$duration" -lt 30 ]  # Should complete in less than 30 seconds
}
```

### Memory Usage Testing

```bash
@test "script does not exceed memory limit" {
    run timeout 30s script.sh --memory-intensive
    assert_success

    # Check if process was killed due to memory (simplified)
    assert refute_output --partial "Killed"
}
```

## Best Practices

1. **Use descriptive test names** that explain what is being tested
2. **Test one behavior per test** - avoid testing multiple scenarios in one test
3. **Use partial matching** when exact output format might vary
4. **Test both success and failure** scenarios
5. **Clean up resources** in teardown functions
6. **Use temporary files** instead of hardcoding paths
7. **Make tests independent** - they should not depend on each other
8. **Test edge cases** like empty input, special characters, large inputs