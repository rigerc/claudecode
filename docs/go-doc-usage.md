# Go Doc Command: Complete Guide and Usage

## Overview

The `go doc` command is a powerful documentation tool built into the Go toolchain that provides quick access to documentation comments for Go packages, symbols, methods, and functions directly from the terminal. It serves as a convenient alternative to web-based documentation, allowing developers to explore package APIs and understand code structure without leaving their development environment.

## Quick Start

```bash
# Show documentation for current package
go doc

# Show documentation for a specific package
go doc fmt

# Show documentation for a specific function
go doc fmt.Printf

# Show documentation for a method on a type
go doc json.Decoder.Decode

# Start HTTP documentation server
go doc -http
```

## Command Syntax

### Basic Syntax

```bash
go doc [flags] [package|[package.]symbol[.methodOrField]]
```

The command accepts zero, one, or two arguments:

1. **No arguments**: Shows package documentation for the current directory
2. **One argument**: Can be a package, symbol, or method using Go-like syntax
3. **Two arguments**: First is package path, second is symbol or method

### Argument Patterns

```bash
# Package-only forms
go doc <pkg>
go doc <pkg>

# Symbol-only forms (current package)
go doc <sym>[.<methodOrField>]

# Package + symbol forms
go doc [<pkg>.]<sym>[.<methodOrField>]
go doc [<pkg>.][<sym>.]<methodOrField>

# Two-argument form
go doc <pkg> <sym>[.<methodOrField>]
```

## Command Flags

### Core Flags

| Flag | Description | Example |
|------|-------------|---------|
| `-all` | Show all documentation for the package | `go doc -all fmt` |
| `-c` | Respect case when matching symbols (exact match) | `go doc -c JSON` |
| `-cmd` | Show exported symbols for command packages (package main) | `go doc -cmd mycmd` |
| `-short` | Show one-line representation for each symbol | `go doc -short fmt` |
| `-src` | Show full source code for the symbol | `go doc -src fmt.Printf` |
| `-u` | Show documentation for unexported symbols | `go doc -u fmt` |
| `-http` | Serve HTML documentation over HTTP | `go doc -http=:6060` |

### HTTP Server Flags

| Flag | Description | Default | Example |
|------|-------------|---------|---------|
| `-http=addr` | Address to serve documentation on | :6060 | `go doc -http=localhost:8080` |

## Usage Patterns

### 1. Package Documentation

#### Current Package
```bash
# Show documentation for package in current directory
go doc

# With all symbols (including unexported)
go doc -all -u

# For command packages, include exported symbols
go doc -cmd
```

#### Specific Packages
```bash
# Full package path
go doc encoding/json

# Short form (lexically matched)
go doc json

# Show all symbols in package
go doc -all encoding/json
```

### 2. Symbol Documentation

#### Functions and Variables
```bash
# Functions in current package
go doc myFunction
go doc myVariable

# Functions in specific package
go doc fmt.Printf
go doc os.Getenv

# Case-sensitive matching
go doc -c JSON  # Only matches uppercase JSON
go doc json    # Matches json, JSON, Json
```

#### Types and Their Methods
```bash
# Type documentation
go doc json.Decoder

# Specific method
go doc json.Decoder.Decode

# All methods for a type
go doc -all json.Decoder

# Including unexported methods
go doc -all -u json.Decoder
```

#### Struct Fields
```bash
# Struct field documentation
go doc time.Time.Year
go doc json.RawMessage
```

### 3. Advanced Usage

#### Source Code Viewing
```bash
# Show full source for a function
go doc -src fmt.Printf

# Show full source for a type
go doc -src json.Decoder

# Show source for unexported details
go doc -src -u fmt
```

#### HTTP Documentation Server
```bash
# Start server for current package
go doc -http

# Custom address and port
go doc -http=localhost:8080

# Server for specific package
cd $GOPATH/src/encoding/json
go doc -http=:8080
```

#### Case-Sensitive Searching
```bash
# Exact case matching
go doc -c JSON
go doc -c HTTP

# Case-insensitive (default)
go doc json  # Matches json, JSON, Json
```

## Practical Examples

### Example 1: Exploring the fmt Package

```bash
# Basic package overview
go doc fmt

# List all functions in fmt
go doc -all fmt

# Get details for specific function
go doc fmt.Printf

# See the actual implementation
go doc -src fmt.Printf
```

**Output for `go doc fmt.Printf`:**
```
package fmt // import "fmt"

func Printf(format string, a ...any) (n int, err error)
    Printf formats according to a format specifier and writes to standard output.
    It returns the number of bytes written and any write error encountered.
```

### Example 2: Working with HTTP Package

