# Koanf Quick Reference

## Installation

```bash
# Core
go get -u github.com/knadh/koanf/v2

# Providers
go get -u github.com/knadh/koanf/providers/file
go get -u github.com/knadh/koanf/providers/env/v2
go get -u github.com/knadh/koanf/providers/posflag
go get -u github.com/knadh/koanf/providers/confmap
go get -u github.com/knadh/koanf/providers/structs

# Parsers
go get -u github.com/knadh/koanf/parsers/yaml
go get -u github.com/knadh/koanf/parsers/json
go get -u github.com/knadh/koanf/parsers/toml
```

## Basic Initialization

```go
import "github.com/knadh/koanf/v2"

// Standard initialization
var k = koanf.New(".")

// With configuration
var k = koanf.NewWithConf(koanf.Conf{
    Delim:       ".",
    StrictMerge: true,
})
```

## Loading Configuration

### From File
```go
k.Load(file.Provider("config.yaml"), yaml.Parser())
```

### From Environment
```go
k.Load(env.Provider("APP_", ".", func(s string) string {
    return strings.Replace(strings.ToLower(
        strings.TrimPrefix(s, "APP_")), "_", ".", -1)
}), nil)
```

### From Flags
```go
k.Load(posflag.Provider(flagSet, ".", k), nil)
```

### From Map
```go
k.Load(confmap.Provider(map[string]interface{}{
    "key": "value",
}, "."), nil)
```

## Accessing Values

```go
k.String("path.to.key")           // String
k.Int("path.to.key")              // Int
k.Int64("path.to.key")            // Int64
k.Bool("path.to.key")             // Bool
k.Float64("path.to.key")          // Float64
k.Duration("path.to.key")         // time.Duration
k.Time("path.to.key", layout)     // time.Time
k.Strings("path.to.key")          // []string
k.Ints("path.to.key")             // []int
k.StringMap("path.to.key")        // map[string]any
k.Exists("path.to.key")           // bool
k.Get("path.to.key")              // interface{}
```

## Unmarshalling

```go
type Config struct {
    Host string `koanf:"host"`
    Port int    `koanf:"port"`
}

var cfg Config

// Basic unmarshal
k.Unmarshal("server", &cfg)

// With configuration
k.UnmarshalWithConf("server", &cfg, koanf.UnmarshalConf{
    Tag:       "koanf",
    FlatPaths: true,
})
```

## File Watching

```go
f := file.Provider("config.yaml")
k.Load(f, yaml.Parser())

f.Watch(func(event interface{}, err error) {
    if err != nil {
        log.Printf("watch error: %v", err)
        return
    }
    // Reload configuration
    k = koanf.New(".")
    k.Load(f, yaml.Parser())
})

// Stop watching
f.Unwatch()
```

## Common Patterns

### Layered Configuration
```go
// 1. Defaults
k.Load(confmap.Provider(defaults, "."), nil)
// 2. File
k.Load(file.Provider("config.yaml"), yaml.Parser())
// 3. Environment
k.Load(env.Provider("APP_", ".", transform), nil)
// 4. Flags
k.Load(posflag.Provider(f, ".", k), nil)
```

### Environment-Specific
```go
env := os.Getenv("ENV")
k.Load(file.Provider("config.yaml"), yaml.Parser())
k.Load(file.Provider(fmt.Sprintf("config.%s.yaml", env)), yaml.Parser())
```

### Optional Files
```go
if _, err := os.Stat("config.yaml"); err == nil {
    k.Load(file.Provider("config.yaml"), yaml.Parser())
}
```

## Providers

| Provider | Import Path | Usage |
|----------|-------------|-------|
| File | `github.com/knadh/koanf/providers/file` | Local files |
| Env | `github.com/knadh/koanf/providers/env/v2` | Environment variables |
| Posflag | `github.com/knadh/koanf/providers/posflag` | pflag (POSIX) |
| Basicflag | `github.com/knadh/koanf/providers/basicflag` | Go flag package |
| Confmap | `github.com/knadh/koanf/providers/confmap` | Go maps |
| Structs | `github.com/knadh/koanf/providers/structs` | Go structs |
| Rawbytes | `github.com/knadh/koanf/providers/rawbytes` | Byte slices |
| S3 | `github.com/knadh/koanf/providers/s3` | AWS S3 |

## Parsers

| Parser | Import Path | Format |
|--------|-------------|--------|
| JSON | `github.com/knadh/koanf/parsers/json` | JSON |
| YAML | `github.com/knadh/koanf/parsers/yaml` | YAML |
| TOML | `github.com/knadh/koanf/parsers/toml` | TOML v1 |
| TOML v2 | `github.com/knadh/koanf/parsers/toml/v2` | TOML v2 |
| HCL | `github.com/knadh/koanf/parsers/hcl` | HashiCorp Config |
| DotEnv | `github.com/knadh/koanf/parsers/dotenv` | .env files |
| NestedText | `github.com/knadh/koanf/parsers/nestedtext` | NestedText |
| HJSON | `github.com/knadh/koanf/parsers/hjson` | Human JSON |

## Error Handling

```go
// Always check errors on Load
if err := k.Load(file.Provider("config.yaml"), yaml.Parser()); err != nil {
    log.Fatalf("error loading config: %v", err)
}

// Always check errors on Unmarshal
if err := k.Unmarshal("", &cfg); err != nil {
    log.Fatalf("error unmarshalling: %v", err)
}
```

## Thread-Safe Configuration

```go
var (
    k  *koanf.Koanf
    mu sync.RWMutex
)

func Get(key string) string {
    mu.RLock()
    defer mu.RUnlock()
    return k.String(key)
}

func Reload() {
    mu.Lock()
    defer mu.Unlock()
    k = koanf.New(".")
    k.Load(file.Provider("config.yaml"), yaml.Parser())
}
```

## Marshalling

```go
// Convert koanf instance back to bytes
b, err := k.Marshal(json.Parser())
if err != nil {
    log.Fatalf("error marshalling: %v", err)
}
fmt.Println(string(b))
```

## Debugging

```go
// Print all configuration
k.Print()

// Get raw map
all := k.All()
fmt.Printf("%+v\n", all)

// Check specific path
if !k.Exists("server.host") {
    log.Println("server.host not found")
}

// Get with type assertion
if val := k.Get("server"); val != nil {
    fmt.Printf("server config: %+v\n", val)
}
```
