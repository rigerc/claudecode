package config

import (
	"fmt"
	"os"
	"strings"

	"github.com/knadh/koanf/parsers/yaml"
	"github.com/knadh/koanf/providers/confmap"
	"github.com/knadh/koanf/providers/env/v2"
	"github.com/knadh/koanf/providers/file"
	"github.com/knadh/koanf/providers/posflag"
	"github.com/knadh/koanf/v2"
	flag "github.com/spf13/pflag"
)

// Config holds the application configuration
type Config struct {
	Server struct {
		Host string `koanf:"host"`
		Port int    `koanf:"port"`
	} `koanf:"server"`

	Database struct {
		Host string `koanf:"host"`
		Port int    `koanf:"port"`
		User string `koanf:"user"`
		Name string `koanf:"name"`
	} `koanf:"database"`

	Log struct {
		Level  string `koanf:"level"`
		Format string `koanf:"format"`
	} `koanf:"log"`
}

var (
	k *koanf.Koanf
	f *flag.FlagSet
)

func init() {
	k = koanf.New(".")

	// Setup command-line flags
	f = flag.NewFlagSet("config", flag.ContinueOnError)
	f.Usage = func() {
		fmt.Println(f.FlagUsages())
		os.Exit(0)
	}

	f.String("config", "config.yaml", "path to config file")
	f.String("server.host", "", "server host")
	f.Int("server.port", 0, "server port")
	f.String("log.level", "", "log level")
}

// Load loads configuration from multiple sources in order of precedence:
// 1. Defaults (lowest priority)
// 2. Configuration file
// 3. Environment variables
// 4. Command-line flags (highest priority)
func Load() (*Config, error) {
	// Parse command-line flags
	if err := f.Parse(os.Args[1:]); err != nil {
		return nil, fmt.Errorf("error parsing flags: %w", err)
	}

	// 1. Load defaults (lowest priority)
	if err := loadDefaults(); err != nil {
		return nil, fmt.Errorf("error loading defaults: %w", err)
	}

	// 2. Load from config file
	configPath, _ := f.GetString("config")
	if err := loadFile(configPath); err != nil {
		return nil, fmt.Errorf("error loading config file: %w", err)
	}

	// 3. Load from environment variables
	if err := loadEnv(); err != nil {
		return nil, fmt.Errorf("error loading env vars: %w", err)
	}

	// 4. Load from command-line flags (highest priority)
	if err := loadFlags(); err != nil {
		return nil, fmt.Errorf("error loading flags: %w", err)
	}

	// Unmarshal into struct
	var cfg Config
	if err := k.Unmarshal("", &cfg); err != nil {
		return nil, fmt.Errorf("error unmarshalling config: %w", err)
	}

	// Validate
	if err := cfg.Validate(); err != nil {
		return nil, fmt.Errorf("invalid configuration: %w", err)
	}

	return &cfg, nil
}

// loadDefaults loads default configuration values
func loadDefaults() error {
	defaults := map[string]interface{}{
		"server.host":   "localhost",
		"server.port":   8080,
		"database.host": "localhost",
		"database.port": 5432,
		"database.user": "app",
		"database.name": "app_db",
		"log.level":     "info",
		"log.format":    "json",
	}

	return k.Load(confmap.Provider(defaults, "."), nil)
}

// loadFile loads configuration from a file
func loadFile(path string) error {
	// Check if file exists
	if _, err := os.Stat(path); os.IsNotExist(err) {
		// File doesn't exist, skip
		return nil
	}

	return k.Load(file.Provider(path), yaml.Parser())
}

// loadEnv loads configuration from environment variables
// Transforms: MYAPP_SERVER_HOST -> server.host
func loadEnv() error {
	return k.Load(env.Provider("MYAPP_", ".", func(s string) string {
		return strings.Replace(
			strings.ToLower(strings.TrimPrefix(s, "MYAPP_")),
			"_", ".", -1,
		)
	}), nil)
}

// loadFlags loads configuration from command-line flags
func loadFlags() error {
	return k.Load(posflag.Provider(f, ".", k), nil)
}

// Validate validates the configuration
func (c *Config) Validate() error {
	if c.Server.Port < 1 || c.Server.Port > 65535 {
		return fmt.Errorf("invalid server port: %d", c.Server.Port)
	}

	if c.Database.Port < 1 || c.Database.Port > 65535 {
		return fmt.Errorf("invalid database port: %d", c.Database.Port)
	}

	validLevels := map[string]bool{
		"debug": true, "info": true, "warn": true, "error": true,
	}
	if !validLevels[c.Log.Level] {
		return fmt.Errorf("invalid log level: %s", c.Log.Level)
	}

	return nil
}

// Reload reloads configuration from all sources
func Reload() (*Config, error) {
	k = koanf.New(".")
	return Load()
}

// Get returns a configuration value by key
func Get(key string) interface{} {
	return k.Get(key)
}

// String returns a string configuration value
func String(key string) string {
	return k.String(key)
}

// Int returns an integer configuration value
func Int(key string) int {
	return k.Int(key)
}

// Bool returns a boolean configuration value
func Bool(key string) bool {
	return k.Bool(key)
}
