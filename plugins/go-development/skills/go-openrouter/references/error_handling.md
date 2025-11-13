# Error Handling and Retry Logic

Best practices for error handling and implementing retry strategies.

## Error Types

### API Error Structure

```go
type APIError struct {
    HTTPStatusCode int
    Message        string
    Type           string
    Code           string
}
```

## Comprehensive Error Handling

### Basic Error Handling

```go
resp, err := client.CreateChatCompletion(ctx, req)
if err != nil {
    if apiErr, ok := err.(*openrouter.APIError); ok {
        switch apiErr.HTTPStatusCode {
        case 401:
            fmt.Println("Authentication failed - check your API key")
        case 429:
            fmt.Println("Rate limit exceeded - implement backoff")
        case 402:
            fmt.Println("Insufficient credits - add funds to your account")
        case 500:
            fmt.Println("Server error - retry with exponential backoff")
        default:
            fmt.Printf("API error: %s\n", apiErr.Message)
        }
        return
    }
    fmt.Printf("Request failed: %v\n", err)
    return
}
```

### HTTP Status Codes

- **400**: Bad Request - Invalid request parameters
- **401**: Unauthorized - Invalid or missing API key
- **402**: Payment Required - Insufficient credits
- **403**: Forbidden - Access denied
- **404**: Not Found - Invalid endpoint or model
- **429**: Too Many Requests - Rate limit exceeded
- **500**: Internal Server Error - Server-side error
- **502**: Bad Gateway - Upstream service error
- **503**: Service Unavailable - Temporary service disruption

## Retry Strategies

### Exponential Backoff

```go
func createChatCompletionWithRetry(
    client *openrouter.Client,
    req openrouter.ChatCompletionRequest,
) (*openrouter.ChatCompletionResponse, error) {
    maxRetries := 3
    baseDelay := 1 * time.Second

    for attempt := 0; attempt < maxRetries; attempt++ {
        resp, err := client.CreateChatCompletion(context.Background(), req)

        if err == nil {
            return resp, nil
        }

        if apiErr, ok := err.(*openrouter.APIError); ok {
            // Retry on rate limit or server errors
            if apiErr.HTTPStatusCode == 429 || apiErr.HTTPStatusCode >= 500 {
                if attempt < maxRetries-1 {
                    delay := baseDelay * time.Duration(1<<attempt)
                    fmt.Printf("Retry attempt %d after %v\n", attempt+1, delay)
                    time.Sleep(delay)
                    continue
                }
            }
            // Don't retry on client errors
            return nil, err
        }

        return nil, err
    }
    return nil, fmt.Errorf("max retries exceeded")
}
```

### Advanced Retry with Jitter

```go
import (
    "math/rand"
    "time"
)

func retryWithJitter(
    client *openrouter.Client,
    req openrouter.ChatCompletionRequest,
    maxRetries int,
) (*openrouter.ChatCompletionResponse, error) {
    baseDelay := 1 * time.Second
    maxDelay := 32 * time.Second

    for attempt := 0; attempt < maxRetries; attempt++ {
        resp, err := client.CreateChatCompletion(context.Background(), req)
        if err == nil {
            return resp, nil
        }

        if apiErr, ok := err.(*openrouter.APIError); ok {
            if !isRetryable(apiErr.HTTPStatusCode) {
                return nil, err
            }

            if attempt < maxRetries-1 {
                // Calculate delay with exponential backoff
                delay := baseDelay * time.Duration(1<<attempt)
                if delay > maxDelay {
                    delay = maxDelay
                }

                // Add jitter (random variation)
                jitter := time.Duration(rand.Int63n(int64(delay / 2)))
                delay = delay + jitter

                fmt.Printf("Retry %d/%d after %v\n", attempt+1, maxRetries, delay)
                time.Sleep(delay)
                continue
            }
        }

        return nil, err
    }

    return nil, fmt.Errorf("max retries (%d) exceeded", maxRetries)
}

func isRetryable(statusCode int) bool {
    switch statusCode {
    case 429, 500, 502, 503:
        return true
    default:
        return false
    }
}
```

### Context-Aware Retry

```go
func retryWithContext(
    ctx context.Context,
    client *openrouter.Client,
    req openrouter.ChatCompletionRequest,
) (*openrouter.ChatCompletionResponse, error) {
    maxRetries := 5
    baseDelay := 1 * time.Second

    for attempt := 0; attempt < maxRetries; attempt++ {
        select {
        case <-ctx.Done():
            return nil, ctx.Err()
        default:
        }

        resp, err := client.CreateChatCompletion(ctx, req)
        if err == nil {
            return resp, nil
        }

        if apiErr, ok := err.(*openrouter.APIError); ok {
            if isRetryable(apiErr.HTTPStatusCode) && attempt < maxRetries-1 {
                delay := baseDelay * time.Duration(1<<attempt)

                select {
                case <-ctx.Done():
                    return nil, ctx.Err()
                case <-time.After(delay):
                    continue
                }
            }
        }

        return nil, err
    }

    return nil, fmt.Errorf("max retries exceeded")
}
```

## Circuit Breaker Pattern

```go
type CircuitBreaker struct {
    maxFailures  int
    timeout      time.Duration
    failures     int
    lastFailTime time.Time
    state        string // "closed", "open", "half-open"
    mu           sync.Mutex
}

func NewCircuitBreaker(maxFailures int, timeout time.Duration) *CircuitBreaker {
    return &CircuitBreaker{
        maxFailures: maxFailures,
        timeout:     timeout,
        state:       "closed",
    }
}

func (cb *CircuitBreaker) Call(
    fn func() (*openrouter.ChatCompletionResponse, error),
) (*openrouter.ChatCompletionResponse, error) {
    cb.mu.Lock()
    defer cb.mu.Unlock()

    if cb.state == "open" {
        if time.Since(cb.lastFailTime) > cb.timeout {
            cb.state = "half-open"
        } else {
            return nil, fmt.Errorf("circuit breaker is open")
        }
    }

    resp, err := fn()
    if err != nil {
        cb.failures++
        cb.lastFailTime = time.Now()

        if cb.failures >= cb.maxFailures {
            cb.state = "open"
        }

        return nil, err
    }

    // Success - reset circuit breaker
    cb.failures = 0
    cb.state = "closed"
    return resp, nil
}
```

## Best Practices

1. **Validate inputs**: Check request parameters before sending
2. **Use timeouts**: Always set context timeouts for requests
3. **Log errors**: Log detailed error information for debugging
4. **Monitor rate limits**: Track API usage to avoid rate limiting
5. **Graceful degradation**: Have fallback strategies for failures
6. **Exponential backoff**: Use increasing delays between retries
7. **Jitter**: Add randomness to avoid thundering herd
8. **Circuit breaker**: Prevent cascading failures in distributed systems
9. **Error metrics**: Track error rates and types for monitoring
10. **User feedback**: Provide clear error messages to users
