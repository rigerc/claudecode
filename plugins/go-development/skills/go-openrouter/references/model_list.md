# OpenRouter Model Reference

## Free Models (Good for Testing)
- `meta-llama/llama-3.1-8b-instruct:free` - Meta's Llama 3.1 8B model (free tier)
- `microsoft/phi-3-mini-128k-instruct:free` - Microsoft's Phi-3 Mini model (free tier)
- `qwen/qwen2-72b-instruct:free` - Qwen's 72B model (free tier)

## OpenAI Models
- `openai/gpt-4o` - Latest GPT-4 model with vision capabilities
- `openai/gpt-4o-mini` - Cost-effective GPT-4 variant
- `openai/gpt-3.5-turbo` - Fast and reliable model
- `openai/gpt-4-turbo` - Previous generation GPT-4

## Anthropic Models
- `anthropic/claude-3-5-sonnet` - Most capable Claude model
- `anthropic/claude-3-haiku` - Fast and cost-effective
- `anthropic/claude-3-opus` - Previous generation Claude

## Meta Models
- `meta-llama/llama-3.1-70b-instruct` - Large open-source model
- `meta-llama/llama-3.1-8b-instruct` - Medium-sized model
- `meta-llama/llama-3.1-405b-instruct` - Massive open-source model

## Google Models
- `google/gemini-pro` - Google's flagship model
- `google/gemini-flash` - Fast variant

## Model Selection Guidelines

### For Simple Q&A:
- Use `meta-llama/llama-3.1-8b-instruct:free` for cost efficiency
- Use `microsoft/phi-3-mini-128k-instruct:free` for quick responses

### For Complex Reasoning:
- Use `anthropic/claude-3-5-sonnet` for best quality
- Use `openai/gpt-4o` for good balance of quality and speed

### For Code Generation:
- Use `openai/gpt-4o-mini` for cost-effective coding
- Use `anthropic/claude-3-5-sonnet` for complex algorithms

### For Creative Writing:
- Use `meta-llama/llama-3.1-70b-instruct` for creativity
- Use `anthropic/claude-3-5-sonnet` for high-quality prose

## Rate Limits and Pricing

Check the OpenRouter dashboard for current pricing and rate limits for each model. Free models have limited requests per day.