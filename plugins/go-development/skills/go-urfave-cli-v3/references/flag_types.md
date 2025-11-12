# urfave/cli v3 Flag Types Reference

This document provides comprehensive reference for all available flag types in urfave/cli v3 with examples.

## Basic Flag Types

### BoolFlag

Boolean flags represent on/off or true/false values.

```go
&cli.BoolFlag{
    Name:     "verbose",
    Aliases:  []string{"v"},
    Usage:    "enable verbose output",
    Value:    false,  // default value
    Required: false,
    Hidden:   false,
    Category: "Output",
}
```

**Usage:**
```bash
myapp --verbose
myapp -v
myapp --verbose=false
```

### StringFlag

String flags accept text values.

```go
&cli.StringFlag{
    Name:         "config",
    Aliases:      []string{"c"},
    Usage:        "configuration file path",
    Value:        "config.yaml",           // default value
    DefaultText:  "config.yaml",           // shown in help
    Required:     true,                    // must be provided
    Destination:  &configVar,              // pointer to store value
    EnvVars:      []string{"APP_CONFIG"},  // environment variables
    Category:     "Configuration",
}
```

**Usage:**
```bash
myapp --config custom.yaml
myapp -c custom.yaml
APP_CONFIG=custom.yaml myapp
```

### IntFlag

Integer flags accept numeric values.

```go
&cli.IntFlag{
    Name:     "port",
    Usage:    "server port",
    Value:    8080,
    Required: false,
    Action: func(ctx context.Context, cmd *cli.Command, v int) error {
        if v < 1 || v > 65535 {
            return fmt.Errorf("port must be between 1 and 65535")
        }
        return nil
    },
    Category: "Server",
}
```

### FloatFlag

Float flags accept decimal values.

```go
&cli.FloatFlag{
    Name:     "threshold",
    Usage:    "detection threshold",
    Value:    0.75,
    Required: false,
    Category: "Processing",
}
```

### DurationFlag

Duration flags accept time durations.

```go
&cli.DurationFlag{
    Name:  "timeout",
    Usage: "operation timeout",
    Value: time.Second * 30,
}
```

**Usage:**
```bash
myapp --timeout 30s
myapp --timeout 5m
myapp --timeout 1h
```

### UintFlag

Unsigned integer flags (non-negative).

```go
&cli.UintFlag{
    Name:  "workers",
    Usage: "number of worker goroutines",
    Value: 4,
}
```

## Slice Flag Types

### StringSliceFlag

Accept multiple string values.

```go
&cli.StringSliceFlag{
    Name:     "files",
    Aliases:  []string{"f"},
    Usage:    "input files to process",
    Required: false,
    Category: "Input",
}
```

**Usage:**
```bash
myapp --files file1.txt --files file2.txt
myapp -f file1.txt -f file2.txt
```

### IntSliceFlag

Accept multiple integer values.

```go
&cli.IntSliceFlag{
    Name:  "ports",
    Usage: "multiple ports to listen on",
    Value: cli.NewIntSlice(8080, 8081),
}
```

### FloatSliceFlag

Accept multiple float values.

```go
&cli.FloatSliceFlag{
    Name:  "coordinates",
    Usage: "GPS coordinates [lat, lng]",
}
```

## Advanced Flag Features

### Flag Categories

Organize flags into logical groups in help output.

```go
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
    Usage:    "database username",
},
```

### Environment Variables

Flags can read values from environment variables.

```go
&cli.StringFlag{
    Name:    "database-url",
    EnvVars: []string{"DATABASE_URL", "DB_URL"},
    Usage:   "database connection URL",
}
```

### Required Flags

Make flags mandatory for the command to execute.

```go
&cli.StringFlag{
    Name:     "api-key",
    Required: true,
    Usage:    "API key for authentication",
}
```

### Persistent Flags

Flags that are available to all subcommands.

```go
&cli.StringFlag{
    Name:       "global-config",
    Persistent: true,
    Usage:      "global configuration file",
},
```

### Hidden Flags

Flags that don't appear in help output.

```go
&cli.StringFlag{
    Name:   "debug-token",
    Usage:  "internal debug token",
    Hidden: true,
}
```

### Custom Validation with Action

Validate flag values immediately after parsing.

```go
&cli.StringFlag{
    Name: "format",
    Usage: "output format",
    Action: func(ctx context.Context, cmd *cli.Command, v string) error {
        formats := []string{"json", "yaml", "table"}
        for _, f := range formats {
            if v == f {
                return nil
            }
        }
        return fmt.Errorf("invalid format: %s (must be json, yaml, or table)", v)
    },
}
```

### Flag Destinations

Store flag values directly in variables.

```go
var (
    configFile string
    verbose    bool
    port       int
)

&cli.StringFlag{
    Name:        "config",
    Destination: &configFile,
    Usage:       "configuration file",
},

&cli.BoolFlag{
    Name:        "verbose",
    Destination: &verbose,
    Usage:       "enable verbose output",
},

&cli.IntFlag{
    Name:        "port",
    Destination: &port,
    Usage:       "server port",
},
```

## Custom Flag Types

You can create custom flag types by implementing the `Flag` interface.

### Example: Email Flag

```go
type EmailFlag struct {
    Name        string
    Usage       string
    Destination *string
    Value       string
}

func (f *EmailFlag) Apply(set *flag.FlagSet) error {
    name := f.Names()[0]
    if f.Destination != nil {
        set.StringVar(f.Destination, name, f.Value, f.Usage)
        return nil
    }

    set.String(name, f.Value, f.Usage)
    return nil
}

func (f *EmailFlag) Names() []string {
    return []string{f.Name}
}

func (f *EmailFlag) IsSet() bool {
    // Implementation
    return false
}

func (f *EmailFlag) String() string {
    return fmt.Sprintf("%s=%v", f.Name, f.Get())
}

func (f *EmailFlag) Get() interface{} {
    if f.Destination != nil {
        return *f.Destination
    }
    return f.Value
}

func (f *EmailFlag) Clone() cli.Flag {
    clone := *f
    return &clone
}
```

## Accessing Flag Values

### In Action Functions

```go
Action: func(ctx context.Context, cmd *cli.Command) error {
    // Basic flags
    verbose := cmd.Bool("verbose")
    config := cmd.String("config")
    port := cmd.Int("port")

    // Slice flags
    files := cmd.StringSlice("files")
    ports := cmd.IntSlice("ports")

    // Check if flag was set
    if cmd.IsSet("config") {
        fmt.Printf("Using custom config: %s\n", config)
    }

    return nil
},
```

### Global Flags

Access flags from parent commands.

```go
Action: func(ctx context.Context, cmd *cli.Command) error {
    // Access global flag from parent
    globalVerbose := cmd.Bool("global-verbose")

    return nil
},
```

### Flag Values with Validation

```go
Action: func(ctx context.Context, cmd *cli.Command) error {
    port := cmd.Int("port")
    if port < 1 || port > 65535 {
        return fmt.Errorf("invalid port: %d", port)
    }

    return nil
},
```

## Best Practices

1. **Use Descriptive Names**: Clear, intuitive flag names
2. **Provide Defaults**: Sensible default values when possible
3. **Add Help Text**: Clear usage descriptions
4. **Use Categories**: Group related flags for better organization
5. **Validate Input**: Use Action functions for validation
6. **Consider Environment Variables**: Allow configuration via environment
7. **Document Complex Flags**: Use examples in help text for complex values