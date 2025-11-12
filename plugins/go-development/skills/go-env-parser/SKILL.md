---
name: go-env-parser
description: This skill should be used when developers need to work with the github.com/caarlos0/env Go package for parsing environment variables into structs. It provides specialized knowledge for creating configuration structures, using advanced tag options, implementing custom parsers, and troubleshooting common issues with environment variable parsing in Go applications.
---

# Go Environment Variable Parser

## Overview

This skill enables developers to effectively use the `github.com/caarlos0/env` package for parsing environment variables into Go structs. It provides expertise in struct tag configuration, type handling, custom parsers, and best practices for environment-based configuration management in Go applications.

## Quick Start

### Basic Configuration Setup

To create a basic configuration structure that reads from environment variables:

1. Define a struct with `env` tags for each field
2. Call `env.Parse()` or `env.ParseAs[T]()` to populate the struct
3. Handle errors appropriately

Example usage:
```go
type Config struct {
    Port    int    `env:"PORT" envDefault:"3000"`
    Debug   bool   `env:"DEBUG" envDefault:"false"`
    DBURL   string `env:"DATABASE_URL" required:"true"`
}

cfg, err := env.ParseAs[Config]()
```

### Common Tasks

Choose the appropriate task based on your requirements:

- **Basic parsing**: Use `env.Parse()` for simple struct-based configuration
- **Generics**: Use `env.ParseAs[T]()` for type-safe configuration parsing
- **Custom types**: Use `env.ParseWithFuncs()` for complex type parsing
- **Nested configs**: Use `envPrefix` for grouped configuration
- **File-based values**: Use `envFile` tag for reading from files

## Task Categories

### 1. Configuration Structure Design

#### Basic Configuration Patterns

Design configuration structures based on application complexity:

**Simple Application:**
- Use basic types with `env` tags
- Provide sensible defaults with `envDefault`
- Mark required fields with `required:"true"`

**Complex Application:**
- Group related configuration using nested structs
- Use `envPrefix` for namespacing
- Implement validation with `envNotEmpty`

**Microservice:**
- Separate service and infrastructure configuration
- Use slices for multi-value configuration
- Implement feature flags with boolean slices

#### Type Selection Guidelines

Choose appropriate types based on environment variable content:

- **String**: Use for text values, URLs, file paths
- **Integer**: Use for numeric values (ports, timeouts, counts)
- **Boolean**: Use for flags and toggles
- **Duration**: Use for time-based configuration with `time.Duration`
- **Slice**: Use for comma-separated values or custom separators
- **Pointer**: Use for optional values

### 2. Advanced Tag Usage

#### Core Tag Combinations

Use these common tag patterns for specific scenarios:

**Database Configuration:**
```go
type DatabaseConfig struct {
    Host     string        `env:"DB_HOST" envDefault:"localhost"`
    Port     int           `env:"DB_PORT" envDefault:"5432"`
    Username string        `env:"DB_USERNAME" envDefault:"postgres"`
    Password string        `env:"DB_PASSWORD" required:"true"`
    Database string        `env:"DB_NAME" required:"true"`
    SSLMode  string        `env:"DB_SSL_MODE" envDefault:"disable"`
    Timeout  time.Duration `env:"DB_TIMEOUT" envDefault:"30s"`
}
```

**Feature Flag Configuration:**
```go
type FeatureConfig struct {
    Features    []string `env:"ENABLED_FEATURES" envSeparator:","`
    BetaUsers   []string `env:"BETA_USERS" envSeparator:":"`
    DebugMode   bool     `env:"DEBUG_MODE" envDefault:"false"`
    LogLevel    string   `env:"LOG_LEVEL" envDefault:"info"`
}
```

#### File-based Configuration

For sensitive configuration stored in files:

**Secret Management:**
```go
type SecretConfig struct {
    APIKey     string `env:"API_KEY_FILE" envFile:"true"`
    CertPath   string `env:"CERT_PATH" envFile:"true"`
    PrivateKey string `env:"PRIVATE_KEY_FILE" envFile:"true" required:"true"`
}
```

#### Environment Variable Expansion

Use `envExpand` for dynamic configuration:

**Path Configuration:**
```go
type PathConfig struct {
    HomeDir     string `env:"HOME_DIR" envExpand:"true"`
    ConfigFile  string `env:"CONFIG_FILE" envDefault:"${HOME_DIR}/.config/app.yaml" envExpand:"true"`
    LogDir      string `env:"LOG_DIR" envDefault:"${HOME_DIR}/logs" envExpand:"true"`
    TempDir     string `env:"TEMP_DIR" envDefault:"${HOME_DIR}/tmp" envExpand:"true"`
}
```

### 3. Custom Parser Implementation

#### Custom Type Handling

Implement custom parsers for complex types:

**IP Address Parsing:**
```go
customParsers := env.CustomParsers{
    reflect.TypeOf(net.IP{}): func(v string) (interface{}, error) {
        ip := net.ParseIP(v)
        if ip == nil {
            return nil, fmt.Errorf("invalid IP address: %s", v)
        }
        return ip, nil
    },
}
```

**URL Parsing:**
```go
customParsers := env.CustomParsers{
    reflect.TypeOf(url.URL{}): func(v string) (interface{}, error) {
        u, err := url.Parse(v)
        if err != nil {
            return nil, fmt.Errorf("invalid URL: %s", v)
        }
        return *u, nil
    },
}
```

