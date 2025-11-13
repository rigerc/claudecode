---
name: go-teastraw
description: Use when creating end-to-end tests for TUI applications in Go using Teastraw. Expertise in testing compiled TUI binaries, simulating user interactions, and golden file testing.
---

# Go Teastraw TUI Testing Expert

Expert assistance for end-to-end testing of Go TUI applications using the Teastraw library.

## When to Use This Skill

Use this skill when you need help with:

- Creating end-to-end tests for TUI applications (Bubble Tea, custom TUI frameworks)
- Testing compiled TUI binaries in real terminal environments
- Simulating user interactions (keyboard input, special keys, navigation)
- Validating screen states using golden file testing
- Testing TUI applications with different terminal sizes
- Debugging TUI application behavior and UI issues

## Quick Start

```go
func TestTUI(t *testing.T) {
    runner, _ := exp.NewTestRunner(
        exp.WithInitialTermSize(80, 24),
        exp.WithCommand(exec.Command("./myapp")),
    )
    defer runner.Cleanup()

    // Wait for screen state
    screen, _ := runner.WaitFor(func(s []byte) bool {
        return bytes.Contains(s, []byte("Welcome"))
    }, exp.WithDuration(2*time.Second))

    runner.Send([]byte("j"))  // Simulate input
    exp.RequireEqualSubtest(t, screen, "welcome_screen")
}
```

## Available Resources

See `references/` for comprehensive documentation:

- **api-reference.md**: Complete Teastraw API documentation and method signatures
- **testing-patterns.md**: Common TUI testing patterns, workflows, and examples
- **troubleshooting.md**: Common issues, debugging strategies, and performance tips