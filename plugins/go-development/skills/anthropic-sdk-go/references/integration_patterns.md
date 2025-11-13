# Integration Patterns

## Web Server Integration

### HTTP Handler with Streaming
```go
func chatHandler(w http.ResponseWriter, r *http.Request) {
    var request struct {
        Message string `json:"message"`
        Stream  bool   `json:"stream,omitempty"`
    }

    if err := json.NewDecoder(r.Body).Decode(&request); err != nil {
        http.Error(w, "Invalid request", http.StatusBadRequest)
        return
    }

    messages := []anthropic.MessageParam{
        anthropic.NewUserMessage(anthropic.NewTextBlock(request.Message)),
    }

    if request.Stream {
        // Handle streaming response
        stream := client.Messages.NewStreaming(r.Context(), anthropic.MessageNewParams{
            Model:     anthropic.ModelClaude3_7SonnetLatest,
            MaxTokens: 1024,
            Messages:  messages,
        })

        w.Header().Set("Content-Type", "text/plain")
        for stream.Next() {
            event := stream.Current()
            if delta := event.AsAny(); event != nil {
                if textDelta, ok := delta.(anthropic.ContentBlockDeltaEvent); ok {
                    if text := textDelta.Delta.AsAny(); text != nil {
                        if textBlock, ok := text.(anthropic.TextDelta); ok {
                            fmt.Fprint(w, textBlock.Text)
                            flusher, _ := w.(http.Flusher)
                            flusher.Flush()
                        }
                    }
                }
            }
        }
    } else {
        // Handle regular response
        message, err := client.Messages.New(r.Context(), anthropic.MessageNewParams{
            Model:     anthropic.ModelClaude3_7SonnetLatest,
            MaxTokens: 1024,
            Messages:  messages,
        })

        if err != nil {
            http.Error(w, err.Error(), http.StatusInternalServerError)
            return
        }

        response := map[string]interface{}{
            "reply":   message.Content[0].AsAny().(anthropic.TextBlock).Text,
            "usage":   message.Usage,
            "model":   message.Model,
        }

        w.Header().Set("Content-Type", "application/json")
        json.NewEncoder(w).Encode(response)
    }
}
```

## API Key Management

### Configuration Pattern
```go
type Config struct {
    APIKey      string
    Timeout     time.Duration
    MaxRetries  int
}

func NewClientWithConfig(cfg Config) *anthropic.Client {
    return anthropic.NewClient(
        option.WithAPIKey(cfg.APIKey),
        option.WithMaxRetries(cfg.MaxRetries),
    )
}

// Use environment variables
client := anthropic.NewClient()
```

## Cost Optimization

### Token Estimation
```go
// Pre-count tokens to estimate costs
func estimateCost(messages []anthropic.MessageParam, model anthropic.Model) (int, error) {
    tokenCount, err := client.Messages.CountTokens(context.Background(), anthropic.MessageCountTokensParams{
        Model:    model,
        Messages: messages,
    })
    return tokenCount.InputTokens, err
}
```

### Dynamic Max Tokens
```go
// Set appropriate max tokens based on task
func getMaxTokensForTask(taskType string) int {
    switch taskType {
    case "simple_qa":
        return 150
    case "code_generation":
        return 2000
    case "creative_writing":
        return 4000
    default:
        return 1024
    }
}
```

## Production Best Practices

### Context Management
- Use `context.WithTimeout` for request timeouts
- Implement proper cancellation handling
- Pass request context through the chain

### Error Handling
- Log errors with structured logging
- Implement exponential backoff for retries
- Monitor error rates and patterns

### Performance
- Reuse client instances
- Use connection pooling
- Monitor token usage and costs
- Implement caching where appropriate

### Security
- Never commit API keys to source control
- Use environment variables or secret management
- Rotate keys regularly
- Implement rate limiting
