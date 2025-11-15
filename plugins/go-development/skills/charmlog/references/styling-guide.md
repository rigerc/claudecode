# Charmbracelet Log Styling Guide

## Custom Styling Overview

Charmbracelet Log uses Lip Gloss for beautiful terminal styling. You can customize colors, formatting, and visual appearance for different log levels, keys, and values.

## Basic Styling Concepts

### Understanding Lip Gloss Styles

```go
package main

import (
    "os"
    "github.com/charmbracelet/log"
    "github.com/charmbracelet/lipgloss"
)

func main() {
    logger := log.New(os.Stdout)

    // Get default styles
    styles := log.DefaultStyles()

    // Customize error level style
    styles.Levels[log.ErrorLevel] = lipgloss.NewStyle().
        SetString("ERROR").
        Padding(0, 1, 0, 1).
        Background(lipgloss.Color("196")).
        Foreground(lipgloss.Color("15")).
        Bold(true)

    // Apply custom styles
    logger.SetStyles(styles)

    // Test the styling
    logger.Error("This error has custom styling", "component", "database")
}
```

### Style Properties Reference

Lip Gloss provides extensive styling options:

```go
// Colors and backgrounds
.Foreground(lipgloss.Color("86"))  // Text color
.Background(lipgloss.Color("196")) // Background color

// Text formatting
.Bold(true)
.Italic(true)
.Underline(true)
.Strikethrough(true)
.Blink(true)
.Reverse(true) // Reverse foreground/background

// Spacing and alignment
.Padding(1, 2, 1, 2) // top, right, bottom, left
.Margin(1, 0)        // vertical, horizontal
.Width(20)           // Fixed width
.Height(5)           // Fixed height

// Borders
.Border(lipgloss.NormalBorder())
.BorderStyle(lipgloss.RoundedBorder())
.BorderForeground(lipgloss.Color("99"))

// Positioning
.Align(lipgloss.Left)   // Left, Center, Right
.AlignHorizontal(lipgloss.Center)
.AlignVertical(lipgloss.Bottom)
```

## Log Level Styling

### Colorful Log Levels

```go
package main

import (
    "os"
    "github.com/charmbracelet/log"
    "github.com/charmbracelet/lipgloss"
)

func setupColorfulLevels() {
    logger := log.New(os.Stdout)
    styles := log.DefaultStyles()

    // Debug level - subtle blue
    styles.Levels[log.DebugLevel] = lipgloss.NewStyle().
        SetString("🐛 DEBUG").
        Foreground(lipgloss.Color("245")).
        Italic(true)

    // Info level - bright green
    styles.Levels[log.InfoLevel] = lipgloss.NewStyle().
        SetString("ℹ️  INFO").
        Foreground(lipgloss.Color("86")).
        Bold(true)

    // Warn level - yellow with warning icon
    styles.Levels[log.WarnLevel] = lipgloss.NewStyle().
        SetString("⚠️  WARN").
        Foreground(lipgloss.Color("226")).
        Bold(true)

    // Error level - red background with white text
    styles.Levels[log.ErrorLevel] = lipgloss.NewStyle().
        SetString("🔴 ERROR").
        Background(lipgloss.Color("196")).
        Foreground(lipgloss.Color("15")).
        Bold(true).
        Padding(0, 1)

    // Fatal level - dramatic red with white background
    styles.Levels[log.FatalLevel] = lipgloss.NewStyle().
        SetString("💀 FATAL").
        Background(lipgloss.Color("196")).
        Foreground(lipgloss.Color("15")).
        Bold(true).
        Underline(true).
        Padding(0, 1)

    logger.SetStyles(styles)
    log.SetDefault(logger)
}
```

### Minimalist Log Levels