```bash
# HTTP package overview
go doc net/http

# Client struct documentation
go doc net/http.Client

# Specific method documentation
go doc net/http.Client.Do

# Server struct
go doc net/http.Server

# Handler interface
go doc net/http.Handler
```

### Example 3: JSON Package Exploration

```bash
# JSON package documentation
go doc encoding/json

# Marshal function
go doc encoding/json.Marshal

# Decoder type
go doc encoding/json.Decoder

# Decoder's Decode method
go doc encoding/json.Decoder.Decode

# Show source code for Marshal
go doc -src encoding/json.Marshal
```

### Example 4: Custom Package Documentation

```bash
# Navigate to your package directory
cd $GOPATH/src/github.com/youruser/yourpkg

# Show package documentation
go doc

# Show specific symbol
go doc YourType

# Show with unexported details
go doc -u

# Start HTTP server for browsing
go doc -http=:8080
```

## Package Matching Algorithm

The `go doc` command follows a specific order when searching for packages:

1. **GOROOT** is always scanned in its entirety first
2. **GOPATH** is scanned next
3. Within each scope, packages are searched in **breadth-first, lexical order**
4. The first match found is returned

### Example Matching Priority

Given these packages:
- `encoding/json`
- `github.com/someuser/json`

The command `go doc json` will match `encoding/json` because:
1. It's in GOROOT (higher priority than GOPATH)
2. It's lexically first at its level

### Case Sensitivity Rules

- **Lowercase arguments**: Case-insensitive matching
  - `go doc json` matches `json`, `JSON`, `Json`
- **Uppercase arguments**: Case-sensitive matching
  - `go doc JSON` matches only `JSON`
- **Mixed case**: Case-sensitive matching
  - `go doc Json` matches only `Json`

## HTTP Documentation Server

### Starting the Server

```bash
# Basic server on default port (6060)
go doc -http

# Custom port
go doc -http=:8080

# Custom address and port
go doc -http=localhost:8080

# Bind to all interfaces
go doc -http=0.0.0.0:6060
```

### Server Features

The HTTP documentation server provides:

1. **Package browsing**: Navigate through all available packages
2. **Source viewing**: View formatted source code with syntax highlighting
3. **Cross-references**: Click on types, functions, and methods to navigate
4. **Search functionality**: Search across all packages and symbols
5. **Responsive design**: Works well on both desktop and mobile devices

### Server URL Structure

Once the server is running:

- `http://localhost:6060/` - Package browser
- `http://localhost:6060/pkg/fmt/` - fmt package documentation
- `http://localhost:6060/pkg/net/http/` - net/http package documentation

## Advanced Techniques

### 1. Working with Command Packages

For `package main` (commands), exported symbols are hidden by default:

```bash
# In a command package directory
go doc                    # Hides exported symbols
go doc -cmd              # Shows exported symbols
go doc -all -cmd         # Shows everything
```

### 2. Exploring Unexported Details

```bash
# See unexported symbols
go doc -u

# See unexported methods
go doc -u json.Decoder

# See unexported fields
go doc -u time.Time
```

### 3. Finding Related Functions

```bash
# Show all functions that return a specific type
go doc -all | grep "func.*json.Decoder"

# Show all methods for a type
go doc -all json.Decoder

# One-line summaries for quick overview
go doc -short fmt
```

### 4. Integrating with Other Tools

```bash
# Combine with grep for searching
go doc -all fmt | grep Print

# Pipe to less for long documentation
go doc -all net/http | less

# Save documentation to file
go doc -src fmt.Printf > printf.go
```

## Best Practices

### 1. Package Discovery

```bash
# Find packages related to HTTP
go doc -all | grep -i http

# Quick package overview
go doc <package>

# Detailed exploration
go doc -all <package>
```

### 2. Function Understanding

```bash
# Quick function signature
go doc -short <function>

# Full documentation
go doc <function>

# Implementation details
go doc -src <function>
```

### 3. Type Exploration

```bash
# Type overview
go doc <type>

# All methods
go doc -all <type>

# Including unexported methods
go doc -all -u <type>
```

### 4. Development Workflow

```bash
# Start documentation server for current project
go doc -http=:8080

# Keep it running in background
go doc -http=:8080 &

# Use for quick reference during development
go doc <symbol>  # Quick lookup
```

## Common Use Cases

### 1. Learning New Packages

```bash
# Package overview
go doc <new-package>

# Key functions
go doc -all <new-package>

# Example usage
go doc -src <new-package>.<function>
```

### 2. Debugging Type Issues

```bash
# Check method signatures
go doc -all <type>

# Verify interface implementation
go doc <interface>

# See unexported details
go doc -u <type>
```

### 3. API Exploration

```bash
# Quick API reference
go doc -short <package>

# Detailed function documentation
go doc <package>.<function>

# HTTP server for visual browsing
go doc -http <package>
```

