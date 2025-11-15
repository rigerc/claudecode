# Zerolog Performance Guide

## Zero Allocation Principles

Zerolog achieves exceptional performance through zero-allocation design. Understanding these principles is crucial for getting the best performance.

### Direct JSON Writing

Zerolog writes directly to JSON format without creating intermediate string representations:

```go
// ✅ Zero allocation - direct JSON writing
log.Info().
    Str("user", "alice").
    Int("count", 42).
    Msg("Action completed")

// ❌ String allocation - avoid
message := fmt.Sprintf("User %s performed %d actions", "alice", 42)
log.Info().Msg(message)
```

### Type Safety Over Reflection

Always use strongly-typed field methods:

```go
// ✅ Fast - typed field methods
log.Info().
    Str("name", user.Name).
    Int("age", user.Age).
    Bool("active", user.Active).
    Msg("User data")

// ❌ Slow - reflection
log.Info().
    Interface("user", user).  // Uses reflection
    Msg("User data")
```

### Conditional Expensive Computations

For expensive operations, check if the log level is enabled:

```go
// ✅ Conditional computation
if e := log.Debug(); e.Enabled() {
    expensiveResult := computeExpensiveMetrics()
    e.Str("metrics", expensiveResult).Msg("Computed metrics")
}

// ✅ Use helper pattern
func logDebugMetrics(metrics string) {
    if log.Debug().Enabled() {
        log.Debug().Str("metrics", metrics).Msg("Debug metrics")
    }
}
```

## Performance Optimization Techniques

### Logger Reuse

Create loggers once and reuse them:

```go
// ❌ Bad - creates new logger each time
func processRequest(reqID string) {
    logger := log.With().Str("request_id", reqID).Logger()
    logger.Info().Msg("Processing")
}

// ✅ Good - reuse logger
var requestLogger = log.With().Str("component", "requests").Logger()

func processRequest(reqID string) {
    requestLogger.Info().Str("request_id", reqID).Msg("Processing")
}
```

### Sub-logger Architecture

Design sub-loggers for component separation:

```go
type Logger struct {
    *zerolog.Logger
}

func NewLogger(base zerolog.Logger, component string) Logger {
    return Logger{
        base.With().Str("component", component).Logger(),
    }
}

func (l Logger) WithRequest(reqID string) Logger {
    return Logger{
        l.With().Str("request_id", reqID).Logger(),
    }
}

// Usage
appLogger := NewLogger(baseLogger, "api")
reqLogger := appLogger.WithRequest("req-123")
reqLogger.Info().Msg("Processing request")
```

### Memory Pooling for Frequent Operations

For high-frequency operations, consider memory pooling:

```go
var bufferPool = sync.Pool{
    New: func() interface{} {
        return new(bytes.Buffer)
    },
}

func logWithPool(data LargeData) {
    buf := bufferPool.Get().(*bytes.Buffer)
    defer func() {
        buf.Reset()
        bufferPool.Put(buf)
    }()

    // Use buffer for expensive formatting
    formatData(buf, data)
    log.Debug().Bytes("formatted", buf.Bytes()).Msg("Large data")
}
```

## Sampling for High-Volume Logging

Reduce log volume while maintaining observability:

```go
// Basic sampling - log every Nth message
sampledLogger := logger.Sample(&zerolog.BasicSampler{N: 10})

// Burst sampling - allow N messages per period, then sample
burstSampled := logger.Sample(&zerolog.BurstSampler{
    Burst:       5,
    Period:      1 * time.Second,
    NextSampler: &zerolog.BasicSampler{N: 100},
})

// Level-specific sampling
levelSampled := logger.Sample(zerolog.LevelSampler{
    DebugSampler: &zerolog.BurstSampler{
        Burst:       3,
        Period:      1 * time.Second,
        NextSampler: &zerolog.BasicSampler{N: 50},
    },
    InfoSampler:  &zerolog.BasicSampler{N: 10},
    // Errors are never sampled by default
})

// Pre-configured samplers
oftenSampled := logger.Sample(zerolog.Often)      // ~1 in 10
sometimesSampled := logger.Sample(zerolog.Sometimes) // ~1 in 100
rarelySampled := logger.Sample(zerolog.Rarely)    // ~1 in 1000
```

## Custom Object Marshaling

Implement efficient custom marshaling for complex objects:

```go
type User struct {
    ID       int64  `json:"id"`
    Username string `json:"username"`
    Email    string `json:"email"`
    Active   bool   `json:"active"`
}

// Fast zero-allocation marshaling
func (u User) MarshalZerologObject(e *zerolog.Event) {
    e.Int64("id", u.ID).
        Str("username", u.Username).
        Str("email", u.Email).
        Bool("active", u.Active)
}

// Batch marshaling for arrays
type Users []User

func (users Users) MarshalZerologArray(a *zerolog.Array) {
    // Pre-allocate capacity if known
    if cap(users) > 0 {
        a = reflect.Append(a)
    }

    for _, user := range users {
        a.Object(user)
    }
}

// Usage
users := getUsers() // Large slice
log.Info().Array("users", users).Msg("Batch operation")
```

