# Boilr Best Practices

This document covers best practices for creating, organizing, and maintaining boilr templates.

## Template Structure Best Practices

### Directory Organization
```
template-name/
├── project.json          # Configuration file
├── template/             # Template files (processed by boilr)
│   ├── cmd/
│   │   └── appname/
│   │       └── main.go
│   ├── internal/
│   │   └── appname/
│   │       ├── server.go
│   │       └── handlers.go
│   ├── pkg/
│   │   └── appname/
│   │       └── client.go
│   ├── go.mod
│   ├── go.sum
│   └── README.md
└── boilerplate/          # Static files (copied as-is)
    ├── .gitignore
    ├── LICENSE
    └── Makefile
```

### Follow Go Project Layout Standards
- Use `cmd/` for main applications
- Use `internal/` for private application code
- Use `pkg/` for public library code
- Use `api/` for API definitions
- Use `configs/` for configuration files
- Use `scripts/` for build and utility scripts

## project.json Best Practices

### Variable Naming
```json
{
  "prompts": [
    {
      "name": "AppName",           // PascalCase, descriptive
      "message": "Application name?",
      "default": "myapp"
    },
    {
      "name": "ModuleName",        // Clear and specific
      "message": "Go module name?",
      "default": "github.com/username/myapp"
    }
  ]
}
```

**Guidelines:**
- Use PascalCase for variable names
- Be descriptive (`ServiceName` instead of `Name`)
- Follow Go naming conventions
- Avoid abbreviations unless widely understood

### Prompt Messages
```json
{
  "prompts": [
    {
      "name": "DatabaseType",
      "message": "What database type do you want to use?",  // Clear question
      "default": "postgres"
    },
    {
      "name": "EnableMetrics",
      "message": "Enable Prometheus metrics?",             // Specific feature
      "default": "true"
    }
  ]
}
```

**Guidelines:**
- Use clear, specific questions
- End with appropriate punctuation
- Provide context when needed
- Be consistent in tone and style

### Default Values
```json
{
  "prompts": [
    {
      "name": "Port",
      "message": "HTTP server port?",
      "default": "8080"              // Standard port
    },
    {
      "name": "License",
      "message": "License type?",
      "default": "MIT"               // Common license
    }
  ]
}
```

**Guidelines:**
- Provide sensible defaults
- Use standard values (ports, licenses, etc.)
- Consider security implications
- Make defaults work out-of-the-box

## Template File Best Practices

### Variable Usage
```go
// Good: Clear variable usage
package main

import (
    "fmt"
    "log"
    "{{.ModuleName}}/internal/config"
)

func main() {
    fmt.Println("Starting {{.AppName}}...")
    fmt.Println("{{.Description}}")
    log.Printf("Module: {{.ModuleName}}")
}
```

**Guidelines:**
- Use variables consistently throughout the template
- Include variables in comments and documentation
- Ensure all variables are defined in project.json
- Test with various input combinations

### Conditional Content
```go
// Good: Conditional feature inclusion
package main

import (
    "log"
    "net/http"
    {{if eq .EnableMetrics "true"}}
    "github.com/prometheus/client_golang/prometheus/promhttp"
    {{end}}
)

func main() {
    mux := http.NewServeMux()

    {{if eq .EnableMetrics "true"}}
    // Metrics endpoint
    mux.Handle("/metrics", promhttp.Handler())
    {{end}}

    log.Printf("Starting server on port {{.Port}}")
    log.Fatal(http.ListenAndServe(":{{.Port}}", mux))
}
```

**Guidelines:**
- Use conditional content for optional features
- Handle boolean flags with proper comparisons
- Include comments explaining conditional sections
- Test both enabled and disabled states

### Configuration Files
```yaml
# configs/{{.AppName}}.yaml
server:
  port: {{.Port}}
  {{if eq .EnableTLS "true"}}
  tls:
    enabled: true
    cert_file: "/etc/ssl/certs/server.crt"
    key_file: "/etc/ssl/private/server.key"
  {{end}}

database:
  type: {{.DatabaseType}}
  host: {{.DatabaseHost}}
  port: {{.DatabasePort}}
  name: {{.DatabaseName}}

logging:
  level: info
  format: json
```

**Guidelines:**
- Include configuration templates for common scenarios
- Use appropriate file formats (YAML, JSON, TOML)
- Provide sensible default structures
- Document configuration options

## Boilerplate Files Best Practices

