# Troubleshooting Koanf

## Configuration Not Loading

### Problem: Empty or Zero Values

**Symptoms**: All configuration values are empty, zero, or default values after loading

**Diagnosis**:
```go
// Check if file exists
if _, err := os.Stat("config.yaml"); os.IsNotExist(err) {
    log.Println("Config file does not exist!")
}

// Check if values were loaded
log.Printf("All keys: %v", k.All())
log.Printf("Key exists: %v", k.Exists("server.host"))
```

**Solutions**:

1. **Verify file path** - Must be absolute or relative to working directory
```go
// Wrong: assumes incorrect working directory
k.Load(file.Provider("config.yaml"), yaml.Parser())

// Right: use absolute path or check working directory
pwd, _ := os.Getwd()
log.Printf("Working directory: %s", pwd)
k.Load(file.Provider(filepath.Join(pwd, "config.yaml")), yaml.Parser())
```

2. **Check parser matches format**
```go
// Wrong: JSON parser for YAML file
k.Load(file.Provider("config.yaml"), json.Parser())

// Right: YAML parser for YAML file
k.Load(file.Provider("config.yaml"), yaml.Parser())
```

3. **Always handle errors**
```go
// Wrong: ignoring errors
k.Load(file.Provider("config.yaml"), yaml.Parser())

// Right: check errors
if err := k.Load(file.Provider("config.yaml"), yaml.Parser()); err != nil {
    log.Fatalf("Failed to load config: %v", err)
}
```

## Environment Variables Not Working

### Problem: Environment Variables Not Overriding

**Symptoms**: Configuration from env vars not applied

**Diagnosis**:
```go
// Test if env vars are set
log.Printf("MYAPP_SERVER_HOST=%s", os.Getenv("MYAPP_SERVER_HOST"))

// Test transform function
transform := func(s string) string {
    result := strings.Replace(
        strings.ToLower(strings.TrimPrefix(s, "MYAPP_")),
        "_", ".", -1,
    )
    log.Printf("Transform: %s -> %s", s, result)
    return result
}
```

**Solutions**:

1. **Verify prefix matches exactly**
```go
// Wrong: prefix mismatch
export APP_SERVER_HOST=localhost
k.Load(env.Provider("MYAPP_", ".", transform), nil) // Looking for MYAPP_*

// Right: matching prefix
export MYAPP_SERVER_HOST=localhost
k.Load(env.Provider("MYAPP_", ".", transform), nil)
```

2. **Check transform function**
```go
// Test transform independently
transform := func(s string) string {
    s = strings.TrimPrefix(s, "MYAPP_")
    s = strings.ToLower(s)
    s = strings.ReplaceAll(s, "_", ".")
    return s
}

// MYAPP_SERVER_HOST -> server.host
```

3. **Ensure env vars are exported**
```bash
# Wrong: variable not exported
MYAPP_HOST=localhost

# Right: exported variable
export MYAPP_HOST=localhost
```

## Unmarshalling Errors

### Problem: Type Mismatch

**Symptoms**: `error unmarshalling: ... cannot unmarshal ...`

**Diagnosis**:
```go
// Check actual value type
val := k.Get("server.port")
log.Printf("Type of server.port: %T, Value: %v", val, val)
```

**Solutions**:

1. **Match types**
```go
// Wrong: port is string in YAML
server:
  port: "8080"  # String

type Config struct {
    Port int `koanf:"port"` # Expecting int
}

// Right: remove quotes
server:
  port: 8080  # Integer
```

2. **Use WeaklyTypedInput**
```go
k.UnmarshalWithConf("", &cfg, koanf.UnmarshalConf{
    Tag: "koanf",
    DecoderConfig: &mapstructure.DecoderConfig{
        WeaklyTypedInput: true, // Allows string -> int conversion
        Result:          &cfg,
        TagName:         "koanf",
    },
})
```

### Problem: Struct Tags Not Matching

**Symptoms**: Fields remain zero-value after unmarshal

**Diagnosis**:
```go
// Print configuration
k.Print()

// Check specific path
log.Printf("server config: %+v", k.Get("server"))
```

**Solutions**:

1. **Verify tags match paths**
```go
// Configuration:
server:
  host: localhost

// Wrong: tag doesn't match
type Config struct {
    Host string `koanf:"hostname"` // Looking for "hostname"
}

// Right: matching tag
type Config struct {
    Host string `koanf:"host"` // Matches "host"
}
```

2. **Use FlatPaths for nested access**
```go
// Configuration:
server:
  host: localhost

// Option 1: Nested struct
type Config struct {
    Server struct {
        Host string `koanf:"host"`
    } `koanf:"server"`
}

// Option 2: Flat paths
type Config struct {
    ServerHost string `koanf:"server.host"`
}
k.UnmarshalWithConf("", &cfg, koanf.UnmarshalConf{
    Tag:       "koanf",
    FlatPaths: true,
})
```

## Type Conflicts During Merge

### Problem: Strict Merge Fails

**Symptoms**: `error loading config: ... type conflict ...`

**Diagnosis**:
```go
// Check types from different sources
log.Printf("From file: %T", k.Get("timeout"))

k.Load(env.Provider(...), nil)
log.Printf("From env: %T", k.Get("timeout"))
```