### Efficient Error Handling

Optimize error logging for high-frequency operations:

```go
// Custom error types for better performance
type APIError struct {
    Code    int
    Message string
    Cause   error
}

func (e APIError) Error() string {
    return fmt.Sprintf("API error %d: %s", e.Code, e.Message)
}

// Fast error marshaling
func (e APIError) MarshalZerologObject(e *zerolog.Event) {
    e.Int("code", e.Code).
        Str("message", e.Message)
    if e.Cause != nil {
        e.Str("cause", e.Cause.Error())
    }
}

// Usage
func handleAPIError(logger zerolog.Logger, err error) {
    if apiErr, ok := err.(APIError); ok {
        logger.Error().Object("error", apiErr).Msg("API error")
        return
    }
    logger.Error().Err(err).Msg("Unknown error")
}
```

## Output Optimization

### Buffered Writing

Use buffered writers for better performance:

```go
// Buffered file writer
file, _ := os.Create("app.log")
bufferedWriter := bufio.NewWriterSize(file, 64*1024) // 64KB buffer

logger := zerolog.New(bufferedWriter).With().Timestamp().Logger()

// Remember to flush periodically
defer func() {
    bufferedWriter.Flush()
    file.Close()
}()

// Or use auto-flush with ticker
flushInterval := time.NewTicker(time.Second)
defer flushInterval.Stop()

go func() {
    for range flushInterval.C {
        bufferedWriter.Flush()
    }
}()
```

### Multi-writer Performance

Optimize multi-writer setups:

```go
// Fast multi-writer with sync
type fastMultiWriter struct {
    writers []io.Writer
}

func (mw *fastMultiWriter) Write(p []byte) (n int, err error) {
    for _, w := range mw.writers {
        n, err = w.Write(p)
        if err != nil {
            return
        }
    }
    return len(p), nil
}

// Usage
fileWriter, _ := os.Create("app.log")
multiWriter := &fastMultiWriter{
    writers: []io.Writer{os.Stdout, fileWriter},
}

logger := zerolog.New(multiWriter).With().Timestamp().Logger()
```

### Concurrent Logging

Ensure thread safety for concurrent access:

```go
// Zerolog is thread-safe, but optimize for concurrent patterns
func processRequestsConcurrently(requests []Request) {
    var wg sync.WaitGroup

    for _, req := range requests {
        wg.Add(1)
        go func(r Request) {
            defer wg.Done()

            // Create logger with request context
            reqLogger := log.With().
                Str("request_id", r.ID).
                Str("user_id", r.UserID).
                Logger()

            reqLogger.Info().Msg("Processing request")
            processRequest(r, reqLogger)
        }(req)
    }

    wg.Wait()
}
```

## Performance Monitoring and Benchmarking

### Performance Metrics

Monitor logging performance:

```go
type LoggingMetrics struct {
    LogCount     int64
    TotalLatency time.Duration
    ErrorCount   int64
}

func (m *LoggingMetrics) RecordLatency(start time.Time, err error) {
    atomic.AddInt64(&m.LogCount, 1)

    latency := time.Since(start)
    atomic.AddInt64(&int64((*time.Duration)(&m.TotalLatency)), int64(latency))

    if err != nil {
        atomic.AddInt64(&m.ErrorCount, 1)
    }
}

func wrapLoggerWithMetrics(logger zerolog.Logger, metrics *LoggingMetrics) zerolog.Logger {
    return logger.Hook(zerolog.HookFunc(func(e *zerolog.Event, level zerolog.Level, message string) {
        start := time.Now()

        // Original logging happens here
        // Hook is called before actual write

        metrics.RecordLatency(start, nil)
    }))
}
```

### Benchmarking

Benchmark your logging patterns:

```go
func BenchmarkSimpleLogging(b *testing.B) {
    logger := zerolog.New(io.Discard)

    b.ResetTimer()
    b.RunParallel(func(pb *testing.PB) {
        for pb.Next() {
            logger.Info().
                Str("user", "alice").
                Int("count", 42).
                Msg("Test message")
        }
    })
}

func BenchmarkComplexLogging(b *testing.B) {
    logger := zerolog.New(io.Discard)

    b.ResetTimer()
    b.RunParallel(func(pb *testing.PB) {
        for pb.Next() {
            logger.Info().
                Str("user", "alice").
                Int("count", 42).
                Float64("value", 123.456).
                Bool("active", true).
                Time("timestamp", time.Now()).
                Dur("latency", 50*time.Millisecond).
                Array("tags", zerolog.Arr().Str("tag1").Str("tag2")).
                Dict("metadata", zerolog.Dict().Str("key", "value")).
                Msg("Complex message")
        }
    })
}
```

