# Go Environment Variable Parsing with github.com/caarlos0/env

A comprehensive guide to the `github.com/caarlos0/env` package for parsing environment variables into Go structs.

## Overview

The `github.com/caarlos0/env` package is a simple, zero-dependencies library that provides a KISS (Keep It Simple, Stupid) way to deal with environment variables in Go. It allows you to parse environment variables directly into struct fields using struct tags.

## Features

- **Zero Dependencies**: No external dependencies required
- **Simple API**: Easy-to-use struct tag based configuration
- **Type Support**: Built-in support for common Go types
- **Custom Parsers**: Extensible with custom parsing functions
- **Advanced Tag Options**: Rich set of configuration tags
- **Generics Support**: Modern Go generics support
- **Error Handling**: Comprehensive error types for debugging

## Installation

```bash
go get github.com/caarlos0/env
```

## Basic Usage

### Simple Example

```go
package main

import (
    "fmt"
    "github.com/caarlos0/env"
)

type Config struct {
    Home         string        `env:"HOME"`
    Port         int           `env:"PORT" envDefault:"3000"`
    IsProduction bool          `env:"PRODUCTION"`
    Debug        bool          `env:"DEBUG" envDefault:"false"`
}

func main() {
    var cfg Config
    if err := env.Parse(&cfg); err != nil {
        fmt.Printf("Error parsing environment: %v\n", err)
        return
    }

    fmt.Printf("Config: %+v\n", cfg)
}
```

### Using Generics

```go
package main

import (
    "fmt"
    "github.com/caarlos0/env"
)

type Config struct {
    DatabaseURL string `env:"DATABASE_URL" envDefault:"localhost:5432"`
    Timeout     int    `env:"TIMEOUT" envDefault:"30"`
}

func main() {
    cfg, err := env.ParseAs[Config]()
    if err != nil {
        fmt.Printf("Error parsing environment: %v\n", err)
        return
    }

    fmt.Printf("Config: %+v\n", cfg)
}
```

## Supported Types

### Built-in Types

- **String**: `string`
- **Integers**: `int`, `uint`, `int64`
- **Booleans**: `bool`
- **Floats**: `float32`, `float64`
- **Time**: `time.Duration`
- **URL**: `url.URL`

### Composite Types

#### Slices

```go
type Config struct {
    Hosts        []string      `env:"HOSTS" envSeparator:":"`
    Ports        []int         `env:"PORTS" envSeparator:","`
    Features     []bool        `env:"FEATURES"`
    Durations    []time.Duration `env:"DURATIONS"`
}
```

#### Pointers

```go
type Config struct {
    OptionalHost *string       `env:"OPTIONAL_HOST"`
    Timeout      *int          `env:"TIMEOUT" envDefault:"30"`
}
```

#### Maps

```go
type Config struct {
    Labels       map[string]string `env:"LABELS"`
}
```

## Struct Tags

### Core Tags

| Tag | Description | Example |
|-----|-------------|---------|
| `env` | Environment variable name | `env:"DATABASE_URL"` |
| `envDefault` | Default value when env var is not set | `envDefault:"3000"` |
| `envSeparator` | Separator for slice types (default: comma) | `envSeparator:":"` |
| `envPrefix` | Prefix for all environment variables | `envPrefix:"APP_"` |

### Advanced Tags

| Tag | Description | Example |
|-----|-------------|---------|
| `envExpand` | Replace `${var}` or `$var` with environment values | `envExpand:"true"` |
| `envFile` | Read value from file path | `envFile:"true"` |
| `envInit` | Initialize field if not set | `envInit:"true"` |
| `envNotEmpty` | Ensure value is not empty | `envNotEmpty:"true"` |
| `required` | Required field (alias for envNotEmpty) | `required:"true"` |
| `envUnset` | Unset environment variable after parsing | `envUnset:"true"` |

## Advanced Examples

