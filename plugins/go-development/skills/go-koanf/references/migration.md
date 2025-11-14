# Migrating from Viper to Koanf

## Why Migrate?

### Binary Size Comparison

- **Standard Go (json)**: ~2MB
- **Koanf**: ~2.5MB
- **Viper**: ~3.5MB

### Dependencies

- **Standard Go**: 0 external dependencies
- **Koanf**: Minimal dependencies (mapstructure, fsnotify)
- **Viper**: Many transitive dependencies

### Design Philosophy

- **Koanf**: Minimal, composable, explicit control
- **Viper**: Feature-rich, implicit, opinionated

## Key Differences

| Feature | Viper | Koanf |
|---------|-------|-------|
| Global instance | `viper.Get()` | Create your own `k := koanf.New()` |
| Auto environment | `viper.AutomaticEnv()` | Explicit `k.Load(env.Provider())` |
| File watching | Built-in `viper.WatchConfig()` | Per-provider `f.Watch()` |
| Defaults | `viper.SetDefault()` | Load map with `confmap.Provider()` |
| Access | `viper.GetString()` | `k.String()` |
| Config paths | `viper.AddConfigPath()` | Explicit file paths |
| Merge | Automatic | Explicit `Load()` calls |

## Migration Guide

### Step 1: Replace Imports

**Before (Viper)**:
```go
import "github.com/spf13/viper"
```

**After (Koanf)**:
```go
import (
    "github.com/knadh/koanf/v2"
    "github.com/knadh/koanf/parsers/yaml"
    "github.com/knadh/koanf/providers/file"
    "github.com/knadh/koanf/providers/env/v2"
)
```

### Step 2: Replace Global Instance

**Before (Viper)**:
```go
viper.SetConfigName("config")
viper.SetConfigType("yaml")
viper.AddConfigPath(".")
viper.AddConfigPath("/etc/myapp/")
viper.ReadInConfig()
```

**After (Koanf)**:
```go
var k = koanf.New(".")

// Try multiple paths
for _, path := range []string{"config.yaml", "/etc/myapp/config.yaml"} {
    if _, err := os.Stat(path); err == nil {
        if err := k.Load(file.Provider(path), yaml.Parser()); err == nil {
            break
        }
    }
}
```

### Step 3: Replace Defaults

**Before (Viper)**:
```go
viper.SetDefault("server.host", "localhost")
viper.SetDefault("server.port", 8080)
```

**After (Koanf)**:
```go
k.Load(confmap.Provider(map[string]interface{}{
    "server.host": "localhost",
    "server.port": 8080,
}, "."), nil)
```

### Step 4: Replace Environment Binding

**Before (Viper)**:
```go
viper.SetEnvPrefix("MYAPP")
viper.AutomaticEnv()
viper.SetEnvKeyReplacer(strings.NewReplacer(".", "_"))
```

**After (Koanf)**:
```go
k.Load(env.Provider("MYAPP_", ".", func(s string) string {
    return strings.Replace(
        strings.ToLower(strings.TrimPrefix(s, "MYAPP_")),
        "_", ".", -1,
    )
}), nil)
```

### Step 5: Replace Value Access

**Before (Viper)**:
```go
host := viper.GetString("server.host")
port := viper.GetInt("server.port")
enabled := viper.GetBool("feature.enabled")
timeout := viper.GetDuration("timeout")
tags := viper.GetStringSlice("tags")
```

**After (Koanf)**:
```go
host := k.String("server.host")
port := k.Int("server.port")
enabled := k.Bool("feature.enabled")
timeout := k.Duration("timeout")
tags := k.Strings("tags")
```

### Step 6: Replace Unmarshalling

**Before (Viper)**:
```go
var cfg Config
viper.Unmarshal(&cfg)
```

**After (Koanf)**:
```go
var cfg Config
k.Unmarshal("", &cfg)
```

### Step 7: Replace File Watching

