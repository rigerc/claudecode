# Go Env Package Troubleshooting

Common issues, error scenarios, and solutions for the `github.com/caarlos0/env` package.

## Common Errors

### 1. ErrNotAStructPtr

**Error Message:** `expected a pointer to a struct`

**Cause:** Passing a non-pointer or non-struct value to `Parse()`.

**Incorrect:**
```go
var config Config
err := env.Parse(config)  // Passes by value
```

```go
var config *Config
err := env.Parse(config)  // Passes nil pointer
```

**Correct:**
```go
var config Config
err := env.Parse(&config)  // Passes pointer to struct
```

```go
config := &Config{}
err := env.Parse(config)  // config is already a pointer
```

### 2. Unsupported Types

**Error Message:** `unsupported type: [type]`

**Cause:** Using a field type that the package doesn't support.

**Common Unsupported Types:**
- `chan`
- `func`
- `interface{}`
- Custom structs without custom parsers
- Nested maps with complex values

**Solution:** Use supported types or implement custom parsers.

```go
type Config struct {
    Data      map[string]interface{}  // Unsupported
    Channel   chan string             // Unsupported
    Callback  func() error            // Unsupported
    CustomObj MyCustomType           // Unsupported without parser
}
```

**Fix with Custom Parser:**
```go
customParsers := env.CustomParsers{
    reflect.TypeOf(MyCustomType{}): func(v string) (interface{}, error) {
        // Parse the string into MyCustomType
        return MyCustomTypeFromString(v), nil
    },
}

err := env.ParseWithFuncs(&config, customParsers)
```

### 3. Unsupported Slice Types

**Error Message:** `unsupported slice type: []CustomType`

**Cause:** Using slice types that aren't built-in supported.

**Supported Slice Types:**
- `[]string`
- `[]int`
- `[]bool`
- `[]float32`
- `[]float64`
- `[]time.Duration`

**Solution:** Implement custom parser for unsupported slice types.

```go
type Config struct {
    CustomItems []MyCustomType  // Not supported by default
}

// Fix with custom parser
customParsers := env.CustomParsers{
    reflect.TypeOf([]MyCustomType{}): func(v string) (interface{}, error) {
        parts := strings.Split(v, ",")
        items := make([]MyCustomType, len(parts))
        for i, part := range parts {
            items[i] = MyCustomTypeFromString(part)
        }
        return items, nil
    },
}
```

### 4. Required Field Errors

**Error Message:** `required environment variable [VAR_NAME] is not set`

**Cause:** Environment variable marked as `required:"true"` but not set.

**Debugging:**
```go
// Print all environment variables (debug only)
for _, env := range os.Environ() {
    fmt.Println(env)
}

// Check specific variable
if value, exists := os.LookupEnv("DATABASE_URL"); !exists {
    fmt.Println("DATABASE_URL not set")
} else {
    fmt.Printf("DATABASE_URL = %s\n", value)
}
```

**Solutions:**
1. Set the environment variable:
```bash
export DATABASE_URL="localhost:5432"
```

2. Provide a default:
```go
type Config struct {
    DatabaseURL string `env:"DATABASE_URL" envDefault:"localhost:5432"`
}
```

3. Make it optional:
```go
type Config struct {
    DatabaseURL *string `env:"DATABASE_URL"`  // Pointer makes it optional
}
```

## Type Conversion Issues

### Boolean Parsing

**Issue:** Environment variables not parsing as expected booleans.

**Supported Boolean Values:**
- **True:** `1`, `t`, `T`, `TRUE`, `true`, `True`
- **False:** `0`, `f`, `F`, `FALSE`, `false`, `False`
- **Empty:** `""` (empty string) → `false`

**Common Issues:**
```go
// These will NOT work:
// DEBUG=yes
// DEBUG=on
// DEBUG=enabled
```

**Fix:**
```go
DEBUG=true    // ✅ Works
DEBUG=1       // ✅ Works
DEBUG=FALSE   // ✅ Works
```

### Integer Parsing

**Issue:** Large numbers or invalid formats causing parsing errors.