### 4. Code Reviews

```bash
# Review function implementation
go doc -src <function>

# Check exported API
go doc -all <package>

# Verify documentation quality
go doc <symbol>
```

## Troubleshooting

### Common Issues

#### 1. "no such package" Error
```bash
# Problem: go doc nonexistentpkg
# Solution: Check package path or GOPATH
go doc <correct-package-path>
```

#### 2. "no such symbol" Error
```bash
# Problem: go doc nonexistentpkg.NonExistentSymbol
# Solutions:
go doc <correct-package-name>        # Check package first
go doc -all <package-name>           # List all symbols
go doc -c <exact-symbol-name>        # Use case-sensitive matching
```

#### 3. Symbol Not Found (Case Issues)
```bash
# Case-sensitive search
go doc -c JSON       # Only matches exact "JSON"
go doc json          # Matches json, JSON, Json
```

#### 4. HTTP Server Won't Start
```bash
# Check if port is in use
go doc -http=:8081   # Try different port

# Check network permissions
go doc -http=127.0.0.1:6060  # Bind to localhost
```

### Debugging Tips

```bash
# List available packages in GOPATH
find $GOPATH/src -name "*.go" -path "*/src/*" | head -10

# CheckGOROOT packages
find $GOROOT/src -name "*.go" | head -10

# Verify package installation
go list -f '{{.Dir}}' <package>

# Test with built-in packages
go doc fmt    # Should always work
go doc -src fmt.Println  # Test source viewing
```

## Integration with IDEs and Editors

### 1. VS Code Integration

Many VS Code Go extensions use `go doc` internally for hover documentation:
```json
{
    "go.useLanguageServer": true,
    "go.docsTool": "go doc"
}
```

### 2. Vim/Neovim Integration

```vim
" Custom command for Go documentation
command! -nargs=1 GoDoc execute '!go doc <args>'
command! GoDocCurrent execute '!go doc'

" View source
command! -nargs=1 GoDocSrc execute '!go doc -src <args>'

" HTTP server
command! GoDocHttp execute '!go doc -http &'
```

### 3. Emacs Integration

```elisp
(defun go-doc (symbol)
  "Show Go documentation for SYMBOL."
  (interactive "sGo doc: ")
  (shell-command (concat "go doc " symbol)))

(defun go-doc-src (symbol)
  "Show Go source for SYMBOL."
  (interactive "sGo doc src: ")
  (shell-command (concat "go doc -src " symbol)))
```

## Performance Considerations

### 1. Large Packages

```bash
# Use -short for quick overview
go doc -short <large-package>

# Use specific symbols instead of -all
go doc <package>.<specific-symbol>

# HTTP server for efficient browsing
go doc -http
```

### 2. Multiple Lookups

```bash
# Use HTTP server for repeated lookups
go doc -http &

# Or pipe to less for large outputs
go doc -all <package> | less
```

### 3. Network Environments

```bash
# Use local cache when available
go doc <package>  # Uses compiled package info

# Avoid repeated network calls
# Keep HTTP server running for browsing
```

## Version-Specific Features

### Go 1.25+ Features

```bash
# New: Enhanced HTTP server integration
go doc -http=package-specific  # Opens specific package

# Improved search and matching
go doc -c <ExactCaseMatch>

# Better source code formatting
go doc -src <symbol>
```

### Legacy Support

For older Go versions, some flags might not be available:
```bash
# Check available flags
go help doc

# Use godoc as fallback (if needed)
go install golang.org/x/tools/cmd/godoc@latest
godoc <package>
```

## Alternatives and Complementary Tools

### 1. godoc

```bash
# Install godoc for advanced features
go install golang.org/x/tools/cmd/godoc@latest

# Start godoc server
godoc -http=:6060

# godoc has additional features like:
# - Corridor browsing
# - Package search
# - Source cross-referencing
```

### 2. pkgsite

```bash
# Install pkgsite for modern web interface
go install golang.org/x/pkgsite/cmd/pkgsite@latest

# Start pkgsite server
pkgsite

# Features:
# - Modern UI
# - Better search
# - Module support
# - Cross-references
```

### 3. Online Resources

- **pkg.go.dev**: Official Go package documentation
- **go.dev**: Official Go documentation and learning resources
- **GitHub**: Source code and inline documentation

## Conclusion

The `go doc` command is an essential tool for Go developers, providing instant access to documentation directly from the terminal. Its simple syntax, powerful features, and integration with the Go toolchain make it ideal for:

- **Quick API lookups** during development
- **Package exploration** and learning
- **Code reviews** and understanding implementations
- **Offline documentation** access
- **Integration** with development workflows

Mastering `go doc` significantly improves productivity and understanding of Go codebases, making it a fundamental tool in every Go developer's toolkit.