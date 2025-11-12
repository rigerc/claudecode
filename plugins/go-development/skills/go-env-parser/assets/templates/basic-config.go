// Basic Application Configuration Template
// Copy this file and customize for your application

package config

import (
    "fmt"
    "time"

    "github.com/caarlos0/env"
)

type Config struct {
    // Server Configuration
    Host string `env:"HOST" envDefault:"0.0.0.0"`
    Port int    `env:"PORT" envDefault:"8080"`

    // Application Settings
    Environment string `env:"ENVIRONMENT" envDefault:"development"`
    Debug       bool   `env:"DEBUG" envDefault:"false"`
    LogLevel    string `env:"LOG_LEVEL" envDefault:"info"`

    // Optional Features
    Version     string `env:"APP_VERSION" envDefault:"1.0.0"`
    ServiceName string `env:"SERVICE_NAME" required:"true"`

    // External Services (optional)
    DatabaseURL string `env:"DATABASE_URL"`
    RedisURL    string `env:"REDIS_URL"`
    APIKey      string `env:"API_KEY"`

    // Paths (with environment variable expansion)
    HomeDir     string `env:"HOME_DIR" envExpand:"true"`
    ConfigFile  string `env:"CONFIG_FILE" envDefault:"${HOME_DIR}/.config/app.yaml" envExpand:"true"`
    LogDir      string `env:"LOG_DIR" envDefault:"${HOME_DIR}/logs" envExpand:"true"`
}

// Parse loads configuration from environment variables
func Parse() (*Config, error) {
    var cfg Config
    if err := env.Parse(&cfg); err != nil {
        return nil, fmt.Errorf("failed to parse config: %w", err)
    }
    return &cfg, nil
}

// ParseWithDefaults loads configuration with provided defaults
func ParseWithDefaults(defaults Config) (*Config, error) {
    if err := env.Parse(&defaults); err != nil {
        return nil, fmt.Errorf("failed to parse config: %w", err)
    }
    return &defaults, nil
}

// MustParse loads configuration and panics on error (use in development)
func MustParse() *Config {
    cfg, err := Parse()
    if err != nil {
        panic(fmt.Sprintf("Failed to load configuration: %v", err))
    }
    return cfg
}

// Validate performs basic validation of the configuration
func (c *Config) Validate() error {
    if c.Port < 1 || c.Port > 65535 {
        return fmt.Errorf("invalid port number: %d (must be 1-65535)", c.Port)
    }

    validLogLevels := []string{"debug", "info", "warn", "error", "fatal"}
    validLevel := false
    for _, level := range validLogLevels {
        if c.LogLevel == level {
            validLevel = true
            break
        }
    }
    if !validLevel {
        return fmt.Errorf("invalid log level: %s (valid: %v)", c.LogLevel, validLogLevels)
    }

    return nil
}

// String returns a string representation of the configuration (excluding secrets)
func (c *Config) String() string {
    return fmt.Sprintf(
        "Config{Host: %s, Port: %d, Environment: %s, Debug: %t, LogLevel: %s, ServiceName: %s, Version: %s}",
        c.Host, c.Port, c.Environment, c.Debug, c.LogLevel, c.ServiceName, c.Version,
    )
}

// IsDevelopment returns true if running in development environment
func (c *Config) IsDevelopment() bool {
    return c.Environment == "development" || c.Environment == "dev"
}

// IsProduction returns true if running in production environment
func (c *Config) IsProduction() bool {
    return c.Environment == "production" || c.Environment == "prod"
}

// HasDatabase returns true if database URL is configured
func (c *Config) HasDatabase() bool {
    return c.DatabaseURL != ""
}

// HasRedis returns true if Redis URL is configured
func (c *Config) HasRedis() bool {
    return c.RedisURL != ""
}