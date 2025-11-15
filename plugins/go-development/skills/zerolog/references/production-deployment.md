# Zerolog Production Deployment Guide

## Production Configuration

### Environment-Based Setup

Configure logging based on environment variables:

```go
package logging

import (
    "os"
    "strconv"
    "time"
    "github.com/rs/zerolog"
)

type Config struct {
    Level           zerolog.Level
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

func LoadConfig() Config {
    config := Config{
        Level:           parseLevel(getEnv("LOG_LEVEL", "info")),
        Format:          getEnv("LOG_FORMAT", "json"),
        ReportTimestamp: getEnvBool("LOG_TIMESTAMP", true),
        ReportCaller:    getEnvBool("LOG_CALLER", false),
        TimeFormat:      getEnv("LOG_TIME_FORMAT", time.RFC3339),
        OutputFile:      getEnv("LOG_OUTPUT", "stdout"),
        MaxSize:         getEnvInt("LOG_MAX_SIZE", 100),
        MaxBackups:      getEnvInt("LOG_MAX_BACKUPS", 3),
        MaxAge:          getEnvInt("LOG_MAX_AGE", 28),
        Compress:        getEnvBool("LOG_COMPRESS", true),
    }

    return config
}

func parseLevel(levelStr string) zerolog.Level {
    level, err := zerolog.ParseLevel(levelStr)
    if err != nil {
        return zerolog.InfoLevel
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

Create a robust logger factory for production:

```go
package logging

import (
    "os"
    "io"
    "compress/gzip"
    "github.com/rs/zerolog"
    "gopkg.in/natefinch/lumberjack.v2"
)

type LoggerFactory struct {
    serviceName string
    version     string
    environment string
    instanceID  string
}

func NewLoggerFactory(serviceName, version, environment string) *LoggerFactory {
    return &LoggerFactory{
        serviceName: serviceName,
        version:     version,
        environment: environment,
        instanceID:  getInstanceID(),
    }
}

func (lf *LoggerFactory) CreateLogger(config Config) zerolog.Logger {
    var output io.Writer

    // Setup output destination
    switch config.OutputFile {
    case "stdout":
        output = os.Stdout
    case "stderr":
        output = os.Stderr
    default:
        output = lf.createRotatingFile(config)
    }

    // Apply compression if enabled
    if config.Compress && config.OutputFile != "stdout" && config.OutputFile != "stderr" {
        output = &compressingWriter{wrapped: output}
    }

    // Create base logger
    logger := zerolog.New(output)

    // Apply configuration
    logger = logger.Level(config.Level)

    if config.ReportTimestamp {
        logger = logger.With().Timestamp()
        if config.TimeFormat != "" {
            logger = logger.With().TimeFormat(config.TimeFormat)
        }
    }

    if config.ReportCaller {
        logger = logger.With().Caller()
    }

    // Add standard fields
    logger = logger.With().
        Str("service", lf.serviceName).
        Str("version", lf.version).
        Str("environment", lf.environment).
        Str("instance_id", lf.instanceID).
        Logger()

    return logger
}

