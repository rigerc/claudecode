# Charmbracelet Log: Minimal and Colorful Go Logging Library

## Overview

**Charmbracelet Log** is a minimal, colorful, and structured logging library for Go applications that provides leveled logging with human-readable terminal output. Built as part of the Charm ecosystem, it combines beautiful visual styling using Lip Gloss with powerful structured logging capabilities, making it ideal for command-line applications, developer tools, and modern Go services.

### Key Features
- **Minimal API**: Simple, intuitive interface for quick adoption
- **Beautiful Output**: Colorful, styled terminal output using Lip Gloss
- **Structured Logging**: Key-value pairs for structured data
- **Multiple Formatters**: Text, JSON, and logfmt output formats
- **Leveled Logging**: Debug, Info, Warn, Error, and Fatal levels
- **Context Integration**: Seamless integration with Go's context package
- **Sub-loggers**: Persistent contextual fields for component-based logging
- **Standard Library Compatibility**: Drop-in replacement for Go's standard logger
- **Slog Handler**: Works with Go's standard log/slog package

## Installation

```bash
go get github.com/charmbracelet/log
```

## Quick Start

```go
package main

import (
    "github.com/charmbracelet/log"
)

func main() {
    // Simple logging with global default logger
    log.Info("Hello, World!")
    // Output: 2024/01/15 10:30:00 INFO Hello, World!

    // Structured logging with key-value pairs
    log.Info("User logged in", "user", "alice", "role", "admin")
    // Output: 2024/01/15 10:30:00 INFO User logged in user=alice role=admin

    // Different log levels
    log.Debug("Debug information")
    log.Warn("Warning message")
    log.Error("Error occurred")
}
```

## Core Concepts

### Logger Creation and Configuration

Charmbracelet Log provides multiple ways to create and configure loggers:

```go
package main

import (
    "os"
    "time"
    "github.com/charmbracelet/log"
)

func main() {
    // Basic logger with default settings
    logger := log.New(os.Stderr)
    logger.Info("Basic logger created")

    // Logger with custom options
    customLogger := log.NewWithOptions(os.Stdout, log.Options{
        ReportTimestamp: true,
        ReportCaller:    true,
        TimeFormat:      time.RFC3339,
        Level:           log.DebugLevel,
        Prefix:          "myapp",
        Formatter:       log.JSONFormatter,
        Fields:          []any{"service", "api", "version", "1.0"},
    })

    customLogger.Info("Custom logger initialized", "status", "ready")
}
```

### Available Options

```go
// All configurable options
options := log.Options{
    ReportTimestamp: true,        // Include timestamp in logs
    TimeFormat:      time.RFC3339, // Custom time format
    ReportCaller:    true,        // Include caller location
    Level:           log.InfoLevel, // Minimum log level
    Prefix:          "app",       // Log message prefix
    Formatter:       log.TextFormatter, // Output format
    Fields:          []any{"env", "dev"}, // Default fields
}
```

### Log Levels

Charmbracelet Log supports five standard log levels:

```go
// Set log level to filter messages
log.SetLevel(log.DebugLevel) // All messages

// Log levels in order of severity
log.Debug("Detailed debugging information")
log.Info("General informational messages")
log.Warn("Warning conditions")
log.Error("Error conditions")
log.Fatal("Fatal errors - calls os.Exit(1)")

// Print without level prefix
log.Print("Custom message without level")

// Available levels (from lowest to highest severity)
log.DebugLevel // Detailed debugging
log.InfoLevel  // General information
log.WarnLevel  // Warning conditions
log.ErrorLevel // Error conditions
log.FatalLevel // Fatal errors

// Parse level from string (useful for configuration)
level, err := log.ParseLevel("info")
if err == nil {
    log.SetLevel(level)
}
```

### Structured Logging with Key-Value Pairs

The library emphasizes structured logging with key-value pairs:

```go
package main

import (
    "github.com/charmbracelet/log"
)

func main() {
    // Basic structured logging
    log.Info("User action", "user_id", 12345, "action", "login", "ip", "192.168.1.1")

    // Complex structured data
    log.Info("HTTP Request",
        "method", "GET",
        "path", "/api/users",
        "status", 200,
        "duration_ms", 45,
        "user_agent", "curl/7.68.0",
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

Printf-style formatting while maintaining structured logging:

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
    logger := log.With("batch_id", 42, "process", "baking")
    logger.Infof("Step %d/%d completed", 3, 5)
    // Output: INFO Step 3/5 completed batch_id=42 process=baking
}
```

## Advanced Features

### Sub-Loggers and Context Fields

Create derived loggers with persistent fields for contextual logging:

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
    requestLogger.Info("Authentication successful", "provider", "oauth2")
    requestLogger.Info("Data processed", "records", 25, "duration_ms", 120)
    requestLogger.Info("Response sent", "status", 200, "size_bytes", 1024)

    // Create sub-logger with prefix for component separation
    dbLogger := baseLogger.WithPrefix("Database")
    dbLogger.Info("Connection established", "host", "localhost:5432")
    dbLogger.Info("Query executed", "sql", "SELECT * FROM users", "rows", 10)

    // Chain sub-loggers for nested contexts
    dbTransactionLogger := dbLogger.With("tx_id", "tx-98765")
    dbTransactionLogger.Info("Transaction started")
    dbTransactionLogger.Info("Query executed", "table", "orders", "affected_rows", 5)
    dbTransactionLogger.Info("Transaction committed")
}
```

### Output Formatters

Supports multiple output formats for different use cases:

```go
package main

import (
    "os"
    "github.com/charmbracelet/log"
)

func main() {
    // Text Formatter (default) - Human-readable with colors
    textLogger := log.NewWithOptions(os.Stdout, log.Options{
        ReportTimestamp: true,
        Formatter:       log.TextFormatter,
    })
    textLogger.Info("User logged in", "user", "alice", "role", "admin")
    // Output: 2024/01/15 10:30:00 INFO User logged in user=alice role=admin

    // JSON Formatter - For log aggregation systems
    jsonLogger := log.NewWithOptions(os.Stdout, log.Options{
        ReportTimestamp: true,
        Formatter:       log.JSONFormatter,
    })
    jsonLogger.Info("User logged in", "user", "alice", "role", "admin")
    // Output: {"time":"2024/01/15 10:30:00","level":"info","msg":"User logged in","user":"alice","role":"admin"}

    // Logfmt Formatter - For log parsing tools
    logfmtLogger := log.NewWithOptions(os.Stdout, log.Options{
        ReportTimestamp: true,
        Formatter:       log.LogfmtFormatter,
    })
    logfmtLogger.Info("User logged in", "user", "alice", "role", "admin")
    // Output: time="2024/01/15 10:30:00" level=info msg="User logged in" user=alice role=admin

    // Switch between formats based on environment
    var logger *log.Logger
    if os.Getenv("ENVIRONMENT") == "production" {
        logger = log.NewWithOptions(os.Stdout, log.Options{
            Formatter: log.JSONFormatter,
        })
    } else {
        logger = log.NewWithOptions(os.Stdout, log.Options{
            Formatter:    log.TextFormatter,
            ReportCaller: true,
        })
    }
    logger.Info("Environment-aware logging", "env", os.Getenv("ENVIRONMENT"))
}
```

### Custom Styling with Lip Gloss

Customize the visual appearance of log output:

```go
package main

import (
    "os"
    "github.com/charmbracelet/log"
    "github.com/charmbracelet/lipgloss"
)

