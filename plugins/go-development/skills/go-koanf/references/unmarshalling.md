# Unmarshalling Configuration

## Basic Unmarshalling

### Simple Struct

```go
type Config struct {
    Name string `koanf:"name"`
    Type string `koanf:"type"`
}

var cfg Config

// Unmarshal entire config
if err := k.Unmarshal("", &cfg); err != nil {
    log.Fatalf("error unmarshalling: %v", err)
}

// Unmarshal specific path
if err := k.Unmarshal("server", &cfg); err != nil {
    log.Fatalf("error unmarshalling: %v", err)
}
```

### Nested Struct

```go
type ServerConfig struct {
    Host string `koanf:"host"`
    Port int    `koanf:"port"`
    TLS  struct {
        Enabled  bool   `koanf:"enabled"`
        CertFile string `koanf:"cert_file"`
        KeyFile  string `koanf:"key_file"`
    } `koanf:"tls"`
}

var cfg ServerConfig
k.Unmarshal("server", &cfg)
```

## Flat Path Unmarshalling

For deeply nested configurations, use flat paths:

```go
type FlatConfig struct {
    ServerHost          string `koanf:"server.host"`
    ServerPort          int    `koanf:"server.port"`
    ServerTLSEnabled    bool   `koanf:"server.tls.enabled"`
    ServerTLSCert       string `koanf:"server.tls.cert_file"`
    DatabaseURL         string `koanf:"database.url"`
    DatabaseMaxConns    int    `koanf:"database.max_connections"`
}

var cfg FlatConfig
k.UnmarshalWithConf("", &cfg, koanf.UnmarshalConf{
    Tag:       "koanf",
    FlatPaths: true,
})
```

## Custom Unmarshalling

### With DecoderConfig

```go
import "github.com/mitchellh/mapstructure"

var cfg Config
k.UnmarshalWithConf("", &cfg, koanf.UnmarshalConf{
    Tag: "koanf",
    DecoderConfig: &mapstructure.DecoderConfig{
        WeaklyTypedInput: true,
        Result:          &cfg,
        TagName:         "koanf",
        DecodeHook: mapstructure.ComposeDecodeHookFunc(
            mapstructure.StringToTimeDurationHookFunc(),
            mapstructure.StringToTimeHookFunc(time.RFC3339),
        ),
    },
})
```

## Configuration Validation

### Basic Validation

```go
type Config struct {
    Server struct {
        Host string `koanf:"host"`
        Port int    `koanf:"port"`
    } `koanf:"server"`
}

func (c *Config) Validate() error {
    if c.Server.Host == "" {
        return fmt.Errorf("server.host is required")
    }

    if c.Server.Port < 1 || c.Server.Port > 65535 {
        return fmt.Errorf("invalid port: %d", c.Server.Port)
    }

    return nil
}

// Usage
var cfg Config
if err := k.Unmarshal("", &cfg); err != nil {
    return fmt.Errorf("unmarshal error: %w", err)
}

if err := cfg.Validate(); err != nil {
    return fmt.Errorf("invalid config: %w", err)
}
```

### Advanced Validation

```go
import "github.com/go-playground/validator/v10"

type Config struct {
    Server struct {
        Host string `koanf:"host" validate:"required,hostname"`
        Port int    `koanf:"port" validate:"required,min=1,max=65535"`
    } `koanf:"server" validate:"required"`

    Database struct {
        URL string `koanf:"url" validate:"required,url"`
    } `koanf:"database" validate:"required"`
}

func (c *Config) Validate() error {
    validate := validator.New()
    return validate.Struct(c)
}
```

## Type Conversion

### Duration Fields

```go
import "time"

type Config struct {
    Timeout time.Duration `koanf:"timeout"`
    TTL     time.Duration `koanf:"ttl"`
}

// In YAML: timeout: 30s

var cfg Config
k.Unmarshal("", &cfg)
// cfg.Timeout is now 30 * time.Second
```

### Time Fields

```go
type Config struct {
    CreatedAt time.Time `koanf:"created_at"`
}

// In YAML: created_at: "2024-01-01T00:00:00Z"

var cfg Config
k.UnmarshalWithConf("", &cfg, koanf.UnmarshalConf{
    Tag: "koanf",
    DecoderConfig: &mapstructure.DecoderConfig{
        DecodeHook: mapstructure.StringToTimeHookFunc(time.RFC3339),
        Result:     &cfg,
        TagName:    "koanf",
    },
})
```

