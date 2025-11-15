# jq: Complete Command-Line JSON Processor Guide

jq is a lightweight, flexible command-line JSON processor written in portable C. It functions like sed, awk, and grep for JSON data, enabling you to slice, filter, map, and transform structured data through a powerful filter-based programming language.

## Table of Contents

- [Installation](#installation)
- [Getting Started](#getting-started)
- [Core Concepts](#core-concepts)
- [Basic Operations](#basic-operations)
- [Advanced Filtering](#advanced-filtering)
- [Command-Line Options](#command-line-options)
- [Practical Examples](#practical-examples)
- [Shell Integration](#shell-integration)
- [Performance Tips](#performance-tips)
- [Troubleshooting](#troubleshooting)

## Installation

### On macOS

```bash
# Using Homebrew
brew install jq

# Using MacPorts
sudo port install jq
```

### On Ubuntu/Debian

```bash
# Using apt
sudo apt update
sudo apt install jq

# For the latest version
sudo apt install snapd
sudo snap install jq
```

### On Other Systems

```bash
# From source
git clone https://github.com/jqlang/jq.git
cd jq
autoreconf -fi
./configure
make -j8
sudo make install

# Binary download
wget https://github.com/jqlang/jq/releases/latest/download/jq-linux64
chmod +x jq-linux64
sudo mv jq-linux64 /usr/local/bin/jq
```

## Getting Started

### Basic Usage

```bash
# Pretty-print JSON
echo '{"name":"Alice","age":30}' | jq '.'
# Output:
# {
#   "name": "Alice",
#   "age": 30
# }

# Extract specific field
echo '{"name":"Alice","age":30}' | jq '.name'
# Output: "Alice"

# Extract nested field
echo '{"user":{"name":"Bob","id":42}}' | jq '.user.name'
# Output: "Bob"

# Array indexing (zero-based)
echo '[10,20,30,40]' | jq '.[2]'
# Output: 30

# Negative indexing
echo '[10,20,30,40]' | jq '.[-1]'
# Output: 40
```

### Reading from Files

```bash
# Process JSON file
jq '.' data.json

# Process multiple files
jq '.' file1.json file2.json

# Filter file and save to another file
jq '.users[] | select(.age > 30)' input.json > output.json
```

## Core Concepts

### Filters and Piping

jq uses a filter language where each filter transforms JSON input to JSON output:

```bash
# Identity filter (passes input through)
echo '{"a":1}' | jq '.'

# Function application
echo '[1,2,3]' | jq 'map(. * 2)'
# Output: [2,4,6]

# Pipe operator (|) - filters are composed left to right
echo '{"items":[1,2,3]}' | jq '.items | map(. * 2)'
# Output: [2,4,6]

# Multiple operations in sequence
echo '[1,2,3,4]' | jq '. | map(. * 2) | add'
# Output: 20
```

### Data Types

```bash
# Numbers
echo '42' | jq '. * 2'                    # 84

# Strings
echo '"hello"' | jq '. + " world"'        # "hello world"

# Booleans
echo 'true' | jq '. and false'           # false

# Arrays
echo '[1,2,3]' | jq '.[1]'                # 2

# Objects
echo '{"a":1}' | jq '.a * 2'              # 2

# null
echo 'null' | jq '. // "default"'         # "default"
```

## Basic Operations

### Object Manipulation

```bash
# Select specific keys
echo '{"a":1,"b":2,"c":3}' | jq '{a,c}'
# Output: {"a":1,"c":3}

# Add/modify fields
echo '{"name":"Alice"}' | jq '. + {age: 30, city: "NYC"}'
# Output: {"name":"Alice","age":30,"city":"NYC"}

# Delete fields
echo '{"a":1,"b":2,"c":3}' | jq 'del(.b)'
# Output: {"a":1,"c":3}

# Get all keys
echo '{"z":1,"a":2,"m":3}' | jq 'keys'
# Output: ["a","m","z"]

# Get all values
echo '{"a":1,"b":2}' | jq '.[]'
# Output:
# 1
# 2

# Check if key exists
echo '{"a":1}' | jq 'has("a")'
# Output: true

echo '{"a":1}' | jq 'has("b")'
# Output: false

# Merge objects
echo '[{"a":1},{"b":2}]' | jq 'add'
# Output: {"a":1,"b":2}

# Deep merge
echo '{"a":{"x":1}}' | jq '. * {"a":{"y":2}}'
# Output: {"a":{"x":1,"y":2}}
```

### Array Operations

```bash
# Iterate array elements
echo '[1,2,3]' | jq '.[]'
# Output:
# 1
# 2
# 3

# Map transformation
echo '[1,2,3,4]' | jq 'map(. * 2)'
# Output: [2,4,6,8]

# Filter with condition
echo '[1,2,3,4,5]' | jq 'map(select(. > 2))'
# Output: [3,4,5]

# Array operations
echo '[[1,2],[3,4]]' | jq 'flatten'
# Output: [1,2,3,4]

echo '[3,1,4,1,5]' | jq 'sort'
# Output: [1,1,3,4,5]

echo '[3,1,4,1,5]' | jq 'unique'
# Output: [1,3,4,5]

echo '[1,2,3]' | jq 'reverse'
# Output: [3,2,1]

# Array slicing [start:end]
echo '[0,1,2,3,4,5]' | jq '.[2:4]'
# Output: [2,3]

echo '["a","b","c","d"]' | jq '.[1:]'
# Output: ["b","c","d"]

echo '["a","b","c","d"]' | jq '.[:3]'
# Output: ["a","b","c"]
```

### String Processing

```bash
# String interpolation
echo '{"name":"Alice","age":30}' | jq '"Hello \(.name), you are \(.age) years old"'
# Output: "Hello Alice, you are 30 years old"

# String functions
echo '"hello"' | jq 'ascii_upcase'
# Output: "HELLO"

echo '"WORLD"' | jq 'ascii_downcase'
# Output: "world"

# String operations
echo '"  trim me  "' | jq 'ltrimstr("  ") | rtrimstr("  ")'
# Output: "trim me"

# Split and join
echo '"a,b,c"' | jq 'split(",")'
# Output: ["a","b","c"]

echo '["a","b","c"]' | jq 'join("-")'
# Output: "a-b-c"

# String contains
echo '"hello world"' | jq 'contains("world")'
# Output: true

echo '"hello"' | jq 'startswith("hel")'
# Output: true

echo '"hello"' | jq 'endswith("lo")'
# Output: true

# Regular expressions
echo '"test123data"' | jq 'test("[0-9]+")'
# Output: true

echo '"email@example.com"' | jq 'match("(.+)@(.+)") | .captures | map(.string)'
# Output: ["email","example.com"]
```

## Advanced Filtering

### Conditional Logic

```bash
# If-then-else
echo '5' | jq 'if . > 3 then "big" else "small" end'
# Output: "big"

# If-elif-else
echo '15' | jq 'if . < 10 then "low" elif . < 20 then "medium" else "high" end'
# Output: "medium"

# Ternary-style with // (null coalescing)
echo 'null' | jq '. // "default"'
# Output: "default"

echo '"value"' | jq '. // "default"'
# Output: "value"

# Boolean operators
echo '{"age":25,"active":true}' | jq '.age > 18 and .active'
# Output: true

echo '10' | jq '. == 10 or . == 20'
# Output: true

# Type checking
echo '[1,"hi",null,true]' | jq 'map(type)'
# Output: ["number","string","null","boolean"]

echo '{"a":1}' | jq 'if type == "object" then "is object" else "not object" end'
# Output: "is object"
```

### Select and Filter

```bash
# Select with condition
echo '[1,2,3,4,5]' | jq '.[] | select(. > 3)'
# Output:
# 4
# 5

# Select objects by property
echo '[{"name":"Alice","age":30},{"name":"Bob","age":25}]' | jq '.[] | select(.age > 28)'
# Output: {"name":"Alice","age":30}

# Multiple conditions
echo '[1,2,3,4,5,6]' | jq '.[] | select(. > 2 and . < 5)'
# Output:
# 3
# 4

# Select with regex
echo '["apple.txt","data.json","image.png"]' | jq '.[] | select(test("\\.json$"))'
# Output: "data.json"
```

### Aggregation Functions

```bash
# Sum array
echo '[1,2,3,4,5]' | jq 'add'
# Output: 15

# Min/max
echo '[5,2,8,1,9]' | jq 'min'
# Output: 1

echo '[5,2,8,1,9]' | jq 'max'
# Output: 9

# Length
echo '[1,2,3]' | jq 'length'
# Output: 3

echo '"hello"' | jq 'length'
# Output: 5

echo '{"a":1,"b":2}' | jq 'length'
# Output: 2

# Mean, average, sum
echo '[1,2,3,4,5]' | jq 'add/length'
# Output: 3

# Custom reduce
echo '[1,2,3,4]' | jq 'reduce .[] as $x (0; . + $x)'
# Output: 10

echo '["a","b","c"]' | jq 'reduce .[] as $x (""; . + $x + ",")'
# Output: "a,b,c,"

# Group by
echo '[{"type":"A","val":1},{"type":"B","val":2},{"type":"A","val":3}]' | jq 'group_by(.type)'
# Output: [[{"type":"A","val":1},{"type":"A","val":3}],[{"type":"B","val":2}]]

# Unique by
echo '[{"id":1,"x":"a"},{"id":2,"x":"b"},{"id":1,"x":"c"}]' | jq 'unique_by(.id)'
# Output: [{"id":1,"x":"a"},{"id":2,"x":"b"}]
```

### Functions and Definitions

```bash
# Define function
echo '5' | jq 'def double: . * 2; double'
# Output: 10

# Function with parameters
echo '10' | jq 'def multiply(x): . * x; multiply(3)'
# Output: 30

# Recursive function
echo '5' | jq 'def factorial: if . <= 1 then 1 else . * ((. - 1) | factorial) end; factorial'
# Output: 120

# Function with multiple parameters
echo '[1,2,3,4]' | jq 'def between(a,b): select(. >= a and . <= b); map(between(2;3))'
# Output: [2,3]

# Built-in functions
echo '"hello world"' | jq 'ltrimstr("hello ")'
# Output: "world"

echo '"filename.txt"' | jq 'rtrimstr(".txt")'
# Output: "filename"

echo '{"a":1,"b":2,"c":3}' | jq 'has("a")'
# Output: true
```

## Command-Line Options

### Output Formatting

```bash
# Compact output (single line)
echo '{"a":1,"b":2}' | jq -c '.'
# Output: {"a":1,"b":2}

# Raw output (no quotes for strings)
echo '{"message":"Hello World"}' | jq -r '.message'
# Output: Hello World

# Slurp mode (read entire input into array)
printf '{"id":1}\n{"id":2}\n{"id":3}\n' | jq -s '.'
# Output: [{"id":1},{"id":2},{"id":3}]

# Raw input (treat input as raw string)
echo 'Hello World' | jq -Rs '.'
# Output: "Hello World"

# Combine raw input and output
printf 'line1\nline2\nline3\n' | jq -Rs 'split("\n")'
# Output: ["line1","line2","line3",""]
```

### Variables

```bash
# Pass string variable
jq -n --arg name "Alice" '{"user": $name}'
# Output: {"user":"Alice"}

# Pass JSON variable
jq -n --argjson age 25 '{"age": $age, "valid": ($age >= 18)}'
# Output: {"age":25,"valid":true}

# Multiple variables
jq -n --arg fname "John" --arg lname "Doe" '{name: ($fname + " " + $lname)}'
# Output: {"name":"John Doe"}

# Combine with input
echo '{"id":1}' | jq --arg status "active" '. + {status: $status}'
# Output: {"id":1,"status":"active"}

# Access all variables
jq -n --arg x "foo" --arg y "bar" '$ARGS.named'
# Output: {"x":"foo","y":"bar"}
```

### File Operations

```bash
# Read file as JSON variable
echo '[1,2,3]' > data.json
jq -n --slurpfile nums data.json '$nums[0] | add'
# Output: 6

# Read file as raw text
echo 'SELECT * FROM users' > query.sql
jq -n --rawfile sql query.sql '{query: $sql}'
# Output: {"query":"SELECT * FROM users"}

# Save filter to file
echo '.name | ascii_upcase' > filter.jq
echo '{"name":"alice"}' | jq -f filter.jq
# Output: "ALICE"
```

### Error Handling

```bash
# Exit status based on output truthiness (-e)
echo 'true' | jq -e '.'
echo $?  # 0 (success)

echo 'false' | jq -e '.'
echo $?  # 1 (failure)

echo 'null' | jq -e '.'
echo $?  # 1 (failure)

# Use in shell conditions
if echo '{"enabled":true}' | jq -e '.enabled' > /dev/null; then
    echo "Feature is enabled"
fi

# Try-catch in jq
echo '{"a":"not a number"}' | jq 'try (.a | tonumber) catch 0'
# Output: 0

echo '{"a":"123"}' | jq 'try (.a | tonumber) catch 0'
# Output: 123

# Optional operator (?)
echo '[1,2,"three",4]' | jq '[.[] | tonumber?]'
# Output: [1,2,4]
```

## Practical Examples

### API Response Processing

```bash
# Extract specific fields from API response
curl -s https://api.github.com/users/jqlang | jq '{login, name, public_repos, followers}'

# Filter array of objects
curl -s https://api.github.com/repos/jqlang/jq/issues | jq '[.[] | select(.state == "open")] | length'

# Process paginated results
for page in {1..3}; do
    curl -s "https://api.example.com/data?page=$page" | jq '.items[]'
done | jq -s '.' > all_items.json
```

### Log Processing

```bash
# Process JSON logs
tail -f app.log | jq '.timestamp + " " + .level + " " + .message'

# Filter logs by level
jq 'select(.level == "ERROR")' app.log > errors.log

# Count occurrences by field
jq 'group_by(.level) | map({level: .[0].level, count: length})' app.log

# Extract specific time range
jq 'select(.timestamp >= "2024-01-01" and .timestamp <= "2024-01-31")' app.log
```

### Configuration Management

```bash
# Extract configuration values
jq '.database.host, .database.port' config.json

# Update configuration
jq '.debug = true | .log.level = "verbose"' config.json > new_config.json

# Merge configurations
jq '. * {"production": {"debug": false}}' config.json

# Validate configuration structure
jq 'has("database") and .database | has("host") and has("port")' config.json
```

### Data Transformation

```bash
# CSV to JSON (simple case)
echo 'name,age,city
Alice,30,NYC
Bob,25,SF' | jq -Rs 'split("\n") | .[1:] | map(split(",") | {name: .[0], age: .[1] | tonumber, city: .[2]})'

# Extract URLs from HTML (simplified)
echo '<a href="http://example.com">Link</a>' | jq -R 'match("href=\\"[^\\"]+\\"") | .string | ltrimstr("href=\\"") | rtrimstr("\\"")'

# Process nested data
jq '.users[] | {name, email: .contact.email, address: .location.city}' users.json

# Flatten nested objects
jq '[leaf_paths as $p | {path: $p, value: getpath($p)} | select(.value | type != "object" and .value | type != "array") | group_by(.path) | map({path: .[0].path, value: map(.value)})] | map({(.path | join(".")): .value}) | add' nested.json
```

## Shell Integration

### Pipeline Integration

```bash
# Combine with other Unix tools
curl -s api.example.com/data | jq '.items[].id' | xargs -I {} curl api.example.com/items/{}

# Generate shell commands
echo '{"files":["a.txt","b.txt"]}' | jq -r '.files[] | "rm " + .'

# Process output from other commands
ps aux | jq -R 'split("\\s+") | {user: .[0], pid: .[1], cpu: .[2]}'

# Use with find and process files
find . -name "*.json" -exec jq '.version' {} + | sort | uniq
```

### Script Usage

```bash
#!/bin/bash
# validate-json.sh - Validate JSON files

for file in "$@"; do
    if jq empty "$file" 2>/dev/null; then
        echo "✅ $file is valid"
    else
        echo "❌ $file has errors"
    fi
done

# Usage: ./validate-json.sh *.json
```

### Configuration Functions

```bash
# Function to extract config value
get_config() {
    local key=$1
    local file=$2
    jq -r "$key // empty" "$file"
}

# Function to update config
set_config() {
    local key=$1
    local value=$2
    local file=$3
    tmp=$(mktemp)
    jq "$key = $value" "$file" > "$tmp" && mv "$tmp" "$file"
}
```

## Performance Tips

### Efficient Filtering

```bash
# Use select() early to reduce data
jq 'map(select(.active)) | map(.name)' large.json  # Good
jq 'map(.name) | map(select(.active))' large.json  # Less efficient

# Use pipes instead of multiple passes
jq '.[] | select(.type == "user") | .name' users.json  # Single pass
jq '.[] | .name | select(.type == "user")' users.json   # Multiple passes

# Stream large files
jq --stream 'select(length == 2) | select(.[0][-1] == "price") | .[1]' huge.json
```

### Memory Optimization

```bash
# Process in chunks for large arrays
jq '[.[] | select(.id % 1000 == 0)]' huge.json > sample.json

# Use delete to remove unwanted data early
jq 'del(.metadata, .debug_info)' large.json > clean.json

# Compact output for storage
jq -c '.' data.json > compact.json
```

### Parallel Processing

```bash
# Process files in parallel
find . -name "*.json" -print0 | xargs -0 -P 4 -I {} jq '.version' {}

# Split large JSON and process in parallel
jq -c '.[]' large.json | split -l 1000 - chunk_ &&
for chunk in chunk_*; do
    jq -s 'map(process)' "$chunk" > "processed_$chunk" &
done
wait
```

## Troubleshooting

### Common Errors

```bash
# "cannot index array with string"
echo '[]' | jq '.key'  # Error: cannot index array with string
# Fix: Check the type first
echo '[]' | jq 'if type == "object" then .key else "not an object" end'

# "index out of bounds"
echo '[1]' | jq '.[5]'  # Error: Cannot index array with number 5
# Fix: Check array length or use optional indexing
echo '[1]' | jq '.[5] // "default"'

# "cannot index string with number"
echo '"hello"' | jq '.[0]'  # Error: Cannot index string with number
# Fix: Split string first if needed
echo '"hello"' |jq 'split("") | .[0]'  # "h"
```

### Debugging

```bash
# Use debug() function for debugging
echo '[1,2,3]' | jq 'map(debug("Processing", .) | . * 2)'
# Output:
# "DEBUG: Processing"
# 1
# "DEBUG: Processing"
# 2
# "DEBUG: Processing"
# 3

# Check data types
echo '{"a":1,"b":"text","c":null}' | jq 'to_entries | map({key: .key, type: (.value | type)})'

# Validate JSON structure
jq 'has("required_field") and .items | type == "array"' data.json
```

### Version Compatibility

```bash
# Check jq version
jq --version

# Use features conditionally based on version
jq 'if $VERSION | tonumber >= 1.6 then .[0:5] else . end' data.json
```

## Best Practices

1. **Always use raw output (-r)** when extracting strings for shell commands
2. **Validate JSON first** with `jq empty` before processing
3. **Use select() early** to filter data and reduce processing time
4. **Employ try-catch** for error handling in robust scripts
5. **Leverage variables** (--arg, --argjson) for dynamic filters
6. **Use --compact-output (-c)** for efficient storage and logging
7. **Process streams** with --stream for very large files
8. **Modularize complex filters** using functions and files (-f)

jq is an incredibly versatile tool that bridges the gap between shell scripting and structured data processing. Its combination of simplicity for basic tasks and power for complex transformations makes it essential for any developer working with JSON data.