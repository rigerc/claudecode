# Anthropic Go SDK Documentation

## Overview

The Anthropic Go SDK (`anthropic-sdk-go`) is the official Go library for accessing the Anthropic REST API, providing convenient access to Claude models and other Anthropic services. This comprehensive SDK supports message creation, streaming responses, tool calling, file handling, batch processing, and advanced features like thinking mode and web search.

## Installation

```bash
go get -u 'github.com/anthropics/anthropic-sdk-go@v1.4.0'
```

## Basic Setup

### Import and Client Initialization

```go
package main

import (
    "context"
    "fmt"
    "os"

    "github.com/anthropics/anthropic-sdk-go"
    "github.com/anthropics/anthropic-sdk-go/option"
)

func main() {
    // Initialize client with API key
    client := anthropic.NewClient(
        option.WithAPIKey("your-anthropic-api-key"), // or use os.Getenv("ANTHROPIC_API_KEY")
    )

    // Client is now ready to use
    fmt.Println("Anthropic client initialized")
}
```

### Environment Variable Configuration

```go
// The SDK automatically uses ANTHROPIC_API_KEY environment variable if present
client := anthropic.NewClient()

// Or set it programmatically
os.Setenv("ANTHROPIC_API_KEY", "your-api-key")
client := anthropic.NewClient()
```

### Cloud Provider Integration

#### Amazon Bedrock

```go
import (
    "github.com/anthropics/anthropic-sdk-go/bedrock"
)

client := anthropic.NewClient(
    bedrock.WithLoadDefaultConfig(context.Background()),
)
```

#### Google Vertex AI

```go
import (
    "github.com/anthropics/anthropic-sdk-go/vertex"
)

client := anthropic.NewClient(
    vertex.WithGoogleAuth(context.Background(), "us-central1", "your-project-id"),
)
```

## Message API

### Basic Message Creation

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

### Using System Prompts

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

if err != nil {
    panic(err)
}

// Add assistant response to conversation history
messages = append(messages, message.ToParam())

// Add another user message
messages = append(messages, anthropic.NewUserMessage(
    anthropic.NewTextBlock("My full name is John Doe"),
))

// Continue conversation
message, err = client.Messages.New(context.TODO(), anthropic.MessageNewParams{
    Model:     anthropic.ModelClaude3_7SonnetLatest,
    Messages:  messages,
    MaxTokens: 1024,
})
```

## Streaming Responses

### Basic Streaming

```go
content := "Write a short story about a robot learning to paint"

stream := client.Messages.NewStreaming(context.TODO(), anthropic.MessageNewParams{
    Model:     anthropic.ModelClaude3_7SonnetLatest,
    MaxTokens: 1024,
    Messages: []anthropic.MessageParam{
        anthropic.NewUserMessage(anthropic.NewTextBlock(content)),
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
        }
    }
}

if stream.Err() != nil {
    panic(stream.Err())
}

fmt.Println("\nStreaming completed")
```

### Advanced Streaming with Event Types

```go
stream := client.Messages.NewStreaming(context.TODO(), params)

for stream.Next() {
    event := stream.Current()

    switch event := event.AsAny().(type) {
    case anthropic.RawMessageStartEvent:
        fmt.Printf("Message started with ID: %s\n", event.Message.ID)

    case anthropic.RawContentBlockStartEvent:
        fmt.Printf("Content block started with index: %d\n", event.Index)

    case anthropic.ContentBlockDeltaEvent:
        switch delta := event.Delta.AsAny().(type) {
        case anthropic.TextDelta:
            fmt.Printf("Text delta: %s\n", delta.Text)
        case anthropic.ThinkingDelta:
            fmt.Printf("Thinking delta: %s\n", delta.Text)
        }

    case anthropic.RawContentBlockStopEvent:
        fmt.Printf("Content block stopped\n")

    case anthropic.RawMessageStopEvent:
        fmt.Printf("Message stopped. Reason: %s\n", event.StopReason)

    case anthropic.RawMessageDeltaEvent:
        if event.Usage != nil {
            fmt.Printf("Usage: %+v\n", event.Usage)
        }
    }
}
```

## Tool Calling

### Define Tool Schema

```go
import (
    "github.com/invopop/jsonschema"
)

