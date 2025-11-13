---
name: go-teastraw
description: This skill should be used when developers need to create end-to-end tests for Terminal User Interface (TUI) applications in Go using the Teastraw library. It provides expertise in testing compiled TUI binaries, simulating user interactions, managing terminal environments, and validating screen states with golden file testing.
allowed-tools: [Read, Write, Edit, Glob, Grep, Bash, WebFetch, mcp__context7__resolve-library-id, mcp__context7__get-library-docs]
---

# Go Teastraw Testing Skill

## Overview

This skill provides specialized expertise for end-to-end testing of Go TUI applications using the Teastraw library. Teastraw enables testing compiled TUI binaries by simulating user interactions, capturing terminal output, and validating screen states against expected results. Unlike unit testing approaches, Teastraw tests fully compiled applications, providing true end-to-end validation of TUI applications built with frameworks like Bubble Tea.

## When to Use

Use this skill when developers need to:
- Create end-to-end tests for TUI applications (Bubble Tea, custom TUI frameworks)
- Test compiled TUI binaries in real terminal environments
- Simulate user interactions including keyboard input, special keys, and navigation
- Validate screen states using golden file testing
- Test TUI applications with different terminal sizes and environments
- Debug TUI application behavior and UI issues
- Test complex multi-step user workflows
- Verify responsive design across different terminal dimensions

## Instructions

### 1. Project Setup and Dependencies

Always start by ensuring proper project setup:

```bash
# Install Teastraw dependency
go get github.com/fiffeek/teastraw

# Verify project structure
find . -name "*_test.go" -type f
```

Check if the project has existing test structure and golden file directory:
- Look for `testdata/` directory with `.golden` files
- Verify test files follow Go testing conventions
- Check if the application compiles properly

### 2. Test Runner Configuration

Create test runners with appropriate configuration based on the application requirements:

```go
runner, err := exp.NewTestRunner(
    exp.WithInitialTermSize(80, 24),  // Standard terminal size
    exp.WithCommand(cmd),             // Application command
    exp.WithTimeout(30*time.Second),  // Operation timeout
    exp.WithEnv(testEnv),            // Environment variables
)
```

Always include `defer runner.Cleanup()` to ensure proper resource cleanup.

### 3. Screen State Management

Implement robust screen waiting strategies:

```go
// Wait for specific content with timeout
screen, err := runner.WaitFor(func(screen []byte) bool {
    return bytes.Contains(screen, []byte("Expected Content"))
}, exp.WithDuration(2*time.Second))
```

Use appropriate timeout values based on operation complexity:
- Quick operations: 100-500ms
- Normal operations: 500ms-2s
- Complex operations: 2-5s

### 4. Input Simulation

Simulate user interactions using correct terminal sequences:

```go
// Basic character input
runner.Send([]byte("j"))

// Special keys (arrows, control sequences)
runner.Send([]byte{27, 91, 66})  // Down arrow (\x1b[B)
runner.Send([]byte{3})          // Ctrl+C

// Text input with confirmation
runner.Send([]byte("text input"))
runner.Send([]byte{13})         // Enter key
```

### 5. Validation and Golden Files

Use golden file testing for screen validation:

```go
exp.RequireEqualSubtest(t, finalScreen, "test_state_name")
```

Ensure golden files are properly organized:
- Place in `testdata/` directory with `.golden` extension
- Update with `go test -update` when UI changes
- Use descriptive names for test states

### 6. Test Structure Patterns

Organize tests using table-driven patterns for complex workflows:

```go
tests := []struct {
    name     string
    setup    func(*exp.TestRunner) error
    input    [][]byte
    validate func([]byte) error
    golden   string
}{
    // Test cases...
}

for _, tt := range tests {
    t.Run(tt.name, func(t *testing.T) {
        // Test implementation...
    })
}
```

### 7. Terminal Size Testing

Test responsive design across multiple terminal dimensions:

```go
terminalSizes := []struct {
    name   string
    width  int
    height int
}{
    {"small", 40, 12},
    {"standard", 80, 24},
    {"wide", 120, 40},
}

for _, size := range terminalSizes {
    t.Run(size.name, func(t *testing.T) {
        runner, err := exp.NewTestRunner(
            exp.WithInitialTermSize(size.width, size.height),
            exp.WithCommand(getAppCmd()),
        )
        // Test with this size...
    })
}
```

### 8. Error Handling and Debugging

Implement comprehensive error handling and debugging:

```go
// Enable verbose logging for debugging
t.Logf("Screen content:\n%s", string(screen))
t.Logf("Sending input: %v", input)

// Debug waiting conditions
condition := func(screen []byte) bool {
    found := bytes.Contains(screen, []byte("expected"))
    t.Logf("Condition check: %v", found)
    return found
}
```

Handle common issues:
- Timeout errors: Increase duration or check condition logic
- Screen content mismatches: Verify terminal size and encoding
- Input not working: Check input sequences and key bindings
- Golden file mismatches: Update with `-update` flag

### 9. Environment Configuration

Set up proper test environments for consistent testing:

```go
testEnv := []string{
    "TEST_MODE=1",
    "NO_COLOR=1",           // Disable colors for consistent testing
    "TERM=xterm-256color",  // Consistent terminal type
    "CI=true",              // CI environment flag
}

func getAppCmd() *exec.Cmd {
    cmd := exec.Command("go", "run", "./cmd/myapp")
    cmd.Env = append(os.Environ(), testEnv...)
    return cmd
}
```

### 10. Performance and Integration

Implement performance testing and integration patterns:

```go
func TestPerformance(t *testing.T) {
    start := time.Now()

    // Perform TUI operations...

    elapsed := time.Since(start)
    t.Logf("Test completed in %v", elapsed)
    assert.Less(t, elapsed, 5*time.Second, "Test took too long")
}
```

## Resource References

### References Files
- `references/api-reference.md`: Complete Teastraw API documentation with method signatures
- `references/testing-patterns.md`: Common TUI testing patterns and examples
- `references/troubleshooting.md`: Troubleshooting guide for common issues

### Scripts
- `scripts/setup-test-environment.sh`: Script for setting up test environment
- `scripts/update-golden-files.sh`: Script for updating golden files across tests
- `scripts/run-tui-tests.sh`: Script for running comprehensive TUI test suites

### Assets
- `assets/testdata-templates/`: Template golden file structures
- `assets/example-apps/`: Example TUI applications for testing practice

## Common Workflows

### Basic TUI Testing Workflow
1. Create TestRunner with appropriate configuration
2. Wait for initial screen state
3. Simulate user inputs and navigation
4. Wait for expected screen changes
5. Validate final state with golden files
6. Clean up resources

### Form Testing Workflow
1. Navigate to form fields
2. Input data into each field
3. Submit form
4. Validate success/error states
5. Test form validation scenarios

### Navigation Testing Workflow
1. Test menu navigation (up/down arrows)
2. Test keyboard shortcuts
3. Test menu selection and activation
4. Test navigation between screens
5. Test back/cancel functionality

### Error Handling Workflow
1. Trigger error conditions
2. Verify error message display
3. Test error recovery mechanisms
4. Test application stability after errors
5. Verify graceful degradation