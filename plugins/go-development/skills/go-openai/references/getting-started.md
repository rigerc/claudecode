# Getting Started with Go OpenAI

## Overview

This guide covers the initial setup and configuration for integrating OpenAI's powerful AI models into Go applications using the go-openai library.

## Quick Start

### Basic Client Setup

```go
import (
    "context"
    "fmt"
    openai "github.com/sashabaranov/go-openai"
)

// Initialize client with API key
client := openai.NewClient("your-openai-api-key")

// Or use environment variable
// client := openai.NewClient(os.Getenv("OPENAI_API_KEY"))
```

### Custom Configuration

```go
config := openai.DefaultConfig("your-token")
config.BaseURL = "https://api.openai.com/v1"
config.OrgID = "your-org-id" // Optional

// Configure custom HTTP client
config.HTTPClient = &http.Client{
    Timeout: 30 * time.Second,
}

client := openai.NewClientWithConfig(config)
```

## Configuration and Deployment

### Azure OpenAI Integration

```go
config := openai.DefaultAzureConfig("your-azure-key", "https://your-resource.openai.azure.com/")

// Map model names to deployment names
config.AzureModelMapperFunc = func(model string) string {
    azureModelMapping := map[string]string{
        "gpt-3.5-turbo": "your-gpt35-deployment-name",
        "gpt-4":         "your-gpt4-deployment-name",
    }
    return azureModelMapping[model]
}

client := openai.NewClientWithConfig(config)
```

### Proxy Configuration

```go
config := openai.DefaultConfig("token")
proxyUrl, err := url.Parse("http://localhost:8080")
if err != nil {
    panic(err)
}

transport := &http.Transport{
    Proxy: http.ProxyURL(proxyUrl),
}

config.HTTPClient = &http.Client{
    Transport: transport,
}

client := openai.NewClientWithConfig(config)
```

## Next Steps

- [Chat Completions & Function Calling](chat-completions.md) - Learn about conversational AI and structured outputs
- [Media Generation](media-generation.md) - Generate images and process audio
- [Embeddings & Fine-tuning](embeddings-and-finetuning.md) - Work with vector embeddings and custom models
- [Integration Patterns](integration-patterns.md) - Error handling, web servers, and CLI tools
- [Best Practices](best-practices.md) - Model selection and cost optimization