// Define input structure
type GetCoordinatesInput struct {
    Location string `json:"location" jsonschema_description:"The location to look up."`
}

// Generate schema from Go struct
var GetCoordinatesInputSchema = GenerateSchema[GetCoordinatesInput]()

type GetCoordinateResponse struct {
    Long float64 `json:"long"`
    Lat  float64 `json:"lat"`
}

func GetCoordinates(location string) GetCoordinateResponse {
    // Mock implementation
    return GetCoordinateResponse{
        Long: -122.4194,
        Lat:  37.7749,
    }
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
```

### Tool Calling Implementation

```go
func main() {
    client := anthropic.NewClient()

    content := "Where is San Francisco?"
    messages := []anthropic.MessageParam{
        anthropic.NewUserMessage(anthropic.NewTextBlock(content)),
    }

    // Define tools
    toolParams := []anthropic.ToolParam{
        {
            Name:        "get_coordinates",
            Description: anthropic.String("Accepts a place as an address, then returns the latitude and longitude coordinates."),
            InputSchema: GetCoordinatesInputSchema,
        },
    }

    tools := make([]anthropic.ToolUnionParam, len(toolParams))
    for i, toolParam := range toolParams {
        tools[i] = anthropic.ToolUnionParam{OfTool: &toolParam}
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

        // Print assistant response
        fmt.Print("[assistant]: ")
        for _, block := range message.Content {
            switch block := block.AsAny().(type) {
            case anthropic.TextBlock:
                fmt.Println(block.Text)
            case anthropic.ToolUseBlock:
                inputJSON, _ := json.Marshal(block.Input)
                fmt.Printf("%s: %s\n", block.Name, string(inputJSON))
            }
        }

        messages = append(messages, message.ToParam())
        toolResults := []anthropic.ContentBlockParamUnion{}

        // Process tool use blocks
        for _, block := range message.Content {
            if toolUse, ok := block.AsAny().(anthropic.ToolUseBlock); ok {
                fmt.Print("[user (" + toolUse.Name + ")]: ")

                var response interface{}
                switch toolUse.Name {
                case "get_coordinates":
                    var input struct {
                        Location string `json:"location"`
                    }
                    err := json.Unmarshal([]byte(toolUse.JSON.Input.Raw()), &input)
                    if err != nil {
                        panic(err)
                    }
                    response = GetCoordinates(input.Location)
                }

                b, err := json.Marshal(response)
                if err != nil {
                    panic(err)
                }
                fmt.Println(string(b))

                toolResults = append(toolResults, anthropic.NewToolResultBlock(toolUse.ID, string(b), false))
            }
        }

        if len(toolResults) == 0 {
            break // No more tools to execute
        }

        messages = append(messages, anthropic.NewUserMessage(toolResults...))
    }
}
```

## File Operations

### File Upload

```go
import (
    "strings"
    "os"
)

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
    File: anthropic.File(strings.NewReader("my file contents"), "custom-name.json", "application/json"),
    Betas: []anthropic.AnthropicBeta{anthropic.AnthropicBetaFilesAPI2025_04_14},
})
```

### File Management

```go
// Get file metadata
metadata, err := client.Beta.Files.GetMetadata(context.TODO(), "file-id", anthropic.BetaFileGetMetadataParams{})

// List files
page, err := client.Beta.Files.List(context.TODO(), anthropic.BetaFileListParams{
    Limit: anthropic.Int(20),
})

// Auto-paging through all files
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

// Read file content
content, err := io.ReadAll(resp.Body)
if err != nil {
    panic(err)
}
fmt.Printf("File content: %s\n", string(content))
```

## Batch Processing

### Create Message Batch

```go
batch, err := client.Beta.Messages.Batches.New(context.TODO(), anthropic.BetaMessageBatchNewParams{
    // Batch parameters
})
```

### Manage Batches

```go
// Get batch status
batch, err := client.Beta.Messages.Batches.Get(context.TODO(), "batch-id", anthropic.BetaMessageBatchGetParams{})

// List batches
page, err := client.Beta.Messages.Batches.List(context.TODO(), anthropic.BetaMessageBatchListParams{
    Limit: anthropic.Int(20),
})

