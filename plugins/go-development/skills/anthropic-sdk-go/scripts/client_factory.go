package main

import (
    "fmt"
    "os"
    "time"

    "github.com/anthropics/anthropic-sdk-go"
    "github.com/anthropics/anthropic-sdk-go/option"
)

// ClientFactory provides different client configurations for Anthropic SDK
type ClientFactory struct{}

// NewClient creates a new Anthropic client with basic configuration
func (cf *ClientFactory) NewClient(apiKey string) *anthropic.Client {
    if apiKey == "" {
        apiKey = os.Getenv("ANTHROPIC_API_KEY")
    }
    return anthropic.NewClient(
        option.WithAPIKey(apiKey),
    )
}

// NewClientWithConfig creates a new Anthropic client with custom configuration
func (cf *ClientFactory) NewClientWithConfig(apiKey string, maxRetries int, timeout time.Duration) *anthropic.Client {
    if apiKey == "" {
        apiKey = os.Getenv("ANTHROPIC_API_KEY")
    }

    options := []option.RequestOption{
        option.WithAPIKey(apiKey),
        option.WithMaxRetries(maxRetries),
    }

    if timeout > 0 {
        options = append(options, option.WithRequestTimeout(timeout))
    }

    return anthropic.NewClient(options...)
}

// NewAzureClient creates a new Anthropic client configured for Azure
func (cf *ClientFactory) NewAzureClient() *anthropic.Client {
    // Note: Azure configuration would need specific Azure endpoint
    // This is a placeholder for Azure-specific setup
    return anthropic.NewClient(
        option.WithAPIKey(os.Getenv("AZURE_ANTHROPIC_API_KEY")),
    )
}

// NewBedrockClient creates a new Anthropic client configured for AWS Bedrock
func (cf *ClientFactory) NewBedrockClient(ctx context.Context) (*anthropic.Client, error) {
    import "github.com/anthropics/anthropic-sdk-go/bedrock"

    client := anthropic.NewClient(
        bedrock.WithLoadDefaultConfig(ctx),
    )
    return client, nil
}

// NewVertexClient creates a new Anthropic client configured for Google Vertex AI
func (cf *ClientFactory) NewVertexClient(ctx context.Context, projectID, region string) *anthropic.Client {
    import "github.com/anthropics/anthropic-sdk-go/vertex"

    return anthropic.NewClient(
        vertex.WithGoogleAuth(ctx, region, projectID),
    )
}

// ValidateConfig validates the required configuration
func (cf *ClientFactory) ValidateConfig() error {
    if os.Getenv("ANTHROPIC_API_KEY") == "" {
        return fmt.Errorf("ANTHROPIC_API_KEY environment variable is required")
    }
    return nil
}

// GetRecommendedModels returns a list of recommended models for different use cases
func (cf *ClientFactory) GetRecommendedModels() map[string]anthropic.Model {
    return map[string]anthropic.Model{
        "simple_qa":        anthropic.ModelClaude3_5HaikuLatest,
        "complex_reasoning": anthropic.ModelClaude3_7SonnetLatest,
        "code_generation":  anthropic.ModelClaude3_5SonnetLatest,
        "creative_writing": anthropic.ModelClaude3_7SonnetLatest,
    }
}