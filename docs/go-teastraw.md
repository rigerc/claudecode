# Teastraw: Go TUI Testing Library Documentation

## Overview

**Tastraw** is a Go testing library specifically designed for end-to-end testing of Terminal User Interface (TUI) applications. It provides a comprehensive framework for testing compiled TUI binaries by simulating user interactions, capturing terminal output, and validating screen states against expected results.

Unlike traditional unit testing approaches that test components in isolation, Teastraw tests fully compiled applications, providing true end-to-end validation of TUI applications built with frameworks like Bubble Tea.

## Key Features

- **Screen Validation**: Golden file testing for terminal output comparison
- **Input Simulation**: Comprehensive keyboard input support including special characters and arrow keys
- **Conditional Waiting**: Configurable timeouts for waiting on specific screen states
- **Graceful Shutdown**: Automatic capture of application shutdown sequences
- **Terminal Sizing**: Customizable terminal dimensions for testing different screen sizes
- **Exit Sequence Handling**: Proper handling of application termination and exit codes
- **End-to-End Testing**: Tests compiled binaries, not isolated components

## Installation

```bash
go get github.com/fiffeek/teastraw
```

## Quick Start

```go
package main

import (
    "bytes"
    "testing"
    "time"

    "github.com/fiffeek/teastraw/exp"
    "github.com/stretchr/testify/assert"
    "github.com/stretchr/testify/require"
)

func TestMyTUIApp(t *testing.T) {
    // Create test runner with custom terminal size
    runner, err := exp.NewTestRunner(
        exp.WithInitialTermSize(80, 24),
        exp.WithCommand(cmd), // Your *exec.Cmd
    )
    require.NoError(t, err)

    // Wait for welcome content to appear
    err = runner.WaitFor(func(screen []byte) bool {
        return bytes.Contains(screen, []byte("Welcome"))
    }, exp.WithDuration(200*time.Millisecond))
    require.NoError(t, err)

    // Simulate user input
    assert.NoError(t, runner.Send([]byte("j"))) // Move down
    assert.NoError(t, runner.Send([]byte("k"))) // Move up

    // Wait for specific state
    finalScreen, err := runner.WaitFor(func(screen []byte) bool {
        return bytes.Contains(screen, []byte("Menu Item"))
    }, exp.WithDuration(500*time.Millisecond))
    require.NoError(t, err)

    // Validate final screen state
    exp.RequireEqualSubtest(t, finalScreen, "__final_screen")
}
```

## Core Concepts

### TestRunner

The `TestRunner` is the main component that manages the TUI application lifecycle:

```go
type TestRunner struct {
    // Internal fields managed by the library
}
```

### Configuration Options

Tastraw provides several configuration options when creating a TestRunner:

```go
// Create runner with custom terminal dimensions
runner, err := exp.NewTestRunner(
    exp.WithInitialTermSize(120, 40), // width, height
    exp.WithCommand(cmd),            // *exec.Cmd to run
)
```

#### Available Options

- **`WithInitialTermSize(width, height int)`**: Set initial terminal dimensions
- **`WithCommand(cmd *exec.Cmd)`**: Specify the command to execute
- **`WithTimeout(duration time.Duration)`**: Set default timeout for operations
- **`WithEnv(env []string)`**: Set environment variables for the test

## API Reference

### TestRunner Creation

```go
func NewTestRunner(opts ...Option) (*TestRunner, error)
```

Creates a new TestRunner instance with the specified configuration options.

### Screen Operations

#### Wait for Screen State

```go
func (r *TestRunner) WaitFor(condition func([]byte) bool, opts ...WaitOption) ([]byte, error)
```

Waits for a condition to be met on the terminal screen.

**Parameters:**
- `condition`: Function that receives screen content and returns true when condition is met
- `opts`: Wait configuration options

**Wait Options:**
- `WithDuration(duration time.Duration)`: Maximum wait time
- `WithInterval(duration time.Duration)`: Check interval

