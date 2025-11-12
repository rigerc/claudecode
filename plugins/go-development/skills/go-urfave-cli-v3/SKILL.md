---
name: go-urfave-cli-v3
description: This skill helps developers create Go CLI applications using urfave/cli v3. Use this skill when building command-line tools, creating CLI interfaces for Go applications, or migrating from urfave/cli v2 to v3. The skill provides code generation, templates, migration tools, and comprehensive reference materials.
---

# Go Urfave CLI v3

## Overview

This skill enables rapid development of Go command-line applications using urfave/cli v3. It provides code generators, templates, reference documentation, and migration tools to help developers create professional CLI tools with minimal boilerplate.

## Quick Start

**When to use this skill:**
- Building a new CLI application in Go
- Adding command-line interface to existing Go applications
- Migrating from urfave/cli v2 to v3
- Learning urfave/cli v3 patterns and best practices
- Generating boilerplate code for common CLI patterns

### Choose Your Approach

**For new CLI applications:** Use the templates and generators
**For learning:** Reference the flag types and command patterns documentation
**For migration:** Use the v2 to v3 migrator tool

## Code Generation

### Generate Basic CLI Application

Use the CLI generator script to create boilerplate applications:

```bash
# Generate a basic CLI app
python3 scripts/generate_cli.py myapp "A sample CLI application" --author "Your Name"

# Generate with subcommands
python3 scripts/generate_cli.py mytool "Tool with subcommands" --type subcommands --commands build deploy test

# Generate advanced app with features
python3 scripts/generate_cli.py advanced "Advanced CLI application" --type advanced --author "Your Name"
```

### Available Templates

1. **Basic App Template** (`assets/templates/basic_app.go`)
   - Simple command structure
   - Basic action function
   - Minimal configuration

2. **Nested Commands Template** (`assets/templates/nested_commands.go`)
   - Hierarchical command structure
   - Global flags
   - Multiple command categories
   - User management, config, server commands

3. **Advanced Features Template** (`assets/templates/advanced_features.go`)
   - Complete feature set
   - Flag validation and categories
   - Shell completion
   - Error handling
   - Interactive modes
   - Setup wizard

## Reference Materials

### Flag Types Reference (`references/flag_types.md`)

Comprehensive documentation for all urfave/cli v3 flag types:

**Basic Flags:**
- BoolFlag, StringFlag, IntFlag, FloatFlag, DurationFlag, UintFlag
- Usage examples and validation patterns

**Advanced Flags:**
- Slice flags (StringSlice, IntSlice, FloatSlice)
- Flag categories and grouping
- Environment variable integration
- Required and persistent flags
- Custom flag types

**Flag Features:**
- Custom validation with Action functions
- Default values and destinations
- Hidden flags and aliases
- Environment variable mapping

### Command Patterns Reference (`references/command_patterns.md`)

Common CLI patterns and best practices:

**Basic Patterns:**
- Simple commands with actions
- Commands with flags and arguments
- Input validation and error handling

**Advanced Patterns:**
- Hierarchical command organization
- Lifecycle hooks (Before/After)
- Interactive commands and prompts
- Context-aware operations
- Shell completion integration

**Organizational Patterns:**
- Command categories and grouping
- Service management CLI
- Configuration management tools
- Interactive wizards

## Migration Tools

### v2 to v3 Migrator (`scripts/v2_to_v3_migrator.py`)

Automated migration tool for urfave/cli v2 to v3:

```bash
# Migrate specific files
python3 scripts/v2_to_v3_migrator.py main.go cmd/*.go

# Migrate with dry run to see changes
python3 scripts/v2_to_v3_migrator.py --dry-run main.go

# Migrate without creating backups
python3 scripts/v2_to_v3_migrator.py --no-backup main.go
```

**Migration Changes:**
- Import statements: `v2` → `v3`
- App creation: `cli.App{}` → `cli.Command{}`
- Action functions: Add `context.Context` parameter
- Flag actions: Updated signature with context
- Function calls: `c.App.Run()` → `cmd.Run(context.Background())`

## Workflow Examples

### Creating a New CLI Tool

1. **Generate basic structure:**
   ```bash
   python3 scripts/generate_cli.py mytool "My CLI tool" --type advanced
   ```

2. **Customize commands:**
   - Use `references/command_patterns.md` for patterns
   - Modify generated templates as needed

3. **Add validation:**
   - Reference `references/flag_types.md` for validation patterns
   - Implement custom flag actions

4. **Test the application:**
   ```bash
   go mod init mytool
   go get github.com/urfave/cli/v3
   go run .
   ```

### Migrating Existing v2 Application

1. **Backup existing code:**
   ```bash
   python3 scripts/v2_to_v3_migrator.py --dry-run *.go
   ```

2. **Apply migration:**
   ```bash
   python3 scripts/v2_to_v3_migrator.py *.go
   ```

3. **Update dependencies:**
   ```bash
   go get github.com/urfave/cli/v3@latest
   ```

4. **Test and fix issues:**
   - Run tests and fix compilation errors
   - Update any custom flag types
   - Test CLI functionality

### Building Complex CLI Applications

1. **Start with advanced template:**
   ```bash
   cp assets/templates/advanced_features.go myapp.go
   ```

2. **Add custom commands:**
   - Reference command patterns for complex structures
   - Implement nested command hierarchies

3. **Integrate with external systems:**
   - Use context for cancellation
   - Implement proper error handling
   - Add configuration management

## Resources

### scripts/
**CLI Generator:** `generate_cli.py` - Automated Go CLI application generator with support for basic, subcommand, and advanced application types.

**Migration Tool:** `v2_to_v3_migrator.py` - Automated migration from urfave/cli v2 to v3 with dry-run support and backup creation.

### references/
**Flag Types:** `flag_types.md` - Comprehensive reference for all urfave/cli v3 flag types, including basic flags, slice flags, and advanced features like validation and environment variables.

**Command Patterns:** `command_patterns.md` - Common CLI patterns and best practices, from basic commands to complex interactive applications with proper error handling.

### assets/templates/
**Basic App:** `basic_app.go` - Simple CLI application template with minimal setup and configuration.

**Nested Commands:** `nested_commands.go` - Template with hierarchical command structure, including user management, configuration, and server commands.

**Advanced Features:** `advanced_features.go` - Full-featured template with validation, shell completion, interactive modes, and comprehensive error handling.

## Best Practices

1. **Always include context:** Use `context.Context` in action functions for cancellation and timeouts
2. **Validate input:** Use flag actions and command-level validation
3. **Provide good help:** Use clear descriptions and categorize flags
4. **Handle errors properly:** Return meaningful errors with proper context
5. **Enable completion:** Use shell completion for better user experience
6. **Organize commands:** Use categories and nested structures for complex CLIs
7. **Test commands:** Write tests for CLI functionality and user interactions
