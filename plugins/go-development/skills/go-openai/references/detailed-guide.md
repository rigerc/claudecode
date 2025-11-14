---
name: go-openai
description: This skill should be used when working with the go-openai library for OpenAI API integration in Go applications. Use it for setting up API clients, implementing chat completions, text completions, function calling, image generation, audio processing, embeddings, fine-tuning, and building comprehensive AI-powered applications.
---

# Go OpenAI - Comprehensive Guide

## Overview

This skill enables developers to integrate OpenAI's powerful AI models into Go applications using the go-openai library, providing comprehensive access to GPT models, DALL-E image generation, Whisper audio processing, embeddings, and fine-tuning capabilities.

## Quick Links

Choose a guide based on what you want to accomplish:

- **🚀 [Getting Started](getting-started.md)** - Basic setup, configuration, and deployment options
- **💬 [Chat Completions, Function Calling & Structured Output](chat-completions.md)** - Conversational AI, tool integration, and structured responses
- **🎨 [Media Generation](media-generation.md)** - DALL-E image generation and Whisper audio processing
- **🔍 [Embeddings & Fine-tuning](embeddings-and-finetuning.md)** - Vector similarity and custom model training
- **🔧 [Integration Patterns](integration-patterns.md)** - Error handling, web servers, and CLI tools
- **📊 [Best Practices](best-practices.md)** - Model selection and cost optimization

## Core Capabilities Overview

### 1. **Chat & Conversational AI**
- Simple and streaming chat completions
- Conversational context management
- Multi-turn conversations with system prompts

### 2. **Function Calling & Structured Output**
- External tool integration
- JSON schema validation
- Automated function execution

### 3. **Media Generation**
- DALL-E 2 & 3 image generation
- Whisper speech-to-text transcription
- Multiple output formats (URL, base64, SRT)

### 4. **Vector Operations**
- Text embeddings for semantic search
- Similarity calculations
- Batch processing for efficiency

### 5. **Custom Models**
- Fine-tuning job management
- Training data upload and validation
- Model deployment and monitoring

### 6. **Enterprise Integration**
- Azure OpenAI support
- Proxy configuration
- Custom HTTP client setup

## Quick Start Example

```go
import (
    "context"
    "fmt"
    openai "github.com/sashabaranov/go-openai"
)

// Initialize client
client := openai.NewClient("your-openai-api-key")

// Simple chat completion
resp, err := client.CreateChatCompletion(
    context.Background(),
    openai.ChatCompletionRequest{
        Model: openai.GPT3Dot5Turbo,
        Messages: []openai.ChatCompletionMessage{
            {
                Role:    openai.ChatMessageRoleUser,
                Content: "Hello! How are you?",
            },
        },
    },
)

if err != nil {
    fmt.Printf("ChatCompletion error: %v\n", err)
    return
}

fmt.Println(resp.Choices[0].Message.Content)
```

## Resources

### references/
- **api_reference.md** - Complete OpenAI API documentation and model specifications
- **models_guide.md** - Model comparison and selection guidelines
- **error_codes.md** - API error codes and troubleshooting strategies
- **fine_tuning_guide.md** - Detailed fine-tuning procedures and best practices

### scripts/
- **client_factory.go** - Client initialization for different environments (OpenAI, Azure, etc.)
- **rate_limiter.go** - Rate limiting and backoff implementation
- **usage_tracker.go** - Token usage monitoring and cost estimation
- **embedding_utils.go** - Vector similarity calculations and embedding utilities

### assets/
- **config_templates/** - Configuration templates for various deployment scenarios
- **training_data_templates/** - JSONL templates for fine-tuning data
- **example_applications/** - Complete applications demonstrating integration patterns
