# Getting Started with Zerolog

## Installation

```bash
go get -u github.com/rs/zerolog/log
```

## Basic Setup

### Simple Global Logger

```go
package main

import (
    "os"
    "github.com/rs/zerolog"
    "github.com/rs/zerolog/log"
)

func main() {
    // Configure global logger
    log.Logger = zerolog.New(os.Stdout).With().Timestamp().Logger()

    // Basic logging
    log.Info().Msg("Hello, World!")
    log.Debug().Msg("Debug message")
    log.Warn().Msg("Warning message")
    log.Error().Msg("Error message")
}
```

### Custom Logger with Options

```go
package main

import (
    "os"
    "time"
    "github.com/rs/zerolog"
)

func main() {
    // Create logger with custom options
    logger := zerolog.New(os.Stdout).With().
        Timestamp().
        Str("service", "my-app").
        Str("version", "1.0.0").
        Int("port", 8080).
        Logger()

    // Use the custom logger
    logger.Info().
        Str("component", "database").
        Msg("Component initialized")

    // Set log level to filter messages
    logger = logger.Level(zerolog.InfoLevel)
    logger.Debug().Msg("This won't be logged") // Filtered out
}
```

### Field Types and Methods

```go
package main

import (
    "time"
    "net"
    "github.com/rs/zerolog/log"
)

func main() {
    // String and numeric fields
    log.Info().
        Str("user", "alice").
        Int("age", 30).
        Float64("balance", 1234.56).
        Bool("active", true).
        Msg("User information")

    // Time and duration fields
    log.Info().
        Time("created", time.Now()).
        Dur("response_time", 250*time.Millisecond).
        Msg("Timing information")

    // Array and dictionary fields
    log.Info().
        Array("tags", zerolog.Arr().
            Str("urgent").
            Str("customer-service").
            Str("billing")).
        Dict("metadata", zerolog.Dict().
            Str("source", "api").
            Int("version", 2)).
        Msg("Complex data structure")

    // Network field types
    ip := net.ParseIP("192.168.1.100")
    log.Info().
        IPAddr("client_ip", ip).
        Str("endpoint", "/api/users").
        Msg("Request received")
}
```

### Sub-loggers with Persistent Fields

```go
package main

import (
    "os"
    "github.com/rs/zerolog"
)

func main() {
    // Parent logger with base context
    baseLogger := zerolog.New(os.Stdout).With().
        Str("service", "api-gateway").
        Str("environment", "production").
        Logger()

    // Create sub-logger for specific component
    authLogger := baseLogger.With().
        Str("component", "auth").
        Str("module", "jwt").
        Logger()

    authLogger.Info().
        Str("user_id", "12345").
        Msg("Token validated")
    // Output includes: service, environment, component, module, user_id

    // Another sub-logger for different component
    dbLogger := baseLogger.With().
        Str("component", "database").
        Str("driver", "postgres").
        Logger()

    dbLogger.Warn().
        Int("pool_size", 45).
        Int("max_size", 50).
        Msg("Connection pool near capacity")
}
```

### Console Writer for Development

```go
package main

import (
    "os"
    "time"
    "github.com/rs/zerolog"
)

func main() {
    // Human-readable console output
    logger := zerolog.New(zerolog.ConsoleWriter{
        Out:        os.Stdout,
        TimeFormat: time.RFC3339,
    })

    logger.Info().
        Str("user", "bob").
        Int("items", 5).
        Msg("Processing complete")
    // Output: 2023-01-15T10:30:00Z INF Processing complete user=bob items=5

    // Customized console writer
    output := zerolog.ConsoleWriter{
        Out:        os.Stdout,
        TimeFormat: time.Kitchen,
        NoColor:    false,
    }

    logger = zerolog.New(output).With().Timestamp().Logger()
    logger.Warn().Str("status", "ok").Msg("Custom format")
    // Output: 3:04PM WRN Custom format status=ok
}
```

### Error Logging with Stack Traces

