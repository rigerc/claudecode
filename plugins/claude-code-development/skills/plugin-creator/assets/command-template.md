---
description: Brief description of what this command does
---

# Command Name

Instructions for Claude when this command is invoked.

## Usage

- `/command-name` - Basic usage
- `/command-name arg1 arg2` - With arguments (use $1, $2, $ARGUMENTS)

## Implementation

1. Validate inputs (check $1, $2 if needed)
2. Perform main task
3. Return clear output

## Optional Frontmatter Fields

```yaml
description: Command description (optional, defaults to first line)
allowed-tools: [Read, Bash, Grep]  # Restrict available tools
model: claude-3-5-sonnet-20241022   # Use specific model
argument-hint: [file-path] [priority]  # Show in autocomplete
disable-model-invocation: false  # Set true for text expansion only
```

## Special Syntax

**Arguments:**
- `$1`, `$2`, `$3` - Positional arguments
- `$ARGUMENTS` - All arguments as string

**Bash execution:**
```
!`git status`
```

**File reference:**
```
@src/file.js
```
