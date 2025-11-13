# Go Doc Troubleshooting Guide

## Common Issues and Solutions

### 1. "no such package" Error

**Problem:**
```bash
$ go doc nonexistentpkg
go doc: no such package "nonexistentpkg"
```

**Solutions:**

#### Check Package Path
```bash
# Verify correct package path
go list <package>

# Example: Check if package exists
go list encoding/json
go list github.com/gorilla/mux

# List available packages
go list all | grep <partial-name>
```

#### Check GOPATH/GOROOT
```bash
# Check Go environment
go env GOPATH
go env GOROOT

# List packages in GOPATH
find $GOPATH/pkg -name "*.a" | head -10

# Install missing package
go get <package-name>
```

#### Try Alternative Names
```bash
# Try full import path
go doc golang.org/x/text/encoding

# Try shorter form
go doc encoding

# Check for module path
go mod why <package>
```

### 2. "no such symbol" Error

**Problem:**
```bash
$ go doc fmt.NonExistent
go doc: no such symbol fmt.NonExistent
```

**Solutions:**

#### Verify Symbol Name
```bash
# List all symbols in package
go doc -all <package>

# Case-sensitive search
go doc -c <ExactSymbolName>

# Search for similar names
go doc -all <package> | grep -i <partial-name>
```

#### Check Current Package
```bash
# If symbol is in current package
cd <package-directory>
go doc -all
go doc <symbol>

# Or use two-argument form
go doc <package> <symbol>
```

#### Verify Export Status
```bash
# Check if symbol is unexported
go doc -u -all <package>

# Unexported symbols need -u flag
go doc -u <package>.<unexportedSymbol>
```

### 3. Multiple Matches Found

**Problem:**
```bash
$ go doc json
# Shows documentation for wrong json package
```

**Solutions:**

#### Use Full Package Path
```bash
# Be specific about package path
go doc encoding/json
go doc github.com/gorilla/websocket/json
```

#### Use Case-Sensitive Matching
```bash
# Use exact case matching
go doc -c JSON          # Only matches exact "JSON"
go doc -c json          # Only matches lowercase "json"
```

#### Use Two-Argument Form
```bash
# Explicitly specify package and symbol
go doc encoding/json Marshal
go doc net/http Client
```

### 4. Command Package Symbols Hidden

**Problem:**
```bash
$ go doc  # In a main package directory
# Shows minimal documentation, no exported symbols
```

**Solutions:**

#### Include Command Symbols
```bash
# Show exported symbols for command packages
go doc -cmd

# Show everything
go doc -all -cmd
```

#### Use Package-Specific Documentation
```bash
# Document specific symbols
go doc <symbol>

# Or use two-argument form
go doc <package> <symbol>
```

### 5. HTTP Server Issues

**Problem:**
```bash
$ go doc -http
# Port already in use or server doesn't start
```

**Solutions:**

#### Use Different Port
```bash
# Try different port
go doc -http=:8080
go doc -http=localhost:8080

# Check available ports
netstat -tlnp | grep :6060
```

#### Check Network Permissions
```bash
# Bind to localhost only
go doc -http=127.0.0.1:6060

# Check firewall settings
# Allow connections to localhost:6060
```

#### Background Process Management
```bash
# Run in background
go doc -http &

# Check if running
ps aux | grep "go doc"

# Kill background process
pkill -f "go doc -http"

# Find and kill specific port
lsof -ti:6060 | xargs kill
```

### 6. Large Package Output Issues

**Problem:**
```bash
$ go doc -all <large-package>
# Output too long to read in terminal
```

**Solutions:**

#### Use Pagination
```bash
# Pipe to pager
go doc -all <package> | less

# Use HTTP server instead
go doc -http &

# Save to file
go doc -all <package> > package-docs.txt
```

#### Use Short Output
```bash
# One-line summaries
go doc -short <package>

# Quick overview
go doc <package>

# Search for specific patterns
go doc -all <package> | grep <pattern>
```

### 7. Case Matching Issues

**Problem:**
```bash
$ go doc JSON
# Shows documentation for lowercase "json" package
```

**Solutions:**

#### Use Case-Sensitive Flag
```bash
# Exact case matching
go doc -c JSON

# Show only exact matches
go doc -c <ExactSymbolName>
```

