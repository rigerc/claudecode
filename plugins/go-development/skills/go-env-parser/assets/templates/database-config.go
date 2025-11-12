// Database Configuration Template
// Supports PostgreSQL, MySQL, and connection pooling

package config

import (
    "fmt"
    "time"

    "github.com/caarlos0/env"
)

type DatabaseConfig struct {
    // Connection Settings
    Host     string `env:"DB_HOST" envDefault:"localhost"`
    Port     int    `env:"DB_PORT" envDefault:"5432"`
    Username string `env:"DB_USERNAME" envDefault:"postgres"`
    Password string `env:"DB_PASSWORD" required:"true" envUnset:"true"`
    Database string `env:"DB_NAME" required:"true"`
    SSLMode  string `env:"DB_SSL_MODE" envDefault:"disable"`

    // Connection Pool Settings
    MaxOpenConns    int           `env:"DB_MAX_OPEN_CONNS" envDefault:"25"`
    MaxIdleConns    int           `env:"DB_MAX_IDLE_CONNS" envDefault:"5"`
    ConnMaxLifetime time.Duration `env:"DB_CONN_MAX_LIFETIME" envDefault:"5m"`
    ConnMaxIdleTime time.Duration `env:"DB_CONN_MAX_IDLE_TIME" envDefault:"5m"`

    // Timeouts and Retries
    ConnectTimeout  time.Duration `env:"DB_CONNECT_TIMEOUT" envDefault:"30s"`
    QueryTimeout    time.Duration `env:"DB_QUERY_TIMEOUT" envDefault:"30s"`
    RetryAttempts   int           `env:"DB_RETRY_ATTEMPTS" envDefault:"3"`
    RetryDelay      time.Duration `env:"DB_RETRY_DELAY" envDefault:"1s"`

    // Database Type (postgresql, mysql, sqlite)
    DBType string `env:"DB_TYPE" envDefault:"postgresql"`

    // SSL/TLS Configuration
    SSLCert  string `env:"DB_SSL_CERT_FILE" envFile:"true"`
    SSLKey   string `env:"DB_SSL_KEY_FILE" envFile:"true"`
    SSLRoot  string `env:"DB_SSL_ROOT_CERT_FILE" envFile:"true"`
    SSLMode2 string `env:"DB_SSL_MODE2" envDefault:"prefer"`

    // Logging
    LogQueries bool `env:"DB_LOG_QUERIES" envDefault:"false"`
    LogLevel   string `env:"DB_LOG_LEVEL" envDefault:"warn"`

    // Migration Settings
    AutoMigrate    bool     `env:"DB_AUTO_MIGRATE" envDefault:"false"`
    MigrateTable   string   `env:"DB_MIGRATE_TABLE" envDefault:"schema_migrations"`
    MigrationsPath string   `env:"DB_MIGRATIONS_PATH" envDefault:"./migrations"`
    SkipMigrations bool     `env:"DB_SKIP_MIGRATIONS" envDefault:"false"`

    // Read Replica Configuration
    ReadReplicaHosts []string `env:"DB_READ_REPLICA_HOSTS" envSeparator:","`
    ReadReplicaPort  int      `env:"DB_READ_REPLICA_PORT" envDefault:"5432"`
    UseReadReplica   bool     `env:"DB_USE_READ_REPLICA" envDefault:"false"`

    // Backup Settings
    BackupEnabled  bool          `env:"DB_BACKUP_ENABLED" envDefault:"false"`
    BackupSchedule string        `env:"DB_BACKUP_SCHEDULE" envDefault:"0 2 * * *"` // Daily at 2 AM
    BackupRetention time.Duration `env:"DB_BACKUP_RETENTION" envDefault:"168h"`      // 7 days
    BackupPath     string        `env:"DB_BACKUP_PATH" envDefault:"./backups"`
}

// ParseDatabaseConfig loads database configuration from environment
func ParseDatabaseConfig() (*DatabaseConfig, error) {
    var cfg DatabaseConfig
    if err := env.Parse(&cfg); err != nil {
        return nil, fmt.Errorf("failed to parse database config: %w", err)
    }
    return &cfg, nil
}

// MustParseDatabaseConfig loads database configuration and panics on error
func MustParseDatabaseConfig() *DatabaseConfig {
    cfg, err := ParseDatabaseConfig()
    if err != nil {
        panic(fmt.Sprintf("Failed to load database configuration: %v", err))
    }
    return cfg
}

// ConnectionString returns the database connection string
func (c *DatabaseConfig) ConnectionString() string {
    switch c.DBType {
    case "postgresql", "postgres":
        return c.postgresConnectionString()
    case "mysql":
        return c.mysqlConnectionString()
    case "sqlite":
        return c.Database
    default:
        return c.postgresConnectionString() // Default to PostgreSQL
    }
}