### .gitignore
```
# Binaries for programs and plugins
*.exe
*.exe~
*.dll
*.so
*.dylib

# Test binary, built with `go test -c`
*.test

# Output of the go coverage tool
*.out

# Go workspace file
go.work

# Dependency directories
vendor/

# IDE files
.vscode/
.idea/
*.swp
*.swo

# OS files
.DS_Store
Thumbs.db

# Environment files
.env
.env.local
.env.production

# Log files
*.log

# Build output
dist/
build/
```

### LICENSE
Include appropriate license files:
- MIT License (permissive, simple)
- Apache-2.0 (patent grant, corporate friendly)
- GPL v3 (copyleft, requires source sharing)

### Makefile
```makefile
.PHONY: build test clean install

# Variables
APP_NAME := {{.AppName}}
VERSION := $(shell git describe --tags --always --dirty)
LDFLAGS := -ldflags "-X main.version=$(VERSION)"

# Build
build:
	go build $(LDFLAGS) -o bin/$(APP_NAME) ./cmd/$(APP_NAME)

# Test
test:
	go test -v ./...

test-coverage:
	go test -v -cover ./...

# Clean
clean:
	rm -rf bin/
	go clean -testcache

# Install
install: build
	cp bin/$(APP_NAME) $(GOPATH)/bin/

# Lint
lint:
	golangci-lint run

# Format
fmt:
	go fmt ./...
```

## Advanced Best Practices

### Template Validation
1. **Test with different inputs**: Try various combinations of user inputs
2. **Validate Go syntax**: Ensure generated Go code is valid
3. **Check dependencies**: Verify required packages are available
4. **Test build process**: Ensure generated projects can be built

### Documentation
1. **Template README**: Include clear instructions for using the template
2. **Inline comments**: Explain complex template logic
3. **Configuration documentation**: Document all configuration options
4. **Usage examples**: Provide examples of common use cases

### Versioning
1. **Semantic versioning**: Use semver for template versions
2. **Changelog**: Track changes between versions
3. **Backward compatibility**: Consider impact of breaking changes
4. **Migration guides**: Help users upgrade between versions

## Security Best Practices

### Input Validation
```go
// Validate user input in generated code
func validateAppName(name string) error {
    if name == "" {
        return errors.New("application name cannot be empty")
    }
    if len(name) > 100 {
        return errors.New("application name too long")
    }
    // Additional validation...
    return nil
}
```

### Dependency Management
1. **Pin versions**: Use specific versions in go.mod
2. **Security scanning**: Regular scan for vulnerabilities
3. **Minimal dependencies**: Include only necessary packages
4. **Vet dependencies**: Review third-party code

### Configuration Security
1. **No hardcoded secrets**: Never include passwords or API keys
2. **Environment variables**: Use environment-specific configuration
3. **Default security**: Enable secure defaults
4. **Documentation**: Document security considerations

## Performance Best Practices

### Template Efficiency
1. **Minimal processing**: Keep template logic simple
2. **Efficient variables**: Use variables efficiently
3. **File organization**: Structure files for performance
4. **Build optimization**: Optimize generated build processes

### Generated Code Performance
1. **Efficient imports**: Only import necessary packages
2. **Proper concurrency**: Use goroutines and channels correctly
3. **Memory management**: Consider memory usage patterns
4. **Error handling**: Include proper error handling

## Maintenance Best Practices

### Regular Updates
1. **Go version updates**: Keep Go versions current
2. **Dependency updates**: Regularly update dependencies
3. **Security patches**: Apply security updates promptly
4. **Feature enhancements**: Add useful new features

### Community Feedback
1. **User feedback**: Collect and act on user feedback
2. **Bug reports**: Address bug reports quickly
3. **Feature requests**: Consider user feature requests
4. **Documentation**: Keep documentation current

### Testing
1. **Template testing**: Test templates with various inputs
2. **Generated code testing**: Test generated code quality
3. **Integration testing**: Test complete workflows
4. **Automated testing**: Set up CI/CD for template testing

## Distribution Best Practices

### Template Repository
1. **Clear README**: Include comprehensive documentation
2. **Examples**: Provide usage examples
3. **Changelog**: Track changes and improvements
4. **Contributing guidelines**: Make it easy to contribute

### Version Management
1. **Semantic versioning**: Use consistent versioning
2. **Release notes**: Document changes in releases
3. **Stable branches**: Maintain stable versions
4. **Backward compatibility**: Consider breaking changes carefully

### User Support
1. **Documentation**: Provide comprehensive documentation
2. **Examples**: Include real-world examples
3. **Troubleshooting**: Common issues and solutions
4. **Community engagement**: Support user community

By following these best practices, you can create high-quality, maintainable boilr templates that provide excellent experiences for users scaffolding Go projects.