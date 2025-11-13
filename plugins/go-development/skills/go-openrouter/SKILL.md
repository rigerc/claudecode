---
name: go-openrouter
description: Use when working with the OpenRouter Go client library for AI model integration. Provides expertise in chat completions, streaming, function calling, and structured outputs.
---

# Go OpenRouter Client Library Expert

Expert assistance for the OpenRouter Go client library, enabling access to hundreds of AI models from multiple providers through a unified API.

## When to Use This Skill

Use this skill when you need help with:

- Setting up OpenRouter API clients in Go
- Implementing chat completions and streaming responses
- Using function calling and structured outputs
- Error handling and retry logic
- Model selection and cost optimization
- Integrating OpenRouter into web servers or CLI tools

## Quick Start

```go
import openrouter "github.com/revrost/go-openrouter"

client := openrouter.NewClient("your-api-key")
resp, err := client.CreateChatCompletion(context.Background(),
    openrouter.ChatCompletionRequest{
        Model: "deepseek/deepseek-chat-v3-0324:free",
        Messages: []openrouter.ChatCompletionMessage{{
            Role: openrouter.ChatMessageRoleUser,
            Content: openrouter.Content{Text: "Hello!"},
        }},
    })
```

## Available Resources

See `references/` for comprehensive documentation:

- **api_reference.md**: Complete API documentation and request/response structures
- **streaming_guide.md**: Streaming responses and real-time chat implementation
- **function_calling.md**: Function calling and structured output patterns
- **error_handling.md**: Error handling, retry logic, and best practices
- **model_selection.md**: Model selection strategies and cost optimization
- **model_list.md**: Available models and provider comparison
- **integration_patterns.md**: Web server, CLI, and application integration examples
