# {{.LibName}}

{{.Description}}

## Installation

```bash
go get {{.ModuleName}}
```

## Usage

```go
package main

import (
    "fmt"
    "{{.ModuleName}}"
)

func main() {
    // Create a new library instance
    lib := {{.LibName}}.New("my-app", "My application")

    // Use the library
    fmt.Println(lib.Greet("World"))

    // Get library information
    info := lib.Info()
    fmt.Printf("Library: %+v\n", info)

    // Output:
    // Hello World! Welcome to my-app.
    // Library: map[created:2023-10-31T12:00:00Z description:My application name:my-app uptime:1.234567ms]
}
```

## Advanced Usage

### Using Options

```go
package main

import (
    "fmt"
    "{{.ModuleName}}"
)

func main() {
    // Create library with options
    lib := {{.LibName}}.New(
        "my-app",
        "My application",
        {{.LibName}}.WithDebug(true),
    )

    fmt.Println(lib.String())
}
```

### Validation

```go
lib := {{.LibName}}.New("", "") // Empty name and description
if err := lib.Validate(); err != nil {
    fmt.Printf("Validation error: %v\n", err)
}
```

## API Documentation

### Functions

- `New(name, description string, opts ...Option) *Library` - Creates a new Library instance
- `WithDebug(debug bool) Option` - Returns an option to enable debug mode
- `Version() string` - Returns the library version

### Methods

- `(*Library) Name() string` - Returns the library name
- `(*Library) Description() string` - Returns the library description
- `(*Library) Created() time.Time` - Returns when the instance was created
- `(*Library) String() string` - Returns string representation
- `(*Library) Greet(who string) string` - Returns a greeting message
- `(*Library) Info() map[string]interface{}` - Returns library information
- `(*Library) Validate() error` - Validates the library configuration

## Development

### Running Tests

```bash
# Run all tests
go test ./...

# Run tests with coverage
go test -cover ./...

# Run specific test
go test -run TestNew

# Run benchmarks
go test -bench=. ./...
```

### Example Output

```bash
$ go test -v ./...
=== RUN   TestNew
--- PASS: TestNew (0.00s)
=== RUN   TestString
--- PASS: TestString (0.00s)
=== RUN   TestGreet
--- PASS: TestGreet (0.00s)
PASS
ok      {{.ModuleName}}    0.002s
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure all tests pass
5. Submit a pull request

## License

{{.License}}

## Author

{{.Author}}