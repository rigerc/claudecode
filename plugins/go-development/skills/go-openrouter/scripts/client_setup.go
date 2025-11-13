package main

import (
    "fmt"
    "os"
    openrouter "github.com/revrost/go-openrouter"
)

// ClientFactory provides different client configurations for OpenRouter
type ClientFactory struct{}

// NewClient creates a new OpenRouter client with basic configuration
func (cf *ClientFactory) NewClient(apiKey string) *openrouter.Client {
    if apiKey == "" {
        apiKey = os.Getenv("OPENROUTER_API_KEY")
    }
    return openrouter.NewClient(apiKey)
}

// NewClientWithConfig creates a new OpenRouter client with custom configuration
func (cf *ClientFactory) NewClientWithConfig(apiKey, appName, appURL string) *openrouter.Client {
    if apiKey == "" {
        apiKey = os.Getenv("OPENROUTER_API_KEY")
    }
    if appName == "" {
        appName = os.Getenv("APP_NAME")
    }
    if appURL == "" {
        appURL = os.Getenv("APP_URL")
    }

    return openrouter.NewClient(
        apiKey,
        openrouter.WithXTitle(appName),
        openrouter.WithHTTPReferer(appURL),
    )
}

// ValidateConfig validates the required configuration
func (cf *ClientFactory) ValidateConfig() error {
    if os.Getenv("OPENROUTER_API_KEY") == "" {
        return fmt.Errorf("OPENROUTER_API_KEY environment variable is required")
    }
    return nil
}

// GetRecommendedModels returns a list of recommended models for different use cases
func (cf *ClientFactory) GetRecommendedModels() map[string][]string {
    return map[string][]string{
        "simple_qa": {
            "meta-llama/llama-3.1-8b-instruct:free",
            "microsoft/phi-3-mini-128k-instruct:free",
        },
        "complex_reasoning": {
            "anthropic/claude-3-5-sonnet",
            "openai/gpt-4o",
        },
        "code_generation": {
            "openai/gpt-4o-mini",
            "anthropic/claude-3-5-sonnet",
        },
        "creative_writing": {
            "meta-llama/llama-3.1-70b-instruct",
            "anthropic/claude-3-5-sonnet",
        },
    }
}