// Get batch results
results, err := client.Beta.Messages.Batches.Results(context.TODO(), "batch-id", anthropic.BetaMessageBatchResultsParams{})
```

## Models API

### List Available Models

```go
// List all models
page, err := client.Models.List(context.TODO(), anthropic.ModelListParams{})
if err != nil {
    panic(err)
}

for page != nil {
    for _, model := range page.Data {
        fmt.Printf("Model: %s\n", model.ID)
        fmt.Printf("Display Name: %s\n", model.DisplayName)
        fmt.Printf("Created At: %s\n", model.CreatedAt)
        fmt.Println("---")
    }
    page, err = page.GetNextPage()
}

// Auto-paging through all models
iter := client.Models.ListAutoPaging(context.TODO(), anthropic.ModelListParams{})
for iter.Next() {
    model := iter.Current()
    fmt.Printf("Model: %s - %s\n", model.ID, model.DisplayName)
}
```

### Get Specific Model Information

```go
modelInfo, err := client.Models.Get(context.TODO(), "claude-3-5-sonnet-20241022", anthropic.ModelGetParams{})
if err != nil {
    panic(err)
}

fmt.Printf("Model ID: %s\n", modelInfo.ID)
fmt.Printf("Display Name: %s\n", modelInfo.DisplayName)
fmt.Printf("Max Tokens: %d\n", modelInfo.MaxTokens)
```

## Advanced Configuration

### Request Options

```go
// Configure client with global options
client := anthropic.NewClient(
    option.WithHeader("X-Some-Header", "custom_header_info"),
    option.WithMaxRetries(3), // Configure default retry behavior
)

// Per-request options
message, err := client.Messages.New(
    context.TODO(),
    anthropic.MessageNewParams{
        MaxTokens: 1024,
        Messages: []anthropic.MessageParam{{
            Content: []anthropic.ContentBlockParamUnion{{
                OfRequestTextBlock: &anthropic.TextBlockParam{Text: "Hello"},
            }},
            Role: anthropic.MessageParamRoleUser,
        }},
        Model: anthropic.ModelClaude3_7SonnetLatest,
    },
    option.WithHeader("X-Some-Header", "override_value"),
    option.WithRequestTimeout(30*time.Second), // Per-retry timeout
)
```

### Timeout Configuration

```go
// Global timeout including retries
ctx, cancel := context.WithTimeout(context.Background(), 5*time.Minute)
defer cancel()

message, err := client.Messages.New(
    ctx,
    anthropic.MessageNewParams{
        MaxTokens: 1024,
        Messages:  messages,
        Model:     anthropic.ModelClaude3_7SonnetLatest,
    },
    option.WithRequestTimeout(20*time.Second), // Per-retry timeout
)
```

### Custom Middleware

```go
func Logger(req *http.Request, next option.MiddlewareNext) (res *http.Response, err error) {
    // Before request
    start := time.Now()
    fmt.Printf("Request: %s %s\n", req.Method, req.URL.Path)

    // Forward request
    res, err = next(req)

    // After request
    duration := time.Since(start)
    fmt.Printf("Response: %d (took %v)\n", res.StatusCode, duration)

    return res, err
}

client := anthropic.NewClient(
    option.WithMiddleware(Logger),
)
```

### Raw HTTP Response Access

```go
var response *http.Response
message, err := client.Messages.New(
    context.TODO(),
    anthropic.MessageNewParams{
        MaxTokens: 1024,
        Messages:  messages,
        Model:     anthropic.ModelClaude3_7SonnetLatest,
    },
    option.WithResponseInto(&response),
)

if err == nil {
    fmt.Printf("Status Code: %d\n", response.StatusCode)
    fmt.Printf("Headers: %+#v\n", response.Header)
}
```

## Error Handling

### API Error Handling

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
    }
    panic(err)
}
```

### Common Error Types

```go
// Rate limiting
if apierr.StatusCode == 429 {
    fmt.Println("Rate limit exceeded - implement backoff")
}

// Authentication errors
if apierr.StatusCode == 401 {
    fmt.Println("Invalid API key")
}

// Invalid request
if apierr.StatusCode == 400 {
    fmt.Println("Invalid request parameters")
}
```

## Special Features

### Beta Features

```go
// Enable beta features
message, err := client.Beta.Messages.New(context.TODO(), anthropic.BetaMessageNewParams{
    Model:     anthropic.ModelClaude3_7SonnetLatest,
    MaxTokens: 1024,
    Messages:  messages,
    Betas: []anthropic.AnthropicBeta{
        anthropic.AnthropicBetaThinkingAPI20241120,
    },
})
```

