package config

import (
	"fmt"
	"log"
	"sync"

	"github.com/knadh/koanf/parsers/yaml"
	"github.com/knadh/koanf/providers/file"
	"github.com/knadh/koanf/v2"
)

// Config holds the application configuration
type Config struct {
	Server struct {
		Host string `koanf:"host"`
		Port int    `koanf:"port"`
	} `koanf:"server"`

	Log struct {
		Level string `koanf:"level"`
	} `koanf:"log"`
}

var (
	k        *koanf.Koanf
	mu       sync.RWMutex
	f        *file.File
	onChange func(*Config) // Callback when config changes
)

// Load loads configuration and sets up file watching
func Load(configPath string, callback func(*Config)) error {
	k = koanf.New(".")
	onChange = callback

	// Create file provider
	f = file.Provider(configPath)

	// Load initial configuration
	if err := k.Load(f, yaml.Parser()); err != nil {
		return fmt.Errorf("error loading config: %w", err)
	}

	// Unmarshal and validate
	cfg, err := unmarshalAndValidate()
	if err != nil {
		return err
	}

	// Call initial callback
	if onChange != nil {
		onChange(cfg)
	}

	// Start watching for changes
	go watchConfig()

	return nil
}

// watchConfig watches the configuration file for changes
func watchConfig() {
	f.Watch(func(event interface{}, err error) {
		if err != nil {
			log.Printf("watch error: %v", err)
			return
		}

		log.Println("config file changed, reloading...")

		// Reload configuration
		mu.Lock()
		newK := koanf.New(".")
		if err := newK.Load(f, yaml.Parser()); err != nil {
			log.Printf("error reloading config: %v", err)
			mu.Unlock()
			return
		}
		k = newK
		mu.Unlock()

		// Unmarshal and validate
		cfg, err := unmarshalAndValidate()
		if err != nil {
			log.Printf("invalid config after reload: %v", err)
			return
		}

		log.Println("config reloaded successfully")

		// Call callback with new config
		if onChange != nil {
			onChange(cfg)
		}
	})
}

// unmarshalAndValidate unmarshals configuration and validates it
func unmarshalAndValidate() (*Config, error) {
	mu.RLock()
	defer mu.RUnlock()

	var cfg Config
	if err := k.Unmarshal("", &cfg); err != nil {
		return nil, fmt.Errorf("error unmarshalling config: %w", err)
	}

	if err := cfg.Validate(); err != nil {
		return nil, fmt.Errorf("invalid configuration: %w", err)
	}

	return &cfg, nil
}

// Validate validates the configuration
func (c *Config) Validate() error {
	if c.Server.Port < 1 || c.Server.Port > 65535 {
		return fmt.Errorf("invalid server port: %d", c.Server.Port)
	}

	validLevels := map[string]bool{
		"debug": true, "info": true, "warn": true, "error": true,
	}
	if !validLevels[c.Log.Level] {
		return fmt.Errorf("invalid log level: %s", c.Log.Level)
	}

	return nil
}

// Get returns a configuration value by key (thread-safe)
func Get(key string) interface{} {
	mu.RLock()
	defer mu.RUnlock()
	return k.Get(key)
}

// String returns a string configuration value (thread-safe)
func String(key string) string {
	mu.RLock()
	defer mu.RUnlock()
	return k.String(key)
}

// Int returns an integer configuration value (thread-safe)
func Int(key string) int {
	mu.RLock()
	defer mu.RUnlock()
	return k.Int(key)
}

// Bool returns a boolean configuration value (thread-safe)
func Bool(key string) bool {
	mu.RLock()
	defer mu.RUnlock()
	return k.Bool(key)
}

// GetConfig returns the current configuration (thread-safe)
func GetConfig() (*Config, error) {
	return unmarshalAndValidate()
}

// Stop stops watching the configuration file
func Stop() {
	if f != nil {
		f.Unwatch()
	}
}

// Example usage:
/*
func main() {
	// Load config with callback
	err := config.Load("config.yaml", func(cfg *config.Config) {
		log.Printf("Configuration updated: %+v", cfg)
		// Update application state based on new config
		// e.g., adjust log level, reconnect to database, etc.
	})
	if err != nil {
		log.Fatalf("failed to load config: %v", err)
	}

	// Use configuration
	host := config.String("server.host")
	port := config.Int("server.port")

	// Stop watching on shutdown
	defer config.Stop()

	// Your application logic...
}
*/