```go
func setupMinimalistLevels() {
    logger := log.New(os.Stdout)
    styles := log.DefaultStyles()

    // Clean, minimal design with brackets
    styles.Levels[log.DebugLevel] = lipgloss.NewStyle().
        SetString("[debug]").
        Foreground(lipgloss.Color("245"))

    styles.Levels[log.InfoLevel] = lipgloss.NewStyle().
        SetString("[info]").
        Foreground(lipgloss.Color("86"))

    styles.Levels[log.WarnLevel] = lipgloss.NewStyle().
        SetString("[warn]").
        Foreground(lipgloss.Color("208"))

    styles.Levels[log.ErrorLevel] = lipgloss.NewStyle().
        SetString("[error]").
        Foreground(lipgloss.Color("196")).
        Bold(true)

    logger.SetStyles(styles)
    log.SetDefault(logger)
}
```

### Professional Log Levels

```go
func setupProfessionalLevels() {
    logger := log.New(os.Stdout)
    styles := log.DefaultStyles()

    // Professional business application styling
    styles.Levels[log.DebugLevel] = lipgloss.NewStyle().
        SetString("DEBUG").
        Foreground(lipgloss.Color("244")).
        SetString("DEBUG")

    styles.Levels[log.InfoLevel] = lipgloss.NewStyle().
        SetString("INFO").
        Foreground(lipgloss.Color("33")).
        Bold(true)

    styles.Levels[log.WarnLevel] = lipgloss.NewStyle().
        SetString("WARN").
        Foreground(lipgloss.Color("214")).
        Bold(true)

    styles.Levels[log.ErrorLevel] = lipgloss.NewStyle().
        SetString("ERROR").
        Foreground(lipgloss("196")).
        Bold(true)

    logger.SetStyles(styles)
    log.SetDefault(logger)
}
```

## Key and Value Styling

### Customizing Keys

```go
package main

import (
    "os"
    "github.com/charmbracelet/log"
    "github.com/charmbracelet/lipgloss"
)

func setupKeyStyling() {
    logger := log.New(os.Stdout)
    styles := log.DefaultStyles()

    // Style specific keys
    styles.Keys["user"] = lipgloss.NewStyle().
        Foreground(lipgloss.Color("86")).
        Bold(true)

    styles.Keys["error"] = lipgloss.NewStyle().
        Foreground(lipgloss.Color("196")).
        Bold(true).
        Underline(true)

    styles.Keys["request_id"] = lipgloss.NewStyle().
        Foreground(lipgloss.Color("147")).
        Italic(true)

    styles.Keys["duration"] = lipgloss.NewStyle().
        Foreground(lipgloss.Color("226"))

    styles.Keys["status"] = lipgloss.NewStyle().
        Foreground(lipgloss.Color("40"))

    // Pattern-based key styling
    styles.Keys["user_id"] = styles.Keys["user"]    // Inherit user style
    styles.Keys["username"] = styles.Keys["user"]   // Inherit user style
    styles.Keys["email"] = styles.Keys["user"]      // Inherit user style

    logger.SetStyles(styles)
    log.SetDefault(logger)

    // Test the key styling
    log.Info("User action",
        "user", "alice",
        "user_id", "12345",
        "request_id", "req-abc-123",
        "duration", "250ms",
        "status", "success",
    )

    log.Error("Operation failed",
        "error", "connection timeout",
        "request_id", "req-abc-123",
    )
}
```

### Customizing Values

```go
func setupValueStyling() {
    logger := log.New(os.Stdout)
    styles := log.DefaultStyles()

    // Style specific values
    styles.Values["alice"] = lipgloss.NewStyle().
        Foreground(lipgloss.Color("120")).
        Bold(true)

    styles.Values["error"] = lipgloss.NewStyle().
        Foreground(lipgloss.Color("196")).
        Bold(true)

    styles.Values["success"] = lipgloss.NewStyle().
        Foreground(lipgloss.Color("46")).
        Bold(true)

    styles.Values["failed"] = lipgloss.NewStyle().
        Foreground(lipgloss.Color("196")).
        Bold(true)

    // Style value patterns (more complex)
    // You'll need to implement custom value detection logic
    // for dynamic styling based on value content

    logger.SetStyles(styles)
    log.SetDefault(logger)

    // Test value styling
    log.Info("User login", "user", "alice", "status", "success")
    log.Error("User login", "user", "bob", "status", "failed", "error", "invalid credentials")
}
```

## Theme Systems

### Dark Theme

