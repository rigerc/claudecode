# Integration Patterns - Error Handling & Deployment

## Overview

This guide covers comprehensive error handling strategies and common integration patterns for deploying Go OpenAI applications.

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

## Related Guides

- [Getting Started](getting-started.md) - Initial setup and configuration
- [Best Practices](best-practices.md) - Model selection and cost optimization