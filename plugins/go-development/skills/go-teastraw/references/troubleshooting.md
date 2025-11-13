# Teastraw Troubleshooting Guide

## Common Issues and Solutions

### 1. Timeout Errors

**Problem**: `context deadline exceeded` or timeout errors when waiting for screen states.

**Solutions**:
- Increase timeout duration: `exp.WithDuration(5*time.Second)`
- Check if the condition logic is correct
- Verify the application is actually running
- Add logging to debug screen content

```go
// Debug timeout issues
t.Logf("Current screen content:\n%s", string(screen))
t.Logf("Waiting for: %s", expectedContent)
```

### 2. Screen Content Mismatch

**Problem**: Expected content not found on screen, or content appears differently.

**Solutions**:
- Check terminal size settings: `exp.WithInitialTermSize(width, height)`
- Verify application output encoding (UTF-8 vs ASCII)
- Look for color codes or formatting characters
- Use `runner.Screen()` to inspect actual content

```go
// Debug screen content
screen, err := runner.Screen()
if err == nil {
    t.Logf("Raw screen content: %q", string(screen))
    t.Logf("Screen length: %d", len(screen))
}
```

### 3. Input Not Working

**Problem**: Keyboard input doesn't trigger expected responses.

**Solutions**:
- Verify key sequences are correct (especially special keys)
- Check if the application requires specific timing between inputs
- Add small delays between inputs if needed
- Verify the application is focused and ready for input

```go
// Add timing for problematic inputs
runner.Send([]byte("test"))
time.Sleep(100 * time.Millisecond) // Small delay if needed
runner.Send([]byte{13}) // Enter
```

### 4. Golden File Mismatches

**Problem**: Tests fail when comparing screen output to golden files.

**Solutions**:
- Update golden files: `go test -update`
- Check for timing-related differences
- Verify terminal environment consistency
- Look for dynamic content (timestamps, random data)

```bash
# Update all golden files
go test -update ./...

# Update specific test
go test -run TestSpecificFunction -update
```

### 5. Application Startup Issues

**Problem**: Application fails to start or takes too long to initialize.

**Solutions**:
- Check application build: `go build ./cmd/app`
- Verify command arguments and working directory
- Check environment variables
- Test application manually outside of tests

```go
// Debug application startup
func getAppCmd() *exec.Cmd {
    cmd := exec.Command("go", "run", "./cmd/myapp")
    cmd.Dir = "."  // Ensure correct working directory
    cmd.Env = append(os.Environ(), "DEBUG=1")
    return cmd
}
```

### 6. Resource Cleanup Issues

**Problem**: Test processes don't terminate properly, causing resource leaks.

**Solutions**:
- Always use `defer runner.Cleanup()`
- Handle panics and test failures gracefully
- Check for background processes or goroutines
- Use proper context cancellation if needed

```go
func TestWithCleanup(t *testing.T) {
    runner, err := exp.NewTestRunner(...)
    require.NoError(t, err)

    // Ensure cleanup even if test panics
    defer func() {
        if r := recover(); r != nil {
            t.Logf("Test panicked: %v", r)
        }
        runner.Cleanup()
    }()

    // Test logic...
}
```

## Debugging Techniques

### 1. Verbose Logging

Add comprehensive logging to understand test behavior:

```go
func TestWithDebugging(t *testing.T) {
    t.Log("Starting test...")

    runner, err := exp.NewTestRunner(...)
    require.NoError(t, err)
    defer runner.Cleanup()

    // Log input sequences
    input := []byte("test input")
    t.Logf("Sending input: %v (%q)", input, string(input))
    err = runner.Send(input)
    require.NoError(t, err)

    // Log waiting conditions
    condition := func(screen []byte) bool {
        found := bytes.Contains(screen, []byte("expected"))
        t.Logf("Condition check - found: %v, screen preview: %s",
            found, string(screen[:min(100, len(screen))]))
        return found
    }

    screen, err := runner.WaitFor(condition, exp.WithDuration(2*time.Second))
    if err != nil {
        t.Logf("Full screen content at timeout:\n%s", string(screen))
    }
    require.NoError(t, err)
}
```