```go
func setupDarkTheme() {
    logger := log.New(os.Stdout)
    styles := log.DefaultStyles()

    // Dark theme optimized for dark terminals
    styles.Levels[log.DebugLevel] = lipgloss.NewStyle().
        SetString("· DEBUG").
        Foreground(lipgloss.Color("242"))

    styles.Levels[log.InfoLevel] = lipgloss.NewStyle().
        SetString("• INFO").
        Foreground(lipgloss.Color("87"))

    styles.Levels[log.WarnLevel] = lipgloss.NewStyle().
        SetString("⚠ WARN").
        Foreground(lipgloss.Color("215")).
        Bold(true)

    styles.Levels[log.ErrorLevel] = lipgloss.NewStyle().
        SetString("✖ ERROR").
        Foreground(lipgloss.Color("203")).
        Bold(true)

    // Key styling for dark theme
    styles.Keys["timestamp"] = lipgloss.NewStyle().
        Foreground(lipgloss.Color("242"))

    styles.Keys["component"] = lipgloss.NewStyle().
        Foreground(lipgloss.Color("140"))

    logger.SetStyles(styles)
    log.SetDefault(logger)
}
```

### Light Theme

```go
func setupLightTheme() {
    logger := log.New(os.Stdout)
    styles := log.DefaultStyles()

    // Light theme optimized for light terminals
    styles.Levels[log.DebugLevel] = lipgloss.NewStyle().
        SetString("· DEBUG").
        Foreground(lipgloss.Color("245"))

    styles.Levels[log.InfoLevel] = lipgloss.NewStyle().
        SetString("• INFO").
        Foreground(lipgloss.Color("25")).
        Bold(true)

    styles.Levels[log.WarnLevel] = lipgloss.NewStyle().
        SetString("⚠ WARN").
        Foreground(lipgloss.Color("94")).
        Bold(true)

    styles.Levels[log.ErrorLevel] = lipgloss.NewStyle().
        SetString("✖ ERROR").
        Foreground(lipgloss.Color("124")).
        Bold(true)

    logger.SetStyles(styles)
    log.SetDefault(logger)
}
```

### High Contrast Theme

```go
func setupHighContrastTheme() {
    logger := log.New(os.Stdout)
    styles := log.DefaultStyles()

    // High contrast for accessibility
    styles.Levels[log.DebugLevel] = lipgloss.NewStyle().
        SetString("DEBUG").
        Background(lipgloss.Color("242")).
        Foreground(lipgloss.Color("0")).
        Bold(true)

    styles.Levels[log.InfoLevel] = lipgloss.NewStyle().
        SetString("INFO").
        Background(lipgloss.Color("33")).
        Foreground(lipgloss.Color("15")).
        Bold(true)

    styles.Levels[log.WarnLevel] = lipgloss.NewStyle().
        SetString("WARN").
        Background(lipgloss.Color("226")).
        Foreground(lipgloss.Color("0")).
        Bold(true)

    styles.Levels[log.ErrorLevel] = lipgloss.NewStyle().
        SetString("ERROR").
        Background(lipgloss.Color("196")).
        Foreground(lipgloss.Color("15")).
        Bold(true)

    logger.SetStyles(styles)
    log.SetDefault(logger)
}
```

## Application-Specific Themes

### CLI Tool Theme

```go
func setupCLITheme() {
    logger := log.New(os.Stdout)
    styles := log.DefaultStyles()

    // CLI tool with emoji and bright colors
    styles.Levels[log.DebugLevel] = lipgloss.NewStyle().
        SetString("🔍 DEBUG").
        Foreground(lipgloss.Color("147")).
        Bold(true)

    styles.Levels[log.InfoLevel] = lipgloss.NewStyle().
        SetString("ℹ️  INFO").
        Foreground(lipgloss.Color("51")).
        Bold(true)

    styles.Levels[log.WarnLevel] = lipgloss.NewStyle().
        SetString("⚠️  WARN").
        Foreground(lipgloss.Color("226")).
        Bold(true)

    styles.Levels[log.ErrorLevel] = lipgloss.NewStyle().
        SetString("❌ ERROR").
        Foreground(lipgloss.Color("196")).
        Bold(true)

    // CLI-specific key styling
    styles.Keys["command"] = lipgloss.NewStyle().
        Foreground(lipgloss.Color("86")).
        Bold(true)

    styles.Keys["file"] = lipgloss.NewStyle().
        Foreground(lipgloss.Color("214"))

    styles.Keys["line"] = lipgloss.NewStyle().
        Foreground(lipgloss.Color("147"))

    logger.SetStyles(styles)
    log.SetDefault(logger)

    // Test CLI theme
    log.Info("Command executed",
        "command", "git status",
        "file", "README.md",
        "line", 42,
    )
}
```

