# Go Doc Complete Guide

## Overview

This guide provides specialized expertise for using Go's built-in `go doc` command to access and navigate Go documentation directly from the terminal. It enables efficient exploration of package APIs, function signatures, type methods, and source code without requiring web browsers or external tools.

## Basic Package Documentation

Start with basic package exploration:

```bash
# Show documentation for current package
go doc

# Show documentation for specific package
go doc <package-name>

# Examples for standard library packages
go doc fmt
go doc encoding/json
go doc net/http
```

## Symbol and Method Documentation

Access specific functions, types, and methods:

```bash
# Function documentation
go doc <package>.<function>
go doc fmt.Printf
go doc json.Marshal

# Type documentation
go doc <package>.<type>
go doc json.Decoder
go doc http.Client

# Method documentation
go doc <package>.<type>.<method>
go doc json.Decoder.Decode
go doc http.Client.Do

# Struct field documentation
go doc <package>.<type>.<field>
go doc time.Time.Year
```

## Command Flags Usage

Utilize appropriate flags for different documentation needs:

```bash
# Show all documentation for package
go doc -all <package>

# Case-sensitive matching
go doc -c <ExactCaseSymbol>

# Show unexported symbols
go doc -u <package>

# One-line summaries
go doc -short <package>

# Show source code
go doc -src <symbol>

# Include exported symbols for command packages
go doc -cmd <command-package>
```

## HTTP Documentation Server

Start web-based documentation browsing:

```bash
# Start HTTP server for current package
go doc -http

# Custom port and address
go doc -http=:8080
go doc -http=localhost:8080

# Keep server running in background
go doc -http &

# Access in browser at: http://localhost:6060
```

## Package Matching and Discovery

Understand and leverage package matching behavior:

```bash
# Lexical matching (case-insensitive by default)
go doc json     # Matches encoding/json
go doc fmt      # Matches fmt package

# Case-sensitive exact matching
go doc -c JSON  # Only matches exact "JSON"

# Full package paths
go doc encoding/json
go doc golang.org/x/tools/cmd/goimports
```

## Advanced Documentation Patterns

Use advanced patterns for comprehensive exploration:

```bash
# Current directory exploration
cd $GOPATH/src/<package>
go doc

# Multiple arguments form
go doc <package> <symbol>
go doc encoding/json Marshal

# Browse related functions
go doc -all <package> | grep <pattern>

# Cross-package symbol exploration
go doc <type>                    # Current package type
go doc <package>.<type>          # Specific package type
```

## Integration with Development Workflows

Integrate documentation access into daily development:

```bash
# Quick lookup during development
go doc <symbol>                  # Current package symbol
go doc -src <function>           # View implementation

# Package exploration and learning
go doc -all <new-package>        # Complete package overview
go doc -short <package>         # Quick API summary

# HTTP server for extended browsing
go doc -http &                   # Keep running for reference
```

## Troubleshooting and Debugging

Resolve common documentation access issues:

```bash
# Verify package installation
go list -f '{{.Dir}}' <package>

# Check available symbols in package
go doc -all <package>

# Case-sensitive search for exact matches
go doc -c <ExactSymbolName>

# Try alternative matching forms
go doc <package>.<symbol>
go doc <symbol>                  # Current package
```

## Performance Optimization

Optimize documentation access for large packages:

```bash
# Use -short for quick overview
go doc -short <large-package>

# Use HTTP server for repeated browsing
go doc -http &

# Target specific symbols instead of -all
go doc <package>.<specific-symbol>

# Pipe output for large documentation
go doc -all <package> | less
```

## Editor and IDE Integration

Integrate with text editors and development environments:

```bash
# Quick command-line access
go doc <symbol>

# Background HTTP server
go doc -http=:6060 &

# Script for frequent lookups
function godoc() { go doc "$@"; }

# Package-specific exploration
cd <package-directory>
go doc
```

## Common Workflows

### Package Learning Workflow
1. Start with `go doc <package>` for overview
2. Use `go doc -all <package>` for complete API
3. Use `go doc -short <package>` for quick reference
4. Start `go doc -http` for interactive browsing
5. Use `go doc <package>.<symbol>` for specific details

### Development Integration Workflow
1. Start HTTP server in background: `go doc -http &`
2. Use `go doc <symbol>` for quick lookups during coding
3. Use `go doc -src <function>` to view implementations
4. Use `go doc -u <type>` to understand internal details

### Troubleshooting Workflow
1. Verify package existence with `go list <package>`
2. Check exact symbol names with `go doc -all <package>`
3. Use case-sensitive search with `go doc -c <ExactSymbol>`
4. Try alternative syntax patterns for symbol access

### Package Discovery Workflow
1. Use lexical matching: `go doc <partial-name>`
2. Check GOROOT and GOPATH package availability
3. Use HTTP server for visual exploration
4. Leverage case-insensitive default matching
