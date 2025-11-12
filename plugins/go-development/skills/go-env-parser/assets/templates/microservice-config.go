// Microservice Configuration Template
// Complete configuration for production microservices

package config

import (
    "fmt"
    "time"

    "github.com/caarlos0/env"
)

type MicroserviceConfig struct {
    // Service Information
    Service struct {
        Name        string `env:"SERVICE_NAME" required:"true"`
        Version     string `env:"SERVICE_VERSION" envDefault:"1.0.0"`
        Environment string `env:"SERVICE_ENV" envDefault:"development"`
        InstanceID  string `env:"INSTANCE_ID" envDefault:"unknown"`
        Region      string `env:"SERVICE_REGION" envDefault:"us-east-1"`
        Zone        string `env:"SERVICE_ZONE"`
    }

    // HTTP Server Configuration
    HTTP struct {
        Host            string        `env:"HTTP_HOST" envDefault:"0.0.0.0"`
        Port            int           `env:"HTTP_PORT" envDefault:"8080"`
        ReadTimeout     time.Duration `env:"HTTP_READ_TIMEOUT" envDefault:"30s"`
        WriteTimeout    time.Duration `env:"HTTP_WRITE_TIMEOUT" envDefault:"30s"`
        IdleTimeout     time.Duration `env:"HTTP_IDLE_TIMEOUT" envDefault:"120s"`
        MaxHeaderBytes  int           `env:"HTTP_MAX_HEADER_BYTES" envDefault:"1048576"` // 1MB
        EnableCORS      bool          `env:"HTTP_ENABLE_CORS" envDefault:"true"`
        CORSOrigins     []string      `env:"HTTP_CORS_ORIGINS" envSeparator:","`
        CORSMethods     []string      `env:"HTTP_CORS_METHODS" envSeparator:"," envDefault:"GET,POST,PUT,DELETE,OPTIONS"`
        CORSHeaders     []string      `env:"HTTP_CORS_HEADERS" envSeparator:"," envDefault:"Content-Type,Authorization"`
        EnableMetrics   bool          `env:"HTTP_ENABLE_METRICS" envDefault:"true"`
        EnableProfiling bool          `env:"HTTP_ENABLE_PROFILING" envDefault:"false"`
    }

    // TLS Configuration
    TLS struct {
        Enabled      bool   `env:"TLS_ENABLED" envDefault:"false"`
        CertFile     string `env:"TLS_CERT_FILE" envFile:"true"`
        KeyFile      string `env:"TLS_KEY_FILE" envFile:"true"`
        ClientAuth   string `env:"TLS_CLIENT_AUTH" envDefault:"request"` // request, require, verify, none
        MinVersion   string `env:"TLS_MIN_VERSION" envDefault:"1.2"`
        Ciphers      []string `env:"TLS_CIPHERS" envSeparator:","`
    }

    // gRPC Server Configuration
    GRPC struct {
        Host           string        `env:"GRPC_HOST" envDefault:"0.0.0.0"`
        Port           int           `env:"GRPC_PORT" envDefault:"9090"`
        Timeout        time.Duration `env:"GRPC_TIMEOUT" envDefault:"30s"`
        MaxRecvMsgSize int           `env:"GRPC_MAX_RECV_MSG_SIZE" envDefault:"4194304"` // 4MB
        MaxSendMsgSize int           `env:"GRPC_MAX_SEND_MSG_SIZE" envDefault:"4194304"` // 4MB
        EnableTLS      bool          `env:"GRPC_ENABLE_TLS" envDefault:"false"`
        EnableReflection bool        `env:"GRPC_ENABLE_REFLECTION" envDefault:"false"`
    }

    // Database Configuration
    Database struct {
        Primary struct {
            Host     string        `env:"DB_PRIMARY_HOST" envDefault:"localhost"`
            Port     int           `env:"DB_PRIMARY_PORT" envDefault:"5432"`
            Username string        `env:"DB_PRIMARY_USERNAME"`
            Password string        `env:"DB_PRIMARY_PASSWORD" envUnset:"true"`
            Database string        `env:"DB_PRIMARY_DATABASE" required:"true"`
            SSLMode  string        `env:"DB_PRIMARY_SSL_MODE" envDefault:"disable"`
            MaxConns int           `env:"DB_PRIMARY_MAX_CONNS" envDefault:"25"`
            Timeout  time.Duration `env:"DB_PRIMARY_TIMEOUT" envDefault:"30s"`
        } `envPrefix:"DB_PRIMARY_"`

        ReadOnly struct {
            Host     string        `env:"DB_READ_HOST"`
            Port     int           `env:"DB_READ_PORT" envDefault:"5432"`
            Username string        `env:"DB_READ_USERNAME"`
            Password string        `env:"DB_READ_PASSWORD" envUnset:"true"`
            Database string        `env:"DB_READ_DATABASE"`
            SSLMode  string        `env:"DB_READ_SSL_MODE" envDefault:"disable"`
            MaxConns int           `env:"DB_READ_MAX_CONNS" envDefault:"10"`
            Timeout  time.Duration `env:"DB_READ_TIMEOUT" envDefault:"30s"`
            Enabled  bool          `env:"DB_READ_ENABLED" envDefault:"false"`
        } `envPrefix:"DB_READ_"`

        Migrations struct {
            AutoMigrate   bool     `env:"DB_AUTO_MIGRATE" envDefault:"false"`
            MigrateTable  string   `env:"DB_MIGRATE_TABLE" envDefault:"schema_migrations"`
            MigrationsDir string   `env:"DB_MIGRATIONS_DIR" envDefault:"./migrations"`
        }
    }

    // Cache Configuration
    Cache struct {
        Type      string        `env:"CACHE_TYPE" envDefault:"redis"` // redis, memory, none
        Host      string        `env:"CACHE_HOST" envDefault:"localhost"`
        Port      int           `env:"CACHE_PORT" envDefault:"6379"`
        Password  string        `env:"CACHE_PASSWORD" envUnset:"true"`
        Database  int           `env:"CACHE_DATABASE" envDefault:"0"`
        TTL       time.Duration `env:"CACHE_TTL" envDefault:"1h"`
        MaxSize   int           `env:"CACHE_MAX_SIZE" envDefault:"1000"` // For memory cache
        PoolSize  int           `env:"CACHE_POOL_SIZE" envDefault:"10"`
        Timeout   time.Duration `env:"CACHE_TIMEOUT" envDefault:"5s"`
    }

    // Message Queue Configuration
    Queue struct {
        Type         string        `env:"QUEUE_TYPE" envDefault:"redis"` // redis, rabbitmq, kafka, sqs
        URL          string        `env:"QUEUE_URL"`
        Name         string        `env:"QUEUE_NAME" envDefault:"default"`
        Concurrency  int           `env:"QUEUE_CONCURRENCY" envDefault:"5"`
        Prefetch     int           `env:"QUEUE_PREFETCH" envDefault:"10"`
        RetryAttempts int          `env:"QUEUE_RETRY_ATTEMPTS" envDefault:"3"`
        RetryDelay   time.Duration `env:"QUEUE_RETRY_DELAY" envDefault:"30s"`
        DeadLetter   string        `env:"QUEUE_DEAD_LETTER"`
        Visibility   time.Duration `env:"QUEUE_VISIBILITY" envDefault:"30s"`
    }

    // Authentication & Security
    Security struct {
        JWTSecret          string        `env:"JWT_SECRET" envUnset:"true"`
        JWTExpiration      string        `env:"JWT_EXPIRATION" envDefault:"24h"`
        RefreshExpiration  string        `env:"REFRESH_EXPIRATION" envDefault:"168h"` // 7 days
        BcryptCost         int           `env:"BCRYPT_COST" envDefault:"12"`
        SessionTimeout     time.Duration `env:"SESSION_TIMEOUT" envDefault:"24h"`
        MaxLoginAttempts   int           `env:"MAX_LOGIN_ATTEMPTS" envDefault:"5"`
        LockoutDuration    time.Duration `env:"LOCKOUT_DURATION" envDefault:"15m"`
        RateLimitEnabled   bool          `env:"RATE_LIMIT_ENABLED" envDefault:"true"`
        RateLimitRPS       int           `env:"RATE_LIMIT_RPS" envDefault:"100"`
        IPWhitelistEnabled bool          `env:"IP_WHITELIST_ENABLED" envDefault:"false"`
        IPWhitelist        []string      `env:"IP_WHITELIST" envSeparator:","`
    }

    // Logging Configuration
    Logging struct {
        Level          string `env:"LOG_LEVEL" envDefault:"info"`
        Format         string `env:"LOG_FORMAT" envDefault:"json"` // json, text
        Output         string `env:"LOG_OUTPUT" envDefault:"stdout"` // stdout, stderr, file
        File           string `env:"LOG_FILE" envDefault:"/var/log/service.log"`
        MaxSize        int    `env:"LOG_MAX_SIZE" envDefault:"100"` // MB
        MaxBackups     int    `env:"LOG_MAX_BACKUPS" envDefault:"3"`
        MaxAge         int    `env:"LOG_MAX_AGE" envDefault:"28"` // days
        Compress       bool   `env:"LOG_COMPRESS" envDefault:"true"`
        EnableRequest  bool   `env:"LOG_REQUEST" envDefault:"false"`
        EnableResponse bool   `env:"LOG_RESPONSE" envDefault:"false"`
        EnableCaller   bool   `env:"LOG_CALLER" envDefault:"true"`
    }

    // Monitoring & Observability
    Observability struct {
        MetricsEnabled     bool          `env:"METRICS_ENABLED" envDefault:"true"`
        MetricsPort        int           `env:"METRICS_PORT" envDefault:"9090"`
        MetricsPath        string        `env:"METRICS_PATH" envDefault:"/metrics"`
        TracingEnabled     bool          `env:"TRACING_ENABLED" envDefault:"false"`
        TracingService     string        `env:"TRACING_SERVICE" envDefault:"unknown"`
        TracingEndpoint    string        `env:"TRACING_ENDPOINT"`
        TracingSampleRate  float64       `env:"TRACING_SAMPLE_RATE" envDefault:"1.0"`
        HealthCheckEnabled bool          `env:"HEALTH_CHECK_ENABLED" envDefault:"true"`
        HealthCheckPath    string        `env:"HEALTH_CHECK_PATH" envDefault:"/health"`
        ReadinessPath      string        `env:"READINESS_PATH" envDefault:"/ready"`
        LivenessPath       string        `env:"LIVENESS_PATH" envDefault:"/live"`
        ProfilingEnabled   bool          `env:"PROFILING_ENABLED" envDefault:"false"`
        ProfilingPath      string        `env:"PROFILING_PATH" envDefault:"/debug/pprof"`
    }

    // External Services
    External struct {
        UserServiceURL    string        `env:"USER_SERVICE_URL"`
        AuthServiceURL    string        `env:"AUTH_SERVICE_URL"`
        NotificationURL   string        `env:"NOTIFICATION_SERVICE_URL"`
        EmailServiceURL   string        `env:"EMAIL_SERVICE_URL"`
        StorageURL        string        `env:"STORAGE_SERVICE_URL"`
        PaymentURL        string        `env:"PAYMENT_SERVICE_URL"`
        AnalyticsURL      string        `env:"ANALYTICS_SERVICE_URL"`
        DefaultTimeout    time.Duration `env:"EXTERNAL_SERVICE_TIMEOUT" envDefault:"30s"`
        RetryAttempts     int           `env:"EXTERNAL_SERVICE_RETRY" envDefault:"3"`
    }

    // Feature Flags
    Features struct {
        Enabled     []string `env:"FEATURES_ENABLED" envSeparator:","`
        Disabled    []string `env:"FEATURES_DISABLED" envSeparator:","`
        Beta        bool     `env:"FEATURES_BETA" envDefault:"false"`
        Development bool     `env:"FEATURES_DEVELOPMENT" envDefault:"false"`
    }

    // Business Configuration
    Business struct {
        MaxItemsPerRequest int           `env:"MAX_ITEMS_PER_REQUEST" envDefault:"100"`
        DefaultPageSize    int           `env:"DEFAULT_PAGE_SIZE" envDefault:"20"`
        MaxPageSize        int           `env:"MAX_PAGE_SIZE" envDefault:"100"`
        CacheTimeout       time.Duration `env:"BUSINESS_CACHE_TIMEOUT" envDefault:"5m"`
        RateWindow         time.Duration `env:"RATE_WINDOW" envDefault:"1m"`
        MaxRequestsPerWindow int          `env:"MAX_REQUESTS_PER_WINDOW" envDefault:"1000"`
    }
}

