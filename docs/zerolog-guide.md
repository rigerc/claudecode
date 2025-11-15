# Zerolog: Zero Allocation JSON Logger - Complete Guide

## Overview

**Zerolog** is a high-performance, zero-allocation JSON logging library for Go that prioritizes speed and efficiency while maintaining a clean, developer-friendly API. Inspired by Uber's zap library but with enhanced simplicity, zerolog achieves exceptional performance by writing log events directly to JSON format without memory allocations or reflection.

### Key Features
- **Zero Allocations**: Minimal memory overhead through direct JSON writing
- **Structured Logging**: Native JSON output with strongly-typed fields
- **High Performance**: Optimized for high-throughput production systems
- **Developer Experience**: Clean chaining API with contextual logging
- **Context Integration**: Seamless integration with Go's `context.Context`
- **HTTP Middleware**: Built-in support for web applications via `hlog` package

## Installation

```bash
go get -u github.com/rs/zerolog/log
```

## Quick Start

```go
package main

import (
    "os"
    "github.com/rs/zerolog"
    "github.com/rs/zerolog/log"
)

func main() {
    // Configure global logger
    log.Logger = zerolog.New(os.Stderr).With().Timestamp().Logger()

    // Basic logging
    log.Info().Msg("Hello, World!")
    // Output: {"level":"info","time":1494567715,"message":"Hello, World!"}

    // Structured logging with fields
    log.Info().
        Str("user", "alice").
        Int("age", 30).
        Msg("User logged in")
    // Output: {"level":"info","user":"alice","age":30,"time":1494567715,"message":"User logged in"}
}
```

## Core Concepts

### Logger Creation

Zerolog provides multiple ways to create and configure loggers:

```go
// Basic logger with console output
logger := zerolog.New(os.Stdout)

// Logger with timestamp
logger := zerolog.New(os.Stdout).With().Timestamp().Logger()

// Logger with multiple context fields
logger := zerolog.New(os.Stdout).With().
    Str("service", "api-gateway").
    Str("version", "1.0.0").
    Int("port", 8080).
    Logger()

// Using the global logger convenience
log.Logger = logger
```

### Log Levels

Zerolog supports standard log levels with configurable filtering:

```go
// Set global log level
zerolog.SetGlobalLevel(zerolog.InfoLevel)

// Available levels (in order of severity)
// zerolog.TraceLevel - Most detailed
// zerolog.DebugLevel - Debugging information
// zerolog.InfoLevel  - General information
// zerolog.WarnLevel  - Warning conditions
// zerolog.ErrorLevel - Error conditions
// zerolog.FatalLevel - Fatal errors (calls os.Exit)
// zerolog.PanicLevel - Panic conditions
// zerolog.NoLevel    - No level specified
// zerolog.Disabled   - Logging disabled

// Level-specific logging
log.Trace().Msg("Detailed trace information")
log.Debug().Msg("Debug details")
log.Info().Msg("General information")
log.Warn().Msg("Warning condition")
log.Error().Msg("Error occurred")
log.Fatal().Msg("Fatal error - application exits")
```

### Field Types

Zerolog provides strongly-typed methods for various data types:

```go
// String fields
log.Info().Str("name", "alice").Msg("User action")

// Numeric fields
log.Info().
    Int("count", 42).
    Int8("small", 127).
    Int16("medium", 32767).
    Int32("large", 2147483647).
    Int64("very_large", 9223372036854775807).
    Uint("unsigned", 42).
    Float32("price_f32", 99.99).
    Float64("price_f64", 123.456).
    Msg("Numeric examples")

// Boolean and time fields
log.Info().
    Bool("active", true).
    Time("created", time.Now()).
    Dur("duration", 250*time.Millisecond).
    Msg("Status update")

// Array and object fields
log.Info().
    Array("tags", zerolog.Arr().Str("urgent").Str("billing")).
    Dict("metadata", zerolog.Dict().
        Str("source", "api").
        Int("version", 2),
    ).
    Msg("Complex data")
```

