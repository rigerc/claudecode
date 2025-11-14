# Koanf Configuration Management Guide

## Overview

[Koanf](https://github.com/knadh/koanf) is a lightweight, extensible Go library for reading configuration from various sources and formats. It provides a cleaner, more flexible alternative to Viper with better abstractions and extensibility.

### Key Features

- **Multiple Sources**: Load configuration from files, environment variables, command-line flags, structs, maps, AWS S3, Vault, Consul, etcd, and more
- **Multiple Formats**: Support for JSON, YAML, TOML, HCL, DotEnv, NestedText, and HJSON
- **Layered Configuration**: Merge configurations from multiple sources with custom merge strategies
- **File Watching**: Automatically reload configuration when files change
- **Type-Safe**: Strong typing with struct unmarshalling support
- **Lightweight**: Minimal dependencies and small binary footprint
- **Extensible**: Easy to create custom providers and parsers

## Installation

### Core Library

```bash
go get -u github.com/knadh/koanf/v2
```

### Providers

Install specific providers as needed:

```bash
# File provider
go get -u github.com/knadh/koanf/providers/file

# Environment variables provider
go get -u github.com/knadh/koanf/providers/env/v2

# Command-line flags provider
go get -u github.com/knadh/koanf/providers/posflag

# S3 provider
go get -u github.com/knadh/koanf/providers/s3

# Map provider
go get -u github.com/knadh/koanf/providers/confmap

# Struct provider
go get -u github.com/knadh/koanf/providers/structs

# Raw bytes provider
go get -u github.com/knadh/koanf/providers/rawbytes
```

### Parsers

Install parsers for your configuration formats:

```bash
# JSON parser
go get -u github.com/knadh/koanf/parsers/json

# YAML parser
go get -u github.com/knadh/koanf/parsers/yaml

# TOML parser
go get -u github.com/knadh/koanf/parsers/toml
# Or TOML v2
go get -u github.com/knadh/koanf/parsers/toml/v2

# HCL parser
go get -u github.com/knadh/koanf/parsers/hcl

# DotEnv parser
go get -u github.com/knadh/koanf/parsers/dotenv

# NestedText parser
go get -u github.com/knadh/koanf/parsers/nestedtext

# HJSON parser
go get -u github.com/knadh/koanf/parsers/hjson
```

## Getting Started

### Basic Usage

Load and merge configuration from JSON and YAML files:

```go
package main

import (
	"fmt"
	"log"

	"github.com/knadh/koanf/v2"
	"github.com/knadh/koanf/parsers/json"
	"github.com/knadh/koanf/parsers/yaml"
	"github.com/knadh/koanf/providers/file"
)

// Global koanf instance. Use "." as the key path delimiter.
var k = koanf.New(".")

func main() {
	// Load JSON config
	if err := k.Load(file.Provider("config.json"), json.Parser()); err != nil {
		log.Fatalf("error loading config: %v", err)
	}

	// Load YAML config and merge into the previously loaded config
	k.Load(file.Provider("config.yml"), yaml.Parser())

	// Access configuration values
	fmt.Println("parent's name is =", k.String("parent1.name"))
	fmt.Println("parent's ID is =", k.Int("parent1.id"))
}
```

### Configuration Delimiter

The delimiter (default: `"."`) is used to access nested configuration:

```go
// Using "." as delimiter
var k = koanf.New(".")
value := k.String("parent.child.key")

// Using "/" as delimiter
var k = koanf.New("/")
value := k.String("parent/child/key")
```

## Configuration Sources

### File Provider

Load configuration from local files:

```go
import (
	"github.com/knadh/koanf/providers/file"
	"github.com/knadh/koanf/parsers/json"
)

if err := k.Load(file.Provider("config.json"), json.Parser()); err != nil {
	log.Fatalf("error loading file: %v", err)
}
```

### Environment Variables

Load configuration from environment variables with prefix filtering and transformation:

```go
import (
	"strings"
	"github.com/knadh/koanf/providers/env/v2"
)

// Load environment variables with prefix "MYVAR_"
// Transform: MYVAR_PARENT1_CHILD1_NAME -> parent1.child1.name
k.Load(env.Provider(".", env.Opt{
	Prefix: "MYVAR_",
	TransformFunc: func(k, v string) (string, any) {
		// Convert to lowercase and replace _ with .
		k = strings.ReplaceAll(
			strings.ToLower(strings.TrimPrefix(k, "MYVAR_")),
			"_",
			".",
		)

		// Transform space-separated values into slices
		// MYVAR_TAGS="foo bar baz" -> tags: ["foo", "bar", "baz"]
		if strings.Contains(v, " ") {
			return k, strings.Split(v, " ")
		}

		return k, v
	},
}), nil)
```

### Command-Line Flags

Integrate with `spf13/pflag` for POSIX-compliant command-line flags:

```go
import (
	"github.com/knadh/koanf/providers/posflag"
	flag "github.com/spf13/pflag"
)

f := flag.NewFlagSet("config", flag.ContinueOnError)
f.StringSlice("conf", []string{"config.toml"}, "path to config files")
f.String("time", "2020-01-01", "a time string")
f.String("type", "xxx", "type of the app")
f.Parse(os.Args[1:])

// Load config files from command line
cFiles, _ := f.GetStringSlice("conf")
for _, c := range cFiles {
	if err := k.Load(file.Provider(c), toml.Parser()); err != nil {
		log.Fatalf("error loading file: %v", err)
	}
}

// Override with command-line flags
if err := k.Load(posflag.Provider(f, ".", k), nil); err != nil {
	log.Fatalf("error loading config: %v", err)
}
```

For Go's standard `flag` package, use `basicflag.Provider` instead.

### Map Provider

Load configuration from a Go map:

```go
import "github.com/knadh/koanf/providers/confmap"

// Load default values from a flat map
k.Load(confmap.Provider(map[string]interface{}{
	"parent1.name": "Default Name",
	"parent3.name": "New name here",
}, "."), nil)
```

### Struct Provider

Load configuration from a Go struct:

```go
import "github.com/knadh/koanf/providers/structs"

type Config struct {
	Type    string `koanf:"type"`
	Parent1 struct {
		Name string `koanf:"name"`
		ID   int    `koanf:"id"`
		Child1 struct {
			Name string `koanf:"name"`
			Type string `koanf:"type"`
		} `koanf:"child1"`
	} `koanf:"parent1"`
}

cfg := Config{
	Type: "json",
	// ... initialize fields
}

k.Load(structs.Provider(cfg, "koanf"), nil)
```

### Raw Bytes Provider

Load configuration from a byte slice:

```go
import (
	"github.com/knadh/koanf/providers/rawbytes"
	"github.com/knadh/koanf/parsers/json"
)

b := []byte(`{"type": "rawbytes", "parent1": {"child1": {"type": "rawbytes"}}}`)
k.Load(rawbytes.Provider(b), json.Parser())
```

### AWS S3 Provider

Load configuration from AWS S3:

```go
import "github.com/knadh/koanf/providers/s3"

if err := k.Load(s3.Provider(s3.Config{
	AccessKey: os.Getenv("AWS_S3_ACCESS_KEY"),
	SecretKey: os.Getenv("AWS_S3_SECRET_KEY"),
	Region:    os.Getenv("AWS_S3_REGION"),
	Bucket:    os.Getenv("AWS_S3_BUCKET"),
	ObjectKey: "dir/config.json",
}), json.Parser()); err != nil {
	log.Fatalf("error loading config: %v", err)
}
```

### Third-Party Providers

Additional providers available:

- **Vault**: Hashicorp Vault provider
- **AppConfig**: AWS AppConfig provider
- **etcd**: CNCF etcd provider
- **Consul**: Hashicorp Consul provider
- **Parameter Store**: AWS Systems Manager Parameter Store
- **Secrets Manager**: AWS Secrets Manager

## Configuration Merging

### Basic Merging

Load multiple configuration sources and merge them:

```go
// Load defaults
k.Load(confmap.Provider(map[string]interface{}{
	"parent1.name": "Default Name",
}, "."), nil)

// Load from file (overrides defaults)
k.Load(file.Provider("config.json"), json.Parser())

// Load from environment (overrides file config)
k.Load(env.Provider("MYAPP_", ".", nil), nil)

// Load from flags (final overrides)
k.Load(posflag.Provider(f, ".", k), nil)
```

### Strict Merge Mode

Enable strict merging to prevent type conflicts:

```go
var conf = koanf.Conf{
	Delim:       ".",
	StrictMerge: true,
}
var k = koanf.NewWithConf(conf)

// This will error if types conflict during merge
if err := k.Load(file.Provider("config.json"), json.Parser()); err != nil {
	log.Fatalf("error loading config: %v", err)
}
```

### Custom Merge Function

Define custom merge logic:

```go
k.Load(file.Provider("config.json"), json.Parser(), koanf.WithMergeFunc(
	func(src, dest map[string]interface{}) error {
		// Custom merge logic
		// Copy values from src into dest as needed
		return nil
	},
))
```

## File Watching

Automatically reload configuration when files change:

```go
// Load initial config
f := file.Provider("config.json")
if err := k.Load(f, json.Parser()); err != nil {
	log.Fatalf("error loading config: %v", err)
}

// Watch for changes
f.Watch(func(event interface{}, err error) {
	if err != nil {
		log.Printf("watch error: %v", err)
		return
	}

	// Reload configuration
	log.Println("config changed. Reloading...")
	k = koanf.New(".")
	k.Load(f, json.Parser())
	k.Print()
})

// Stop watching when done
// f.Unwatch()
```

Providers that support watching:
- `file`
- `appconfig`
- `vault`
- `consul`

## Accessing Configuration

### Basic Access Methods

```go
// String values
name := k.String("parent1.name")

// Integer values
id := k.Int("parent1.id")

// Boolean values
enabled := k.Bool("feature.enabled")

// Float values
price := k.Float64("product.price")

// Time values
timestamp := k.Time("event.timestamp", time.RFC3339)

// Duration values
timeout := k.Duration("server.timeout")

// Slice values
tags := k.Strings("metadata.tags")
ids := k.Ints("user.ids")

// Map values
metadata := k.StringMap("app.metadata")

// Check if key exists
if k.Exists("parent1.name") {
	// Key exists
}
```

## Unmarshalling

### Basic Unmarshalling

Unmarshal configuration into structs:

```go
type Config struct {
	Name string `koanf:"name"`
	Type string `koanf:"type"`
	GrandChild struct {
		Ids []int `koanf:"ids"`
		On  bool  `koanf:"on"`
	} `koanf:"grandchild1"`
}

var cfg Config

// Unmarshal a specific path
k.Unmarshal("parent1.child1", &cfg)

// Unmarshal with custom config
k.UnmarshalWithConf("parent1.child1", &cfg, koanf.UnmarshalConf{
	Tag: "koanf",
})
```

### Flat Path Unmarshalling

Unmarshal nested configuration into flat structs:

```go
type FlatConfig struct {
	Type                        string `koanf:"type"`
	Parent1Name                 string `koanf:"parent1.name"`
	Parent1ID                   int    `koanf:"parent1.id"`
	Parent1Child1Name           string `koanf:"parent1.child1.name"`
	Parent1Child1Grandchild1IDs []int  `koanf:"parent1.child1.grandchild1.ids"`
}

var cfg FlatConfig
k.UnmarshalWithConf("", &cfg, koanf.UnmarshalConf{
	Tag:       "koanf",
	FlatPaths: true,
})
```

### Default Decoder Configuration

Koanf uses `mapstructure` with the following defaults:

```go
mapstructure.DecoderConfig{
	WeaklyTypedInput: true,  // Flexible type conversions
	TagName:          "koanf", // Struct tag name
}
```

## Marshalling

Convert koanf instance back to bytes:

```go
// Marshal to JSON
b, err := k.Marshal(json.Parser())
if err != nil {
	log.Fatalf("error marshalling: %v", err)
}
fmt.Println(string(b))

// Marshal to YAML
b, err := k.Marshal(yaml.Parser())
if err != nil {
	log.Fatalf("error marshalling: %v", err)
}
fmt.Println(string(b))
```

## Parsers

### Available Parsers

```go
// JSON
json.Parser()

// YAML
yaml.Parser()

// TOML
toml.Parser()

// TOML v2
tomlv2.Parser()

// HCL (Hashicorp Configuration Language)
hcl.Parser(flattenSlices bool) // Set flattenSlices to true

// DotEnv
dotenv.Parser()

// NestedText
nestedtext.Parser()

// HJSON (Human JSON)
hjson.Parser()
```

### Parser Usage

Parsers convert configuration bytes into nested or flat Go maps:

```go
// Nested map (most formats)
k.Load(file.Provider("config.yaml"), yaml.Parser())

// Flat map (DotEnv, NestedText)
k.Load(file.Provider(".env"), dotenv.Parser())
```

## Best Practices

### 1. Layered Configuration Strategy

Load configuration in order of precedence:

```go
func loadConfig() error {
	// 1. Load defaults from struct
	k.Load(structs.Provider(defaultConfig, "koanf"), nil)

	// 2. Load from config file
	if err := k.Load(file.Provider("config.yaml"), yaml.Parser()); err != nil {
		return err
	}

	// 3. Load from environment variables
	k.Load(env.Provider("APP_", ".", func(s string) string {
		return strings.ToLower(strings.TrimPrefix(s, "APP_"))
	}), nil)

	// 4. Load from command-line flags (highest priority)
	return k.Load(posflag.Provider(flags, ".", k), nil)
}
```

### 2. Configuration Validation

Validate configuration after loading:

```go
type Config struct {
	Server struct {
		Host string `koanf:"host"`
		Port int    `koanf:"port"`
	} `koanf:"server"`
}

var cfg Config
if err := k.Unmarshal("", &cfg); err != nil {
	return fmt.Errorf("failed to unmarshal config: %w", err)
}

// Validate
if cfg.Server.Port < 1 || cfg.Server.Port > 65535 {
	return fmt.Errorf("invalid port: %d", cfg.Server.Port)
}
```

### 3. Error Handling

Always handle errors when loading configuration:

```go
if err := k.Load(file.Provider("config.yaml"), yaml.Parser()); err != nil {
	log.Fatalf("error loading config: %v", err)
}
```

### 4. Use Struct Tags

Use struct tags for clear mapping:

```go
type Config struct {
	ServerHost string `koanf:"server.host"`
	ServerPort int    `koanf:"server.port"`
}
```

### 5. Thread Safety

When using file watching, ensure thread-safe access:

```go
var (
	k    *koanf.Koanf
	mu   sync.RWMutex
)

func getConfig() *koanf.Koanf {
	mu.RLock()
	defer mu.RUnlock()
	return k
}

func reloadConfig() {
	mu.Lock()
	defer mu.Unlock()
	k = koanf.New(".")
	k.Load(f, json.Parser())
}
```

## Common Patterns

### Environment-Specific Configuration

```go
env := os.Getenv("APP_ENV")
if env == "" {
	env = "development"
}

// Load base config
k.Load(file.Provider("config.yaml"), yaml.Parser())

// Load environment-specific overrides
envFile := fmt.Sprintf("config.%s.yaml", env)
k.Load(file.Provider(envFile), yaml.Parser())
```

### Optional Configuration Files

```go
if _, err := os.Stat("config.yaml"); err == nil {
	if err := k.Load(file.Provider("config.yaml"), yaml.Parser()); err != nil {
		log.Fatalf("error loading config: %v", err)
	}
}
```

### Configuration with Defaults

```go
// Get string with default
host := k.String("server.host")
if host == "" {
	host = "localhost"
}

// Or use map defaults
k.Load(confmap.Provider(map[string]interface{}{
	"server.host": "localhost",
	"server.port": 8080,
}, "."), nil)
```

## Comparison with Viper

Koanf offers several advantages over Viper:

### Binary Size

- **Standard Go (json)**: ~2MB
- **Koanf**: ~2.5MB
- **Viper**: ~3.5MB

### Dependencies

- **Standard Go**: 0 external dependencies
- **Koanf**: Minimal dependencies
- **Viper**: Many transitive dependencies

### Design Philosophy

- **Koanf**: Minimal, composable, explicit
- **Viper**: Feature-rich, implicit, opinionated

### Use Koanf When

- You need a lightweight configuration solution
- You want explicit control over configuration loading
- You need custom providers or parsers
- Binary size matters

### Use Viper When

- You need all-in-one configuration management
- You prefer convention over configuration
- You're already using Viper in your project

## Troubleshooting

### Configuration Not Loading

1. Check file paths are correct
2. Verify parser matches file format
3. Ensure proper error handling
4. Check file permissions

### Type Conflicts During Merge

Enable strict merge to catch conflicts:

```go
var k = koanf.NewWithConf(koanf.Conf{
	Delim:       ".",
	StrictMerge: true,
})
```

### Environment Variables Not Working

1. Verify prefix matches your env vars
2. Check transform function is correct
3. Ensure env vars are exported

### Unmarshalling Errors

1. Check struct tags match configuration paths
2. Verify types are compatible
3. Use `FlatPaths: true` for deeply nested configs
4. Enable `WeaklyTypedInput` for type flexibility

## Additional Resources

- [GitHub Repository](https://github.com/knadh/koanf)
- [API Documentation](https://pkg.go.dev/github.com/knadh/koanf/v2)
- [Examples](https://github.com/knadh/koanf/tree/master/examples)
- [Comparison with Viper](https://github.com/knadh/koanf/wiki/Comparison-with-spf13-viper)

## License

Koanf is released under the MIT License.
