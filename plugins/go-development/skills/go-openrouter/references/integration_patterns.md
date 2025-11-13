# Integration Patterns

Common integration patterns for web servers, CLI tools, and applications.

## Web Server Integration

### REST API Handler

```go
package main

import (
    "encoding/json"
    "net/http"
    "os"

    openrouter "github.com/revrost/go-openrouter"
)

var client *openrouter.Client

func init() {
    client = openrouter.NewClient(os.Getenv("OPENROUTER_API_KEY"))
}

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

func main() {
    http.HandleFunc("/chat", chatHandler)
    http.ListenAndServe(":8080", nil)
}
```

### Middleware Pattern

```go
func openRouterMiddleware(apiKey string) func(http.Handler) http.Handler {
    client := openrouter.NewClient(apiKey)

    return func(next http.Handler) http.Handler {
        return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
            // Add client to context
            ctx := context.WithValue(r.Context(), "openrouter", client)
            next.ServeHTTP(w, r.WithContext(ctx))
        })
    }
}

// Usage
func handler(w http.ResponseWriter, r *http.Request) {
    client := r.Context().Value("openrouter").(*openrouter.Client)
    // Use client...
}

func main() {
    mux := http.NewServeMux()
    mux.HandleFunc("/chat", handler)

    wrapped := openRouterMiddleware(os.Getenv("OPENROUTER_API_KEY"))(mux)
    http.ListenAndServe(":8080", wrapped)
}
```

## CLI Tool Integration

### Basic CLI

```go
package main

import (
    "context"
    "fmt"
    "os"
    "strings"

    openrouter "github.com/revrost/go-openrouter"
)

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

### Interactive CLI with urfave/cli

```go
package main

import (
    "context"
    "fmt"
    "os"

    openrouter "github.com/revrost/go-openrouter"
    "github.com/urfave/cli/v2"
)

func main() {
    var model string
    var stream bool

    app := &cli.App{
        Name:  "openrouter-cli",
        Usage: "Chat with AI models via OpenRouter",
        Flags: []cli.Flag{
            &cli.StringFlag{
                Name:        "model",
                Aliases:     []string{"m"},
                Value:       "meta-llama/llama-3.1-8b-instruct:free",
                Usage:       "Model to use",
                Destination: &model,
            },
            &cli.BoolFlag{
                Name:        "stream",
                Aliases:     []string{"s"},
                Usage:       "Stream response",
                Destination: &stream,
            },
        },
        Action: func(c *cli.Context) error {
            if c.Args().Len() == 0 {
                return fmt.Errorf("please provide a message")
            }

            apiKey := os.Getenv("OPENROUTER_API_KEY")
            if apiKey == "" {
                return fmt.Errorf("OPENROUTER_API_KEY not set")
            }

            client := openrouter.NewClient(apiKey)
            message := c.Args().First()

            if stream {
                return streamChat(client, model, message)
            }

            return regularChat(client, model, message)
        },
    }

    if err := app.Run(os.Args); err != nil {
        fmt.Fprintln(os.Stderr, err)
        os.Exit(1)
    }
}

func regularChat(client *openrouter.Client, model, message string) error {
    resp, err := client.CreateChatCompletion(
        context.Background(),
        openrouter.ChatCompletionRequest{
            Model: model,
            Messages: []openrouter.ChatCompletionMessage{
                {
                    Role:    openrouter.ChatMessageRoleUser,
                    Content: openrouter.Content{Text: message},
                },
            },
        },
    )

    if err != nil {
        return err
    }

    fmt.Println(resp.Choices[0].Message.Content)
    return nil
}

func streamChat(client *openrouter.Client, model, message string) error {
    stream, err := client.CreateChatCompletionStream(
        context.Background(),
        openrouter.ChatCompletionRequest{
            Model: model,
            Messages: []openrouter.ChatCompletionMessage{
                {
                    Role:    openrouter.ChatMessageRoleUser,
                    Content: openrouter.Content{Text: message},
                },
            },
            Stream: true,
        },
    )

    if err != nil {
        return err
    }
    defer stream.Close()

    for {
        response, err := stream.Recv()
        if err == io.EOF {
            fmt.Println()
            return nil
        }
        if err != nil {
            return err
        }

        if len(response.Choices) > 0 {
            fmt.Print(response.Choices[0].Delta.Content)
        }
    }
}
```

## Service Layer Pattern

### Chat Service

```go
package service

