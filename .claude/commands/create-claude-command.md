---
allowed-tools: Write, Edit, Read, Bash(mkdir, ls, test)
description: Create a new Claude Code slash command with proper structure and validation
---

# Create Claude Code Command

This command helps you create a new Claude Code slash command with the proper structure, frontmatter, and content template.

## Usage

```
/create-command <command-name> "<command-description>"
```

## Parameters

- **command-name**: The name of the command (without slash, 3-50 chars, alphanumeric + hyphens)
- **command-description**: Brief description of what the command does (enclose in quotes)

## Requirements

- Command names must be unique and not conflict with existing commands
- Use kebab-case for multi-word commands (e.g., `deploy-staging`)
- Description should be concise but descriptive
- Commands directory must exist or be creatable

## Command Structure

Creates a new command file at `.claude/commands/<command-name>.md` with:

1. **Frontmatter**: Contains allowed tools, description, and other metadata
2. **Usage section**: Shows how to use the command
3. **Parameters section**: Documents command parameters
4. **Implementation section**: The actual command logic
5. **Examples section**: Usage examples (optional)

## Template Features

- Automatic directory creation if needed
- Pre-configured common allowed tools
- Standard command structure
- Placeholder content with clear instructions
- Validation for command name format

## Implementation

When executed, this command will:

1. Validate the command name (alphanumeric, hyphens only)
2. Ensure the `.claude/commands` directory exists
3. Create the command file with proper structure
4. Add a helpful template with placeholders
5. Show next steps for customizing the command

## Command Template

The generated command file will include:

```markdown
---
allowed-tools: Read, Write, Edit, Bash
description: {{DESCRIPTION}}
---

# {{COMMAND_NAME}}

## Usage

```
/{{COMMAND_NAME}} [options]
```

## Implementation

[Your command implementation goes here]

## Examples

```bash
/{{COMMAND_NAME}} --help
```
```

## Validation Rules

- Command name must be 3-50 characters
- Only letters, numbers, and hyphens allowed
- Must not start or end with hyphen
- Must not conflict with existing commands

## Examples

```bash
# Create a deployment command
/create-command deploy "Build and deploy application to production"

# Create a testing command
/create-command test "Run comprehensive test suite"

# Create a code review command
/create-command review "Perform automated code review"
```

## Next Steps After Creation

1. Edit the generated command file at `.claude/commands/<command-name>.md`
2. Customize the allowed tools in the frontmatter
3. Implement the actual command logic
4. Add examples and documentation
5. Test the new command with `/<command-name>`

## Notes

- Command names should be descriptive and concise
- Use kebab-case for multi-word commands
- Include only necessary tools in allowed-tools for security
- Test commands thoroughly before sharing