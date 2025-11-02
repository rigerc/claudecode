# Test Organization Guidelines

This document provides guidelines for organizing bats-core test suites effectively.

## Directory Structure

### Basic Project Structure
```
project/
├── src/
│   ├── script1.sh
│   ├── script2.sh
│   └── lib/
│       └── helper_functions.sh
├── test/
│   ├── bats/                     # git submodule
│   ├── test_helper/
│   │   ├── bats-support/         # git submodule
│   │   ├── bats-assert/          # git submodule
│   │   └── common-setup.bash     # shared setup functions
│   ├── unit/
│   │   ├── script1_test.bats
│   │   └── script2_test.bats
│   ├── integration/
│   │   └── workflow_test.bats
│   └── fixtures/
│       ├── sample_input.txt
│       └── expected_output.txt
└── README.md
```

### Advanced Project Structure
```
project/
├── src/
├── test/
│   ├── bats/
│   ├── test_helper/
│   │   ├── common/
│   │   │   ├── setup.bash
│   │   │   ├── assertions.bash
│   │   │   └── utilities.bash
│   │   └── external/
│   │       ├── bats-support/
│   │       ├── bats-assert/
│   │       └── bats-file/
│   ├── unit/
│   │   ├── core_functions_test.bats
│   │   ├── utilities_test.bats
│   │   └── error_handling_test.bats
│   ├── integration/
│   │   ├── api_integration_test.bats
│   │   ├── database_integration_test.bats
│   │   └── file_operations_test.bats
│   ├── end_to_end/
│   │   ├── user_workflows_test.bats
│   │   └── regression_test.bats
│   ├── performance/
│   │   ├── load_test.bats
│   │   └── memory_test.bats
│   ├── fixtures/
│   │   ├── data/
│   │   │   ├── small_dataset.json
│   │   │   ├── large_dataset.json
│   │   │   └── corrupted_dataset.json
│   │   ├── configs/
│   │   │   ├── valid_config.conf
│   │   │   ├── invalid_config.conf
│   │   │   └── empty_config.conf
│   │   └── scripts/
│   │       ├── setup_test_env.sh
│   │       └── cleanup_test_env.sh
│   └── lib/
│       ├── test_utilities.bash
│       ├── mock_services.bash
│       └── data_generators.bash
└── Makefile
```

## Test Categories

### Unit Tests
Test individual functions and small pieces of functionality in isolation.

**Characteristics:**
- Fast execution
- No external dependencies
- Focus on single function/script behavior
- Use mocks and stubs when necessary

**Example file naming:**
- `function_name_test.bats`
- `script_name_unit_test.bats`

### Integration Tests
Test how multiple components work together.

**Characteristics:**
- Test interaction between scripts
- May use external services/databases
- Focus on data flow and interfaces
- Slower than unit tests

**Example file naming:**
- `api_integration_test.bats`
- `database_integration_test.bats`
- `workflow_test.bats`

### End-to-End Tests
Test complete user scenarios from start to finish.

**Characteristics:**
- Test entire workflows
- Use real environments
- Focus on user requirements
- Slowest test category

**Example file naming:**
- `user_registration_test.bats`
- `data_processing_pipeline_test.bats`
- `backup_restore_test.bats`

### Performance Tests
Test system performance under various conditions.

**Characteristics:**
- Measure timing, memory usage
- Test with large datasets
- Focus on performance requirements
- May be run separately

**Example file naming:**
- `load_test.bats`
- `memory_usage_test.bats`
- `stress_test.bats`

## File Naming Conventions

### Test Files
- Use `.bats` extension for all test files
- Use descriptive names ending with `_test.bats`
- Use snake_case for file names
- Include the component being tested in the name

**Good examples:**
- `user_authentication_test.bats`
- `file_upload_test.bats`
- `data_validation_test.bats`

**Avoid:**
- `test1.bats`
- `temp.bats`
- `tests.bats`

### Helper Files
- Use `.bash` extension for helper scripts
- Include purpose in the name
- Group related helpers in subdirectories

**Examples:**
- `common/setup.bash`
- `test_helper/assertions.bash`
- `lib/test_utilities.bash`

