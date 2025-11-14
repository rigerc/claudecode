# Configuration Loading

## Loading from Files

### Basic File Loading

```go
import (
    "github.com/knadh/koanf/providers/file"
    "github.com/knadh/koanf/parsers/yaml"
    "github.com/knadh/koanf/parsers/json"
    "github.com/knadh/koanf/parsers/toml"
)

// YAML
k.Load(file.Provider("config.yaml"), yaml.Parser())

// JSON
k.Load(file.Provider("config.json"), json.Parser())

// TOML
k.Load(file.Provider("config.toml"), toml.Parser())
```

### Optional Files

```go
if _, err := os.Stat("config.yaml"); err == nil {
    if err := k.Load(file.Provider("config.yaml"), yaml.Parser()); err != nil {
        log.Fatalf("error loading config: %v", err)
    }
} else {
    log.Println("config.yaml not found, using defaults")
}
```

### Environment-Specific Files

```go
env := os.Getenv("APP_ENV")
if env == "" {
    env = "development"
}

// Load base config
k.Load(file.Provider("config.yaml"), yaml.Parser())

// Load environment-specific overrides
envFile := fmt.Sprintf("config.%s.yaml", env)
if _, err := os.Stat(envFile); err == nil {
    k.Load(file.Provider(envFile), yaml.Parser())
}
```

## Loading from Environment Variables

### Basic Environment Loading

```go
import (
    "strings"
    "github.com/knadh/koanf/providers/env/v2"
)

// Load with prefix and transform
// MYAPP_SERVER_HOST -> server.host
k.Load(env.Provider("MYAPP_", ".", func(s string) string {
    return strings.Replace(
        strings.ToLower(strings.TrimPrefix(s, "MYAPP_")),
        "_", ".", -1,
    )
}), nil)
```

### Advanced Environment Loading

```go
k.Load(env.Provider(".", env.Opt{
    Prefix: "MYAPP_",
    TransformFunc: func(k, v string) (string, any) {
        // Transform key: MYAPP_SERVER_HOST -> server.host
        k = strings.ReplaceAll(
            strings.ToLower(strings.TrimPrefix(k, "MYAPP_")),
            "_", ".",
        )

        // Transform space-separated values into slices
        // MYAPP_TAGS="foo bar baz" -> tags: ["foo", "bar", "baz"]
        if strings.Contains(v, " ") {
            return k, strings.Split(v, " ")
        }

        return k, v
    },
}), nil)
```

## Loading from Command-Line Flags

### Using spf13/pflag

```go
import (
    "github.com/knadh/koanf/providers/posflag"
    flag "github.com/spf13/pflag"
)

f := flag.NewFlagSet("config", flag.ContinueOnError)
f.StringSlice("conf", []string{"config.toml"}, "path to config files")
f.String("host", "localhost", "server host")
f.Int("port", 8080, "server port")
f.Parse(os.Args[1:])

// Load config files from command line
cFiles, _ := f.GetStringSlice("conf")
for _, c := range cFiles {
    if err := k.Load(file.Provider(c), toml.Parser()); err != nil {
        log.Fatalf("error loading file: %v", err)
    }
}

// Override with command-line flags
if err := k.Load(posflag.Provider(f, ".", k), nil); err != nil {
    log.Fatalf("error loading config: %v", err)
}
```

### Using Standard Flag Package

```go
import (
    "flag"
    "github.com/knadh/koanf/providers/basicflag"
)

f := flag.NewFlagSet("config", flag.ExitOnError)
f.String("host", "localhost", "server host")
f.Int("port", 8080, "server port")
f.Parse(os.Args[1:])

k.Load(basicflag.Provider(f, "."), nil)
```

## Loading from Maps and Structs

### From Map (Defaults)

```go
import "github.com/knadh/koanf/providers/confmap"

// Load default values from a flat map
k.Load(confmap.Provider(map[string]interface{}{
    "server.host": "localhost",
    "server.port": 8080,
    "log.level": "info",
}, "."), nil)
```

### From Struct

```go
import "github.com/knadh/koanf/providers/structs"

type DefaultConfig struct {
    Server struct {
        Host string `koanf:"host"`
        Port int    `koanf:"port"`
    } `koanf:"server"`
}

cfg := DefaultConfig{}
cfg.Server.Host = "localhost"
cfg.Server.Port = 8080

k.Load(structs.Provider(cfg, "koanf"), nil)
```

## Loading from Raw Bytes

```go
import (
    "github.com/knadh/koanf/providers/rawbytes"
    "github.com/knadh/koanf/parsers/json"
)

b := []byte(`{"server": {"host": "localhost", "port": 8080}}`)
k.Load(rawbytes.Provider(b), json.Parser())
```

## Loading from AWS S3

```go
import "github.com/knadh/koanf/providers/s3"

if err := k.Load(s3.Provider(s3.Config{
    AccessKey: os.Getenv("AWS_S3_ACCESS_KEY"),
    SecretKey: os.Getenv("AWS_S3_SECRET_KEY"),
    Region:    os.Getenv("AWS_S3_REGION"),
    Bucket:    os.Getenv("AWS_S3_BUCKET"),
    ObjectKey: "config/app.json",
}), json.Parser()); err != nil {
    log.Fatalf("error loading from S3: %v", err)
}
```

## Configuration Merging

### Basic Merging

Load multiple sources and merge them:

```go
// Load defaults
k.Load(confmap.Provider(defaults, "."), nil)

// Load from file (overrides defaults)
k.Load(file.Provider("config.json"), json.Parser())

// Load from environment (overrides file config)
k.Load(env.Provider("MYAPP_", ".", transform), nil)

// Load from flags (final overrides)
k.Load(posflag.Provider(f, ".", k), nil)
```

### Strict Merge Mode

Enable strict merging to prevent type conflicts:

```go
var k = koanf.NewWithConf(koanf.Conf{
    Delim:       ".",
    StrictMerge: true,
})

// This will error if types conflict during merge
if err := k.Load(file.Provider("config.json"), json.Parser()); err != nil {
    log.Fatalf("merge error: %v", err)
}
```

### Custom Merge Function

```go
k.Load(file.Provider("config.json"), json.Parser(), koanf.WithMergeFunc(
    func(src, dest map[string]interface{}) error {
        // Custom merge logic
        for k, v := range src {
            dest[k] = v // Simple override
        }
        return nil
    },
))
```

## Available Providers

| Provider | Package | Description |
|----------|---------|-------------|
| file | github.com/knadh/koanf/providers/file | Local files |
| env | github.com/knadh/koanf/providers/env/v2 | Environment variables |
| posflag | github.com/knadh/koanf/providers/posflag | pflag (POSIX) |
| basicflag | github.com/knadh/koanf/providers/basicflag | Go flag package |
| confmap | github.com/knadh/koanf/providers/confmap | Go maps |
| structs | github.com/knadh/koanf/providers/structs | Go structs |
| rawbytes | github.com/knadh/koanf/providers/rawbytes | Byte slices |
| s3 | github.com/knadh/koanf/providers/s3 | AWS S3 |

## Third-Party Providers

- **vault** - HashiCorp Vault
- **appconfig** - AWS AppConfig
- **etcd** - CNCF etcd
- **consul** - HashiCorp Consul
- **parameterstore** - AWS Systems Manager Parameter Store
- **secretsmanager** - AWS Secrets Manager