**Supported Formats:**
- Decimal: `1234`
- Octal: `0123` (leading zero)
- Hexadecimal: `0x1A` (leading 0x)

**Common Issues:**
```go
// These will fail:
PORT=not-a-number
TIMEOUT=abc
COUNT=1.5  // For int fields
```

**Fix:**
```go
PORT=8080          // ✅ Valid decimal
PORT=0755         // ✅ Valid octal (493 decimal)
PORT=0x1F4        // ✅ Valid hex (500 decimal)
```

### Duration Parsing

**Issue:** Invalid duration format strings.

**Supported Duration Units:**
- `ns` (nanoseconds)
- `us` (microseconds)
- `ms` (milliseconds)
- `s` (seconds)
- `m` (minutes)
- `h` (hours)

**Valid Examples:**
```go
TIMEOUT=30s        // 30 seconds
TIMEOUT=5m         // 5 minutes
TIMEOUT=2h         // 2 hours
TIMEOUT=100ms      // 100 milliseconds
TIMEOUT=1h30m      // 1 hour 30 minutes
```

**Invalid Examples:**
```go
TIMEOUT=30         // Missing unit
TIMEOUT=30sec      // Wrong unit
TIMEOUT=1:30       // Wrong format
```

## Environment Variable Issues

### Case Sensitivity

**Issue:** Environment variable names don't match.

**Rules:**
- Environment variable names are case-sensitive
- Use uppercase for consistency
- Check exact spelling

**Common Mistakes:**
```go
type Config struct {
    Port int `env:"port"`           // Should be "PORT"
    Host string `env:"HOSTNAME"`    // But environment has "HOST"
}
```

### Spaces and Special Characters

**Issue:** Spaces or special characters in environment variable values.

**Problems:**
```bash
export HOSTS="host1, host2, host3"     # Spaces cause issues
export HOSTS="host1:port1,host2:port2" # Complex parsing needed
```

**Solutions:**
```bash
export HOSTS="host1,host2,host3"       # Remove spaces
export HOSTS="host1:8080,host2:8081"   # Use consistent format
```

Or use custom separators:
```go
type Config struct {
    Hosts []string `env:"HOSTS" envSeparator:"|"`  // Allows "host1|host2|host3"
}
```

### File-based Configuration

**Issue:** `envFile` tag not working as expected.

**Common Problems:**
1. File doesn't exist
2. File permissions prevent reading
3. Environment variable points to non-existent file

**Debugging:**
```go
type Config struct {
    Secret string `env:"SECRET_FILE" envFile:"true"`
}

// Check if file exists
filePath := os.Getenv("SECRET_FILE")
if filePath == "" {
    fmt.Println("SECRET_FILE environment variable not set")
} else {
    if _, err := os.Stat(filePath); os.IsNotExist(err) {
        fmt.Printf("File does not exist: %s\n", filePath)
    }
}
```

## Performance and Memory Issues

### Large Configuration Files

**Issue:** Configuration parsing is slow or uses too much memory.

**Solutions:**
1. Use pointers for optional fields:
```go
type Config struct {
    OptionalField *string `env:"OPTIONAL_FIELD"`
}
```

2. Parse only once at startup:
```go
func init() {
    config, err := env.ParseAs[Config]()
    if err != nil {
        log.Fatal(err)
    }
    globalConfig = config
}
```

### Frequent Re-parsing

**Issue:** Calling `Parse()` repeatedly in hot paths.

**Bad:**
```go
func handleRequest() {
    var config Config
    env.Parse(&config)  // Parses on every request!
    // Use config...
}
```

**Good:**
```go
var globalConfig Config

func init() {
    env.Parse(&globalConfig)  // Parse once at startup
}

func handleRequest() {
    config := globalConfig  // Use cached config
    // Use config...
}
```

## Testing Issues

### Environment Variable Cleanup

**Issue:** Tests interfering with each other's environment variables.

**Bad:**
```go
func TestConfig1(t *testing.T) {
    os.Setenv("PORT", "8080")
    // Test...
}

func TestConfig2(t *testing.T) {
    os.Setenv("PORT", "9090")  // Tests might run in parallel
    // Test...
}
```

