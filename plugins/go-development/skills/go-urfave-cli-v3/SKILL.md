---
name: go-urfave-cli-v3
description: Use when building Go CLI applications with urfave/cli v3. Provides code generation, templates, migration tools, and reference documentation for command-line tools.
---

# Go Urfave CLI v3 Expert

Expert assistance for building Go command-line applications using urfave/cli v3.

## When to Use This Skill

- Building new CLI applications in Go
- Adding command-line interfaces to existing applications
- Migrating from urfave/cli v2 to v3
- Implementing flags, commands, and subcommands
- Learning urfave/cli v3 patterns and best practices

## Quick Start

```go
import (
    "context"
    "github.com/urfave/cli/v3"
)

cmd := &cli.Command{
    Name: "mytool",
    Action: func(ctx context.Context, cmd *cli.Command) error {
        // Your logic here
        return nil
    },
}
cmd.Run(context.Background(), os.Args)
```

## Code Generation

```bash
# Generate basic app
python3 scripts/generate_cli.py myapp "Description"

# Generate with subcommands
python3 scripts/generate_cli.py mytool "Description" --type subcommands --commands build test
```

## Available Resources

See `references/` for comprehensive documentation:

- **flag_types.md**: Flag types and validation patterns
- **command_patterns.md**: CLI patterns and best practices
- **workflows.md**: Step-by-step workflow guides
- **migration.md**: v2 to v3 migration guide

See `assets/templates/` for ready-to-use code templates.
