# Charmbracelet Log Production Guide

## Production Configuration

### Environment-Based Setup

Configure logging based on environment variables for production deployment:

```go
package logging

import (
    "os"
    "strconv"
    "time"
    "github.com/charmbracelet/log"
)

type ProductionConfig struct {
    Level           log.Level
    Format          string
    ReportTimestamp bool
    ReportCaller    bool
    TimeFormat      string
    OutputFile      string
    MaxSize         int    // MB
    MaxBackups      int
    MaxAge          int    // days
    Compress        bool
}

func LoadProductionConfig() ProductionConfig {
    return ProductionConfig{
        Level:           parseLevel(getEnv("LOG_LEVEL", "info")),
        Format:          getEnv("LOG_FORMAT", "json"),
        ReportTimestamp: getEnvBool("LOG_TIMESTAMP", true),
        ReportCaller:    getEnvBool("LOG_CALLER", false), // Disabled in production
        TimeFormat:      getEnv("LOG_TIME_FORMAT", time.RFC3339),
        OutputFile:      getEnv("LOG_OUTPUT", "stdout"),
        MaxSize:         getEnvInt("LOG_MAX_SIZE", 100),
        MaxBackups:      getEnvInt("LOG_MAX_BACKUPS", 7),
        MaxAge:          getEnvInt("LOG_MAX_AGE", 30),
        Compress:        getEnvBool("LOG_COMPRESS", true),
    }
}

func SetupProductionLogger() zerolog.Logger {
    config := LoadProductionConfig()

    var output io.Writer
    switch config.OutputFile {
    case "stdout":
        output = os.Stdout
    case "stderr":
        output = os.Stderr
    default:
        output = createRotatingFile(config.OutputFile, config.MaxSize, config.MaxBackups, config.MaxAge, config.Compress)
    }

    // Choose formatter based on environment
    var formatter log.Formatter
    switch config.Format {
    case "json":
        formatter = log.JSONFormatter
    case "logfmt":
        formatter = log.LogfmtFormatter
    default:
        // Use plain text formatter for production (no colors)
        formatter = log.TextFormatter
    }

    logger := log.NewWithOptions(output, log.Options{
        Level:           config.Level,
        Formatter:       formatter,
        ReportTimestamp: config.ReportTimestamp,
        ReportCaller:    config.ReportCaller,
        Prefix:          getEnv("APP_NAME", "app"),
        TimeFormat:      config.TimeFormat,
        Fields: []any{
            "service", getEnv("SERVICE_NAME", "unknown"),
            "version", getEnv("SERVICE_VERSION", "unknown"),
            "environment", getEnv("ENVIRONMENT", "production"),
            "instance_id", getInstanceID(),
        },
    })

    return logger
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

func getEnvInt(key string, defaultValue int) int {
    if value := os.Getenv(key); value != "" {
        if parsed, err := strconv.Atoi(value); err == nil {
            return parsed
        }
    }
    return defaultValue
}
```

### Production Logger Factory

Create a robust logger factory for production environments:

```go
package logging

import (
    "io"
    "os"
    "compress/gzip"
    "gopkg.in/natefinch/lumberjack.v2"
)

type ProductionLoggerFactory struct {
    serviceName string
    version     string
    environment string
    instanceID  string
}

func NewProductionLoggerFactory(serviceName, version, environment string) *ProductionLoggerFactory {
    return &ProductionLoggerFactory{
        serviceName: serviceName,
        version:     version,
        environment: environment,
        instanceID:  getInstanceID(),
    }
}

func (plf *ProductionLoggerFactory) CreateLogger(config ProductionConfig) *log.Logger {
    var output io.Writer

    // Setup output destination
    switch config.OutputFile {
    case "stdout":
        output = os.Stdout
    case "stderr":
        output = os.Stderr
    default:
        output = plf.createRotatingFile(config)
    }

    // Apply compression if enabled for file output
    if config.Compress && config.OutputFile != "stdout" && config.OutputFile != "stderr" {
        output = &compressingWriter{wrapped: output}
    }

    // Create logger with production configuration
    logger := log.NewWithOptions(output, log.Options{
        Level:           config.Level,
        Formatter:       plf.getFormatter(config.Format),
        ReportTimestamp: config.ReportTimestamp,
        ReportCaller:    config.ReportCaller,
        TimeFormat:      config.TimeFormat,
        Prefix:          plf.serviceName,
    })

    // Add production fields
    logger = logger.With().
        Str("service", plf.serviceName).
        Str("version", plf.version).
        Str("environment", plf.environment).
        Str("instance_id", plf.instanceID).
        Str("hostname", getHostname()).
        Logger()

    return logger
}

func (plf *ProductionLoggerFactory) getFormatter(format string) log.Formatter {
    switch format {
    case "json":
        return log.JSONFormatter
    case "logfmt":
        return log.LogfmtFormatter
    default:
        return log.TextFormatter // Plain text for production
    }
}

func (plf *ProductionLoggerFactory) createRotatingFile(config ProductionConfig) io.Writer {
    return &lumberjack.Logger{
        Filename:   config.OutputFile,
        MaxSize:    config.MaxSize,    // MB
        MaxBackups: config.MaxBackups,
        MaxAge:     config.MaxAge,     // days
        Compress:   config.Compress,
        LocalTime:  true,
    }
}

// Custom writer for gzip compression
type compressingWriter struct {
    wrapped io.Writer
    gzipWriter *gzip.Writer
}

func (cw *compressingWriter) Write(p []byte) (int, error) {
    if cw.gzipWriter == nil {
        cw.gzipWriter = gzip.NewWriter(cw.wrapped)
    }
    return cw.gzipWriter.Write(p)
}

func (cw *compressingWriter) Close() error {
    if cw.gzipWriter != nil {
        return cw.gzipWriter.Close()
    }
    return nil
}

func getInstanceID() string {
    if instanceID := os.Getenv("INSTANCE_ID"); instanceID != "" {
        return instanceID
    }

    // Generate unique instance ID
    hostname, _ := os.Hostname()
    pid := os.Getpid()
    return fmt.Sprintf("%s-%d", hostname, pid)
}

func getHostname() string {
    if hostname, err := os.Hostname(); err == nil {
        return hostname
    }
    return "unknown"
}
```

