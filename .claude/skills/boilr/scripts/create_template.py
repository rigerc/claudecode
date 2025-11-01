#!/usr/bin/env python3
"""
Boilr Template Creation Helper
Automates the creation of boilr templates with common patterns and configurations.
"""

import os
import json
import sys
import argparse
from pathlib import Path

def create_project_json(template_dir, config):
    """Create project.json configuration file."""
    project_json = {
        "prompts": config.get("prompts", [])
    }

    project_json_path = Path(template_dir) / "project.json"
    with open(project_json_path, 'w') as f:
        json.dump(project_json, f, indent=2)

    print(f"✅ Created {project_json_path}")

def create_template_structure(template_dir, template_config):
    """Create the basic template directory structure."""
    template_path = Path(template_dir) / "template"
    template_path.mkdir(parents=True, exist_ok=True)

    print(f"✅ Created template structure at {template_path}")
    return template_path

def create_boilerplate_structure(template_dir, template_config):
    """Create boilerplate directory for static files."""
    boilerplate_path = Path(template_dir) / "boilerplate"
    boilerplate_path.mkdir(parents=True, exist_ok=True)

    print(f"✅ Created boilerplate structure at {boilerplate_path}")
    return boilerplate_path

def create_template_files(template_path, template_config):
    """Create common template files based on configuration."""
    files = template_config.get("files", [])

    for file_config in files:
        file_path = template_path / file_config["name"]
        content = file_config.get("content", "")

        # Create parent directories if needed
        file_path.parent.mkdir(parents=True, exist_ok=True)

        with open(file_path, 'w') as f:
            f.write(content)

        print(f"✅ Created template file: {file_path}")

def create_boilerplate_files(boilerplate_path, template_config):
    """Create static boilerplate files."""
    files = template_config.get("boilerplate_files", [])

    for file_config in files:
        file_path = boilerplate_path / file_config["name"]
        content = file_config.get("content", "")

        # Create parent directories if needed
        file_path.parent.mkdir(parents=True, exist_ok=True)

        with open(file_path, 'w') as f:
            f.write(content)

        print(f"✅ Created boilerplate file: {file_path}")

