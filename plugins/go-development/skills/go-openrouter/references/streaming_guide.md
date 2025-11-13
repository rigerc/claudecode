# Streaming Response Guide

Guide to implementing streaming responses for real-time chat applications.

## Basic Streaming

### Creating a Stream

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
```

### Processing Stream Data

```go
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

## Advanced Streaming Patterns

### Streaming with Context Cancellation

```go
ctx, cancel := context.WithTimeout(context.Background(), 30*time.Second)
defer cancel()

stream, err := client.CreateChatCompletionStream(ctx, request)
if err != nil {
    return err
}
defer stream.Close()

for {
    select {
    case <-ctx.Done():
        return ctx.Err()
    default:
        response, err := stream.Recv()
        if errors.Is(err, io.EOF) {
            return nil
        }
        if err != nil {
            return err
        }
        // Process response
    }
}
```

### Streaming to HTTP Response

```go
func streamHandler(w http.ResponseWriter, r *http.Request) {
    // Set headers for SSE (Server-Sent Events)
    w.Header().Set("Content-Type", "text/event-stream")
    w.Header().Set("Cache-Control", "no-cache")
    w.Header().Set("Connection", "keep-alive")

    flusher, ok := w.(http.Flusher)
    if !ok {
        http.Error(w, "Streaming unsupported", http.StatusInternalServerError)
        return
    }

    stream, err := client.CreateChatCompletionStream(
        r.Context(),
        openrouter.ChatCompletionRequest{
            Model: "meta-llama/llama-3.1-8b-instruct:free",
            Messages: []openrouter.ChatCompletionMessage{
                {
                    Role:    openrouter.ChatMessageRoleUser,
                    Content: openrouter.Content{Text: "Hello!"},
                },
            },
            Stream: true,
        },
    )

    if err != nil {
        http.Error(w, err.Error(), http.StatusInternalServerError)
        return
    }
    defer stream.Close()

    for {
        response, err := stream.Recv()
        if errors.Is(err, io.EOF) {
            fmt.Fprintf(w, "data: [DONE]\n\n")
            flusher.Flush()
            return
        }
        if err != nil {
            fmt.Fprintf(w, "data: {\"error\": \"%s\"}\n\n", err.Error())
            flusher.Flush()
            return
        }

        if len(response.Choices) > 0 {
            data, _ := json.Marshal(response)
            fmt.Fprintf(w, "data: %s\n\n", data)
            flusher.Flush()
        }
    }
}
```

### Streaming with Buffer

```go
type StreamBuffer struct {
    buffer  strings.Builder
    mu      sync.Mutex
}

func (sb *StreamBuffer) Write(s string) {
    sb.mu.Lock()
    defer sb.mu.Unlock()
    sb.buffer.WriteString(s)
}

func (sb *StreamBuffer) String() string {
    sb.mu.Lock()
    defer sb.mu.Unlock()
    return sb.buffer.String()
}

func streamWithBuffer(client *openrouter.Client, req openrouter.ChatCompletionRequest) (string, error) {
    stream, err := client.CreateChatCompletionStream(context.Background(), req)
    if err != nil {
        return "", err
    }
    defer stream.Close()

    var buffer StreamBuffer

    for {
        response, err := stream.Recv()
        if errors.Is(err, io.EOF) {
            return buffer.String(), nil
        }
        if err != nil {
            return "", err
        }

        if len(response.Choices) > 0 {
            buffer.Write(response.Choices[0].Delta.Content)
        }
    }
}
```

## Best Practices

1. **Always close streams**: Use `defer stream.Close()` to ensure proper cleanup
2. **Handle io.EOF properly**: It signals normal stream completion
3. **Use context cancellation**: Implement timeouts and cancellation for long-running streams
4. **Buffer management**: For UI applications, consider buffering to smooth out rendering
5. **Error recovery**: Implement retry logic for transient network errors
6. **Rate limiting**: Be mindful of rate limits when creating multiple concurrent streams
