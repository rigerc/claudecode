# Workflow Examples

## Creating a New CLI Tool

### 1. Generate Basic Structure

```bash
python3 scripts/generate_cli.py mytool "My CLI tool" --type advanced --author "Your Name"
```

### 2. Customize Commands

- Use `references/command_patterns.md` for patterns
- Modify generated templates as needed
- Add custom flags and validation

### 3. Add Validation

- Reference `references/flag_types.md` for validation patterns
- Implement custom flag actions
- Add Before/After hooks for command-level validation

### 4. Test the Application

```bash
go mod init mytool
go get github.com/urfave/cli/v3
go run .
```

## Migrating Existing v2 Application

### 1. Backup Existing Code

```bash
# Dry run to preview changes
python3 scripts/v2_to_v3_migrator.py --dry-run *.go
```

### 2. Apply Migration

```bash
# Apply migration with automatic backups
python3 scripts/v2_to_v3_migrator.py *.go

# Or without backups
python3 scripts/v2_to_v3_migrator.py --no-backup *.go
```

### 3. Update Dependencies

```bash
go get github.com/urfave/cli/v3@latest
go mod tidy
```

### 4. Test and Fix Issues

- Run tests and fix compilation errors
- Update any custom flag types
- Test CLI functionality
- Verify context handling in action functions

## Building Complex CLI Applications

### 1. Start with Advanced Template

```bash
cp assets/templates/advanced_features.go myapp.go
```

### 2. Add Custom Commands

- Reference command patterns for complex structures
- Implement nested command hierarchies
- Add command categories for organization

### 3. Integrate with External Systems

- Use context for cancellation and timeouts
- Implement proper error handling
- Add configuration management
- Integrate with external APIs or services

## Available Templates

### Basic App Template (`assets/templates/basic_app.go`)
- Simple command structure
- Basic action function
- Minimal configuration
- Best for: Simple single-command tools

### Nested Commands Template (`assets/templates/nested_commands.go`)
- Hierarchical command structure
- Global flags
- Multiple command categories
- User management, config, server commands
- Best for: Multi-command tools with subcommands

### Advanced Features Template (`assets/templates/advanced_features.go`)
- Complete feature set
- Flag validation and categories
- Shell completion
- Error handling
- Interactive modes
- Setup wizard
- Best for: Production-grade CLI applications

## Code Generation Options

### Basic Generation

```bash
python3 scripts/generate_cli.py myapp "A sample CLI application"
```

### With Subcommands

```bash
python3 scripts/generate_cli.py mytool "Tool with subcommands" \
  --type subcommands \
  --commands build deploy test status
```

### Advanced Generation

```bash
python3 scripts/generate_cli.py advanced "Advanced CLI application" \
  --type advanced \
  --author "Your Name"
```

## Best Practices

1. **Always include context**: Use `context.Context` in action functions for cancellation and timeouts
2. **Validate input**: Use flag actions and command-level validation
3. **Provide good help**: Use clear descriptions and categorize flags
4. **Handle errors properly**: Return meaningful errors with proper context
5. **Enable completion**: Use shell completion for better user experience
6. **Organize commands**: Use categories and nested structures for complex CLIs
7. **Test commands**: Write tests for CLI functionality and user interactions
