package {{.LibName}}

import (
	"fmt"
	"time"
)

// Library represents the main library instance
type Library struct {
	name        string
	description string
	created     time.Time
}

// Config holds configuration for the library
type Config struct {
	Name        string
	Description string
	Debug       bool
}

// Option is a function that configures the library
type Option func(*Config)

// WithDebug enables debug mode
func WithDebug(debug bool) Option {
	return func(c *Config) {
		c.Debug = debug
	}
}

// New creates a new Library instance with the given options
func New(name, description string, opts ...Option) *Library {
	config := &Config{
		Name:        name,
		Description: description,
		Debug:       false,
	}

	for _, opt := range opts {
		opt(config)
	}

	return &Library{
		name:        config.Name,
		description: config.Description,
		created:     time.Now(),
	}
}

// Name returns the library name
func (l *Library) Name() string {
	return l.name
}

// Description returns the library description
func (l *Library) Description() string {
	return l.description
}

// Created returns when the library instance was created
func (l *Library) Created() time.Time {
	return l.created
}

// String returns a string representation of the library
func (l *Library) String() string {
	return fmt.Sprintf("%s: %s", l.name, l.description)
}

// Greet returns a greeting message
func (l *Library) Greet(who string) string {
	return fmt.Sprintf("Hello %s! Welcome to %s.", who, l.name)
}

// Info returns information about the library instance
func (l *Library) Info() map[string]interface{} {
	return map[string]interface{}{
		"name":        l.name,
		"description": l.description,
		"created":     l.created.Format(time.RFC3339),
		"uptime":      time.Since(l.created).String(),
	}
}

// Version returns the library version
func Version() string {
	return "1.0.0"
}

// Validate checks if the library configuration is valid
func (l *Library) Validate() error {
	if l.name == "" {
		return fmt.Errorf("library name cannot be empty")
	}
	if l.description == "" {
		return fmt.Errorf("library description cannot be empty")
	}
	return nil
}