### Web Service Theme

```go
func setupWebServiceTheme() {
    logger := log.New(os.Stdout)
    styles := log.DefaultStyles()

    // Clean web service theme
    styles.Levels[log.DebugLevel] = lipgloss.NewStyle().
        SetString("DEBUG").
        Foreground(lipgloss.Color("245"))

    styles.Levels[log.InfoLevel] = lipgloss.NewStyle().
        SetString("INFO").
        Foreground(lipgloss.Color("32")).
        Bold(true)

    styles.Levels[log.WarnLevel] = lipgloss.NewStyle().
        SetString("WARN").
        Foreground(lipgloss.Color("208")).
        Bold(true)

    styles.Levels[log.ErrorLevel] = lipgloss.NewStyle().
        SetString("ERROR").
        Foreground(lipgloss.Color("196")).
        Bold(true)

    // Web service-specific styling
    styles.Keys["method"] = lipgloss.NewStyle().
        Foreground(lipgloss.Color("33")).
        Bold(true)

    styles.Keys["status"] = lipgloss.NewStyle().
        Bold(true)

    // Style HTTP status codes by value
    styles.Values["200"] = lipgloss.NewStyle().
        Foreground(lipgloss.Color("46"))
    styles.Values["404"] = lipgloss.NewStyle().
        Foreground(lipgloss.Color("208"))
    styles.Values["500"] = lipgloss.NewStyle().
        Foreground(lipgloss.Color("196"))

    logger.SetStyles(styles)
    log.SetDefault(logger)

    // Test web service theme
    log.Info("HTTP Request",
        "method", "GET",
        "path", "/api/users",
        "status", "200",
    )

    log.Warn("HTTP Request",
        "method", "GET",
        "path", "/api/missing",
        "status", "404",
    )
}
```

## Advanced Styling Techniques

### Dynamic Styling Based on Content

```go
package main

import (
    "os"
    "github.com/charmbracelet/log"
    "github.com/charmbracelet/lipgloss"
)

// Dynamic styler that changes based on log content
type DynamicStyler struct {
    baseStyles log.Styles
}

func NewDynamicStyler() *DynamicStyler {
    return &DynamicStyler{
        baseStyles: log.DefaultStyles(),
    }
}

func (ds *DynamicStyler) GetStyle(key string, value interface{}) lipgloss.Style {
    style := ds.baseStyles.Keys[key]

    // Dynamic styling based on value
    switch v := value.(type) {
    case string:
        switch v {
        case "success", "ok", "completed":
            return style.Foreground(lipgloss.Color("46")).Bold(true)
        case "error", "failed", "timeout":
            return style.Foreground(lipgloss.Color("196")).Bold(true)
        case "warning", "deprecated":
            return style.Foreground(lipgloss.Color("226")).Bold(true)
        }
    case int:
        if v >= 400 && v < 500 {
            return style.Foreground(lipgloss.Color("208")).Bold(true) // HTTP 4xx
        }
        if v >= 500 {
            return style.Foreground(lipgloss.Color("196")).Bold(true) // HTTP 5xx
        }
    }

    return style
}

func setupDynamicStyling() {
    logger := log.New(os.Stdout)
    styler := NewDynamicStyler()

    // Apply base styles first
    logger.SetStyles(styler.baseStyles)
    log.SetDefault(logger)

    // For truly dynamic styling, you'd need to implement a custom logger
    // or use hooks to modify the output based on content
}
```

### Conditional Styling