## Log Rotation and Retention

### Lumberjack Integration

Use lumberjack for automatic log rotation in production:

```go
package logging

import (
    "os"
    "time"
    "gopkg.in/natefinch/lumberjack.v2"
)

func setupFileLogging(logFile string, maxSize, maxBackups, maxAge int) io.Writer {
    return &lumberjack.Logger{
        Filename:   logFile,
        MaxSize:    maxSize,    // MB
        MaxBackups: maxBackups,
        MaxAge:     maxAge,     // days
        Compress:   true,       // compress old logs
        LocalTime:  true,       // use local time for rotation
    }
}

func createProductionLogger(logFile string) *log.Logger {
    // Log rotation configuration
    maxSize := getEnvInt("LOG_MAX_SIZE", 100)    // 100MB
    maxBackups := getEnvInt("LOG_MAX_BACKUPS", 7) // Keep 7 backups
    maxAge := getEnvInt("LOG_MAX_AGE", 30)       // Keep for 30 days

    output := setupFileLogging(logFile, maxSize, maxBackups, maxAge)

    logger := log.NewWithOptions(output, log.Options{
        ReportTimestamp: true,
        TimeFormat:      time.RFC3339,
        Formatter:       log.JSONFormatter, // JSON for production
        Prefix:          "my-service",
        Level:           log.InfoLevel,
    })

    // Add production fields
    logger = logger.With().
        Str("service", "my-service").
        Str("version", os.Getenv("SERVICE_VERSION")).
        Str("environment", os.Getenv("ENVIRONMENT")).
        Logger()

    return logger
}
```

### Advanced Log Rotation

Implement more sophisticated log rotation strategies:

```go
package logging

import (
    "fmt"
    "os"
    "path/filepath"
    "time"
    "github.com/natefinch/lumberjack"
)

type AdvancedLogRotator struct {
    *lumberjack.Logger
    compress     bool
    maxAge       time.Duration
    rotateOnSize int64
    rotateOnTime time.Duration
    lastRotate   time.Time
    currentSize  int64
}

func NewAdvancedLogRotator(config LogRotationConfig) *AdvancedLogRotator {
    return &AdvancedLogRotator{
        Logger: &lumberjack.Logger{
            Filename:   config.Filename,
            MaxSize:    config.MaxSize,
            MaxBackups: config.MaxBackups,
            MaxAge:     config.MaxAge,
            Compress:   config.Compress,
            LocalTime:  true,
        },
        maxAge:       time.Duration(config.MaxAge) * 24 * time.Hour,
        rotateOnSize: int64(config.MaxSize) * 1024 * 1024,
        rotateOnTime: time.Hour, // Rotate every hour
        lastRotate:   time.Now(),
    }
}

type LogRotationConfig struct {
    Filename   string
    MaxSize    int  // MB
    MaxBackups int
    MaxAge     int  // days
    Compress   bool
}

func (alr *AdvancedLogRotator) Write(p []byte) (n int, err error) {
    n, err = alr.Logger.Write(p)
    alr.currentSize += int64(n)

    // Check if rotation is needed
    if alr.shouldRotate() {
        alr.rotate()
    }

    return n, err
}

func (alr *AdvancedLogRotator) shouldRotate() bool {
    // Rotate based on size
    if alr.currentSize >= alr.rotateOnSize {
        return true
    }

    // Rotate based on time
    if time.Since(alr.lastRotate) >= alr.rotateOnTime {
        return true
    }

    return false
}

func (alr *AdvancedLogRotator) rotate() {
    // Create backup with timestamp
    timestamp := time.Now().Format("20060102-150405")
    backupFile := fmt.Sprintf("%s.%s", alr.Filename, timestamp)

    // Rename current file
    if err := os.Rename(alr.Filename, backupFile); err != nil {
        return
    }

    // Compress if enabled
    if alr.compress {
        go alr.compressFile(backupFile)
    }

    // Reset counters
    alr.currentSize = 0
    alr.lastRotate = time.Now()
}

func (alr *AdvancedLogRotator) compressFile(filename string) {
    // Implement gzip compression
    // ...
}
```

## Structured Production Logging

### Standardized Log Format

Implement consistent log structure for production:

