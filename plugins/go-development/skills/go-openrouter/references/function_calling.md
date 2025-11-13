# Function Calling and Structured Output

Guide to implementing function calling and structured outputs with OpenRouter.

## Function Calling

### Define Function Schema

```go
import "github.com/invopop/jsonschema"

funcDef := &openrouter.FunctionDefinition{
    Name:        "get_current_weather",
    Description: "Get the current weather for a location",
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

### Use Function Calling

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

    // Parse arguments
    var args map[string]interface{}
    json.Unmarshal([]byte(arguments), &args)

    // Call your actual function
    result := getWeather(args["location"].(string), args["unit"].(string))

    // Send result back to model
    followUpResp, _ := client.CreateChatCompletion(
        context.Background(),
        openrouter.ChatCompletionRequest{
            Model: "anthropic/claude-3-haiku",
            Messages: append(resp.Messages, openrouter.ChatCompletionMessage{
                Role:    openrouter.ChatMessageRoleFunction,
                Name:    functionName,
                Content: openrouter.Content{Text: result},
            }),
        },
    )
}
```

### Multiple Function Definitions

```go
weatherFunc := openrouter.FunctionDefinition{
    Name: "get_weather",
    Parameters: jsonschema.Definition{
        Type: jsonschema.Object,
        Properties: map[string]jsonschema.Definition{
            "location": {Type: jsonschema.String},
        },
        Required: []string{"location"},
    },
}

newsFunc := openrouter.FunctionDefinition{
    Name: "get_news",
    Parameters: jsonschema.Definition{
        Type: jsonschema.Object,
        Properties: map[string]jsonschema.Definition{
            "topic": {Type: jsonschema.String},
        },
        Required: []string{"topic"},
    },
}

resp, err := client.CreateChatCompletion(
    context.Background(),
    openrouter.ChatCompletionRequest{
        Model:        "anthropic/claude-3-haiku",
        Messages:     messages,
        Functions:    []openrouter.FunctionDefinition{weatherFunc, newsFunc},
        FunctionCall: "auto",
    },
)
```

## Structured Output

### Define Output Schema

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
    return err
}
```

### Request with Structured Output

```go
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

resp, err := client.CreateChatCompletion(context.Background(), request)
if err != nil {
    return err
}

// Parse structured response
var weatherData WeatherResult
json.Unmarshal([]byte(resp.Choices[0].Message.Content), &weatherData)
```

### Complex Structured Output

```go
type Task struct {
    ID          string   `json:"id"`
    Title       string   `json:"title"`
    Description string   `json:"description"`
    Priority    string   `json:"priority"`
    Tags        []string `json:"tags"`
    DueDate     string   `json:"due_date"`
}

type TaskList struct {
    Tasks      []Task `json:"tasks"`
    TotalCount int    `json:"total_count"`
}

var taskList TaskList
schema, _ := jsonschema.GenerateSchemaForType(taskList)

request := openrouter.ChatCompletionRequest{
    Model: openrouter.DeepseekV3,
    Messages: []openrouter.ChatCompletionMessage{
        {
            Role: openrouter.ChatMessageRoleUser,
            Content: openrouter.Content{
                Text: "Create a task list for planning a conference",
            },
        },
    },
    ResponseFormat: &openrouter.ChatCompletionResponseFormat{
        Type: openrouter.ChatCompletionResponseFormatTypeJSONSchema,
        JSONSchema: &openrouter.ChatCompletionResponseFormatJSONSchema{
            Name:   "task_list",
            Schema: schema,
            Strict: true,
        },
    },
}
```

## Best Practices

1. **Clear function descriptions**: Help the model understand when to call functions
2. **Validate function arguments**: Always validate parsed arguments before use
3. **Handle missing functions**: Check for undefined function calls
4. **Use strict mode**: Enable strict schema validation for structured outputs
5. **Error handling**: Handle parsing errors gracefully
6. **Type safety**: Use Go structs with proper JSON tags for structured outputs
