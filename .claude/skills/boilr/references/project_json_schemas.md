# project.json Schema Reference

This document provides comprehensive schemas and patterns for `project.json` files in boilr templates.

## Basic Schema Structure

```json
{
  "prompts": [
    {
      "name": "variable_name",
      "message": "Prompt message for user",
      "default": "default_value",
      "type": "string"
    }
  ]
}
```

## Required Fields

### prompts (array)
An array of prompt objects that define what values to ask the user when applying the template.

**Each prompt object must contain:**
- `name` (string): The variable name used in templates (must be valid Go identifier)
- `message` (string): The prompt message shown to the user

## Optional Fields

### default (string)
The default value if the user doesn't provide one.

### type (string)
The type of input expected. Default is "string".
- `"string"`: Text input
- `"array"`: Multi-line input (one item per line)

## Common Prompt Patterns

### Basic Information Prompts

#### Application/Service Name
```json
{
  "name": "AppName",
  "message": "What is your application name?",
  "default": "myapp"
}
```

#### Go Module Name
```json
{
  "name": "ModuleName",
  "message": "What is your Go module name?",
  "default": "github.com/username/myapp"
}
```

#### Description
```json
{
  "name": "Description",
  "message": "Provide a short description:",
  "default": "A Go application"
}
```

#### Author Information
```json
{
  "name": "Author",
  "message": "Who is the author?",
  "default": ""
}
```

#### License
```json
{
  "name": "License",
  "message": "License type?",
  "default": "MIT"
}
```

### Configuration Prompts

#### Port Configuration
```json
{
  "name": "Port",
  "message": "Server port?",
  "default": "8080"
}
```

#### Boolean Configuration
```json
{
  "name": "EnableTLS",
  "message": "Enable TLS?",
  "default": "false"
}
```

#### Database Configuration
```json
{
  "name": "DatabaseType",
  "message": "Database type?",
  "default": "postgres"
}
```

### Array Input Prompts

#### Dependencies
```json
{
  "name": "Dependencies",
  "message": "Enter dependencies (one per line, empty when done):",
  "type": "array"
}
```

#### Features
```json
{
  "name": "Features",
  "message": "Select features (one per line, empty when done):",
  "type": "array"
}
```

## Complete Example Schemas

### CLI Application Schema
```json
{
  "prompts": [
    {
      "name": "AppName",
      "message": "What is your CLI application name?",
      "default": "mycli"
    },
    {
      "name": "ModuleName",
      "message": "What is your Go module name?",
      "default": "github.com/username/mycli"
    },
    {
      "name": "Description",
      "message": "Provide a short description:",
      "default": "A CLI application"
    },
    {
      "name": "Author",
      "message": "Who is the author?",
      "default": ""
    },
    {
      "name": "Version",
      "message": "Initial version?",
      "default": "v0.1.0"
    }
  ]
}
```

### Web Service Schema
```json
{
  "prompts": [
    {
      "name": "ServiceName",
      "message": "Service name?",
      "default": "myservice"
    },
    {
      "name": "ModuleName",
      "message": "Go module name?",
      "default": "github.com/username/myservice"
    },
    {
      "name": "Port",
      "message": "HTTP port?",
      "default": "8080"
    },
    {
      "name": "Description",
      "message": "Service description?",
      "default": "A web service"
    },
    {
      "name": "EnableTLS",
      "message": "Enable TLS?",
      "default": "false"
    },
    {
      "name": "DatabaseType",
      "message": "Database type?",
      "default": "postgres"
    },
    {
      "name": "EnableMetrics",
      "message": "Enable metrics?",
      "default": "true"
    }
  ]
}
```

### Library Schema
```json
{
  "prompts": [
    {
      "name": "LibName",
      "message": "Library name?",
      "default": "mylib"
    },
    {
      "name": "ModuleName",
      "message": "Go module name?",
      "default": "github.com/username/mylib"
    },
    {
      "name": "Description",
      "message": "Library description?",
      "default": "A Go library"
    },
    {
      "name": "Author",
      "message": "Author name?",
      "default": ""
    },
    {
      "name": "License",
      "message": "License type?",
      "default": "MIT"
    },
    {
      "name": "Version",
      "message": "Initial version?",
      "default": "v1.0.0"
    }
  ]
}
```