```go
package logging

import (
    "context"
    "time"
    "github.com/charmbracelet/log"
)

// Standardized log fields for production
const (
    FieldTimestamp    = "timestamp"
    FieldLevel        = "level"
    FieldService      = "service"
    FieldVersion      = "version"
    FieldEnvironment  = "environment"
    FieldInstanceID   = "instance_id"
    FieldHostname     = "hostname"
    FieldRequestID    = "request_id"
    FieldTraceID      = "trace_id"
    FieldSpanID       = "span_id"
    FieldUserID       = "user_id"
    FieldSessionID    = "session_id"
    FieldComponent    = "component"
    FieldOperation    = "operation"
    FieldDuration     = "duration_ms"
    FieldErrorCode    = "error_code"
    FieldErrorMessage = "error_message"
    FieldStatus       = "status"
    FieldStatusCode   = "status_code"
    FieldSource       = "source"
    FieldTarget       = "target"
)

// ProductionLogger provides standardized production logging
type ProductionLogger struct {
    *log.Logger
    serviceName string
    version     string
    environment string
}

func NewProductionLogger(base *log.Logger, serviceName, version, environment string) *ProductionLogger {
    // Add production fields
    logger := base.With().
        Str("service", serviceName).
        Str("version", version).
        Str("environment", environment).
        Str("hostname", getHostname()).
        Str("instance_id", getInstanceID()).
        Logger()

    return &ProductionLogger{
        Logger:      &logger,
        serviceName: serviceName,
        version:     version,
        environment: environment,
    }
}

func (pl *ProductionLogger) WithRequest(requestID, traceID, spanID string) *ProductionLogger {
    logger := pl.Logger.With().
        Str("request_id", requestID).
        Str("trace_id", traceID).
        Str("span_id", spanID).
        Logger()

    return &ProductionLogger{
        Logger:      &logger,
        serviceName: pl.serviceName,
        version:     pl.version,
        environment: pl.environment,
    }
}

func (pl *ProductionLogger) WithUser(userID, sessionID string) *ProductionLogger {
    logger := pl.Logger.With().
        Str("user_id", userID).
        Str("session_id", sessionID).
        Logger()

    return &ProductionLogger{
        Logger:      &logger,
        serviceName: pl.serviceName,
        version:     pl.version,
        environment: pl.environment,
    }
}

func (pl *ProductionLogger) LogHTTPRequest(method, path string, statusCode int, duration time.Duration, responseSize int64) {
    pl.Logger.Info().
        Str("operation", "http_request").
        Str("method", method).
        Str("path", path).
        Int("status_code", statusCode).
        Int64("duration_ms", duration.Milliseconds()).
        Int64("response_size", responseSize).
        Msg("HTTP request")
}

func (pl *ProductionLogger) LogError(operation string, err error, fields map[string]interface{}) {
    event := pl.Logger.Error().
        Str("operation", operation).
        Err(err)

    for k, v := range fields {
        event.Interface(k, v)
    }

    event.Msg("Operation failed")
}

func (pl *ProductionLogger) LogBusinessEvent(eventType string, fields map[string]interface{}) {
    event := pl.Logger.Info().
        Str("event_type", eventType).
        Str("category", "business")

    for k, v := range fields {
        event.Interface(k, v)
    }

    event.Msg("Business event")
}

func (pl *ProductionLogger) LogMetric(name string, value float64, tags map[string]string) {
    event := pl.Logger.Info().
        Str("metric_name", name).
        Float64("metric_value", value).
        Str("category", "metric")

    for k, v := range tags {
        event.Str("metric_tag_"+k, v)
    }

    event.Msg("Metric recorded")
}
```

### Context Integration for Production

Implement context-aware logging for distributed systems:

```go
package logging

import (
    "context"
    "github.com/charmbracelet/log"
)

type ContextKey string

const (
    LoggerContextKey ContextKey = "logger"
    RequestIDKey    ContextKey = "request_id"
    TraceIDKey      ContextKey = "trace_id"
    UserIDKey       ContextKey = "user_id"
)

func WithLogger(ctx context.Context, logger *ProductionLogger) context.Context {
    return context.WithValue(ctx, LoggerContextKey, logger)
}

func FromContext(ctx context.Context) *ProductionLogger {
    if logger, ok := ctx.Value(LoggerContextKey).(*ProductionLogger); ok {
        return logger
    }
    return DefaultProductionLogger
}

func WithRequestContext(ctx context.Context, requestID, traceID, spanID string) context.Context {
    logger := FromContext(ctx).WithRequest(requestID, traceID, spanID)
    ctx = WithLogger(ctx, logger)

    ctx = context.WithValue(ctx, RequestIDKey, requestID)
    ctx = context.WithValue(ctx, TraceIDKey, traceID)

    return ctx
}

func WithUserContext(ctx context.Context, userID, sessionID string) context.Context {
    logger := FromContext(ctx).WithUser(userID, sessionID)
    ctx = WithLogger(ctx, logger)

    ctx = context.WithValue(ctx, UserIDKey, userID)

    return ctx
}

// Middleware for HTTP services
func LoggingMiddleware(next http.Handler) http.Handler {
    return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        // Generate request context
        requestID := generateRequestID()
        traceID := getTraceID(r.Header)
        spanID := generateSpanID()

        ctx := WithRequestContext(r.Context(), requestID, traceID, spanID)

        // Add request information to context
        logger := FromContext(ctx).Logger.With().
            Str("method", r.Method).
            Str("path", r.URL.Path).
            Str("remote_addr", r.RemoteAddr).
            Str("user_agent", r.UserAgent()).
            Logger()

        ctx = WithLogger(ctx, &ProductionLogger{
            Logger:      &logger,
            serviceName: FromContext(ctx).serviceName,
            version:     FromContext(ctx).version,
            environment: FromContext(ctx).environment,
        })

        // Pass context to next handler
        next.ServeHTTP(w, r.WithContext(ctx))
    })
}

func getTraceID(headers http.Header) string {
    if traceID := headers.Get("X-Trace-ID"); traceID != "" {
        return traceID
    }
    if traceID := headers.Get("X-B3-TraceId"); traceID != "" {
        return traceID
    }
    return generateTraceID()
}
```