**Example:**
```go
screen, err := runner.WaitFor(func(screen []byte) bool {
    return bytes.Contains(screen, []byte("Ready"))
}, exp.WithDuration(2*time.Second))
```

#### Send Input

```go
func (r *TestRunner) Send(input []byte) error
```

Sends keyboard input to the running TUI application.

**Example:**
```go
// Send single key
runner.Send([]byte("j"))

// Send special keys
runner.Send([]byte{27, 91, 66}) // Down arrow

// Send text input
runner.Send([]byte("hello world"))
runner.Send([]byte{13}) // Enter key
```

#### Get Current Screen

```go
func (r *TestRunner) Screen() ([]byte, error)
```

Returns the current terminal screen content.

### Validation Helpers

#### Equal Screen Test

```go
func RequireEqualSubtest(t *testing.T, screen []byte, testName string)
```

Validates that the screen content matches the expected golden file.

**Golden File Format:**
Golden files should be placed in `testdata/` directory with `.golden` extension:
```
testdata/
├── __final_screen.golden
├── __welcome_screen.golden
└── __error_state.golden
```

**Example Usage:**
```go
// This will compare screen content with testdata/__final_screen.golden
exp.RequireEqualSubtest(t, finalScreen, "__final_screen")
```

## Testing Patterns

### Basic TUI Navigation Test

```go
func TestNavigation(t *testing.T) {
    runner, err := exp.NewTestRunner(
        exp.WithInitialTermSize(80, 24),
        exp.WithCommand(getAppCmd()),
    )
    require.NoError(t, err)
    defer runner.Cleanup()

    // Wait for initial screen
    _, err = runner.WaitFor(func(screen []byte) bool {
        return bytes.Contains(screen, []byte("Main Menu"))
    }, exp.WithDuration(1*time.Second))
    require.NoError(t, err)

    // Navigate through menu
    testCases := []struct {
        input    string
        expected string
    }{
        {"j", "Settings"},
        {"j", "Help"},
        {"k", "Settings"},
        {"\x1b[B", "Help"}, // Down arrow
        {"\x1b[A", "Settings"}, // Up arrow
    }

    for _, tc := range testCases {
        t.Run(fmt.Sprintf("navigate_%s", tc.expected), func(t *testing.T) {
            err := runner.Send([]byte(tc.input))
            require.NoError(t, err)

            screen, err := runner.WaitFor(func(screen []byte) bool {
                return bytes.Contains(screen, []byte(tc.expected))
            }, exp.WithDuration(500*time.Millisecond))
            require.NoError(t, err)

            exp.RequireEqualSubtest(t, screen, tc.expected)
        })
    }
}
```

### Form Input Test

```go
func TestFormInput(t *testing.T) {
    runner, err := exp.NewTestRunner(
        exp.WithInitialTermSize(100, 30),
        exp.WithCommand(getFormAppCmd()),
    )
    require.NoError(t, err)
    defer runner.Cleanup()

    // Wait for form to be ready
    _, err = runner.WaitFor(func(screen []byte) bool {
        return bytes.Contains(screen, []byte("Name:"))
    }, exp.WithDuration(1*time.Second))
    require.NoError(t, err)

    // Fill form fields
    formInputs := []struct {
        field   string
        input   string
        confirm string // Enter key to move to next field
    }{
        {"Name:", "John Doe", "\t"},     // Tab to next field
        {"Email:", "john@example.com", "\t"},
        {"Phone:", "555-0123", "\r"},    // Enter to submit
    }

    for _, input := range formInputs {
        // Wait for field to be active
        _, err := runner.WaitFor(func(screen []byte) bool {
            return bytes.Contains(screen, []byte(input.field))
        }, exp.WithDuration(500*time.Millisecond))
        require.NoError(t, err)

        // Send field value
        err = runner.Send([]byte(input.input))
        require.NoError(t, err)

        // Send navigation key
        err = runner.Send([]byte(input.confirm))
        require.NoError(t, err)
    }

    // Wait for success message
    successScreen, err := runner.WaitFor(func(screen []byte) bool {
        return bytes.Contains(screen, []byte("Form submitted successfully"))
    }, exp.WithDuration(2*time.Second))
    require.NoError(t, err)

    exp.RequireEqualSubtest(t, successScreen, "form_success")
}
```

