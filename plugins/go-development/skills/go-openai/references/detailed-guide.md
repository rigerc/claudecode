---
name: go-openai
description: This skill should be used when working with the go-openai library for OpenAI API integration in Go applications. Use it for setting up API clients, implementing chat completions, text completions, function calling, image generation, audio processing, embeddings, fine-tuning, and building comprehensive AI-powered applications.
---

# Go OpenAI

## Overview

This skill enables developers to integrate OpenAI's powerful AI models into Go applications using the go-openai library, providing comprehensive access to GPT models, DALL-E image generation, Whisper audio processing, embeddings, and fine-tuning capabilities.

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

## Core Capabilities

### 1. Chat Completions

#### Simple Chat Request
```go
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

#### Streaming Chat Response
```go
req := openai.ChatCompletionRequest{
    Model: openai.GPT3Dot5Turbo,
    MaxTokens: 20,
    Messages: []openai.ChatCompletionMessage{
        {
            Role:    openai.ChatMessageRoleUser,
            Content: "Tell me a story",
        },
    },
    Stream: true,
}

stream, err := client.CreateChatCompletionStream(ctx, req)
if err != nil {
    fmt.Printf("ChatCompletionStream error: %v\n", err)
    return
}
defer stream.Close()

for {
    response, err := stream.Recv()
    if errors.Is(err, io.EOF) {
        fmt.Println("\nStream finished")
        return
    }

    if err != nil {
        fmt.Printf("\nStream error: %v\n", err)
        return
    }

    fmt.Printf(response.Choices[0].Delta.Content)
}
```

#### Conversational Context Management
```go
messages := make([]openai.ChatCompletionMessage, 0)

// Add system message
messages = append(messages, openai.ChatCompletionMessage{
    Role:    openai.ChatMessageRoleSystem,
    Content: "You are a helpful assistant.",
})

