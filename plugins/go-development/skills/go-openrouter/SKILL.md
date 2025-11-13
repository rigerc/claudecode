---
name: go-openrouter
description: This skill should be used when working with the OpenRouter Go client library for AI model integration. Use it for setting up API clients, implementing chat completions, streaming responses, function calling, structured outputs, and building AI-powered applications in Go.
---

# Go OpenRouter

## Overview

This skill enables developers to integrate OpenRouter's unified AI API into Go applications, providing access to hundreds of AI models from multiple providers through a single interface.

## Quick Start

### Basic Client Setup

Initialize the OpenRouter client with your API key:

```go
import (
    "context"
    openrouter "github.com/revrost/go-openrouter"
)

// Initialize with API key
client := openrouter.NewClient("your-openrouter-api-key")

// Or with environment variable
// client := openrouter.NewClient(os.Getenv("OPENROUTER_API_KEY"))
```

### Client Configuration

```go
client := openrouter.NewClient(
    "your-api-key",
    openrouter.WithXTitle("My App"),           // App name for analytics
    openrouter.WithHTTPReferer("https://myapp.com"), // App URL
)
```

## Core Capabilities

### 1. Chat Completions

#### Simple Chat Request
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

#### Streaming Chat Response
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

    if len(response.Choices) > 0 {
        fmt.Print(response.Choices[0].Delta.Content)
    }
}
```

### 2. Function Calling

#### Define Function Schema
```go
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

// Check if model wants to call a function
if len(resp.Choices) > 0 && resp.Choices[0].Message.FunctionCall != nil {
    functionName := resp.Choices[0].Message.FunctionCall.Name
    arguments := resp.Choices[0].Message.FunctionCall.Arguments

    // Parse arguments and call your actual function
    // Then send the result back to the model
}
```

### 3. Structured Output

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

request := openrouter.ChatCompletionRequest{
    Model: openrouter.DeepseekV3,
    Messages: []openrouter.ChatCompletionMessage{
        {
            Role:    openrouter.ChatMessageRoleUser,
            Content: openrouter.Content{Text: "What's the current weather like in London?"},
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
```

### 4. Error Handling and Retry Logic

#### Comprehensive Error Handling
```go
resp, err := client.CreateChatCompletion(ctx, req)
if err != nil {
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
    fmt.Printf("Request failed: %v\n", err)
    return
}
```

#### Retry with Exponential Backoff
```go
func createChatCompletionWithRetry(req openrouter.ChatCompletionRequest) (*openrouter.ChatCompletionResponse, error) {
    maxRetries := 3
    baseDelay := 1 * time.Second

    for attempt := 0; attempt < maxRetries; attempt++ {
        resp, err := client.CreateChatCompletion(context.Background(), req)

        if err == nil {
            return resp, nil
        }

        if apiErr, ok := err.(*openrouter.APIError); ok {
            if apiErr.HTTPStatusCode == 429 || apiErr.HTTPStatusCode >= 500 {
                if attempt < maxRetries-1 {
                    delay := baseDelay * time.Duration(1<<attempt)
                    time.Sleep(delay)
                    continue
                }
            }
        }
        return nil, err
    }
    return nil, fmt.Errorf("max retries exceeded")
}
```

### 5. Model Selection and Cost Optimization

#### Model Selection Strategy
```go
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

// Fallback strategy
func getChatResponse(messages []openrouter.ChatCompletionMessage) (string, error) {
    models := []string{
        "anthropic/claude-3-5-sonnet",
        "openai/gpt-4o-mini",
        "meta-llama/llama-3.1-8b-instruct:free",
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

## Integration Patterns

### Web Server Integration
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

### CLI Tool Integration
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

## Best Practices

### Environment Configuration
```go
type Config struct {
    APIKey       string
    AppName      string
    AppURL       string
    DefaultModel string
    MaxTokens    int
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
```

### Token Usage Tracking
```go
func trackUsage(resp *openrouter.ChatCompletionResponse) {
    if resp.Usage != nil {
        fmt.Printf("Tokens used: %d (prompt: %d, completion: %d)\n",
            resp.Usage.TotalTokens,
            resp.Usage.PromptTokens,
            resp.Usage.CompletionTokens)
    }
}
```

## Resources

### references/
- **api_reference.md** - Complete OpenRouter API documentation and model listings
- **model_list.md** - Comprehensive list of available models with capabilities
- **error_codes.md** - API error codes and handling strategies

### scripts/
- **client_setup.go** - Client initialization and configuration utilities
- **retry_handler.go** - Exponential backoff and retry logic
- **usage_tracker.go** - Token usage monitoring and cost tracking

### assets/
- **config_templates/** - Configuration file templates for different environments
- **example_projects/** - Complete example applications demonstrating integration patterns
