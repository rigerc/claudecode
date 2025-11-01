# Boilr Template Examples

This document provides comprehensive examples of boilr templates for various Go project types.

## Basic CLI Application Template

### project.json
```json
{
  "prompts": [
    {
      "name": "AppName",
      "message": "What is your application name?",
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
    }
  ]
}
```

### Template Files

#### template/{{.AppName}}.go
```go
package main

import (
	"flag"
	"fmt"
	"log"
	"os"
)

var (
	version = flag.Bool("version", false, "Show version information")
	help    = flag.Bool("help", false, "Show help information")
)

func main() {
	flag.Parse()

	if *version {
		fmt.Printf("{{.AppName}} v1.0.0\n")
		fmt.Printf("{{.Description}}\n")
		fmt.Printf("Author: {{.Author}}\n")
		os.Exit(0)
	}

	if *help || len(os.Args) == 1 {
		fmt.Println("{{.AppName}} - {{.Description}}")
		fmt.Println("\nUsage:")
		fmt.Printf("  %s [options] <command>\n", os.Args[0])
		fmt.Println("\nOptions:")
		fmt.Println("  -version  Show version information")
		fmt.Println("  -help     Show this help message")
		fmt.Println("\nCommands:")
		fmt.Println("  hello     Say hello")
		fmt.Println("  version   Show version")
		os.Exit(0)
	}

	if len(flag.Args()) < 1 {
		fmt.Println("Error: No command specified")
		fmt.Println("Use -help for usage information")
		os.Exit(1)
	}

	command := flag.Args()[0]
	switch command {
	case "hello":
		fmt.Println("Hello from {{.AppName}}!")
	case "version":
		fmt.Printf("{{.AppName}} v1.0.0\n")
	default:
		log.Printf("Unknown command: %s", command)
		os.Exit(1)
	}
}
```

#### template/go.mod
```go
module {{.ModuleName}}

go 1.21

require (
	github.com/spf13/cobra v1.7.0
	github.com/spf13/viper v1.16.0
)
```

#### template/README.md
```markdown
# {{.AppName}}

{{.Description}}

## Installation

```bash
go install {{.ModuleName}}@latest
```

## Usage

```bash
{{.AppName}} hello
{{.AppName}} -version
{{.AppName}} -help
```

## Development

```bash
# Clone the repository
git clone {{.ModuleName}}.git
cd {{.AppName}}

# Install dependencies
go mod tidy

# Run tests
go test ./...

# Build
go build -o {{.AppName}} .
```

## Author

{{.Author}}
```

## Web Service Template

### project.json
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
      "message": "Server port?",
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
    }
  ]
}
```

### Template Files

#### template/cmd/{{.ServiceName}}/main.go
```go
package main

import (
	"context"
	"fmt"
	"log"
	"net/http"
	"os"
	"os/signal"
	"syscall"
	"time"

	"{{.ModuleName}}/internal/config"
	"{{.ModuleName}}/internal/server"
)