### 2. Step-by-Step Testing

Break complex tests into smaller steps for debugging:

```go
func TestStepByStep(t *testing.T) {
    runner, err := exp.NewTestRunner(...)
    require.NoError(t, err)
    defer runner.Cleanup()

    // Step 1: Wait for initial state
    t.Log("Step 1: Waiting for initial state")
    _, err = runner.WaitFor(func(s []byte) bool {
        return bytes.Contains(s, []byte("Welcome"))
    }, exp.WithDuration(3*time.Second))
    require.NoError(t, err)

    // Step 2: Send first input
    t.Log("Step 2: Sending navigation input")
    err = runner.Send([]byte("j"))
    require.NoError(t, err)

    // Step 3: Verify navigation worked
    t.Log("Step 3: Verifying navigation")
    screen, err := runner.WaitFor(func(s []byte) bool {
        return bytes.Contains(s, []byte("Next Item"))
    }, exp.WithDuration(2*time.Second))
    require.NoError(t, err)

    t.Logf("Step 3 success - screen preview: %s",
        string(screen[:min(50, len(screen))]))
}
```

### 3. Manual Testing

Test the application manually to verify behavior:

```go
func TestManualVerification(t *testing.T) {
    if testing.Short() {
        t.Skip("Skipping manual verification in short mode")
    }

    t.Log("Starting manual verification...")
    t.Log("Please observe the terminal output and press Enter to continue")

    // Run application with manual inspection
    cmd := exec.Command("go", "run", "./cmd/myapp")
    cmd.Stdin = os.Stdin
    cmd.Stdout = os.Stdout
    cmd.Stderr = os.Stderr

    err := cmd.Run()
    if err != nil {
        t.Logf("Application exited with error: %v", err)
    }

    t.Log("Manual verification complete")
}
```

## Environment Issues

### Terminal Settings

Ensure consistent terminal environment:

```go
func TestWithConsistentEnvironment(t *testing.T) {
    // Disable colors for consistent testing
    testEnv := []string{
        "NO_COLOR=1",
        "TERM=xterm-256color",
        "COLUMNS=80",
        "LINES=24",
        "TEST_MODE=1",
    }

    runner, err := exp.NewTestRunner(
        exp.WithInitialTermSize(80, 24),
        exp.WithCommand(getAppCmd()),
        exp.WithEnv(testEnv),
    )
    require.NoError(t, err)
    defer runner.Cleanup()

    // Test logic...
}
```

### Build Issues

Verify application builds correctly:

```bash
# Check if application builds
go build ./cmd/myapp

# Run application manually
./myapp

# Check dependencies
go mod tidy
go mod verify
```

## Performance Issues

### Slow Tests

Identify and optimize slow test operations:

```go
func TestPerformanceProfiling(t *testing.T) {
    start := time.Now()

    runner, err := exp.NewTestRunner(...)
    require.NoError(t, err)
    defer runner.Cleanup()

    setupTime := time.Since(start)
    t.Logf("TestRunner setup took: %v", setupTime)

    // Profile individual operations
    operationStart := time.Now()
    _, err = runner.WaitFor(func(s []byte) bool {
        return bytes.Contains(s, []byte("Ready"))
    }, exp.WithDuration(5*time.Second))
    operationTime := time.Since(operationStart)
    t.Logf("Wait operation took: %v", operationTime)

    require.NoError(t, err)

    totalTime := time.Since(start)
    t.Logf("Total test time: %v", totalTime)

    // Assert performance requirements
    assert.Less(t, totalTime, 10*time.Second, "Test took too long")
}
```

## Best Practices for Avoiding Issues

1. **Use appropriate timeouts** based on operation complexity
2. **Always clean up resources** with `defer runner.Cleanup()`
3. **Test with consistent environments** and terminal settings
4. **Update golden files** when UI changes intentionally
5. **Add comprehensive logging** for debugging complex scenarios
6. **Break complex tests** into smaller, manageable steps
7. **Test different terminal sizes** for responsive design validation
8. **Handle timing issues** with appropriate delays and synchronization
9. **Validate input sequences** before using them in tests
10. **Monitor resource usage** to prevent leaks and performance issues