## Error Handling and Monitoring

### Production Error Classification

Implement structured error handling for production monitoring:

```go
package logging

import (
    "errors"
    "net/http"
    "github.com/charmbracelet/log"
)

// Error types for production monitoring
type ProductionErrorType string

const (
    ErrorTypeValidation   ProductionErrorType = "validation"
    ErrorTypeDatabase     ProductionErrorType = "database"
    ErrorTypeNetwork      ProductionErrorType = "network"
    ErrorTypeAuth         ProductionErrorType = "authentication"
    ErrorTypeAuthz        ProductionErrorType = "authorization"
    ErrorTypeBusiness     ProductionErrorType = "business"
    ErrorTypeSystem       ProductionErrorType = "system"
    ErrorTypeThirdParty   ProductionErrorType = "third_party"
    ErrorTypeRateLimit    ProductionErrorType = "rate_limit"
    ErrorTypeTimeout      ProductionErrorType = "timeout"
)

type ProductionError struct {
    Type        ProductionErrorType `json:"type"`
    Code        string             `json:"code"`
    Message     string             `json:"message"`
    Details     string             `json:"details,omitempty"`
    Retryable   bool               `json:"retryable"`
    HTTPStatus  int                `json:"http_status,omitempty"`
    Cause       error              `json:"-"`
    Severity    string             `json:"severity"`
    Component   string             `json:"component"`
    Operation   string             `json:"operation"`
    RequestID   string             `json:"request_id,omitempty"`
    UserID      string             `json:"user_id,omitempty"`
    Timestamp   int64              `json:"timestamp"`
    Alerting    bool               `json:"alerting"`
}

func (e ProductionError) Error() string {
    return e.Message
}

// Error builder for production
type ProductionErrorBuilder struct {
    error ProductionError
}

func NewProductionError(errType ProductionErrorType, code, message string) *ProductionErrorBuilder {
    return &ProductionErrorBuilder{
        error: ProductionError{
            Type:      errType,
            Code:      code,
            Message:   message,
            Timestamp: time.Now().Unix(),
            Severity:  "medium",
            Alerting:  false,
        },
    }
}

func (peb *ProductionErrorBuilder) Details(details string) *ProductionErrorBuilder {
    peb.error.Details = details
    return peb
}

func (peb *ProductionErrorBuilder) Retryable(retryable bool) *ProductionErrorBuilder {
    peb.error.Retryable = retryable
    return peb
}

func (peb *ProductionErrorBuilder) HTTPStatus(status int) *ProductionErrorBuilder {
    peb.error.HTTPStatus = status
    return peb
}

func (peb *ProductionErrorBuilder) Cause(err error) *ProductionErrorBuilder {
    peb.error.Cause = err
    return peb
}

func (peb *ProductionErrorBuilder) Severity(severity string) *ProductionErrorBuilder {
    peb.error.Severity = severity
    return peb
}

func (peb *ProductionErrorBuilder) Alerting(alerting bool) *ProductionErrorBuilder {
    peb.error.Alerting = alerting
    return peb
}

func (peb *ProductionErrorBuilder) Component(component string) *ProductionErrorBuilder {
    peb.error.Component = component
    return peb
}

func (peb *ProductionErrorBuilder) Operation(operation string) *ProductionErrorBuilder {
    peb.error.Operation = operation
    return peb
}

func (peb *ProductionErrorBuilder) Build() ProductionError {
    return peb.error
}

func (pl *ProductionLogger) LogProductionError(ctx context.Context, prodErr ProductionError) {
    // Add context fields if available
    event := pl.Logger.Error()

    // Add standard error fields
    event = event.Str("error_type", string(prodErr.Type)).
        Str("error_code", prodErr.Code).
        Str("error_message", prodErr.Message).
        Bool("retryable", prodErr.Retryable).
        Str("severity", prodErr.Severity).
        Str("component", prodErr.Component).
        Str("operation", prodErr.Operation).
        Int64("timestamp", prodErr.Timestamp).
        Bool("alerting", prodErr.Alerting)

    if prodErr.Details != "" {
        event = event.Str("error_details", prodErr.Details)
    }
    if prodErr.HTTPStatus > 0 {
        event = event.Int("http_status", prodErr.HTTPStatus)
    }
    if prodErr.Cause != nil {
        event = event.Err(prodErr.Cause)
    }

    // Add context fields
    if requestID := ctx.Value(RequestIDKey); requestID != nil {
        event = event.Str("request_id", requestID.(string))
    }
    if userID := ctx.Value(UserIDKey); userID != nil {
        event = event.Str("user_id", userID.(string))
    }

    // Choose log level based on severity
    switch prodErr.Severity {
    case "low":
        event.Msg("Low severity error occurred")
    case "medium":
        event.Msg("Medium severity error occurred")
    case "high", "critical":
        event.Str("alert", "oncall").Msg("High severity error occurred")
    }
}

// Example usage
func ExampleErrorHandling(pl *ProductionLogger, ctx context.Context) {
    // Create production error
    prodErr := NewProductionError(ErrorTypeDatabase, "DB_CONN_FAILED", "Database connection failed").
        Details("Unable to connect to PostgreSQL server").
        Retryable(true).
        HTTPStatus(503).
        Severity("high").
        Alerting(true).
        Component("database").
        Operation("connect").
        Build()

    // Log the error
    pl.LogProductionError(ctx, prodErr)
}
```

