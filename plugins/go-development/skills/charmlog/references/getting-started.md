# Getting Started with Charmbracelet Log

## Installation

```bash
go get github.com/charmbracelet/log
```

## Basic Setup

### Simple Usage

```go
package main

import (
    "github.com/charmbracelet/log"
)

func main() {
    // Basic logging - uses global default logger
    log.Info("Hello, World!")
    // Output: 2024/01/15 10:30:00 INFO Hello, World!

    // Structured logging with key-value pairs
    log.Info("User logged in", "user", "alice", "role", "admin")
    // Output: 2024/01/15 10:30:00 INFO User logged in user=alice role=admin

    // Different log levels
    log.Debug("Debug information")
    log.Info("General information")
    log.Warn("Warning message")
    log.Error("Error occurred")
    // log.Fatal("Fatal error - calls os.Exit(1)")

    // Print without level prefix
    log.Print("Custom message without level")
}
```

### Custom Logger Creation

```go
package main

import (
    "os"
    "time"
    "github.com/charmbracelet/log"
)

func main() {
    // Create logger with custom options
    logger := log.NewWithOptions(os.Stdout, log.Options{
        ReportTimestamp: true,
        ReportCaller:    true,
        TimeFormat:      time.RFC3339,
        Level:           log.DebugLevel,
        Prefix:          "myapp",
        Formatter:       log.JSONFormatter,
        Fields:          []any{"service", "api", "version", "1.0"},
    })

    // Use the custom logger
    logger.Info("Custom logger initialized", "status", "ready")
    // JSON output: {"time":"2024-01-15T10:30:00Z","level":"info","caller":"main.go:20","prefix":"myapp","msg":"Custom logger initialized","service":"api","version":"1.0","status":"ready"}
}
```

### Logger Configuration Options

```go
// All available configuration options
options := log.Options{
    ReportTimestamp: true,        // Include timestamp in logs
    TimeFormat:      time.RFC3339, // Custom time format
    ReportCaller:    true,        // Include caller location
    Level:           log.InfoLevel, // Minimum log level
    Prefix:          "app",       // Log message prefix
    Formatter:       log.TextFormatter, // Output format
    Fields:          []any{"env", "dev"}, // Default fields
}

// Apply to logger
logger := log.NewWithOptions(os.Stdout, options)
```

## Log Levels

Charmbracelet Log supports five standard log levels:

```go
// Set log level to filter messages
log.SetLevel(log.DebugLevel) // All messages

// Available levels (from lowest to highest severity)
log.DebugLevel // Detailed debugging
log.InfoLevel  // General information
log.WarnLevel  // Warning conditions
log.ErrorLevel // Error conditions
log.FatalLevel // Fatal errors (calls os.Exit)

// Parse level from string (useful for configuration)
level, err := log.ParseLevel("info")
if err == nil {
    log.SetLevel(level)
}

// Convert level to string
currentLevel := log.GetLevel()
fmt.Printf("Current level: %s\n", currentLevel.String())
```

### Log Level Examples

```go
func setupLogging() {
    // Configure global default logger
    log.SetLevel(log.InfoLevel) // Filter out debug messages
    log.SetReportTimestamp(true)
    log.SetTimeFormat(time.Kitchen) // "3:04PM"
    log.SetPrefix("myapp")

    // Package-level functions use global logger
    log.Debug("This won't be logged") // Filtered out
    log.Info("This will be logged")   // Visible
    log.Warn("Warning message")       // Visible
    log.Error("Error message")        // Visible
}
```

## Structured Logging

### Basic Key-Value Pairs

```go
package main

import (
    "errors"
    "github.com/charmbracelet/log"
)

func main() {
    // Basic structured logging
    log.Info("User action", "user_id", 12345, "action", "login", "ip", "192.168.1.1")

    // Multiple data types
    log.Info("HTTP Request",
        "method", "GET",
        "path", "/api/users",
        "status", 200,
        "duration_ms", 45,
        "user_agent", "curl/7.68.0",
        "authenticated", true,
    )

    // Error logging with structured context
    err := errors.New("connection timeout")
    log.Error("Database operation failed",
        "operation", "SELECT",
        "table", "users",
        "duration_ms", 5000,
        "retry_count", 3,
        "err", err,
    )
}
```

### Formatted Logging

Combine printf-style formatting with structured logging:

```go
package main

import (
    "github.com/charmbracelet/log"
)

func main() {
    temperature := 375
    bakeTime := 15

    // Formatted messages with level methods
    log.Debugf("Temperature set to %d°F", temperature)
    log.Infof("Baking for %d minutes at %d°F", bakeTime, temperature)
    log.Warnf("Temperature exceeds recommended %d°F", 350)
    log.Errorf("Failed to process batch %d: %s", 42, "invalid format")
    log.Printf("Status: %s completed", "processing")

    // Combine with structured fields using sub-loggers
    logger := log.With("batch_id", 42)
    logger.Infof("Step %d/%d completed", 3, 5)
    // Output: INFO Step 3/5 completed batch_id=42
}
```

### Sub-Loggers with Persistent Fields

Create derived loggers with persistent fields:

```go
package main

import (
    "os"
    "github.com/charmbracelet/log"
)

func main() {
    // Base logger with common configuration
    baseLogger := log.NewWithOptions(os.Stdout, log.Options{
        ReportTimestamp: true,
        Prefix:          "myapp",
    })

    // Create sub-logger with persistent fields
    requestLogger := baseLogger.With(
        "request_id", "req-12345",
        "user_id", "user-789",
        "ip", "192.168.1.100",
        "session_id", "sess-abcde",
    )

    // All subsequent logs include persistent fields
    requestLogger.Info("Request received", "path", "/api/users", "method", "GET")
    // Output: 2024/01/15 10:30:00 INFO Request received request_id=req-12345 user_id=user-789 ip=192.168.1.100 session_id=sess-abcde path=/api/users method=GET

    requestLogger.Info("Authentication successful", "provider", "oauth2")
    requestLogger.Info("Data processed", "records", 25, "duration_ms", 120)
    requestLogger.Info("Response sent", "status", 200, "size_bytes", 1024)

    // Create sub-logger with prefix for component separation
    dbLogger := baseLogger.WithPrefix("Database")
    dbLogger.Info("Connection established", "host", "localhost:5432")
    // Output: 2024/01/15 10:30:00 INFO Database Connection established host=localhost:5432
}
```

## Output Formats

Charmbracelet Log supports multiple output formats:

### Text Formatter (Default)

```go
// Human-readable colored output
textLogger := log.NewWithOptions(os.Stdout, log.Options{
    ReportTimestamp: true,
    Formatter:       log.TextFormatter,
})

textLogger.Info("User logged in", "user", "alice", "role", "admin")
// Output: 2024/01/15 10:30:00 INFO User logged in user=alice role=admin
```

### JSON Formatter

```go
// Structured JSON for log aggregation
jsonLogger := log.NewWithOptions(os.Stdout, log.Options{
    ReportTimestamp: true,
    Formatter:       log.JSONFormatter,
})

jsonLogger.Info("User logged in", "user", "alice", "role", "admin")
// Output: {"time":"2024/01/15 10:30:00","level":"info","msg":"User logged in","user":"alice","role":"admin"}
```

### Logfmt Formatter

```go
// Logfmt format for parsing tools
logfmtLogger := log.NewWithOptions(os.Stdout, log.Options{
    ReportTimestamp: true,
    Formatter:       log.LogfmtFormatter,
})

logfmtLogger.Info("User logged in", "user", "alice", "role", "admin")
// Output: time="2024/01/15 10:30:00" level=info msg="User logged in" user=alice role=admin
```

### Environment-Based Format Selection

```go
func setupLogger() {
    var formatter log.Formatter
    switch os.Getenv("LOG_FORMAT") {
    case "json":
        formatter = log.JSONFormatter
    case "logfmt":
        formatter = log.LogfmtFormatter
    default:
        formatter = log.TextFormatter
    }

    logger := log.NewWithOptions(os.Stdout, log.Options{
        Formatter: formatter,
        ReportTimestamp: true,
    })

    log.SetDefault(logger)
    log.Info("Environment-aware logging", "format", os.Getenv("LOG_FORMAT"))
}
```

## Time Configuration

### Custom Time Formats

```go
package main

import (
    "time"
    "github.com/charmbracelet/log"
)

func main() {
    logger := log.NewWithOptions(log.Default().GetOutput(), log.Options{
        ReportTimestamp: true,
    })

    // Standard time formats
    logger.SetTimeFormat(time.RFC3339)          // "2006-01-02T15:04:05Z07:00"
    logger.SetTimeFormat(time.Kitchen)          // "3:04PM"
    logger.SetTimeFormat("2006-01-02 15:04:05") // Custom format
    logger.SetTimeFormat(time.RFC822)           // "02 Jan 06 15:04 MST"

    // Set custom time function (UTC time)
    logger.SetTimeFunction(log.NowUTC)

    // Custom time function with timezone
    logger.SetTimeFunction(func() time.Time {
        return time.Now().UTC().Truncate(time.Second)
    })

    // Disable timestamp reporting
    logger.SetReportTimestamp(false)

    logger.Info("Time configuration demo", "timestamp_format", "custom")
}
```