### Thinking Mode

```go
message, err := client.Messages.New(context.TODO(), anthropic.MessageNewParams{
    Model:     anthropic.ModelClaude3_7SonnetLatest,
    MaxTokens: 1024,
    Messages:  messages,
    ThinkingConfig: anthropic.ThinkingConfigParamUnion{
        OfThinkingConfigEnabled: &anthropic.ThinkingConfigEnabledParam{
            Budget: anthropic.Int(5000), // Thinking budget tokens
        },
    },
})
```

### Web Search Integration

```go
// Enable web search tool
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

### Counting Tokens

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

## Testing

### Unit Testing

```go
func TestMessageCreation(t *testing.T) {
    client := anthropic.NewClient(
        option.WithAPIKey("test-key"),
    )

    params := anthropic.MessageNewParams{
        Model:     anthropic.ModelClaude3_7SonnetLatest,
        MaxTokens: 1024,
        Messages: []anthropic.MessageParam{{
            Content: []anthropic.ContentBlockParamUnion{{
                OfRequestTextBlock: &anthropic.TextBlockParam{Text: "Hello"},
            }},
            Role: anthropic.MessageParamRoleUser,
        }},
    }

    // Test parameter validation
    if params.Model != anthropic.ModelClaude3_7SonnetLatest {
        t.Error("Model not set correctly")
    }
}
```

### Integration Testing

```go
func TestRealAPI(t *testing.T) {
    if testing.Short() {
        t.Skip("Skipping integration test")
    }

    client := anthropic.NewClient()

    message, err := client.Messages.New(context.Background(), anthropic.MessageNewParams{
        Model:     anthropic.ModelClaude3_7SonnetLatest,
        MaxTokens: 10,
        Messages: []anthropic.MessageParam{{
            Content: []anthropic.ContentBlockParamUnion{{
                OfRequestTextBlock: &anthropic.TextBlockParam{Text: "Say 'test'"},
            }},
            Role: anthropic.MessageParamRoleUser,
        }},
    })

    if err != nil {
        t.Fatalf("API call failed: %v", err)
    }

    if len(message.Content) == 0 {
        t.Error("Expected non-empty response")
    }
}
```

## Best Practices

### 1. **API Key Management**
- Use environment variables for API keys
- Never commit API keys to version control
- Use different keys for different environments

### 2. **Context Management**
- Always use appropriate context timeouts
- Implement proper context cancellation for long-running operations

### 3. **Error Handling**
- Always check for API errors
- Implement exponential backoff for rate limits
- Log raw requests/responses for debugging

### 4. **Token Optimization**
- Use `CountTokens` to estimate costs
- Set appropriate `MaxTokens` limits
- Monitor usage with `Usage` information

### 5. **Streaming for Long Responses**
- Use streaming for responses longer than a few hundred tokens
- Handle stream events appropriately
- Implement proper error handling for streams

### 6. **Tool Design**
- Keep tool functions simple and focused
- Provide clear descriptions and input schemas
- Handle tool errors gracefully

## Available Models

### Claude 3.7 Series
- `claude-3-7-sonnet-latest` - Latest Sonnet model
- `claude-3-7-sonnet-20250219` - Specific version

### Claude 3.5 Series
- `claude-3-5-sonnet-latest` - Latest 3.5 Sonnet
- `claude-3-5-sonnet-20241022` - Specific version
- `claude-3-5-haiku-latest` - Latest 3.5 Haiku
- `claude-3-5-haiku-20241022` - Specific version

### Claude 3 Series
- `claude-3-opus-latest` - Most capable Claude 3
- `claude-3-sonnet-latest` - Balanced performance
- `claude-3-haiku-latest` - Fastest and most cost-effective

## Resources

- [Official Anthropic Documentation](https://docs.anthropic.com)
- [Anthropic Go SDK GitHub](https://github.com/anthropics/anthropic-sdk-go)
- [API Reference](https://docs.anthropic.com/api)
- [Claude Models Overview](https://docs.anthropic.com/claude/docs/models-overview)
- [Pricing Information](https://docs.anthropic.com/claude/docs/pricing)