package main

import (
    "context"
    "fmt"
    "log"
    "os"

    "github.com/urfave/cli/v3"
)

func main() {
    cmd := &cli.Command{
        Name:        "{{.AppName}}",
        Description: "{{.Description}}",
        Usage:       "{{.Usage}}",
        {{if .Version}}
        Version:     "{{.Version}}",
        {{end}}

        // Global flags available to all subcommands
        Flags: []cli.Flag{
            &cli.StringFlag{
                Name:     "config",
                Aliases:  []string{"c"},
                Usage:    "configuration file path",
                Category: "Global",
            },
            &cli.BoolFlag{
                Name:     "verbose",
                Aliases:  []string{"v"},
                Usage:    "enable verbose output",
                Category: "Global",
            },
        },

        Commands: []*cli.Command{
            {
                Name:        "user",
                Usage:       "manage users",
                Description: "Commands for user management",
                Category:    "Management",

                Commands: []*cli.Command{
                    {
                        Name:      "create",
                        Usage:     "create a new user",
                        ArgsUsage: "<username>",
                        Action: func(ctx context.Context, cmd *cli.Command) error {
                            username := cmd.Args().First()
                            if username == "" {
                                return fmt.Errorf("username is required")
                            }
                            fmt.Printf("Creating user: %s\n", username)
                            return nil
                        },
                    },
                    {
                        Name:      "delete",
                        Usage:     "delete a user",
                        ArgsUsage: "<username>",
                        Flags: []cli.Flag{
                            &cli.BoolFlag{
                                Name:  "force",
                                Usage: "force delete without confirmation",
                            },
                        },
                        Action: func(ctx context.Context, cmd *cli.Command) error {
                            username := cmd.Args().First()
                            force := cmd.Bool("force")
                            if username == "" {
                                return fmt.Errorf("username is required")
                            }
                            fmt.Printf("Deleting user: %s (force: %v)\n", username, force)
                            return nil
                        },
                    },
                    {
                        Name:  "list",
                        Usage: "list all users",
                        Flags: []cli.Flag{
                            &cli.StringFlag{
                                Name:  "format",
                                Value: "table",
                                Usage: "output format (table, json, yaml)",
                            },
                        },
                        Action: func(ctx context.Context, cmd *cli.Command) error {
                            format := cmd.String("format")
                            fmt.Printf("Listing users in format: %s\n", format)
                            return nil
                        },
                    },
                },
            },
            {
                Name:        "config",
                Usage:       "manage configuration",
                Description: "Commands for configuration management",
                Category:    "Configuration",

                Commands: []*cli.Command{
                    {
                        Name:      "get",
                        Usage:     "get configuration value",
                        ArgsUsage: "<key>",
                        Action: func(ctx context.Context, cmd *cli.Command) error {
                            key := cmd.Args().First()
                            if key == "" {
                                return fmt.Errorf("key is required")
                            }
                            fmt.Printf("Getting config for key: %s\n", key)
                            return nil
                        },
                    },
                    {
                        Name:      "set",
                        Usage:     "set configuration value",
                        ArgsUsage: "<key> <value>",
                        Action: func(ctx context.Context, cmd *cli.Command) error {
                            args := cmd.Args()
                            if args.Len() < 2 {
                                return fmt.Errorf("key and value are required")
                            }
                            key := args.Get(0)
                            value := args.Get(1)
                            fmt.Printf("Setting config: %s = %s\n", key, value)
                            return nil
                        },
                    },
                    {
                        Name:  "show",
                        Usage: "show all configuration",
                        Flags: []cli.Flag{
                            &cli.BoolFlag{
                                Name:  "secrets",
                                Usage: "include secret values in output",
                            },
                        },
                        Action: func(ctx context.Context, cmd *cli.Command) error {
                            showSecrets := cmd.Bool("secrets")
                            fmt.Printf("Showing configuration (secrets: %v)\n", showSecrets)
                            return nil
                        },
                    },
                },
            },
            {
                Name:        "server",
                Usage:       "server management",
                Description: "Commands for server operations",
                Category:    "Operations",

                Commands: []*cli.Command{
                    {
                        Name:  "start",
                        Usage: "start the server",
                        Flags: []cli.Flag{
                            &cli.IntFlag{
                                Name:  "port",
                                Value: 8080,
                                Usage: "server port",
                            },
                            &cli.DurationFlag{
                                Name:  "timeout",
                                Value: 0,
                                Usage: "server timeout",
                            },
                        },
                        Action: func(ctx context.Context, cmd *cli.Command) error {
                            port := cmd.Int("port")
                            timeout := cmd.Duration("timeout")
                            fmt.Printf("Starting server on port %d (timeout: %v)\n", port, timeout)
                            return nil
                        },
                    },
                    {
                        Name:  "stop",
                        Usage: "stop the server",
                        Flags: []cli.Flag{
                            &cli.DurationFlag{
                                Name:  "grace-period",
                                Value: 0,
                                Usage: "graceful shutdown period",
                            },
                        },
                        Action: func(ctx context.Context, cmd *cli.Command) error {
                            gracePeriod := cmd.Duration("grace-period")
                            fmt.Printf("Stopping server (grace period: %v)\n", gracePeriod)
                            return nil
                        },
                    },
                    {
                        Name:  "status",
                        Usage: "check server status",
                        Action: func(ctx context.Context, cmd *cli.Command) error {
                            fmt.Println("Server status: Running")
                            return nil
                        },
                    },
                },
            },
        },

        // Enable shell completion
        EnableShellCompletion: true,
        Suggest:              true,

        // Application lifecycle hooks
        Before: func(ctx context.Context, cmd *cli.Command) (context.Context, error) {
            config := cmd.String("config")
            verbose := cmd.Bool("verbose")

            if verbose {
                fmt.Printf("Starting %s with config: %s\n", cmd.Name, config)
            }
            return ctx, nil
        },

        After: func(ctx context.Context, cmd *cli.Command) error {
            fmt.Println("Operation completed")
            return nil
        },

        // Default action when no subcommand is specified
        Action: func(ctx context.Context, cmd *cli.Command) error {
            fmt.Println("Use a subcommand to proceed")
            fmt.Println("Available commands:")
            for _, subcmd := range cmd.VisibleCommands() {
                fmt.Printf("  %s - %s\n", subcmd.Name, subcmd.Usage)
            }
            return nil
        },
    }

    if err := cmd.Run(context.Background(), os.Args); err != nil {
        log.Fatal(err)
    }
}