## Advanced Features

### Sub-Loggers and Context

Create child loggers that inherit parent context while adding specific fields:

```go
// Parent logger with base context
parentLogger := zerolog.New(os.Stdout).With().
    Str("service", "api-gateway").
    Str("environment", "production").
    Logger()

// Sub-logger for authentication component
authLogger := parentLogger.With().
    Str("component", "auth").
    Str("module", "jwt").
    Logger()

authLogger.Info().Str("user_id", "12345").Msg("Token validated")
// Output: {"service":"api-gateway","environment":"production","component":"auth","module":"jwt","user_id":"12345","time":1494567715,"level":"info","message":"Token validated"}
```

### Custom Object Marshaling

Implement `LogObjectMarshaler` for zero-allocation custom object logging:

```go
type User struct {
    Name    string    `json:"name"`
    Email   string    `json:"email"`
    Age     int       `json:"age"`
    Created time.Time `json:"created"`
}

// Implement for zero-allocation marshaling
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

// Usage
user := User{
    Name:    "Bob",
    Email:   "bob@example.com",
    Age:     25,
    Created: time.Now(),
}

log.Info().Object("user", user).Msg("User registered")
```

### Error Handling and Stack Traces

Comprehensive error logging with optional stack traces:

```go
import (
    "github.com/pkg/errors"
    "github.com/rs/zerolog/pkgerrors"
)

// Enable stack trace marshaling
zerolog.ErrorStackMarshaler = pkgerrors.MarshalStack

// Basic error logging
err := errors.New("database connection failed")
log.Error().Err(err).Str("database", "postgres").Msg("Connection error")

// Error with stack trace
err = processRequest()
log.Error().Stack().Err(err).Msg("Request processing failed")

// Multiple errors
errs := []error{
    errors.New("connection timeout"),
    errors.New("max retries exceeded"),
}
log.Error().Errs("failures", errs).Msg("Multiple errors occurred")
```

### Console Writer for Development

Human-readable console output with colors and formatting:

```go
// Simple console writer
logger := zerolog.New(zerolog.ConsoleWriter{Out: os.Stderr})

// Customized console writer
consoleWriter := zerolog.ConsoleWriter{
    Out:        os.Stdout,
    TimeFormat: time.RFC3339,
    NoColor:    false, // Enable colors
}

// Custom field formatting
consoleWriter.FormatLevel = func(i interface{}) string {
    return fmt.Sprintf("| %-6s|", i)
}
consoleWriter.FormatMessage = func(i interface{}) string {
    return fmt.Sprintf("***%s***", i)
}

logger := zerolog.New(consoleWriter).With().Timestamp().Logger()
logger.Info().Str("status", "ok").Msg("Custom format")
// Output: 2023-01-15T10:30:00Z | INFO  | ***Custom format*** status:ok
```

### Log Sampling

Reduce log volume in high-throughput systems:

```go
// Basic sampling - log every 10th event
sampledLogger := logger.Sample(&zerolog.BasicSampler{N: 10})

// Random sampling - approximately 1 in 100 events
randomSampled := logger.Sample(zerolog.RandomSampler(100))

// Burst sampler - allow 5 messages per second, then sample 1 in 100
burstSampled := logger.Sample(&zerolog.BurstSampler{
    Burst:       5,
    Period:      1 * time.Second,
    NextSampler: &zerolog.BasicSampler{N: 100},
})

// Pre-configured samplers
oftenSampled := logger.Sample(zerolog.Often)      // ~1 in 10
sometimesSampled := logger.Sample(zerolog.Sometimes) // ~1 in 100
rarelySampled := logger.Sample(zerolog.Rarely)    // ~1 in 1000
```

### Hooks for Custom Processing

Implement hooks to add dynamic fields or process events:

```go
// Custom hook implementation
type SeverityHook struct{}

func (h SeverityHook) Run(e *zerolog.Event, level zerolog.Level, msg string) {
    if level != zerolog.NoLevel {
        e.Str("severity", level.String())
    }
}

// Hook function using HookFunc adapter
var messageCounterHook = zerolog.HookFunc(func(e *zerolog.Event, level zerolog.Level, message string) {
    e.Int("message_length", len(message))
})

// Apply hooks
logger := zerolog.New(os.Stdout).
    Hook(SeverityHook{}).
    Hook(messageCounterHook)

logger.Info().Msg("This will have additional fields")
```

### Context Integration

Seamless integration with Go's context for request-scoped logging:

```go
import "github.com/rs/zerolog/log"

// Store logger in context
ctx := context.Background()
ctx = logger.WithContext(ctx)

// Retrieve logger from context anywhere
func handleRequest(ctx context.Context) {
    logger := zerolog.Ctx(ctx)
    logger.Info().Str("handler", "main").Msg("Handling request")
}

// Using global logger with context
log.Info().Ctx(ctx).Msg("Processing with trace context")
```

### HTTP Middleware (hlog)

Built-in middleware for web applications:

```go
import (
    "net/http"
    "github.com/rs/zerolog/hlog"
)

// Create HTTP handler with logging
func setupHTTPHandler() http.Handler {
    logger := zerolog.New(os.Stdout).With().Timestamp().Logger()
    mux := http.NewServeMux()

    // Add your handlers
    mux.HandleFunc("/api/users", handleUsers)

    // Wrap with hlog middleware
    handler := hlog.NewHandler(logger)(mux)
    handler = hlog.RequestIDHandler("request_id", "X-Request-ID")(handler)
    handler = hlog.AccessHandler(func(r *http.Request, status, size int, duration time.Duration) {
        hlog.FromRequest(r).Info().
            Str("method", r.Method).
            Stringer("url", r.URL).
            Int("status", status).
            Int("size", size).
            Dur("duration", duration).
            Msg("Request completed")
    })(handler)

    return handler
}

func handleUsers(w http.ResponseWriter, r *http.Request) {
    // Get logger from request context
    logger := hlog.FromRequest(r)
    logger.Info().Str("endpoint", "/api/users").Msg("Fetching users")
}
```

### Network and Advanced Field Types

Specialized support for network-related data:

```go
import "net"

// IP addresses
ipv4 := net.ParseIP("192.168.1.100")
ipv6 := net.ParseIP("2001:0db8::1")
log.Info().
    IPAddr("client_ipv4", ipv4).
    IPAddr("client_ipv6", ipv6).
    Msg("Connection established")

// IP prefix (CIDR)
_, network, _ := net.ParseCIDR("10.0.0.0/8")
log.Info().IPPrefix("network", *network).Msg("Routing update")

// MAC addresses
mac, _ := net.ParseMAC("00:1B:44:11:3A:B7")
log.Info().MACAddr("device_mac", mac).Msg("Device registered")

// Raw JSON embedding
rawJSON := []byte(`{"custom":"data","nested":{"key":"value"}}`)
log.Info().RawJSON("metadata", rawJSON).Msg("With raw JSON")

// Binary data (hex encoded)
binaryData := []byte{0xDE, 0xAD, 0xBE, 0xEF}
log.Info().Hex("signature", binaryData).Msg("Data packet received")
```

## Configuration

### Global Settings

Configure global behavior:

```go
// Customize field names
zerolog.TimestampFieldName = "ts"
zerolog.LevelFieldName = "severity"
zerolog.MessageFieldName = "msg"
zerolog.ErrorFieldName = "err"
zerolog.CallerFieldName = "caller"

// Time format
zerolog.TimeFieldFormat = zerolog.TimeFormatUnix // Unix timestamp
// Other options: TimeFormatUnixMs, TimeFormatUnixMicro, time.RFC3339

// Duration formatting
zerolog.DurationFieldUnit = time.Second
zerolog.DurationFieldInteger = true // Use integers

// Set global log level
zerolog.SetGlobalLevel(zerolog.InfoLevel)

// Configure caller skip frames
zerolog.CallerSkipFrameCount = 2

// Set floating point precision
zerolog.FloatingPointPrecision = 2
```