### Environment Variable Expansion

```go
type Config struct {
    HomeDir    string `env:"HOME_DIR" envExpand:"true"`
    ConfigFile string `env:"CONFIG_FILE" envDefault:"${HOME_DIR}/.config/app.yaml" envExpand:"true"`
    LogPath    string `env:"LOG_PATH" envExpand:"true"`
}
```

### File-based Configuration

```go
type Config struct {
    SecretKey string `env:"SECRET_KEY_FILE" envFile:"true"`
    CertPath  string `env:"CERT_PATH" envFile:"true" envDefault:"/etc/ssl/cert.pem"`
}
```

### Custom Parsers

```go
package main

import (
    "fmt"
    "net"
    "github.com/caarlos0/env"
)

type Config struct {
    ServerIP net.IP `env:"SERVER_IP"`
    DatabaseURL string `env:"DATABASE_URL"`
}

func main() {
    customParsers := env.CustomParsers{
        reflect.TypeOf(net.IP{}): func(v string) (interface{}, error) {
            ip := net.ParseIP(v)
            if ip == nil {
                return nil, fmt.Errorf("invalid IP address: %s", v)
            }
            return ip, nil
        },
    }

    var cfg Config
    if err := env.ParseWithFuncs(&cfg, customParsers); err != nil {
        fmt.Printf("Error parsing: %v\n", err)
        return
    }

    fmt.Printf("Config: %+v\n", cfg)
}
```

### Using ParseWithOptions

```go
package main

import (
    "fmt"
    "github.com/caarlos0/env"
)

type Config struct {
    Port int `env:"PORT"`
    Host string `env:"HOST"`
}

func main() {
    opts := env.Options{
        Prefix: "APP_",
    }

    var cfg Config
    if err := env.ParseWithOptions(&cfg, opts); err != nil {
        fmt.Printf("Error parsing: %v\n", err)
        return
    }

    fmt.Printf("Config: %+v\n", cfg)
}
```

## Error Handling

### Error Types

```go
package main

import (
    "fmt"
    "github.com/caarlos0/env"
)

func main() {
    var cfg Config

    err := env.Parse(&cfg)
    if err != nil {
        switch {
        case errors.Is(err, env.ErrNotAStructPtr):
            fmt.Println("Error: Must pass a pointer to a struct")
        case errors.Is(err, env.ErrUnsupportedType):
            fmt.Println("Error: Unsupported field type")
        case errors.Is(err, env.ErrUnsupportedSliceType):
            fmt.Println("Error: Unsupported slice type")
        default:
            fmt.Printf("Error: %v\n", err)
        }
        return
    }
}
```

### Must Parse (Panics on Error)

```go
package main

import (
    "fmt"
    "github.com/caarlos0/env"
)

type Config struct {
    Port int `env:"PORT" envDefault:"3000"`
}

func main() {
    cfg := env.MustParseAs[Config]()
    fmt.Printf("Config: %+v\n", cfg)
}
```

## Real-World Examples

### Database Configuration

```go
type DatabaseConfig struct {
    Host         string        `env:"DB_HOST" envDefault:"localhost"`
    Port         int           `env:"DB_PORT" envDefault:"5432"`
    Username     string        `env:"DB_USERNAME" envDefault:"postgres"`
    Password     string        `env:"DB_PASSWORD" required:"true"`
    Database     string        `env:"DB_NAME" envDefault:"app"`
    SSLMode      string        `env:"DB_SSL_MODE" envDefault:"disable"`
    MaxConns     int           `env:"DB_MAX_CONNS" envDefault:"10"`
    ConnTimeout  time.Duration `env:"DB_CONN_TIMEOUT" envDefault:"30s"`
    Migrations   []string      `env:"DB_MIGRATIONS" envSeparator:","`
}

type AppConfig struct {
    Port      int              `env:"PORT" envDefault:"8080"`
    Debug     bool             `env:"DEBUG" envDefault:"false"`
    LogLevel  string           `env:"LOG_LEVEL" envDefault:"info"`
    Database  DatabaseConfig   `envPrefix:"DB_"`
}
```

