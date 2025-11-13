# Model Selection and Cost Optimization

Strategies for selecting models and optimizing costs.

## Model Selection Strategy

### Task-Based Model Selection

```go
func getModelForTask(taskType string) string {
    switch taskType {
    case "simple_qa":
        return "meta-llama/llama-3.1-8b-instruct:free"
    case "complex_reasoning":
        return "anthropic/claude-3-5-sonnet"
    case "code_generation":
        return "openai/gpt-4o-mini"
    case "creative_writing":
        return "meta-llama/llama-3.1-70b-instruct"
    case "fast_response":
        return "deepseek/deepseek-chat-v3-0324:free"
    default:
        return "openai/gpt-3.5-turbo"
    }
}

// Usage
model := getModelForTask("code_generation")
resp, err := client.CreateChatCompletion(
    context.Background(),
    openrouter.ChatCompletionRequest{
        Model:    model,
        Messages: messages,
    },
)
```

### Fallback Strategy

```go
func getChatResponse(
    client *openrouter.Client,
    messages []openrouter.ChatCompletionMessage,
) (string, error) {
    // Try models in order of preference/cost
    models := []string{
        "meta-llama/llama-3.1-8b-instruct:free",  // Free, fast
        "openai/gpt-4o-mini",                      // Low cost
        "anthropic/claude-3-5-sonnet",             // High quality
    }

    for _, model := range models {
        resp, err := client.CreateChatCompletion(
            context.Background(),
            openrouter.ChatCompletionRequest{
                Model:    model,
                Messages: messages,
            },
        )

        if err == nil {
            return resp.Choices[0].Message.Content, nil
        }

        fmt.Printf("Model %s failed: %v, trying next...\n", model, err)
    }

    return "", fmt.Errorf("all models failed")
}
```

## Available Models

### Free Models (No Cost)

- `meta-llama/llama-3.1-8b-instruct:free` - Fast, general purpose
- `deepseek/deepseek-chat-v3-0324:free` - High quality, free tier
- `qwen/qwen3-235b-a22b-07-25:free` - Advanced reasoning

### Premium Models (Low Cost)

- `openai/gpt-4o-mini` - Balanced cost/quality
- `anthropic/claude-3-haiku` - Fast, affordable
- `meta-llama/llama-3.1-70b-instruct` - High quality, reasonable cost

### Premium Models (High Quality)

- `anthropic/claude-3-5-sonnet` - Best reasoning
- `openai/gpt-4o` - Multimodal, high quality
- `anthropic/claude-3-opus` - Most capable

## Cost Optimization

### Token Limit Strategy

```go
func optimizeTokenUsage(
    client *openrouter.Client,
    messages []openrouter.ChatCompletionMessage,
    budget int, // Maximum tokens
) (*openrouter.ChatCompletionResponse, error) {
    // Estimate prompt tokens (rough estimate)
    promptTokens := estimateTokens(messages)

    // Reserve budget for completion
    maxCompletionTokens := budget - promptTokens

    if maxCompletionTokens <= 0 {
        return nil, fmt.Errorf("prompt exceeds token budget")
    }

    return client.CreateChatCompletion(
        context.Background(),
        openrouter.ChatCompletionRequest{
            Model:     "openai/gpt-4o-mini",
            Messages:  messages,
            MaxTokens: maxCompletionTokens,
        },
    )
}

func estimateTokens(messages []openrouter.ChatCompletionMessage) int {
    // Rough estimate: ~4 characters per token
    totalChars := 0
    for _, msg := range messages {
        totalChars += len(msg.Content.Text)
    }
    return totalChars / 4
}
```

### Caching Strategy

```go
type ResponseCache struct {
    cache map[string]string
    mu    sync.RWMutex
    ttl   time.Duration
}

type CacheEntry struct {
    response  string
    timestamp time.Time
}

func NewResponseCache(ttl time.Duration) *ResponseCache {
    return &ResponseCache{
        cache: make(map[string]string),
        ttl:   ttl,
    }
}

func (rc *ResponseCache) Get(key string) (string, bool) {
    rc.mu.RLock()
    defer rc.mu.RUnlock()

    response, exists := rc.cache[key]
    return response, exists
}

func (rc *ResponseCache) Set(key, response string) {
    rc.mu.Lock()
    defer rc.mu.Unlock()

    rc.cache[key] = response
}

func getCachedResponse(
    cache *ResponseCache,
    client *openrouter.Client,
    prompt string,
) (string, error) {
    // Generate cache key
    key := fmt.Sprintf("%x", sha256.Sum256([]byte(prompt)))

    // Check cache
    if cached, exists := cache.Get(key); exists {
        return cached, nil
    }

    // Call API
    resp, err := client.CreateChatCompletion(
        context.Background(),
        openrouter.ChatCompletionRequest{
            Model: "openai/gpt-4o-mini",
            Messages: []openrouter.ChatCompletionMessage{
                {
                    Role:    openrouter.ChatMessageRoleUser,
                    Content: openrouter.Content{Text: prompt},
                },
            },
        },
    )

    if err != nil {
        return "", err
    }

    response := resp.Choices[0].Message.Content
    cache.Set(key, response)

    return response, nil
}
```

### Batch Processing

```go
func processBatch(
    client *openrouter.Client,
    prompts []string,
) ([]string, error) {
    results := make([]string, len(prompts))
    errors := make([]error, len(prompts))

    var wg sync.WaitGroup
    semaphore := make(chan struct{}, 5) // Limit concurrent requests

    for i, prompt := range prompts {
        wg.Add(1)
        go func(index int, p string) {
            defer wg.Done()

            semaphore <- struct{}{}        // Acquire
            defer func() { <-semaphore }() // Release

            resp, err := client.CreateChatCompletion(
                context.Background(),
                openrouter.ChatCompletionRequest{
                    Model: "meta-llama/llama-3.1-8b-instruct:free",
                    Messages: []openrouter.ChatCompletionMessage{
                        {
                            Role:    openrouter.ChatMessageRoleUser,
                            Content: openrouter.Content{Text: p},
                        },
                    },
                },
            )

            if err != nil {
                errors[index] = err
                return
            }

            results[index] = resp.Choices[0].Message.Content
        }(i, prompt)
    }

    wg.Wait()

    // Check for errors
    for _, err := range errors {
        if err != nil {
            return results, err
        }
    }

    return results, nil
}
```

## Best Practices

1. **Start with free models**: Test with free tiers before using premium models
2. **Use appropriate model size**: Don't use expensive models for simple tasks
3. **Implement caching**: Cache responses for repeated queries
4. **Monitor token usage**: Track and log token consumption
5. **Set token limits**: Prevent runaway costs with MaxTokens
6. **Batch when possible**: Group similar requests
7. **Fallback to cheaper models**: Have cost-effective fallbacks
8. **Regular cost analysis**: Review API usage and costs regularly
9. **Optimize prompts**: Shorter, clearer prompts use fewer tokens
10. **Use streaming wisely**: Streaming can help with perceived performance but doesn't reduce costs
