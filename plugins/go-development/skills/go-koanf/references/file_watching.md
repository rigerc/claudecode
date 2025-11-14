# File Watching and Hot-Reloading

## Basic File Watching

```go
import (
    "github.com/knadh/koanf/providers/file"
    "github.com/knadh/koanf/parsers/yaml"
)

// Load initial config
f := file.Provider("config.yaml")
if err := k.Load(f, yaml.Parser()); err != nil {
    log.Fatalf("error loading config: %v", err)
}

// Watch for changes
f.Watch(func(event interface{}, err error) {
    if err != nil {
        log.Printf("watch error: %v", err)
        return
    }

    log.Println("config changed, reloading...")

    // Reload configuration
    k = koanf.New(".")
    if err := k.Load(f, yaml.Parser()); err != nil {
        log.Printf("error reloading config: %v", err)
        return
    }

    log.Println("config reloaded successfully")
})

// Stop watching when done
// defer f.Unwatch()
```

## Thread-Safe Watching

```go
var (
    k  *koanf.Koanf
    mu sync.RWMutex
    f  *file.File
)

func InitConfig(path string) error {
    k = koanf.New(".")
    f = file.Provider(path)

    // Load initial config
    if err := k.Load(f, yaml.Parser()); err != nil {
        return err
    }

    // Start watching
    f.Watch(func(event interface{}, err error) {
        if err != nil {
            log.Printf("watch error: %v", err)
            return
        }

        reloadConfig()
    })

    return nil
}

func reloadConfig() {
    mu.Lock()
    defer mu.Unlock()

    k = koanf.New(".")
    if err := k.Load(f, yaml.Parser()); err != nil {
        log.Printf("error reloading: %v", err)
        return
    }

    log.Println("config reloaded")
}

func GetString(key string) string {
    mu.RLock()
    defer mu.RUnlock()
    return k.String(key)
}

func GetInt(key string) int {
    mu.RLock()
    defer mu.RUnlock()
    return k.Int(key)
}

func Stop() {
    if f != nil {
        f.Unwatch()
    }
}
```

## Watching with Callbacks

```go
type ConfigManager struct {
    k         *koanf.Koanf
    mu        sync.RWMutex
    f         *file.File
    callbacks []func(*Config)
}

func NewConfigManager(path string) (*ConfigManager, error) {
    cm := &ConfigManager{
        k:         koanf.New("."),
        callbacks: make([]func(*Config), 0),
    }

    cm.f = file.Provider(path)
    if err := cm.k.Load(cm.f, yaml.Parser()); err != nil {
        return nil, err
    }

    cm.f.Watch(func(event interface{}, err error) {
        if err != nil {
            log.Printf("watch error: %v", err)
            return
        }
        cm.reload()
    })

    return cm, nil
}

func (cm *ConfigManager) reload() {
    cm.mu.Lock()
    defer cm.mu.Unlock()

    cm.k = koanf.New(".")
    if err := cm.k.Load(cm.f, yaml.Parser()); err != nil {
        log.Printf("error reloading: %v", err)
        return
    }

    // Get new config
    var cfg Config
    if err := cm.k.Unmarshal("", &cfg); err != nil {
        log.Printf("error unmarshalling: %v", err)
        return
    }

    // Notify callbacks
    for _, callback := range cm.callbacks {
        callback(&cfg)
    }
}

func (cm *ConfigManager) OnChange(callback func(*Config)) {
    cm.mu.Lock()
    defer cm.mu.Unlock()
    cm.callbacks = append(cm.callbacks, callback)
}

func (cm *ConfigManager) GetConfig() (*Config, error) {
    cm.mu.RLock()
    defer cm.mu.RUnlock()

    var cfg Config
    if err := cm.k.Unmarshal("", &cfg); err != nil {
        return nil, err
    }
    return &cfg, nil
}

// Usage
func main() {
    cm, err := NewConfigManager("config.yaml")
    if err != nil {
        log.Fatal(err)
    }

    // Register callback
    cm.OnChange(func(cfg *Config) {
        log.Printf("Config updated: %+v", cfg)
        // Update application state
    })

    // Use config
    cfg, _ := cm.GetConfig()
    log.Printf("Current config: %+v", cfg)
}
```

## Watching Multiple Files

