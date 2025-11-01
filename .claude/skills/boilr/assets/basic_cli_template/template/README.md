# {{.AppName}}

{{.Description}}

## Installation

```bash
go install {{.ModuleName}}@latest
```

## Usage

```bash
{{.AppName}} hello
{{.AppName}} version
{{.AppName}} -version
{{.AppName}} -help
```

## Commands

- `hello` - Say hello
- `version` - Show version information

## Options

- `-version` - Show version information
- `-help` - Show help information

## Development

```bash
# Clone the repository
git clone {{.ModuleName}}.git
cd {{.AppName}}

# Install dependencies
go mod tidy

# Run tests
go test ./...

# Build
go build -o {{.AppName}} .

# Run
./{{.AppName}} hello
```

## Author

{{.Author}}

## License

This project is licensed under the MIT License.