```go
func setupEnvironmentBasedStyling() {
    logger := log.New(os.Stdout)
    styles := log.DefaultStyles()

    environment := os.Getenv("ENVIRONMENT")

    switch environment {
    case "production":
        // Minimal styling for production
        styles.Levels[log.InfoLevel] = lipgloss.NewStyle().SetString("INFO")
        styles.Levels[log.ErrorLevel] = lipgloss.NewStyle().SetString("ERROR").Bold(true)

    case "development":
        // Colorful styling for development
        styles.Levels[log.DebugLevel] = lipgloss.NewStyle().
            SetString("🐛 DEBUG").
            Foreground(lipgloss.Color("147"))

        styles.Levels[log.InfoLevel] = lipgloss.NewStyle().
            SetString("ℹ️  INFO").
            Foreground(lipgloss.Color("86"))

        styles.Levels[log.ErrorLevel] = lipgloss.NewStyle().
            SetString("🔴 ERROR").
            Foreground(lipgloss.Color("196")).
            Bold(true)

    case "test":
        // Test environment styling
        styles.Levels[log.InfoLevel] = lipgloss.NewStyle().
            SetString("TEST").
            Foreground(lipgloss.Color("214"))

    default:
        // Default styling
    }

    logger.SetStyles(styles)
    log.SetDefault(logger)
}
```

## Color Palette Reference

### ANSI Color Codes

```go
// Standard ANSI colors (0-7)
lipgloss.Color("0")   // Black
lipgloss.Color("1")   // Red
lipgloss.Color("2")   // Green
lipgloss.Color("3")   // Yellow
lipgloss.Color("4")   // Blue
lipgloss.Color("5")   // Magenta
lipgloss.Color("6")   // Cyan
lipgloss.Color("7")   // White

// High intensity colors (8-15)
lipgloss.Color("8")   // Bright Black (Gray)
lipgloss.Color("9")   // Bright Red
lipgloss.Color("10")  // Bright Green
lipgloss.Color("11")  // Bright Yellow
lipgloss.Color("12")  // Bright Blue
lipgloss.Color("13")  // Bright Magenta
lipgloss.Color("14")  // Bright Cyan
lipgloss.Color("15")  // Bright White

// 256-color palette (16-255)
lipgloss.Color("196") // Red
lipgloss.Color("46")  // Green
lipgloss.Color("51")  // Cyan
lipgloss.Color("226") // Yellow
lipgloss.Color("208") // Orange
lipgloss.Color("214") // Orange
lipgloss.Color("33")  // Blue
lipgloss.Color("147") // Purple
lipgloss.Color("245") // Gray
```

### Common Color Combinations

```go
// Success colors
lipgloss.Color("46")   // Bright green
lipgloss.Color("120")  // Light green
lipgloss.Color("34")   // Green

// Warning colors
lipgloss.Color("226")  // Yellow
lipgloss.Color("214")  // Orange
lipgloss.Color("208")  // Orange-red

// Error colors
lipgloss.Color("196")  // Red
lipgloss.Color("203")  // Light red
lipgloss.Color("124")  // Dark red

// Info colors
lipgloss.Color("51")   // Cyan
lipgloss.Color("87")   // Light cyan
lipgloss.Color("33")   // Blue

// Neutral colors
lipgloss.Color("245")  // Light gray
lipgloss.Color("242")  // Gray
lipgloss.Color("244")  // Dark gray
```

## Practical Examples

### Complete Styled Logger Setup

