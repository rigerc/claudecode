# Go Env Package Examples

Real-world examples and configuration patterns for common application types.

## Basic Web Application

### Simple Configuration

```go
package main

import (
    "fmt"
    "github.com/caarlos0/env"
)

type Config struct {
    Port     int    `env:"PORT" envDefault:"8080"`
    Host     string `env:"HOST" envDefault:"localhost"`
    Debug    bool   `env:"DEBUG" envDefault:"false"`
    LogLevel string `env:"LOG_LEVEL" envDefault:"info"`
}

func main() {
    cfg, err := env.ParseAs[Config]()
    if err != nil {
        panic(err)
    }

    fmt.Printf("Server starting on %s:%d\n", cfg.Host, cfg.Port)
}
```

### Environment Variables

```bash
export PORT=3000
export DEBUG=true
export LOG_LEVEL=debug
```

## Database Configuration

### PostgreSQL Configuration

```go
type DatabaseConfig struct {
    Host         string        `env:"DB_HOST" envDefault:"localhost"`
    Port         int           `env:"DB_PORT" envDefault:"5432"`
    Username     string        `env:"DB_USERNAME" envDefault:"postgres"`
    Password     string        `env:"DB_PASSWORD" required:"true" envUnset:"true"`
    Database     string        `env:"DB_NAME" required:"true"`
    SSLMode      string        `env:"DB_SSL_MODE" envDefault:"disable"`
    MaxOpenConns int           `env:"DB_MAX_OPEN_CONNS" envDefault:"25"`
    MaxIdleConns int           `env:"DB_MAX_IDLE_CONNS" envDefault:"5"`
    ConnMaxLifetime time.Duration `env:"DB_CONN_MAX_LIFETIME" envDefault:"5m"`
}

func (c DatabaseConfig) ConnectionString() string {
    return fmt.Sprintf("host=%s port=%d user=%s password=%s dbname=%s sslmode=%s",
        c.Host, c.Port, c.Username, c.Password, c.Database, c.SSLMode)
}
```

### Redis Configuration

```go
type RedisConfig struct {
    Host     string        `env:"REDIS_HOST" envDefault:"localhost"`
    Port     int           `env:"REDIS_PORT" envDefault:"6379"`
    Password string        `env:"REDIS_PASSWORD"`
    Database int           `env:"REDIS_DATABASE" envDefault:"0"`
    PoolSize int           `env:"REDIS_POOL_SIZE" envDefault:"10"`
    Timeout  time.Duration `env:"REDIS_TIMEOUT" envDefault:"5s"`
}

func (c RedisConfig) Addr() string {
    return fmt.Sprintf("%s:%d", c.Host, c.Port)
}
```

### Multi-Database Configuration

```go
type DatabaseConfig struct {
    Primary   PostgresConfig `envPrefix:"PRIMARY_DB_"`
    Secondary PostgresConfig `envPrefix:"SECONDARY_DB_"`
    Cache     RedisConfig    `envPrefix:"CACHE_"`
}

type PostgresConfig struct {
    Host     string `env:"HOST" envDefault:"localhost"`
    Port     int    `env:"PORT" envDefault:"5432"`
    Username string `env:"USERNAME"`
    Password string `env:"PASSWORD" required:"true" envUnset:"true"`
    Database string `env:"DATABASE" required:"true"`
    SSLMode  string `env:"SSL_MODE" envDefault:"disable"`
}
```

## Microservice Configuration

### Complete Microservice Config

