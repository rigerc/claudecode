# Bats Testing Setup Guide

## Project Structure

The recommended structure for bats tests:

```
test/
├── bats/              <- git submodule (bats-core)
├── test_helper/
│   ├── bats-support/  <- git submodule
│   └── bats-assert/   <- git submodule
└── test.bats          <- your test files
```

## Installation

### Using Git Submodules

Initialize bats-core and helper libraries as git submodules:

```bash
# Add bats-core
git submodule add https://github.com/bats-core/bats-core.git test/bats

# Add bats-support (test helpers)
git submodule add https://github.com/bats-core/bats-support.git test/test_helper/bats-support

# Add bats-assert (assertion helpers)
git submodule add https://github.com/bats-core/bats-assert.git test/test_helper/bats-assert

# Initialize and update submodules
git submodule update --init --recursive
```

### Loading Helpers in Tests

At the top of your `.bats` files:

```bash
#!/usr/bin/env bats

# Load bats-support and bats-assert
load 'test_helper/bats-support/load'
load 'test_helper/bats-assert/load'

# Now you can use assert_success, assert_output, etc.
```

## Running Tests

### Basic Execution

```bash
# Run all tests
test/bats/bin/bats test/

# Run specific test file
test/bats/bin/bats test/my_test.bats

# Run with verbose output
test/bats/bin/bats -t test/

# Run with timing information
test/bats/bin/bats --timing test/
```

### CI/CD Integration

Example GitHub Actions workflow:

```yaml
name: Test
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
        with:
          submodules: recursive
      - name: Run tests
        run: test/bats/bin/bats test/
```