```go
package main

import (
    "errors"
    "github.com/rs/zerolog"
    "github.com/rs/zerolog/pkgerrors"
)

func main() {
    // Enable stack trace marshaling
    zerolog.ErrorStackMarshaler = pkgerrors.MarshalStack

    logger := zerolog.New(os.Stdout).With().Timestamp().Logger()

    // Simple error logging
    err := errors.New("database connection failed")
    logger.Error().
        Err(err).
        Str("database", "postgres").
        Int("retry_count", 3).
        Msg("Connection error")

    // Error with stack trace
    err = processRequest()
    logger.Error().
        Stack().
        Err(err).
        Msg("Request processing failed")

    // Multiple errors in array
    errs := []error{
        errors.New("connection timeout"),
        errors.New("max retries exceeded"),
    }
    logger.Error().
        Errs("failures", errs).
        Msg("Multiple errors occurred")
}

func processRequest() error {
    return errors.New("database query failed")
}
```

### Log Level Configuration

```go
package main

import (
    "os"
    "github.com/rs/zerolog"
    "github.com/rs/zerolog/log"
)

func main() {
    // Set global log level
    zerolog.SetGlobalLevel(zerolog.InfoLevel)

    // This will be filtered out
    log.Debug().Msg("This won't appear")

    // This will be logged
    log.Info().Msg("This will appear")

    // Parse level from string
    level, err := zerolog.ParseLevel("warn")
    if err == nil {
        log.SetLevel(level)
    }

    // Create logger with specific level
    logger := zerolog.New(os.Stdout).
        Level(zerolog.ErrorLevel).
        With().Timestamp().
        Logger()

    logger.Info().Msg("Also won't appear") // Filtered
    logger.Error().Msg("Will appear")     // Logged

    // Available levels (from lowest to highest severity)
    // zerolog.TraceLevel - Most detailed
    // zerolog.DebugLevel - Debugging information
    // zerolog.InfoLevel  - General information
    // zerolog.WarnLevel  - Warning conditions
    // zerolog.ErrorLevel - Error conditions
    // zerolog.FatalLevel - Fatal errors (calls os.Exit)
    // zerolog.Disabled   - Logging disabled
}
```

### Custom Object Marshaling

```go
package main

import (
    "time"
    "github.com/rs/zerolog/log"
)

type User struct {
    Name    string    `json:"name"`
    Email   string    `json:"email"`
    Age     int       `json:"age"`
    Created time.Time `json:"created"`
}

// Implement LogObjectMarshaler for zero-allocation marshaling
func (u User) MarshalZerologObject(e *zerolog.Event) {
    e.Str("name", u.Name).
        Str("email", u.Email).
        Int("age", u.Age).
        Time("created", u.Created)
}

type Users []User

func (users Users) MarshalZerologArray(a *zerolog.Array) {
    for _, user := range users {
        a.Object(user)
    }
}

func main() {
    user := User{
        Name:    "Bob",
        Email:   "bob@example.com",
        Age:     25,
        Created: time.Now(),
    }

    // Log custom object
    log.Info().Object("user", user).Msg("User registered")

    // Log array of custom objects
    users := Users{
        User{"Alice", "alice@example.com", 30, time.Now()},
        User{"Charlie", "charlie@example.com", 35, time.Now()},
    }

    log.Info().Array("users", users).Msg("Batch user import")
}
```

### Global Settings and Configuration

