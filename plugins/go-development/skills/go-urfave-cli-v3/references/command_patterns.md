# urfave/cli v3 Command Patterns Reference

This document covers common command patterns and best practices for building CLI applications with urfave/cli v3.

## Basic Command Structure

### Simple Command

The most basic command with just an action.

```go
&cli.Command{
    Name:  "ping",
    Usage: "ping the server",
    Action: func(ctx context.Context, cmd *cli.Command) error {
        fmt.Println("pong")
        return nil
    },
}
```

### Command with Flags

Command with configuration flags.

```go
&cli.Command{
    Name:  "deploy",
    Usage: "deploy the application",
    Flags: []cli.Flag{
        &cli.StringFlag{
            Name:     "env",
            Aliases:  []string{"e"},
            Usage:    "deployment environment",
            Value:    "development",
            Required: false,
            Category: "Deployment",
        },
        &cli.BoolFlag{
            Name:     "force",
            Aliases:  []string{"f"},
            Usage:    "force deployment",
            Category: "Deployment",
        },
    },
    Action: func(ctx context.Context, cmd *cli.Command) error {
        env := cmd.String("env")
        force := cmd.Bool("force")
        fmt.Printf("Deploying to %s environment (force: %v)\n", env, force)
        return nil
    },
}
```

### Command with Arguments

Command that processes positional arguments.

```go
&cli.Command{
    Name:      "process",
    Usage:     "process input files",
    ArgsUsage: "[files...]",
    Action: func(ctx context.Context, cmd *cli.Command) error {
        args := cmd.Args()
        if !args.Present() {
            return fmt.Errorf("at least one file is required")
        }

        for _, file := range args.Slice() {
            fmt.Printf("Processing: %s\n", file)
        }
        return nil
    },
}
```

## Advanced Command Patterns

### Command with Lifecycle Hooks

Commands with Before/After hooks for setup and cleanup.

```go
&cli.Command{
    Name:  "backup",
    Usage: "create a backup",
    Before: func(ctx context.Context, cmd *cli.Command) (context.Context, error) {
        fmt.Println("Preparing backup...")
        // Setup backup environment
        return ctx, nil
    },
    Action: func(ctx context.Context, cmd *cli.Command) error {
        fmt.Println("Creating backup...")
        // Backup logic
        return nil
    },
    After: func(ctx context.Context, cmd *cli.Command) error {
        fmt.Println("Cleaning up backup resources...")
        // Cleanup logic
        return nil
    },
}
```

### Command with Custom Error Handling

Commands with custom error handling and exit codes.

```go
&cli.Command{
    Name:  "validate",
    Usage: "validate configuration",
    OnUsageError: func(ctx context.Context, cmd *cli.Command, err error, isSubcommand bool) error {
        if isSubcommand {
            return err
        }
        fmt.Fprintf(cmd.Root().Writer, "Usage error: %v\n", err)
        return nil
    },
    Action: func(ctx context.Context, cmd *cli.Command) error {
        if someCondition {
            return cli.Exit("Validation failed", 1)
        }
        fmt.Println("Validation passed")
        return nil
    },
}
```

### Command with Shell Completion

Command that provides custom shell completion.

```go
&cli.Command{
    Name:  "connect",
    Usage: "connect to a service",
    ShellComplete: func(ctx context.Context, cmd *cli.Command) {
        // Provide completion options
        fmt.Fprintf(cmd.Root().Writer, "production\n")
        fmt.Fprintf(cmd.Root().Writer, "staging\n")
        fmt.Fprintf(cmd.Root().Writer, "development\n")
    },
    Action: func(ctx context.Context, cmd *cli.Command) error {
        service := cmd.Args().First()
        fmt.Printf("Connecting to: %s\n", service)
        return nil
    },
}
```

## Command Organization

### Hierarchical Commands

Organize commands in a logical hierarchy.

