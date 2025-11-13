# Migration Guide: urfave/cli v2 to v3

## Overview

This guide covers migrating from urfave/cli v2 to v3 using the automated migration tool and manual migration steps.

## Automated Migration Tool

### v2 to v3 Migrator (`scripts/v2_to_v3_migrator.py`)

The automated migration tool handles common migration patterns:

```bash
# Migrate specific files
python3 scripts/v2_to_v3_migrator.py main.go cmd/*.go

# Dry run to preview changes
python3 scripts/v2_to_v3_migrator.py --dry-run main.go

# Migrate without creating backups
python3 scripts/v2_to_v3_migrator.py --no-backup main.go
```

### What the Migrator Changes

1. **Import statements**: `github.com/urfave/cli/v2` → `github.com/urfave/cli/v3`

2. **App creation**: `cli.App{}` → `cli.Command{}`

3. **Action functions**: Adds `context.Context` parameter
   ```go
   // v2
   Action: func(c *cli.Context) error {

   // v3
   Action: func(ctx context.Context, c *cli.Command) error {
   ```

4. **Flag actions**: Updates signature with context
   ```go
   // v2
   Action: func(c *cli.Context, value string) error {

   // v3
   Action: func(ctx context.Context, c *cli.Command, value string) error {
   ```

5. **Function calls**: Updates app run calls
   ```go
   // v2
   c.App.Run(os.Args)

   // v3
   cmd.Run(context.Background(), os.Args)
   ```

## Manual Migration Steps

### 1. Update Imports

Replace:
```go
import "github.com/urfave/cli/v2"
```

With:
```go
import "github.com/urfave/cli/v3"
```

### 2. Change App to Command

Replace:
```go
app := &cli.App{
    Name:  "myapp",
    Usage: "My application",
    Action: func(c *cli.Context) error {
        // ...
    },
}
```

With:
```go
cmd := &cli.Command{
    Name:  "myapp",
    Usage: "My application",
    Action: func(ctx context.Context, c *cli.Command) error {
        // ...
    },
}
```

### 3. Add Context Parameter

All action functions now receive a `context.Context` as the first parameter:

```go
// v2
Action: func(c *cli.Context) error {
    name := c.String("name")
    return nil
}

// v3
Action: func(ctx context.Context, c *cli.Command) error {
    name := c.String("name")
    return nil
}
```

### 4. Update App Run Calls

Replace:
```go
if err := app.Run(os.Args); err != nil {
    log.Fatal(err)
}
```

With:
```go
if err := cmd.Run(context.Background(), os.Args); err != nil {
    log.Fatal(err)
}
```

### 5. Update Flag Actions

Flag actions also receive a context parameter:

```go
// v2
&cli.StringFlag{
    Name: "config",
    Action: func(c *cli.Context, value string) error {
        // ...
    },
}

// v3
&cli.StringFlag{
    Name: "config",
    Action: func(ctx context.Context, c *cli.Command, value string) error {
        // ...
    },
}
```

### 6. Update Before/After Hooks

```go
// v2
Before: func(c *cli.Context) error {
    // ...
}

// v3
Before: func(ctx context.Context, c *cli.Command) error {
    // ...
}
```

## Common Migration Issues

### Issue 1: Missing Context Parameter

**Error**: `cannot use func literal as cli.ActionFunc value`

**Solution**: Add `context.Context` as first parameter to action functions

### Issue 2: App vs Command

**Error**: `undefined: cli.App`

**Solution**: Change `cli.App` to `cli.Command`

### Issue 3: Run Method Signature

**Error**: `not enough arguments in call to cmd.Run`

**Solution**: Add `context.Background()` as first argument to `Run()`

### Issue 4: Flag Type Changes

Some flag types may have changed their struct fields or methods. Check the flag_types.md reference for updated field names.

## Testing After Migration

1. **Compile the application**:
   ```bash
   go build
   ```

2. **Run tests**:
   ```bash
   go test ./...
   ```

3. **Test CLI functionality**:
   ```bash
   # Test help
   ./myapp --help

   # Test commands
   ./myapp subcommand --flag value

   # Test error cases
   ./myapp invalid-command
   ```

4. **Verify context handling**:
   - Test with timeouts
   - Test cancellation behavior
   - Verify cleanup in Before/After hooks

## Resources

- Migration tool: `scripts/v2_to_v3_migrator.py`
- Flag reference: `references/flag_types.md`
- Command patterns: `references/command_patterns.md`
- Example workflows: `references/workflows.md`
