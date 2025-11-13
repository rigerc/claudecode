# Bats Testing Patterns

## Basic Test Structure

```bash
#!/usr/bin/env bats

@test "test description" {
  # test code here
  [ condition ]
}
```

## Running Commands

### Using `run`

The `run` command captures exit status and output:

```bash
@test "command succeeds" {
  run ./my_script.sh
  [ "$status" -eq 0 ]
}

@test "command fails" {
  run ./failing_script.sh
  [ "$status" -ne 0 ]
}

@test "command produces output" {
  run echo "hello world"
  [ "$output" = "hello world" ]
}
```

## Basic Assertions

### Exit Status

```bash
@test "function returns correct value" {
  result=$(my_function)
  [ "$result" = "expected" ]
}

@test "command fails with specific exit code" {
  run failing_command
  [ "$status" -eq 1 ]
}
```

### String Comparison

```bash
@test "exact string match" {
  run ./script.sh
  [ "$output" = "exact output" ]
}

@test "partial string match" {
  run ./script.sh
  [[ "$output" == *"substring"* ]]
}

@test "output starts with" {
  run ./script.sh
  [[ "$output" == "prefix"* ]]
}
```

## Using bats-assert

When you load `bats-assert`, you get cleaner assertions:

```bash
load 'test_helper/bats-assert/load'

@test "using assert helpers" {
  run ./script.sh
  assert_success
  assert_output "expected output"
}

@test "partial output matching" {
  run ./script.sh
  assert_output --partial "substring"
}

@test "regex matching" {
  run ./script.sh
  assert_output --regexp "^line [0-9]+$"
}

@test "checking lines" {
  run ./script.sh
  assert_line "first line"
  assert_line --index 0 "first line"
  assert_line --partial "partial match"
}
```

## Setup and Teardown

### Test-Level

Runs before/after each test:

```bash
setup() {
  # Runs before each @test
  export TEST_VAR="test_value"
  mkdir -p /tmp/test_dir
}

teardown() {
  # Runs after each @test
  rm -rf /tmp/test_dir
  unset TEST_VAR
}

@test "uses setup values" {
  [ "$TEST_VAR" = "test_value" ]
  [ -d /tmp/test_dir ]
}
```

### File-Level

Runs once per file:

```bash
setup_file() {
  # Runs once before all tests in file
  export SHARED_RESOURCE="value"
}

teardown_file() {
  # Runs once after all tests in file
  unset SHARED_RESOURCE
}
```

## Testing Files

```bash
@test "file exists" {
  [ -f /path/to/file ]
}

@test "directory exists" {
  [ -d /path/to/dir ]
}

@test "file is executable" {
  [ -x /path/to/script ]
}

@test "file contains text" {
  run grep "pattern" /path/to/file
  [ "$status" -eq 0 ]
}
```

## Skipping Tests

```bash
@test "work in progress" {
  skip "not implemented yet"
  # test code
}

@test "platform specific" {
  if [[ "$OSTYPE" != "linux-gnu"* ]]; then
    skip "only runs on Linux"
  fi
  # test code
}
```
