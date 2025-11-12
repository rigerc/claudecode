# Go Env Package Tag Reference

Complete reference for all struct tags available in the `github.com/caarlos0/env` package.

## Core Tags

### env

Specifies the environment variable name to read from.

```go
type Config struct {
    Port int `env:"PORT"`
    Host string `env:"HOST"`
}
```

### envDefault

Provides a default value when the environment variable is not set.

```go
type Config struct {
    Port int `env:"PORT" envDefault:"3000"`
    Host string `env:"HOST" envDefault:"localhost"`
    Debug bool `env:"DEBUG" envDefault:"false"`
}
```

### envSeparator

Specifies the separator for slice types. Default is comma (`,`).

```go
type Config struct {
    Hosts []string `env:"HOSTS" envSeparator:":"`  // HOSTS="host1:host2:host3"
    Ports []int `env:"PORTS" envSeparator:";"`      // PORTS="8080;8081;8082"
    Tags []string `env:"TAGS" envSeparator:"|"`     // TAGS="web|api|db"
}
```

## Prefix and Namespacing

### envPrefix

Adds a prefix to all environment variables in nested structs.

```go
type DatabaseConfig struct {
    Host string `env:"HOST" envDefault:"localhost"`
    Port int    `env:"PORT" envDefault:"5432"`
}

type AppConfig struct {
    Database DatabaseConfig `envPrefix:"DB_"`
    // Result: DB_HOST, DB_PORT
}
```

## Value Processing Tags

### envExpand

Enables environment variable expansion within values using `${var}` or `$var` syntax.

```go
type Config struct {
    HomeDir    string `env:"HOME_DIR" envExpand:"true"`
    ConfigFile string `env:"CONFIG_FILE" envDefault:"${HOME_DIR}/.config/app.yaml" envExpand:"true"`
    LogPath    string `env:"LOG_PATH" envDefault:"$HOME_DIR/logs" envExpand:"true"`
}
```

### envFile

Reads the value from a file path specified in the environment variable.

```go
type Config struct {
    SecretKey string `env:"SECRET_KEY_FILE" envFile:"true"`
    CertPath  string `env:"CERT_PATH" envFile:"true"`
    // SECRET_KEY_FILE contains path to file with actual secret
}
```

## Validation Tags

### envNotEmpty

Ensures the environment variable value is not empty after parsing.

```go
type Config struct {
    DatabaseURL string `env:"DATABASE_URL" envNotEmpty:"true"`
    APIKey      string `env:"API_KEY" envNotEmpty:"true"`
}
```

### required

Alias for `envNotEmpty:"true"`. Ensures the environment variable is set and not empty.

```go
type Config struct {
    DatabaseURL string `env:"DATABASE_URL" required:"true"`
    APIKey      string `env:"API_KEY" required:"true"`
}
```

## Lifecycle Tags

### envInit

Initializes the field if not set (useful for pointers and maps).

```go
type Config struct {
    Metadata map[string]string `env:"METADATA" envInit:"true"`
    Headers  map[string]string `env:"HEADERS" envInit:"true"`
}
```

### envUnset

Unsets the environment variable after parsing (for security with sensitive data).

```go
type Config struct {
    SecretKey string `env:"SECRET_KEY" envUnset:"true"`
    Password  string `env:"PASSWORD" envUnset:"true"`
}
```

## Advanced Tag Combinations

### Database Configuration

```go
type DatabaseConfig struct {
    Host     string        `env:"DB_HOST" envDefault:"localhost"`
    Port     int           `env:"DB_PORT" envDefault:"5432"`
    Username string        `env:"DB_USERNAME" envDefault:"postgres"`
    Password string        `env:"DB_PASSWORD" required:"true" envUnset:"true"`
    Database string        `env:"DB_NAME" required:"true"`
    SSLMode  string        `env:"DB_SSL_MODE" envDefault:"disable"`
    Timeout  time.Duration `env:"DB_TIMEOUT" envDefault:"30s"`
    Options  []string      `env:"DB_OPTIONS" envSeparator:","`
}
```

### HTTP Server Configuration