**Before (Viper)**:
```go
viper.WatchConfig()
viper.OnConfigChange(func(e fsnotify.Event) {
    log.Println("Config file changed:", e.Name)
    // Config is automatically reloaded
})
```

**After (Koanf)**:
```go
f := file.Provider("config.yaml")
k.Load(f, yaml.Parser())

f.Watch(func(event interface{}, err error) {
    if err != nil {
        log.Printf("watch error: %v", err)
        return
    }

    // Must explicitly reload
    k = koanf.New(".")
    k.Load(f, yaml.Parser())
    log.Println("Config reloaded")
})
```

## Complete Migration Example

### Before (Viper)

```go
package main

import (
    "fmt"
    "log"
    "strings"

    "github.com/spf13/viper"
)

type Config struct {
    Server struct {
        Host string
        Port int
    }
    Database struct {
        URL string
    }
}

func main() {
    // Set defaults
    viper.SetDefault("server.host", "localhost")
    viper.SetDefault("server.port", 8080)

    // Read config file
    viper.SetConfigName("config")
    viper.SetConfigType("yaml")
    viper.AddConfigPath(".")

    if err := viper.ReadInConfig(); err != nil {
        log.Fatalf("error reading config: %v", err)
    }

    // Environment variables
    viper.SetEnvPrefix("MYAPP")
    viper.AutomaticEnv()
    viper.SetEnvKeyReplacer(strings.NewReplacer(".", "_"))

    // Watch for changes
    viper.WatchConfig()
    viper.OnConfigChange(func(e fsnotify.Event) {
        log.Println("Config changed")
    })

    // Access values
    host := viper.GetString("server.host")
    port := viper.GetInt("server.port")

    // Unmarshal
    var cfg Config
    viper.Unmarshal(&cfg)

    fmt.Printf("Server: %s:%d\n", host, port)
}
```

### After (Koanf)

```go
package main

import (
    "fmt"
    "log"
    "strings"
    "sync"

    "github.com/knadh/koanf/parsers/yaml"
    "github.com/knadh/koanf/providers/confmap"
    "github.com/knadh/koanf/providers/env/v2"
    "github.com/knadh/koanf/providers/file"
    "github.com/knadh/koanf/v2"
)

type Config struct {
    Server struct {
        Host string `koanf:"host"`
        Port int    `koanf:"port"`
    } `koanf:"server"`
    Database struct {
        URL string `koanf:"url"`
    } `koanf:"database"`
}

var (
    k  *koanf.Koanf
    mu sync.RWMutex
    f  *file.File
)

func main() {
    k = koanf.New(".")

    // 1. Load defaults
    k.Load(confmap.Provider(map[string]interface{}{
        "server.host": "localhost",
        "server.port": 8080,
    }, "."), nil)

    // 2. Load config file
    f = file.Provider("config.yaml")
    if err := k.Load(f, yaml.Parser()); err != nil {
        log.Fatalf("error loading config: %v", err)
    }

    // 3. Load environment variables
    k.Load(env.Provider("MYAPP_", ".", func(s string) string {
        return strings.Replace(
            strings.ToLower(strings.TrimPrefix(s, "MYAPP_")),
            "_", ".", -1,
        )
    }), nil)

    // 4. Watch for changes (with thread safety)
    f.Watch(func(event interface{}, err error) {
        if err != nil {
            log.Printf("watch error: %v", err)
            return
        }

        mu.Lock()
        k = koanf.New(".")
        k.Load(f, yaml.Parser())
        mu.Unlock()

        log.Println("Config changed")
    })

    // Access values (thread-safe)
    mu.RLock()
    host := k.String("server.host")
    port := k.Int("server.port")
    mu.RUnlock()

    // Unmarshal
    var cfg Config
    mu.RLock()
    k.Unmarshal("", &cfg)
    mu.RUnlock()

    fmt.Printf("Server: %s:%d\n", host, port)
}
```

## Common Migration Patterns

