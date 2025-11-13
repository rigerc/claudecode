# Go Doc Command Quick Reference

## Basic Syntax

```bash
go doc [flags] [package|[package.]symbol[.methodOrField]]
```

## Command Flags

| Flag | Description | Example |
|------|-------------|---------|
| `-all` | Show all documentation for the package | `go doc -all fmt` |
| `-c` | Respect case when matching symbols | `go doc -c JSON` |
| `-cmd` | Show exported symbols for command packages | `go doc -cmd mycmd` |
| `-short` | Show one-line representation for each symbol | `go doc -short fmt` |
| `-src` | Show full source code for the symbol | `go doc -src fmt.Printf` |
| `-u` | Show documentation for unexported symbols | `go doc -u fmt` |
| `-http` | Serve HTML documentation over HTTP | `go doc -http=:6060` |

## Argument Patterns

### No Arguments
```bash
go doc                    # Current package documentation
go doc -all               # Current package with all symbols
go doc -u                 # Include unexported symbols
```

### Single Argument - Package
```bash
go doc fmt                # Standard library package
go doc encoding/json      # Full package path
go doc json               # Lexical matching
```

### Single Argument - Symbol (Current Package)
```bash
go doc MyFunction         # Function in current package
go doc MyType             # Type in current package
go doc MyType.Method      # Method in current package
```

### Single Argument - Package + Symbol
```bash
go doc fmt.Printf         # Function in package
go doc json.Decoder       # Type in package
go doc json.Decode        # Method (matches Decoder.Decode)
go doc http.Client.Do     # Method on specific type
```

### Two Arguments
```bash
go doc encoding/json Marshal    # Package and symbol
go doc net/http Client          # Package and type
go doc text/template New        # Resolve ambiguity
```

## Common Examples

### Package Documentation
```bash
go doc fmt                    # Basic package info
go doc -all fmt               # Complete package documentation
go doc -short fmt             # One-line summaries only
go doc -u fmt                 # Include unexported details
```

### Function Documentation
```bash
go doc fmt.Printf             # Function signature and documentation
go doc -src fmt.Printf        # Include source code
go doc json.Marshal           # Function in specific package
```

### Type Documentation
```bash
go doc json.Decoder           # Type documentation
go doc -all json.Decoder      # Type with all methods
go doc -u json.Decoder        # Include unexported methods
```

### Method Documentation
```bash
go doc json.Decoder.Decode    # Specific method
go doc http.Client.Do         # Method on type
go doc time.Time.Now          # Static method
```

### HTTP Server
```bash
go doc -http                  # Default port 6060
go doc -http=:8080            # Custom port
go doc -http=localhost:6080   # Custom address
go doc -http &                 # Background process
```

## Case Sensitivity

### Default Behavior (Case-Insensitive)
```bash
go doc json      # Matches: json, JSON, Json
go doc fmt       # Matches: fmt, FMT, Fmt
```

### Case-Sensitive Matching
```bash
go doc -c JSON   # Matches only: JSON
go doc -c fmt    # Matches only: fmt (lowercase)
```

## Package Matching Priority

1. GOROOT packages (scanned completely first)
2. GOPATH packages (scanned after GOROOT)
3. Lexical order within each scope
4. First match found is returned

## Special Cases

### Command Packages (package main)
```bash
go doc                    # Hides exported symbols
go doc -cmd              # Shows exported symbols
go doc -all -cmd         # Shows everything
```

### Unexported Symbols
```bash
go doc -u                # Show unexported symbols
go doc -u <type>         # Show unexported methods
go doc -src -u <symbol>  # Show unexported source code
```

### Source Code Viewing
```bash
go doc -src <symbol>      # Show complete source code
go doc -src fmt.Printf   # Function implementation
go doc -src time.Time    # Type definition
```

## URL Patterns for HTTP Server

```
http://localhost:6060/           # Package browser
http://localhost:6060/pkg/fmt/    # fmt package
http://localhost:6060/pkg/net/http/  # net/http package
```

## Integration Examples

### Bash Function
```bash
function godoc() {
    go doc "$@"
}
```

### Vim Command
```vim
command! -nargs=1 GoDoc execute '!go doc <args>'
```

### Development Workflow
```bash
# Start documentation server
go doc -http &

# Quick lookups during development
go doc <symbol>
go doc -src <function>
go doc -all <package>
```