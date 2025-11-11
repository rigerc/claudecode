---
name: bats-tester
description: Use PROACTIVELY when creating tests for bash scripts using the bats-core testing framework. MUST BE USED for any bats-core related tasks including writing .bats test files, setting up test environments, using helper libraries like bats-support and bats-assert, and following best practices for bash script testing. This skill provides comprehensive guidance for automated testing of shell scripts, command-line tools, or bash functions.
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

## Troubleshooting

### Setup and Installation Issues

**Problem**: Git submodules not found or not working
- **Cause**: Submodules not initialized or updated
- **Solution**: Run `git submodule update --init --recursive`
- **Verify**: Check that `test/bats/bin/bats` exists and is executable

**Problem**: Helper libraries (bats-support, bats-assert) not loading
- **Cause**: Incorrect path in load statements or missing submodules
- **Solution**: Verify submodule paths and use absolute paths if needed
- **Debug**: Add `echo "Loading from: $(pwd)"` in setup() to check paths

**Problem**: Scripts not found in PATH during tests
- **Cause**: PATH not correctly set in setup() function
- **Solution**: Verify DIR calculation and PATH modification
- **Check**: Use `which script_name` in test to verify PATH

### Test Execution Issues

**Problem**: Tests failing with "command not found" errors
- **Cause**: Script dependencies not installed or PATH issues
- **Solution**: Install required dependencies and verify PATH setup
- **Debug**: Add `type -a command_name` to test availability

**Problem**: Tests passing when they should fail
- **Cause**: Missing assertion checks or incorrect test logic
- **Solution**: Add proper assertions and verify test conditions
- **Review**: Ensure each test has explicit assertions

**Problem**: Tests failing with permission denied errors
- **Cause**: Scripts not executable or file permission issues
- **Solution**: Run `chmod +x` on scripts and test files
- **Check**: Verify permissions with `ls -la` on test files

### Assertion and Output Issues

**Problem**: `assert_output` failing due to whitespace differences
- **Cause**: Exact matching when output formatting varies
- **Solution**: Use `--partial` matching or normalize output
- **Fix**: Trim whitespace with `echo "$output" | tr -d '[:space:]'`

**Problem**: Tests failing due to colored output or formatting
- **Cause**: Scripts outputting ANSI color codes or formatting
- **Solution**: Disable colors in test environment or strip formatting
- **Fix**: Use command flags like `--no-color` when available

**Problem**: `assert_success` failing for scripts that exit with 0
- **Cause**: Hidden command in test returning non-zero exit code
- **Solution**: Check all commands in test for proper exit codes
- **Debug**: Add `echo "Status: $status"` before assertions

### Environment and Dependency Issues

**Problem**: Tests only work in specific directories
- **Cause**: Hardcoded paths or relative path assumptions
- **Solution**: Use absolute paths and `$BATS_TEST_DIRNAME`
- **Best Practice**: Always calculate paths relative to test file location

**Problem**: Tests failing on different systems or shells
- **Cause**: Platform-specific commands or shell differences
- **Solution**: Use portable commands and test compatibility
- **Check**: Verify required tools exist with `command -v`

**Problem**: Tests creating files that persist between runs
- **Cause**: Missing cleanup in teardown functions
- **Solution**: Implement proper teardown to remove test artifacts
- **Pattern**: Use temporary files in `/tmp` with unique names

### Performance and Timing Issues

**Problem**: Tests running slowly or timing out
- **Cause**: Inefficient operations or external dependencies
- **Solution**: Optimize test operations and mock external calls
- **Monitor**: Use `time` command to identify slow tests

**Problem**: Race conditions in tests
- **Cause**: Concurrent operations or timing dependencies
- **Solution**: Add proper synchronization and waiting
- **Fix**: Use sleep or polling for async operations

### Debugging Techniques

**Enable Verbose Output**
```bash
# Run with verbose output
test/bats/bin/bats -v test/test.bats

# Run with detailed output
test/bats/bin/bats --verbose-run test/test.bats

# Run single test with debugging
test/bats/bin/bats --filter "specific test name" test/test.bats
```

**Debug Variables and Paths**
```bash
# Add to setup() for debugging
setup() {
    echo "BATS_TEST_FILENAME: $BATS_TEST_FILENAME"
    echo "BATS_TEST_DIRNAME: $BATS_TEST_DIRNAME"
    echo "PATH: $PATH"
    echo "PWD: $(pwd)"
}
```

**Check Helper Functions**
```bash
# Test helper library loading
@test "helper libraries loaded" {
    assert [ -n "$ bats_install_prefix" ]  # Check if bats-support is loaded
}
```

