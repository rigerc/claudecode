---
name: go-koanf
description: Use when implementing Go configuration management with Koanf. Load from files, env vars, flags with hot-reloading and type-safe unmarshalling.
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Grep
  - Glob
---

# Koanf Configuration Management

## When to Use

- Setting up configuration for Go applications
- Loading from multiple sources (files, env, flags)
- Hot-reloading configuration
- Migrating from Viper

## Quick Start

```go
import (
    "github.com/knadh/koanf/v2"
    "github.com/knadh/koanf/parsers/yaml"
    "github.com/knadh/koanf/providers/file"
)

var k = koanf.New(".")

// Load config
k.Load(file.Provider("config.yaml"), yaml.Parser())

// Access values
host := k.String("server.host")
port := k.Int("server.port")
```

## Implementation Guide

1. **Install**: `go get -u github.com/knadh/koanf/v2` + providers/parsers
2. **Choose template**: Use `templates/basic_config.go`, `layered_config.go`, or `file_watching.go`
3. **Load configuration**: File → Env → Flags (in order of precedence)
4. **Unmarshal & validate**: Always validate after unmarshalling

## Detailed Documentation

- `references/quick_reference.md` - Commands and common patterns
- `references/configuration_loading.md` - Loading from sources
- `references/unmarshalling.md` - Type-safe structs
- `references/file_watching.md` - Hot-reloading
- `references/troubleshooting.md` - Common issues
- `references/migration.md` - Migrating from Viper

## Templates

- `templates/basic_config.go` - Simple file-based config
- `templates/layered_config.go` - Multi-source with precedence
- `templates/file_watching.go` - Hot-reloading with thread safety
- `templates/config.yaml` - Example configuration