## Memory Usage Optimization

### Field Reuse

Reuse field builders for high-frequency operations:

```go
// Field builder pool
var strFieldPool = sync.Pool{
    New: func() interface{} {
        return make([]string, 0, 10)
    },
}

func logWithReusableFields(key, value string) {
    fields := strFieldPool.Get().([]string)
    defer func() {
        fields = fields[:0] // Reset but keep capacity
        strFieldPool.Put(fields)
    }()

    fields = append(fields, key, value)

    // Use fields efficiently
    log.Info().Strs("fields", fields).Msg("Reusable fields")
}
```

### Avoid String Concatenation

Prefer direct field addition:

```go
// ❌ Bad - creates intermediate strings
log.Info().Msgf("User %s performed action %s", username, action)

// ✅ Good - direct field addition
log.Info().
    Str("user", username).
    Str("action", action).
    Msg("User action")
```

### Efficient Context Passing

Pass logger context efficiently:

```go
// Use context for logger propagation
func handleRequest(ctx context.Context, req Request) error {
    logger := zerolog.Ctx(ctx)

    logger.Info().
        Str("request_id", req.ID).
        Str("operation", "process").
        Msg("Processing request")

    return processData(ctx, req.Data)
}

// Initialize context with logger
func createContextWithLogger(parent context.Context) context.Context {
    return log.WithContext(parent)
}
```

## Production Performance Tips

### Log Level Filtering

Set appropriate log levels for production:

```go
// Production configuration
func setupProductionLogger() zerolog.Logger {
    logger := zerolog.New(os.Stdout).
        With().
        Timestamp().
        Str("environment", "production").
        Logger()

    // Set info level for production (filter out debug)
    return logger.Level(zerolog.InfoLevel)
}

// Development configuration
func setupDevelopmentLogger() zerolog.Logger {
    logger := zerolog.New(zerolog.ConsoleWriter{Out: os.Stdout}).
        With().
        Timestamp().
        Caller().
        Logger()

    // Include debug in development
    return logger.Level(zerolog.DebugLevel)
}
```

### Async Logging (Advanced)

For extreme performance, consider async logging:

```go
type AsyncLogger struct {
    logger  zerolog.Logger
    channel chan logEntry
    wg      sync.WaitGroup
}

type logEntry struct {
    level   zerolog.Level
    message string
    fields  map[string]interface{}
}

func NewAsyncLogger(baseLogger zerolog.Logger, bufferSize int) *AsyncLogger {
    al := &AsyncLogger{
        logger:  baseLogger,
        channel: make(chan logEntry, bufferSize),
    }

    al.wg.Add(1)
    go al.processLogs()

    return al
}

func (al *AsyncLogger) processLogs() {
    defer al.wg.Done()

    for entry := range al.channel {
        event := al.logger.WithLevel(entry.level)

        for k, v := range entry.fields {
            event.Interface(k, v)
        }

        event.Msg(entry.message)
    }
}

func (al *AsyncLogger) Log(level zerolog.Level, message string, fields map[string]interface{}) {
    select {
    case al.channel <- logEntry{level, message, fields}:
    default:
        // Channel full, drop log or handle overflow
    }
}
```

## Performance Testing

### Load Testing with Logging

Test logging performance under load:

```go
func TestLoggingUnderLoad(t *testing.T) {
    logger := zerolog.New(os.Stdout)

    numGoroutines := 100
    logsPerGoroutine := 1000

    var wg sync.WaitGroup
    start := time.Now()

    for i := 0; i < numGoroutines; i++ {
        wg.Add(1)
        go func(id int) {
            defer wg.Done()

            for j := 0; j < logsPerGoroutine; j++ {
                logger.Info().
                    Int("goroutine", id).
                    Int("iteration", j).
                    Str("data", "test-data").
                    Msg("Load test message")
            }
        }(i)
    }

    wg.Wait()
    duration := time.Since(start)

    totalLogs := numGoroutines * logsPerGoroutine
    logsPerSecond := float64(totalLogs) / duration.Seconds()

    t.Logf("Logged %d messages in %v (%.2f logs/sec)", totalLogs, duration, logsPerSecond)
}
```

## Performance Checklist

- [ ] Use typed field methods (Str, Int, Bool, etc.) instead of Interface{}
- [ ] Implement MarshalZerologObject for custom types
- [ ] Check log level before expensive computations with Enabled()
- [ ] Use sampling for high-volume debug logs
- [ ] Create loggers once and reuse them
- [ ] Use buffered writers for file output
- [ ] Consider async logging for extreme performance needs
- [ ] Benchmark logging patterns in your specific use case
- [ ] Monitor memory usage and GC pressure
- [ ] Set appropriate log levels for production vs development

Remember: Zerolog is designed for performance, but proper usage patterns are essential to achieve maximum throughput and minimal overhead.