func (lf *LoggerFactory) createRotatingFile(config Config) io.Writer {
    return &lumberjack.Logger{
        Filename:   config.OutputFile,
        MaxSize:    config.MaxSize,    // MB
        MaxBackups: config.MaxBackups,
        MaxAge:     config.MaxAge,     // days
        Compress:   config.Compress,
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
```

### Production Initialization

Initialize logger for production deployment:

```go
package main

import (
    "os"
    "github.com/rs/zerolog/log"
    "your-project/logging"
)

func initLogger() {
    config := logging.LoadConfig()
    factory := logging.NewLoggerFactory(
        getEnv("SERVICE_NAME", "my-service"),
        getEnv("SERVICE_VERSION", "1.0.0"),
        getEnv("ENVIRONMENT", "production"),
    )

    logger := factory.CreateLogger(config)
    log.SetDefault(logger)

    // Log initialization
    log.Info().
        Str("config", "loaded").
        Msg("Logger initialized for production")
}

func main() {
    initLogger()

    log.Info().
        Str("event", "application_started").
        Msg("Application started successfully")

    // Application logic...
}
```

## Log Rotation and Retention

### Lumberjack Integration

Use lumberjack for automatic log rotation:

```go
package logging

import (
    "os"
    "time"
    "github.com/rs/zerolog"
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

func createProductionLogger(logFile string) zerolog.Logger {
    // Log rotation configuration
    maxSize := getEnvInt("LOG_MAX_SIZE", 100)    // 100MB
    maxBackups := getEnvInt("LOG_MAX_BACKUPS", 7) // Keep 7 backups
    maxAge := getEnvInt("LOG_MAX_AGE", 30)       // Keep for 30 days

    output := setupFileLogging(logFile, maxSize, maxBackups, maxAge)

    logger := zerolog.New(output).
        With().
        Timestamp().
        Str("service", "my-service").
        Str("version", os.Getenv("SERVICE_VERSION")).
        Logger()

    // Set production-appropriate log level
    level := parseLevel(getEnv("LOG_LEVEL", "info"))
    logger = logger.Level(level)

    return logger
}
```

### Structured Log Format

Standardize log structure for production:

```go
package logging

import (
    "context"
    "time"
    "github.com/rs/zerolog"
)

// Standardized log fields
const (
    FieldTimestamp    = "timestamp"
    FieldLevel        = "level"
    FieldService      = "service"
    FieldVersion      = "version"
    FieldEnvironment  = "environment"
    FieldInstanceID   = "instance_id"
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

// RequestLogger provides standardized request logging
type RequestLogger struct {
    logger zerolog.Logger
    ctx    context.Context
}

func NewRequestLogger(logger zerolog.Logger, ctx context.Context) *RequestLogger {
    return &RequestLogger{
        logger: logger,
        ctx:    ctx,
    }
}

func (rl *RequestLogger) WithRequest(requestID, traceID, spanID string) *RequestLogger {
    logger := rl.logger.With().
        Str(FieldRequestID, requestID).
        Str(FieldTraceID, traceID).
        Str(FieldSpanID, spanID).
        Logger()

    return &RequestLogger{logger: logger, ctx: rl.ctx}
}

func (rl *RequestLogger) WithUser(userID, sessionID string) *RequestLogger {
    logger := rl.logger.With().
        Str(FieldUserID, userID).
        Str(FieldSessionID, sessionID).
        Logger()

    return &RequestLogger{logger: logger, ctx: rl.ctx}
}

func (rl *RequestLogger) LogRequest(method, path string, headers map[string]string) {
    rl.logger.Info().
        Str(FieldOperation, "http_request").
        Str("method", method).
        Str("path", path).
        Dict("headers", rl.toDict(headers)).
        Msg("HTTP request received")
}

func (rl *RequestLogger) LogResponse(statusCode int, duration time.Duration, responseSize int64) {
    rl.logger.Info().
        Str(FieldOperation, "http_response").
        Int(FieldStatusCode, statusCode).
        Int64(FieldDuration, duration.Milliseconds()).
        Int64("response_size", responseSize).
        Msg("HTTP response sent")
}

func (rl *RequestLogger) LogError(operation string, err error, fields map[string]interface{}) {
    event := rl.logger.Error().
        Str(FieldOperation, operation).
        Err(err)

    for k, v := range fields {
        event.Interface(k, v)
    }

    event.Msg("Operation failed")
}

func (rl *RequestLogger) toDict(m map[string]string) zerolog.LogObjectMarshalerFunc {
    return func(e *zerolog.Event) {
        for k, v := range m {
            e.Str(k, v)
        }
    }
}
```

## Error Handling and Monitoring

### Error Classification

Implement structured error handling:

```go
package logging

import (
    "errors"
    "net/http"
    "github.com/rs/zerolog"
)

// Error types for better monitoring
type ErrorType string

const (
    ErrorTypeValidation   ErrorType = "validation"
    ErrorTypeDatabase     ErrorType = "database"
    ErrorTypeNetwork      ErrorType = "network"
    ErrorTypeAuth         ErrorType = "authentication"
    ErrorTypeAuthz        ErrorType = "authorization"
    ErrorTypeBusiness     ErrorType = "business"
    ErrorTypeSystem       ErrorType = "system"
    ErrorTypeThirdParty   ErrorType = "third_party"
    ErrorTypeRateLimit    ErrorType = "rate_limit"
    ErrorTypeTimeout      ErrorType = "timeout"
)

type AppError struct {
    Type        ErrorType `json:"type"`
    Code        string    `json:"code"`
    Message     string    `json:"message"`
    Details     string    `json:"details,omitempty"`
    Retryable   bool      `json:"retryable"`
    HTTPStatus  int       `json:"http_status,omitempty"`
    Cause       error     `json:"-"`
    Severity    string    `json:"severity"`
    Component   string    `json:"component"`
    Operation   string    `json:"operation"`
    RequestID   string    `json:"request_id,omitempty"`
    UserID      string    `json:"user_id,omitempty"`
    Timestamp   int64     `json:"timestamp"`
}

func (e AppError) Error() string {
    return e.Message
}

func (e AppError) MarshalZerologObject(event *zerolog.Event) {
    event.Str("error_type", string(e.Type)).
        Str("error_code", e.Code).
        Str("error_message", e.Message).
        Bool("retryable", e.Retryable).
        Str("severity", e.Severity).
        Str("component", e.Component).
        Str("operation", e.Operation).
        Int64("timestamp", e.Timestamp)

    if e.Details != "" {
        event.Str("error_details", e.Details)
    }
    if e.HTTPStatus > 0 {
        event.Int("http_status", e.HTTPStatus)
    }
    if e.RequestID != "" {
        event.Str("request_id", e.RequestID)
    }
    if e.UserID != "" {
        event.Str("user_id", e.UserID)
    }
    if e.Cause != nil {
        event.Err(e.Cause)
    }
}

// Error builder
type ErrorBuilder struct {
    error AppError
}

func NewError(errType ErrorType, code, message string) *ErrorBuilder {
    return &ErrorBuilder{
        error: AppError{
            Type:      errType,
            Code:      code,
            Message:   message,
            Timestamp: time.Now().Unix(),
            Severity:  "medium",
        },
    }
}

func (eb *ErrorBuilder) Details(details string) *ErrorBuilder {
    eb.error.Details = details
    return eb
}

func (eb *ErrorBuilder) Retryable(retryable bool) *ErrorBuilder {
    eb.error.Retryable = retryable
    return eb
}

func (eb *ErrorBuilder) HTTPStatus(status int) *ErrorBuilder {
    eb.error.HTTPStatus = status
    return eb
}

func (eb *ErrorBuilder) Cause(err error) *ErrorBuilder {
    eb.error.Cause = err
    return eb
}

func (eb *ErrorBuilder) Severity(severity string) *ErrorBuilder {
    eb.error.Severity = severity
    return eb
}

func (eb *ErrorBuilder) Component(component string) *ErrorBuilder {
    eb.error.Component = component
    return eb
}

func (eb *ErrorBuilder) Operation(operation string) *ErrorBuilder {
    eb.error.Operation = operation
    return eb
}

func (eb *ErrorBuilder) RequestID(requestID string) *ErrorBuilder {
    eb.error.RequestID = requestID
    return eb
}

func (eb *ErrorBuilder) Build() AppError {
    return eb.error
}
```

### Error Logging Best Practices

Implement comprehensive error logging:

```go
package logging

import (
    "context"
    "github.com/rs/zerolog"
)

type ErrorLogger struct {
    logger zerolog.Logger
}

func NewErrorLogger(logger zerolog.Logger) *ErrorLogger {
    return &ErrorLogger{logger: logger}
}

func (el *ErrorLogger) LogAppError(ctx context.Context, appErr AppError) {
    // Add context fields if available
    event := el.logger.Error().Object("error", appErr)

    if requestID := ctx.Value("request_id"); requestID != nil {
        event.Str("request_id", requestID.(string))
    }
    if userID := ctx.Value("user_id"); userID != nil {
        event.Str("user_id", userID.(string))
    }

    // Set level based on severity
    switch appErr.Severity {
    case "low":
        event = el.logger.Warn().Object("error", appErr)
    case "medium":
        event = el.logger.Error().Object("error", appErr)
    case "high", "critical":
        event = el.logger.Error().Object("error", appErr).Str("alert", "oncall")
    }

    event.Msg("Application error occurred")
}

func (el *ErrorLogger) LogPanic(ctx context.Context, err interface{}, stack string) {
    event := el.logger.Error().
        Interface("panic", err).
        Str("stack_trace", stack)

    if requestID := ctx.Value("request_id"); requestID != nil {
        event.Str("request_id", requestID.(string))
    }

    event.Str("alert", "oncall").Msg("Application panic occurred")
}
```

## Health Monitoring and Metrics

### Logging Metrics Integration

Integrate logging with application metrics:

```go
package logging

import (
    "sync/atomic"
    "time"
    "github.com/rs/zerolog"
)

type LoggingMetrics struct {
    // Counters
    LogCount       int64
    ErrorCount     int64
    WarnCount      int64
    InfoCount      int64
    DebugCount     int64

    // Timings
    TotalWriteTime time.Duration
    MaxWriteTime   time.Duration

    // Sizes
    TotalBytesWritten int64
    MaxLogSize        int64
}

func (lm *LoggingMetrics) RecordLog(level zerolog.Level, writeTime time.Duration, size int) {
    atomic.AddInt64(&lm.LogCount, 1)
    atomic.AddInt64((*int64)(&lm.TotalWriteTime), int64(writeTime))
    atomic.AddInt64(&lm.TotalBytesWritten, int64(size))

    // Update max values
    for {
        current := atomic.LoadInt64(&lm.MaxWriteTime)
        if int64(writeTime) <= current {
            break
        }
        if atomic.CompareAndSwapInt64(&lm.MaxWriteTime, current, int64(writeTime)) {
            break
        }
    }

    for {
        current := atomic.LoadInt64(&lm.MaxLogSize)
        if int64(size) <= current {
            break
        }
        if atomic.CompareAndSwapInt64(&lm.MaxLogSize, current, int64(size)) {
            break
        }
    }

    // Level-specific counters
    switch level {
    case zerolog.ErrorLevel:
        atomic.AddInt64(&lm.ErrorCount, 1)
    case zerolog.WarnLevel:
        atomic.AddInt64(&lm.WarnCount, 1)
    case zerolog.InfoLevel:
        atomic.AddInt64(&lm.InfoCount, 1)
    case zerolog.DebugLevel:
        atomic.AddInt64(&lm.DebugCount, 1)
    }
}

// Metrics hook for zerolog
type MetricsHook struct {
    metrics *LoggingMetrics
}

func NewMetricsHook(metrics *LoggingMetrics) *MetricsHook {
    return &MetricsHook{metrics: metrics}
}

func (mh *MetricsHook) Run(e *zerolog.Event, level zerolog.Level, message string) {
    start := time.Now()

    // The actual write will happen after this hook
    // We'll capture the timing and size in a separate mechanism
    go func() {
        writeTime := time.Since(start)
        size := len(message) // This is approximate
        mh.metrics.RecordLog(level, writeTime, size)
    }()
}
```

### Health Check Integration

Include logging health in application health checks:

```go
package health

import (
    "sync"
    "time"
    "github.com/rs/zerolog"
)

type LoggingHealth struct {
    logger    zerolog.Logger
    healthy   bool
    lastCheck time.Time
    error     error
    mu        sync.RWMutex
}

func NewLoggingHealth(logger zerolog.Logger) *LoggingHealth {
    return &LoggingHealth{
        logger: logger,
        healthy: true,
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

    // Check if logging takes too long (>1 second)
    if duration > time.Second {
        lh.healthy = false
        lh.error = fmt.Errorf("logging took too long: %v", duration)
        return
    }

    // Check if logger is nil
    if testLogger.GetLevel() == zerolog.Disabled {
        lh.healthy = false
        lh.error = fmt.Errorf("logging is disabled")
        return
    }

    lh.healthy = true
    lh.error = nil
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
        "healthy":    lh.healthy,
        "last_check": lh.lastCheck,
        "error":      lh.error,
    }
}
```

## Security Considerations

### Sensitive Data Filtering

Prevent sensitive data from being logged:

```go
package logging

import (
    "strings"
    "regexp"
)

// Sensitive data patterns
var (
    emailPattern     = regexp.MustCompile(`\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b`)
    passwordPattern  = regexp.MustCompile(`(?i)password['"]?\s*[:=]\s*['"]?([^'"\s]+)`)
    tokenPattern     = regexp.MustCompile(`(?i)(token|key|secret)['"]?\s*[:=]\s*['"]?([^'"\s]{10,})['"]?`)
    creditCardPattern = regexp.MustCompile(`\b\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}\b`)
    ssnPattern       = regexp.MustCompile(`\b\d{3}-?\d{2}-?\d{4}\b`)
)

type SanitizingHook struct{}

func (sh *SanitizingHook) Run(e *zerolog.Event, level zerolog.Level, message string) {
    // This hook doesn't modify the event directly
    // Sanitization should be done before logging
}

// Sanitize message before logging
func SanitizeMessage(message string) string {
    message = emailPattern.ReplaceAllString(message, "email@redacted")
    message = passwordPattern.ReplaceAllString(message, "password=***")
    message = tokenPattern.ReplaceAllString(message, "$1=***")
    message = creditCardPattern.ReplaceAllString(message, "****-****-****-****")
    message = ssnPattern.ReplaceAllString(message, "***-**-****")

    return message
}

// Sanitize string values
func SanitizeValue(key, value string) string {
    if isSensitiveKey(key) {
        return "***"
    }
    return SanitizeMessage(value)
}

func isSensitiveKey(key string) bool {
    sensitiveKeys := []string{
        "password", "passwd", "pwd", "secret", "token", "key", "apikey",
        "api_key", "access_token", "auth_token", "session_id", "csrf_token",
        "credit_card", "ssn", "social_security_number", "pin",
    }

    lowerKey := strings.ToLower(key)
    for _, sensitive := range sensitiveKeys {
        if strings.Contains(lowerKey, sensitive) {
            return true
        }
    }
    return false
}
```

### Access Control

Implement access control for log files:

```go
package logging

import (
    "os"
    "syscall"
)

func SecureLogFile(path string) error {
    // Set file permissions to read/write for owner only
    if err := os.Chmod(path, 0600); err != nil {
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

    // Check if file is owned by current user
    if stat.Uid != uint32(os.Getuid()) {
        return fmt.Errorf("file is not owned by current user")
    }

    return nil
}
```

## Monitoring and Alerting

### Log-Based Alerting

Implement alerting based on log patterns:

```go
package monitoring

import (
    "context"
    "time"
    "github.com/rs/zerolog"
)

type AlertManager struct {
    logger         zerolog.Logger
    errorThreshold int
    timeWindow     time.Duration
    errorCount     int64
    windowStart    time.Time
    alertChannel   chan Alert
}

type Alert struct {
    Type      string    `json:"type"`
    Message   string    `json:"message"`
    Severity  string    `json:"severity"`
    Timestamp time.Time `json:"timestamp"`
    Count     int64     `json:"count"`
}

func NewAlertManager(logger zerolog.Logger, threshold int, window time.Duration) *AlertManager {
    return &AlertManager{
        logger:         logger,
        errorThreshold: threshold,
        timeWindow:     window,
        alertChannel:   make(chan Alert, 100),
    }
}

func (am *AlertManager) ErrorHook(e *zerolog.Event, level zerolog.Level, message string) {
    if level == zerolog.ErrorLevel || level == zerolog.FatalLevel {
        atomic.AddInt64(&am.errorCount, 1)
        am.checkErrorThreshold()
    }
}

func (am *AlertManager) checkErrorThreshold() {
    now := time.Now()

    // Reset window if needed
    if now.Sub(am.windowStart) > am.timeWindow {
        atomic.StoreInt64(&am.errorCount, 0)
        am.windowStart = now
        return
    }

    count := atomic.LoadInt64(&am.errorCount)
    if count >= int64(am.errorThreshold) {
        alert := Alert{
            Type:      "error_threshold",
            Message:   fmt.Sprintf("Error threshold exceeded: %d errors in %v", count, am.timeWindow),
            Severity:  "high",
            Timestamp: now,
            Count:     count,
        }

        select {
        case am.alertChannel <- alert:
        default:
            // Channel full, drop alert
        }

        // Reset counter after alert
        atomic.StoreInt64(&am.errorCount, 0)
    }
}

func (am *AlertManager) StartAlertProcessor(ctx context.Context) {
    go func() {
        for {
            select {
            case alert := <-am.alertChannel:
                am.processAlert(alert)
            case <-ctx.Done():
                return
            }
        }
    }()
}

func (am *AlertManager) processAlert(alert Alert) {
    // Log the alert
    am.logger.Error().
        Str("alert_type", alert.Type).
        Str("message", alert.Message).
        Str("severity", alert.Severity).
        Time("timestamp", alert.Timestamp).
        Int64("count", alert.Count).
        Msg("Alert triggered")

    // Send to external monitoring system
    // sendToMonitoringSystem(alert)
}
```

## Deployment Checklist

### Production Deployment Verification

Before deploying to production, verify:

- [ ] Environment variables are properly configured
- [ ] Log file permissions are set correctly (600 or 640)
- [ ] Log rotation is configured and tested
- [ ] Error handling includes proper context
- [ ] Sensitive data filtering is implemented
- [ ] Log levels are appropriate for production
- [ ] Performance impact is measured and acceptable
- [ ] Monitoring and alerting are configured
- [ ] Backup and retention policies are defined
- [ ] Log aggregation is configured (if needed)

### Environment Variables Checklist

Required environment variables for production:

```bash
# Basic logging configuration
LOG_LEVEL=info                    # debug, info, warn, error
LOG_FORMAT=json                  # json or logfmt
LOG_OUTPUT=/var/log/app/app.log  # stdout, stderr, or file path
LOG_TIMESTAMP=true
LOG_CALLER=false

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
```

### Health Check Endpoints

Include logging health in application health endpoints:

```go
package main

import (
    "encoding/json"
    "net/http"
    "your-project/logging"
    "your-project/health"
)

func healthHandler(w http.ResponseWriter, r *http.Request) {
    healthStatus := map[string]interface{}{
        "status": "healthy",
        "timestamp": time.Now().Unix(),
        "version": os.Getenv("SERVICE_VERSION"),
    }

    // Check logging health
    loggingHealth := logging.GetHealthStatus()
    healthStatus["logging"] = loggingHealth

    if !loggingHealth["healthy"].(bool) {
        healthStatus["status"] = "degraded"
        w.WriteHeader(http.StatusServiceUnavailable)
    }

    json.NewEncoder(w).Encode(healthStatus)
}
```

This comprehensive production deployment guide ensures that Zerolog is properly configured for production environments with appropriate security, monitoring, and operational considerations.