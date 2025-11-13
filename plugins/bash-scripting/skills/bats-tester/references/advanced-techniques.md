# Advanced Bats Testing Techniques

## Test Helpers

Create reusable helper functions in `test/test_helper.bash`:

```bash
# test/test_helper.bash
setup_temp_dir() {
  TEST_TEMP_DIR="$(mktemp -d)"
  cd "$TEST_TEMP_DIR"
}

cleanup_temp_dir() {
  rm -rf "$TEST_TEMP_DIR"
}

create_test_file() {
  local filename="$1"
  local content="$2"
  echo "$content" > "$filename"
}
```

Load in your tests:

```bash
#!/usr/bin/env bats

load '../test_helper'

setup() {
  setup_temp_dir
}

teardown() {
  cleanup_temp_dir
}

@test "uses helper functions" {
  create_test_file "test.txt" "hello"
  [ -f "test.txt" ]
}
```

## Mocking Commands

### Simple Mock

```bash
@test "mocks external command" {
  # Create mock in PATH
  mock_curl() {
    echo "mocked response"
  }
  export -f mock_curl

  # Override curl temporarily
  curl() { mock_curl "$@"; }
  export -f curl

  run ./script_that_uses_curl.sh
  assert_output --partial "mocked response"
}
```

### Mock with Stub File

```bash
setup() {
  # Create temporary bin directory
  export MOCK_BIN="$(mktemp -d)"
  export PATH="$MOCK_BIN:$PATH"
}

teardown() {
  rm -rf "$MOCK_BIN"
}

@test "mocks command with stub" {
  # Create mock executable
  cat > "$MOCK_BIN/git" << 'EOF'
#!/bin/bash
echo "git version 2.0.0"
EOF
  chmod +x "$MOCK_BIN/git"

  run ./script.sh
  assert_success
}
```

## Testing with Fixtures

```bash
# test/fixtures/sample.json
{
  "key": "value"
}
```

```bash
@test "parses fixture file" {
  run ./parser.sh "test/fixtures/sample.json"
  assert_success
  assert_output --partial "value"
}
```

## Testing Environment Variables

```bash
@test "respects environment variable" {
  export MY_VAR="custom_value"
  run ./script.sh
  assert_output --partial "custom_value"
}

@test "handles missing env var" {
  unset MY_VAR
  run ./script.sh
  assert_failure
  assert_output --partial "MY_VAR not set"
}
```

## Testing Input/Output

### Testing stdin

```bash
@test "reads from stdin" {
  run bash -c 'echo "input data" | ./script.sh'
  assert_success
  assert_output --partial "processed: input data"
}
```

### Testing stderr

```bash
@test "writes to stderr" {
  run ./script.sh
  [ "$status" -eq 1 ]
  [[ "$stderr" == *"error message"* ]]
}
```

## Parallel Testing

```bash
# Run tests in parallel
bats --jobs 4 test/

# Some tests need to run serially
@test "requires exclusive access" {
  bats_require_minimum_version 1.5.0
  bats_lock_test_file
  # test code that needs exclusive access
}
```

## Debugging Tests

```bash
@test "debug output" {
  run ./script.sh
  # Show captured output for debugging
  echo "status: $status" >&3
  echo "output: $output" >&3
  assert_success
}

@test "debug with set -x" {
  set -x  # Enable bash debugging
  run ./script.sh
  assert_success
  set +x  # Disable bash debugging
}
```

## Testing Error Conditions

```bash
@test "handles invalid input" {
  run ./script.sh --invalid-flag
  assert_failure
  assert_output --partial "Unknown option"
}

@test "fails gracefully on missing file" {
  run ./script.sh /nonexistent/file
  assert_failure
  assert_line --index 0 "Error: File not found"
}
```

## Performance Testing

```bash
@test "completes within time limit" {
  start=$(date +%s)
  run ./script.sh
  end=$(date +%s)
  duration=$((end - start))

  assert_success
  [ "$duration" -lt 5 ]  # Must complete in under 5 seconds
}
```

## Integration with Other Tools

### Using with shellcheck

```bash
@test "script passes shellcheck" {
  run shellcheck ./script.sh
  assert_success
}
```

### Using with docker

```bash
@test "runs in container" {
  run docker run --rm -v "$PWD:/app" alpine:latest /app/script.sh
  assert_success
}
```