### Pattern 1: Config File Search Paths

**Viper**:
```go
viper.SetConfigName("config")
viper.AddConfigPath("/etc/myapp/")
viper.AddConfigPath("$HOME/.myapp")
viper.AddConfigPath(".")
viper.ReadInConfig()
```

**Koanf**:
```go
searchPaths := []string{
    "/etc/myapp/config.yaml",
    filepath.Join(os.Getenv("HOME"), ".myapp", "config.yaml"),
    "config.yaml",
}

for _, path := range searchPaths {
    if _, err := os.Stat(path); err == nil {
        if err := k.Load(file.Provider(path), yaml.Parser()); err == nil {
            log.Printf("Loaded config from: %s", path)
            break
        }
    }
}
```

### Pattern 2: Bind Specific Environment Variables

**Viper**:
```go
viper.BindEnv("server.host", "SERVER_HOST")
viper.BindEnv("server.port", "SERVER_PORT")
```

**Koanf**:
```go
// Option 1: Manual mapping
if host := os.Getenv("SERVER_HOST"); host != "" {
    k.Set("server.host", host)
}
if port := os.Getenv("SERVER_PORT"); port != "" {
    k.Set("server.port", port)
}

// Option 2: Custom transform
k.Load(env.Provider("", ".", func(s string) string {
    switch s {
    case "SERVER_HOST":
        return "server.host"
    case "SERVER_PORT":
        return "server.port"
    default:
        return ""
    }
}), nil)
```

### Pattern 3: Command-Line Flags

**Viper**:
```go
import "github.com/spf13/pflag"

pflag.String("host", "localhost", "server host")
pflag.Int("port", 8080, "server port")
pflag.Parse()

viper.BindPFlags(pflag.CommandLine)
```

**Koanf**:
```go
import (
    "github.com/knadh/koanf/providers/posflag"
    flag "github.com/spf13/pflag"
)

f := flag.NewFlagSet("config", flag.ContinueOnError)
f.String("host", "localhost", "server host")
f.Int("port", 8080, "server port")
f.Parse(os.Args[1:])

k.Load(posflag.Provider(f, ".", k), nil)
```

## Benefits After Migration

1. **Smaller Binaries**: ~1MB reduction in binary size
2. **Fewer Dependencies**: Reduced attack surface and faster builds
3. **Explicit Control**: Clearer configuration loading flow
4. **Better Performance**: Lighter weight, faster startup
5. **Easier Testing**: No global state, easier to mock

## Migration Checklist

- [ ] Replace `viper` imports with `koanf` imports
- [ ] Create koanf instance (replace global viper usage)
- [ ] Replace `SetDefault()` with `confmap.Provider()`
- [ ] Replace `ReadInConfig()` with `k.Load(file.Provider())`
- [ ] Replace `AutomaticEnv()` with `k.Load(env.Provider())`
- [ ] Replace `BindPFlags()` with `k.Load(posflag.Provider())`
- [ ] Replace `Get*()` methods with `k.String()`, `k.Int()`, etc.
- [ ] Replace `Unmarshal()` with `k.Unmarshal()`
- [ ] Add struct tags if missing (`koanf:"fieldname"`)
- [ ] Replace `WatchConfig()` with `f.Watch()`
- [ ] Add mutexes for thread-safe access
- [ ] Update tests
- [ ] Validate configuration still works

## When NOT to Migrate

Consider staying with Viper if:

- You rely heavily on Viper-specific features (remote config, etc.)
- Your application is already working well and binary size isn't a concern
- You don't have time for comprehensive testing
- Your team is unfamiliar with explicit configuration patterns

## Further Reading

- [Koanf GitHub](https://github.com/knadh/koanf)
- [Viper to Koanf Comparison](https://github.com/knadh/koanf/wiki/Comparison-with-spf13-viper)
- [Koanf Examples](https://github.com/knadh/koanf/tree/master/examples)
