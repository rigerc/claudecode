# Bats-Core Functions Reference

This document provides a comprehensive reference of bats-core built-in functions and special variables.

## Core Functions

### `run <command>`
Execute a command and capture its output and exit status.

**Usage:**
```bash
run your_script.sh arg1 arg2
```

**Special Variables Set:**
- `$status` - Exit code of the command
- `$output` - Combined stdout and stderr of the command

**Note:** `run` always returns 0, so test failures must be checked with assertions.

### `load <path>`
Load a bats helper library or external bash file.

**Usage:**
```bash
load 'test_helper/bats-support/load'
load 'test_helper/bats-assert/load'
```

**Behavior:** Automatically appends `.bash` extension if not present.

### `skip [reason]`
Skip the current test with an optional reason.

**Usage:**
```bash
if ! command -v docker &> /dev/null; then
    skip "docker is not available"
fi
```

## Setup and Teardown Functions

### `setup()`
Function called before each individual test.

**Usage:**
```bash
setup() {
    # Load helper libraries
    load 'test_helper/bats-support/load'

    # Set up test environment
    export TEST_VAR="value"
}
```

### `teardown()`
Function called after each individual test, regardless of success or failure.

**Usage:**
```bash
teardown() {
    # Clean up temporary files
    rm -f /tmp/test_file
}
```

### `setup_file()`
Function called once before all tests in a file.

**Usage:**
```bash
setup_file() {
    # Start a service that will be used by all tests
    start_test_service &
    export SERVICE_PID=$!
}
```

### `teardown_file()`
Function called once after all tests in a file, even if tests fail.

**Usage:**
```bash
teardown_file() {
    # Stop the service
    kill "$SERVICE_PID" 2>/dev/null || true
}
```

## Special Variables

### `$BATS_TEST_FILENAME`
Path to the current test file.

**Usage:**
```bash
DIR="$( cd "$( dirname "$BATS_TEST_FILENAME" )" >/dev/null 2>&1 && pwd )"
```

### `$BATS_TEST_DESCRIPTION`
Description/name of the current test.

### `$BATS_TEST_NUMBER`
Sequence number of the current test.

### `$BATS_TMPDIR`
Temporary directory for the current test run.

## Test Definition

### `@test "description" { ... }`
Define a test case with a description.

**Usage:**
```bash
@test "script shows welcome message" {
    run script.sh
    assert_output --partial "Welcome"
}
```

**Best Practices:**
- Use descriptive test names that explain what is being tested
- Focus on one behavior per test
- Use consistent naming conventions

## Command Line Options

### Common Bats Options

- `--formatter <formatter>` - Specify output formatter (junit, tap, pretty)
- `--jobs <n>` - Run tests in parallel (default: number of CPU cores)
- `--timing` - Show timing information for each test
- `--verbose-run` - Show output of failed `run` commands
- `-r` - Recursive test discovery

**Example:**
```bash
./test/bats/bin/bats --formatter junit test/
./test/bats/bin/bats --jobs 4 --timing test/
```

## Environment Variables

### `BATS_TMPDIR`
Override the temporary directory used by bats.

**Usage:**
```bash
export BATS_TMPDIR=/custom/temp/dir
./test/bats/bin/bats test/
```

### `BATS_CWD_TMPDIR`
Create temporary directory in current working directory.

## File Organization Patterns

### Single Test File
```bash
test/
├── bats/
├── test_helper/
│   ├── bats-support/
│   └── bats-assert/
└── script_test.bats
```

### Multiple Test Files
```bash
test/
├── bats/
├── test_helper/
│   ├── common-setup.bash
│   ├── bats-support/
│   └── bats-assert/
├── unit/
│   ├── function1_test.bats
│   └── function2_test.bats
├── integration/
│   └── workflow_test.bats
└── end_to_end/
    └── full_scenario_test.bats
```

## Error Handling

### Debugging Failed Tests

1. **Use `--verbose-run`** to see output of failed commands:
   ```bash
   ./test/bats/bin/bats --verbose-run test/
   ```

2. **Check temporary files** in `$BATS_TMPDIR` for debugging information.

3. **Add debug output** in tests:
   ```bash
   @test "debug test" {
       echo "Debug info: $VAR" >&3
       run command
   }
   ```

### Common Pitfalls

1. **Forgetting `run`**: Without `run`, command failures will immediately fail the test.
2. **PATH issues**: Always ensure scripts are accessible via PATH or use full paths.
3. **File permissions**: Make sure test scripts have execute permissions.
4. **Timing issues**: Use sleep or wait mechanisms when testing async operations.