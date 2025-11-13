package main

import (
    "context"
    "fmt"
    "time"
    openrouter "github.com/revrost/go-openrouter"
)

// RetryHandler provides retry logic with exponential backoff for OpenRouter API calls
type RetryHandler struct {
    maxRetries int
    baseDelay  time.Duration
}

// NewRetryHandler creates a new retry handler with default settings
func NewRetryHandler() *RetryHandler {
    return &RetryHandler{
        maxRetries: 3,
        baseDelay:  1 * time.Second,
    }
}

// NewRetryHandlerWithConfig creates a new retry handler with custom settings
func NewRetryHandlerWithConfig(maxRetries int, baseDelay time.Duration) *RetryHandler {
    return &RetryHandler{
        maxRetries: maxRetries,
        baseDelay:  baseDelay,
    }
}

// CreateChatCompletionWithRetry attempts to create a chat completion with retry logic
func (rh *RetryHandler) CreateChatCompletionWithRetry(
    client *openrouter.Client,
    req openrouter.ChatCompletionRequest,
) (*openrouter.ChatCompletionResponse, error) {
    var lastErr error

    for attempt := 0; attempt < rh.maxRetries; attempt++ {
        if attempt > 0 {
            delay := rh.baseDelay * time.Duration(1<<uint(attempt-1))
            fmt.Printf("Retrying in %v (attempt %d/%d)\n", delay, attempt+1, rh.maxRetries)
            time.Sleep(delay)
        }

        resp, err := client.CreateChatCompletion(context.Background(), req)
        if err == nil {
            return resp, nil
        }

        lastErr = err

        // Check if error is retryable
        if apiErr, ok := err.(*openrouter.APIError); ok {
            if apiErr.HTTPStatusCode == 429 || apiErr.HTTPStatusCode >= 500 {
                continue // Retry on rate limit or server errors
            }
            // Don't retry on client errors (4xx except 429)
            break
        }

        // Don't retry on other types of errors
        break
    }

    return nil, fmt.Errorf("max retries exceeded: %w", lastErr)
}

// IsRetryableError checks if an error is retryable
func (rh *RetryHandler) IsRetryableError(err error) bool {
    if apiErr, ok := err.(*openrouter.APIError); ok {
        return apiErr.HTTPStatusCode == 429 || apiErr.HTTPStatusCode >= 500
    }
    return false
}

// GetRetryDelay calculates the delay for a given attempt using exponential backoff
func (rh *RetryHandler) GetRetryDelay(attempt int) time.Duration {
    return rh.baseDelay * time.Duration(1<<uint(attempt))
}