# urfave/cli/v3: Complete Guide

urfave/cli is a declarative, simple, fast, and fun package for building command line tools in Go. This guide covers version 3 of the library and provides comprehensive examples and best practices.

## Table of Contents

- [Getting Started](#getting-started)
- [Installation](#installation)
- [Basic Concepts](#basic-concepts)
- [Commands](#commands)
- [Flags](#flags)
- [Arguments](#arguments)
- [Advanced Features](#advanced-features)
- [Error Handling](#error-handling)
- [Shell Completion](#shell-completion)
- [Examples](#examples)
- [Migration from v2](#migration-from-v2)

## Getting Started

### Installation

```bash
go get github.com/urfave/cli/v3
```

### Minimal Example

```go
package main

import (
	"fmt"
	"log"
	"os"
	"context"

	"github.com/urfave/cli/v3"
)

func main() {
	cmd := &cli.Command{
		Name:  "boom",
		Usage: "make an explosive entrance",
		Action: func(context.Context, *cli.Command) error {
			fmt.Println("boom! I say!")
			return nil
		},
	}

	if err := cmd.Run(context.Background(), os.Args); err != nil {
		log.Fatal(err)
	}
}
```

## Basic Concepts

urfave/cli v3 is built around the concept of commands and flags:

- **Command**: Represents an action that can be executed
- **Flag**: Represents a command-line option that modifies behavior
- **Context**: Provides access to parsed arguments, flags, and application state

### Core Structure

Every CLI application is built from a `Command` struct:

```go
type Command struct {
    // Basic identification
    Name        string
    Usage       string
    Description string

    // Execution
    Action func(context.Context, *Command) error

    // Configuration
    Flags     []Flag
    Commands  []*Command

    // Behavior control
    HideHelp              bool
    HideVersion           bool
    EnableShellCompletion bool
}
```

## Commands

### Command Definition

```go
cmd := &cli.Command{
    Name:        "deploy",
    Aliases:     []string{"dep", "dpl"},
    Usage:       "deploy the application",
    Description: "Deploy the application to the specified environment",
    UsageText:   "deploy [environment] [options]",
    ArgsUsage:   "[environment]",

    Action: func(ctx context.Context, cmd *cli.Command) error {
        env := cmd.Args().First()
        fmt.Printf("Deploying to %s environment\n", env)
        return nil
    },

    Before: func(ctx context.Context, cmd *cli.Command) (context.Context, error) {
        fmt.Println("Preparing for deployment...")
        return ctx, nil
    },

    After: func(ctx context.Context, cmd *cli.Command) error {
        fmt.Println("Deployment completed")
        return nil
    },
}
```

### Nested Commands

```go
rootCmd := &cli.Command{
    Name: "app",
    Commands: []*cli.Command{
        {
            Name: "config",
            Commands: []*cli.Command{
                {
                    Name:  "set",
                    Usage: "set a configuration value",
                    Action: setConfigAction,
                },
                {
                    Name:  "get",
                    Usage: "get a configuration value",
                    Action: getConfigAction,
                },
            },
        },
    },
}
```

### Command Categories

```go
cmd := &cli.Command{
    Name: "tool",
    Commands: []*cli.Command{
        {
            Name:     "build",
            Category: "Development",
            Usage:    "build the project",
        },
        {
            Name:     "deploy",
            Category: "Operations",
            Usage:    "deploy the project",
        },
    },
}
```

## Flags

### Basic Flag Types

```go
flags := []cli.Flag{
    // Boolean flag
    &cli.BoolFlag{
        Name:    "verbose",
        Aliases: []string{"v"},
        Usage:   "enable verbose output",
    },

    // String flag with default value
    &cli.StringFlag{
        Name:        "config",
        Aliases:     []string{"c"},
        Usage:       "configuration file path",
        Value:       "config.yaml",
        DefaultText: "config.yaml",
    },

    // Integer flag with validation
    &cli.IntFlag{
        Name: "port",
        Usage: "port number",
        Value: 8080,
        Action: func(ctx context.Context, cmd *cli.Command, v int) error {
            if v < 1 || v > 65535 {
                return fmt.Errorf("port must be between 1 and 65535")
            }
            return nil
        },
    },

    // Duration flag
    &cli.DurationFlag{
        Name:  "timeout",
        Usage: "request timeout",
        Value: time.Second * 30,
    },

    // Float flag
    &cli.FloatFlag{
        Name:  "threshold",
        Usage: "threshold value",
        Value: 0.5,
    },
}
```

### Slice Flags

```go
flags := []cli.Flag{
    // String slice
    &cli.StringSliceFlag{
        Name:    "files",
        Aliases: []string{"f"},
        Usage:   "input files",
    },

    // Integer slice
    &cli.IntSliceFlag{
        Name:  "ports",
        Usage: "multiple ports",
    },

    // Float slice
    &cli.FloatSliceFlag{
        Name:  "coordinates",
        Usage: "GPS coordinates",
    },
}
```

### Advanced Flag Features

#### Flag Categories

```go
flags := []cli.Flag{
    &cli.StringFlag{
        Name:     "host",
        Category: "Connection",
        Usage:    "server host",
    },
    &cli.IntFlag{
        Name:     "port",
        Category: "Connection",
        Usage:    "server port",
    },
    &cli.StringFlag{
        Name:     "username",
        Category: "Authentication",
        Usage:    "username",
    },
}
```

#### Persistent Flags

Flags that are available to subcommands:

```go
flags := []cli.Flag{
    &cli.StringFlag{
        Name:       "global-flag",
        Persistent: true,
        Usage:      "flag available to all subcommands",
    },
}
```

#### Hidden Flags

```go
&cli.StringFlag{
    Name:  "debug-token",
    Usage: "internal debug token",
    Hidden: true,
}
```

## Arguments

### Accessing Arguments

```go
Action: func(ctx context.Context, cmd *cli.Command) error {
    // Get all arguments
    args := cmd.Args()

    // Get first argument
    first := args.First()

    // Get argument by index
    second := args.Get(1)

    // Check if arguments are present
    if args.Present() {
        fmt.Printf("Arguments: %v\n", args.Slice())
    }

    // Get remaining arguments after first
    tail := args.Tail()

    // Count arguments
    count := args.Len()

    return nil
},
```

### Argument Validation

```go
Action: func(ctx context.Context, cmd *cli.Command) error {
    if cmd.NArg() < 2 {
        return fmt.Errorf("requires at least 2 arguments")
    }

    filename := cmd.Args().First()
    if filename == "" {
        return fmt.Errorf("filename is required")
    }

    return nil,
},
```

## Advanced Features

### Context Awareness

```go
Action: func(ctx context.Context, cmd *cli.Command) error {
    // Access context values
    if timeout, ok := ctx.Deadline(); ok {
        fmt.Printf("Command will timeout at: %v\n", timeout)
    }

    // Get command lineage
    lineage := cmd.Lineage()
    fmt.Printf("Command path: %v\n", lineage)

    return nil,
},
```

### Custom Exit Codes

```go
import "github.com/urfave/cli/v3"

Action: func(ctx context.Context, cmd *cli.Command) error {
    if someErrorCondition {
        return cli.Exit("Custom error message", 42)
    }
    return nil,
},
```

### Command and Flag Suggestions

Enable suggestions for mistyped commands and flags:

```go
cmd := &cli.Command{
    Name:    "app",
    Suggest: true,  // Enable suggestions
    Commands: []*cli.Command{
        {
            Name:  "deploy",
            Usage: "deploy application",
        },
    },
}
```

### Custom Error Handling

```go
cmd := &cli.Command{
    CommandNotFound: func(ctx context.Context, cmd *cli.Command, command string) {
        fmt.Fprintf(cmd.Root().Writer, "Unknown command: %s\n", command)
        fmt.Fprintf(cmd.Root().Writer, "Did you mean one of these?\n")
        for _, c := range cmd.VisibleCommands() {
            fmt.Fprintf(cmd.Root().Writer, "  - %s\n", c.Name)
        }
    },

    OnUsageError: func(ctx context.Context, cmd *cli.Command, err error, isSubcommand bool) error {
        if isSubcommand {
            return err
        }
        fmt.Fprintf(cmd.Root().Writer, "Usage error: %v\n", err)
        return nil
    },
}
```

## Error Handling

### Standard Error Handling

```go
Action: func(ctx context.Context, cmd *cli.Command) error {
    file, err := os.Open(cmd.String("file"))
    if err != nil {
        return fmt.Errorf("failed to open file: %w", err)
    }
    defer file.Close()

    // Process file...
    return nil,
},
```

### Custom Error Types

```go
type AppError struct {
    Code    int
    Message string
    Cause   error
}

func (e *AppError) Error() string {
    return e.Message
}

func (e *AppError) Unwrap() error {
    return e.Cause
}

// Usage in action
Action: func(ctx context.Context, cmd *cli.Command) error {
    return &AppError{
        Code:    1001,
        Message: "custom application error",
        Cause:   originalError,
    }
},
```

## Shell Completion

### Enable Shell Completion

```go
cmd := &cli.Command{
    Name:                   "myapp",
    EnableShellCompletion:  true,

    // Custom completion function
    ShellComplete: func(ctx context.Context, cmd *cli.Command) {
        fmt.Fprintf(cmd.Root().Writer, "option1\noption2\noption3\n")
    },
}
```

### Command-Specific Completion

```go
{
    Name:  "add",
    Usage: "add a task",
    ShellComplete: func(ctx context.Context, cmd *cli.Command) {
        // Complete task names
        fmt.Fprintf(cmd.Root().Writer, "bug\nfeature\ndocumentation\n")
    },
}
```

### Generate Completion Scripts

```bash
# Generate fish completion
myapp --generate-shell-completion=fish

# Generate bash completion
myapp --generate-shell-completion=bash

# Generate zsh completion
myapp --generate-shell-completion=zsh
```

## Examples

### Complete Web Server CLI

```go
package main

import (
    "context"
    "fmt"
    "log"
    "net/http"
    "os"
    "time"

    "github.com/urfave/cli/v3"
)

func main() {
    cmd := &cli.Command{
        Name:  "webserver",
        Usage: "a simple web server",
        Description: "A configurable web server with various options",

        Flags: []cli.Flag{
            &cli.StringFlag{
                Name:     "host",
                Aliases:  []string{"H"},
                Value:    "localhost",
                Category: "Server",
                Usage:    "server host",
            },
            &cli.IntFlag{
                Name:     "port",
                Aliases:  []string{"p"},
                Value:    8080,
                Category: "Server",
                Usage:    "server port",
                Action: func(ctx context.Context, cmd *cli.Command, v int) error {
                    if v < 1 || v > 65535 {
                        return fmt.Errorf("port must be between 1 and 65535")
                    }
                    return nil
                },
            },
            &cli.DurationFlag{
                Name:     "timeout",
                Value:    time.Second * 30,
                Category: "Server",
                Usage:    "request timeout",
            },
            &cli.StringFlag{
                Name:     "log-level",
                Value:    "info",
                Category: "Logging",
                Usage:    "log level (debug, info, warn, error)",
            },
            &cli.BoolFlag{
                Name:     "cors",
                Category: "Features",
                Usage:    "enable CORS",
            },
        },

        Commands: []*cli.Command{
            {
                Name:  "start",
                Usage: "start the web server",
                Action: startServer,
            },
            {
                Name:  "version",
                Usage: "show version information",
                Action: func(ctx context.Context, cmd *cli.Command) error {
                    fmt.Println("webserver version 1.0.0")
                    return nil
                },
            },
        },

        EnableShellCompletion: true,
        Suggest:              true,
    }

    if err := cmd.Run(context.Background(), os.Args); err != nil {
        log.Fatal(err)
    }
}

func startServer(ctx context.Context, cmd *cli.Command) error {
    host := cmd.String("host")
    port := cmd.Int("port")
    timeout := cmd.Duration("timeout")
    logLevel := cmd.String("log-level")
    cors := cmd.Bool("cors")

    addr := fmt.Sprintf("%s:%d", host, port)

    fmt.Printf("Starting server on %s\n", addr)
    fmt.Printf("Log level: %s\n", logLevel)
    fmt.Printf("Timeout: %v\n", timeout)
    fmt.Printf("CORS enabled: %v\n", cors)

    server := &http.Server{
        Addr:         addr,
        ReadTimeout:  timeout,
        WriteTimeout: timeout,
    }

    if cors {
        // Add CORS middleware
        server.Handler = corsMiddleware(http.DefaultServeMux)
    }

    return server.ListenAndServe()
}

func corsMiddleware(next http.Handler) http.Handler {
    return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        w.Header().Set("Access-Control-Allow-Origin", "*")
        w.Header().Set("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS")
        w.Header().Set("Access-Control-Allow-Headers", "Content-Type, Authorization")

        if r.Method == "OPTIONS" {
            w.WriteHeader(http.StatusOK)
            return
        }

        next.ServeHTTP(w, r)
    })
}
```

### Configuration Management CLI

```go
package main

import (
    "context"
    "fmt"
    "log"
    "os"
    "path/filepath"

    "github.com/urfave/cli/v3"
)

func main() {
    cmd := &cli.Command{
        Name:  "config",
        Usage: "configuration management tool",

        Flags: []cli.Flag{
            &cli.StringFlag{
                Name:    "config-dir",
                Aliases: []string{"d"},
                Value:   getDefaultConfigDir(),
                Usage:   "configuration directory",
            },
            &cli.StringFlag{
                Name:    "format",
                Aliases: []string{"f"},
                Value:   "yaml",
                Usage:   "configuration format (yaml, json, toml)",
            },
        },

        Commands: []*cli.Command{
            {
                Name:  "set",
                Usage: "set a configuration value",
                UsageText: "config set <key> <value>",
                Action: setConfig,
            },
            {
                Name:  "get",
                Usage: "get a configuration value",
                UsageText: "config get <key>",
                Action: getConfig,
            },
            {
                Name:  "list",
                Usage: "list all configuration values",
                Action: listConfig,
            },
            {
                Name:  "delete",
                Usage: "delete a configuration value",
                UsageText: "config delete <key>",
                Action: deleteConfig,
            },
        },
    }

    if err := cmd.Run(context.Background(), os.Args); err != nil {
        log.Fatal(err)
    }
}

func getDefaultConfigDir() string {
    home, _ := os.UserHomeDir()
    return filepath.Join(home, ".config", "myapp")
}

func setConfig(ctx context.Context, cmd *cli.Command) error {
    args := cmd.Args()
    if args.Len() < 2 {
        return fmt.Errorf("key and value are required")
    }

    key := args.Get(0)
    value := args.Get(1)
    configDir := cmd.String("config-dir")

    fmt.Printf("Setting %s=%s in %s\n", key, value, configDir)
    // Implementation would save to file
    return nil
}

func getConfig(ctx context.Context, cmd *cli.Command) error {
    args := cmd.Args()
    if args.Len() < 1 {
        return fmt.Errorf("key is required")
    }

    key := args.First()
    fmt.Printf("Getting value for key: %s\n", key)
    // Implementation would read from file
    return nil
}

func listConfig(ctx context.Context, cmd *cli.Command) error {
    configDir := cmd.String("config-dir")
    fmt.Printf("Listing configuration from %s\n", configDir)
    // Implementation would list all keys
    return nil
}

func deleteConfig(ctx context.Context, cmd *cli.Command) error {
    args := cmd.Args()
    if args.Len() < 1 {
        return fmt.Errorf("key is required")
    }

    key := args.First()
    fmt.Printf("Deleting key: %s\n", key)
    // Implementation would delete from file
    return nil
}
```

## Migration from v2

### Key Changes in v3

1. **Context Parameter**: Action functions now receive `context.Context` as first parameter
2. **Command Run Method**: Use `cmd.Run(ctx, os.Args)` instead of `app.Run(os.Args)`
3. **Flag Actions**: Updated signature to include context
4. **Improved Error Handling**: Better support for custom exit codes

### Migration Example

#### v2 Code
```go
&cli.App{
    Name: "app",
    Action: func(c *cli.Context) error {
        return doSomething(c.String("flag"))
    },
    Flags: []cli.Flag{
        &cli.StringFlag{Name: "flag"},
    },
}
```

#### v3 Equivalent
```go
&cli.Command{
    Name: "app",
    Action: func(ctx context.Context, c *cli.Command) error {
        return doSomething(c.String("flag"))
    },
    Flags: []cli.Flag{
        &cli.StringFlag{Name: "flag"},
    },
}
```

## Best Practices

1. **Use Context**: Always handle the context parameter properly
2. **Validate Input**: Use flag actions and command-level validation
3. **Provide Good Help**: Use clear usage strings and descriptions
4. **Handle Errors**: Return meaningful errors with proper context
5. **Enable Completion**: Use shell completion for better user experience
6. **Organize Commands**: Use categories and nested commands for complex CLIs
7. **Document Options**: Use environment variables and default values appropriately

## Resources

- [Official urfave/cli Repository](https://github.com/urfave/cli)
- [v3 Documentation](https://github.com/urfave/cli/blob/main/docs/v3/)
- [Examples Repository](https://github.com/urfave/cli/tree/main/docs/v3/examples)
- [Migration Guide](https://github.com/urfave/cli/blob/main/docs/v3/MIGRATION.md)

This documentation provides a comprehensive guide to using urfave/cli v3 for building command-line applications in Go. The library's declarative approach makes it easy to create sophisticated CLI tools with minimal boilerplate code.