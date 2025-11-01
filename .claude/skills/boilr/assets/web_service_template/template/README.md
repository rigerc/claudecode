# {{.ServiceName}}

{{.Description}}

## Running the service

### Development

```bash
go run cmd/{{.ServiceName}}/main.go
```

### Build and run

```bash
go build -o {{.ServiceName}} ./cmd/{{.ServiceName}}
./{{.ServiceName}}
```

## API Endpoints

- `GET /` - Welcome message
- `GET /health` - Health check
- `GET /api/v1/info` - Service information

### Health Check

```bash
curl http://localhost:{{.Port}}/health
```

Response:
```json
{
  "status": "ok",
  "service": "{{.ServiceName}}",
  "timestamp": "2023-10-31T12:00:00Z",
  "port": {{.Port}}
}
```

### Service Info

```bash
curl http://localhost:{{.Port}}/api/v1/info
```

Response:
```json
{
  "service": "{{.ServiceName}}",
  "description": "{{.Description}}",
  "version": "1.0.0",
  "endpoints": [
    "/",
    "/health",
    "/api/v1/info"
  ],
  "port": {{.Port}}
}
```

## Environment Variables

- `PORT` - Server port (default: {{.Port}})
- `ENABLE_TLS` - Enable TLS (default: {{.EnableTLS}})

## Development

```bash
# Install dependencies
go mod tidy

# Run tests
go test ./...

# Run with specific port
PORT=3000 go run cmd/{{.ServiceName}}/main.go

# Run with TLS
ENABLE_TLS=true go run cmd/{{.ServiceName}}/main.go
```

## Docker

```dockerfile
FROM golang:1.21-alpine AS builder
WORKDIR /app
COPY go.mod go.sum ./
RUN go mod download
COPY . .
RUN CGO_ENABLED=0 GOOS=linux go build -o {{.ServiceName}} ./cmd/{{.ServiceName}}

FROM alpine:latest
RUN apk --no-cache add ca-certificates
WORKDIR /root/
COPY --from=builder /app/{{.ServiceName}} .
EXPOSE {{.Port}}
CMD ["./{{.ServiceName}}"]
```

## License

This project is licensed under the MIT License.