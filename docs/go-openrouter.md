# go-openrouter Library Documentation

## Overview

The `go-openrouter` library is an unofficial Go client library for the OpenRouter API, which provides unified access to hundreds of AI models from various providers through a single API endpoint. This library supports chat completions, streaming responses, function calling, structured outputs, and prompt caching.

OpenRouter allows you to access models from OpenAI, Anthropic, Google, Meta, and many other providers through a consistent API interface.

## Installation

```bash
go get github.com/revrost/go-openrouter
```

## API Key Setup

1. Visit the [OpenRouter website](https://openrouter.ai/docs/quick-start)
2. Sign up or log in to your account
3. Navigate to the API key management page
4. Click "Create new secret key"
5. Provide a name for the key and click "Create secret key"
6. Use the generated API key in your application

**Security Note**: Treat your API key as sensitive information and do not share it or commit it to version control.

## Basic Usage

### Client Initialization

```go
package main

import (
    "context"
    "fmt"
    "os"
    openrouter "github.com/revrost/go-openrouter"
)

func main() {
    // Initialize client with API key
    client := openrouter.NewClient("your-openrouter-api-key")

    // Or use environment variable
    // client := openrouter.NewClient(os.Getenv("OPENROUTER_API_KEY"))
}
```

### Client Configuration Options

```go
client := openrouter.NewClient(
    "your-api-key",
    openrouter.WithXTitle("My App"),           // Set app name for OpenRouter analytics
    openrouter.WithHTTPReferer("https://myapp.com"), // Set your app URL
)
```

### Simple Chat Completion

```go
resp, err := client.CreateChatCompletion(
    context.Background(),
    openrouter.ChatCompletionRequest{
        Model: "deepseek/deepseek-chat-v3-0324:free",
        Messages: []openrouter.ChatCompletionMessage{
            {
                Role:    openrouter.ChatMessageRoleUser,
                Content: openrouter.Content{Text: "Hello! How are you?"},
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

### Streaming Chat Completion

```go
stream, err := client.CreateChatCompletionStream(
    context.Background(),
    openrouter.ChatCompletionRequest{
        Model: "qwen/qwen3-235b-a22b-07-25:free",
        Messages: []openrouter.ChatCompletionMessage{
            {
                Role:    openrouter.ChatMessageRoleUser,
                Content: openrouter.Content{Text: "Tell me a story about AI"},
            },
        },
        Stream: true,
    },
)

if err != nil {
    fmt.Printf("Stream error: %v\n", err)
    return
}
defer stream.Close()

for {
    response, err := stream.Recv()
    if err != nil && err != io.EOF {
        fmt.Printf("Stream error: %v\n", err)
        return
    }

    if errors.Is(err, io.EOF) {
        fmt.Println("\nStream finished")
        return
    }

    // Print the delta content
    if len(response.Choices) > 0 {
        fmt.Print(response.Choices[0].Delta.Content)
    }
}
```

## Advanced Features

### Function Calling

#### Define Function Schema

```go
// Using JSON schema format
funcDef := map[string]interface{}{
    "name":        "get_current_weather",
    "description": "Get the current weather in a given location",
    "parameters": map[string]interface{}{
        "type": "object",
        "properties": map[string]interface{}{
            "location": map[string]interface{}{
                "type":        "string",
                "description": "The city and state, e.g. San Francisco, CA",
            },
            "unit": map[string]interface{}{
                "type": "string",
                "enum": []string{"celsius", "fahrenheit"},
            },
        },
        "required": []string{"location"},
    },
}

// Or using Go structs with jsonschema
funcDef := &openrouter.FunctionDefinition{
    Name: "get_current_weather",
    Parameters: jsonschema.Definition{
        Type: jsonschema.Object,
        Properties: map[string]jsonschema.Definition{
            "location": {
                Type:        jsonschema.String,
                Description: "The city and state, e.g. San Francisco, CA",
            },
            "unit": {
                Type: jsonschema.String,
                Enum: []string{"celsius", "fahrenheit"},
            },
        },
        Required: []string{"location"},
    },
}
```

#### Use Function Calling

```go
resp, err := client.CreateChatCompletion(
    context.Background(),
    openrouter.ChatCompletionRequest{
        Model: "anthropic/claude-3-haiku",
        Messages: []openrouter.ChatCompletionMessage{
            {
                Role:    openrouter.ChatMessageRoleUser,
                Content: openrouter.Content{Text: "What's the weather like in New York?"},
            },
        },
        Functions: []openrouter.FunctionDefinition{*funcDef},
        FunctionCall: "auto",
    },
)

if err != nil {
    fmt.Printf("ChatCompletion error: %v\n", err)
    return
}

// Check if model wants to call a function
if len(resp.Choices) > 0 && resp.Choices[0].Message.FunctionCall != nil {
    functionName := resp.Choices[0].Message.FunctionCall.Name
    arguments := resp.Choices[0].Message.FunctionCall.Arguments

    fmt.Printf("Function call: %s\n", functionName)
    fmt.Printf("Arguments: %s\n", arguments)

    // Parse arguments and call your actual function
    // Then send the result back to the model
}
```

### Structured Output with JSON Schema

```go
type WeatherResult struct {
    Location    string  `json:"location"`
    Temperature float64 `json:"temperature"`
    Condition   string  `json:"condition"`
    Humidity    int     `json:"humidity"`
    WindSpeed   float64 `json:"wind_speed"`
}

var result WeatherResult
schema, err := jsonschema.GenerateSchemaForType(result)
if err != nil {
    log.Fatalf("GenerateSchemaForType error: %v", err)
}

request := openrouter.ChatCompletionRequest{
    Model: openrouter.DeepseekV3,
    Messages: []openrouter.ChatCompletionMessage{
        {
            Role:    openrouter.ChatMessageRoleUser,
            Content: openrouter.Content{Text: "What's the current weather like in London? Include temperature, conditions, humidity, and wind speed."},
        },
    },
    ResponseFormat: &openrouter.ChatCompletionResponseFormat{
        Type: openrouter.ChatCompletionResponseFormatTypeJSONSchema,
        JSONSchema: &openrouter.ChatCompletionResponseFormatJSONSchema{
            Name:   "weather",
            Schema: schema,
            Strict: true,
        },
    },
}

resp, err := client.CreateChatCompletion(ctx, request)
if err != nil {
    fmt.Printf("Error: %v\n", err)
    return
}

// Parse the structured response
err = json.Unmarshal([]byte(resp.Choices[0].Message.Content), &result)
if err != nil {
    fmt.Printf("JSON unmarshal error: %v\n", err)
    return
}

fmt.Printf("Weather in %s:\n", result.Location)
fmt.Printf("Temperature: %.1f°F\n", result.Temperature)
fmt.Printf("Condition: %s\n", result.Condition)
fmt.Printf("Humidity: %d%%\n", result.Humidity)
fmt.Printf("Wind Speed: %.1f mph\n", result.WindSpeed)
```

### Multi-turn Conversations

```go
messages := []openrouter.ChatCompletionMessage{
    {
        Role:    openrouter.ChatMessageRoleSystem,
        Content: openrouter.Content{Text: "You are a helpful AI assistant. Be concise and accurate."},
    },
}

// Function to continue conversation
func continueConversation(userInput string) {
    // Add user message
    messages = append(messages, openrouter.ChatCompletionMessage{
        Role:    openrouter.ChatMessageRoleUser,
        Content: openrouter.Content{Text: userInput},
    })

    // Get response
    resp, err := client.CreateChatCompletion(
        context.Background(),
        openrouter.ChatCompletionRequest{
            Model:    "meta-llama/llama-3.1-8b-instruct:free",
            Messages: messages,
        },
    )

    if err != nil {
        fmt.Printf("Error: %v\n", err)
        return
    }

    assistantResponse := resp.Choices[0].Message.Content

    // Add assistant response to maintain context
    messages = append(messages, openrouter.ChatCompletionMessage{
        Role:    openrouter.ChatMessageRoleAssistant,
        Content: openrouter.Content{Text: assistantResponse},
    })

    fmt.Printf("Assistant: %s\n", assistantResponse)
}
```

## Available Models

OpenRouter provides access to hundreds of models. Here are some popular categories:

### OpenAI Models
- `openai/gpt-4o` - Latest GPT-4 model
- `openai/gpt-4o-mini` - Cost-effective GPT-4 variant
- `openai/gpt-3.5-turbo` - Fast and reliable
- `openai/gpt-4-turbo` - Previous generation

### Anthropic Models
- `anthropic/claude-3-5-sonnet` - Most capable Claude model
- `anthropic/claude-3-haiku` - Fast and cost-effective
- `anthropic/claude-3-opus` - Previous generation

### Meta Models
- `meta-llama/llama-3.1-70b-instruct` - Large open-source model
- `meta-llama/llama-3.1-8b-instruct` - Medium-sized model
- `meta-llama/llama-3.1-405b-instruct` - Massive open-source model

### Google Models
- `google/gemini-pro` - Google's flagship model
- `google/gemini-flash` - Fast variant

### Free Models (for testing)
- `meta-llama/llama-3.1-8b-instruct:free`
- `microsoft/phi-3-mini-128k-instruct:free`
- `qwen/qwen2-72b-instruct:free`

### Model Selection Strategy

```go
// Fallback strategy: try preferred model, fall back to free model
func getChatResponse(messages []openrouter.ChatCompletionMessage) (string, error) {
    models := []string{
        "anthropic/claude-3-5-sonnet",
        "openai/gpt-4o-mini",
        "meta-llama/llama-3.1-8b-instruct:free", // fallback
    }

    for _, model := range models {
        resp, err := client.CreateChatCompletion(
            context.Background(),
            openrouter.ChatCompletionRequest{
                Model:    model,
                Messages: messages,
            },
        )

        if err == nil {
            return resp.Choices[0].Message.Content, nil
        }

        fmt.Printf("Model %s failed: %v, trying next...\n", model, err)
    }

    return "", fmt.Errorf("all models failed")
}
```

## Error Handling

### Comprehensive Error Handling

```go
resp, err := client.CreateChatCompletion(ctx, req)
if err != nil {
    // Check for specific API errors
    if apiErr, ok := err.(*openrouter.APIError); ok {
        switch apiErr.HTTPStatusCode {
        case 401:
            fmt.Println("Authentication failed - check your API key")
        case 429:
            fmt.Println("Rate limit exceeded - implement backoff")
        case 402:
            fmt.Println("Insufficient credits - add funds to your account")
        case 500:
            fmt.Println("Server error - retry with exponential backoff")
        default:
            fmt.Printf("API error: %s\n", apiErr.Message)
        }
        return
    }

    // Handle other errors
    fmt.Printf("Request failed: %v\n", err)
    return
}

// Process successful response
response := resp.Choices[0].Message.Content
fmt.Printf("Response: %s\n", response)
```

### Retry Logic with Exponential Backoff

```go
func createChatCompletionWithRetry(req openrouter.ChatCompletionRequest) (*openrouter.ChatCompletionResponse, error) {
    maxRetries := 3
    baseDelay := 1 * time.Second

    for attempt := 0; attempt < maxRetries; attempt++ {
        resp, err := client.CreateChatCompletion(context.Background(), req)

        if err == nil {
            return resp, nil
        }

        // Check if error is retryable
        if apiErr, ok := err.(*openrouter.APIError); ok {
            if apiErr.HTTPStatusCode == 429 || apiErr.HTTPStatusCode >= 500 {
                if attempt < maxRetries-1 {
                    delay := baseDelay * time.Duration(1<<attempt)
                    fmt.Printf("Retrying in %v (attempt %d/%d)\n", delay, attempt+1, maxRetries)
                    time.Sleep(delay)
                    continue
                }
            }
        }

        // Non-retryable error or max retries reached
        return nil, err
    }

    return nil, fmt.Errorf("max retries exceeded")
}
```

## Configuration and Best Practices

### Environment Configuration

```go
// Recommended: Use environment variables
type Config struct {
    APIKey      string
    AppName     string
    AppURL      string
    DefaultModel string
    MaxTokens   int
}

func loadConfig() *Config {
    return &Config{
        APIKey:       os.Getenv("OPENROUTER_API_KEY"),
        AppName:      os.Getenv("APP_NAME"),
        AppURL:       os.Getenv("APP_URL"),
        DefaultModel: os.Getenv("DEFAULT_MODEL"),
        MaxTokens:    1000,
    }
}

// Initialize client with config
config := loadConfig()
client := openrouter.NewClient(
    config.APIKey,
    openrouter.WithXTitle(config.AppName),
    openrouter.WithHTTPReferer(config.AppURL),
)
```

### Cost Optimization

```go
// Use appropriate models for different tasks
func getModelForTask(taskType string) string {
    switch taskType {
    case "simple_qa":
        return "meta-llama/llama-3.1-8b-instruct:free"
    case "complex_reasoning":
        return "anthropic/claude-3-5-sonnet"
    case "code_generation":
        return "openai/gpt-4o-mini"
    case "creative_writing":
        return "meta-llama/llama-3.1-70b-instruct"
    default:
        return "openai/gpt-3.5-turbo"
    }
}

// Monitor token usage
func trackUsage(resp *openrouter.ChatCompletionResponse) {
    if resp.Usage != nil {
        fmt.Printf("Tokens used: %d (prompt: %d, completion: %d)\n",
            resp.Usage.TotalTokens,
            resp.Usage.PromptTokens,
            resp.Usage.CompletionTokens)
    }
}
```

### Request Optimization

```go
// Set appropriate parameters
req := openrouter.ChatCompletionRequest{
    Model: getModelForTask("simple_qa"),
    Messages: messages,
    MaxTokens: 500,           // Limit response length
    Temperature: 0.7,         // Balance creativity and accuracy
    TopP: 0.9,               // Nucleus sampling
    Stream: false,           // Set to true for long responses
}

// Add system prompt for better results
systemPrompt := "You are a helpful assistant. Provide concise, accurate answers."
messages = append([]openrouter.ChatCompletionMessage{
    {
        Role:    openrouter.ChatMessageRoleSystem,
        Content: openrouter.Content{Text: systemPrompt},
    },
}, messages...)
```

## Integration Examples

### Web Server Example

```go
func chatHandler(w http.ResponseWriter, r *http.Request) {
    if r.Method != "POST" {
        http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
        return
    }

    var request struct {
        Message string `json:"message"`
        Model   string `json:"model,omitempty"`
    }

    if err := json.NewDecoder(r.Body).Decode(&request); err != nil {
        http.Error(w, "Invalid request", http.StatusBadRequest)
        return
    }

    model := request.Model
    if model == "" {
        model = "meta-llama/llama-3.1-8b-instruct:free"
    }

    resp, err := client.CreateChatCompletion(
        r.Context(),
        openrouter.ChatCompletionRequest{
            Model: model,
            Messages: []openrouter.ChatCompletionMessage{
                {
                    Role:    openrouter.ChatMessageRoleUser,
                    Content: openrouter.Content{Text: request.Message},
                },
            },
        },
    )

    if err != nil {
        http.Error(w, err.Error(), http.StatusInternalServerError)
        return
    }

    response := map[string]string{
        "reply": resp.Choices[0].Message.Content,
    }

    w.Header().Set("Content-Type", "application/json")
    json.NewEncoder(w).Encode(response)
}
```

### CLI Tool Example

```go
func main() {
    if len(os.Args) < 2 {
        fmt.Println("Usage: go-openrouter-cli \"your message here\"")
        os.Exit(1)
    }

    apiKey := os.Getenv("OPENROUTER_API_KEY")
    if apiKey == "" {
        fmt.Println("Error: OPENROUTER_API_KEY environment variable not set")
        os.Exit(1)
    }

    client := openrouter.NewClient(apiKey)

    resp, err := client.CreateChatCompletion(
        context.Background(),
        openrouter.ChatCompletionRequest{
            Model: "meta-llama/llama-3.1-8b-instruct:free",
            Messages: []openrouter.ChatCompletionMessage{
                {
                    Role:    openrouter.ChatMessageRoleUser,
                    Content: openrouter.Content{Text: strings.Join(os.Args[1:], " ")},
                },
            },
        },
    )

    if err != nil {
        fmt.Printf("Error: %v\n", err)
        os.Exit(1)
    }

    fmt.Println(resp.Choices[0].Message.Content)
}
```

## Testing

### Unit Testing

```go
func TestChatCompletion(t *testing.T) {
    // Mock client for testing
    client := openrouter.NewClient("test-key")

    req := openrouter.ChatCompletionRequest{
        Model: "meta-llama/llama-3.1-8b-instruct:free",
        Messages: []openrouter.ChatCompletionMessage{
            {
                Role:    openrouter.ChatMessageRoleUser,
                Content: openrouter.Content{Text: "Hello"},
            },
        },
    }

    // Test the request structure
    if req.Model != "meta-llama/llama-3.1-8b-instruct:free" {
        t.Errorf("Expected model to be set correctly")
    }

    if len(req.Messages) != 1 {
        t.Errorf("Expected exactly one message")
    }
}
```

### Integration Testing

```go
func TestRealAPI(t *testing.T) {
    if testing.Short() {
        t.Skip("Skipping integration test in short mode")
    }

    apiKey := os.Getenv("OPENROUTER_API_KEY")
    if apiKey == "" {
        t.Skip("OPENROUTER_API_KEY not set for integration test")
    }

    client := openrouter.NewClient(apiKey)

    resp, err := client.CreateChatCompletion(
        context.Background(),
        openrouter.ChatCompletionRequest{
            Model: "meta-llama/llama-3.1-8b-instruct:free",
            Messages: []openrouter.ChatCompletionMessage{
                {
                    Role:    openrouter.ChatMessageRoleUser,
                    Content: openrouter.Content{Text: "Say 'test response'"},
                },
            },
        },
    )

    if err != nil {
        t.Fatalf("API request failed: %v", err)
    }

    if resp.Choices[0].Message.Content == "" {
        t.Error("Expected non-empty response")
    }
}
```

## Resources

- [OpenRouter Documentation](https://openrouter.ai/docs)
- [OpenRouter Model List](https://openrouter.ai/models)
- [Go OpenRouter GitHub Repository](https://github.com/revrost/go-openrouter)
- [OpenRouter Pricing](https://openrouter.ai/pricing)
- [OpenRouter API Reference](https://openrouter.ai/docs/quick-start)