### Multiple Output Destinations

Write to multiple destinations simultaneously:

```go
// Multi-writer for console and file
consoleWriter := zerolog.ConsoleWriter{Out: os.Stderr}
fileWriter, _ := os.OpenFile("app.log", os.O_CREATE|os.O_APPEND|os.O_WRONLY, 0644)

multiWriter := zerolog.MultiLevelWriter(consoleWriter, fileWriter)
logger := zerolog.New(multiWriter).With().Timestamp().Logger()

logger.Info().Msg("Logged to both console and file")
```

## Performance Considerations

### Zero Allocation Design

Zerolog achieves zero allocations through:

- **Direct JSON Writing**: No intermediate string building
- **Typed Field Methods**: Avoid interface{} boxing
- **Stack-based Context**: No heap allocation for fields
- **Pre-calculated Field Names**: Constants for JSON keys

### Best Practices for Maximum Performance

```go
// ✅ Good: Use typed field methods
log.Info().Str("user", "alice").Int("count", 42).Msg("Action completed")

// ❌ Avoid: Interface{} usage (causes reflection)
log.Info().Interface("data", map[string]interface{}{"user": "alice"}).Msg("Slower")

// ✅ Good: Conditional expensive computation
if e := log.Debug(); e.Enabled() {
    expensiveValue := computeExpensiveMetric()
    e.Str("metric", expensiveValue).Msg("Computed metric")
}

// ✅ Good: Reuse loggers
userLogger := log.With().Str("component", "user-service").Logger()
userLogger.Info().Msg("Reusable sub-logger")

// ✅ Good: Use sampling for high-volume logs
highVolumeLogger := log.Sample(&zerolog.BasicSampler{N: 100})
```

### Performance Benchmarks

Based on typical benchmarks (operations per second):
- **Zerolog**: ~10M+ ops/sec (zero allocation)
- **Zap**: ~8M ops/sec (some allocation)
- **Logrus**: ~1M ops/sec (high allocation)
- **Standard log**: ~500K ops/sec (formatting overhead)

## Production Integration

### Structured Logging Pipeline

```go
// Production-ready logger setup
func setupProductionLogger() zerolog.Logger {
    // File writer for persistent storage
    fileWriter, err := os.OpenFile(
        "/var/log/app/app.log",
        os.O_CREATE|os.O_APPEND|os.O_WRONLY,
        0644,
    )
    if err != nil {
        panic(err)
    }

    // Multi-writer: file + stderr for critical errors
    multiWriter := zerolog.MultiLevelWriter(
        fileWriter,
        zerolog.LevelWriterAdapter{Writer: os.Stderr, Level: zerolog.ErrorLevel},
    )

    return zerolog.New(multiWriter).
        With().
        Timestamp().
        Str("service", "my-service").
        Str("version", os.Getenv("APP_VERSION")).
        Str("instance_id", getInstanceID()).
        Logger()
}
```

### Distributed Tracing Integration

```go
// Tracing-aware logger
type TracingHook struct{}

func (h TracingHook) Run(e *zerolog.Event, level zerolog.Level, msg string) {
    ctx := e.GetCtx()
    if ctx == nil {
        return
    }

    // Extract tracing information
    if traceID := extractTraceID(ctx); traceID != "" {
        e.Str("trace_id", traceID)
    }
    if spanID := extractSpanID(ctx); spanID != "" {
        e.Str("span_id", spanID)
    }
}

// Usage with OpenTelemetry
logger := zerolog.New(os.Stdout).Hook(TracingHook{})
```

### Environment-Based Configuration

