# OpenRouter API Reference

Complete API documentation for the OpenRouter Go client library.

## Client Initialization

### Basic Client Setup

```go
import openrouter "github.com/revrost/go-openrouter"

// Initialize with API key
client := openrouter.NewClient("your-openrouter-api-key")

// Or with environment variable
client := openrouter.NewClient(os.Getenv("OPENROUTER_API_KEY"))
```

### Client Configuration Options

```go
client := openrouter.NewClient(
    "your-api-key",
    openrouter.WithXTitle("My App"),           // App name for analytics
    openrouter.WithHTTPReferer("https://myapp.com"), // App URL
)
```

## Chat Completion Request

### Basic Request Structure

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

### Request Parameters

- `Model` (string): The model ID to use (e.g., "deepseek/deepseek-chat-v3-0324:free")
- `Messages` ([]ChatCompletionMessage): Array of conversation messages
- `MaxTokens` (int, optional): Maximum tokens to generate
- `Temperature` (float64, optional): Sampling temperature (0-2)
- `TopP` (float64, optional): Nucleus sampling threshold
- `N` (int, optional): Number of completions to generate
- `Stream` (bool, optional): Enable streaming response
- `Stop` ([]string, optional): Stop sequences
- `PresencePenalty` (float64, optional): Penalty for new tokens
- `FrequencyPenalty` (float64, optional): Penalty for frequent tokens
- `Functions` ([]FunctionDefinition, optional): Available functions for calling
- `FunctionCall` (string/object, optional): Function calling behavior
- `ResponseFormat` (ChatCompletionResponseFormat, optional): Structured output format

### Response Structure

```go
type ChatCompletionResponse struct {
    ID      string                   `json:"id"`
    Object  string                   `json:"object"`
    Created int64                    `json:"created"`
    Model   string                   `json:"model"`
    Choices []ChatCompletionChoice   `json:"choices"`
    Usage   *Usage                   `json:"usage,omitempty"`
}

type ChatCompletionChoice struct {
    Index        int                      `json:"index"`
    Message      ChatCompletionMessage    `json:"message"`
    FinishReason string                   `json:"finish_reason"`
}

type Usage struct {
    PromptTokens     int `json:"prompt_tokens"`
    CompletionTokens int `json:"completion_tokens"`
    TotalTokens      int `json:"total_tokens"`
}
```

## Message Types

### User Message

```go
openrouter.ChatCompletionMessage{
    Role:    openrouter.ChatMessageRoleUser,
    Content: openrouter.Content{Text: "Your question here"},
}
```

### Assistant Message

```go
openrouter.ChatCompletionMessage{
    Role:    openrouter.ChatMessageRoleAssistant,
    Content: openrouter.Content{Text: "Assistant's response"},
}
```

### System Message

```go
openrouter.ChatCompletionMessage{
    Role:    openrouter.ChatMessageRoleSystem,
    Content: openrouter.Content{Text: "System instructions"},
}
```

## Environment Configuration

### Configuration Structure

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

## Token Usage Tracking

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

## Common Models

### Free Models
- `meta-llama/llama-3.1-8b-instruct:free`
- `deepseek/deepseek-chat-v3-0324:free`
- `qwen/qwen3-235b-a22b-07-25:free`

### Premium Models
- `anthropic/claude-3-5-sonnet`
- `openai/gpt-4o-mini`
- `meta-llama/llama-3.1-70b-instruct`

See `model_list.md` for a comprehensive list of available models.