```go
package main

import (
    "os"
    "github.com/charmbracelet/log"
    "github.com/charmbracelet/lipgloss"
)

func setupCompleteStyledLogger() {
    logger := log.NewWithOptions(os.Stdout, log.Options{
        ReportTimestamp: true,
        ReportCaller:    true,
        Prefix:          "myapp",
    })

    styles := log.DefaultStyles()

    // Log level styling with emojis
    styles.Levels[log.DebugLevel] = lipgloss.NewStyle().
        SetString("🔍 DEBUG").
        Foreground(lipgloss.Color("147")).
        Italic(true)

    styles.Levels[log.InfoLevel] = lipgloss.NewStyle().
        SetString("ℹ️  INFO").
        Foreground(lipgloss.Color("86")).
        Bold(true)

    styles.Levels[log.WarnLevel] = lipgloss.NewStyle().
        SetString("⚠️  WARN").
        Foreground(lipgloss.Color("226")).
        Bold(true)

    styles.Levels[log.ErrorLevel] = lipgloss.NewStyle().
        SetString("❌ ERROR").
        Foreground(lipgloss.Color("196")).
        Bold(true)

    // Key styling
    styles.Keys["user"] = lipgloss.NewStyle().
        Foreground(lipgloss.Color("86")).
        Bold(true)

    styles.Keys["error"] = lipgloss.NewStyle().
        Foreground(lipgloss.Color("196")).
        Bold(true)

    styles.Keys["request_id"] = lipgloss.NewStyle().
        Foreground(lipgloss.Color("147")).
        Italic(true)

    // Value styling
    styles.Values["alice"] = lipgloss.NewStyle().
        Foreground(lipgloss.Color("120")).
        Bold(true)

    styles.Values["success"] = lipgloss.NewStyle().
        Foreground(lipgloss.Color("46")).
        Bold(true)

    styles.Values["error"] = lipgloss.NewStyle().
        Foreground(lipgloss.Color("196")).
        Bold(true)

    logger.SetStyles(styles)
    log.SetDefault(logger)
}

func main() {
    setupCompleteStyledLogger()

    // Test the styled logger
    log.Debug("Debugging application startup")
    log.Info("Application started", "version", "1.0.0", "environment", "development")
    log.Warn("Configuration warning", "setting", "deprecated_api", "replacement", "new_api")
    log.Error("Database connection failed", "error", "connection timeout", "retries", 3)

    // Test with sub-logger
    requestLogger := log.With(
        "request_id", "req-12345",
        "user", "alice",
    )

    requestLogger.Info("Processing request", "action", "user_login", "status", "success")
}
```

## Testing Styled Output

### Verifying Styles Work

```go
func testAllStyles(logger zerolog.Logger) {
    // Test all log levels
    logger.Debug("Debug message")
    logger.Info("Info message")
    logger.Warn("Warning message")
    logger.Error("Error message")

    // Test styled keys and values
    logger.Info("Styled test",
        "user", "alice",
        "status", "success",
        "error", "none",
        "request_id", "req-12345",
    )
}
```

## Performance Considerations

### Style Caching

```go
// Pre-compute styles for better performance
type StyleCache struct {
    levelStyles map[log.Level]lipgloss.Style
    keyStyles   map[string]lipgloss.Style
    valueStyles map[string]lipgloss.Style
}

func NewStyleCache() *StyleCache {
    return &StyleCache{
        levelStyles: make(map[log.Level]lipgloss.Style),
        keyStyles:   make(map[string]lipgloss.Style),
        valueStyles: make(map[string]lipgloss.Style),
    }
}

func (sc *StyleCache) GetLevelStyle(level log.Level) lipgloss.Style {
    if style, ok := sc.levelStyles[level]; ok {
        return style
    }

    // Create and cache the style
    style := createLevelStyle(level)
    sc.levelStyles[level] = style
    return style
}
```

## Troubleshooting

### Common Issues

1. **Colors not showing**: Check if terminal supports colors
   ```go
   if lipgloss.HasColor() {
       // Colors are supported
   } else {
       // Fallback to no colors
       logger.SetFormatter(log.TextFormatter)
   }
   ```

2. **Styles not applying**: Ensure styles are set before first log message
   ```go
   // ✅ Set styles before logging
   setupLoggerStyles()
   log.Info("This will be styled")

   // ❌ Logging before setting styles
   log.Info("This won't be styled")
   setupLoggerStyles()
   ```

3. **Performance issues**: Complex styles can impact performance
   ```go
   // Keep styles simple for high-volume logging
   styles.Levels[log.InfoLevel] = lipgloss.NewStyle().
       SetString("INFO").
       Foreground(lipgloss.Color("86")) // Simple is better
   ```

This styling guide provides comprehensive coverage of Charmbracelet Log's styling capabilities, enabling you to create beautiful, professional-looking terminal output that matches your application's visual identity.