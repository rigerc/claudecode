package main

import (
    "context"
    "fmt"
    "math"

    "github.com/anthropics/anthropic-sdk-go"
)

// TokenCounter provides token counting and cost estimation functionality
type TokenCounter struct {
    client   *anthropic.Client
    pricing  map[anthropic.Model]PricingInfo
}

// PricingInfo contains pricing information for a model
type PricingInfo struct {
    InputCostPerMillion  float64 // USD per 1M input tokens
    OutputCostPerMillion float64 // USD per 1M output tokens
}

// NewTokenCounter creates a new token counter with default pricing
func NewTokenCounter(client *anthropic.Client) *TokenCounter {
    return &TokenCounter{
        client: client,
        pricing: map[anthropic.Model]PricingInfo{
            anthropic.ModelClaude3_7SonnetLatest: {
                InputCostPerMillion:  15.0,
                OutputCostPerMillion: 75.0,
            },
            anthropic.ModelClaude3_5SonnetLatest: {
                InputCostPerMillion:  3.0,
                OutputCostPerMillion: 15.0,
            },
            anthropic.ModelClaude3_5HaikuLatest: {
                InputCostPerMillion:  1.0,
                OutputCostPerMillion: 5.0,
            },
            anthropic.ModelClaude3OpusLatest: {
                InputCostPerMillion:  15.0,
                OutputCostPerMillion: 75.0,
            },
        },
    }
}

// CountTokens counts the tokens in a message list for a given model
func (tc *TokenCounter) CountTokens(ctx context.Context, model anthropic.Model, messages []anthropic.MessageParam) (*anthropic.MessageCountTokensResponse, error) {
    return tc.client.Messages.CountTokens(ctx, anthropic.MessageCountTokensParams{
        Model:    model,
        Messages: messages,
    })
}

// EstimateCost estimates the cost of a request based on token counts
func (tc *TokenCounter) EstimateCost(model anthropic.Model, inputTokens, outputTokens int) float64 {
    pricing, exists := tc.pricing[model]
    if !exists {
        return 0.0 // Unknown model, cannot estimate
    }

    inputCost := float64(inputTokens) / 1000000.0 * pricing.InputCostPerMillion
    outputCost := float64(outputTokens) / 1000000.0 * pricing.OutputCostPerMillion

    return inputCost + outputCost
}

// GetMaxTokensForTask returns recommended max tokens based on task type
func (tc *TokenCounter) GetMaxTokensForTask(taskType string) int {
    switch taskType {
    case "simple_qa":
        return 150
    case "code_generation":
        return 2000
    case "creative_writing":
        return 4000
    case "analysis":
        return 3000
    default:
        return 1000
    }
}

// TrackUsage prints usage information and estimated cost
func (tc *TokenCounter) TrackUsage(model anthropic.Model, usage *anthropic.MessageUsage) {
    if usage == nil {
        return
    }

    cost := tc.EstimateCost(model, usage.InputTokens, usage.OutputTokens)

    fmt.Printf("📊 Usage Statistics:\n")
    fmt.Printf("  Input Tokens:  %d\n", usage.InputTokens)
    fmt.Printf("  Output Tokens: %d\n", usage.OutputTokens)
    fmt.Printf("  Total Tokens:  %d\n", usage.InputTokens+usage.OutputTokens)
    fmt.Printf("  Estimated Cost: $%.6f\n", cost)
}

// OptimizeMessages optimizes message list to reduce token usage
func (tc *TokenCounter) OptimizeMessages(messages []anthropic.MessageParam) []anthropic.MessageParam {
    // Simple optimization: remove system messages if they're too long
    optimized := make([]anthropic.MessageParam, 0, len(messages))

    for _, msg := range messages {
        if msg.Role == anthropic.MessageParamRoleSystem {
            // Truncate very long system messages
            if len(msg.Content) > 0 {
                if content := msg.Content[0].OfRequestTextBlock; content != nil {
                    if len(content.Text) > 1000 {
                        content.Text = content.Text[:1000] + "..."
                    }
                }
            }
        }
        optimized = append(optimized, msg)
    }

    return optimized
}

// GetModelLimits returns token limits for different models
func (tc *TokenCounter) GetModelLimits(model anthropic.Model) (maxInput, maxOutput int) {
    switch model {
    case anthropic.ModelClaude3_7SonnetLatest:
        return 200000, 8192
    case anthropic.ModelClaude3_5SonnetLatest:
        return 200000, 8192
    case anthropic.ModelClaude3_5HaikuLatest:
        return 200000, 8192
    case anthropic.ModelClaude3OpusLatest:
        return 200000, 4096
    default:
        return 100000, 4096
    }
}

// ShouldUseStreaming determines if streaming should be used based on expected output length
func (tc *TokenCounter) ShouldUseStreaming(taskType string) bool {
    streamingTasks := map[string]bool{
        "creative_writing": true,
        "analysis":         true,
        "code_generation":  true,
    }

    return streamingTasks[taskType] || false
}