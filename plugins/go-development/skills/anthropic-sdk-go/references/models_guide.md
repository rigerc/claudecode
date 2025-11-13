# Claude Models Guide

## Claude 3.7 Series (Latest)
- `claude-3-7-sonnet-latest` - Most capable Claude model
- **Best for**: Complex reasoning, code generation, analysis
- **Context Window**: 200K tokens
- **Cost**: Higher ($15/M input, $75/M output)

## Claude 3.5 Series
- `claude-3-5-sonnet-latest` - Balanced performance and cost
- **Best for**: General tasks, coding, writing
- **Context Window**: 200K tokens
- **Cost**: Medium ($3/M input, $15/M output)

- `claude-3-5-haiku-latest` - Fast and cost-effective
- **Best for**: Simple Q&A, quick responses
- **Context Window**: 200K tokens
- **Cost**: Low ($1/M input, $5/M output)

## Claude 3 Series
- `claude-3-opus-latest` - Previous generation, still powerful
- **Best for**: Creative writing, complex analysis
- **Context Window**: 200K tokens
- **Cost**: Higher ($15/M input, $75/M output)

## Model Selection Guidelines

### For Simple Q&A:
- Use `claude-3-5-haiku-latest` for speed and cost efficiency
- Good for: Basic questions, categorization, simple analysis

### For Code Generation:
- Use `claude-3-5-sonnet-latest` for balanced performance
- Use `claude-3-7-sonnet-latest` for complex algorithms
- Good for: Bug fixing, feature implementation, code review

### For Creative Writing:
- Use `claude-3-5-sonnet-latest` for quality writing
- Use `claude-3-7-sonnet-latest` for complex narratives
- Good for: Stories, marketing copy, technical documentation

### For Data Analysis:
- Use `claude-3-7-sonnet-latest` for complex reasoning
- Use `claude-3-5-sonnet-latest` for standard analysis
- Good for: Data interpretation, insights generation

### For Multimodal Tasks (Images):
- Use `claude-3-5-sonnet-latest` or `claude-3-7-sonnet-latest`
- Both models support image analysis

## Special Features

### Thinking Mode (Claude 3.7):
- Enables transparent reasoning process
- Best for complex problem-solving
- Requires `anthropic.AnthropicBetaThinkingAPI20241120` beta flag

### Tool Calling:
- All Claude 3.5+ models support function calling
- Best for integrating with external APIs and tools

### Web Search:
- Available as a beta feature
- Combines Claude with real-time web information
- Use `anthropic.BetaWebSearchTool20250305Param`

## Performance Tips

1. **Use appropriate max tokens**: Set reasonable limits based on task complexity
2. **Optimize prompts**: Clear, specific prompts yield better results
3. **Consider streaming**: For long responses, use streaming to improve UX
4. **Monitor usage**: Track token usage to control costs
5. **Choose right model**: Balance quality requirements with cost constraints

## Rate Limits

Check Anthropic dashboard for current rate limits:
- Higher tiers have increased rate limits
- Consider implementing retry logic for rate limit handling