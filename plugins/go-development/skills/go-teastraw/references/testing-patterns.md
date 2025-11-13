# TUI Testing Patterns

## Basic Navigation Testing

```go
func TestBasicNavigation(t *testing.T) {
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

    // Test arrow key navigation
    testCases := []struct {
        input    []byte
        expected string
    }{
        {[]byte("j"), "Settings Menu"},
        {[]byte("k"), "Main Menu"},
        {[]byte{27, 91, 66}, "Settings Menu"}, // Down arrow
        {[]byte{27, 91, 65}, "Main Menu"},     // Up arrow
    }

    for _, tc := range testCases {
        t.Run(fmt.Sprintf("navigate_%s", string(tc.input)), func(t *testing.T) {
            err = runner.Send(tc.input)
            require.NoError(t, err)

            screen, err := runner.WaitFor(func(screen []byte) bool {
                return bytes.Contains(screen, tc.expected)
            }, exp.WithDuration(500*time.Millisecond))
            require.NoError(t, err)
        })
    }
}
```

## Form Input Testing

```go
func TestFormSubmission(t *testing.T) {
    runner, err := exp.NewTestRunner(
        exp.WithInitialTermSize(100, 30),
        exp.WithCommand(getFormAppCmd()),
    )
    require.NoError(t, err)
    defer runner.Cleanup()

    // Wait for form fields to be ready
    formFields := []struct {
        field     string
        value     string
        confirm   []byte
        validator func([]byte) bool
    }{
        {
            field:     "Name:",
            value:     "John Doe",
            confirm:   []byte{9}, // Tab
            validator: func(s []byte) bool { return bytes.Contains(s, []byte("Email:")) },
        },
        {
            field:     "Email:",
            value:     "john@example.com",
            confirm:   []byte{13}, // Enter
            validator: func(s []byte) bool { return bytes.Contains(s, []byte("Submitted")) },
        },
    }

    for _, field := range formFields {
        // Wait for field to be active
        _, err := runner.WaitFor(func(screen []byte) bool {
            return bytes.Contains(screen, []byte(field.field))
        }, exp.WithDuration(1*time.Second))
        require.NoError(t, err)

        // Send field value
        err = runner.Send([]byte(field.value))
        require.NoError(t, err)

        // Send confirmation key
        err = runner.Send(field.confirm)
        require.NoError(t, err)

        // Wait for next field or submission
        _, err = runner.WaitFor(field.validator, exp.WithDuration(1*time.Second))
        require.NoError(t, err)
    }
}
```

## Error State Testing

```go
func TestErrorHandling(t *testing.T) {
    runner, err := exp.NewTestRunner(
        exp.WithInitialTermSize(80, 24),
        exp.WithCommand(getAppCmd()),
    )
    require.NoError(t, err)
    defer runner.Cleanup()

    errorScenarios := []struct {
        name        string
        input       []byte
        errorText   string
        recoveryKey []byte
    }{
        {
            name:        "invalid_command",
            input:       []byte("x"),
            errorText:   "Error: Invalid command",
            recoveryKey: []byte("q"),
        },
        {
            name:        "file_not_found",
            input:       []byte("o non-existent.txt"),
            errorText:   "Error: File not found",
            recoveryKey: []byte("esc"),
        },
    }

    for _, scenario := range errorScenarios {
        t.Run(scenario.name, func(t *testing.T) {
            // Trigger error
            err = runner.Send(scenario.input)
            require.NoError(t, err)

            // Wait for error message
            errorScreen, err := runner.WaitFor(func(screen []byte) bool {
                return bytes.Contains(screen, []byte(scenario.errorText))
            }, exp.WithDuration(2*time.Second))
            require.NoError(t, err)

            exp.RequireEqualSubtest(t, errorScreen, scenario.name+"_error")

            // Test recovery
            err = runner.Send(scenario.recoveryKey)
            require.NoError(t, err)

            // Verify recovery to normal state
            _, err = runner.WaitFor(func(screen []byte) bool {
                return !bytes.Contains(screen, []byte("Error:"))
            }, exp.WithDuration(1*time.Second))
            require.NoError(t, err)
        })
    }
}
```

## Multi-Step Workflow Testing

```go
func TestCompleteWorkflow(t *testing.T) {
    runner, err := exp.NewTestRunner(
        exp.WithInitialTermSize(80, 24),
        exp.WithCommand(getWorkflowAppCmd()),
    )
    require.NoError(t, err)
    defer runner.Cleanup()

    workflowSteps := []struct {
        name        string
        input       []byte
        waitFor     string
        timeout     time.Duration
        description string
    }{
        {
            name:        "start_application",
            input:       nil,
            waitFor:     "Welcome to Workflow App",
            timeout:     2 * time.Second,
            description: "Application startup",
        },
        {
            name:        "navigate_to_settings",
            input:       []byte("s"),
            waitFor:     "Settings Menu",
            timeout:     1 * time.Second,
            description: "Navigate to settings",
        },
        {
            name:        "configure_option",
            input:       []byte("c"),
            waitFor:     "Configuration Options",
            timeout:     1 * time.Second,
            description: "Open configuration",
        },
        {
            name:        "save_settings",
            input:       []byte{13}, // Enter
            waitFor:     "Settings saved",
            timeout:     2 * time.Second,
            description: "Save configuration",
        },
        {
            name:        "return_to_main",
            input:       []byte("q"),
            waitFor:     "Main Menu",
            timeout:     1 * time.Second,
            description: "Return to main menu",
        },
        {
            name:        "exit_application",
            input:       []byte("q"),
            waitFor:     "Goodbye",
            timeout:     1 * time.Second,
            description: "Exit application",
        },
    }

    for _, step := range workflowSteps {
        t.Run(step.name, func(t *testing.T) {
            if step.input != nil {
                err = runner.Send(step.input)
                require.NoError(t, err)
            }

            screen, err := runner.WaitFor(func(s []byte) bool {
                return bytes.Contains(s, []byte(step.waitFor))
            }, exp.WithDuration(step.timeout))
            require.NoError(t, err)

            exp.RequireEqualSubtest(t, screen, step.name)
        })
    }
}
```

## Table-Driven Test Pattern

```go
func TestMultipleScenarios(t *testing.T) {
    testCases := []struct {
        name     string
        setup    func(*exp.TestRunner) error
        input    [][]byte
        validate func([]byte) error
        golden   string
    }{
        {
            name: "quick_navigation",
            setup: func(r *exp.TestRunner) error {
                // Setup for quick navigation test
                return nil
            },
            input: [][]byte{
                []byte("j"), // Move down
                []byte("j"), // Move down again
                []byte("k"), // Move up
            },
            validate: func(screen []byte) error {
                if !bytes.Contains(screen, []byte("Menu Item 2")) {
                    return fmt.Errorf("expected 'Menu Item 2' on screen")
                }
                return nil
            },
            golden: "quick_navigation_result",
        },
        {
            name: "form_completion",
            setup: func(r *exp.TestRunner) error {
                // Setup for form completion
                return nil
            },
            input: [][]byte{
                []byte("test input"),
                []byte{13}, // Enter
            },
            validate: func(screen []byte) error {
                if !bytes.Contains(screen, []byte("Success")) {
                    return fmt.Errorf("expected 'Success' message")
                }
                return nil
            },
            golden: "form_completion_result",
        },
    }

    for _, tt := range testCases {
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
            }, exp.WithDuration(3*time.Second))
            require.NoError(t, err)

            if tt.golden != "" {
                exp.RequireEqualSubtest(t, screen, tt.golden)
            }
        })
    }
}
```