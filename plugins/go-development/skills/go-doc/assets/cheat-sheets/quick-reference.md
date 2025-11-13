# Go Doc Quick Reference Cheat Sheet

## Essential Commands

### Basic Usage
```bash
go doc                          # Current package
go doc fmt                      # Specific package
go doc fmt.Printf               # Function
go doc json.Decoder             # Type
go doc json.Decoder.Decode      # Method
```

### Flags
```bash
-all                           # Show all documentation
-short                         # One-line summaries
-u                             # Include unexported symbols
-c                             # Case-sensitive matching
-src                           # Show source code
-cmd                           # Include command symbols
-http                          # Start HTTP server
```

### HTTP Server
```bash
go doc -http                   # Default port 6060
go doc -http=:8080            # Custom port
go doc -http &                 # Background
```

## Common Patterns

### Package Discovery
```bash
go doc -all <package>          # Complete API
go doc -short <package>        # Quick overview
go doc -u <package>            # Include unexported
```

### Function Exploration
```bash
go doc -src <function>         # View implementation
go doc -all | grep <pattern>   # Search for pattern
```

### Type Analysis
```bash
go doc -all <type>             # All methods
go doc -u <type>               # Unexported methods
```

## Troubleshooting

### Package Not Found
```bash
go list <package>              # Verify package exists
go doc -c <ExactSymbol>        # Case-sensitive search
```

### Multiple Matches
```bash
go doc encoding/json           # Use full path
go doc <package> <symbol>      # Two-argument form
```

## Integration

### Development Workflow
```bash
go doc -http &                 # Start server
go doc <symbol>                # Quick lookup
go doc -src <function>         # View code
```

### Editor Integration
```bash
function godoc() { go doc "$@"; }
godoc <symbol>
```

## URL Patterns
```
http://localhost:6060/pkg/fmt/
http://localhost:6060/pkg/net/http/
```