```go
// Environment-aware logger configuration
func initLogger() zerolog.Logger {
    var output io.Writer = os.Stdout

    // Environment-specific configuration
    switch os.Getenv("GO_ENV") {
    case "production":
        output = zerolog.MultiLevelWriter(
            os.Stdout,
            getFileWriter("/var/log/app/production.log"),
        )
        zerolog.SetGlobalLevel(zerolog.InfoLevel)
    case "development":
        output = zerolog.ConsoleWriter{Out: os.Stdout}
        zerolog.SetGlobalLevel(zerolog.DebugLevel)
    default:
        output = zerolog.ConsoleWriter{Out: os.Stdout}
        zerolog.SetGlobalLevel(zerolog.TraceLevel)
    }

    return zerolog.New(output).With().Timestamp().Logger()
}
```

## Troubleshooting

### Common Issues

**1. Logs not appearing**
```go
// Check global log level
currentLevel := zerolog.GlobalLevel()
if currentLevel > zerolog.InfoLevel {
    zerolog.SetGlobalLevel(zerolog.InfoLevel)
}

// Verify logger is not disabled
if logger.GetLevel() == zerolog.Disabled {
    logger = logger.Level(zerolog.InfoLevel)
}
```

**2. Missing timestamps**
```go
// Ensure timestamp field is configured
logger := zerolog.New(os.Stdout).With().Timestamp().Logger()

// Or set global time field format
zerolog.TimeFieldFormat = time.RFC3339
```

**3. Poor performance**
```go
// Avoid interface{} usage
// ❌ Slow
log.Info().Interface("data", complexStruct).Msg("Slow")

// ✅ Fast - implement MarshalZerologObject
log.Info().Object("data", complexStruct).Msg("Fast")

// Use sampling for high-volume logs
logger := log.Sample(&zerolog.BasicSampler{N: 10})
```

**4. Memory leaks**
```go
// Reuse loggers instead of creating new ones
// ❌ Creates new logger each time
func logRequest() {
    logger := zerolog.New(os.Stdout).With().Str("request", "123").Logger()
    logger.Info().Msg("Request processed")
}

// ✅ Reuse logger with context
var requestLogger = log.With().Str("component", "requests").Logger()
func logRequest() {
    requestLogger.Info().Str("request_id", "123").Msg("Request processed")
}
```

### Debug Mode

Enable detailed debugging:

```go
// Enable caller information
logger := zerolog.New(os.Stdout).With().Timestamp().Caller().Logger()

// Set to lowest level for debugging
zerolog.SetGlobalLevel(zerolog.TraceLevel)

// Enable debug output
zerolog.DisableSampling(true)
```

## Migration Guide

### From Standard Log

```go
// Before (standard log)
log.Printf("User %s logged in from %s", username, ip)

// After (zerolog)
log.Info().
    Str("user", username).
    Str("ip", ip).
    Msg("User logged in")
```

### From Logrus

```go
// Before (logrus)
log.WithFields(logrus.Fields{
    "user":  username,
    "count": count,
}).Info("Action completed")

// After (zerolog)
log.Info().
    Str("user", username).
    Int("count", count).
    Msg("Action completed")
```

### From Zap

```go
// Before (zap)
logger.Info("User action",
    zap.String("user", username),
    zap.Int("count", count),
)

// After (zerolog)
log.Info().
    Str("user", username).
    Int("count", count).
    Msg("User action")
```

## Integrations

### Popular Frameworks

**Gin Framework:**
```go
import "github.com/gin-gonic/gin"

func ginLogger() gin.HandlerFunc {
    return func(c *gin.Context) {
        start := time.Now()
        path := c.Request.URL.Path
        raw := c.Request.URL.RawQuery

        // Process request
        c.Next()

        // Log request
        latency := time.Since(start)
        clientIP := c.ClientIP()
        statusCode := c.Writer.Status()

        if raw != "" {
            path = path + "?" + raw
        }

        log.Info().
            Str("method", c.Request.Method).
            Str("path", path).
            Int("status", statusCode).
            Str("ip", clientIP).
            Dur("latency", latency).
            Msg("HTTP Request")
    }
}
```