### Health Monitoring Integration

Include logging health in application monitoring:

```go
package health

import (
    "sync"
    "time"
    "github.com/charmbracelet/log"
)

type LoggingHealth struct {
    logger     *log.Logger
    healthy    bool
    lastCheck  time.Time
    error      error
    metrics    LoggingHealthMetrics
    mu         sync.RWMutex
}

type LoggingHealthMetrics struct {
    LogsWritten      int64
    ErrorsLogged     int64
    AverageLatency   time.Duration
    MaxLatency       time.Duration
    LastLogTime      time.Time
    LogRatePerSecond float64
}

func NewLoggingHealth(logger *log.Logger) *LoggingHealth {
    return &LoggingHealth{
        logger:  logger,
        healthy: true,
        metrics: LoggingHealthMetrics{
            LastLogTime: time.Now(),
        },
    }
}

func (lh *LoggingHealth) Check() {
    lh.mu.Lock()
    defer lh.mu.Unlock()

    lh.lastCheck = time.Now()

    // Test logging functionality
    testLogger := lh.logger.With().Str("health_check", "true").Logger()

    start := time.Now()
    testLogger.Debug().Msg("Health check log")
    duration := time.Since(start)

    // Update metrics
    lh.metrics.AverageLatency = time.Duration((int64(lh.metrics.AverageLatency) + int64(duration)) / 2)
    if duration > lh.metrics.MaxLatency {
        lh.metrics.MaxLatency = duration
    }

    // Check logging health
    if duration > time.Second {
        lh.healthy = false
        lh.error = fmt.Errorf("logging took too long: %v", duration)
        return
    }

    // Check log rate
    timeSinceLastLog := time.Since(lh.metrics.LastLogTime)
    if timeSinceLastLog > 5*time.Minute {
        lh.metrics.LogRatePerSecond = 0
        // Don't fail health check for low log rate in production
    }

    lh.healthy = true
    lh.error = nil
}

func (lh *LoggingHealth) RecordLog() {
    lh.mu.Lock()
    defer lh.mu.Unlock()

    now := time.Now()
    lh.metrics.LogsWritten++
    lh.metrics.LastLogTime = now

    // Calculate log rate
    timeSinceStart := now.Sub(lh.metrics.LastLogTime)
    if timeSinceStart > 0 {
        lh.metrics.LogRatePerSecond = float64(lh.metrics.LogsWritten) / timeSinceStart.Seconds()
    }
}

func (lh *LoggingHealth) RecordError() {
    lh.mu.Lock()
    defer lh.mu.Unlock()

    lh.metrics.ErrorsLogged++
}

func (lh *LoggingHealth) IsHealthy() bool {
    lh.mu.RLock()
    defer lh.mu.RUnlock()
    return lh.healthy
}

func (lh *LoggingHealth) GetError() error {
    lh.mu.RLock()
    defer lh.mu.RUnlock()
    return lh.error
}

func (lh *LoggingHealth) GetStatus() map[string]interface{} {
    lh.mu.RLock()
    defer lh.mu.RUnlock()

    return map[string]interface{}{
        "healthy":            lh.healthy,
        "last_check":         lh.lastCheck,
        "error":              lh.error,
        "logs_written":       lh.metrics.LogsWritten,
        "errors_logged":      lh.metrics.ErrorsLogged,
        "average_latency_ms": lh.metrics.AverageLatency.Milliseconds(),
        "max_latency_ms":     lh.metrics.MaxLatency.Milliseconds(),
        "log_rate_per_sec":   lh.metrics.LogRatePerSecond,
        "last_log_time":      lh.metrics.LastLogTime,
    }
}
```

## Security and Compliance

### Sensitive Data Filtering

Implement comprehensive sensitive data filtering for production:

