# Chat Completions, Function Calling & Structured Output

## Overview

This guide covers conversational AI capabilities using OpenAI's chat models, including function calling for external tool integration and structured output generation.

## 1. Chat Completions

### Simple Chat Request

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

### Streaming Chat Response

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

### Conversational Context Management

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

## 2. Function Calling

### Define Function Schema

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

### Implement Function Calling

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

## 3. Structured Output

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

## Related Guides

- [Getting Started](getting-started.md) - Initial setup and configuration
- [Integration Patterns](integration-patterns.md) - Error handling and deployment patterns
- [Best Practices](best-practices.md) - Model selection and optimization