#### Understand Default Behavior
```bash
# Default is case-insensitive
go doc json          # Matches json, JSON, Json

# Case-sensitive requires -c flag
go doc -c JSON       # Only matches JSON
```

### 8. Module-Related Issues

**Problem:**
```bash
$ go doc <module-package>
# Package not found despite being in go.mod
```

**Solutions:**

#### Verify Module Installation
```bash
# Check if module is downloaded
go list -m <module-name>

# Download module if needed
go mod download <module-name>

# Verify package exists in module
go list <module-package>
```

#### Check Go Version
```bash
# Check Go version
go version

# Some features require newer Go versions
go help doc
```

#### Clean Module Cache
```bash
# Clean module cache
go clean -modcache

# Re-download dependencies
go mod download
```

### 9. Source Code Access Issues

**Problem:**
```bash
$ go doc -src <symbol>
# Source code not displayed
```

**Solutions:**

#### Check Package Installation
```bash
# Verify package is installed with source
go list -f '{{.Dir}}' <package>

# Reinstall with source
go get -d <package>
```

#### Check for Unexported Symbols
```bash
# Include unexported symbols
go doc -src -u <symbol>

# Check if symbol is unexported
go doc -u -all <package>
```

### 10. Performance Issues

**Problem:**
```bash
$ go doc -all <package>
# Command is very slow
```

**Solutions:**

#### Use More Specific Queries
```bash
# Instead of full package, query specific symbol
go doc <package>.<symbol>

# Use short output for overview
go doc -short <package>

# Use HTTP server for browsing
go doc -http &
```

#### Optimize Environment
```bash
# Check for slow network storage
go env GOCACHE
go env GOMODCACHE

# Use local package if available
cd $GOPATH/src/<package>
go doc -all
```

## Debugging Techniques

### 1. Verify Go Environment
```bash
# Check Go installation
go version
go env

# Check package paths
go env GOPATH
go env GOROOT

# Test basic functionality
go doc fmt
go doc -src fmt.Println
```

### 2. Package Validation
```bash
# Verify package exists
go list <package>

# Check package contents
go list -f '{{.Dir}}' <package>

# List package files
find $(go list -f '{{.Dir}}' <package>) -name "*.go"
```

### 3. Symbol Discovery
```bash
# List all symbols
go doc -all <package>

# Search for patterns
go doc -all <package> | grep -i <pattern>

# Case-sensitive search
go doc -c <ExactSymbol>
```

### 4. HTTP Server Debugging
```bash
# Test HTTP server
go doc -http=:8080 &
curl http://localhost:8080/

# Check server logs
go doc -http=:8080 -v

# Test with specific package
cd <package-directory>
go doc -http=:8080 &
```

### 5. Cross-Reference Verification
```bash
# Compare with online documentation
# Visit: https://pkg.go.dev/<package>

# Compare with godoc tool
go install golang.org/x/tools/cmd/godoc@latest
godoc <package>
```

## Common Mistakes to Avoid

### 1. Incorrect Package Paths
```bash
# Wrong
go doc json          # May match wrong package

# Correct
go doc encoding/json
```

### 2. Missing Case-Sensitive Flag
```bash
# Wrong (case-insensitive)
go doc JSON          # May match "json"

# Correct (case-sensitive)
go doc -c JSON
```

### 3. Not Using -cmd for Commands
```bash
# Wrong (hides exported symbols)
go doc              # In main package

# Correct
go doc -cmd
```

### 4. Not Including -u for Unexported
```bash
# Wrong (misses unexported symbols)
go doc -all <package>

# Correct
go doc -all -u <package>
```

## Getting Help

### Built-in Help
```bash
# General help
go help

# Specific help for doc command
go help doc

# Check available flags
go doc -help
```

### Community Resources
- Go documentation: https://golang.org/doc/
- Package documentation: https://pkg.go.dev/
- Go forums: https://forum.golangbridge.org/
- Stack Overflow: https://stackoverflow.com/questions/tagged/go

### Reporting Issues
If you encounter what appears to be a bug with the `go doc` command:

1. Check Go version: `go version`
2. Reproduce with minimal example
3. Report to: https://github.com/golang/go/issues
4. Include: Go version, OS, package name, exact command used