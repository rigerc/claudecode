---
name: go-env-parser
description: Use when working with github.com/caarlos0/env for parsing environment variables into Go structs. Covers struct tags, custom parsers, envFile/envExpand/envPrefix options, and troubleshooting.
---

# Go Environment Variable Parser Expert

Expert assistance for the github.com/caarlos0/env package, providing environment-based configuration management for Go applications.

## When to Use This Skill

Use this skill when you need help with:

- Creating configuration structures with env tags
- Implementing custom parsers for complex types
- Using advanced tag options (envFile, envExpand, envPrefix)
- Troubleshooting environment variable parsing issues
- Migrating from v2 to v3 with generics support
- Testing and validating configuration

## Quick Start

```go
import "github.com/caarlos0/env/v11"

type Config struct {
    Port    int    `env:"PORT" envDefault:"3000"`
    Debug   bool   `env:"DEBUG" envDefault:"false"`
    DBURL   string `env:"DATABASE_URL,required"`
}

func main() {
    cfg, err := env.ParseAs[Config]()
    if err != nil {
        log.Fatal(err)
    }
    // Use cfg...
}
```

## Available Resources

See `references/` for comprehensive documentation:

- **tag-reference.md**: Complete documentation of all struct tags and usage patterns
- **examples.md**: Real-world configuration examples for different application types
- **troubleshooting.md**: Common issues and solutions for environment variable parsing