func main() {
    logger := log.New(os.Stdout)

    // Get default styles and customize them
    styles := log.DefaultStyles()

    // Customize error level styling
    styles.Levels[log.ErrorLevel] = lipgloss.NewStyle().
        SetString("🔴 ERROR").
        Padding(0, 1, 0, 1).
        Background(lipgloss.Color("196")).
        Foreground(lipgloss.Color("15")).
        Bold(true)

    // Customize warning level with emoji
    styles.Levels[log.WarnLevel] = lipgloss.NewStyle().
        SetString("⚠️  WARN").
        Foreground(lipgloss.Color("226")).
        Bold(true)

    // Customize info level
    styles.Levels[log.InfoLevel] = lipgloss.NewStyle().
        SetString("ℹ️  INFO").
        Foreground(lipgloss.Color("86")).
        Bold(true)

    // Customize debug level
    styles.Levels[log.DebugLevel] = lipgloss.NewStyle().
        SetString("🐛 DEBUG").
        Foreground(lipgloss.Color("245")).
        Italic(true)

    // Custom styles for specific keys
    styles.Keys["user"] = lipgloss.NewStyle().
        Foreground(lipgloss.Color("86")).
        Bold(true)

    styles.Keys["err"] = lipgloss.NewStyle().
        Foreground(lipgloss.Color("196")).
        Bold(true)

    styles.Keys["request_id"] = lipgloss.NewStyle().
        Foreground(lipgloss.Color("147")).
        Italic(true)

    // Custom styles for specific values
    styles.Values["err"] = lipgloss.NewStyle().
        Bold(true).
        Foreground(lipgloss.Color("196"))

    styles.Values["user"] = lipgloss.NewStyle().
        Foreground(lipgloss.Color("120"))

    // Apply custom styles
    logger.SetStyles(styles)

    // Test styled output
    logger.Debug("Processing request", "request_id", "req-123")
    logger.Info("User authenticated", "user", "alice")
    logger.Warn("High memory usage", "usage_mb", 850, "limit_mb", 1024)
    logger.Error("Database connection failed", "err", "connection timeout", "retries", 3)
}
```

### Time Configuration

Customize timestamp formatting and time functions:

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

### Caller Location Reporting

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

### Context Integration

Seamlessly integrate with Go's context package:

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

func main() {
    mux := http.NewServeMux()
    mux.HandleFunc("/api/users", handleAPIRequest)

    handler := loggingMiddleware(mux)
    log.Info("Server starting", "port", 8080)
    http.ListenAndServe(":8080", handler)
}
```

### Helper Functions for Caller Reporting

Mark helper functions to skip in caller stack traces:

```go
package main

import (
    "errors"
    "github.com/charmbracelet/log"
)

// Helper function wrapper
func logError(msg string, err error) {
    // Mark this as a helper function so caller reporting skips it
    log.Helper()
    log.Error(msg, "err", err)
}

func logDebug(msg string, keyvals ...any) {
    log.Helper()
    log.Debug(msg, keyvals...)
}

// Application functions
func processUser(userID int) error {
    log.SetReportCaller(true)

    // This will report processUser as the caller, not logDebug
    logDebug("Starting user processing", "user_id", userID)
    // Output: DEBUG <main.go:35> Starting user processing user_id=42

    // Process user data
    if userID <= 0 {
        logError("Invalid user ID", errors.New("user ID must be positive"))
        // Output: ERROR <main.go:39> Invalid user ID err=user ID must be positive
        return errors.New("invalid user")
    }

    logDebug("User processing completed", "user_id", userID)
    return nil
}

// Method with helper logging
type UserService struct {
    logger *log.Logger
}

func (us *UserService) logOperation(operation string, userID string) {
    us.logger.Helper()
    us.logger.Info(operation, "user_id", userID)
}

func (us *UserService) processUser(userID string) error {
    us.logger.SetReportCaller(true)

    // Reports processUser as caller, not logOperation
    us.logOperation("Starting user processing", userID)
    // Output: INFO <main.go:58> Starting user processing user_id=alice

    return nil
}

func main() {
    processUser(42)
    processUser(-1)

    userService := &UserService{logger: log.New(log.Default().GetOutput())}
    userService.processUser("alice")
}
```