// ParseMicroserviceConfig loads the complete microservice configuration
func ParseMicroserviceConfig() (*MicroserviceConfig, error) {
    var cfg MicroserviceConfig
    if err := env.Parse(&cfg); err != nil {
        return nil, fmt.Errorf("failed to parse microservice config: %w", err)
    }
    return &cfg, nil
}

// MustParseMicroserviceConfig loads configuration and panics on error
func MustParseMicroserviceConfig() *MicroserviceConfig {
    cfg, err := ParseMicroserviceConfig()
    if err != nil {
        panic(fmt.Sprintf("Failed to load microservice configuration: %v", err))
    }
    return cfg
}

// Validate performs comprehensive validation of the microservice configuration
func (c *MicroserviceConfig) Validate() error {
    // Validate service info
    if c.Service.Name == "" {
        return fmt.Errorf("service name is required")
    }

    // Validate ports
    if c.HTTP.Port < 1 || c.HTTP.Port > 65535 {
        return fmt.Errorf("invalid HTTP port: %d", c.HTTP.Port)
    }

    if c.Observability.MetricsPort < 1 || c.Observability.MetricsPort > 65535 {
        return fmt.Errorf("invalid metrics port: %d", c.Observability.MetricsPort)
    }

    if c.GRPC.Port < 1 || c.GRPC.Port > 65535 {
        return fmt.Errorf("invalid gRPC port: %d", c.GRPC.Port)
    }

    // Validate database configuration
    if c.Database.Primary.Database == "" {
        return fmt.Errorf("primary database name is required")
    }

    // Validate timeouts
    if c.HTTP.ReadTimeout <= 0 {
        return fmt.Errorf("HTTP read timeout must be positive")
    }

    if c.HTTP.WriteTimeout <= 0 {
        return fmt.Errorf("HTTP write timeout must be positive")
    }

    // Validate security settings
    if c.Security.JWTSecret == "" {
        return fmt.Errorf("JWT secret is required")
    }

    if c.Security.BcryptCost < 4 || c.Security.BcryptCost > 31 {
        return fmt.Errorf("bcrypt cost must be between 4 and 31")
    }

    // Validate logging
    validLogLevels := []string{"debug", "info", "warn", "error", "fatal"}
    validLogLevel := false
    for _, level := range validLogLevels {
        if c.Logging.Level == level {
            validLogLevel = true
            break
        }
    }
    if !validLogLevel {
        return fmt.Errorf("invalid log level: %s", c.Logging.Level)
    }

    return nil
}

