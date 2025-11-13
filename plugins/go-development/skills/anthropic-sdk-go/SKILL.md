---
name: anthropic-sdk-go
description: Use when integrating the official Anthropic Go SDK for Claude. Covers API clients, messages, streaming, function calling, files, and beta features like thinking mode.
---

# Anthropic SDK Go Expert

Expert assistance for integrating Anthropic's Claude models into Go applications using the official SDK.

## When to Use This Skill

Use this skill when you need help with:

- Setting up API clients (direct, Bedrock, Vertex AI)
- Creating messages and managing conversations
- Streaming responses and event handling
- Function calling and schema generation
- File operations and management
- Beta features (thinking mode, web search)
- Error handling and cost optimization

## Quick Start

```go
import (
    "github.com/anthropics/anthropic-sdk-go"
    "github.com/anthropics/anthropic-sdk-go/option"
)

client := anthropic.NewClient(option.WithAPIKey("your-api-key"))

message, _ := client.Messages.New(context.TODO(), anthropic.MessageNewParams{
    Model:     anthropic.ModelClaude3_7SonnetLatest,
    MaxTokens: 1024,
    Messages: []anthropic.MessageParam{
        anthropic.NewUserMessage(anthropic.NewTextBlock("Hello!")),
    },
})
```

## Available Resources

See `references/` for comprehensive documentation:

- **api_reference.md**: Complete API documentation and examples
- **tool_calling.md**: Function schema generation and implementation
- **file_operations.md**: File upload, download, and management
- **beta_features.md**: Thinking mode and web search integration
- **models_guide.md**: Claude models comparison and selection
- **integration_patterns.md**: Production patterns and best practices