```go
package security

import (
    "regexp"
    "strings"
    "github.com/charmbracelet/log"
)

// Comprehensive sensitive data patterns
var (
    // Email addresses
    emailPattern = regexp.MustCompile(`\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b`)

    // Passwords and secrets
    passwordPattern = regexp.MustCompile(`(?i)(password|passwd|pwd|secret|token|key|api_key)['"]?\s*[:=]\s*['"]?([^'"\s]{6,})['"]?`)

    // Credit cards
    creditCardPattern = regexp.MustCompile(`\b\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}\b`)

    // Social Security Numbers
    ssnPattern = regexp.MustCompile(`\b\d{3}-?\d{2}-?\d{4}\b`)

    // Phone numbers
    phonePattern = regexp.MustCompile(`\b\d{3}[-.\s]?\d{3}[-.\s]?\d{4}\b`)

    // IP addresses (optional - often needed for debugging)
    ipPattern = regexp.MustCompile(`\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b`)

    // JWT tokens
    jwtPattern = regexp.MustCompile(`eyJ[A-Za-z0-9_-]*\.eyJ[A-Za-z0-9_-]*\.[A-Za-z0-9_-]*`)
)

type SecureLogger struct {
    *log.Logger
    filterKeys map[string]bool
}

func NewSecureLogger(logger *log.Logger) *SecureLogger {
    return &SecureLogger{
        Logger: logger,
        filterKeys: map[string]bool{
            "password": true, "passwd": true, "pwd": true,
            "secret": true, "token": true, "key": true,
            "api_key": true, "apikey": true, "access_token": true,
            "refresh_token": true, "auth_token": true, "session_token": true,
            "csrf_token": true, "bearer_token": true,
            "credit_card": true, "cc_number": true, "ssn": true,
            "social_security_number": true, "phone": true, "email": true,
            "private_key": true, "certificate": true,
        },
    }
}

func (sl *SecureLogger) sanitizeMessage(message string) string {
    message = emailPattern.ReplaceAllString(message, "email@***.***")
    message = passwordPattern.ReplaceAllString(message, "$1=***")
    message = creditCardPattern.ReplaceAllString(message, "****-****-****-****")
    message = ssnPattern.ReplaceAllString(message, "***-**-****")
    message = phonePattern.ReplaceAllString(message, "***-***-****")
    message = jwtPattern.ReplaceAllString(message, "jwt.***.***")

    return message
}

func (sl *SecureLogger) sanitizeKey(key string) string {
    lowerKey := strings.ToLower(key)

    // Check exact matches
    if sl.filterKeys[lowerKey] {
        return key
    }

    // Check partial matches
    sensitiveSuffixes := []string{"_token", "_key", "_secret", "_password", "_hash"}
    for _, suffix := range sensitiveSuffixes {
        if strings.HasSuffix(lowerKey, suffix) {
            return key
        }
    }

    return key
}

func (sl *SecureLogger) sanitizeValue(key, value string) string {
    // Skip sanitization for keys that need to preserve data
    preserveKeys := map[string]bool{
        "ip_address": true, "client_ip": true, "user_agent": true,
        "request_id": true, "trace_id": true, "span_id": true,
    }

    if preserveKeys[strings.ToLower(key)] {
        return value
    }

    // If key is sensitive, mask the value
    if sl.filterKeys[strings.ToLower(key)] {
        return "***"
    }

    return sl.sanitizeMessage(value)
}

func (sl *SecureLogger) Info(msg string, keyvals ...interface{}) {
    // Sanitize the message
    sanitizedMsg := sl.sanitizeMessage(msg)

    // Sanitize key-value pairs
    sanitized := make([]interface{}, len(keyvals))
    for i := 0; i < len(keyvals); i += 2 {
        if i+1 < len(keyvals) {
            key, ok := keyvals[i].(string)
            if ok {
                sanitizedKey := sl.sanitizeKey(key)
                sanitized[i] = sanitizedKey

                value, ok := keyvals[i+1].(string)
                if ok {
                    sanitized[i+1] = sl.sanitizeValue(sanitizedKey, value)
                } else {
                    sanitized[i+1] = keyvals[i+1]
                }
            } else {
                sanitized[i] = keyvals[i]
                if i+1 < len(keyvals) {
                    sanitized[i+1] = keyvals[i+1]
                }
            }
        } else {
            sanitized[i] = keyvals[i]
        }
    }

    sl.Logger.Info(sanitizedMsg, sanitized...)
}

// Custom error that prevents sensitive data leakage
type SecureError struct {
    Code    string
    Message string
    Details string
}

func (se SecureError) Error() string {
    return se.Message
}

func (se SecureError) SanitizeForLogging() string {
    return fmt.Sprintf("SecureError{code:%s, message:%s}", se.Code, se.Message)
}
```

### Access Control for Logs

Implement proper access controls for log files:

```go
package security

import (
    "os"
    "syscall"
    "fmt"
)

func SecureLogFile(path string) error {
    // Set file permissions to read/write for owner and group only
    if err := os.Chmod(path, 0640); err != nil {
        return fmt.Errorf("failed to set file permissions: %w", err)
    }

    // Get file info to check ownership
    fileInfo, err := os.Stat(path)
    if err != nil {
        return fmt.Errorf("failed to get file info: %w", err)
    }

    stat, ok := fileInfo.Sys().(*syscall.Stat_t)
    if !ok {
        return fmt.Errorf("failed to get file stat")
    }

    // Check if file is owned by current user or service user
    expectedUID := uint32(os.Getuid())
    if stat.Uid != expectedUID {
        return fmt.Errorf("file is not owned by current user (UID %d)", expectedUID)
    }

    // Optionally check group ownership
    expectedGID := uint32(os.Getgid())
    if stat.Gid != expectedGID {
        // Set group ownership if needed
        if err := os.Chown(path, int(expectedUID), int(expectedGID)); err != nil {
            return fmt.Errorf("failed to set group ownership: %w", err)
        }
    }

    return nil
}