```go
type MicroserviceConfig struct {
    Service struct {
        Name        string `env:"SERVICE_NAME" required:"true"`
        Version     string `env:"SERVICE_VERSION" envDefault:"1.0.0"`
        Environment string `env:"SERVICE_ENV" envDefault:"development"`
        InstanceID  string `env:"INSTANCE_ID" envDefault:"unknown"`
    }

    HTTP struct {
        Host           string        `env:"HTTP_HOST" envDefault:"0.0.0.0"`
        Port           int           `env:"HTTP_PORT" envDefault:"8080"`
        ReadTimeout    time.Duration `env:"HTTP_READ_TIMEOUT" envDefault:"30s"`
        WriteTimeout   time.Duration `env:"HTTP_WRITE_TIMEOUT" envDefault:"30s"`
        IdleTimeout    time.Duration `env:"HTTP_IDLE_TIMEOUT" envDefault:"120s"`
        MaxHeaderBytes int           `env:"HTTP_MAX_HEADER_BYTES" envDefault:"1048576"`
        EnableCORS     bool          `env:"HTTP_ENABLE_CORS" envDefault:"true"`
        CORSOrigins    []string      `env:"HTTP_CORS_ORIGINS" envSeparator:","`
    }

    GRPC struct {
        Host         string        `env:"GRPC_HOST" envDefault:"0.0.0.0"`
        Port         int           `env:"GRPC_PORT" envDefault:"9090"`
        Timeout      time.Duration `env:"GRPC_TIMEOUT" envDefault:"30s"`
        MaxRecvMsgSize int         `env:"GRPC_MAX_RECV_MSG_SIZE" envDefault:"4194304"`
        MaxSendMsgSize int         `env:"GRPC_MAX_SEND_MSG_SIZE" envDefault:"4194304"`
    }

    Database DatabaseConfig `envPrefix:"DB_"`
    Cache    RedisConfig    `envPrefix:"CACHE_"`

    Security struct {
        JWTSecret     string `env:"JWT_SECRET" required:"true" envUnset:"true"`
        JWTExpiration string `env:"JWT_EXPIRATION" envDefault:"24h"`
        BcryptCost    int    `env:"BCRYPT_COST" envDefault:"12"`
        RateLimiting  bool   `env:"RATE_LIMITING" envDefault:"true"`
    }

    Logging struct {
        Level      string `env:"LOG_LEVEL" envDefault:"info"`
        Format     string `env:"LOG_FORMAT" envDefault:"json"`
        Output     string `env:"LOG_OUTPUT" envDefault:"stdout"`
        LogFile    string `env:"LOG_FILE" envDefault:"/var/log/service.log"`
        MaxSize    int    `env:"LOG_MAX_SIZE" envDefault:"100"`
        MaxBackups int    `env:"LOG_MAX_BACKUPS" envDefault:"3"`
        MaxAge     int    `env:"LOG_MAX_AGE" envDefault:"28"`
    }

    Monitoring struct {
        MetricsPort      int           `env:"METRICS_PORT" envDefault:"9090"`
        MetricsPath      string        `env:"METRICS_PATH" envDefault:"/metrics"`
        HealthCheckPath  string        `env:"HEALTH_CHECK_PATH" envDefault:"/health"`
        ReadinessPath    string        `env:"READINESS_PATH" envDefault:"/ready"`
        EnableProfiling  bool          `env:"ENABLE_PROFILING" envDefault:"false"`
        ProfilePath      string        `env:"PROFILE_PATH" envDefault:"/debug/pprof"`
        TracingEnabled   bool          `env:"TRACING_ENABLED" envDefault:"false"`
        TracingService   string        `env:"TRACING_SERVICE" envDefault:"unknown"`
        TracingEndpoint  string        `env:"TRACING_ENDPOINT"`
    }

    Features struct {
        Enabled  []string `env:"ENABLED_FEATURES" envSeparator:","`
        Disabled []string `env:"DISABLED_FEATURES" envSeparator:","`
        Beta     bool     `env:"BETA_FEATURES" envDefault:"false"`
    }

    External struct {
        UserServiceURL string `env:"USER_SERVICE_URL" required:"true"`
        AuthServiceURL string `env:"AUTH_SERVICE_URL" required:"true"`
        EmailServiceURL string `env:"EMAIL_SERVICE_URL"`
        StorageURL     string `env:"STORAGE_URL"`
        PaymentURL     string `env:"PAYMENT_URL"`
    }
}
```

## API Gateway Configuration

