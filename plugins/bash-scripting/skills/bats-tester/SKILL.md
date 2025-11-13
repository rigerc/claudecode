---
name: bats-tester
description: Use PROACTIVELY when creating tests for bash scripts using the bats-core testing framework. MUST BE USED for any bats-core related tasks including writing .bats test files, setting up test environments, and following best practices for bash script testing.
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
  - TodoWrite
---

# Bats Tester

## Quick Start

Create basic bats test for `script.sh`:

```bash
#!/usr/bin/env bats

@test "script runs successfully" {
  run ./script.sh
  [ "$status" -eq 0 ]
}

@test "script produces expected output" {
  run ./script.sh arg1
  [ "$status" -eq 0 ]
  [[ "$output" == *"expected"* ]]
}
```

## Project Structure

```
test/
├── bats/              <- git submodule
├── test_helper/
│   ├── bats-support/  <- git submodule
│   └── bats-assert/   <- git submodule
└── test.bats
```

Initialize with:
```bash
git submodule add https://github.com/bats-core/bats-core.git test/bats
git submodule add https://github.com/bats-core/bats-support.git test/test_helper/bats-support
git submodule add https://github.com/bats-core/bats-assert.git test/test_helper/bats-assert
```

## Testing Patterns

### Basic Assertions
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

### Setup and Teardown
```bash
setup() {
  export TEST_VAR="test_value"
}

teardown() {
  rm -f /tmp/test_file
}
```

Run tests with: `test/bats/bin/bats test/`

For detailed examples and advanced patterns, see `references/detailed-guide.md`.