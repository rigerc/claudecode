# go-openai Library Documentation

## Overview

The `go-openai` library is a Go client for the OpenAI API that provides convenient access to OpenAI's powerful AI models including GPT-3, GPT-4, DALL-E, and Whisper. This comprehensive library supports chat completions, text completions, image generation, audio transcription, embeddings, fine-tuning, and more.

## Installation

```bash
go get github.com/sashabaranov/go-openai
```

## Basic Usage

### Client Initialization

```go
package main

import (
    "context"
    "fmt"
    openai "github.com/sashabaranov/go-openai"
)

func main() {
    // Initialize client with API key
    client := openai.NewClient("your-openai-api-key")

    // Or use environment variable
    // client := openai.NewClient(os.Getenv("OPENAI_API_KEY"))
}
```

### Chat Completions

#### Simple Chat Completion

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

#### Streaming Chat Completion

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

#### Conversational Context

```go
messages := make([]openai.ChatCompletionMessage, 0)

// Add system message
messages = append(messages, openai.ChatCompletionMessage{
    Role:    openai.ChatMessageRoleSystem,
    Content: "You are a helpful assistant.",
})

// Add user message and get response
userInput := "What is the capital of France?"
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

// Add assistant response to maintain context
messages = append(messages, openai.ChatCompletionMessage{
    Role:    openai.ChatMessageRoleAssistant,
    Content: resp.Choices[0].Message.Content,
})
```

### Text Completions (Legacy)

```go
req := openai.CompletionRequest{
    Model:     openai.GPT3Babbage002,
    MaxTokens: 5,
    Prompt:    "Lorem ipsum",
}

resp, err := client.CreateCompletion(ctx, req)
if err != nil {
    fmt.Printf("Completion error: %v\n", err)
    return
}

fmt.Println(resp.Choices[0].Text)
```

### Function Calling

#### Define Function Schema

```go
// Using JSON schema
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

// Or using Go structs with jsonschema
funcDef := &openai.FunctionDefinition{
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

    // Parse arguments and call your function
    // Then send the result back to the model
}
```

### Structured Output with JSON Schema

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

## Advanced Features

### Image Generation

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
    Prompt:            "Parrot on a skateboard performing a trick. Large bold text \"SKATE MASTER\" banner at the bottom of the image. Cartoon style, natural light, high detail, 1:1 aspect ratio.",
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

### Audio Processing

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

### Embeddings

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

### Fine-tuning

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

## Configuration Options

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

### Azure OpenAI Integration

```go
config := openai.DefaultAzureConfig("your-azure-key", "https://your-resource.openai.azure.com/")

// Optional: Map model names to deployment names
config.AzureModelMapperFunc = func(model string) string {
    azureModelMapping := map[string]string{
        "gpt-3.5-turbo": "your-gpt35-deployment-name",
        "gpt-4":         "your-gpt4-deployment-name",
    }
    return azureModelMapping[model]
}

client := openai.NewClientWithConfig(config)
```

## Error Handling

### API Error Handling

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

For deterministic responses (temperature 0), use this workaround:

```go
import "math"

req := openai.ChatCompletionRequest{
    Model:      openai.GPT3Dot5Turbo,
    Messages:   messages,
    Temperature: math.SmallestNonzeroFloat32, // Mimics temperature 0
}
```

## Best Practices

1. **API Key Security**: Never expose your API key in code. Use environment variables or secure configuration management.

2. **Context Management**: Keep conversation context manageable by limiting message history or implementing summarization.

3. **Error Handling**: Always handle API errors gracefully, especially rate limiting (429) and server errors (500).

4. **Streaming**: Use streaming for long responses to improve user experience.

5. **Rate Limiting**: Implement exponential backoff for rate limit errors.

6. **Cost Management**: Monitor token usage and set reasonable limits for MaxTokens.

## Models Reference

### Chat Models
- `gpt-4` - Most capable model
- `gpt-4-turbo` - Faster version of GPT-4
- `gpt-3.5-turbo` - Fast and cost-effective
- `gpt-3.5-turbo-16k` - Larger context window

### Completion Models
- `text-davinci-003` - Most capable completion model
- `text-curie-001` - Fast and capable
- `text-babbage-002` - Capable and cheaper
- `text-ada-001` - Fastest and cheapest

### Embedding Models
- `text-embedding-ada-002` - General purpose embeddings

### Image Models
- `dall-e-3` - Latest image generation model
- `dall-e-2` - Previous generation image model

### Audio Models
- `whisper-1` - Speech-to-text model

## Resources

- [Official OpenAI API Documentation](https://platform.openai.com/docs)
- [Go OpenAI GitHub Repository](https://github.com/sashabaranov/go-openai)
- [OpenAI Playground](https://platform.openai.com/playground)
- [Pricing Information](https://openai.com/pricing)