func SetupLogDirectory(logDir string) error {
    // Create log directory if it doesn't exist
    if err := os.MkdirAll(logDir, 0755); err != nil {
        return fmt.Errorf("failed to create log directory: %w", err)
    }

    // Set directory permissions
    if err := os.Chmod(logDir, 0755); err != nil {
        return fmt.Errorf("failed to set directory permissions: %w", err)
    }

    return nil
}
```

## Performance Monitoring

### Production Logging Metrics

Monitor logging performance in production:

```go
package monitoring

import (
    "sync/atomic"
    "time"
    "github.com/charmbracelet/log"
)

type ProductionLoggingMetrics struct {
    // Counters
    TotalLogs      int64
    ErrorLogs      int64
    WarnLogs       int64
    InfoLogs       int64
    DebugLogs      int64

    // Performance metrics
    TotalWriteTime time.Duration
    MaxWriteTime   time.Duration
    AverageWriteTime time.Duration

    // Size metrics
    TotalBytesWritten int64
    MaxLogSize        int64

    // Rate metrics
    LogsPerSecond     float64
    BytesPerSecond    float64

    // Error metrics
    WriteErrors       int64
    BufferOverflows   int64

    // Timestamps
    StartTime         time.Time
    LastLogTime       time.Time
    LastResetTime     time.Time
}

func (plm *ProductionLoggingMetrics) RecordLog(level log.Level, writeTime time.Duration, size int) {
    atomic.AddInt64(&plm.TotalLogs, 1)
    atomic.AddInt64((*int64)(&plm.TotalWriteTime), int64(writeTime))
    atomic.AddInt64(&plm.TotalBytesWritten, int64(size))

    now := time.Now()
    atomic.StoreInt64((*int64)(&plm.LastLogTime), now.UnixNano())

    // Update maximums
    updateMaxInt64(&plm.MaxWriteTime, int64(writeTime))
    updateMaxInt64(&plm.MaxLogSize, int64(size))

    // Level-specific counters
    switch level {
    case log.ErrorLevel:
        atomic.AddInt64(&plm.ErrorLogs, 1)
    case log.WarnLevel:
        atomic.AddInt64(&plm.WarnLogs, 1)
    case log.InfoLevel:
        atomic.AddInt64(&plm.InfoLogs, 1)
    case log.DebugLevel:
        atomic.AddInt64(&plm.DebugLogs, 1)
    }

    // Calculate averages and rates
    plm.calculateRates()
}

func updateMaxInt64(current *int64, value int64) {
    for {
        old := atomic.LoadInt64(current)
        if value <= old {
            break
        }
        if atomic.CompareAndSwapInt64(current, old, value) {
            break
        }
    }
}

func (plm *ProductionLoggingMetrics) calculateRates() {
    totalLogs := atomic.LoadInt64(&plm.TotalLogs)
    totalBytes := atomic.LoadInt64(&plm.TotalBytesWritten)
    totalWriteTime := atomic.LoadInt64(&plm.TotalWriteTime)

    if totalLogs > 0 {
        atomic.StoreInt64((*int64)(&plm.AverageWriteTime), totalWriteTime/totalLogs)
    }

    // Calculate rates per second
    now := time.Now()
    elapsed := now.Sub(plm.StartTime).Seconds()
    if elapsed > 0 {
        atomic.StoreInt64((*int64)(&plm.LogsPerSecond), int64(float64(totalLogs)/elapsed))
        atomic.StoreInt64((*int64)(&plm.BytesPerSecond), int64(float64(totalBytes)/elapsed))
    }
}

func (plm *ProductionLoggingMetrics) Reset() {
    atomic.StoreInt64(&plm.TotalLogs, 0)
    atomic.StoreInt64(&plm.ErrorLogs, 0)
    atomic.StoreInt64(&plm.WarnLogs, 0)
    atomic.StoreInt64(&plm.InfoLogs, 0)
    atomic.StoreInt64(&plm.DebugLogs, 0)
    atomic.StoreInt64(&plm.TotalWriteTime, 0)
    atomic.StoreInt64(&plm.MaxWriteTime, 0)
    atomic.StoreInt64(&plm.TotalBytesWritten, 0)
    atomic.StoreInt64(&plm.MaxLogSize, 0)
    atomic.StoreInt64(&plm.LogsPerSecond, 0)
    atomic.StoreInt64(&plm.BytesPerSecond, 0)
    atomic.StoreInt64(&plm.WriteErrors, 0)
    atomic.StoreInt64(&plm.BufferOverflows, 0)
    atomic.StoreInt64((*int64)(&plm.LastResetTime), time.Now().UnixNano())
}