// IsDevelopment returns true if running in development environment
func (c *MicroserviceConfig) IsDevelopment() bool {
    return c.Service.Environment == "development" || c.Service.Environment == "dev"
}

// IsProduction returns true if running in production environment
func (c *MicroserviceConfig) IsProduction() bool {
    return c.Service.Environment == "production" || c.Service.Environment == "prod"
}

// IsFeatureEnabled checks if a feature is enabled
func (c *MicroserviceConfig) IsFeatureEnabled(feature string) bool {
    // Check if explicitly disabled
    for _, disabled := range c.Features.Disabled {
        if disabled == feature {
            return false
        }
    }

    // Check if explicitly enabled
    for _, enabled := range c.Features.Enabled {
        if enabled == feature {
            return true
        }
    }

    // Default behavior
    return c.IsDevelopment() || c.Features.Beta
}

// GetHTTPAddress returns the HTTP server address
func (c *MicroserviceConfig) GetHTTPAddress() string {
    return fmt.Sprintf("%s:%d", c.HTTP.Host, c.HTTP.Port)
}

// GetGRPCAddress returns the gRPC server address
func (c *MicroserviceConfig) GetGRPCAddress() string {
    return fmt.Sprintf("%s:%d", c.GRPC.Host, c.GRPC.Port)
}

// GetMetricsAddress returns the metrics server address
func (c *MicroserviceConfig) GetMetricsAddress() string {
    return fmt.Sprintf("%s:%d", c.HTTP.Host, c.Observability.MetricsPort)
}

// String returns a string representation (excluding sensitive data)
func (c *MicroserviceConfig) String() string {
    return fmt.Sprintf(
        "MicroserviceConfig{Name: %s, Version: %s, Env: %s, HTTP: %s:%d, GRPC: %s:%d, DB: %s@%s:%d/%s}",
        c.Service.Name, c.Service.Version, c.Service.Environment,
        c.HTTP.Host, c.HTTP.Port,
        c.GRPC.Host, c.GRPC.Port,
        c.Database.Primary.Username, c.Database.Primary.Host, c.Database.Primary.Port, c.Database.Primary.Database,
    )
}