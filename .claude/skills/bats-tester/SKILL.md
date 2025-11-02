---
name: bats-tester
description: This skill should be used when creating tests for bash scripts using the bats-core testing framework. It provides guidance for writing effective .bats test files, setting up test environments, using helper libraries like bats-support and bats-assert, and following best practices for bash script testing. Use this skill when users need to create automated tests for shell scripts, command-line tools, or bash functions.
---

# Bats Tester

## Overview

This skill enables the creation of comprehensive tests for bash scripts using the bats-core framework. It provides templates, best practices, and workflows for setting up test environments, writing test cases, and organizing test suites effectively.

## Quick Start

To create a basic bats test file for a bash script:

1. Set up the project structure with bats-core as a git submodule
2. Create a `.bats` test file with proper setup functions
3. Write test cases using `@test` syntax
4. Use helper libraries for assertions and utilities

Use the templates in `assets/` as starting points for common test patterns.

## Test Creation Workflow

### 1. Project Setup

Create the recommended directory structure:
```
src/
    script.sh
test/
    bats/               <- git submodule
    test_helper/
        bats-support/   <- git submodule
        bats-assert/    <- git submodule
    test.bats
```

Initialize git submodules:
```bash
git submodule add https://github.com/bats-core/bats-core.git test/bats
git submodule add https://github.com/bats-core/bats-support.git test/test_helper/bats-support
git submodule add https://github.com/bats-core/bats-assert.git test/test_helper/bats-assert
```

### 2. Test File Structure

Use the standard setup pattern to make scripts accessible via PATH:
```bash
setup() {
    load 'test_helper/bats-support/load'
    load 'test_helper/bats-assert/load'

    DIR="$( cd "$( dirname "$BATS_TEST_FILENAME" )" >/dev/null 2>&1 && pwd )"
    PATH="$DIR/../src:$PATH"
}
```

### 3. Writing Test Cases

Use the `run` command to execute scripts and capture output:
```bash
@test "script shows welcome message" {
    run script.sh
    assert_output --partial 'Welcome'
    assert_success
}
```

### 4. Cleanup

Implement teardown functions to clean up test artifacts:
```bash
teardown() {
    rm -f /tmp/test-artifact-file
}
```

## Common Test Patterns

### Testing Command Output
Use `assert_output` for exact matches, `assert_output --partial` for substring matching, and `refute_output` to ensure output doesn't contain specific text.

### Testing Exit Codes
Use `assert_success` to check for exit code 0, `assert_failure` for non-zero exit codes, or check specific codes with `assert_equal $status 1`.

### Testing File Operations
Use the bats-file helper library for file-based assertions, or create temporary files with `mktemp` in setup functions.

### Testing Error Conditions
Redirect stderr to stdout with `2>&1` when testing error messages, or use `run` separately to capture both streams.

## Best Practices

1. **Always use setup()** to establish PATH and load helper libraries
2. **Prefer partial matching** with `--partial` when output format might vary
3. **Use teardown()** to clean up temporary files and processes
4. **Group related tests** in the same .bats file when they share setup
5. **Use descriptive test names** that explain what is being tested
6. **Handle environment dependencies** with `skip` when required tools are missing

## Resources

This skill includes specialized resources for bats-core testing:

### scripts/
Automation scripts for test setup and management:

- `setup_test_project.sh` - Initialize a new project with bats-core submodules
- `run_tests.sh` - Execute test suites with proper environment setup
- `generate_test_template.py` - Create test file templates based on script analysis

### references/
Comprehensive documentation for test development:

- `bats_functions.md` - Complete reference of bats-core built-in functions
- `assertion_patterns.md` - Common assertion patterns and examples
- `test_organization.md` - Guidelines for structuring test suites
- `troubleshooting.md` - Common issues and solutions

### assets/
Templates and boilerplate files for quick test creation:

- `basic_test_template.bats` - Template for simple script tests
- `complex_test_template.bats` - Template with advanced setup/teardown
- `common_setup.bash` - Reusable setup functions
- `project_structure/` - Example directory layouts

---

**Note:** These resources provide ready-to-use templates and comprehensive guidance for bats-core testing scenarios.