```go
type MultiFileWatcher struct {
    k       *koanf.Koanf
    mu      sync.RWMutex
    files   []*file.File
    parsers []koanf.Parser
}

func NewMultiFileWatcher(configs []string) (*MultiFileWatcher, error) {
    mw := &MultiFileWatcher{
        k:       koanf.New("."),
        files:   make([]*file.File, 0),
        parsers: make([]koanf.Parser, 0),
    }

    for _, path := range configs {
        f := file.Provider(path)
        parser := yaml.Parser() // Or detect based on extension

        // Load initial config
        if err := mw.k.Load(f, parser); err != nil {
            return nil, err
        }

        mw.files = append(mw.files, f)
        mw.parsers = append(mw.parsers, parser)

        // Watch for changes
        f.Watch(func(event interface{}, err error) {
            if err != nil {
                log.Printf("watch error: %v", err)
                return
            }
            mw.reloadAll()
        })
    }

    return mw, nil
}

func (mw *MultiFileWatcher) reloadAll() {
    mw.mu.Lock()
    defer mw.mu.Unlock()

    mw.k = koanf.New(".")
    for i, f := range mw.files {
        if err := mw.k.Load(f, mw.parsers[i]); err != nil {
            log.Printf("error reloading: %v", err)
            return
        }
    }
    log.Println("all configs reloaded")
}

func (mw *MultiFileWatcher) Stop() {
    for _, f := range mw.files {
        f.Unwatch()
    }
}
```

## Graceful Reload with Validation

```go
func reloadWithValidation() {
    // Create temporary koanf instance
    tempK := koanf.New(".")
    if err := tempK.Load(f, yaml.Parser()); err != nil {
        log.Printf("error loading new config: %v", err)
        return
    }

    // Unmarshal and validate
    var cfg Config
    if err := tempK.Unmarshal("", &cfg); err != nil {
        log.Printf("error unmarshalling: %v", err)
        return
    }

    if err := cfg.Validate(); err != nil {
        log.Printf("invalid config: %v", err)
        return
    }

    // Only swap if validation passes
    mu.Lock()
    k = tempK
    mu.Unlock()

    log.Println("config reloaded and validated")
}
```

## Providers That Support Watching

- **file** - Local file watching using fsnotify
- **appconfig** - AWS AppConfig polling
- **vault** - HashiCorp Vault secrets
- **consul** - HashiCorp Consul KV store

## Best Practices

### 1. Always Use Mutexes

```go
var (
    k  *koanf.Koanf
    mu sync.RWMutex // REQUIRED for thread safety
)

func Get(key string) string {
    mu.RLock()
    defer mu.RUnlock()
    return k.String(key)
}
```

### 2. Validate Before Swapping

```go
// Create new instance
newK := koanf.New(".")
newK.Load(f, yaml.Parser())

// Validate
var cfg Config
if err := newK.Unmarshal("", &cfg); err != nil {
    return // Don't swap on error
}
if err := cfg.Validate(); err != nil {
    return // Don't swap if invalid
}

// Only swap if valid
mu.Lock()
k = newK
mu.Unlock()
```

### 3. Handle Errors Gracefully

```go
f.Watch(func(event interface{}, err error) {
    if err != nil {
        log.Printf("watch error: %v", err)
        return // Keep old config on error
    }

    if err := reloadConfig(); err != nil {
        log.Printf("reload failed: %v", err)
        return // Keep old config on reload error
    }
})
```

### 4. Stop Watching on Shutdown

```go
func main() {
    // ... setup watching ...

    // Stop on shutdown
    defer f.Unwatch()

    // Or with signal handling
    sigChan := make(chan os.Signal, 1)
    signal.Notify(sigChan, os.Interrupt, syscall.SIGTERM)

    <-sigChan
    log.Println("shutting down...")
    f.Unwatch()
}
```

### 5. Notify Application Components

```go
type App struct {
    server   *http.Server
    database *sql.DB
}

func (app *App) OnConfigChange(cfg *Config) {
    // Update log level
    log.SetLevel(cfg.Log.Level)

    // Reconnect database if URL changed
    if cfg.Database.URL != app.currentDBURL {
        app.reconnectDatabase(cfg.Database.URL)
    }

    // Update server timeouts
    app.server.ReadTimeout = cfg.Server.ReadTimeout
    app.server.WriteTimeout = cfg.Server.WriteTimeout
}
```

## Complete Example

See `templates/file_watching.go` for a complete, production-ready implementation with:
- Thread-safe access
- Validation before swapping
- Callback support
- Error handling
- Graceful shutdown