### Microservice Configuration

```go
type ServiceConfig struct {
    ServiceName    string        `env:"SERVICE_NAME" required:"true"`
    Version        string        `env:"SERVICE_VERSION" envDefault:"1.0.0"`

    // HTTP Server
    Host           string        `env:"HOST" envDefault:"0.0.0.0"`
    Port           int           `env:"PORT" envDefault:"8080"`
    ReadTimeout    time.Duration `env:"READ_TIMEOUT" envDefault:"30s"`
    WriteTimeout   time.Duration `env:"WRITE_TIMEOUT" envDefault:"30s"`

    // Features
    EnabledFeatures []string    `env:"ENABLED_FEATURES" envSeparator:","`

    // External Services
    UserServiceURL string        `env:"USER_SERVICE_URL" required:"true"`
    AuthServiceURL string        `env:"AUTH_SERVICE_URL" required:"true"`

    // Monitoring
    MetricsPort    int           `env:"METRICS_PORT" envDefault:"9090"`
    HealthCheck    bool          `env:"HEALTH_CHECK" envDefault:"true"`
}
```

## Best Practices

1. **Always Provide Defaults**: Use `envDefault` for non-critical configuration
2. **Use Required Tags**: Mark critical configuration as required
3. **Environment Variable Naming**: Use consistent, uppercase naming
4. **Group Related Config**: Use nested structs with `envPrefix`
5. **Type Safety**: Let the package handle type conversion
6. **Error Handling**: Always check for parsing errors
7. **Documentation**: Document your configuration structure

## Performance Considerations

- The library uses reflection for parsing, which has minimal overhead
- Parsing is typically done once at application startup
- Custom parsers should be efficient for better performance
- Consider using `MustParseAs` in production when configuration is validated

## Migration from v2 to v3

If upgrading from v2 to v3:

```go
// v2
func Parse(v interface{}) error

// v3 (backward compatible)
func Parse(v interface{}) error

// v3 generics
func ParseAs[T any]() (T, error)
func MustParseAs[T any]() T
```

## Troubleshooting

### Common Issues

1. **Nil Pointer Errors**: Always pass a pointer to a struct
2. **Unsupported Types**: Use custom parsers for complex types
3. **Environment Variables Not Found**: Check variable names and use defaults
4. **Type Conversion Errors**: Ensure environment variable values match expected types

### Debug Configuration

```go
type DebugConfig struct {
    DebugParse    bool   `env:"DEBUG_PARSE" envDefault:"false"`
    PrintConfig   bool   `env:"PRINT_CONFIG" envDefault:"false"`
    ConfigFile    string `env:"CONFIG_FILE"`
}
```

## API Reference

### Functions

- `Parse(v interface{}) error`: Parse environment variables into struct
- `ParseWithFuncs(v interface{}, funcMap CustomParsers) error`: Parse with custom parsers
- `ParseAs[T any]() (T, error)`: Parse with generics
- `ParseWithOptions(v interface{}, opts Options) error`: Parse with options
- `MustParseAs[T any]() T`: Parse with generics, panic on error

### Types

- `CustomParsers`: Map of type to custom parser function
- `ParserFunc`: Function signature for custom parsers
- `Options`: Configuration options for parsing

### Error Types

- `ErrNotAStructPtr`: Expected a pointer to a struct
- `ErrUnsupportedType`: Type is not supported
- `ErrUnsupportedSliceType`: Unsupported slice type

## License

This package is licensed under the MIT License. See the LICENSE file for details.

## Repository

- GitHub: https://github.com/caarlos0/env
- Documentation: https://pkg.go.dev/github.com/caarlos0/env
- Issues: https://github.com/caarlos0/env/issues