### Standard Library Integration

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
        ForceLevel: log.ErrorLevel, // All messages logged at Error level
    })

    // Use with HTTP server error logging
    server := &http.Server{
        Addr:     ":8080",
        Handler:  http.DefaultServeMux,
        ErrorLog: stdlog, // Expects *log.Logger
    }

    // Standard log adapter that infers levels from message prefixes
    inferLogger := charmLogger.StandardLog()
    inferLogger.Println("INFO: Server starting")    // Logged as Info
    inferLogger.Println("ERROR: Connection failed") // Logged as Error
    inferLogger.Println("WARN: High memory usage")  // Logged as Warning
    inferLogger.Println("DEBUG: Request details")   // Logged as Debug
    inferLogger.Println("Regular message")          // Logged as Info (default)

    // Use with existing libraries that expect *log.Logger
    databaseLogger := log.New(os.Stderr).StandardLog(log.StandardLogOptions{
        ForceLevel: log.DebugLevel,
    })
    log.SetOutput(databaseLogger.Writer()) // Redirect standard log

    log.Println("This will use charm logging")
    log.Printf("Formatted message: %s", "hello")

    charmLogger.Info("Starting server", "addr", server.Addr)
    // server.ListenAndServe() // Uncomment to start server
}
```

### Slog Handler Integration

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

    logger.Warn("Performance warning",
        slog.Float64("response_time", 2.5),
        slog.Float64("threshold", 1.0),
    )

    logger.Error("Error occurred",
        slog.String("error", "connection refused"),
        slog.Int("retry_count", 3),
        slog.Duration("retry_delay", time.Second*5),
    )

    // Custom attributes
    logger.Info("Custom attributes",
        slog.Any("metadata", map[string]interface{}{
            "service": "api",
            "env":     "production",
        }),
    )
}
```

## Configuration and Customization

### Global Default Logger Configuration

Configure the package-level default logger:

```go
package main

import (
    "os"
    "time"
    "github.com/charmbracelet/log"
)

func main() {
    // Configure global default logger
    log.SetLevel(log.DebugLevel)
    log.SetReportTimestamp(true)
    log.SetTimeFormat(time.Kitchen)
    log.SetPrefix("myapp")

    // Enable caller reporting with custom formatter
    log.SetReportCaller(true)
    log.SetCallerFormatter(log.LongCallerFormatter)

    // Set custom output
    logFile, _ := os.Create("app.log")
    log.SetOutput(logFile)

    // Replace default logger completely
    customLogger := log.NewWithOptions(log.Default().GetOutput(), log.Options{
        Formatter:       log.JSONFormatter,
        ReportTimestamp: true,
        Level:           log.InfoLevel,
    })
    log.SetDefault(customLogger)

    // All package-level calls now use the new default logger
    log.Info("Using custom default logger", "format", "json")
    log.Debug("This won't show due to InfoLevel")
    log.Error("Error message", "key", "value")
}
```

### Environment-Based Configuration

Configure logging based on environment variables:

```go
package main

import (
    "os"
    "strconv"
    "github.com/charmbracelet/log"
)

func configureLogger() {
    // Get configuration from environment
    levelStr := getEnv("LOG_LEVEL", "info")
    format := getEnv("LOG_FORMAT", "text")
    timestamp := getEnvBool("LOG_TIMESTAMP", true)
    caller := getEnvBool("LOG_CALLER", false)

    // Parse log level
    level, err := log.ParseLevel(levelStr)
    if err != nil {
        level = log.InfoLevel
        log.Warn("Invalid LOG_LEVEL, using default", "provided", levelStr, "default", "info")
    }

    // Create logger with environment-based configuration
    var formatter log.Formatter
    switch format {
    case "json":
        formatter = log.JSONFormatter
    case "logfmt":
        formatter = log.LogfmtFormatter
    default:
        formatter = log.TextFormatter
    }

    logger := log.NewWithOptions(os.Stdout, log.Options{
        Level:           level,
        Formatter:       formatter,
        ReportTimestamp: timestamp,
        ReportCaller:    caller,
        Prefix:          getEnv("APP_NAME", "app"),
    })

    log.SetDefault(logger)
    log.Info("Logger configured from environment", "level", level.String(), "format", format)
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
    configureLogger()
    log.Info("Application started")
    log.Debug("Debug information")
    log.Warn("Warning message")
}
```

