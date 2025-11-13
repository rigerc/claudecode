# Example TUI Applications

This directory contains example TUI applications that can be used for testing and learning Teastraw.

## Example Applications

### 1. Simple Menu App
A basic menu-driven TUI application with navigation and selection.

### 2. Form Input App
An application that demonstrates form input and validation.

### 3. Multi-screen App
An application with multiple screens and state management.

### 4. Error Handling App
An application that demonstrates error states and recovery.

## Using Example Apps

These example applications are designed to help you:

1. **Learn Teastraw basics**: Simple examples for getting started
2. **Practice testing patterns**: Real applications to test against
3. **Understand common workflows**: Navigation, forms, errors, etc.
4. **Develop test strategies**: See different approaches to TUI testing

## Building and Running

```bash
# Build specific example
cd simple-menu
go build -o simple-menu .

# Run example directly
./simple-menu

# Run with Go
go run main.go
```

## Testing Examples

Use these applications to practice Teastraw testing:

```go
// Example test for simple menu app
func TestSimpleMenuNavigation(t *testing.T) {
    cmd := exec.Command("go", "run", "./assets/example-apps/simple-menu/main.go")

    runner, err := exp.NewTestRunner(
        exp.WithInitialTermSize(80, 24),
        exp.WithCommand(cmd),
    )
    require.NoError(t, err)
    defer runner.Cleanup()

    // Test navigation logic...
}
```

## Creating Your Own Examples

When creating your own example applications for testing:

1. **Keep them simple**: Focus on one or two specific features
2. **Include variety**: Different types of interactions and states
3. **Document behavior**: Clear descriptions of what each app does
4. **Test thoroughly**: Provide example tests for each application
5. **Use realistic scenarios**: Mirror real-world TUI application patterns