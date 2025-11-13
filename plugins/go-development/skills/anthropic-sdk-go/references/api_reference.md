# Anthropic API Reference

## Client Initialization

### Basic Setup
```go
import (
    "github.com/anthropics/anthropic-sdk-go"
    "github.com/anthropics/anthropic-sdk-go/option"
)

// With API key
client := anthropic.NewClient(
    option.WithAPIKey("your-anthropic-api-key"),
)

// Using environment variable (ANTHROPIC_API_KEY)
client := anthropic.NewClient()
```

### Cloud Provider Integration

#### Amazon Bedrock
```go
import "github.com/anthropics/anthropic-sdk-go/bedrock"

client := anthropic.NewClient(
    bedrock.WithLoadDefaultConfig(context.Background()),
)
```

#### Google Vertex AI
```go
import "github.com/anthropics/anthropic-sdk-go/vertex"

client := anthropic.NewClient(
    vertex.WithGoogleAuth(context.Background(), "us-central1", "your-project-id"),
)
```

## Message Creation

### Basic Message
```go
message, err := client.Messages.New(context.TODO(), anthropic.MessageNewParams{
    MaxTokens: 1024,
    Messages: []anthropic.MessageParam{{
        Content: []anthropic.ContentBlockParamUnion{{
            OfRequestTextBlock: &anthropic.TextBlockParam{Text: "What is a quaternion?"},
        }},
        Role: anthropic.MessageParamRoleUser,
    }},
    Model: anthropic.ModelClaude3_7SonnetLatest,
})

// Access response content
for _, block := range message.Content {
    switch block := block.AsAny().(type) {
    case anthropic.TextBlock:
        fmt.Println(block.Text)
    }
}
```

### System Prompts
```go
message, err := client.Messages.New(context.TODO(), anthropic.MessageNewParams{
    Model:     anthropic.ModelClaude3_7SonnetLatest,
    MaxTokens: 1024,
    System: []anthropic.TextBlockParam{
        {Text: "You are a helpful AI assistant. Be concise and accurate."},
    },
    Messages: []anthropic.MessageParam{{
        Content: []anthropic.ContentBlockParamUnion{{
            OfRequestTextBlock: &anthropic.TextBlockParam{Text: "Explain quantum computing"},
        }},
        Role: anthropic.MessageParamRoleUser,
    }},
})
```

### Multi-turn Conversations
```go
// Initialize conversation
messages := []anthropic.MessageParam{
    anthropic.NewUserMessage(anthropic.NewTextBlock("What is my first name?")),
}

// First message
message, err := client.Messages.New(context.TODO(), anthropic.MessageNewParams{
    Model:     anthropic.ModelClaude3_7SonnetLatest,
    Messages:  messages,
    MaxTokens: 1024,
})

// Add assistant response to conversation history
messages = append(messages, message.ToParam())

// Continue conversation
messages = append(messages, anthropic.NewUserMessage(
    anthropic.NewTextBlock("My full name is John Doe"),
))

message, err = client.Messages.New(context.TODO(), anthropic.MessageNewParams{
    Model:     anthropic.ModelClaude3_7SonnetLatest,
    Messages:  messages,
    MaxTokens: 1024,
})
```

## Streaming Responses

### Basic Streaming
```go
stream := client.Messages.NewStreaming(context.TODO(), anthropic.MessageNewParams{
    Model:     anthropic.ModelClaude3_7SonnetLatest,
    MaxTokens: 1024,
    Messages: []anthropic.MessageParam{
        anthropic.NewUserMessage(anthropic.NewTextBlock("Write a short story")),
    },
})

message := anthropic.Message{}
for stream.Next() {
    event := stream.Current()
    err := message.Accumulate(event)
    if err != nil {
        panic(err)
    }

    switch eventVariant := event.AsAny().(type) {
    case anthropic.ContentBlockDeltaEvent:
        switch deltaVariant := eventVariant.Delta.AsAny().(type) {
        case anthropic.TextDelta:
            print(deltaVariant.Text)
        case anthropic.ThinkingDelta:
            print("🤔 " + deltaVariant.Text)
        }
    }
}

if stream.Err() != nil {
    panic(stream.Err())
}
```

### Advanced Event Handling
```go
for stream.Next() {
    event := stream.Current()
    switch event := event.AsAny().(type) {
    case anthropic.RawMessageStartEvent:
        fmt.Printf("Message started with ID: %s\n", event.Message.ID)
    case anthropic.ContentBlockDeltaEvent:
        switch delta := event.Delta.AsAny().(type) {
        case anthropic.TextDelta:
            fmt.Printf("Text: %s\n", delta.Text)
        case anthropic.ThinkingDelta:
            fmt.Printf("Thinking: %s\n", delta.Text)
        }
    case anthropic.RawMessageStopEvent:
        fmt.Printf("Message stopped. Reason: %s\n", event.StopReason)
    }
}
```

## Token Counting
```go
tokenCount, err := client.Messages.CountTokens(context.TODO(), anthropic.MessageCountTokensParams{
    Model: anthropic.ModelClaude3_7SonnetLatest,
    Messages: []anthropic.MessageParam{
        anthropic.NewUserMessage(anthropic.NewTextBlock("Your message here")),
    },
})

if err != nil {
    panic(err)
}

fmt.Printf("Token count: %d\n", tokenCount.InputTokens)
```

## Error Handling

### Comprehensive Error Handling
```go
message, err := client.Messages.New(context.TODO(), params)
if err != nil {
    var apierr *anthropic.Error
    if errors.As(err, &apierr) {
        fmt.Printf("API Error: %s\n", apierr.Error())
        fmt.Printf("Status Code: %d\n", apierr.StatusCode)

        // Debug with raw request/response
        fmt.Printf("Request: %s\n", string(apierr.DumpRequest(true)))
        fmt.Printf("Response: %s\n", string(apierr.DumpResponse(true)))

        // Handle specific error types
        switch apierr.StatusCode {
        case 429:
            fmt.Println("Rate limit exceeded - implement backoff")
        case 401:
            fmt.Println("Invalid API key")
        case 400:
            fmt.Println("Invalid request parameters")
        }
    }
    panic(err)
}
```

## Advanced Configuration

```go
// Configure client with global options
client := anthropic.NewClient(
    option.WithHeader("X-Custom-Header", "value"),
    option.WithMaxRetries(3),
)

// Custom middleware
func Logger(req *http.Request, next option.MiddlewareNext) (res *http.Response, err error) {
    start := time.Now()
    fmt.Printf("Request: %s %s\n", req.Method, req.URL.Path)
    res, err = next(req)
    duration := time.Since(start)
    fmt.Printf("Response: %d (took %v)\n", res.StatusCode, duration)
    return res, err
}

client := anthropic.NewClient(
    option.WithMiddleware(Logger),
)

// Per-request timeout
message, err := client.Messages.New(
    context.Background(),
    params,
    option.WithRequestTimeout(30*time.Second),
)
```
