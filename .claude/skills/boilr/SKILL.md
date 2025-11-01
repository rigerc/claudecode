---
name: boilr
description: A template manager for Go projects that enables quick scaffolding from pre-defined templates. This skill should be used when users need to create new Go projects, set up boilerplate code, or manage project templates for team standardization.
---

# Boilr

## Overview

This skill enables users to create, manage, and use boilr templates for Go projects. It provides tools for template creation, validation, and project scaffolding with support for CLI applications, web services, libraries, and microservices.

## Core Capabilities

### 1. Template Management
- **Download templates** from GitHub repositories
- **Save local directories** as templates
- **List and remove** templates from registry
- **Validate template structure** and syntax

### 2. Template Creation
- **Automated template creation** using predefined configurations
- **Template validation** for structure and syntax errors
- **Best practices guidance** for Go project layouts
- **Common template patterns** for different project types

### 3. Project Scaffolding
- **Generate projects** from templates with variable substitution
- **Support for conditional content** based on user input
- **Complex project structures** with multiple directories
- **Integration with Go tools** and workflows

## Quick Start

### Using Existing Templates
```bash
# List available templates
boilr template ls

# Download a template from GitHub
boilr template download github.com/golang-standards/project-layout

# Use a template to create a new project
boilr template use project-layout ./my-new-project
```

### Creating Custom Templates
```bash
# Use the template creation script
python3 scripts/create_template.py my-template ./output --preset basic-cli

# Validate the template
python3 scripts/validate_template.py ./output/my-template

# Save the template to registry
boilr template save my-template ./output/my-template
```

## Template Types

### 1. CLI Applications
Use when creating command-line tools, utilities, or console applications.

**Key Features:**
- Flag-based command structure
- Version and help commands
- Proper error handling
- Cross-platform compatibility

**Variables:**
- `AppName` - Application name
- `ModuleName` - Go module path
- `Description` - Application description
- `Author` - Author name
- `Version` - Initial version

### 2. Web Services
Use when creating HTTP servers, REST APIs, or web applications.

**Key Features:**
- HTTP server setup with graceful shutdown
- Health check endpoints
- JSON API responses
- Environment variable configuration
- Optional TLS support

**Variables:**
- `ServiceName` - Service name
- `ModuleName` - Go module path
- `Port` - HTTP port number
- `Description` - Service description
- `EnableTLS` - TLS configuration flag

### 3. Libraries
Use when creating reusable Go packages for distribution.

**Key Features:**
- Package structure with public API
- Comprehensive test suite with examples
- Documentation and API reference
- Version management
- Dependency management

**Variables:**
- `LibName` - Library name
- `ModuleName` - Go module path
- `Description` - Library description
- `Author` - Author name
- `License` - License type

## Workflow Decision Tree

### New Project Creation

1. **Determine project type:**
   - CLI application → Use basic-cli template
   - Web service → Use web-service template
   - Library → Use library template
   - Custom needs → Create new template

2. **Choose template source:**
   - Existing template → Download and use directly
   - Custom template → Create from scratch or modify existing

3. **Apply template:**
   - Use `boilr template use` with variable prompts
   - Verify generated project structure
   - Customize as needed

### Template Development

1. **Start with template assets:**
   - Copy relevant template from `assets/`
   - Modify project.json for custom variables
   - Update template files for specific needs

2. **Validate template:**
   - Run validation script for syntax checking
   - Test template generation
   - Verify generated projects compile

3. **Save and distribute:**
   - Save to local registry
   - Publish to GitHub for sharing
   - Document usage instructions

## Common Usage Patterns

### Pattern 1: Team Standardization
```bash
# Create team-specific template
python3 scripts/create_template.py company-web-service ./templates --preset web-service

# Customize with company standards
# Add company headers, CI/CD, security settings

# Save to shared registry
boilr template save company-web-service ./templates/company-web-service
```

### Pattern 2: Project Initialization
```bash
# Quick project start
boilr template use basic-cli ./new-cli-tool
boilr template use web-service ./new-api
boilr template use library ./new-library
```

### Pattern 3: Template Updates
```bash
# Update existing template
cd templates/my-template
# Make changes to template files
# Validate changes
python3 ../scripts/validate_template.py .

# Re-save updated template
boilr template save my-template .
```

## Advanced Features

### Conditional Content
Template files can include conditional sections based on user input:

```go
{{if eq .EnableMetrics "true"}}
import "github.com/prometheus/client_golang/prometheus"
{{end}}
```

### Array Variables
Handle multiple inputs like dependencies or features:

```go
{{range .Dependencies}}
import "{{.}}"
{{end}}
```

### Template Functions
Use Go template functions for advanced formatting:

```go
Created: {{time "2006-01-02"}}
Module: {{.ModuleName | upper}}
```

## Resources

### Scripts (`scripts/`)
- **create_template.py** - Automated template creation with presets
- **validate_template.py** - Template validation and error checking

**Usage Examples:**
```bash
# Create CLI template
python3 scripts/create_template.py my-cli ./output --preset basic-cli

# Validate template
python3 scripts/validate_template.py ./my-template --strict
```

### References (`references/`)
- **template_examples.md** - Complete template examples for different project types
- **project_json_schemas.md** - Comprehensive project.json configuration patterns
- **best_practices.md** - Template creation and maintenance guidelines

**When to use references:**
- Learning template structure patterns
- Designing complex template configurations
- Understanding best practices
- Troubleshooting template issues

### Assets (`assets/`)
- **basic_cli_template/** - Complete CLI application template
- **web_service_template/** - HTTP server template with API endpoints
- **library_template/** - Reusable library template with tests

**Using template assets:**
- Copy and customize for specific needs
- Use as starting points for custom templates
- Reference for proper project structure
- Learn Go project layout patterns

## Integration with Go Workflows

### go.mod Integration
Templates automatically include proper go.mod files with module substitution:
```go
module {{.ModuleName}}
```

### Testing Integration
Templates include comprehensive test setups:
- Unit tests with testify
- Example functions for documentation
- Benchmark tests for performance
- Test coverage reporting

### CI/CD Integration
Template assets include CI/CD configurations:
- GitHub Actions workflows
- Docker containerization
- Automated testing and deployment

## Troubleshooting

### Common Issues

1. **Template variables not found:**
   - Check variable names in project.json
   - Ensure consistent naming (PascalCase)
   - Validate template syntax

2. **Generated code doesn't compile:**
   - Run validation script before using template
   - Check Go import paths
   - Verify syntax in template files

3. **Template not found:**
   - Use `boilr template ls` to verify installation
   - Download template from GitHub if missing
   - Check template registry path

### Debugging Steps

1. **Validate template:**
   ```bash
   python3 scripts/validate_template.py ./my-template
   ```

2. **Test template generation:**
   ```bash
   boilr template use my-template ./test-output
   cd test-output && go mod tidy && go build
   ```

3. **Check template structure:**
   - Verify project.json format
   - Check template/ directory exists
   - Ensure proper file permissions

## Best Practices

### Template Design
- Use descriptive variable names
- Provide sensible defaults
- Include comprehensive documentation
- Follow Go project layout standards

### Maintenance
- Test templates regularly
- Update Go versions in templates
- Validate generated projects
- Keep dependencies current

### Distribution
- Use semantic versioning
- Include clear README instructions
- Provide usage examples
- Document changes in changelog