func (plm *ProductionLoggingMetrics) GetSnapshot() map[string]interface{} {
    return map[string]interface{}{
        "total_logs":         atomic.LoadInt64(&plm.TotalLogs),
        "error_logs":         atomic.LoadInt64(&plm.ErrorLogs),
        "warn_logs":          atomic.LoadInt64(&plm.WarnLogs),
        "info_logs":          atomic.LoadInt64(&plm.InfoLogs),
        "debug_logs":         atomic.LoadInt64(&plm.DebugLogs),
        "total_write_time_ms": atomic.LoadInt64(&plm.TotalWriteTime) / 1e6,
        "max_write_time_ms":   atomic.LoadInt64(&plm.MaxWriteTime) / 1e6,
        "avg_write_time_ms":   atomic.LoadInt64(&plm.AverageWriteTime) / 1e6,
        "total_bytes_written": atomic.LoadInt64(&plm.TotalBytesWritten),
        "max_log_size":        atomic.LoadInt64(&plm.MaxLogSize),
        "logs_per_second":     atomic.LoadInt64(&plm.LogsPerSecond),
        "bytes_per_second":    atomic.LoadInt64(&plm.BytesPerSecond),
        "write_errors":        atomic.LoadInt64(&plm.WriteErrors),
        "buffer_overflows":    atomic.LoadInt64(&plm.BufferOverflows),
        "uptime_seconds":      time.Since(plm.StartTime).Seconds(),
        "last_log_time":       time.Unix(0, atomic.LoadInt64(&plm.LastLogTime)),
        "last_reset_time":     time.Unix(0, atomic.LoadInt64(&plm.LastResetTime)),
    }
}

// Metrics hook for production
type ProductionMetricsHook struct {
    metrics *ProductionLoggingMetrics
}

func NewProductionMetricsHook(metrics *ProductionLoggingMetrics) *ProductionMetricsHook {
    return &ProductionMetricsHook{metrics: metrics}
}

func (pmh *ProductionMetricsHook) Run(e *log.Event, level log.Level, message string) {
    start := time.Now()

    // This hook runs before the actual write
    // We'll capture timing and size in a post-write mechanism
    go func() {
        writeTime := time.Since(start)
        size := len(message) // Approximate size
        pmh.metrics.RecordLog(level, writeTime, size)
    }()
}
```

## Production Deployment Checklist

### Environment Variables Required

```bash
# Basic logging configuration
LOG_LEVEL=info                    # debug, info, warn, error
LOG_FORMAT=json                  # json, logfmt, or text
LOG_OUTPUT=/var/log/app/app.log  # stdout, stderr, or file path
LOG_TIMESTAMP=true
LOG_CALLER=false                 # Disabled in production for performance

# Log rotation
LOG_MAX_SIZE=100                 # MB
LOG_MAX_BACKUPS=7                 # Number of backup files
LOG_MAX_AGE=30                    # Days to retain logs
LOG_COMPRESS=true

# Application context
SERVICE_NAME=my-service
SERVICE_VERSION=1.0.0
ENVIRONMENT=production
INSTANCE_ID=i-1234567890abcdef0

# Security
LOG_FILE_PERMISSIONS=640         # File permissions for log files
LOG_ENCRYPTION=false             # Enable log encryption if needed
LOG_MASK_SECRETS=true            # Mask sensitive data
```

### Deployment Verification

Before deploying to production, verify:

```go
package verification

import (
    "testing"
    "time"
    "github.com/charmbracelet/log"
)

func TestProductionLoggingSetup(t *testing.T) {
    // Test logger creation
    logger := SetupProductionLogger()
    if logger == nil {
        t.Fatal("Failed to create production logger")
    }

    // Test basic logging
    start := time.Now()
    logger.Info("Test message", "test", true)
    duration := time.Since(start)

    // Verify logging performance
    if duration > 100*time.Millisecond {
        t.Errorf("Logging took too long: %v", duration)
    }

    // Test error logging
    err := errors.New("test error")
    logger.Error("Test error", "error", err)

    // Test structured logging
    logger.Info("Structured test",
        "string", "value",
        "number", 42,
        "boolean", true,
    )
}

func TestSecurityFiltering(t *testing.T) {
    secureLogger := NewSecureLogger(log.Default())

    // Test email filtering
    secureLogger.Info("User login",
        "email", "user@example.com",
        "user_id", "12345",
    )

    // Test password filtering
    secureLogger.Info("Authentication",
        "password", "secret123",
        "result", "success",
    )

    // Verify no sensitive data in logs (would need log capture mechanism)
}

func TestPerformanceUnderLoad(t *testing.T) {
    logger := SetupProductionLogger()
    numGoroutines := 10
    logsPerGoroutine := 1000

    start := time.Now()

    var wg sync.WaitGroup
    for i := 0; i < numGoroutines; i++ {
        wg.Add(1)
        go func(id int) {
            defer wg.Done()

            for j := 0; j < logsPerGoroutine; j++ {
                logger.Info("Load test",
                    "goroutine", id,
                    "iteration", j,
                    "data", "test-data-xyz",
                )
            }
        }(i)
    }

    wg.Wait()
    duration := time.Since(start)

    totalLogs := numGoroutines * logsPerGoroutine
    logsPerSecond := float64(totalLogs) / duration.Seconds()

    t.Logf("Logged %d messages in %v (%.2f logs/sec)", totalLogs, duration, logsPerSecond)

    // Verify performance meets requirements
    if logsPerSecond < 1000 {
        t.Errorf("Logging performance below threshold: %.2f logs/sec", logsPerSecond)
    }
}
```

This comprehensive production guide ensures that Charmbracelet Log is properly configured for production environments with appropriate security, monitoring, performance considerations, and operational best practices.