```go
app := &cli.Command{
    Name: "myapp",
    Commands: []*cli.Command{
        {
            Name: "database",
            Commands: []*cli.Command{
                {
                    Name:  "migrate",
                    Usage: "run database migrations",
                    Action: migrateAction,
                },
                {
                    Name:  "seed",
                    Usage: "seed database with initial data",
                    Action: seedAction,
                },
                {
                    Name: "backup",
                    Commands: []*cli.Command{
                        {
                            Name:  "create",
                            Usage: "create database backup",
                            Action: createBackupAction,
                        },
                        {
                            Name:  "restore",
                            Usage: "restore database from backup",
                            Action: restoreBackupAction,
                        },
                    },
                },
            },
        },
        {
            Name: "user",
            Commands: []*cli.Command{
                {
                    Name:  "create",
                    Usage: "create a new user",
                    Action: createUserAction,
                },
                {
                    Name:  "delete",
                    Usage: "delete a user",
                    Action: deleteUserAction,
                },
                {
                    Name:  "list",
                    Usage: "list all users",
                    Action: listUsersAction,
                },
            },
        },
    },
}
```

### Command Categories

Group related commands using categories.

```go
&cli.Command{
    Name: "app",
    Commands: []*cli.Command{
        {
            Name:     "build",
            Category: "Development",
            Usage:    "build the application",
        },
        {
            Name:     "test",
            Category: "Development",
            Usage:    "run tests",
        },
        {
            Name:     "deploy",
            Category: "Operations",
            Usage:    "deploy to production",
        },
        {
            Name:     "monitor",
            Category: "Operations",
            Usage:    "monitor application health",
        },
        {
            Name:     "logs",
            Category: "Operations",
            Usage:    "view application logs",
        },
    },
}
```

## Specialized Command Patterns

### Configuration Management CLI

A command that manages configuration files.

```go
&cli.Command{
    Name:  "config",
    Usage: "manage application configuration",
    Flags: []cli.Flag{
        &cli.StringFlag{
            Name:    "format",
            Aliases: []string{"f"},
            Value:   "yaml",
            Usage:   "configuration format (yaml, json, toml)",
        },
    },
    Commands: []*cli.Command{
        {
            Name:      "get",
            Usage:     "get a configuration value",
            ArgsUsage: "<key>",
            Action: func(ctx context.Context, cmd *cli.Command) error {
                key := cmd.Args().First()
                if key == "" {
                    return fmt.Errorf("key is required")
                }
                // Implementation for getting config value
                return nil
            },
        },
        {
            Name:      "set",
            Usage:     "set a configuration value",
            ArgsUsage: "<key> <value>",
            Action: func(ctx context.Context, cmd *cli.Command) error {
                args := cmd.Args()
                if args.Len() < 2 {
                    return fmt.Errorf("key and value are required")
                }
                key := args.Get(0)
                value := args.Get(1)
                // Implementation for setting config value
                return nil
            },
        },
        {
            Name:  "list",
            Usage: "list all configuration values",
            Action: func(ctx context.Context, cmd *cli.Command) error {
                // Implementation for listing config
                return nil
            },
        },
    },
}
```

### Service Management CLI

A command for managing services.

```go
&cli.Command{
    Name:  "service",
    Usage: "manage application services",
    Commands: []*cli.Command{
        {
            Name:  "start",
            Usage: "start the service",
            Flags: []cli.Flag{
                &cli.StringFlag{
                    Name:  "config",
                    Usage: "configuration file",
                },
                &cli.DurationFlag{
                    Name:  "timeout",
                    Value: time.Second * 30,
                    Usage: "startup timeout",
                },
            },
            Action: func(ctx context.Context, cmd *cli.Command) error {
                config := cmd.String("config")
                timeout := cmd.Duration("timeout")
                fmt.Printf("Starting service with config: %s, timeout: %v\n", config, timeout)
                return nil
            },
        },
        {
            Name:  "stop",
            Usage: "stop the service",
            Flags: []cli.Flag{
                &cli.DurationFlag{
                    Name:  "grace-period",
                    Value: time.Second * 10,
                    Usage: "graceful shutdown period",
                },
            },
            Action: func(ctx context.Context, cmd *cli.Command) error {
                gracePeriod := cmd.Duration("grace-period")
                fmt.Printf("Stopping service with grace period: %v\n", gracePeriod)
                return nil
            },
        },
        {
            Name:  "status",
            Usage: "check service status",
            Action: func(ctx context.Context, cmd *cli.Command) error {
                fmt.Println("Service status: Running")
                return nil
            },
        },
        {
            Name:  "restart",
            Usage: "restart the service",
            Action: func(ctx context.Context, cmd *cli.Command) error {
                // Start, then stop
                return nil
            },
        },
    },
}
```

### Interactive Command

A command that provides interactive prompts.

