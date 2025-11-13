# Beta Features Guide

## Thinking Mode

Enable extended thinking capabilities for complex reasoning tasks.

```go
message, err := client.Messages.New(context.TODO(), anthropic.MessageNewParams{
    Model:     anthropic.ModelClaude3_7SonnetLatest,
    MaxTokens: 1024,
    Messages:  messages,
    Betas: []anthropic.AnthropicBeta{
        anthropic.AnthropicBetaThinkingAPI20241120,
    },
    ThinkingConfig: anthropic.ThinkingConfigParamUnion{
        OfThinkingConfigEnabled: &anthropic.ThinkingConfigEnabledParam{
            Budget: anthropic.Int(5000), // Thinking budget tokens
        },
    },
})
```

### Thinking Events in Streaming

```go
for stream.Next() {
    event := stream.Current()
    switch eventVariant := event.AsAny().(type) {
    case anthropic.ContentBlockDeltaEvent:
        switch deltaVariant := eventVariant.Delta.AsAny().(type) {
        case anthropic.ThinkingDelta:
            fmt.Printf("Thinking: %s\n", deltaVariant.Text)
        case anthropic.TextDelta:
            fmt.Printf("Response: %s\n", deltaVariant.Text)
        }
    }
}
```

## Web Search Integration

Enable Claude to search the web for current information.

```go
tools := []anthropic.ToolUnionParam{
    {
        OfBetaTool: &anthropic.BetaToolParam{
            OfWebSearchTool20250305: &anthropic.BetaWebSearchTool20250305Param{
                SearchContextSize: anthropic.BetaWebSearchTool20250305SearchContextSizeMedium,
                UserLocation: anthropic.BetaWebSearchTool20250305UserLocationParamUnion{
                    OfFreeform: &anthropic.BetaWebSearchTool20250305UserLocationFreeformParam{
                        Country: "US",
                        City:    "San Francisco",
                    },
                },
            },
        },
    },
}

message, err := client.Messages.New(context.TODO(), anthropic.MessageNewParams{
    Model:     anthropic.ModelClaude3_7SonnetLatest,
    MaxTokens: 1024,
    Messages:  messages,
    Tools:     tools,
    Betas: []anthropic.AnthropicBeta{
        anthropic.AnthropicBetaWebSearchTool20250305,
    },
})
```

### Search Context Sizes
- `Small`: Faster, less context
- `Medium`: Balanced performance and context
- `Large`: Comprehensive results, slower

## Beta Feature Best Practices

### Version Management
- Always specify beta versions explicitly
- Monitor beta release notes for changes
- Plan migration path to stable APIs

### Testing
- Test beta features thoroughly in development
- Have fallback mechanisms for production
- Monitor usage and costs carefully

### Gradual Adoption
- Start with non-critical features
- Gather metrics on performance and cost
- Scale usage based on results
