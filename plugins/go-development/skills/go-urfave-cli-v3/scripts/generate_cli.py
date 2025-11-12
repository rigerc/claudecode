#!/usr/bin/env python3
"""
Generate Go CLI application boilerplate using urfave/cli/v3.
This script creates a complete CLI application structure with commands, flags, and features.
"""

import argparse
import os
import sys
from pathlib import Path

def generate_basic_app(name: str, description: str, author: str = "") -> str:
    """Generate a basic CLI application template."""
    template = f'''package main

import (
    "context"
    "fmt"
    "log"
    "os"

    "github.com/urfave/cli/v3"
)

func main() {{
    cmd := &cli.Command{{
        Name:        "{name.lower().replace(' ', '-')}",
        Description: "{description}",
        Authors: []any{{
            &cli.Author{{
                Name:  "{author}",
                Email: "",
            }},
        }},
        Action: func(ctx context.Context, cmd *cli.Command) error {{
            fmt.Println("Hello from {name}!")
            return nil
        }},
    }}

    if err := cmd.Run(context.Background(), os.Args); err != nil {{
        log.Fatal(err)
    }}
}}
'''
    return template

def generate_app_with_subcommands(name: str, description: str, commands: list) -> str:
    """Generate a CLI application with subcommands."""
    command_definitions = ""
    for cmd in commands:
        command_definitions += f'''        {{
            Name:        "{cmd['name']}",
            Aliases:     []string{{{cmd.get('aliases', '')}}},
            Usage:       "{cmd.get('usage', cmd['name'])}",
            Description: "{cmd.get('description', '')}",
            Action: func(ctx context.Context, cmd *cli.Command) error {{
                fmt.Println("Executing {cmd['name']}")
                return nil
            }},
        }},
'''

    template = f'''package main

import (
    "context"
    "fmt"
    "log"
    "os"

    "github.com/urfave/cli/v3"
)

func main() {{
    cmd := &cli.Command{{
        Name:        "{name.lower().replace(' ', '-')}",
        Description: "{description}",
        Commands: []*cli.Command{{{command_definitions}
        }},
        Action: func(ctx context.Context, cmd *cli.Command) error {{
            fmt.Println("Use a subcommand to proceed")
            return nil
        }},
    }}

    if err := cmd.Run(context.Background(), os.Args); err != nil {{
        log.Fatal(err)
    }}
}}
'''
    return template

def generate_advanced_app(name: str, description: str) -> str:
    """Generate an advanced CLI application with features."""
    template = f'''package main

import (
    "context"
    "fmt"
    "log"
    "os"
    "time"

    "github.com/urfave/cli/v3"
)

func main() {{
    cmd := &cli.Command{{
        Name:        "{name.lower().replace(' ', '-')}",
        Description: "{description}",
        Version:     "1.0.0",

        Flags: []cli.Flag{{
            &cli.StringFlag{{
                Name:     "config",
                Aliases:  []string{{"c"}},
                Usage:    "configuration file path",
                Category: "Configuration",
            }},
            &cli.BoolFlag{{
                Name:     "verbose",
                Aliases:  []string{{"v"}},
                Usage:    "enable verbose output",
                Category: "Output",
            }},
            &cli.DurationFlag{{
                Name:     "timeout",
                Aliases:  []string{{"t"}},
                Value:    time.Second * 30,
                Usage:    "operation timeout",
                Category: "Configuration",
            }},
        }},

        Commands: []*cli.Command{{
            {{
                Name:        "start",
                Usage:       "start the service",
                Description: "Start the {name.lower()} service",
                Action: func(ctx context.Context, cmd *cli.Command) error {{
                    config := cmd.String("config")
                    verbose := cmd.Bool("verbose")
                    timeout := cmd.Duration("timeout")

                    fmt.Printf("Starting service with config: %s\\n", config)
                    if verbose {{
                        fmt.Println("Verbose mode enabled")
                    }}
                    fmt.Printf("Timeout: %v\\n", timeout)
                    return nil
                }},
            }},
            {{
                Name:        "status",
                Usage:       "check service status",
                Description: "Display the current status of the {name.lower()} service",
                Action: func(ctx context.Context, cmd *cli.Command) error {{
                    fmt.Println("Service status: Running")
                    return nil
                }},
            }},
        }},

        EnableShellCompletion: true,
        Suggest:              true,

        Before: func(ctx context.Context, cmd *cli.Command) (context.Context, error) {{
            fmt.Println("Initializing {name}...")
            return ctx, nil
        }},

        After: func(ctx context.Context, cmd *cli.Command) error {{
            fmt.Println("Cleanup completed")
            return nil
        }},
    }}

    if err := cmd.Run(context.Background(), os.Args); err != nil {{
        log.Fatal(err)
    }}
}}
'''
    return template

def main():
    parser = argparse.ArgumentParser(description="Generate Go CLI application using urfave/cli v3")
    parser.add_argument("name", help="Application name")
    parser.add_argument("description", help="Application description")
    parser.add_argument("--author", default="", help="Author name")
    parser.add_argument("--type", choices=["basic", "subcommands", "advanced"],
                       default="basic", help="Type of CLI application")
    parser.add_argument("--commands", nargs="+", help="Subcommands (for subcommands type)")
    parser.add_argument("--output", "-o", help="Output file path")
    parser.add_argument("--overwrite", action="store_true", help="Overwrite existing file")

    args = parser.parse_args()

    # Generate content based on type
    if args.type == "basic":
        content = generate_basic_app(args.name, args.description, args.author)
    elif args.type == "subcommands":
        if not args.commands:
            print("Error: --commands required for subcommands type")
            sys.exit(1)
        commands = [{"name": cmd} for cmd in args.commands]
        content = generate_app_with_subcommands(args.name, args.description, commands)
    elif args.type == "advanced":
        content = generate_advanced_app(args.name, args.description)

    # Determine output path
    if args.output:
        output_path = args.output
    else:
        output_path = f"{args.name.lower().replace(' ', '-')}.go"

    # Check if file exists
    if os.path.exists(output_path) and not args.overwrite:
        response = input(f"File {output_path} exists. Overwrite? (y/N): ")
        if response.lower() != 'y':
            print("Aborted")
            sys.exit(0)

    # Write file
    with open(output_path, 'w') as f:
        f.write(content)

    print(f"✅ Generated {args.type} CLI application: {output_path}")
    print("\nNext steps:")
    print("1. Run: go mod init <module-name>")
    print("2. Run: go get github.com/urfave/cli/v3")
    print("3. Run: go run " + output_path)

if __name__ == "__main__":
    main()