// Function to continue conversation
func continueConversation(userInput string) {
    // Add user message
    messages = append(messages, openai.ChatCompletionMessage{
        Role:    openai.ChatMessageRoleUser,
        Content: userInput,
    })

    resp, err := client.CreateChatCompletion(
        context.Background(),
        openai.ChatCompletionRequest{
            Model:    openai.GPT3Dot5Turbo,
            Messages: messages,
        },
    )

    if err != nil {
        fmt.Printf("Error: %v\n", err)
        return
    }

    assistantResponse := resp.Choices[0].Message.Content

    // Add assistant response to maintain context
    messages = append(messages, openai.ChatCompletionMessage{
        Role:    openai.ChatMessageRoleAssistant,
        Content: assistantResponse,
    })

    fmt.Printf("Assistant: %s\n", assistantResponse)
}
```

### 2. Function Calling

#### Define Function Schema
```go
funcDef := &openai.FunctionDefinition{
    Name:        "get_current_weather",
    Description: "Get the current weather in a given location",
    Parameters: map[string]interface{}{
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
```

#### Implement Function Calling
```go
resp, err := client.CreateChatCompletion(
    context.Background(),
    openai.ChatCompletionRequest{
        Model: openai.GPT4,
        Messages: []openai.ChatCompletionMessage{
            {
                Role:    openai.ChatMessageRoleUser,
                Content: "What's the weather like in Boston?",
            },
        },
        Functions: []openai.FunctionDefinition{*funcDef},
        FunctionCall: "auto",
    },
)

if err != nil {
    fmt.Printf("ChatCompletion error: %v\n", err)
    return
}

// Check if model wants to call a function
if resp.Choices[0].FinishReason == "function_call" {
    functionName := resp.Choices[0].Message.FunctionCall.Name
    arguments := resp.Choices[0].Message.FunctionCall.Arguments

    fmt.Printf("Function call: %s\n", functionName)
    fmt.Printf("Arguments: %s\n", arguments)

    // Parse arguments and call your actual function
    // Then send the result back to the model
}
```

### 3. Structured Output

```go
type Result struct {
    Steps []struct {
        Explanation string `json:"explanation"`
        Output      string `json:"output"`
    } `json:"steps"`
    FinalAnswer string `json:"final_answer"`
}

var result Result
schema, err := jsonschema.GenerateSchemaForType(result)
if err != nil {
    log.Fatalf("GenerateSchemaForType error: %v", err)
}

resp, err := client.CreateChatCompletion(ctx, openai.ChatCompletionRequest{
    Model: openai.GPT4oMini,
    Messages: []openai.ChatCompletionMessage{
        {
            Role:    openai.ChatMessageRoleUser,
            Content: "how can I solve 8x + 7 = -23",
        },
    },
    ResponseFormat: &openai.ChatCompletionResponseFormat{
        Type: openai.ChatCompletionResponseFormatTypeJSONSchema,
        JSONSchema: &openai.ChatCompletionResponseFormatJSONSchema{
            Name:   "math_reasoning",
            Schema: schema,
            Strict: true,
        },
    },
})

err = schema.Unmarshal(resp.Choices[0].Message.Content, &result)
if err != nil {
    log.Fatalf("Unmarshal schema error: %v", err)
}
fmt.Println(result)
```

### 4. Image Generation

#### DALL-E 2 Image Generation
```go
req := openai.ImageRequest{
    Prompt:         "Parrot on a skateboard performs a trick, cartoon style, natural light, high detail",
    Size:           openai.CreateImageSize256x256,
    ResponseFormat: openai.CreateImageResponseFormatURL,
    N:              1,
}

resp, err := client.CreateImage(ctx, req)
if err != nil {
    fmt.Printf("Image creation error: %v\n", err)
    return
}

fmt.Println(resp.Data[0].URL)
```

#### DALL-E 3 / GPT Image Generation
```go
req := openai.ImageRequest{
    Prompt:            "Parrot on a skateboard performing a trick. Large bold text \"SKATE MASTER\" banner at the bottom.",
    Background:        openai.CreateImageBackgroundOpaque,
    Model:             openai.CreateImageModelGptImage1,
    Size:              openai.CreateImageSize1024x1024,
    N:                 1,
    Quality:           openai.CreateImageQualityLow,
    OutputCompression: 100,
    OutputFormat:      openai.CreateImageOutputFormatJPEG,
}

resp, err := client.CreateImage(ctx, req)
if err != nil {
    fmt.Printf("Image creation error: %v\n", err)
    return
}

// Decode base64 image
imgBytes, err := base64.StdEncoding.DecodeString(resp.Data[0].B64JSON)
if err != nil {
    fmt.Printf("Base64 decode error: %v\n", err)
    return
}

// Save to file
err = os.WriteFile("generated_image.jpg", imgBytes, 0644)
if err != nil {
    fmt.Printf("Failed to write image file: %v\n", err)
    return
}
```

### 5. Audio Processing

#### Speech-to-Text Transcription
```go
req := openai.AudioRequest{
    Model:    openai.Whisper1,
    FilePath: "recording.mp3",
}

resp, err := client.CreateTranscription(ctx, req)
if err != nil {
    fmt.Printf("Transcription error: %v\n", err)
    return
}

fmt.Println(resp.Text)
```

#### Generate SRT Captions
```go
req := openai.AudioRequest{
    Model:    openai.Whisper1,
    FilePath: "audio.mp3",
    Format:   openai.AudioResponseFormatSRT,
}

resp, err := client.CreateTranscription(context.Background(), req)
if err != nil {
    fmt.Printf("Transcription error: %v\n", err)
    return
}

// Save SRT captions
f, err := os.Create("audio.srt")
if err != nil {
    fmt.Printf("Could not open file: %v\n", err)
    return
}
defer f.Close()

if _, err := f.WriteString(resp.Text); err != nil {
    fmt.Printf("Error writing to file: %v\n", err)
    return
}
```

### 6. Embeddings

#### Create Text Embeddings
```go
req := openai.EmbeddingRequest{
    Input: []string{"The quick brown fox jumps over the lazy dog"},
    Model: openai.AdaEmbeddingV2,
}

resp, err := client.CreateEmbeddings(context.Background(), req)
if err != nil {
    fmt.Printf("CreateEmbeddings error: %v\n", err)
    return
}

embeddings := resp.Data[0].Embedding // []float32 with 1536 dimensions
fmt.Printf("Embedding dimensions: %d\n", len(embeddings))
```

#### Calculate Similarity
```go
// Create embeddings for two texts
queryReq := openai.EmbeddingRequest{
    Input: []string{"What is the capital of France?"},
    Model: openai.AdaEmbeddingV2,
}

targetReq := openai.EmbeddingRequest{
    Input: []string{"Paris is the capital city of France"},
    Model: openai.AdaEmbeddingV2,
}

queryResp, _ := client.CreateEmbeddings(context.Background(), queryReq)
targetResp, _ := client.CreateEmbeddings(context.Background(), targetReq)

// Calculate similarity (dot product)
queryEmbedding := queryResp.Data[0]
targetEmbedding := targetResp.Data[0]

similarity, err := queryEmbedding.DotProduct(&targetEmbedding)
if err != nil {
    log.Fatal("Error calculating dot product:", err)
}

fmt.Printf("Similarity score: %f\n", similarity)
```

### 7. Fine-tuning

#### Upload Training Data
```go
file, err := client.CreateFile(ctx, openai.FileRequest{
    FilePath: "training_data.jsonl",
    Purpose:  "fine-tune",
})
if err != nil {
    fmt.Printf("Upload file error: %v\n", err)
    return
}

fmt.Printf("File uploaded with ID: %s\n", file.ID)
```

#### Create Fine-tuning Job
```go
fineTuningJob, err := client.CreateFineTuningJob(ctx, openai.FineTuningJobRequest{
    TrainingFile: file.ID,
    Model:        "davinci-002", // or "gpt-3.5-turbo-0613", "babbage-002"
})
if err != nil {
    fmt.Printf("Creating fine-tuning job error: %v\n", err)
    return
}

fmt.Printf("Fine-tuning job created with ID: %s\n", fineTuningJob.ID)
```

#### Check Fine-tuning Status
```go
job, err := client.RetrieveFineTuningJob(ctx, fineTuningJob.ID)
if err != nil {
    fmt.Printf("Retrieving fine-tuning job error: %v\n", err)
    return
}

fmt.Printf("Job status: %s\n", job.Status)
if job.FineTunedModel != "" {
    fmt.Printf("Fine-tuned model: %s\n", job.FineTunedModel)
}
```

### 8. Configuration and Deployment

#### Azure OpenAI Integration
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

#### Proxy Configuration
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

## Error Handling

### Comprehensive Error Handling
```go
resp, err := client.CreateChatCompletion(ctx, req)
if err != nil {
    // Check for specific API errors
    apiErr := &openai.APIError{}
    if errors.As(err, &apiErr) {
        switch apiErr.HTTPStatusCode {
        case 401:
            fmt.Println("Invalid authentication or API key")
        case 429:
            fmt.Println("Rate limit exceeded. Please wait and retry")
        case 500:
            fmt.Println("OpenAI server error. Please retry")
        default:
            fmt.Printf("API error: %v\n", apiErr)
        }
        return
    }

    // Handle other errors
    fmt.Printf("Error: %v\n", err)
    return
}
```

### Temperature Workaround
```go
import "math"

req := openai.ChatCompletionRequest{
    Model:      openai.GPT3Dot5Turbo,
    Messages:   messages,
    Temperature: math.SmallestNonzeroFloat32, // Mimics temperature 0
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
        Stream  bool   `json:"stream,omitempty"`
        Model   string `json:"model,omitempty"`
    }

    if err := json.NewDecoder(r.Body).Decode(&request); err != nil {
        http.Error(w, "Invalid request", http.StatusBadRequest)
        return
    }

    model := openai.GPT3Dot5Turbo
    if request.Model != "" {
        model = request.Model
    }

    if request.Stream {
        // Handle streaming response
        stream := client.CreateChatCompletionStream(r.Context(), openai.ChatCompletionRequest{
            Model: model,
            Messages: []openai.ChatCompletionMessage{
                {
                    Role:    openai.ChatMessageRoleUser,
                    Content: request.Message,
                },
            },
            Stream: true,
        })

        w.Header().Set("Content-Type", "text/plain")
        for {
            response, err := stream.Recv()
            if errors.Is(err, io.EOF) {
                return
            }
            if err != nil {
                http.Error(w, err.Error(), http.StatusInternalServerError)
                return
            }
            fmt.Fprint(w, response.Choices[0].Delta.Content)
            flusher, _ := w.(http.Flusher)
            flusher.Flush()
        }
    } else {
        // Handle regular response
        resp, err := client.CreateChatCompletion(r.Context(), openai.ChatCompletionRequest{
            Model: model,
            Messages: []openai.ChatCompletionMessage{
                {
                    Role:    openai.ChatMessageRoleUser,
                    Content: request.Message,
                },
            },
        })

        if err != nil {
            http.Error(w, err.Error(), http.StatusInternalServerError)
            return
        }

        response := map[string]interface{}{
            "reply":   resp.Choices[0].Message.Content,
            "usage":   resp.Usage,
            "model":   resp.Model,
        }

        w.Header().Set("Content-Type", "application/json")
        json.NewEncoder(w).Encode(response)
    }
}
```

### CLI Tool Integration
```go
func main() {
    if len(os.Args) < 2 {
        fmt.Println("Usage: go-openai-cli \"your message here\"")
        os.Exit(1)
    }

    apiKey := os.Getenv("OPENAI_API_KEY")
    if apiKey == "" {
        fmt.Println("Error: OPENAI_API_KEY environment variable not set")
        os.Exit(1)
    }

    client := openai.NewClient(apiKey)

    resp, err := client.CreateChatCompletion(
        context.Background(),
        openai.ChatCompletionRequest{
            Model: openai.GPT3Dot5Turbo,
            Messages: []openai.ChatCompletionMessage{
                {
                    Role:    openai.ChatMessageRoleUser,
                    Content: strings.Join(os.Args[1:], " "),
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

### Model Selection
```go
func getModelForTask(taskType string) string {
    switch taskType {
    case "simple_qa":
        return openai.GPT3Dot5Turbo
    case "complex_reasoning":
        return openai.GPT4
    case "code_generation":
        return openai.GPT4
    case "cost_sensitive":
        return openai.GPT3Dot5Turbo
    default:
        return openai.GPT3Dot5Turbo
    }
}
```

### Cost Optimization
```go
// Monitor token usage
func trackUsage(resp *openai.ChatCompletionResponse) {
    if resp.Usage != nil {
        fmt.Printf("Tokens used: %d (prompt: %d, completion: %d)\n",
            resp.Usage.TotalTokens,
            resp.Usage.PromptTokens,
            resp.Usage.CompletionTokens)
    }
}

// Set appropriate limits
func getOptimalMaxTokens(taskType string) int {
    switch taskType {
    case "short_answer":
        return 150
    case "medium_answer":
        return 500
    case "long_answer":
        return 2000
    default:
        return 1000
    }
}
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
