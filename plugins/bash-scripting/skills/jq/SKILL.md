---
name: jq
# IMPORTANT: Keep description on ONE line for Claude Code compatibility
# prettier-ignore
description: Use for JSON processing with jq command in bash scripts, data filtering, transformation, and API response parsing
---

# jq - JSON Processor

## Quick Start

jq is a lightweight command-line JSON processor for slicing, filtering, and transforming JSON data.

```bash
# Extract specific field from JSON
echo '{"name":"Alice","age":30}' | jq '.name'
# Output: "Alice"

# Filter array objects
echo '[{"id":1,"type":"A"},{"id":2,"type":"B"}]' | jq '.[] | select(.type == "A")'
# Output: {"id":1,"type":"A"}

# Process API responses in bash
if curl -s api.example.com/data | jq -e '.success'; then
    echo "API call succeeded"
fi
```

## Core Principles

- **Filter Language**: jq uses a powerful filter language to transform JSON input to JSON output
- **Streaming Compatible**: Works with Unix pipelines and can process JSON streams
- **Shell Integration**: Perfect for bash scripts, with raw output modes for text processing
- **Zero Dependencies**: Written in portable C with no runtime dependencies

## Common Patterns

### API Response Processing

Parse, filter, and extract data from API responses in shell scripts. Use jq -e for conditional processing and jq -r for raw string output.

### Configuration Management

Validate, extract, and update JSON configuration files. Use jq for checking required fields and merging configurations.

## Reference Files

For detailed documentation, see:
- [references/jq-guide.md](references/jq-guide.md) - Complete jq command guide
- [references/](references/) - Additional examples and patterns

## Notes

- Always use jq -e for exit status control in conditional statements
- Use jq -r for raw string output when piping to other commands
- Validate JSON with `jq empty file.json` before processing

<!--
PROGRESSIVE DISCLOSURE GUIDELINES:
- Keep this file ~50 lines total (max ~150 lines)
- Use 1-2 code blocks only (recommend 1)
- Keep description <200 chars for Level 1 efficiency
- Move detailed docs to references/ for Level 3 loading
- This is Level 2 - quick reference ONLY, not a manual

LLM WORKFLOW (when editing this file):
1. Write/edit SKILL.md
2. Format (if formatter available)
3. Run: claude-skills-cli validate <path>
4. If multi-line description warning: run claude-skills-cli doctor <path>
5. Validate again to confirm
-->