**Good:**
```go
func TestConfig(t *testing.T) {
    // Save original values
    originalPort := os.Getenv("PORT")

    // Set test values
    os.Setenv("PORT", "8080")
    defer os.Setenv("PORT", originalPort)  // Cleanup

    // Test...
}
```

**Better (Table-driven):**
```go
func TestConfig(t *testing.T) {
    tests := []struct {
        name    string
        envVars map[string]string
        want    Config
        wantErr bool
    }{
        {
            name: "basic config",
            envVars: map[string]string{
                "PORT": "8080",
                "HOST": "localhost",
            },
            want: Config{Port: 8080, Host: "localhost"},
            wantErr: false,
        },
    }

    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            // Set environment variables
            for k, v := range tt.envVars {
                os.Setenv(k, v)
            }

            // Cleanup after test
            defer func() {
                for k := range tt.envVars {
                    os.Unsetenv(k)
                }
            }()

            // Test...
        })
    }
}
```

## Debugging Techniques

### Print Environment Variables

```go
func debugEnv() {
    fmt.Println("=== Environment Variables ===")
    for _, env := range os.Environ() {
        if strings.HasPrefix(env, "APP_") ||
           strings.Contains(env, "DATABASE") ||
           strings.Contains(env, "REDIS") {
            fmt.Println(env)
        }
    }
    fmt.Println("=== End Environment ===")
}
```

### Validate Configuration

```go
func validateConfig(config Config) error {
    if config.Port < 1 || config.Port > 65535 {
        return fmt.Errorf("invalid port: %d", config.Port)
    }

    if config.DatabaseURL != "" {
        if !strings.Contains(config.DatabaseURL, ":") {
            return fmt.Errorf("invalid database URL format")
        }
    }

    return nil
}

func main() {
    var config Config
    if err := env.Parse(&config); err != nil {
        log.Fatal(err)
    }

    if err := validateConfig(config); err != nil {
        log.Fatal(err)
    }
}
```

### Use MustParse for Development

```go
func main() {
    // Development: Panic on error for fast feedback
    config := env.MustParseAs[Config]()

    // Production: Handle gracefully
    config, err := env.ParseAs[Config]()
    if err != nil {
        log.Fatalf("Failed to parse configuration: %v", err)
    }
}
```

## Common Solutions

### 1. Use Environment Variable Expansion

For complex paths or dependent values:

```go
type Config struct {
    HomeDir    string `env:"HOME_DIR" envExpand:"true"`
    ConfigFile string `env:"CONFIG_FILE" envDefault:"${HOME_DIR}/.config/app.yaml" envExpand:"true"`
    LogDir     string `env:"LOG_DIR" envDefault:"${HOME_DIR}/logs" envExpand:"true"`
}
```

### 2. Implement Validation After Parsing

Add business logic validation:

```go
func (c Config) Validate() error {
    var errs []error

    if c.Port < 1 || c.Port > 65535 {
        errs = append(errs, fmt.Errorf("invalid port number: %d", c.Port))
    }

    if c.DatabaseURL == "" {
        errs = append(errs, fmt.Errorf("database URL is required"))
    }

    if len(errs) > 0 {
        return fmt.Errorf("validation errors: %v", errs)
    }

    return nil
}
```

### 3. Use Separate Configurations for Different Environments

```go
type Config struct {
    Environment string `env:"ENVIRONMENT" envDefault:"development"`

    // Development specific
    Debug bool `env:"DEBUG" envDefault:"false"`

    // Production specific
    TLSCert string `env:"TLS_CERT_FILE" envFile:"true"`
}
```

### 4. Handle Missing Optional Values Gracefully

```go
type Config struct {
    OptionalURL *string `env:"OPTIONAL_URL"`  // nil if not set
    OptionalPort *int   `env:"OPTIONAL_PORT"` // nil if not set
}

func (c Config) GetURL() string {
    if c.OptionalURL == nil {
        return "http://localhost:8080"  // Default
    }
    return *c.OptionalURL
}
```