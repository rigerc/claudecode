# Bats-Core Troubleshooting Guide

This document provides solutions to common issues encountered when working with bats-core tests.

## Common Issues and Solutions

### Tests Fail to Run

#### Issue: "Permission denied" when running test file
```bash
$ ./test/bats/bin/bats test/script_test.bats
bash: ./test/bats/bin/bats: Permission denied
```

**Solution:**
```bash
chmod +x ./test/bats/bin/bats
chmod +x ./test/bats/libexec/bats-core/bats
```

#### Issue: "No such file or directory" for bats executable
```bash
$ ./test/bats/bin/bats test/script_test.bats
./test/bats/bin/bats: No such file or directory
```

**Solution:**
```bash
# Initialize git submodules
git submodule update --init --recursive

# Or clone manually
git clone https://github.com/bats-core/bats-core.git test/bats
```

### Test Failures

#### Issue: Tests failing with "command not found"
```bash
✗ script runs successfully
   (in test file test/script_test.bats, line 15)
     `script.sh' failed with status 127
```

**Causes and Solutions:**

1. **PATH not set correctly**
   ```bash
   setup() {
       DIR="$( cd "$( dirname "$BATS_TEST_FILENAME" )" >/dev/null 2>&1 && pwd )"
       PATH="$DIR/../src:$PATH"
   }
   ```

2. **Script doesn't have execute permissions**
   ```bash
   chmod +x src/script.sh
   ```

3. **Using relative path incorrectly**
   ```bash
   # Wrong - uses relative path from current directory
   run ../src/script.sh

   # Correct - script is on PATH
   run script.sh
   ```

#### Issue: Test fails but no output shown
```bash
✗ script should show message
   (in test file test/script_test.bats, line 20)
     `assert_output --partial "expected message"' failed
```

**Solutions:**

1. **Use --verbose-run to see command output**
   ```bash
   ./test/bats/bin/bats --verbose-run test/script_test.bats
   ```

2. **Debug the command directly**
   ```bash
   # In test file
   @test "debug test" {
       echo "Running script with debug:" >&3
       script.sh >&3
       run script.sh
   }
   ```

3. **Check for output in stderr vs stdout**
   ```bash
   run script.sh 2>&1  # Capture both stdout and stderr
   echo "$output" >&3  # Print output for debugging
   ```

#### Issue: Tests pass but shouldn't (false positives)
```bash
✓ script handles invalid input  # This should fail!
```

**Common Causes:**

1. **Missing `run` command**
   ```bash
   # Wrong - command failure won't fail test
   script.sh --invalid
   assert_failure

   # Correct
   run script.sh --invalid
   assert_failure
   ```

2. **Assertions not checking the right thing**
   ```bash
   # Wrong - only checks exit code, not error message
   run script.sh --invalid
   assert_failure

   # Correct - checks both exit code and error message
   run script.sh --invalid
   assert_failure
   assert_output --partial "Invalid input"
   ```

### Setup and Teardown Issues

#### Issue: Setup function not called
```bash
@test "test fails with PATH not set" {
    run script.sh
    assert_success  # Fails because script not found
}
```

**Solution:**
```bash
setup() {
    load 'test_helper/bats-support/load'
    load 'test_helper/bats-assert/load'

    DIR="$( cd "$( dirname "$BATS_TEST_FILENAME" )" >/dev/null 2>&1 && pwd )"
    PATH="$DIR/../src:$PATH"
}
```

#### Issue: Teardown not cleaning up files
```bash
# Files left in /tmp after test runs
```

**Solution:**
```bash
teardown() {
    # Use a consistent temp directory
    if [[ -n "$TEST_TEMP_DIR" && -d "$TEST_TEMP_DIR" ]]; then
        rm -rf "$TEST_TEMP_DIR"
    fi
}

setup() {
    TEST_TEMP_DIR=$(mktemp -d)
    export TEST_TEMP_DIR
}
```

#### Issue: setup_file/teardown_file not working
```bash
setup_file() {
    export GLOBAL_VAR="value"  # Not available in tests
}
```

**Solution:**
```bash
setup_file() {
    # Must export variables to make them available
    export GLOBAL_VAR="value"

    # Or write to a file and read it in setup()
    echo "value" > /tmp/test_global_var
}

setup() {
    GLOBAL_VAR=$(cat /tmp/test_global_var)
}
```

### Helper Library Issues

#### Issue: "load: cannot find" helper library
```bash
✗ setup() failed
   (in test file test/script_test.bats, line 5)
     load 'test_helper/bats-support/load' failed
```

**Solutions:**

1. **Check file paths**
   ```bash
   ls -la test/test_helper/bats-support/
   # Should show: load, setup.bash, etc.
   ```

2. **Initialize submodules**
   ```bash
   git submodule update --init --recursive
   ```

3. **Use absolute paths if needed**
   ```bash
   load "$BATS_TEST_DIRNAME/../test_helper/bats-support/load"
   ```

#### Issue: Assertion functions not found
```bash
✗ test assertion
   (in test file test/script_test.bats, line 15)
     `assert_output' failed