**Echo Framework:**
```go
import "github.com/labstack/echo/v4"

func echoLogger() echo.MiddlewareFunc {
    return func(next echo.HandlerFunc) echo.HandlerFunc {
        return func(c echo.Context) error {
            req := c.Request()
            res := c.Response()

            start := time.Now()

            if err := next(c); err != nil {
                c.Error(err)
            }

            latency := time.Since(start)

            log.Info().
                Str("method", req.Method).
                Str("uri", req.RequestURI).
                Int("status", res.Status).
                Dur("latency", latency).
                Msg("Echo Request")

            return nil
        }
    }
}
```

### Observability Platforms

**ELK Stack Integration:**
```go
// Configure for Elasticsearch ingestion
logger := zerolog.New(os.Stdout).
    With().
    Timestamp().
    Str("service", "my-service").
    Str("environment", os.Getenv("ENVIRONMENT")).
    Str("version", os.Getenv("APP_VERSION")).
    Logger()
```

**Datadog Integration:**
```go
// Add Datadog-specific fields
logger := zerolog.New(os.Stdout).
    With().
    Timestamp().
    Str("dd.service", "my-service").
    Str("dd.env", os.Getenv("ENVIRONMENT")).
    Str("dd.version", os.Getenv("APP_VERSION")).
    Logger()
```

## Advanced Patterns

### Request-Scoped Logging

```go
type RequestContext struct {
    RequestID string
    UserID    string
    TraceID   string
}

func (rc RequestContext) ToLogger(logger zerolog.Logger) zerolog.Logger {
    return logger.With().
        Str("request_id", rc.RequestID).
        Str("user_id", rc.UserID).
        Str("trace_id", rc.TraceID).
        Logger()
}

// Usage in HTTP handlers
func handleRequest(w http.ResponseWriter, r *http.Request) {
    ctx := r.Context()
    reqCtx := GetRequestContext(ctx)

    logger := reqCtx.ToLogger(log.Logger)
    logger.Info().Msg("Processing request")
}
```

### Component-Based Logging

```go
// Create logger factory for components
type LoggerFactory struct {
    base zerolog.Logger
}

func NewLoggerFactory(base zerolog.Logger) *LoggerFactory {
    return &LoggerFactory{base: base}
}

func (lf *LoggerFactory) ForComponent(name string) zerolog.Logger {
    return lf.base.With().Str("component", name).Logger()
}

// Usage
factory := NewLoggerFactory(log.Logger)
dbLogger := factory.ForComponent("database")
authLogger := factory.ForComponent("authentication")
```

### Conditional Logging with Feature Flags

```go
type FeatureFlags struct {
    DetailedLogging bool
    DebugMode      bool
}

func (ff FeatureFlags) ConfigureLogger(base zerolog.Logger) zerolog.Logger {
    logger := base

    if ff.DetailedLogging {
        logger = logger.With().Str("mode", "detailed").Logger()
    }

    if ff.DebugMode {
        zerolog.SetGlobalLevel(zerolog.DebugLevel)
    } else {
        zerolog.SetGlobalLevel(zerolog.InfoLevel)
    }

    return logger
}
```

## References

### Official Resources
- **GitHub Repository**: https://github.com/rs/zerolog
- **API Documentation**: https://pkg.go.dev/github.com/rs/zerolog
- **Performance Benchmarks**: Available in repository README

### Related Packages
- **hlog**: HTTP middleware (`github.com/rs/zerolog/hlog`)
- **pkgerrors**: Error stack trace integration (`github.com/rs/zerolog/pkgerrors`)

### Community
- **Issues and Discussions**: GitHub repository issues
- **Examples**: Repository examples directory
- **Contributing**: Repository contribution guidelines

---

*This guide covers zerolog v1.x.x. For the latest features and updates, refer to the official documentation.*