```go
package main

import (
    "os"
    "time"
    "github.com/rs/zerolog"
    "github.com/rs/zerolog/log"
)

func main() {
    // Customize field names
    zerolog.TimestampFieldName = "ts"
    zerolog.LevelFieldName = "severity"
    zerolog.MessageFieldName = "msg"
    zerolog.ErrorFieldName = "err"

    // Customize time format
    zerolog.TimeFieldFormat = time.RFC3339
    // Other options: TimeFormatUnix, TimeFormatUnixMs, TimeFormatUnixMicro

    // Set global log level
    zerolog.SetGlobalLevel(zerolog.InfoLevel)

    // Configure caller skip frames
    zerolog.CallerSkipFrameCount = 2

    // Set floating point precision
    zerolog.FloatingPointPrecision = 2

    logger := zerolog.New(os.Stdout).
        With().
        Timestamp().
        Caller().
        Logger()

    logger.Info().
        Float64("price", 99.999).
        Dur("elapsed", 1500*time.Millisecond).
        Msg("Custom configuration")

    // Multiple output destinations
    consoleWriter := zerolog.ConsoleWriter{Out: os.Stderr}
    fileWriter, _ := os.Create("app.log")

    multiWriter := zerolog.MultiLevelWriter(consoleWriter, fileWriter)
    logger = zerolog.New(multiWriter).With().Timestamp().Logger()

    logger.Info().Msg("Logged to both console and file")
}
```

## Environment-Based Configuration

```go
package main

import (
    "os"
    "strconv"
    "github.com/rs/zerolog"
    "github.com/rs/zerolog/log"
)

func setupLogger() zerolog.Logger {
    // Get configuration from environment
    levelStr := getEnv("LOG_LEVEL", "info")
    jsonFormat := getEnvBool("LOG_JSON", false)
    timestamp := getEnvBool("LOG_TIMESTAMP", true)

    // Parse log level
    level, err := zerolog.ParseLevel(levelStr)
    if err != nil {
        level = zerolog.InfoLevel
    }

    // Choose formatter
    var formatter zerolog.Formatter
    if jsonFormat {
        formatter = zerolog.JSONFormatter
    } else {
        formatter = zerolog.ConsoleWriter{Out: os.Stdout}
    }

    // Create logger
    logger := zerolog.New(os.Stdout).
        With().
        Timestamp().
        Str("service", "myapp").
        Str("version", getEnv("APP_VERSION", "unknown")).
        Logger()

    // Configure logger
    logger = logger.Level(level)
    if !timestamp {
        logger = logger.Output(zerolog.ConsoleWriter{
            Out:          os.Stdout,
            PartsOrder:   []string{"level", "message"},
            TimeFormat:   "",
        })
    }

    return logger
}

func getEnv(key, defaultValue string) string {
    if value := os.Getenv(key); value != "" {
        return value
    }
    return defaultValue
}

func getEnvBool(key string, defaultValue bool) bool {
    if value := os.Getenv(key); value != "" {
        if parsed, err := strconv.ParseBool(value); err == nil {
            return parsed
        }
    }
    return defaultValue
}

func main() {
    logger := setupLogger()
    log.SetDefault(logger)

    log.Info("Application started", "env", os.Getenv("ENVIRONMENT"))
    log.Debug("Debug mode enabled", "level", log.GetLevel().String())
}
```

## Next Steps

After mastering the basics, explore:

1. **Performance Optimization**: See [performance-guide.md](performance-guide.md)
2. **Production Deployment**: See [production-deployment.md](production-deployment.md)
3. **HTTP Middleware**: Use hlog package for web applications
4. **Context Integration**: Store loggers in Go context for request tracing
5. **Custom Hooks**: Implement custom log processing
6. **Sampling**: Reduce log volume in high-throughput systems

## Common Pitfalls

1. **Using Interface{}**: Avoid reflection-based logging
   ```go
   // ❌ Slow - uses reflection
   log.Info().Interface("data", complexStruct).Msg("Slow logging")

   // ✅ Fast - implement MarshalZerologObject
   log.Info().Object("data", complexStruct).Msg("Fast logging")
   ```

2. **Forgetting Level Configuration**: Logs may be filtered out
   ```go
   // Set appropriate level for your needs
   zerolog.SetGlobalLevel(zerolog.DebugLevel)
   ```

3. **Expensive Computations**: Check if logging is enabled
   ```go
   // ✅ Check before expensive computation
   if e := log.Debug(); e.Enabled() {
       expensiveResult := computeExpensiveValue()
       e.Str("result", expensiveResult).Msg("Debug info")
   }
   ```