### Slice Fields

```go
type Config struct {
    Tags        []string `koanf:"tags"`
    Ports       []int    `koanf:"ports"`
    AllowedIPs  []string `koanf:"allowed_ips"`
}

// In YAML:
// tags:
//   - foo
//   - bar
// ports: [8080, 8081, 8082]
```

### Map Fields

```go
type Config struct {
    Metadata   map[string]string      `koanf:"metadata"`
    Settings   map[string]interface{} `koanf:"settings"`
}

// In YAML:
// metadata:
//   env: production
//   region: us-west-2
```

## Unmarshalling Patterns

### Configuration with Defaults

```go
type Config struct {
    Server struct {
        Host string `koanf:"host"`
        Port int    `koanf:"port"`
    } `koanf:"server"`
}

func LoadConfig() (*Config, error) {
    // Set defaults
    cfg := &Config{}
    cfg.Server.Host = "localhost"
    cfg.Server.Port = 8080

    // Load from koanf (overrides defaults)
    if err := k.Unmarshal("", cfg); err != nil {
        return nil, err
    }

    return cfg, nil
}
```

### Partial Unmarshalling

```go
// Only unmarshal server config
var serverCfg ServerConfig
k.Unmarshal("server", &serverCfg)

// Only unmarshal database config
var dbCfg DatabaseConfig
k.Unmarshal("database", &dbCfg)
```

### Multi-Environment Configuration

```go
type Config struct {
    Environment string `koanf:"environment"`
    Server      struct {
        Host string `koanf:"host"`
        Port int    `koanf:"port"`
    } `koanf:"server"`
}

func (c *Config) IsDevelopment() bool {
    return c.Environment == "development"
}

func (c *Config) IsProduction() bool {
    return c.Environment == "production"
}
```

## Common Patterns

### Configuration Factory

```go
func NewConfig() (*Config, error) {
    var cfg Config

    if err := k.Unmarshal("", &cfg); err != nil {
        return nil, fmt.Errorf("unmarshal error: %w", err)
    }

    if err := cfg.Validate(); err != nil {
        return nil, fmt.Errorf("validation error: %w", err)
    }

    return &cfg, nil
}
```

### Singleton Pattern

```go
var (
    once     sync.Once
    instance *Config
)

func GetConfig() *Config {
    once.Do(func() {
        var cfg Config
        if err := k.Unmarshal("", &cfg); err != nil {
            log.Fatalf("failed to load config: %v", err)
        }
        instance = &cfg
    })
    return instance
}
```

### Dynamic Reloading

```go
var (
    currentConfig *Config
    configMutex   sync.RWMutex
)

func GetConfig() *Config {
    configMutex.RLock()
    defer configMutex.RUnlock()
    return currentConfig
}

func ReloadConfig() error {
    var cfg Config
    if err := k.Unmarshal("", &cfg); err != nil {
        return err
    }

    if err := cfg.Validate(); err != nil {
        return err
    }

    configMutex.Lock()
    currentConfig = &cfg
    configMutex.Unlock()

    return nil
}
```

## Troubleshooting

### Type Mismatch Errors

**Problem**: Unmarshal fails with type errors

**Solution**: Ensure struct field types match configuration values
```go
// Wrong: port is string in YAML but int in struct
type Config struct {
    Port int `koanf:"port"` // YAML has "port: \"8080\""
}

// Fix: Use string or convert in YAML
type Config struct {
    Port int `koanf:"port"` // YAML has "port: 8080" (no quotes)
}
```

### Missing Required Fields

**Problem**: Fields are zero-value after unmarshal

**Solution**: Check struct tags and configuration paths match exactly
```go
// Configuration path: server.host
// Struct tag must match
type Config struct {
    ServerHost string `koanf:"server.host"` // Correct with FlatPaths
    // OR
    Server struct {
        Host string `koanf:"host"` // Correct with nested struct
    } `koanf:"server"`
}
```

### Tag Not Found

**Problem**: Koanf ignores fields

**Solution**: Ensure correct tag name is used
```go
// Default tag name is "koanf"
type Config struct {
    Host string `koanf:"host"` // Correct
    Port int    `json:"port"`  // Wrong - will be ignored
}
```
