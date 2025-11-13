# Common Go Doc Usage Patterns

## 1. Package Learning Pattern

### Initial Package Exploration
```bash
# Step 1: Get basic overview
go doc <package>

# Step 2: See complete API
go doc -all <package>

# Step 3: Quick reference
go doc -short <package>

# Step 4: Start HTTP server for browsing
go doc -http &
```

### Example: Learning fmt Package
```bash
go doc fmt
go doc -all fmt
go doc -short fmt
go doc -http &
# Visit http://localhost:6060/pkg/fmt/
```

## 2. Function Discovery Pattern

### Finding Functions in Package
```bash
# List all functions
go doc -all <package>

# Search for specific function type
go doc -all <package> | grep "func.*<pattern>"

# Case-sensitive search
go doc -c <ExactFunctionName>
```

### Example: Find JSON Functions
```bash
go doc -all encoding/json
go doc -all encoding/json | grep "func.*[Mm]arshal"
go doc -c Marshal
```

## 3. Type Exploration Pattern

### Understanding a Type
```bash
# Type documentation
go doc <package>.<type>

# All methods for type
go doc -all <package>.<type>

# Including unexported methods
go doc -all -u <package>.<type>

# Specific method
go doc <package>.<type>.<method>
```

### Example: Understanding http.Client
```bash
go doc net/http.Client
go doc -all net/http.Client
go doc net/http.Client.Do
go doc -src net/http.Client.Do
```

## 4. Method Chaining Pattern

### Exploring Method Chains
```bash
# Starting type
go doc <package>.<type>

# First method
go doc <package>.<type>.<method1>

# Return type analysis
go doc <package>.<return-type>

# Continue chain
go doc <package>.<return-type>.<method2>
```

### Example: Database Connection Chain
```bash
go doc database/sql.DB
go doc database/sql.DB.Query
go doc database/sql.Rows
go doc database/sql.Rows.Scan
```

## 5. Interface Implementation Pattern

### Finding Interface Implementations
```bash
# Interface documentation
go doc <package>.<interface>

# Common implementations
go doc -all <package> | grep "type.*struct"

# Specific implementation
go doc <package>.<implementation>
```

### Example: io.Reader Implementations
```bash
go doc io.Reader
go doc -all fmt | grep "Reader"
go doc -all bytes | grep "Reader"
go doc bytes.Buffer
```

## 6. Error Handling Pattern

### Understanding Error Types
```bash
# Error type documentation
go doc <package>.<Error>

# Error variables
go doc -all <package> | grep "var.*err\|Error"

# Error creation functions
go doc <package>.New
go doc <package>.Errorf
```

### Example: HTTP Errors
```bash
go doc net/http.Error
go doc -all net/http | grep "var.*[Ee]rror"
go doc net/http.StatusText
```

## 7. Configuration Pattern

### Exploring Configuration Options
```bash
# Config type documentation
go doc <package>.<Config>

# Constructor functions
go doc <package>.New
go doc <package>.DefaultConfig

# Option functions
go doc -all <package> | grep "func.*[Ww]ith\|Option"
```

### Example: HTTP Server Configuration
```bash
go doc net/http.Server
go doc net/http.ListenAndServe
go doc -all net/http | grep "func.*[Ss]erver"
```

## 8. Testing Pattern

### Finding Testing Utilities
```bash
# Testing package overview
go doc testing

# Testing functions
go doc -all testing | grep "func.*[Tt]est\|Assert"

# Mock types
go doc -all <package> | grep "type.*[Mm]ock\|Fake"
```

### Example: HTTP Testing
```bash
go doc net/http/httptest
go doc net/http/httptest.NewServer
go doc -all net/http/httptest
```

## 9. Debugging Pattern

### Debugging Symbol Access
```bash
# Check if symbol exists
go doc <package>.<symbol>

# Try different case combinations
go doc -c <ExactSymbol>
go doc <lowercase-symbol>

# List all symbols to find correct name
go doc -all <package>

# Check current package symbols
go doc -all
```

### Example: Debugging JSON Issues
```bash
go doc encoding/json.Unmarshal
go doc -src encoding/json.Unmarshal
go doc -u encoding/json.Unmarshal
go doc json.UnmarshalError
```

## 10. Integration Development Pattern

### During Development
```bash
# Start HTTP server for reference
go doc -http &

# Quick symbol lookups
go doc <symbol>

# View implementation
go doc -src <function>

# Check method availability
go doc -all <type>
```

### Example: Building HTTP Handler
```bash
# Start doc server
go doc -http &

# Research handler interface
go doc net/http.Handler
go doc net/http.HandlerFunc

# Check response writer
go doc net/http.ResponseWriter

# View example implementation
go doc -src net/http.HandlerFunc.ServeHTTP
```

## 11. Package Migration Pattern

### When Moving Between Packages
```bash
# Old package overview
go doc <old-package>

# New package overview
go doc <new-package>

# Compare specific functions
go doc <old-package>.<function>
go doc <new-package>.<function>

# Find equivalents
go doc -all <new-package> | grep "<pattern>"
```

### Example: Migration from JSON
```bash
go doc encoding/json
go doc -all encoding/json | grep Marshal

# Research alternative
go doc github.com/json-iterator/go
go doc -all github.com/json-iterator/go | grep Marshal
```

## 12. Performance Analysis Pattern

### Understanding Performance Characteristics
```bash
# Function documentation for complexity notes
go doc <package>.<function>

# Source code for implementation details
go doc -src <package>.<function>

# Related types for memory usage
go doc <package>.<type>

# Benchmark functions
go doc -all <package> | grep "func.*[Bb]enchmark"
```

### Example: Container Performance
```bash
go doc container/list
go doc -src container/list.PushBack
go doc -src container/list.Len
go doc -all container/list | grep benchmark
```

## 13. Cross-Package Analysis Pattern

### Understanding Dependencies
```bash
# Main package documentation
go doc <main-package>

# Referenced package types
go doc <dependency-package>.<type>

# Integration patterns
go doc -all <main-package> | grep <dependency>

# Interface implementations
go doc <main-package>.<type>
go doc <dependency-package>.<interface>
```

### Example: HTTP + JSON Integration
```bash
go doc net/http
go doc encoding/json
go doc net/http.Client
go doc encoding/json.Decoder
go doc -all net/http | grep json
```

## 14. Source Code Learning Pattern

### Learning from Implementations
```bash
# View source code
go doc -src <package>.<function>

# Study unexported helpers
go doc -src -u <package>

# Understand type definitions
go doc -src <package>.<type>

# Analyze algorithm implementations
go doc -src <algorithm-function>
```

### Example: Learning Sort Implementation
```bash
go doc sort
go doc -src sort.Sort
go doc -src sort.Interface
go doc -src -u sort
```

## 15. Quick Reference Pattern

### Rapid Information Access
```bash
# One-liner summaries
go doc -short <package>

# Quick function signature
go doc <package>.<function>

# Method list for type
go doc -short -all <package>

# HTTP server for visual browsing
go doc -http &
```

### Example: Quick fmt Reference
```bash
go doc -short fmt
go doc fmt.Printf
go doc -short -all fmt
go doc -http &
```