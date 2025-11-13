---
name: go-doc
description: Use when working with Go's `go doc` command to access package documentation, explore APIs, view symbols, and manage HTTP documentation servers for terminal workflows.
allowed-tools: [Read, Write, Edit, Glob, Grep, Bash, WebFetch, mcp__context7__resolve-library-id, mcp__context7__get-library-docs]
---

# Go Documentation Expert

Expert assistance for using Go's built-in `go doc` command to access and navigate documentation directly from the terminal.

## When to Use This Skill

Use this skill when you need help with:

- Accessing documentation for Go packages, functions, or methods
- Exploring package APIs and understanding their structure
- Finding specific symbols, methods, or type documentation
- Starting and managing HTTP documentation servers
- Troubleshooting documentation access issues
- Integrating documentation lookup into development workflows

## Quick Start

```bash
# View package documentation
go doc fmt
go doc encoding/json

# View function/method documentation
go doc fmt.Printf
go doc json.Decoder.Decode

# View all package documentation
go doc -all <package>

# Start HTTP documentation server
go doc -http=:6060

# View source code
go doc -src <function>
```

## Available Resources

See `references/` for comprehensive documentation:

- **complete-guide.md**: Full guide covering all go doc features and workflows
- **quick-reference.md**: Quick command syntax and flag reference
- **troubleshooting/issues.md**: Solutions to common documentation access problems
- **examples/common-patterns.md**: Common usage patterns and best practices