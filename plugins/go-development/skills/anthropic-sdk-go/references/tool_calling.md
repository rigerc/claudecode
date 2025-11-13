# Tool Calling Guide

## Define Tool Schema

```go
import (
    "github.com/invopop/jsonschema"
    "encoding/json"
)

type GetCoordinatesInput struct {
    Location string `json:"location" jsonschema_description:"The location to look up."`
}

func GenerateSchema[T any]() anthropic.ToolInputSchemaParam {
    reflector := jsonschema.Reflector{
        AllowAdditionalProperties: false,
        DoNotReference:            true,
    }
    var v T
    schema := reflector.Reflect(v)
    return anthropic.ToolInputSchemaParam{
        Properties: schema.Properties,
    }
}

type GetCoordinateResponse struct {
    Long float64 `json:"long"`
    Lat  float64 `json:"lat"`
}

func GetCoordinates(location string) GetCoordinateResponse {
    // Mock implementation
    return GetCoordinateResponse{Long: -122.4194, Lat: 37.7749}
}
```

## Tool Calling Implementation

```go
func main() {
    client := anthropic.NewClient()

    // Define tools
    tools := []anthropic.ToolUnionParam{
        {
            OfTool: &anthropic.ToolParam{
                Name:        "get_coordinates",
                Description: anthropic.String("Get coordinates for a location"),
                InputSchema: GenerateSchema[GetCoordinatesInput](),
            },
        },
    }

    messages := []anthropic.MessageParam{
        anthropic.NewUserMessage(anthropic.NewTextBlock("Where is San Francisco?")),
    }

    // Conversation loop for tool calling
    for {
        message, err := client.Messages.New(context.TODO(), anthropic.MessageNewParams{
            Model:     anthropic.ModelClaude3_7SonnetLatest,
            MaxTokens: 1024,
            Messages:  messages,
            Tools:     tools,
        })

        if err != nil {
            panic(err)
        }

        messages = append(messages, message.ToParam())
        toolResults := []anthropic.ContentBlockParamUnion{}

        // Process tool use blocks
        for _, block := range message.Content {
            if toolUse, ok := block.AsAny().(anthropic.ToolUseBlock); ok {
                var response interface{}
                switch toolUse.Name {
                case "get_coordinates":
                    var input GetCoordinatesInput
                    err := json.Unmarshal([]byte(toolUse.JSON.Input.Raw()), &input)
                    if err != nil {
                        panic(err)
                    }
                    response = GetCoordinates(input.Location)
                }

                result, _ := json.Marshal(response)
                toolResults = append(toolResults, anthropic.NewToolResultBlock(toolUse.ID, string(result), false))
            }
        }

        if len(toolResults) == 0 {
            break // No more tools to execute
        }

        messages = append(messages, anthropic.NewUserMessage(toolResults...))
    }
}
```

## Best Practices

### Schema Generation
- Use the `jsonschema` library for automatic schema generation
- Add `jsonschema_description` tags for parameter descriptions
- Set `AllowAdditionalProperties: false` for strict validation
- Set `DoNotReference: true` to avoid JSON Schema references

### Error Handling
- Always validate tool input before execution
- Return meaningful error messages in tool results
- Use the `is_error` parameter in `NewToolResultBlock` for failures

### Performance
- Minimize tool execution time to reduce API latency
- Cache tool results when appropriate
- Implement timeout handling for long-running tools