## Caller Location Reporting

Show source code location for log entries:

```go
package main

import (
    "github.com/charmbracelet/log"
)

func processData() {
    log.Info("Processing data")
}

func main() {
    // Enable caller reporting
    log.SetReportCaller(true)

    // Default caller formatter (short path)
    log.Info("Caller reporting enabled")
    // Output: INFO <main.go:23> Caller reporting enabled

    // Long caller formatter (full path)
    log.SetCallerFormatter(log.LongCallerFormatter)
    log.Info("Long caller format")
    // Output: INFO <github.com/user/project/main.go:26> Long caller format

    // Adjust caller offset to skip helper functions
    log.SetCallerOffset(1)

    processData() // Will show correct caller location
}
```

### Helper Function Marking

Mark helper functions to skip in caller reporting:

```go
// Helper function wrapper
func logError(msg string, err error) {
    // Mark this as a helper function so caller reporting skips it
    log.Helper()
    log.Error(msg, "err", err)
}

func debugWrapper(msg string, keyvals ...any) {
    log.Helper()
    log.Debug(msg, keyvals...)
}

// Application functions
func processUser(userID int) error {
    log.SetReportCaller(true)

    // This will report processUser as the caller, not debugWrapper
    debugWrapper("Starting user processing", "user_id", userID)
    // Output: DEBUG <main.go:35> Starting user processing user_id=42

    if userID <= 0 {
        logError("Invalid user ID", errors.New("user ID must be positive"))
        // Output: ERROR <main.go:39> Invalid user ID err=user ID must be positive
        return errors.New("invalid user")
    }

    return nil
}
```

## Context Integration

Store and retrieve loggers from Go context:

```go
package main

import (
    "context"
    "net/http"
    "github.com/charmbracelet/log"
)

// Middleware to add logger to request context
func loggingMiddleware(next http.Handler) http.Handler {
    return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        // Create request-specific logger with context
        requestLogger := log.Default().With(
            "request_id", generateRequestID(),
            "method", r.Method,
            "path", r.URL.Path,
            "remote_addr", r.RemoteAddr,
            "user_agent", r.UserAgent(),
        )

        // Store logger in context
        ctx := log.WithContext(r.Context(), requestLogger)

        // Pass context with logger to next handler
        next.ServeHTTP(w, r.WithContext(ctx))
    })
}

func handleAPIRequest(w http.ResponseWriter, r *http.Request) {
    // Retrieve logger from context
    logger := log.FromContext(r.Context())

    logger.Info("Processing API request")

    // Process data with context propagation
    result, err := processUserData(r.Context(), "user123")
    if err != nil {
        logger.Error("Failed to process user data", "err", err, "user_id", "user123")
        http.Error(w, "Internal server error", http.StatusInternalServerError)
        return
    }

    logger.Info("Request processed successfully", "result", result)
    w.WriteHeader(http.StatusOK)
}

func processUserData(ctx context.Context, userID string) (string, error) {
    logger := log.FromContext(ctx)
    logger.Debug("Processing user data", "user_id", userID)
    return "processed_data", nil
}

func generateRequestID() string {
    return "req-" + time.Now().Format("20060102150405")
}
```

## Standard Library Integration

### slog Handler Integration

Works with Go's standard log/slog package:

```go
package main

import (
    "log/slog"
    "os"
    "time"
    "github.com/charmbracelet/log"
)

func main() {
    // Create charm log handler with options
    handler := log.NewWithOptions(os.Stdout, log.Options{
        ReportTimestamp: true,
        TimeFunction:    log.NowUTC,
        TimeFormat:      time.RFC3339,
        Level:           log.DebugLevel,
        Prefix:          "app",
    })

    // Create slog logger with charm handler
    logger := slog.New(handler)

    // Use standard slog API with charm styling
    logger.Info("Application started",
        slog.String("version", "1.0.0"),
        slog.Int("port", 8080),
        slog.Bool("debug", true),
    )

    logger.Debug("Debug information",
        slog.Group("server",
            slog.String("host", "localhost"),
            slog.Int("port", 8080),
            slog.String("protocol", "http"),
        ),
    )

    logger.Error("Error occurred",
        slog.String("error", "connection refused"),
        slog.Int("retry_count", 3),
    )
}
```

### Standard Log Adapter

Create adapters for compatibility with existing code:

```go
package main

import (
    "log"
    "net/http"
    "os"
    "github.com/charmbracelet/log"
)

func main() {
    // Create charm logger
    charmLogger := log.NewWithOptions(os.Stderr, log.Options{
        Prefix:          "http",
        ReportTimestamp: true,
    })

    // Create standard log adapter with forced level
    stdlog := charmLogger.StandardLog(log.StandardLogOptions{
        ForceLevel: log.ErrorLevel,
    })

    // Use with HTTP server error logging
    server := &http.Server{
        Addr:     ":8080",
        Handler:  http.DefaultServeMux,
        ErrorLog: stdlog, // Expects *log.Logger
    }

    // Standard log adapter that infers levels from message prefixes
    inferLogger := charmLogger.StandardLog()
    inferLogger.Println("INFO: Server started")    // Logged as Info
    inferLogger.Println("ERROR: Connection failed") // Logged as Error
    inferLogger.Println("WARN: High memory usage")  // Logged as Warning
    inferLogger.Println("DEBUG: Request details")   // Logged as Debug
    inferLogger.Println("Regular message")          // Logged as Info (default)

    charmLogger.Info("Starting server", "addr", server.Addr)
    // server.ListenAndServe() // Uncomment to start server
}
```

## Environment-Based Configuration

Configure logging based on environment variables:

```go
package main

import (
    "os"
    "strconv"
    "github.com/charmbracelet/log"
)

type LoggerConfig struct {
    Level           log.Level
    Format          string
    ReportTimestamp bool
    ReportCaller    bool
    Prefix          string
}

func loadConfig() LoggerConfig {
    return LoggerConfig{
        Level:           parseLevel(getEnv("LOG_LEVEL", "info")),
        Format:          getEnv("LOG_FORMAT", "text"),
        ReportTimestamp: getEnvBool("LOG_TIMESTAMP", true),
        ReportCaller:    getEnvBool("LOG_CALLER", false),
        Prefix:          getEnv("APP_NAME", "app"),
    }
}

func setupLogger() {
    config := loadConfig()

    var formatter log.Formatter
    switch config.Format {
    case "json":
        formatter = log.JSONFormatter
    case "logfmt":
        formatter = log.LogfmtFormatter
    default:
        formatter = log.TextFormatter
    }

    logger := log.NewWithOptions(os.Stdout, log.Options{
        Level:           config.Level,
        Formatter:       formatter,
        ReportTimestamp: config.ReportTimestamp,
        ReportCaller:    config.ReportCaller,
        Prefix:          config.Prefix,
    })

    log.SetDefault(logger)
    log.Info("Logger configured from environment",
        "level", config.Level.String(),
        "format", config.Format,
        "prefix", config.Prefix)
}

func parseLevel(levelStr string) log.Level {
    level, err := log.ParseLevel(levelStr)
    if err != nil {
        return log.InfoLevel
    }
    return level
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
    setupLogger()

    log.Info("Application started", "env", os.Getenv("ENVIRONMENT"))
    log.Debug("Debug mode enabled", "level", log.GetLevel().String())
}
```

## Next Steps

After mastering the basics, explore:

1. **Custom Styling**: See [styling-guide.md](styling-guide.md) for beautiful terminal output
2. **Production Deployment**: See [production-guide.md](production-guide.md) for production patterns
3. **Integration Examples**: Use with Bubble Tea and other Charm libraries
4. **Advanced Configuration**: Multiple output destinations and custom time functions
5. **Testing**: Mock logging for unit tests

## Common Pitfalls

1. **Missing Context**: Forgetting to pass context through the call chain
   ```go
   // ❌ Bad - context lost
   func processRequest(req Request) {
       log.Info("Processing", "id", req.ID)
       processData(req.Data) // Context lost here
   }

   // ✅ Good - context propagated
   func processRequest(ctx context.Context, req Request) {
       logger := log.FromContext(ctx)
       logger.Info("Processing", "id", req.ID)
       processData(ctx, req.Data) // Context preserved
   }
   ```

2. **Incorrect Log Level**: Messages may not appear if level is too high
   ```go
   // Check if logging is configured correctly
   log.SetLevel(log.DebugLevel) // Show all messages for debugging
   fmt.Printf("Current log level: %s\n", log.GetLevel().String())
   ```

3. **Mixing Formatters**: Different formatters may not work well together
   ```go
   // ✅ Consistent formatting across the application
   logger := log.NewWithOptions(os.Stdout, log.Options{
       Formatter: log.JSONFormatter, // Use one format consistently
   })
   log.SetDefault(logger)
   ```