```go
type GatewayConfig struct {
    Service struct {
        Name    string `env:"SERVICE_NAME" required:"true"`
        Port    int    `env:"PORT" envDefault:"8080"`
        Domain  string `env:"DOMAIN"`
        TLSCert string `env:"TLS_CERT_FILE" envFile:"true"`
        TLSKey  string `env:"TLS_KEY_FILE" envFile:"true"`
    }

    Upstreams []struct {
        Name      string        `env:"UPSTREAM_NAME" required:"true"`
        URL       string        `env:"UPSTREAM_URL" required:"true"`
        Timeout   time.Duration `env:"UPSTREAM_TIMEOUT" envDefault:"30s"`
        Retries   int           `env:"UPSTREAM_RETRIES" envDefault:"3"`
        CircuitBreaker struct {
            Enabled           bool          `env:"CIRCUIT_BREAKER_ENABLED" envDefault:"false"`
            Threshold         int           `env:"CIRCUIT_BREAKER_THRESHOLD" envDefault:"5"`
            Timeout           time.Duration `env:"CIRCUIT_BREAKER_TIMEOUT" envDefault:"60s"`
            HalfOpenRequests  int           `env:"CIRCUIT_BREAKER_HALF_OPEN_REQUESTS" envDefault:"3"`
        } `envPrefix:"CIRCUIT_BREAKER_"`
    } `envPrefix:"UPSTREAM_"`
}
```

## CLI Application Configuration

```go
type CLIConfig struct {
    ConfigFile string `env:"CONFIG_FILE" envDefault:"$HOME/.config/app/config.yaml" envExpand:"true"`
    DataDir    string `env:"DATA_DIR" envDefault:"$HOME/.local/share/app" envExpand:"true"`
    CacheDir   string `env:"CACHE_DIR" envDefault:"$HOME/.cache/app" envExpand:"true"`

    Output struct {
        Format   string `env:"OUTPUT_FORMAT" envDefault:"table"`
        Verbose  bool   `env:"VERBOSE" envDefault:"false"`
        Quiet    bool   `env:"QUIET" envDefault:"false"`
        Color    bool   `env:"COLOR" envDefault:"true"`
    }

    Network struct {
        Timeout     time.Duration `env:"TIMEOUT" envDefault:"30s"`
        Retries     int           `env:"RETRIES" envDefault:"3"`
        ProxyURL    string        `env:"PROXY_URL"`
        UserAgent   string        `env:"USER_AGENT" envDefault:"app-cli/1.0"`
        MaxConns    int           `env:"MAX_CONNS" envDefault:"10"`
    }
}
```

## Background Worker Configuration

```go
type WorkerConfig struct {
    Service struct {
        Name        string `env:"WORKER_NAME" required:"true"`
        Environment string `env:"ENVIRONMENT" envDefault:"development"`
        Concurrency int    `env:"CONCURRENCY" envDefault:"5"`
    }

    Queue struct {
        Type      string `env:"QUEUE_TYPE" envDefault:"redis"`
        URL       string `env:"QUEUE_URL" required:"true"`
        Name      string `env:"QUEUE_NAME" envDefault:"default"`
        Prefetch  int    `env:"QUEUE_PREFETCH" envDefault:"10"`
    }

    Processing struct {
        Timeout       time.Duration `env:"PROCESSING_TIMEOUT" envDefault:"5m"`
        RetryAttempts int           `env:"RETRY_ATTEMPTS" envDefault:"3"`
        RetryDelay    time.Duration `env:"RETRY_DELAY" envDefault:"30s"`
        MaxMemoryMB   int           `env:"MAX_MEMORY_MB" envDefault:"512"`
    }

    Database DatabaseConfig `envPrefix:"DB_"`
    Cache    RedisConfig    `envPrefix:"CACHE_"`
}
```

## Testing Configuration

### Development Configuration

```go
type DevConfig struct {
    Server struct {
        Port    int    `env:"DEV_PORT" envDefault:"8080"`
        Host    string `env:"DEV_HOST" envDefault:"localhost"`
        TLSEnabled bool `env:"DEV_TLS_ENABLED" envDefault:"false"`
    }

    Database struct {
        Host     string `env:"DEV_DB_HOST" envDefault:"localhost"`
        Port     int    `env:"DEV_DB_PORT" envDefault:"5432"`
        Username string `env:"DEV_DB_USERNAME" envDefault:"dev_user"`
        Password string `env:"DEV_DB_PASSWORD" envDefault:"dev_password"`
        Database string `env:"DEV_DB_NAME" envDefault:"dev_db"`
    }

    Features struct {
        Debug       bool     `env:"DEBUG" envDefault:"true"`
        MockExternalServices bool `env:"MOCK_EXTERNAL" envDefault:"true"`
        LogLevel    string   `env:"LOG_LEVEL" envDefault:"debug"`
        HotReload   bool     `env:"HOT_RELOAD" envDefault:"true"`
    }
}
```