### Common Error Messages and Solutions

**"bats: command not found"**
- Install bats-core or use submodule approach
- Check PATH includes bats binary location
- Verify executable permissions on bats binary

**"load: command not found"**
- Ensure using proper bats syntax (inside @test functions)
- Check that helper libraries are properly installed
- Verify file paths in load statements

**"assert_success: command not found"**
- Ensure bats-assert helper library is loaded
- Check that load statement comes before test functions
- Verify submodule is properly initialized

**"No such file or directory" for script paths**
- Verify PATH setup in setup() function
- Check that script files exist and are executable
- Use absolute paths for debugging

### Getting Help

1. **Check skill references**: `references/troubleshooting.md`
2. **Review official docs**: bats-core documentation on GitHub
3. **Test setup script**: Use `scripts/setup_test_project.sh`
4. **Examine templates**: Compare with working examples in `assets/`
5. **Community resources**: bats-core GitHub issues and discussions

## Performance Considerations

### Test Execution Performance

**Optimize Test Suite Speed**
- Use `setup()` and `teardown()` efficiently to minimize repeated operations
- Group related tests that share setup requirements
- Avoid expensive operations (network calls, large file operations) in tests
- Use mocking for external dependencies when possible

**Parallel Test Execution**
- Bats-core supports parallel execution with `--jobs` flag
- Design tests to be independent and avoid shared state
- Use unique temporary file names to prevent conflicts
- Consider test isolation when running in parallel

**Reduce Test Overhead**
- Minimize use of external commands in test loops
- Cache expensive operations in setup() when possible
- Use built-in bash operations instead of external tools
- Avoid unnecessary file I/O operations

### Memory and Resource Management

**Efficient File Handling**
- Use temporary files in `/tmp` with unique names
- Clean up resources promptly in teardown() functions
- Avoid accumulating large files during test execution
- Use file descriptors efficiently and close them properly

**Process Management**
- Kill background processes started during tests
- Use proper process cleanup in teardown functions
- Monitor for zombie processes or orphaned resources
- Limit the number of concurrent processes in tests

**Memory Usage Patterns**
- Avoid loading large datasets into memory
- Process files incrementally when possible
- Clean up variables that hold large data structures
- Monitor memory usage in long-running test suites

### Large Test Suite Management

**Test Organization for Performance**
- Split large test suites into multiple .bats files
- Use descriptive naming to organize tests by functionality
- Consider test execution time when organizing test groups
- Implement test skipping mechanisms for expensive operations

**Selective Test Execution**
- Use `--filter` to run specific tests during development
- Tag tests by type (unit, integration, performance)
- Implement test categories for different execution scenarios
- Use environment variables to control test scope

**Continuous Integration Optimization**
- Cache test dependencies between CI runs
- Parallelize test execution across multiple runners
- Use test result caching when code hasn't changed
- Implement incremental testing strategies

### Profiling and Monitoring

**Test Execution Time Analysis**
```bash
# Time individual tests
test/bats/bin/bats --timing test/test.bats

# Profile test execution
time test/bats/bin/bats test/test.bats

# Identify slow tests
test/bats/bin/bats --formatter tap test/test.bats | grep "^ok" | sort -k3 -n
```

**Resource Usage Monitoring**
```bash
# Monitor memory usage during tests
/usr/bin/time -v test/bats/bin/bats test/test.bats

# Track file descriptor usage
lsof -p $(pgrep -f "test/bats") | wc -l

# Monitor process creation
ps aux | grep -c bats
```

**Performance Benchmarking**
- Establish baseline performance metrics
- Track test execution time over time
- Monitor resource usage patterns
- Set performance alerts for degrading test times

### Best Practices for High Performance

1. **Minimize External Dependencies**: Reduce reliance on external commands and services
2. **Use Efficient Data Structures**: Choose appropriate bash data structures and algorithms
3. **Implement Proper Cleanup**: Ensure resources are released promptly
4. **Design for Parallel Execution**: Write tests that can run safely in parallel
5. **Monitor Performance Metrics**: Track execution time and resource usage
6. **Optimize Critical Paths**: Focus optimization efforts on frequently executed code

### Performance Anti-Patterns

**Avoid These Common Issues**:
- Expensive operations in setup/teardown that run repeatedly
- Tests that depend on execution order or shared state
- Large file operations in tight loops
- External network calls without proper mocking
- Memory leaks from unclosed file descriptors or processes

**Replace With Better Patterns**:
- Use lazy loading for expensive resources
- Design independent, isolated tests
- Process data incrementally rather than loading all at once
- Mock external dependencies for fast, reliable tests
- Implement comprehensive resource cleanup

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
