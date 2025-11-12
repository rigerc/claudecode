package main

import (
    "bufio"
    "context"
    "fmt"
    "log"
    "os"
    "strings"
    "time"

    "github.com/urfave/cli/v3"
)

func main() {
    cmd := &cli.Command{
        Name:        "{{.AppName}}",
        Description: "{{.Description}}",
        Usage:       "{{.Usage}}",
        Version:     "{{.Version}}",
        Authors: []any{
            &cli.Author{
                Name:  "{{.Author}}",
                Email: "{{.Email}}",
            },
        },
        Copyright: "© {{.Year}} {{.Company}}",

        Flags: []cli.Flag{
            // Configuration flags
            &cli.StringFlag{
                Name:        "config",
                Aliases:     []string{"c"},
                Usage:       "configuration file path",
                Value:       "config.yaml",
                DefaultText: "config.yaml",
                EnvVars:     []string{"APP_CONFIG", "CONFIG"},
                Category:    "Configuration",
                Persistent:  true,
            },
            &cli.StringFlag{
                Name:        "log-level",
                Aliases:     []string{"l"},
                Usage:       "logging level",
                Value:       "info",
                DefaultText: "info",
                Category:    "Configuration",
                Action: func(ctx context.Context, cmd *cli.Command, v string) error {
                    levels := []string{"debug", "info", "warn", "error"}
                    for _, level := range levels {
                        if v == level {
                            return nil
                        }
                    }
                    return fmt.Errorf("invalid log level: %s (must be one of: %s)", v, strings.Join(levels, ", "))
                },
                Persistent: true,
            },

            // Server configuration
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
                Usage:    "operation timeout",
            },

            // Feature flags
            &cli.BoolFlag{
                Name:     "cors",
                Category: "Features",
                Usage:    "enable CORS",
            },
            &cli.BoolFlag{
                Name:     "metrics",
                Category: "Features",
                Usage:    "enable metrics collection",
            },
            &cli.BoolFlag{
                Name:     "debug",
                Category: "Features",
                Usage:    "enable debug mode",
                Hidden:   true,
            },

            // Output options
            &cli.StringFlag{
                Name:     "output",
                Aliases:  []string{"o"},
                Value:    "table",
                Category: "Output",
                Usage:    "output format (table, json, yaml)",
            },
            &cli.BoolFlag{
                Name:     "quiet",
                Aliases:  []string{"q"},
                Category: "Output",
                Usage:    "suppress output",
            },

            // Advanced options
            &cli.IntSliceFlag{
                Name:     "workers",
                Value:    cli.NewIntSlice(4),
                Category: "Performance",
                Usage:    "number of worker goroutines",
            },
        },

        Commands: []*cli.Command{
            {
                Name:        "server",
                Usage:       "server operations",
                Description: "Commands for server management",
                Category:    "Operations",

                Commands: []*cli.Command{
                    {
                        Name:  "start",
                        Usage: "start the server",
                        Flags: []cli.Flag{
                            &cli.BoolFlag{
                                Name:  "daemon",
                                Usage: "run as daemon",
                            },
                            &cli.StringFlag{
                                Name:  "pid-file",
                                Usage: "PID file path",
                            },
                        },
                        Action: func(ctx context.Context, cmd *cli.Command) error {
                            host := cmd.String("host")
                            port := cmd.Int("port")
                            timeout := cmd.Duration("timeout")
                            cors := cmd.Bool("cors")
                            debug := cmd.Bool("debug")
                            daemon := cmd.Bool("daemon")

                            addr := fmt.Sprintf("%s:%d", host, port)

                            fmt.Printf("Starting server at %s\n", addr)
                            fmt.Printf("Timeout: %v\n", timeout)
                            fmt.Printf("CORS: %v\n", cors)
                            fmt.Printf("Debug: %v\n", debug)
                            fmt.Printf("Daemon: %v\n", daemon)

                            if daemon {
                                fmt.Println("Running in daemon mode...")
                            }

                            return nil
                        },
                        Before: func(ctx context.Context, cmd *cli.Command) (context.Context, error) {
                            fmt.Println("Initializing server...")
                            return ctx, nil
                        },
                        After: func(ctx context.Context, cmd *cli.Command) error {
                            fmt.Println("Server started successfully")
                            return nil
                        },
                    },
                    {
                        Name:  "stop",
                        Usage: "stop the server",
                        Flags: []cli.Flag{
                            &cli.DurationFlag{
                                Name:  "grace-period",
                                Value: time.Second * 10,
                                Usage: "graceful shutdown period",
                            },
                        },
                        Action: func(ctx context.Context, cmd *cli.Command) error {
                            gracePeriod := cmd.Duration("grace-period")
                            fmt.Printf("Stopping server with grace period: %v\n", gracePeriod)
                            return nil
                        },
                    },
                    {
                        Name:  "status",
                        Usage: "check server status",
                        Action: func(ctx context.Context, cmd *cli.Command) error {
                            fmt.Println("Server Status:")
                            fmt.Println("  State: Running")
                            fmt.Println("  Uptime: 2h 15m 30s")
                            fmt.Println("  Connections: 42")
                            return nil
                        },
                    },
                },
            },
            {
                Name:        "database",
                Usage:       "database operations",
                Description: "Commands for database management",
                Category:    "Data",

                Commands: []*cli.Command{
                    {
                        Name:  "migrate",
                        Usage: "run database migrations",
                        Flags: []cli.Flag{
                            &cli.StringFlag{
                                Name:  "version",
                                Usage: "migrate to specific version",
                            },
                            &cli.BoolFlag{
                                Name:  "dry-run",
                                Usage: "show what would be migrated",
                            },
                        },
                        Action: func(ctx context.Context, cmd *cli.Command) error {
                            version := cmd.String("version")
                            dryRun := cmd.Bool("dry-run")

                            if dryRun {
                                fmt.Println("DRY RUN: Would run migrations")
                            } else {
                                fmt.Printf("Running migrations to version: %s\n", version)
                            }
                            return nil
                        },
                    },
                    {
                        Name:  "backup",
                        Usage: "create database backup",
                        Flags: []cli.Flag{
                            &cli.StringFlag{
                                Name:  "output",
                                Usage: "backup output file",
                            },
                            &cli.BoolFlag{
                                Name:  "compress",
                                Usage: "compress backup",
                            },
                        },
                        Action: func(ctx context.Context, cmd *cli.Command) error {
                            output := cmd.String("output")
                            compress := cmd.Bool("compress")

                            fmt.Printf("Creating database backup to: %s\n", output)
                            fmt.Printf("Compression: %v\n", compress)
                            return nil
                        },
                    },
                },
            },
            {
                Name:  "interactive",
                Usage: "start interactive mode",
                Flags: []cli.Flag{
                    &cli.BoolFlag{
                        Name:  "wizard",
                        Usage: "use setup wizard",
                    },
                },
                Action: func(ctx context.Context, cmd *cli.Command) error {
                    wizard := cmd.Bool("wizard")

                    if wizard {
                        return runSetupWizard(ctx, cmd)
                    }

                    return runInteractiveShell(ctx, cmd)
                },
            },
        },

        // Application features
        EnableShellCompletion: true,
        Suggest:              true,
        HideHelp:             false,
        HideVersion:          false,

        // Shell completion
        ShellComplete: func(ctx context.Context, cmd *cli.Command) {
            fmt.Fprintf(cmd.Root().Writer, "server\n")
            fmt.Fprintf(cmd.Root().Writer, "database\n")
            fmt.Fprintf(cmd.Root().Writer, "interactive\n")
        },

        // Error handling
        CommandNotFound: func(ctx context.Context, cmd *cli.Command, command string) {
            fmt.Fprintf(cmd.Root().Writer, "Unknown command: %s\n", command)
            fmt.Fprintf(cmd.Root().Writer, "Did you mean one of these?\n")
            for _, c := range cmd.VisibleCommands() {
                if strings.Contains(c.Name, command) || strings.Contains(command, c.Name) {
                    fmt.Fprintf(cmd.Root().Writer, "  - %s\n", c.Name)
                }
            }
        },

        OnUsageError: func(ctx context.Context, cmd *cli.Command, err error, isSubcommand bool) error {
            if isSubcommand {
                return err
            }
            fmt.Fprintf(cmd.Root().Writer, "Usage error: %v\n", err)
            fmt.Fprintf(cmd.Root().Writer, "Use --help for usage information\n")
            return nil
        },

        // Application lifecycle hooks
        Before: func(ctx context.Context, cmd *cli.Command) (context.Context, error) {
            config := cmd.String("config")
            logLevel := cmd.String("log-level")

            fmt.Printf("Loading configuration from: %s\n", config)
            fmt.Printf("Log level: %s\n", logLevel)

            // Validate config file exists
            if _, err := os.Stat(config); os.IsNotExist(err) {
                fmt.Printf("Warning: Config file not found: %s\n", config)
            }

            return ctx, nil
        },

        After: func(ctx context.Context, cmd *cli.Command) error {
            fmt.Println("Cleanup completed")
            return nil
        },

        // Default action
        Action: func(ctx context.Context, cmd *cli.Command) error {
            if cmd.Bool("quiet") {
                return nil
            }

            fmt.Printf("Welcome to %s v%s\n", cmd.Name, cmd.Version)
            fmt.Println("Use --help for usage information")
            fmt.Println("Available commands:")

            for _, subcmd := range cmd.VisibleCommands() {
                fmt.Printf("  %-12s %s\n", subcmd.Name, subcmd.Usage)
            }

            return nil
        },
    }

    if err := cmd.Run(context.Background(), os.Args); err != nil {
        log.Fatal(err)
    }
}