```go
&cli.Command{
    Name:  "interactive",
    Usage: "start interactive mode",
    Flags: []cli.Flag{
        &cli.BoolFlag{
            Name:  "wizard",
            Usage: "use wizard mode",
        },
    },
    Action: func(ctx context.Context, cmd *cli.Command) error {
        wizard := cmd.Bool("wizard")

        if wizard {
            return runWizard(ctx, cmd)
        }

        return runInteractive(ctx, cmd)
    },
}

func runWizard(ctx context.Context, cmd *cli.Command) error {
    reader := bufio.NewReader(os.Stdin)

    fmt.Print("Enter your name: ")
    name, _ := reader.ReadString('\n')

    fmt.Print("Enter your email: ")
    email, _ := reader.ReadString('\n')

    fmt.Printf("Hello %s (%s)!\n", strings.TrimSpace(name), strings.TrimSpace(email))
    return nil
}
```

## Command Best Practices

### Input Validation

Validate arguments and flags in actions.

```go
Action: func(ctx context.Context, cmd *cli.Command) error {
    // Validate required arguments
    if cmd.NArg() < 2 {
        return fmt.Errorf("requires at least 2 arguments")
    }

    // Validate flag values
    port := cmd.Int("port")
    if port < 1 || port > 65535 {
        return fmt.Errorf("port must be between 1 and 65535")
    }

    // Validate file existence
    config := cmd.String("config")
    if _, err := os.Stat(config); os.IsNotExist(err) {
        return fmt.Errorf("config file not found: %s", config)
    }

    return nil
},
```

### Error Handling

Provide meaningful error messages.

```go
Action: func(ctx context.Context, cmd *cli.Command) error {
    result, err := someOperation()
    if err != nil {
        return fmt.Errorf("failed to perform operation: %w", err)
    }

    if result.Status == "error" {
        return cli.Exit(result.Message, 1)
    }

    fmt.Printf("Operation completed: %s\n", result.Message)
    return nil
},
```

### Progress Reporting

Show progress for long-running operations.

```go
Action: func(ctx context.Context, cmd *cli.Command) error {
    tasks := []string{"task1", "task2", "task3"}

    for i, task := range tasks {
        fmt.Printf("[%d/%d] Processing %s...\n", i+1, len(tasks), task)

        if err := processTask(ctx, task); err != nil {
            return fmt.Errorf("failed to process %s: %w", task, err)
        }

        fmt.Printf("✓ Completed %s\n", task)
    }

    fmt.Println("All tasks completed successfully")
    return nil
},
```

### Context Awareness

Use context for cancellation and timeouts.

```go
Action: func(ctx context.Context, cmd *cli.Command) error {
    timeout := cmd.Duration("timeout")

    ctx, cancel := context.WithTimeout(ctx, timeout)
    defer cancel()

    done := make(chan error, 1)

    go func() {
        done <- longRunningOperation(ctx)
    }()

    select {
    case err := <-done:
        if err != nil {
            return fmt.Errorf("operation failed: %w", err)
        }
        fmt.Println("Operation completed successfully")

    case <-ctx.Done():
        return cli.Exit("Operation timed out", 1)
    }

    return nil
},
```

## Command Testing

### Testing Commands

Test command actions using a table-driven approach.

```go
func TestDeployCommand(t *testing.T) {
    tests := []struct {
        name     string
        args     []string
        expected string
        wantErr  bool
    }{
        {
            name:     "default environment",
            args:     []string{"deploy"},
            expected: "Deploying to development environment (force: false)",
            wantErr:  false,
        },
        {
            name:     "production deployment",
            args:     []string{"deploy", "--env", "production"},
            expected: "Deploying to production environment (force: false)",
            wantErr:  false,
        },
        {
            name:     "force deployment",
            args:     []string{"deploy", "--force"},
            expected: "Deploying to development environment (force: true)",
            wantErr:  false,
        },
    }

    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            buf := new(bytes.Buffer)

            cmd := createDeployCommand()
            cmd.Writer = buf

            err := cmd.Run(context.Background(), tt.args)

            if (err != nil) != tt.wantErr {
                t.Errorf("Run() error = %v, wantErr %v", err, tt.wantErr)
                return
            }

            if !tt.wantErr && !strings.Contains(buf.String(), tt.expected) {
                t.Errorf("Expected output to contain %q, got %q", tt.expected, buf.String())
            }
        })
    }
}
```