```go
type ServerConfig struct {
    Host         string        `env:"HOST" envDefault:"0.0.0.0"`
    Port         int           `env:"PORT" envDefault:"8080"`
    ReadTimeout  time.Duration `env:"READ_TIMEOUT" envDefault:"30s"`
    WriteTimeout time.Duration `env:"WRITE_TIMEOUT" envDefault:"30s"`
    IdleTimeout  time.Duration `env:"IDLE_TIMEOUT" envDefault:"120s"`
    CORSOrigins  []string      `env:"CORS_ORIGINS" envSeparator:","`
    TLS          struct {
        CertFile string `env:"TLS_CERT_FILE" envFile:"true" required:"true"`
        KeyFile  string `env:"TLS_KEY_FILE" envFile:"true" required:"true"`
    }
}
```

### Logging Configuration

```go
type LoggingConfig struct {
    Level      string `env:"LOG_LEVEL" envDefault:"info"`
    Format     string `env:"LOG_FORMAT" envDefault:"json"`
    Output     string `env:"LOG_OUTPUT" envDefault:"stdout"`
    LogFile    string `env:"LOG_FILE" envDefault:"${HOME_DIR}/logs/app.log" envExpand:"true"`
    MaxSize    int    `env:"LOG_MAX_SIZE" envDefault:"100"`
    MaxBackups int    `env:"LOG_MAX_BACKUPS" envDefault:"3"`
    MaxAge     int    `env:"LOG_MAX_AGE" envDefault:"28"`
}
```

## Type-Specific Behavior

### Boolean Types

Environment variables for boolean fields accept:
- `1`, `t`, `T`, `TRUE`, `true`, `True` → `true`
- `0`, `f`, `F`, `FALSE`, `false`, `False` → `false`
- Empty string → `false` (unless `required` or `envNotEmpty`)

```go
type Config struct {
    Debug      bool `env:"DEBUG" envDefault:"false"`
    Production bool `env:"PRODUCTION"`
    Verbose    bool `env:"VERBOSE"`
}
```

### Integer Types

Supports decimal, octal (with `0` prefix), and hexadecimal (with `0x` prefix) formats.

```go
type Config struct {
    Port     int    `env:"PORT" envDefault:"8080"`
    Timeout  int64  `env:"TIMEOUT" envDefault:"30"`
    MaxConn  uint   `env:"MAX_CONN" envDefault:"10"`
    FileMode int    `env:"FILE_MODE" envDefault:"0644"`  // Octal
}
```

### Duration Types

Accepts Go duration format strings.

```go
type Config struct {
    Timeout    time.Duration `env:"TIMEOUT" envDefault:"30s"`
    RetryDelay time.Duration `env:"RETRY_DELAY" envDefault:"5m"`
    MaxWait    time.Duration `env:"MAX_WAIT" envDefault:"1h"`
}
```

### Slice Types

Splits values using the specified separator (default: comma).

```go
type Config struct {
    Hosts        []string      `env:"HOSTS"`                     // "host1,host2,host3"
    Ports        []int         `env:"PORTS" envSeparator:";"`     // "8080;8081;8082"
    Features     []bool        `env:"FEATURES"`                   // "true,false,true"
    Timeouts     []time.Duration `env:"TIMEOUTS"`                 // "30s,60s,90s"
}
```

### Pointer Types

Nil pointers remain nil if environment variable is not set.

```go
type Config struct {
    OptionalHost *string `env:"OPTIONAL_HOST"`
    OptionalPort *int    `env:"OPTIONAL_PORT"`
    RequiredURL  *string `env:"REQUIRED_URL" required:"true"`
}
```

## Error Handling Tags

### Common Error Scenarios

1. **Missing Required Field**: When `required:"true"` or `envNotEmpty:"true"` but variable not set
2. **Invalid Format**: When value cannot be converted to target type
3. **Unsupported Type**: When field type is not supported by the package
4. **Invalid Struct Pointer**: When passed value is not a pointer to struct

### Error Messages

```go
type Config struct {
    Port int `env:"PORT"`
}

// Error types:
// env.ErrNotAStructPtr - "expected a pointer to a struct"
// env.ErrUnsupportedType - "unsupported type: chan int"
// env.ErrUnsupportedSliceType - "unsupported slice type: []net.IP"
// Custom errors for missing required fields
```