package main

import (
    "fmt"
    "net/http"
    "net/url"
    "os"
    "time"

    openai "github.com/sashabaranov/go-openai"
)

// ClientFactory provides different client configurations for OpenAI API
type ClientFactory struct{}

// NewClient creates a new OpenAI client with basic configuration
func (cf *ClientFactory) NewClient(apiKey string) *openai.Client {
    if apiKey == "" {
        apiKey = os.Getenv("OPENAI_API_KEY")
    }
    return openai.NewClient(apiKey)
}

// NewClientWithConfig creates a new OpenAI client with custom configuration
func (cf *ClientFactory) NewClientWithConfig(apiKey, baseURL, orgID string, timeout time.Duration) *openai.Client {
    config := openai.DefaultConfig(apiKey)

    if baseURL != "" {
        config.BaseURL = baseURL
    }
    if orgID != "" {
        config.OrgID = orgID
    }
    if timeout > 0 {
        config.HTTPClient = &http.Client{
            Timeout: timeout,
        }
    }

    return openai.NewClientWithConfig(config)
}

// NewAzureClient creates a new OpenAI client configured for Azure OpenAI
func (cf *ClientFactory) NewAzureClient(apiKey, endpoint string) *openai.Client {
    config := openai.DefaultAzureConfig(apiKey, endpoint)

    // Map model names to deployment names
    config.AzureModelMapperFunc = func(model string) string {
        azureModelMapping := map[string]string{
            "gpt-3.5-turbo":           os.Getenv("AZURE_GPT35_DEPLOYMENT"),
            "gpt-4":                   os.Getenv("AZURE_GPT4_DEPLOYMENT"),
            "gpt-4-turbo":             os.Getenv("AZURE_GPT4_TURBO_DEPLOYMENT"),
            "text-embedding-ada-002":   os.Getenv("AZURE_EMBEDDING_DEPLOYMENT"),
        }
        if deployment, exists := azureModelMapping[model]; exists {
            return deployment
        }
        return model
    }

    return openai.NewClientWithConfig(config)
}

// NewClientWithProxy creates a new OpenAI client with proxy configuration
func (cf *ClientFactory) NewClientWithProxy(apiKey, proxyURL string) (*openai.Client, error) {
    config := openai.DefaultConfig(apiKey)

    if proxyURL != "" {
        parsedURL, err := url.Parse(proxyURL)
        if err != nil {
            return nil, fmt.Errorf("invalid proxy URL: %w", err)
        }

        transport := &http.Transport{
            Proxy: http.ProxyURL(parsedURL),
        }

        config.HTTPClient = &http.Client{
            Transport: transport,
            Timeout:   30 * time.Second,
        }
    }

    return openai.NewClientWithConfig(config), nil
}

// ValidateConfig validates the required configuration
func (cf *ClientFactory) ValidateConfig() error {
    if os.Getenv("OPENAI_API_KEY") == "" {
        return fmt.Errorf("OPENAI_API_KEY environment variable is required")
    }
    return nil
}

// GetRecommendedModels returns a list of recommended models for different use cases
func (cf *ClientFactory) GetRecommendedModels() map[string]string {
    return map[string]string{
        "simple_qa":        openai.GPT3Dot5Turbo,
        "complex_reasoning": openai.GPT4,
        "code_generation":  openai.GPT4,
        "creative_writing": openai.GPT4,
        "embeddings":       openai.AdaEmbeddingV2,
        "image_generation": openai.CreateImageModelDallE3,
    }
}

// GetModelPricing returns pricing information for models (approximate)
func (cf *ClientFactory) GetModelPricing() map[string]ModelPricing {
    return map[string]ModelPricing{
        openai.GPT4: {
            InputCostPerToken:  0.00003,  // $0.03 per 1K input tokens
            OutputCostPerToken: 0.00006,  // $0.06 per 1K output tokens
        },
        openai.GPT3Dot5Turbo: {
            InputCostPerToken:  0.000001, // $0.001 per 1K input tokens
            OutputCostPerToken: 0.000002, // $0.002 per 1K output tokens
        },
        openai.GPT4o: {
            InputCostPerToken:  0.000005, // $0.005 per 1K input tokens
            OutputCostPerToken: 0.000015, // $0.015 per 1K output tokens
        },
        openai.AdaEmbeddingV2: {
            InputCostPerToken:  0.0000001, // $0.0001 per 1K tokens
        },
    }
}

// ModelPricing contains pricing information for a model
type ModelPricing struct {
    InputCostPerToken  float64
    OutputCostPerToken float64
}