func main() {
	// Load configuration
	cfg, err := config.Load()
	if err != nil {
		log.Fatalf("Failed to load configuration: %v", err)
	}

	// Create HTTP server
	srv := server.New(cfg)

	// Start server in a goroutine
	go func() {
		addr := fmt.Sprintf(":%d", cfg.Port)
		log.Printf("Starting {{.ServiceName}} on %s", addr)
		if err := srv.ListenAndServe(); err != nil && err != http.ErrServerClosed {
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

	if err := srv.Shutdown(ctx); err != nil {
		log.Fatalf("Server forced to shutdown: %v", err)
	}

	log.Println("Server exited")
}
```

#### template/internal/config/config.go
```go
package config

import (
	"fmt"
	"os"
	"strconv"
)

type Config struct {
	Port        int
	EnableTLS   bool
	ServiceName string
	Description string
}

func Load() (*Config, error) {
	port := {{.Port}}
	if envPort := os.Getenv("PORT"); envPort != "" {
		p, err := strconv.Atoi(envPort)
		if err != nil {
			return nil, fmt.Errorf("invalid PORT value: %s", envPort)
		}
		port = p
	}

	enableTLS := {{.EnableTLS}} == "true"
	if envTLS := os.Getenv("ENABLE_TLS"); envTLS != "" {
		enableTLS = envTLS == "true"
	}

	return &Config{
		Port:        port,
		EnableTLS:   enableTLS,
		ServiceName: "{{.ServiceName}}",
		Description: "{{.Description}}",
	}, nil
}
```

#### template/internal/server/server.go
```go
package server

import (
	"encoding/json"
	"fmt"
	"net/http"
	"time"

	"{{.ModuleName}}/internal/config"
)

type Server struct {
	config *config.Config
	server *http.Server
}

func New(cfg *config.Config) *Server {
	s := &Server{
		config: cfg,
	}

	mux := http.NewServeMux()
	mux.HandleFunc("/", s.handleHome)
	mux.HandleFunc("/health", s.handleHealth)
	mux.HandleFunc("/api/v1/info", s.handleInfo)

	s.server = &http.Server{
		Addr:         fmt.Sprintf(":%d", cfg.Port),
		Handler:      mux,
		ReadTimeout:  15 * time.Second,
		WriteTimeout: 15 * time.Second,
		IdleTimeout:  60 * time.Second,
	}

	return s
}

func (s *Server) ListenAndServe() error {
	return s.server.ListenAndServe()
}

func (s *Server) Shutdown(ctx context.Context) error {
	return s.server.Shutdown(ctx)
}

func (s *Server) handleHome(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodGet {
		http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
		return
	}

	fmt.Fprintf(w, "Welcome to %s!\n", s.config.ServiceName)
	fmt.Fprintf(w, "%s\n", s.config.Description)
}

func (s *Server) handleHealth(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodGet {
		http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
		return
	}

	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(map[string]string{
		"status":    "ok",
		"service":   s.config.ServiceName,
		"timestamp": time.Now().UTC().Format(time.RFC3339),
	})
}

func (s *Server) handleInfo(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodGet {
		http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
		return
	}

	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(map[string]interface{}{
		"service":     s.config.ServiceName,
		"description": s.config.Description,
		"version":     "1.0.0",
		"endpoints": []string{
			"/",
			"/health",
			"/api/v1/info",
		},
	})
}
```

## Library Template

### project.json
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
    }
  ]
}
```

### Template Files

#### template/{{.LibName}}.go
```go
package {{.LibName}}

import (
	"fmt"
)

// Library represents the main library instance
type Library struct {
	name        string
	description string
}

// New creates a new Library instance
func New(name, description string) *Library {
	return &Library{
		name:        name,
		description: description,
	}
}

// Name returns the library name
func (l *Library) Name() string {
	return l.name
}

// Description returns the library description
func (l *Library) Description() string {
	return l.description
}

// String returns a string representation of the library
func (l *Library) String() string {
	return fmt.Sprintf("%s: %s", l.name, l.description)
}

// Greet returns a greeting message
func (l *Library) Greet(who string) string {
	return fmt.Sprintf("Hello %s! Welcome to %s.", who, l.name)
}
```

#### template/{{.LibName}}_test.go
```go
package {{.LibName}}

import (
	"testing"
)

func TestNew(t *testing.T) {
	name := "test-lib"
	description := "A test library"

	lib := New(name, description)

	if lib.Name() != name {
		t.Errorf("Expected name %s, got %s", name, lib.Name())
	}

	if lib.Description() != description {
		t.Errorf("Expected description %s, got %s", description, lib.Description())
	}
}

func TestString(t *testing.T) {
	lib := New("test-lib", "A test library")
	expected := "test-lib: A test library"
	actual := lib.String()

	if actual != expected {
		t.Errorf("Expected %s, got %s", expected, actual)
	}
}

func TestGreet(t *testing.T) {
	lib := New("test-lib", "A test library")
	who := "World"
	expected := "Hello World! Welcome to test-lib."
	actual := lib.Greet(who)

	if actual != expected {
		t.Errorf("Expected %s, got %s", expected, actual)
	}
}

// ExampleNew demonstrates how to create a new Library instance
func ExampleNew() {
	lib := New("my-lib", "My awesome library")
	fmt.Println(lib.String())
	// Output: my-lib: My awesome library
}

// ExampleLibrary_Greet demonstrates how to use the Greet method
func ExampleLibrary_Greet() {
	lib := New("my-lib", "My awesome library")
	fmt.Println(lib.Greet("Alice"))
	// Output: Hello Alice! Welcome to my-lib.
}
```

#### template/go.mod
```go
module {{.ModuleName}}

go 1.21

require (
	// Add dependencies here
)
```

#### template/README.md
```markdown
# {{.LibName}}

{{.Description}}

## Installation

```bash
go get {{.ModuleName}}
```

## Usage

```go
package main

import (
    "fmt"
    "{{.ModuleName}}"
)

func main() {
    lib := {{.LibName}}.New("my-app", "My application")
    fmt.Println(lib.Greet("World"))

    // Output: Hello World! Welcome to my-app.
}
```

## API Documentation

### Functions

- `New(name, description string) *Library` - Creates a new Library instance

### Methods

- `(*Library) Name() string` - Returns the library name
- `(*Library) Description() string` - Returns the library description
- `(*Library) String() string` - Returns string representation
- `(*Library) Greet(who string) string` - Returns a greeting message

## Development

```bash
# Run tests
go test ./...

# Run tests with coverage
go test -cover ./...

# Run benchmarks
go test -bench=. ./...
```

## License

{{.License}}

## Author

{{.Author}}
```

## Microservice Template

### project.json
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
    }
  ]
}
```

### Template Files

#### template/cmd/{{.ServiceName}}/main.go
```go
package main