### Test Configuration

```go
type TestConfig struct {
    Database struct {
        Host     string `env:"TEST_DB_HOST" envDefault:"localhost"`
        Port     int    `env:"TEST_DB_PORT" envDefault:"5432"`
        Username string `env:"TEST_DB_USERNAME" envDefault:"test_user"`
        Password string `env:"TEST_DB_PASSWORD" envDefault:"test_password"`
        Database string `env:"TEST_DB_NAME"`
        Migrations string `env:"TEST_DB_MIGRATIONS"`
    }

    Redis struct {
        Host string `env:"TEST_REDIS_HOST" envDefault:"localhost"`
        Port int    `env:"TEST_REDIS_PORT" envDefault:"6379"`
        Database int `env:"TEST_REDIS_DATABASE" envDefault:"1"`
    }

    TestOptions struct {
        Parallel     bool `env:"TEST_PARALLEL" envDefault:"true"`
        Coverage     bool `env:"TEST_COVERAGE" envDefault:"true"`
        RaceDetector bool `env:"TEST_RACE" envDefault:"true"`
        Short        bool `env:"TEST_SHORT" envDefault:"false"`
    }
}
```

## Production Configuration

### Production Config with Security

```go
type ProductionConfig struct {
    Server struct {
        Host      string `env:"HOST" envDefault:"0.0.0.0"`
        Port      int    `env:"PORT" envDefault:"443"`
        TLSCert   string `env:"TLS_CERT_FILE" envFile:"true" required:"true"`
        TLSKey    string `env:"TLS_KEY_FILE" envFile:"true" required:"true"`
        TLSCACert string `env:"TLS_CA_CERT_FILE" envFile:"true"`
    }

    Security struct {
        JWTSecret     string `env:"JWT_SECRET_FILE" envFile:"true" required:"true"`
        EncryptionKey string `env:"ENCRYPTION_KEY_FILE" envFile:"true" required:"true"`
        AllowedOrigins []string `env:"ALLOWED_ORIGINS" envSeparator:"," required:"true"`
        RateLimitRPS  int `env:"RATE_LIMIT_RPS" envDefault:"100"`
        SessionTimeout time.Duration `env:"SESSION_TIMEOUT" envDefault:"24h"`
    }

    Monitoring struct {
        JaegerEndpoint  string `env:"JAEGER_ENDPOINT" required:"true"`
        PrometheusPort  int    `env:"PROMETHEUS_PORT" envDefault:"9090"`
        GrafanaURL      string `env:"GRAFANA_URL"`
        AlertWebhookURL string `env:"ALERT_WEBHOOK_URL"`
    }

    Database DatabaseConfig `envPrefix:"DB_"`
    Cache    RedisConfig    `envPrefix:"CACHE_"`
}
```

## Environment-Specific Examples

### Docker Environment

```go
type DockerConfig struct {
    Service struct {
        Name string `env:"SERVICE_NAME" required:"true"`
        Port int    `env:"PORT" envDefault:"8080"`
    }

    Database struct {
        Host     string `env:"DB_HOST" envDefault:"postgres"`
        Port     int    `env:"DB_PORT" envDefault:"5432"`
        Username string `env:"DB_USERNAME" envDefault:"postgres"`
        Password string `env:"DB_PASSWORD"`
        Database string `env:"DB_NAME" envDefault:"app"`
    }

    Redis struct {
        Host string `env:"REDIS_HOST" envDefault:"redis"`
        Port int    `env:"REDIS_PORT" envDefault:"6379"`
    }
}
```

### Kubernetes Environment

```go
type K8sConfig struct {
    Pod struct {
        Name      string `env:"POD_NAME"`
        Namespace string `env:"POD_NAMESPACE"`
        IP        string `env:"POD_IP"`
        Labels    []string `env:"POD_LABELS" envSeparator:","`
    }

    Service struct {
        Name      string `env:"SERVICE_NAME"`
        Port      int    `env:"SERVICE_PORT"`
        TargetPort int   `env:"SERVICE_TARGET_PORT"`
    }

    Config struct {
        MapName string `env:"CONFIG_MAP_NAME"`
        SecretName string `env:"SECRET_NAME"`
        MountPath string `env:"CONFIG_MOUNT_PATH" envDefault:"/etc/config"`
    }
}
```