func runSetupWizard(ctx context.Context, cmd *cli.Command) error {
    reader := bufio.NewReader(os.Stdin)

    fmt.Println("=== Setup Wizard ===")
    fmt.Println("This wizard will help you configure the application")

    fmt.Print("Server host (default: localhost): ")
    host, _ := reader.ReadString('\n')
    host = strings.TrimSpace(host)
    if host == "" {
        host = "localhost"
    }

    fmt.Print("Server port (default: 8080): ")
    portStr, _ := reader.ReadString('\n')
    portStr = strings.TrimSpace(portStr)
    if portStr == "" {
        portStr = "8080"
    }

    fmt.Print("Enable CORS? (y/N): ")
    corsStr, _ := reader.ReadString('\n')
    cors := strings.ToLower(strings.TrimSpace(corsStr)) == "y"

    fmt.Printf("\nConfiguration Summary:\n")
    fmt.Printf("  Host: %s\n", host)
    fmt.Printf("  Port: %s\n", portStr)
    fmt.Printf("  CORS: %v\n", cors)

    fmt.Print("\nSave configuration? (y/N): ")
    saveStr, _ := reader.ReadString('\n')
    if strings.ToLower(strings.TrimSpace(saveStr)) == "y" {
        fmt.Println("Configuration saved!")
    }

    return nil
}

func runInteractiveShell(ctx context.Context, cmd *cli.Command) error {
    reader := bufio.NewReader(os.Stdin)

    fmt.Println("=== Interactive Shell ===")
    fmt.Println("Type 'help' for available commands, 'exit' to quit")

    for {
        fmt.Print("> ")
        input, _ := reader.ReadString('\n')
        input = strings.TrimSpace(input)

        switch input {
        case "help":
            fmt.Println("Available commands:")
            fmt.Println("  status - Show application status")
            fmt.Println("  config - Show configuration")
            fmt.Println("  exit   - Exit interactive shell")

        case "status":
            fmt.Println("Application Status:")
            fmt.Println("  State: Running")
            fmt.Println("  Uptime: 2h 15m 30s")

        case "config":
            fmt.Println("Configuration:")
            fmt.Printf("  Config: %s\n", cmd.String("config"))
            fmt.Printf("  Host: %s\n", cmd.String("host"))
            fmt.Printf("  Port: %d\n", cmd.Int("port"))

        case "exit", "quit":
            fmt.Println("Goodbye!")
            return nil

        case "":
            // Empty input, continue

        default:
            fmt.Printf("Unknown command: %s\n", input)
            fmt.Println("Type 'help' for available commands")
        }
    }
}