// postgresConnectionString returns PostgreSQL connection string
func (c *DatabaseConfig) postgresConnectionString() string {
    sslMode := c.SSLMode
    if c.SSLMode2 != "" && c.SSLMode2 != c.SSLMode {
        sslMode = c.SSLMode2
    }

    return fmt.Sprintf("host=%s port=%d user=%s password=%s dbname=%s sslmode=%s",
        c.Host, c.Port, c.Username, c.Password, c.Database, sslMode)
}

// mysqlConnectionString returns MySQL connection string
func (c *DatabaseConfig) mysqlConnectionString() string {
    return fmt.Sprintf("%s:%s@tcp(%s:%d)/%s?charset=utf8mb4&parseTime=True&loc=Local",
        c.Username, c.Password, c.Host, c.Port, c.Database)
}

// ReplicaConnectionString returns connection string for read replicas
func (c *DatabaseConfig) ReplicaConnectionString() string {
    if len(c.ReadReplicaHosts) == 0 {
        return c.ConnectionString()
    }

    // Return first replica's connection string
    host := c.ReadReplicaHosts[0]
    port := c.ReadReplicaPort
    if port == 0 {
        port = c.Port
    }

    switch c.DBType {
    case "postgresql", "postgres":
        return fmt.Sprintf("host=%s port=%d user=%s password=%s dbname=%s sslmode=%s",
            host, port, c.Username, c.Password, c.Database, c.SSLMode)
    case "mysql":
        return fmt.Sprintf("%s:%s@tcp(%s:%d)/%s?charset=utf8mb4&parseTime=True&loc=Local",
            c.Username, c.Password, host, port, c.Database)
    default:
        return fmt.Sprintf("host=%s port=%d user=%s password=%s dbname=%s sslmode=%s",
            host, port, c.Username, c.Password, c.Database, c.SSLMode)
    }
}

// AllConnectionStrings returns connection strings for primary and replicas
func (c *DatabaseConfig) AllConnectionStrings() []string {
    connections := []string{c.ConnectionString()}

    if c.UseReadReplica && len(c.ReadReplicaHosts) > 0 {
        for _, host := range c.ReadReplicaHosts {
            port := c.ReadReplicaPort
            if port == 0 {
                port = c.Port
            }

            var connStr string
            switch c.DBType {
            case "postgresql", "postgres":
                connStr = fmt.Sprintf("host=%s port=%d user=%s password=%s dbname=%s sslmode=%s",
                    host, port, c.Username, c.Password, c.Database, c.SSLMode)
            case "mysql":
                connStr = fmt.Sprintf("%s:%s@tcp(%s:%d)/%s?charset=utf8mb4&parseTime=True&loc=Local",
                    c.Username, c.Password, host, port, c.Database)
            default:
                connStr = fmt.Sprintf("host=%s port=%d user=%s password=%s dbname=%s sslmode=%s",
                    host, port, c.Username, c.Password, c.Database, c.SSLMode)
            }
            connections = append(connections, connStr)
        }
    }

    return connections
}

// Validate performs basic validation of the database configuration
func (c *DatabaseConfig) Validate() error {
    if c.Host == "" {
        return fmt.Errorf("database host is required")
    }

    if c.Port < 1 || c.Port > 65535 {
        return fmt.Errorf("invalid database port: %d (must be 1-65535)", c.Port)
    }

    if c.Database == "" {
        return fmt.Errorf("database name is required")
    }

    validDBTypes := []string{"postgresql", "postgres", "mysql", "sqlite"}
    validType := false
    for _, dbType := range validDBTypes {
        if c.DBType == dbType {
            validType = true
            break
        }
    }
    if !validType {
        return fmt.Errorf("invalid database type: %s (valid: %v)", c.DBType, validDBTypes)
    }

    if c.MaxOpenConns < 1 {
        return fmt.Errorf("MaxOpenConns must be at least 1")
    }

    if c.MaxIdleConns < 0 {
        return fmt.Errorf("MaxIdleConns cannot be negative")
    }

    if c.MaxIdleConns > c.MaxOpenConns {
        return fmt.Errorf("MaxIdleConns cannot be greater than MaxOpenConns")
    }

    return nil
}

// IsSSLMode returns true if SSL/TLS is enabled
func (c *DatabaseConfig) IsSSLMode() bool {
    sslModes := []string{"require", "verify-ca", "verify-full"}
    for _, mode := range sslModes {
        if c.SSLMode == mode || c.SSLMode2 == mode {
            return true
        }
    }
    return false
}

// HasReplicas returns true if read replicas are configured
func (c *DatabaseConfig) HasReplicas() bool {
    return c.UseReadReplica && len(c.ReadReplicaHosts) > 0
}

// String returns a string representation (excluding password)
func (c *DatabaseConfig) String() string {
    return fmt.Sprintf(
        "DatabaseConfig{Host: %s, Port: %d, Username: %s, Database: %s, SSLMode: %s, MaxOpenConns: %d, MaxIdleConns: %d}",
        c.Host, c.Port, c.Username, c.Database, c.SSLMode, c.MaxOpenConns, c.MaxIdleConns,
    )
}