**Solutions**:

1. **Ensure consistent types across sources**
```yaml
# config.yaml
timeout: 30s  # string duration

# But environment has:
# MYAPP_TIMEOUT=30  # integer
```

Fix by making both sources use the same type:
```yaml
# config.yaml
timeout: 30s  # string

# Environment
export MYAPP_TIMEOUT="30s"  # string
```

2. **Disable strict merge** (not recommended)
```go
var k = koanf.NewWithConf(koanf.Conf{
    Delim:       ".",
    StrictMerge: false, // Allow type conflicts
})
```

## File Watching Issues

### Problem: Watch Not Triggering

**Symptoms**: Config changes not detected

**Solutions**:

1. **Check file system events support**
```go
// Some systems/file systems don't support fsnotify
// Use polling instead
```

2. **Verify watch is started before changes**
```go
// Wrong: file modified before watch starts
k.Load(f, yaml.Parser())
// ... modify file ...
f.Watch(...) // Too late

// Right: start watching immediately
k.Load(f, yaml.Parser())
f.Watch(...)
// ... now modify file ...
```

3. **Check error in watch callback**
```go
f.Watch(func(event interface{}, err error) {
    if err != nil {
        log.Printf("watch error: %v", err) // Check this!
        return
    }
    // reload...
})
```

### Problem: Concurrent Access Crashes

**Symptoms**: Race conditions, panics, corrupted data

**Solution**: Always use mutexes
```go
var (
    k  *koanf.Koanf
    mu sync.RWMutex // REQUIRED
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
    k.Load(f, yaml.Parser())
}
```

## Performance Issues

### Problem: Slow Configuration Loading

**Diagnosis**:
```go
import "time"

start := time.Now()
k.Load(file.Provider("config.yaml"), yaml.Parser())
log.Printf("Load took: %v", time.Since(start))
```

**Solutions**:

1. **Load only needed configurations**
```go
// Wrong: loading entire large config
k.Load(file.Provider("huge-config.yaml"), yaml.Parser())

// Right: split into smaller files
k.Load(file.Provider("server.yaml"), yaml.Parser())
k.Load(file.Provider("database.yaml"), yaml.Parser())
```

2. **Cache parsed configuration**
```go
var cachedConfig *Config

func GetConfig() *Config {
    if cachedConfig != nil {
        return cachedConfig
    }

    var cfg Config
    k.Unmarshal("", &cfg)
    cachedConfig = &cfg
    return cachedConfig
}
```

## Debug Tips

### Enable Debug Logging

```go
// Print all configuration
k.Print()

// Get all keys
allKeys := k.All()
log.Printf("All config: %+v", allKeys)

// Check specific path
log.Printf("server: %+v", k.Get("server"))
log.Printf("server.host exists: %v", k.Exists("server.host"))
```

### Validate Configuration Step by Step

```go
// Load and check after each step
k.Load(confmap.Provider(defaults, "."), nil)
log.Printf("After defaults: %+v", k.All())

k.Load(file.Provider("config.yaml"), yaml.Parser())
log.Printf("After file: %+v", k.All())

k.Load(env.Provider("APP_", ".", transform), nil)
log.Printf("After env: %+v", k.All())
```

### Marshal and Print

```go
// Marshal to JSON for inspection
b, _ := k.Marshal(json.Parser())
fmt.Println(string(b))
```

## Common Mistakes

### 1. Not Checking Errors
```go
// Wrong
k.Load(file.Provider("config.yaml"), yaml.Parser())

// Right
if err := k.Load(file.Provider("config.yaml"), yaml.Parser()); err != nil {
    log.Fatalf("error: %v", err)
}
```

### 2. Wrong Delimiter
```go
// Configuration uses dots
server.host=localhost

// Wrong: using slash delimiter
k := koanf.New("/")
k.String("server.host") // Returns empty!

// Right: use dot delimiter
k := koanf.New(".")
k.String("server.host") // Works!
```

### 3. Modifying Koanf Without Mutex
```go
// Wrong: concurrent access
go func() {
    k.Load(...) // Race condition!
}()
go func() {
    k.String("key") // Race condition!
}()

// Right: use mutex
var mu sync.RWMutex

go func() {
    mu.Lock()
    k.Load(...)
    mu.Unlock()
}()
go func() {
    mu.RLock()
    k.String("key")
    mu.RUnlock()
}()
```

### 4. Not Validating After Reload
```go
// Wrong: no validation
f.Watch(func(event interface{}, err error) {
    k = koanf.New(".")
    k.Load(f, yaml.Parser()) // Could be invalid!
})

// Right: validate before swapping
f.Watch(func(event interface{}, err error) {
    tempK := koanf.New(".")
    tempK.Load(f, yaml.Parser())

    var cfg Config
    if err := tempK.Unmarshal("", &cfg); err != nil {
        log.Printf("invalid config: %v", err)
        return // Keep old config
    }

    if err := cfg.Validate(); err != nil {
        log.Printf("validation failed: %v", err)
        return // Keep old config
    }

    k = tempK // Only swap if valid
})
```
