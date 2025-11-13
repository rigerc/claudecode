---
name: anthropic-sdk-go
description: This skill should be used when working with the official Anthropic Go SDK for Claude API integration. Use it for setting up API clients, implementing message creation, streaming responses, tool calling, file handling, batch processing, and advanced features like thinking mode and web search in Go applications.
---

# Anthropic SDK Go

## Overview

This skill enables developers to integrate Anthropic's Claude models into Go applications using the official SDK, providing comprehensive access to Claude's advanced AI capabilities including message creation, streaming, tool calling, and file operations.

## Quick Start

### Basic Client Setup

```go
import (
    "context"
    "github.com/anthropics/anthropic-sdk-go"
    "github.com/anthropics/anthropic-sdk-go/option"
)

// Initialize client with API key
client := anthropic.NewClient(
    option.WithAPIKey("your-anthropic-api-key"),
)

// Or use environment variable (ANTHROPIC_API_KEY)
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

## Core Capabilities

### 1. Message Creation

#### Basic Message
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

if err != nil {
    panic(err.Error())
}

// Access response content
for _, block := range message.Content {
    switch block := block.AsAny().(type) {
    case anthropic.TextBlock:
        fmt.Println(block.Text)
    }
}
```

#### System Prompts
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

#### Multi-turn Conversations
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

### 2. Streaming Responses

#### Basic Streaming
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
            print(deltaVariant.Text) // Print text as it streams
        case anthropic.ThinkingDelta:
            print("🤔 " + deltaVariant.Text) // Print thinking
        }
    }
}

if stream.Err() != nil {
    panic(stream.Err())
}
```

#### Advanced Event Handling
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

### 3. Tool Calling

#### Define Tool Schema
```go
import (
    "github.com/invopop/jsonschema"
    "encoding/json"
)

type GetCoordinatesInput struct {
    Location string `json:"location" jsonschema_description:"The location to look up."`
}

func GenerateSchema[T any]() anthropic.ToolInputSchemaParam {
    reflector := jsonschema.Reflector{
        AllowAdditionalProperties: false,
        DoNotReference:            true,
    }
    var v T
    schema := reflector.Reflect(v)
    return anthropic.ToolInputSchemaParam{
        Properties: schema.Properties,
    }
}

type GetCoordinateResponse struct {
    Long float64 `json:"long"`
    Lat  float64 `json:"lat"`
}

func GetCoordinates(location string) GetCoordinateResponse {
    // Mock implementation
    return GetCoordinateResponse{Long: -122.4194, Lat: 37.7749}
}
```

#### Tool Calling Implementation
```go
func main() {
    client := anthropic.NewClient()

    // Define tools
    tools := []anthropic.ToolUnionParam{
        {
            OfTool: &anthropic.ToolParam{
                Name:        "get_coordinates",
                Description: anthropic.String("Get coordinates for a location"),
                InputSchema: GenerateSchema[GetCoordinatesInput](),
            },
        },
    }

    messages := []anthropic.MessageParam{
        anthropic.NewUserMessage(anthropic.NewTextBlock("Where is San Francisco?")),
    }

    // Conversation loop for tool calling
    for {
        message, err := client.Messages.New(context.TODO(), anthropic.MessageNewParams{
            Model:     anthropic.ModelClaude3_7SonnetLatest,
            MaxTokens: 1024,
            Messages:  messages,
            Tools:     tools,
        })

        if err != nil {
            panic(err)
        }

        messages = append(messages, message.ToParam())
        toolResults := []anthropic.ContentBlockParamUnion{}

        // Process tool use blocks
        for _, block := range message.Content {
            if toolUse, ok := block.AsAny().(anthropic.ToolUseBlock); ok {
                var response interface{}
                switch toolUse.Name {
                case "get_coordinates":
                    var input GetCoordinatesInput
                    err := json.Unmarshal([]byte(toolUse.JSON.Input.Raw()), &input)
                    if err != nil {
                        panic(err)
                    }
                    response = GetCoordinates(input.Location)
                }

                result, _ := json.Marshal(response)
                toolResults = append(toolResults, anthropic.NewToolResultBlock(toolUse.ID, string(result), false))
            }
        }

        if len(toolResults) == 0 {
            break // No more tools to execute
        }

        messages = append(messages, anthropic.NewUserMessage(toolResults...))
    }
}
```

### 4. File Operations

#### File Upload
```go
import "strings"

// Upload from file system
file, err := os.Open("/path/to/file.json")
if err != nil {
    panic(err)
}
defer file.Close()

fileMetadata, err := client.Beta.Files.Upload(context.TODO(), anthropic.BetaFileUploadParams{
    File: anthropic.File(file, "custom-name.json", "application/json"),
    Betas: []anthropic.AnthropicBeta{anthropic.AnthropicBetaFilesAPI2025_04_14},
})

// Upload from string
fileMetadata, err = client.Beta.Files.Upload(context.TODO(), anthropic.BetaFileUploadParams{
    File: anthropic.File(strings.NewReader("file contents"), "custom-name.json", "application/json"),
    Betas: []anthropic.AnthropicBeta{anthropic.AnthropicBetaFilesAPI2025_04_14},
})
```

#### File Management
```go
// List files with auto-paging
iter := client.Beta.Files.ListAutoPaging(context.TODO(), anthropic.BetaFileListParams{
    Limit: anthropic.Int(20),
})

for iter.Next() {
    file := iter.Current()
    fmt.Printf("File: %+v\n", file)
}

if err := iter.Err(); err != nil {
    panic(err.Error())
}

// Download file content
resp, err := client.Beta.Files.Download(context.TODO(), "file-id", anthropic.BetaFileDownloadParams{})
if err != nil {
    panic(err)
}
defer resp.Body.Close()

content, err := io.ReadAll(resp.Body)
fmt.Printf("File content: %s\n", string(content))
```

### 5. Advanced Features

#### Thinking Mode
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

#### Web Search Integration
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
```

#### Token Counting
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

### 6. Error Handling and Configuration

#### Comprehensive Error Handling
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

#### Advanced Configuration
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

## Integration Patterns

### Web Server Integration
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

## Best Practices

### API Key Management
```go
// Use environment variables
client := anthropic.NewClient()

// Or configure with structured approach
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
```

### Cost Optimization
```go
// Pre-count tokens to estimate costs
func estimateCost(messages []anthropic.MessageParam, model anthropic.Model) (int, error) {
    tokenCount, err := client.Messages.CountTokens(context.Background(), anthropic.MessageCountTokensParams{
        Model:    model,
        Messages: messages,
    })
    return tokenCount.InputTokens, err
}

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

## Resources

### references/
- **api_reference.md** - Complete Anthropic API documentation and endpoints
- **models_guide.md** - Claude models comparison and selection guide
- **error_codes.md** - API error codes and troubleshooting
- **beta_features.md** - Documentation for beta features and experimental APIs

### scripts/
- **client_factory.go** - Client initialization utilities for different environments
- **middleware_logger.go** - Request/response logging middleware
- **token_counter.go** - Token counting and cost estimation utilities
- **tool_validator.go** - Tool schema validation and testing

### assets/
- **config_templates/** - Configuration templates for different deployment scenarios
- **example_applications/** - Complete applications demonstrating integration patterns