### Fixture Files
- Organize fixtures by type (data, configs, scripts)
- Use descriptive names
- Include size or type in name when relevant

**Examples:**
- `fixtures/data/small_dataset.json`
- `fixtures/configs/invalid_config.conf`
- `fixtures/scripts/mock_server.sh`

## Test File Organization

### Single Test File Structure
```bash
#!/usr/bin/env bats

# Load common setup
load 'test_helper/common-setup'

setup() {
    _common_setup
    # Test-specific setup
}

teardown() {
    # Test-specific cleanup
}

@test "descriptive test name" {
    # Test implementation
}

@test "another descriptive test name" {
    # Test implementation
}
```

### Multiple Test Files with Shared Setup
**common-setup.bash:**
```bash
_common_setup() {
    load 'test_helper/bats-support/load'
    load 'test_helper/bats-assert/load'

    DIR="$( cd "$( dirname "$BATS_TEST_FILENAME" )" >/dev/null 2>&1 && pwd )"
    PATH="$DIR/../src:$PATH"

    export TEST_TEMP_DIR=$(mktemp -d)
}

_common_teardown() {
    rm -rf "$TEST_TEMP_DIR"
}
```

**Individual test file:**
```bash
#!/usr/bin/env bats

load 'test_helper/common-setup'

setup() {
    _common_setup
    # Additional setup for this test suite
}

teardown() {
    _common_teardown
    # Additional cleanup
}

@test "test specific to this file" {
    # Test implementation
}
```

## Running Tests

### Running All Tests
```bash
# Run all tests in test directory
./test/bats/bin/bats test/

# Run with parallel execution
./test/bats/bin/bats --jobs 4 test/

# Run with timing information
./test/bats/bin/bats --timing test/
```

### Running Specific Test Categories
```bash
# Run only unit tests
./test/bats/bin/bats test/unit/

# Run only integration tests
./test/bats/bin/bats test/integration/

# Run specific test file
./test/bats/bin/bats test/unit/script_test.bats
```

### Running with Different Formatters
```bash
# TAP output (default)
./test/bats/bin/bats test/

# Pretty output
./test/bats/bin/bats --formatter pretty test/

# JUnit XML for CI systems
./test/bats/bin/bats --formatter junit test/
```

## Makefile Integration

### Example Makefile
```makefile
.PHONY: test test-unit test-integration test-e2e test-performance

# Run all tests
test:
	./test/bats/bin/bats test/

# Run unit tests only
test-unit:
	./test/bats/bin/bats test/unit/

# Run integration tests only
test-integration:
	./test/bats/bin/bats test/integration/

# Run end-to-end tests only
test-e2e:
	./test/bats/bin/bats test/end_to_end/

# Run performance tests
test-performance:
	./test/bats/bin/bats test/performance/

# Run tests with coverage
test-coverage:
	./test/bats/bin/bats --timing --jobs 4 test/

# Run tests in CI environment
test-ci:
	./test/bats/bin/bats --formatter junit --jobs 2 test/

# Setup test environment
test-setup:
	git submodule update --init --recursive
	chmod +x src/*.sh

# Clean test artifacts
test-clean:
	rm -rf /tmp/bats-*
	find . -name "*.tmp" -delete
```

## Best Practices

### Test Organization
1. **Group related tests** in the same file or directory
2. **Use descriptive names** for files and test cases
3. **Separate test concerns** - unit vs integration vs e2e
4. **Keep tests independent** - no dependencies between test files
5. **Use shared setup** functions to reduce code duplication

### File Structure
1. **Mirror source structure** in test directory when logical
2. **Separate fixtures** from test code
3. **Use helper libraries** for common operations
4. **Document complex setup** in comments or README files
5. **Version control fixtures** that are needed for reproducible tests

### Execution Strategy
1. **Run fast tests first** - unit tests should be quick
2. **Use parallel execution** for independent tests
3. **Separate slow tests** for occasional execution
4. **Use CI integration** for automated testing
5. **Generate test reports** for visibility

### Maintenance
1. **Review test organization** regularly
2. **Refactor duplicate code** in setup/teardown
3. **Update fixtures** when requirements change
4. **Document test conventions** in project README
5. **Monitor test execution times** for optimization opportunities