import (
	"context"
	"log"
	"net/http"
	"os"
	"os/signal"
	"syscall"
	"time"

	"{{.ModuleName}}/internal/config"
	"{{.ModuleName}}/internal/database"
	"{{.ModuleName}}/internal/grpcserver"
	"{{.ModuleName}}/internal/httpserver"
	"{{.ModuleName}}/internal/repository"
	"{{.ModuleName}}/internal/service"
)

func main() {
	// Load configuration
	cfg, err := config.Load()
	if err != nil {
		log.Fatalf("Failed to load configuration: %v", err)
	}

	// Initialize database
	db, err := database.New(cfg.DatabaseURL)
	if err != nil {
		log.Fatalf("Failed to connect to database: %v", err)
	}
	defer db.Close()

	// Initialize repositories
	repos := repository.New(db)

	// Initialize services
	services := service.New(repos)

	// Create servers
	httpServer := httpserver.New(cfg, services)
	grpcServer := grpcserver.New(cfg, services)

	// Start servers
	ctx, cancel := context.WithCancel(context.Background())
	defer cancel()

	// HTTP Server
	go func() {
		log.Printf("Starting HTTP server on port %d", cfg.HTTPPort)
		if err := httpServer.ListenAndServe(); err != nil && err != http.ErrServerClosed {
			log.Fatalf("HTTP server failed: %v", err)
		}
	}()

	// gRPC Server
	go func() {
		log.Printf("Starting gRPC server on port %d", cfg.GRPCPort)
		if err := grpcServer.ListenAndServe(); err != nil {
			log.Fatalf("gRPC server failed: %v", err)
		}
	}()

	// Wait for interrupt signal
	quit := make(chan os.Signal, 1)
	signal.Notify(quit, syscall.SIGINT, syscall.SIGTERM)
	<-quit

	log.Println("Shutting down servers...")

	// Graceful shutdown
	shutdownCtx, shutdownCancel := context.WithTimeout(context.Background(), 30*time.Second)
	defer shutdownCancel()

	if err := httpServer.Shutdown(shutdownCtx); err != nil {
		log.Printf("HTTP server shutdown error: %v", err)
	}

	grpcServer.GracefulStop()

	log.Println("Servers stopped")
}
```

#### template/Dockerfile
```dockerfile
# Build stage
FROM golang:1.21-alpine AS builder

WORKDIR /app
COPY go.mod go.sum ./
RUN go mod download

COPY . .
RUN CGO_ENABLED=0 GOOS=linux go build -o {{.ServiceName}} ./cmd/{{.ServiceName}}

# Runtime stage
FROM alpine:latest

RUN apk --no-cache add ca-certificates tzdata
WORKDIR /root/

COPY --from=builder /app/{{.ServiceName}} .
COPY --from=builder /app/configs ./configs

EXPOSE {{.Port}}

CMD ["./{{.ServiceName}}"]
```

#### template/docker-compose.yml
```yaml
version: '3.8'

services:
  {{.ServiceName}}:
    build: .
    ports:
      - "{{.Port}}:{{.Port}}"
      - "{{.GRPCPort}}:{{.GRPCPort}}"
    environment:
      - DATABASE_URL=postgres://user:password@postgres:5432/{{.ServiceName}}?sslmode=disable
      - REDIS_URL=redis://redis:6379
    depends_on:
      - postgres
      {{- if eq .EnableRedis "true"}}
      - redis
      {{- end}}
    restart: unless-stopped

  postgres:
    image: postgres:15-alpine
    environment:
      - POSTGRES_DB={{.ServiceName}}
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=password
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"
    restart: unless-stopped

{{- if eq .EnableRedis "true"}}
  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    restart: unless-stopped
{{- end}}

volumes:
  postgres_data:
```

These examples demonstrate various template patterns and can be used as starting points for creating custom boilr templates.