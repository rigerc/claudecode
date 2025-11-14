# Best Practices - Model Selection & Cost Optimization

## Overview

This guide covers best practices for selecting appropriate models and optimizing costs when using OpenAI's API with Go applications.

## Model Selection

### Choose the Right Model for Your Task

```go
func getModelForTask(taskType string) string {
    switch taskType {
    case "simple_qa":
        return openai.GPT3Dot5Turbo
    case "complex_reasoning":
        return openai.GPT4
    case "code_generation":
        return openai.GPT4
    case "cost_sensitive":
        return openai.GPT3Dot5Turbo
    default:
        return openai.GPT3Dot5Turbo
    }
}
```

### Model Guidelines

- **GPT-3.5-Turbo**: Best for most general-purpose tasks, cost-effective
- **GPT-4**: Superior for complex reasoning, code generation, and nuanced understanding
- **GPT-4o-mini**: Great balance of capability and cost for structured output
- **Fine-tuned models**: Use for specialized domains or specific formatting requirements

## Cost Optimization

### Monitor Token Usage

```go
// Monitor token usage
func trackUsage(resp *openai.ChatCompletionResponse) {
    if resp.Usage != nil {
        fmt.Printf("Tokens used: %d (prompt: %d, completion: %d)\n",
            resp.Usage.TotalTokens,
            resp.Usage.PromptTokens,
            resp.Usage.CompletionTokens)
    }
}
```

### Set Appropriate Limits

```go
// Set appropriate limits
func getOptimalMaxTokens(taskType string) int {
    switch taskType {
    case "short_answer":
        return 150
    case "medium_answer":
        return 500
    case "long_answer":
        return 2000
    default:
        return 1000
    }
}
```

### Optimization Strategies

1. **Use streaming for long responses** to provide immediate feedback
2. **Set reasonable max_tokens limits** to prevent unexpected costs
3. **Cache embeddings** for frequently queried text
4. **Use appropriate models** - don't use GPT-4 when GPT-3.5-Turbo suffices
5. **Monitor usage** and implement rate limiting for cost control
6. **Consider fine-tuning** if you have consistent patterns and high volume

## Performance Tips

### Connection Reuse

```go
// Reuse HTTP client for better performance
httpClient := &http.Client{
    Timeout: 30 * time.Second,
}

config := openai.DefaultConfig("your-api-key")
config.HTTPClient = httpClient
client := openai.NewClientWithConfig(config)
```

### Batching Requests

```go
// Process multiple embeddings in a single request for efficiency
req := openai.EmbeddingRequest{
    Input: []string{
        "Text 1 to embed",
        "Text 2 to embed",
        "Text 3 to embed",
    },
    Model: openai.AdaEmbeddingV2,
}

resp, err := client.CreateEmbeddings(context.Background(), req)
```

## Related Guides

- [Getting Started](getting-started.md) - Initial setup and configuration
- [Integration Patterns](integration-patterns.md) - Error handling and deployment
- [Chat Completions](chat-completions.md) - Core conversational capabilities