### Error Handling Test

```go
func TestErrorHandling(t *testing.T) {
    runner, err := exp.NewTestRunner(
        exp.WithInitialTermSize(80, 24),
        exp.WithCommand(getAppCmd()),
    )
    require.NoError(t, err)
    defer runner.Cleanup()

    // Trigger error condition
    err = runner.Send([]byte("x")) // Invalid command
    require.NoError(t, err)

    // Wait for error message
    errorScreen, err := runner.WaitFor(func(screen []byte) bool {
        return bytes.Contains(screen, []byte("Error: Invalid command"))
    }, exp.WithDuration(1*time.Second))
    require.NoError(t, err)

    exp.RequireEqualSubtest(t, errorScreen, "error_state")

    // Verify recovery
    err = runner.Send([]byte("q"))
    require.NoError(t, err)

    quitScreen, err := runner.WaitFor(func(screen []byte) bool {
        return bytes.Contains(screen, []byte("Goodbye"))
    }, exp.WithDuration(500*time.Millisecond))
    require.NoError(t, err)
}
```

## Special Keys and Input

### Arrow Keys

```go
// Arrow key sequences for terminal applications
arrowKeys := map[string][]byte{
    "up":    {27, 91, 65}, // \x1b[A
    "down":  {27, 91, 66}, // \x1b[B
    "right": {27, 91, 67}, // \x1b[C
    "left":  {27, 91, 68}, // \x1b[D
}

// Usage
runner.Send(arrowKeys["down"])
```

### Control Sequences

```go
controlKeys := map[string]byte{
    "ctrl+c":  3,
    "ctrl+d":  4,
    "ctrl+z":  26,
    "enter":   13,
    "tab":     9,
    "backspace": 127,
    "escape":  27,
}

// Usage
runner.Send([]byte{controlKeys["ctrl+c"]})
```

### Function Keys

```go
// Function key sequences
functionKeys := map[string][]byte{
    "f1": {27, 79, 80},  // \x1bOP
    "f2": {27, 79, 81},  // \x1bOQ
    "f3": {27, 79, 82},  // \x1bOR
    // ... more function keys
}
```

## Best Practices

### 1. Test Structure

Organize your tests logically:

```go
func TestMyTUIApp(t *testing.T) {
    tests := []struct {
        name     string
        setup    func(*exp.TestRunner) error
        input    [][]byte
        validate func([]byte) error
        golden   string
    }{
        {
            name: "basic_navigation",
            setup: func(r *exp.TestRunner) error {
                // Initial setup
                return nil
            },
            input: [][]byte{
                []byte("j"), // Move down
                []byte("j"), // Move down again
            },
            validate: func(screen []byte) error {
                if !bytes.Contains(screen, []byte("Third Item")) {
                    return fmt.Errorf("expected 'Third Item' on screen")
                }
                return nil
            },
            golden: "navigation_result",
        },
    }

    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            runner, err := exp.NewTestRunner(
                exp.WithInitialTermSize(80, 24),
                exp.WithCommand(getAppCmd()),
            )
            require.NoError(t, err)
            defer runner.Cleanup()

            err = tt.setup(runner)
            require.NoError(t, err)

            for _, input := range tt.input {
                err = runner.Send(input)
                require.NoError(t, err)
            }

            screen, err := runner.WaitFor(func(s []byte) bool {
                return tt.validate(s) == nil
            }, exp.WithDuration(2*time.Second))
            require.NoError(t, err)

            if tt.golden != "" {
                exp.RequireEqualSubtest(t, screen, tt.golden)
            }
        })
    }
}
```

### 2. Timeout Management

Use appropriate timeouts based on the operation complexity:

```go
// Quick operations
quickTimeout := 100 * time.Millisecond

// Normal operations
normalTimeout := 500 * time.Millisecond

// Complex operations (loading, processing)
longTimeout := 5 * time.Second
```