### Multiple Output Destinations

Write to multiple outputs simultaneously:

```go
package main

import (
    "io"
    "os"
    "github.com/charmbracelet/log"
)

func main() {
    // Create multi-writer for console and file
    file, _ := os.Create("app.log")
    multiWriter := io.MultiWriter(os.Stdout, file)

    // Logger with multi-writer
    logger := log.NewWithOptions(multiWriter, log.Options{
        ReportTimestamp: true,
        Prefix:          "multi-output",
    })

    logger.Info("This message goes to both stdout and file")

    // Separate loggers for different outputs
    consoleLogger := log.NewWithOptions(os.Stdout, log.Options{
        Formatter: log.TextFormatter,
        Prefix:    "console",
    })

    fileLogger := log.NewWithOptions(file, log.Options{
        Formatter: log.JSONFormatter,
        Prefix:    "file",
    })

    consoleLogger.Info("Colorful console output")
    fileLogger.Info("Structured file output", "structured", true)
}
```

## Use Cases and Patterns

### CLI Applications

Perfect for command-line tools with beautiful output:

```go
package main

import (
    "flag"
    "fmt"
    "os"
    "github.com/charmbracelet/log"
)

func main() {
    // Command-line flags for logging configuration
    var (
        verbose   bool
        json      bool
        logFile   string
    )

    flag.BoolVar(&verbose, "verbose", false, "Enable debug logging")
    flag.BoolVar(&json, "json", false, "Output JSON logs")
    flag.StringVar(&logFile, "log-file", "", "Write logs to file")
    flag.Parse()

    // Configure logger based on flags
    var output io.Writer = os.Stderr
    if logFile != "" {
        file, err := os.Create(logFile)
        if err != nil {
            fmt.Fprintf(os.Stderr, "Failed to create log file: %v\n", err)
            os.Exit(1)
        }
        output = file
    }

    formatter := log.TextFormatter
    if json {
        formatter = log.JSONFormatter
    }

    level := log.InfoLevel
    if verbose {
        level = log.DebugLevel
    }

    logger := log.NewWithOptions(output, log.Options{
        Level:           level,
        Formatter:       formatter,
        ReportTimestamp: true,
        ReportCaller:    verbose,
        Prefix:          "cli-app",
    })

    // Use configured logger
    logger.Info("CLI application started", "args", flag.Args())
    logger.Debug("Debug mode enabled")

    if len(flag.Args()) == 0 {
        logger.Warn("No arguments provided")
    }

    // Application logic
    processFiles(logger, flag.Args())
}

func processFiles(logger *log.Logger, files []string) {
    for i, file := range files {
        logger.Info("Processing file", "file", file, "index", i+1, "total", len(files))
        // Process file...
    }
    logger.Info("All files processed", "count", len(files))
}
```

### Microservices Logging

Structured logging for microservice environments:

```go
package main

import (
    "net/http"
    "os"
    "time"
    "github.com/charmbracelet/log"
)

type Service struct {
    name    string
    version string
    logger  *log.Logger
}

func NewService(name, version string) *Service {
    logger := log.NewWithOptions(os.Stdout, log.Options{
        ReportTimestamp: true,
        Formatter:       getLogFormat(),
        Level:           getLogLevel(),
        Fields: []any{
            "service", name,
            "version", version,
            "instance_id", getInstanceID(),
        },
    })

    return &Service{
        name:    name,
        version: version,
        logger:  logger,
    }
}

func (s *Service) Start(port string) error {
    s.logger.Info("Starting service", "port", port)

    // HTTP middleware for request logging
    handler := s.loggingMiddleware(http.HandlerFunc(s.handleRequest))

    server := &http.Server{
        Addr:         ":" + port,
        Handler:      handler,
        ReadTimeout:  5 * time.Second,
        WriteTimeout: 10 * time.Second,
    }

    s.logger.Info("Server listening", "port", port)
    return server.ListenAndServe()
}

func (s *Service) loggingMiddleware(next http.Handler) http.Handler {
    return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        start := time.Now()

        // Create request logger
        requestLogger := s.logger.With(
            "method", r.Method,
            "path", r.URL.Path,
            "remote_addr", r.RemoteAddr,
            "user_agent", r.UserAgent(),
        )

        // Process request
        next.ServeHTTP(w, r)

        // Log request completion
        duration := time.Since(start)
        requestLogger.Info("Request completed", "duration_ms", duration.Milliseconds())
    })
}

func (s *Service) handleRequest(w http.ResponseWriter, r *http.Request) {
    logger := log.FromContext(r.Context())
    logger.Info("Handling request")

    w.WriteHeader(http.StatusOK)
    w.Write([]byte("Hello from " + s.name))
}

func getLogFormat() log.Formatter {
    if os.Getenv("LOG_FORMAT") == "json" {
        return log.JSONFormatter
    }
    return log.TextFormatter
}

func getLogLevel() log.Level {
    if levelStr := os.Getenv("LOG_LEVEL"); levelStr != "" {
        if level, err := log.ParseLevel(levelStr); err == nil {
            return level
        }
    }
    return log.InfoLevel
}

func getInstanceID() string {
    if id := os.Getenv("INSTANCE_ID"); id != "" {
        return id
    }
    return "local-dev"
}

func main() {
    service := NewService("user-service", "1.0.0")
    if err := service.Start("8080"); err != nil {
        log.Fatal("Service failed", "err", err)
    }
}
```

### Development vs Production Logging

Environment-aware logging configuration:

```go
package main

import (
    "os"
    "github.com/charmbracelet/log"
)

type LoggerConfig struct {
    Level           log.Level
    Format          log.Formatter
    ReportTimestamp bool
    ReportCaller    bool
    Prefix          string
}

func getProductionConfig() LoggerConfig {
    return LoggerConfig{
        Level:           log.InfoLevel,
        Format:          log.JSONFormatter,
        ReportTimestamp: true,
        ReportCaller:    false,
        Prefix:          "production",
    }
}

func getDevelopmentConfig() LoggerConfig {
    return LoggerConfig{
        Level:           log.DebugLevel,
        Format:          log.TextFormatter,
        ReportTimestamp: true,
        ReportCaller:    true,
        Prefix:          "dev",
    }
}

func setupLogger() *log.Logger {
    env := os.Getenv("ENVIRONMENT")
    var config LoggerConfig

    switch env {
    case "production", "prod":
        config = getProductionConfig()
    case "staging":
        config = getProductionConfig()
        config.Level = log.DebugLevel
    default:
        config = getDevelopmentConfig()
    }

    return log.NewWithOptions(os.Stdout, log.Options{
        Level:           config.Level,
        Formatter:       config.Format,
        ReportTimestamp: config.ReportTimestamp,
        ReportCaller:    config.ReportCaller,
        Prefix:          config.Prefix,
        Fields: []any{
            "service", "myapp",
            "version", os.Getenv("APP_VERSION"),
            "env", env,
        },
    })
}

func main() {
    logger := setupLogger()
    log.SetDefault(logger)

    log.Info("Application started", "config", "loaded")
    log.Debug("Debug information visible in development")
    log.Info("Structured logging works in all environments")
}
```

### Testing with Logging

Mock and test logging behavior:

```go
package main

import (
    "bytes"
    "strings"
    "testing"
    "github.com/charmbracelet/log"
)

func TestProcessUser(t *testing.T) {
    // Capture log output
    var buf bytes.Buffer
    logger := log.NewWithOptions(&buf, log.Options{
        ReportTimestamp: false,
        Prefix:          "test",
    })

    // Test function that logs
    processUserWithLogger(logger, "alice", "admin")

    output := buf.String()

    // Verify log output contains expected information
    if !strings.Contains(output, "Processing user") {
        t.Errorf("Expected 'Processing user' in log output: %s", output)
    }
    if !strings.Contains(output, "user=alice") {
        t.Errorf("Expected 'user=alice' in log output: %s", output)
    }
    if !strings.Contains(output, "role=admin") {
        t.Errorf("Expected 'role=admin' in log output: %s", output)
    }
}

func TestErrorHandling(t *testing.T) {
    var buf bytes.Buffer
    logger := log.NewWithOptions(&buf, log.Options{
        ReportTimestamp: false,
    })

    err := processWithError(logger, "invalid-input")

    if err == nil {
        t.Error("Expected error but got nil")
    }

    output := buf.String()
    if !strings.Contains(output, "ERROR") {
        t.Error("Expected ERROR in log output")
    }
}

func processUserWithLogger(logger *log.Logger, user, role string) {
    logger.Info("Processing user", "user", user, "role", role)
    // Processing logic...
}

func processWithError(logger *log.Logger, input string) error {
    logger.Debug("Processing input", "input", input)
    if input == "invalid-input" {
        logger.Error("Invalid input detected", "input", input)
        return log.NewError("invalid input")
    }
    return nil
}
```

## Best Practices

### Performance Considerations

1. **Use Appropriate Log Levels**: Set appropriate minimum log levels for production
2. **Avoid String Concatenation**: Use structured key-value pairs instead
3. **Lazy Evaluation**: For expensive computations, check if logging is enabled
4. **Reuse Loggers**: Create loggers once and reuse them
5. **Consider Sampling**: For high-volume logs, implement sampling strategies

```go
// Good: Structured logging
log.Info("User action", "user", id, "action", "login")

// Avoid: String concatenation
log.Info(fmt.Sprintf("User %s performed %s", id, action))

// Check if debug logging is enabled before expensive operations
if log.Default().GetLevel() <= log.DebugLevel {
    debugInfo := computeExpensiveDebugInfo()
    log.Debug("Debug info", "details", debugInfo)
}
```

### Security Considerations

1. **Sensitive Data**: Avoid logging passwords, tokens, or PII
2. **Sanitize Input**: Clean user input before logging
3. **Log Rotation**: Implement log rotation to prevent disk exhaustion
4. **Access Control**: Restrict access to log files

```go
// Avoid logging sensitive data
log.Info("User login", "user_id", userID) // Good
log.Info("User login", "password", password) // Bad!

// Sanitize input
func sanitizeInput(input string) string {
    // Remove or mask sensitive information
    return strings.ReplaceAll(input, "secret", "***")
}

log.Info("API request", "query", sanitizeInput(queryParam))
```

### Structured Logging Guidelines

1. **Consistent Keys**: Use consistent key names across your application
2. **Meaningful Messages**: Write clear, descriptive log messages
3. **Contextual Information**: Include relevant context (request IDs, user IDs)
4. **Structured Data**: Use appropriate data types (numbers, booleans)

```go
// Good: Consistent, structured logging
log.Info("API request completed",
    "request_id", "req-123",
    "user_id", "user-456",
    "method", "GET",
    "path", "/api/users",
    "status", 200,
    "duration_ms", 45,
    "cache_hit", true,
)

// Bad: Inconsistent, unstructured logging
log.Info("Request done", "req-123 GET /api/users 200 45ms")
```

## Troubleshooting

### Common Issues

**1. Logs not appearing**
```go
// Check log level
currentLevel := log.Default().GetLevel()
if currentLevel > log.DebugLevel {
    log.SetLevel(log.DebugLevel) // Lower level to see more messages
}

// Verify output destination
if log.Default().GetOutput() == nil {
    log.SetOutput(os.Stderr)
}
```

**2. Missing timestamps**
```go
// Enable timestamp reporting
log.SetReportTimestamp(true)

// Set custom time format
log.SetTimeFormat(time.RFC3339)
```

**3. Caller location not showing**
```go
// Enable caller reporting
log.SetReportCaller(true)

// Check for helper functions
func debugWrapper(msg string) {
    log.Helper() // Skip this function in caller reporting
    log.Debug(msg)
}
```