import (
    "context"
    "fmt"
    "sync"

    openrouter "github.com/revrost/go-openrouter"
)

type ChatService struct {
    client       *openrouter.Client
    defaultModel string
    mu           sync.RWMutex
    sessions     map[string][]openrouter.ChatCompletionMessage
}

func NewChatService(apiKey, defaultModel string) *ChatService {
    return &ChatService{
        client:       openrouter.NewClient(apiKey),
        defaultModel: defaultModel,
        sessions:     make(map[string][]openrouter.ChatCompletionMessage),
    }
}

func (s *ChatService) Chat(ctx context.Context, sessionID, message string) (string, error) {
    s.mu.Lock()
    messages := s.sessions[sessionID]
    messages = append(messages, openrouter.ChatCompletionMessage{
        Role:    openrouter.ChatMessageRoleUser,
        Content: openrouter.Content{Text: message},
    })
    s.sessions[sessionID] = messages
    s.mu.Unlock()

    resp, err := s.client.CreateChatCompletion(
        ctx,
        openrouter.ChatCompletionRequest{
            Model:    s.defaultModel,
            Messages: messages,
        },
    )

    if err != nil {
        return "", err
    }

    reply := resp.Choices[0].Message.Content

    s.mu.Lock()
    s.sessions[sessionID] = append(messages, openrouter.ChatCompletionMessage{
        Role:    openrouter.ChatMessageRoleAssistant,
        Content: openrouter.Content{Text: reply},
    })
    s.mu.Unlock()

    return reply, nil
}

func (s *ChatService) ClearSession(sessionID string) {
    s.mu.Lock()
    defer s.mu.Unlock()
    delete(s.sessions, sessionID)
}
```

## Worker Pool Pattern

```go
type Job struct {
    ID      string
    Prompt  string
    Model   string
    Result  chan Result
}

type Result struct {
    ID       string
    Response string
    Error    error
}

type Worker struct {
    client *openrouter.Client
    jobs   <-chan Job
}

func NewWorker(client *openrouter.Client, jobs <-chan Job) *Worker {
    return &Worker{
        client: client,
        jobs:   jobs,
    }
}

func (w *Worker) Start(ctx context.Context) {
    for {
        select {
        case <-ctx.Done():
            return
        case job := <-w.jobs:
            w.processJob(ctx, job)
        }
    }
}

func (w *Worker) processJob(ctx context.Context, job Job) {
    resp, err := w.client.CreateChatCompletion(
        ctx,
        openrouter.ChatCompletionRequest{
            Model: job.Model,
            Messages: []openrouter.ChatCompletionMessage{
                {
                    Role:    openrouter.ChatMessageRoleUser,
                    Content: openrouter.Content{Text: job.Prompt},
                },
            },
        },
    )

    result := Result{ID: job.ID}
    if err != nil {
        result.Error = err
    } else {
        result.Response = resp.Choices[0].Message.Content
    }

    job.Result <- result
}

// Usage
func main() {
    client := openrouter.NewClient(os.Getenv("OPENROUTER_API_KEY"))
    jobs := make(chan Job, 100)

    // Start workers
    ctx := context.Background()
    for i := 0; i < 5; i++ {
        worker := NewWorker(client, jobs)
        go worker.Start(ctx)
    }

    // Submit jobs
    // ...
}
```

## Best Practices

1. **Singleton client**: Create one client instance and reuse it
2. **Context propagation**: Pass context through all layers
3. **Graceful shutdown**: Handle cleanup properly
4. **Configuration management**: Externalize configuration
5. **Session management**: Track conversation history
6. **Error handling**: Implement comprehensive error handling
7. **Logging**: Add structured logging
8. **Metrics**: Track performance and usage
9. **Rate limiting**: Implement client-side rate limiting
10. **Testing**: Write unit and integration tests