### 3. Cleanup

Always clean up test runners:

```go
func TestWithCleanup(t *testing.T) {
    runner, err := exp.NewTestRunner(...)
    require.NoError(t, err)

    // Ensure cleanup even if test fails
    defer runner.Cleanup()

    // Test logic here...
}
```

### 4. Golden Files

Manage golden files properly:

```bash
# Update golden files when UI changes
go test -update

# Run tests with verbose output
go test -v
```

### 5. Terminal Size Testing

Test with different terminal dimensions:

```go
terminalSizes := []struct {
    name  string
    width int
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
        require.NoError(t, err)
        defer runner.Cleanup()

        // Test with this terminal size...
    })
}
```

## Comparison with Other Testing Libraries

### Teastraw vs Teatest

| Feature | Teastraw | Teatest |
|---------|----------|---------|
| Testing Scope | End-to-end (compiled binaries) | Unit testing (models in isolation) |
| Screen Validation | Golden file testing | Direct state assertion |
| Input Simulation | Full keyboard support | Message-based input |
| Terminal Size | Customizable | Fixed |
| Integration | Real environment | Mocked environment |

### When to Use Teastraw

- **End-to-end testing**: Test the complete application flow
- **UI validation**: Verify visual appearance and layout
- **Integration testing**: Test with real terminal environments
- **Complex interactions**: Test multi-step user workflows
- **Terminal size testing**: Validate responsive design

### When to Use Teatest

- **Unit testing**: Test individual model logic
- **Fast feedback**: Quick model state validation
- **Component isolation**: Test components independently
- **Business logic**: Focus on application logic over UI

## Advanced Usage

### Custom Test Commands

```go
func getAppCmd() *exec.Cmd {
    cmd := exec.Command("go", "run", "./cmd/myapp")
    cmd.Env = append(os.Environ(),
        "TEST_MODE=1",
        "NO_COLOR=1", // Disable colors for consistent testing
    )
    return cmd
}
```

### Environment Variables

```go
func TestWithEnvironment(t *testing.T) {
    testEnv := []string{
        "TEST_MODE=1",
        "DEBUG=1",
        "CONFIG_FILE=testdata/config.yaml",
        "TERM=xterm-256color",
    }

    runner, err := exp.NewTestRunner(
        exp.WithInitialTermSize(80, 24),
        exp.WithCommand(getAppCmd()),
        exp.WithEnv(testEnv),
    )
    require.NoError(t, err)
    defer runner.Cleanup()

    // Test with custom environment...
}
```

### Performance Testing

```go
func TestPerformance(t *testing.T) {
    start := time.Now()

    runner, err := exp.NewTestRunner(...)
    require.NoError(t, err)
    defer runner.Cleanup()

    // Perform operations...

    elapsed := time.Since(start)
    t.Logf("Test completed in %v", elapsed)

    // Assert performance requirements
    assert.Less(t, elapsed, 5*time.Second, "Test took too long")
}
```

## Troubleshooting

### Common Issues

1. **Timeout Errors**: Increase timeout duration or check condition logic
2. **Screen Content Mismatch**: Verify terminal size and encoding
3. **Input Not Working**: Check input sequences and key bindings
4. **Golden File Mismatches**: Update golden files with `-update` flag

### Debugging Tips

```go
// Enable verbose logging
t.Logf("Screen content:\n%s", string(screen))

// Debug input sequences
input := []byte("test input")
t.Logf("Sending input: %v", input)

// Check waiting conditions
condition := func(screen []byte) bool {
    found := bytes.Contains(screen, []byte("expected"))
    t.Logf("Condition check: %v", found)
    return found
}
```

## Conclusion

Tastraw provides a comprehensive solution for end-to-end testing of TUI applications in Go. By testing compiled binaries in real terminal environments, it ensures that your TUI applications work correctly across different scenarios and user interactions.

For more examples and advanced usage patterns, refer to the project's test files and examples in the GitHub repository.