```

**Solution:**
```bash
setup() {
    # Load both support and assert libraries
    load 'test_helper/bats-support/load'
    load 'test_helper/bats-assert/load'
}
```

### File and Directory Issues

#### Issue: Tests can't find files
```bash
✗ test reads configuration file
   `script.sh --config test.conf' failed with status 1
```

**Solutions:**

1. **Use absolute paths**
   ```bash
   @test "test with config file" {
       config_file="$BATS_TMPDIR/test.conf"
       echo "setting=value" > "$config_file"
       run script.sh --config "$config_file"
   }
   ```

2. **Set working directory correctly**
   ```bash
   setup() {
       cd "$BATS_TMPDIR"
       # Now relative paths work from temp directory
   }
   ```

3. **Copy files to temp directory**
   ```bash
   setup() {
       cp fixtures/test.conf "$BATS_TMPDIR/"
       cd "$BATS_TMPDIR"
   }
   ```

#### Issue: Permission denied on file operations
```bash
✗ test creates output file
   `touch /root/output.txt' failed with status 1
```

**Solution:**
```bash
setup() {
    # Always use temp directory, not system directories
    export TEST_TEMP_DIR=$(mktemp -d)
    cd "$TEST_TEMP_DIR"
}
```

### Environment Issues

#### Issue: Tests pass locally but fail in CI

**Common Causes:**

1. **Different shell environments**
   ```bash
   # In CI script
   export SHELL=/bin/bash
   ./test/bats/bin/bats test/
   ```

2. **Missing dependencies**
   ```bash
   # Add dependency checks to tests
   setup() {
       if ! command -v jq &> /dev/null; then
           skip "jq is required for these tests"
       fi
   }
   ```

3. **File system differences**
   ```bash
   # Use cross-compatible paths
   setup() {
       TEST_TEMP_DIR=$(mktemp -d)
       cd "$TEST_TEMP_DIR"
       # Avoid assuming specific permissions or owners
   }
   ```

#### Issue: Tests timing out or hanging

**Solutions:**

1. **Add timeouts to long-running commands**
   ```bash
   @test "test with timeout" {
       run timeout 30s script.sh --long-operation
       assert_success
   }
   ```

2. **Check for infinite loops**
   ```bash
   # Add debug output to identify where script hangs
   run script.sh --debug 2>&1 | tee /tmp/debug.log &
   script_pid=$!
   sleep 10
   if kill -0 $script_pid 2>/dev/null; then
       kill $script_pid
       echo "Script still running after 10 seconds" >&3
       cat /tmp/debug.log >&3
       false
   fi
   ```

3. **Use background processes for servers**
   ```bash
   setup() {
       start_test_server &
       export SERVER_PID=$!
       sleep 2  # Give server time to start
   }

   teardown() {
       kill $SERVER_PID 2>/dev/null || true
   }
   ```

### Performance Issues

#### Issue: Tests running slowly

**Optimizations:**

1. **Use setup_file for expensive operations**
   ```bash
   setup_file() {
       # Heavy setup done once per file
       setup_database
       start_services
   }

   setup() {
       # Light setup done per test
       export TEST_FILE=$(mktemp)
   }
   ```

2. **Run tests in parallel**
   ```bash
   ./test/bats/bin/bats --jobs 4 test/
   ```

3. **Avoid unnecessary file operations**
   ```bash
   # Bad - creates files for every test
   setup() {
       echo "test data" > test_file.txt
   }

   # Good - reuse setup
   setup_file() {
       echo "test data" > "$TEST_TEMP_DIR/shared_data.txt"
   }
   ```

### Debugging Techniques

#### 1. Use Bats Debug Output
```bash
@test "debug test" {
    echo "Variable value: $VAR" >&3
    echo "Current directory: $(pwd)" >&3
    echo "PATH: $PATH" >&3
    run script.sh
    echo "Exit status: $status" >&3
    echo "Output: $output" >&3
}
```

#### 2. Run Bats Verbose
```bash
./test/bats/bin/bats --verbose-run test/
./test/bats/bin/bats --print-output-on-failure test/
```

#### 3. Run Individual Tests
```bash
./test/bats/bin/bats --filter "test name contains this text" test/
```

#### 4. Check Temporary Files
```bash
# Bats creates temp directories, check them for debugging
ls -la /tmp/bats-run-*
```

#### 5. Use Shell Debugging
```bash
# Add set -x to scripts for debugging
run bash -x script.sh
```

## Getting Help

### Bats-Core Resources
- [Bats-Core GitHub](https://github.com/bats-core/bats-core)
- [Bats-Core Documentation](https://bats-core.readthedocs.io/)
- [Bats-Support](https://github.com/bats-core/bats-support)
- [Bats-Assert](https://github.com/bats-core/bats-assert)

### Community Support
- GitHub Issues for each library
- Stack Overflow with `bats` tag
- Bash IRC channels and forums

### Common Debugging Commands
```bash
# Check bats installation
./test/bats/bin/bats --version

# Validate test file syntax
bash -n test/script_test.bats

# Check file permissions
ls -la src/ test/

# Verify git submodules
git submodule status
```