### Microservice Schema
```json
{
  "prompts": [
    {
      "name": "ServiceName",
      "message": "Microservice name?",
      "default": "myservice"
    },
    {
      "name": "ModuleName",
      "message": "Go module name?",
      "default": "github.com/username/myservice"
    },
    {
      "name": "HTTPPort",
      "message": "HTTP port?",
      "default": "8080"
    },
    {
      "name": "GRPCPort",
      "message": "gRPC port?",
      "default": "9090"
    },
    {
      "name": "DatabaseType",
      "message": "Database type?",
      "default": "postgres"
    },
    {
      "name": "EnableRedis",
      "message": "Enable Redis?",
      "default": "true"
    },
    {
      "name": "EnableKafka",
      "message": "Enable Kafka?",
      "default": "false"
    },
    {
      "name": "DockerRegistry",
      "message": "Docker registry?",
      "default": "docker.io/username"
    }
  ]
}
```

## Advanced Schema Patterns

### Conditional Prompts Handling
While project.json doesn't support conditional prompts directly, you can structure prompts to handle related options:

```json
{
  "prompts": [
    {
      "name": "DatabaseType",
      "message": "Database type?",
      "default": "postgres"
    },
    {
      "name": "DatabaseHost",
      "message": "Database host?",
      "default": "localhost"
    },
    {
      "name": "DatabasePort",
      "message": "Database port?",
      "default": "5432"
    },
    {
      "name": "DatabaseName",
      "message": "Database name?",
      "default": "myservice"
    }
  ]
}
```

### Feature Flags Schema
```json
{
  "prompts": [
    {
      "name": "EnableAuth",
      "message": "Enable authentication?",
      "default": "true"
    },
    {
      "name": "EnableLogging",
      "message": "Enable structured logging?",
      "default": "true"
    },
    {
      "name": "EnableMetrics",
      "message": "Enable Prometheus metrics?",
      "default": "true"
    },
    {
      "name": "EnableTracing",
      "message": "Enable distributed tracing?",
      "default": "false"
    }
  ]
}
```

### Development Environment Schema
```json
{
  "prompts": [
    {
      "name": "DevEnvironment",
      "message": "Development environment?",
      "default": "local"
    },
    {
      "name": "DockerCompose",
      "message": "Include docker-compose.yml?",
      "default": "true"
    },
    {
      "name": "Makefile",
      "message": "Include Makefile?",
      "default": "true"
    },
    {
      "name": "GitHubActions",
      "message": "Include GitHub Actions CI/CD?",
      "default": "true"
    }
  ]
}
```

## Naming Conventions

### Variable Names
- Use PascalCase for variable names (e.g., `AppName`, `ModuleName`)
- Must be valid Go identifiers
- Should be descriptive and clear

### Default Values
- Provide sensible defaults for all prompts
- Use lowercase for simple defaults
- Use standard ports (8080, 9090, etc.) for services
- Use standard license names (MIT, Apache-2.0, etc.)

### Message Guidelines
- Be clear and concise
- End with appropriate punctuation (? or :)
- Provide context for what information is needed

## Template Usage

### Variables in Filenames
Use `{{.VariableName}}` syntax in filenames:
- `{{.AppName}}.go`
- `cmd/{{.ServiceName}}/main.go`
- `configs/{{.AppName}}.yaml`

### Variables in File Content
Use the same syntax in file content:
```go
package main

import (
    "fmt"
    "log"
)

func main() {
    fmt.Println("{{.AppName}} - {{.Description}}")
    fmt.Println("Module: {{.ModuleName}}")
}
```

### Conditional Content in Templates
While project.json doesn't support conditionals, you can handle them in template files:
```go
{{if eq .EnableTLS "true"}}
import "crypto/tls"
{{end}}
```

## Best Practices

1. **Always provide defaults** - Users may accept all defaults
2. **Use descriptive names** - Clear variable names improve template readability
3. **Group related prompts** - Database configuration, ports, features, etc.
4. **Provide context** - Clear prompt messages help users understand what to provide
5. **Validate in templates** - Check for required values in template files
6. **Document dependencies** - Mention if certain prompts depend on others

## Validation Tips

- Variable names must match Go identifier rules
- All prompts must have both `name` and `message`
- Arrays are collected one item per line
- Template processing will fail if variables are undefined
- Test templates with various input combinations