**4. Colors not showing in output**
```go
// Colors are automatically disabled when output is not a TTY
// To force colors, use a different output:
logger := log.New(os.Stdout) // os.Stdout is typically a TTY in terminals

// Or check if colors are supported
if lipgloss.HasColor() {
    // Colors are supported
}
```

### Debug Mode

Enable comprehensive debugging:

```go
func enableDebugMode() {
    logger := log.NewWithOptions(os.Stdout, log.Options{
        Level:           log.DebugLevel,
        ReportTimestamp: true,
        ReportCaller:    true,
        Prefix:          "DEBUG",
    })

    // Custom styles for debugging
    styles := log.DefaultStyles()
    styles.Levels[log.DebugLevel] = lipgloss.NewStyle().
        SetString("DEBUG").
        Foreground(lipgloss.Color("8")).
        Italic(true)
    logger.SetStyles(styles)

    log.SetDefault(logger)
    log.Debug("Debug mode enabled", "level", logger.GetLevel().String())
}
```

## Integration Examples

### With Bubble Tea

Integrate with Bubble Tea TUI applications:

```go
package main

import (
    "github.com/charmbracelet/bubbletea"
    "github.com/charmbracelet/log"
)

type model struct {
    logger *log.Logger
    items  []string
}

func (m model) Init() tea.Cmd {
    m.logger.Info("Application initialized", "items_count", len(m.items))
    return nil
}

func (m model) Update(msg tea.Msg) (tea.Model, tea.Cmd) {
    switch msg := msg.(type) {
    case tea.KeyMsg:
        m.logger.Debug("Key pressed", "key", msg.String())
        // Handle key messages...
    }
    return m, nil
}

func (m model) View() string {
    return "Hello, Bubble Tea!"
}

func main() {
    logger := log.NewWithOptions(log.Default().GetOutput(), log.Options{
        ReportTimestamp: true,
        Prefix:          "bubbletea-app",
    })

    initialModel := model{
        logger: logger,
        items:  []string{"item1", "item2"},
    }

    p := tea.NewProgram(initialModel)
    if _, err := p.Run(); err != nil {
        logger.Error("Bubble Tea program failed", "err", err)
    }
}
```

### With Other Charm Libraries

Works seamlessly with other Charm ecosystem libraries:

```go
package main

import (
    "github.com/charmbracelet/bubbles/list"
    "github.com/charmbracelet/lipgloss"
    "github.com/charmbracelet/log"
)

func main() {
    // Shared styling across Charm libraries
    docStyle := lipgloss.NewStyle().Margin(1, 2)

    // Logger with consistent styling
    logger := log.NewWithOptions(log.Default().GetOutput(), log.Options{
        ReportTimestamp: true,
        Prefix:          "charm-app",
    })

    // Customize logger styles to match app theme
    styles := log.DefaultStyles()
    styles.Levels[log.InfoLevel] = lipgloss.NewStyle().
        Foreground(lipgloss.Color("86")).
        Bold(true)
    logger.SetStyles(styles)

    logger.Info("Application with Charm libraries", "components", []string{"lipgloss", "bubbles", "log"})

    // Use with other Charm components
    items := []list.Item{
        list.Item("Item 1"),
        list.Item("Item 2"),
    }

    logger.Debug("List created", "items_count", len(items))
    // Continue with Bubble Tea app...
}
```

## References

### Official Resources
- **GitHub Repository**: https://github.com/charmbracelet/log
- **API Documentation**: https://pkg.go.dev/github.com/charmbracelet/log
- **Charm Ecosystem**: https://charm.sh/

### Related Libraries
- **Lip Gloss**: Terminal styling (https://github.com/charmbracelet/lipgloss)
- **Bubble Tea**: TUI framework (https://github.com/charmbracelet/bubbletea)
- **Termenv**: Terminal environment detection (https://github.com/muesli/termenv)

### Standard Library Integration
- **log/slog**: Go's structured logging (https://pkg.go.dev/log/slog)
- **context**: Context passing (https://pkg.go.dev/context)

---

*This guide covers charmbracelet/log v0.x.x. For the latest features and updates, refer to the official documentation.*