**Enum-like String Parsing:**
```go
type LogLevel string

const (
    LogLevelDebug LogLevel = "debug"
    LogLevelInfo  LogLevel = "info"
    LogLevelWarn  LogLevel = "warn"
    LogLevelError LogLevel = "error"
)

customParsers := env.CustomParsers{
    reflect.TypeOf(LogLevel("")): func(v string) (interface{}, error) {
        switch strings.ToLower(v) {
        case "debug", "info", "warn", "error":
            return LogLevel(strings.ToLower(v)), nil
        default:
            return nil, fmt.Errorf("invalid log level: %s", v)
        }
    },
}
```

### 4. Error Handling and Validation

#### Error Type Handling

Implement proper error handling based on error types:

```go
err := env.Parse(&config)
if err != nil {
    switch {
    case errors.Is(err, env.ErrNotAStructPtr):
        log.Fatal("Configuration error: Must pass a pointer to a struct")
    case errors.Is(err, env.ErrUnsupportedType):
        log.Fatal("Configuration error: Unsupported field type in config")
    case errors.Is(err, env.ErrUnsupportedSliceType):
        log.Fatal("Configuration error: Unsupported slice type in config")
    default:
        if strings.Contains(err.Error(), "required") {
            log.Fatal("Configuration error: Missing required environment variable")
        }
        log.Fatalf("Configuration error: %v", err)
    }
}
```

#### Validation Patterns

Add validation after parsing:

**Port Range Validation:**
```go
if cfg.Port < 1 || cfg.Port > 65535 {
    return fmt.Errorf("invalid port number: %d (must be 1-65535)", cfg.Port)
}
```

**URL Validation:**
```go
if cfg.DatabaseURL != "" {
    if _, err := url.Parse(cfg.DatabaseURL); err != nil {
        return fmt.Errorf("invalid database URL: %v", err)
    }
}
```

### 5. Testing Configuration

#### Unit Testing Configuration

Test configuration parsing with environment setup:

```go
func TestConfigParsing(t *testing.T) {
    // Set test environment variables
    os.Setenv("PORT", "8080")
    os.Setenv("DEBUG", "true")
    os.Setenv("DATABASE_URL", "localhost:5432")
    defer func() {
        os.Unsetenv("PORT")
        os.Unsetenv("DEBUG")
        os.Unsetenv("DATABASE_URL")
    }()

    var config Config
    err := env.Parse(&config)
    assert.NoError(t, err)
    assert.Equal(t, 8080, config.Port)
    assert.True(t, config.Debug)
    assert.Equal(t, "localhost:5432", config.DatabaseURL)
}
```

#### Table-Driven Testing

Test multiple configuration scenarios:

```go
func TestConfigValidation(t *testing.T) {
    tests := []struct {
        name    string
        envVars map[string]string
        wantErr bool
        errMsg  string
    }{
        {
            name: "valid config",
            envVars: map[string]string{
                "PORT":         "3000",
                "DATABASE_URL": "localhost:5432",
            },
            wantErr: false,
        },
        {
            name: "missing required field",
            envVars: map[string]string{
                "PORT": "3000",
            },
            wantErr: true,
            errMsg:  "DATABASE_URL",
        },
    }

    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            for k, v := range tt.envVars {
                os.Setenv(k, v)
            }
            defer func() {
                for k := range tt.envVars {
                    os.Unsetenv(k)
                }
            }()

            var config Config
            err := env.Parse(&config)
            if tt.wantErr {
                assert.Error(t, err)
                assert.Contains(t, err.Error(), tt.errMsg)
            } else {
                assert.NoError(t, err)
            }
        })
    }
}
```

### 6. Migration and Versioning

#### Migrating from v2 to v3

Update code to use modern generics API:

**Before (v2):**
```go
var cfg Config
if err := env.Parse(&cfg); err != nil {
    log.Fatal(err)
}
```

**After (v3 with generics):**
```go
cfg, err := env.ParseAs[Config]()
if err != nil {
    log.Fatal(err)
}
```

**With MustParse for production:**
```go
cfg := env.MustParseAs[Config]()
```

## Resources

### references/

The skill includes comprehensive reference materials:

- **tag-reference.md**: Complete documentation of all available struct tags and their usage patterns
- **examples.md**: Real-world configuration examples for different application types
- **troubleshooting.md**: Common issues and their solutions

Load these references when detailed information is needed for specific tag combinations or advanced usage patterns.

### assets/templates/

Ready-to-use configuration templates for common scenarios:

- **basic-config.go**: Simple application configuration template
- **database-config.go**: Database configuration with connection pooling settings
- **microservice-config.go**: Complete microservice configuration template

Use these templates as starting points for new projects, copying and customizing them as needed.

## Usage Guidelines

### When to Use This Skill

Use this skill when:
- Setting up environment variable parsing for new Go applications
- Migrating existing configuration to use the env package
- Implementing complex configuration with custom types
- Troubleshooting environment variable parsing issues
- Creating reusable configuration patterns
- Adding validation to existing configuration structures

### Best Practices

Follow these best practices for effective environment variable configuration:

1. **Always provide defaults** for non-critical configuration
2. **Use required tags** for essential configuration values
3. **Group related configuration** using nested structs with prefixes
4. **Implement custom parsers** for complex types
5. **Add validation** after parsing for business logic constraints
6. **Document configuration** with clear environment variable names
7. **Test configuration** with different environment variable combinations
8. **Handle errors gracefully** with informative error messages

### Common Pitfalls

Avoid these common issues:

- Don't use environment variable names that conflict with system variables
- Avoid required fields in development environments
- Don't ignore error handling for configuration parsing
- Avoid complex nested structures that are hard to debug
- Don't use slice separators that might appear in actual data
- Avoid case-sensitive environment variable naming issues