def get_template_presets():
    """Return predefined template configurations."""
    return {
        "basic-cli": {
            "prompts": [
                {"name": "AppName", "message": "What is your application name?", "default": "mycli"},
                {"name": "ModuleName", "message": "What is your Go module name?", "default": "github.com/username/mycli"},
                {"name": "Description", "message": "Provide a short description:", "default": "A CLI application"},
                {"name": "Author", "message": "Who is the author?", "default": ""}
            ],
            "files": [
                {
                    "name": "{{.AppName}}.go",
                    "content": """package main

import (
    "fmt"
    "log"
    "os"
)

func main() {
    fmt.Println("{{.AppName}} - {{.Description}}")
    fmt.Println("Author: {{.Author}}")

    if len(os.Args) < 2 {
        fmt.Println("Usage: {{.AppName}} <command>")
        os.Exit(1)
    }

    command := os.Args[1]
    switch command {
    case "hello":
        fmt.Println("Hello from {{.AppName}}!")
    default:
        log.Printf("Unknown command: %s", command)
        os.Exit(1)
    }
}
"""
                },
                {
                    "name": "go.mod",
                    "content": """module {{.ModuleName}}

go 1.21

require (
    // Add dependencies here
)
"""
                },
                {
                    "name": "README.md",
                    "content": """# {{.AppName}}

{{.Description}}

## Installation

```bash
go install {{.ModuleName}}
```

## Usage

```bash
{{.AppName}} hello
```

## Author

{{.Author}}
"""
                }
            ],
            "boilerplate_files": [
                {
                    "name": ".gitignore",
                    "content": """# Binaries for programs and plugins
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

# IDE
.vscode/
.idea/
*.swp
*.swo
"""
                }
            ]
        },
        "web-service": {
            "prompts": [
                {"name": "ServiceName", "message": "Service name?", "default": "myservice"},
                {"name": "ModuleName", "message": "Go module name?", "default": "github.com/username/myservice"},
                {"name": "Port", "message": "Server port?", "default": "8080"},
                {"name": "Description", "message": "Service description?", "default": "A web service"},
                {"name": "EnableTLS", "message": "Enable TLS?", "default": "false"}
            ],
            "files": [
                {
                    "name": "cmd/{{.ServiceName}}/main.go",
                    "content": """package main

import (
    "context"
    "fmt"
    "log"
    "net/http"
    "os"
    "os/signal"
    "syscall"
    "time"
)

func main() {
    // Configuration
    port := "{{.Port}}"
    if envPort := os.Getenv("PORT"); envPort != "" {
        port = envPort
    }

    // Setup HTTP server
    mux := http.NewServeMux()
    mux.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
        fmt.Fprintf(w, "Hello from {{.ServiceName}}!\\n")
        fmt.Fprintf(w, "{{.Description}}\\n")
    })

    mux.HandleFunc("/health", func(w http.ResponseWriter, r *http.Request) {
        fmt.Fprintf(w, "OK\\n")
    })

    server := &http.Server{
        Addr:         ":" + port,
        Handler:      mux,
        ReadTimeout:  15 * time.Second,
        WriteTimeout: 15 * time.Second,
        IdleTimeout:  60 * time.Second,
    }

    // Start server in a goroutine
    go func() {
        log.Printf("Starting {{.ServiceName}} on port %s", port)
        if err := server.ListenAndServe(); err != nil && err != http.ErrServerClosed {
            log.Fatalf("Server failed to start: %v", err)
        }
    }()

    // Wait for interrupt signal to gracefully shutdown the server
    quit := make(chan os.Signal, 1)
    signal.Notify(quit, syscall.SIGINT, syscall.SIGTERM)
    <-quit

    log.Println("Shutting down server...")
    ctx, cancel := context.WithTimeout(context.Background(), 30*time.Second)
    defer cancel()

    if err := server.Shutdown(ctx); err != nil {
        log.Fatalf("Server forced to shutdown: %v", err)
    }

    log.Println("Server exited")
}
"""
                },
                {
                    "name": "go.mod",
                    "content": """module {{.ModuleName}}

go 1.21

require (
    // Add dependencies here
)
"""
                },
                {
                    "name": "README.md",
                    "content": """# {{.ServiceName}}

{{.Description}}

## Running the service

```bash
go run cmd/{{.ServiceName}}/main.go
```

## API Endpoints

- `GET /` - Welcome message
- `GET /health` - Health check

## Environment Variables

- `PORT` - Server port (default: {{.Port}})

## Development

```bash
go mod tidy
go run cmd/{{.ServiceName}}/main.go
```
"""
                }
            ],
            "boilerplate_files": [
                {
                    "name": ".gitignore",
                    "content": """# Binaries for programs and plugins
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

# IDE
.vscode/
.idea/
*.swp
*.swo

# Environment
.env
.env.local
"""
                }
            ]
        }
    }

def main():
    parser = argparse.ArgumentParser(description="Create boilr templates")
    parser.add_argument("template_name", help="Name of the template to create")
    parser.add_argument("output_dir", help="Output directory for the template")
    parser.add_argument("--preset", choices=["basic-cli", "web-service"],
                       help="Use a predefined template preset")
    parser.add_argument("--config", help="JSON configuration file")

    args = parser.parse_args()

    # Get template configuration
    if args.preset:
        config = get_template_presets().get(args.preset)
        if not config:
            print(f"❌ Unknown preset: {args.preset}")
            sys.exit(1)
        print(f"🎯 Using preset: {args.preset}")
    elif args.config:
        with open(args.config, 'r') as f:
            config = json.load(f)
        print(f"📁 Using config file: {args.config}")
    else:
        print("❌ Please specify either --preset or --config")
        sys.exit(1)

    # Create template directory
    template_dir = Path(args.output_dir) / args.template_name
    template_dir.mkdir(parents=True, exist_ok=True)

    print(f"📁 Creating template: {args.template_name}")
    print(f"📍 Output directory: {template_dir}")

    # Create template structure
    template_path = create_template_structure(template_dir, config)
    boilerplate_path = create_boilerplate_structure(template_dir, config)

    # Create configuration file
    create_project_json(template_dir, config)

    # Create template files
    create_template_files(template_path, config)
    create_boilerplate_files(boilerplate_path, config)

    print(f"\n✅ Template '{args.template_name}' created successfully!")
    print(f"📂 Location: {template_dir}")
    print(f"\n📋 Next steps:")
    print(f"   1. Review the generated template files")
    print(f"   2. Customize as needed")
    print(f"   3. Save with: boilr template save {args.template_name} {template_dir}")
    print(f"   4. Use with: boilr template use {args.template_name} <target-directory>")

if __name__ == "__main__":
    main()