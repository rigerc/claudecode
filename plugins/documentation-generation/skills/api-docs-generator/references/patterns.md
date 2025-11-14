---
name: patterns
description: Common patterns, additional resources, and tips for better API documentation generation results
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash
  - WebFetch
  - TodoWrite
---

# API Documentation Generator - Patterns and Resources

## Additional Resources

See the templates directory for:
- [REST API Template](templates/REST_API_TEMPLATE.md) - Standard REST API documentation structure
- [GraphQL API Template](templates/GRAPHQL_API_TEMPLATE.md) - GraphQL schema documentation
- [WebSocket API Template](templates/WEBSOCKET_API_TEMPLATE.md) - Real-time API documentation

See the examples directory for:
- [OpenAPI Example](examples/openapi-example.yaml) - Complete OpenAPI spec
- [Python Docstrings Example](examples/python-api.py) - Well-documented Python API
- [TypeScript Example](examples/typescript-api.ts) - TypeScript with JSDoc

See the scripts directory for:
- [openapi_to_markdown.py](scripts/openapi_to_markdown.py) - Convert OpenAPI to Markdown
- [extract_docstrings.py](scripts/extract_docstrings.py) - Extract Python docstrings
- [generate_docs.sh](scripts/generate_docs.sh) - Automated doc generation

## Tips for Better Results

1. **Provide Complete Source**: Include all files with API definitions
2. **Specify Base URL**: Mention the API base URL if known
3. **Include Examples**: Provide example requests/responses if available
4. **Note Authentication**: Specify auth requirements
5. **Mention Versioning**: Include API version information
6. **Request Specific Sections**: Ask for specific parts if updating existing docs

## Common Patterns

### REST APIs
- Standard CRUD operations (GET, POST, PUT, DELETE)
- Resource-based URLs (/users, /posts)
- JSON request/response bodies
- HTTP status codes for responses

### GraphQL APIs
- Single endpoint (usually /graphql)
- Query and Mutation documentation
- Schema type definitions
- Resolver examples

### WebSocket APIs
- Connection establishment
- Event types and payloads
- Error handling
- Reconnection logic

### Microservices Architecture
- Service discovery and registration
- Inter-service communication patterns
- API gateway documentation
- Service contracts and SLAs

### Event-Driven APIs
- Event sourcing documentation
- Message queue schemas
- Consumer patterns
- Event versioning strategies

### Authentication Patterns

#### Bearer Token Authentication
```
Authorization: Bearer <token>
```
- Token-based authentication
- JWT (JSON Web Tokens) documentation
- Token refresh mechanisms
- Scope and permissions

#### API Key Authentication
```
X-API-Key: <api-key>
```
- Key generation and management
- Rate limiting per key
- Key rotation policies
- Environment-specific keys

#### OAuth 2.0 Flows
- Authorization Code Grant
- Client Credentials Grant
- Implicit Grant (deprecated)
- Resource Owner Password Credentials

### Response Patterns

#### Standard Response Format
```json
{
  "data": { ... },
  "meta": {
    "version": "1.0",
    "timestamp": "2024-12-16T10:00:00Z"
  },
  "links": { ... }
}
```

#### Error Response Format
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid input",
    "details": { ... }
  }
}
```

#### Paginated Response Format
```json
{
  "data": [ ... ],
  "pagination": {
    "page": 1,
    "limit": 20,
    "total": 150,
    "total_pages": 8
  }
}
```

### Documentation Structure Patterns

#### Single File Documentation
```
API.md
├── Overview
├── Authentication
├── Endpoints
│   ├── Users
│   ├── Posts
│   └── Comments
├── Models/Schemas
├── Error Codes
└── Changelog
```

#### Multi-File Documentation
```
docs/
├── README.md          # Overview and quick start
├── authentication.md  # Auth details
├── endpoints/
│   ├── users.md       # User endpoints
│   ├── posts.md       # Post endpoints
│   └── comments.md    # Comment endpoints
├── models.md          # Data models
├── errors.md          # Error reference
└── changelog.md       # Version history
```

#### Versioned Documentation
```
docs/
├── v1/
│   ├── README.md
│   ├── endpoints/
│   └── models/
├── v2/
│   ├── README.md
│   ├── endpoints/
│   └── models/
└── migration-guide.md # v1 to v2 migration
```

### API Design Patterns

#### Resource Naming Conventions
- Use plural nouns for collections: `/users`, `/posts`
- Use specific identifiers: `/users/{id}`, `/posts/{slug}`
- Hierarchical resources: `/users/{id}/posts`
- Query parameters for filtering: `/users?role=admin`

#### HTTP Method Usage
- `GET`: Retrieve resources (no side effects)
- `POST`: Create new resources
- `PUT`: Replace entire resources
- `PATCH`: Partial updates to resources
- `DELETE`: Remove resources

#### Status Code Patterns
- `200 OK`: Successful GET, PUT, PATCH
- `201 Created`: Successful POST
- `204 No Content`: Successful DELETE
- `400 Bad Request`: Validation errors
- `401 Unauthorized`: Authentication required
- `403 Forbidden`: Insufficient permissions
- `404 Not Found`: Resource doesn't exist
- `409 Conflict`: Resource already exists
- `422 Unprocessable Entity`: Validation failed

### Content Type Patterns

#### JSON APIs
```
Content-Type: application/json
Accept: application/json
```

#### Multipart Form Data
```
Content-Type: multipart/form-data
```

#### XML APIs
```
Content-Type: application/xml
Accept: application/xml
```

#### Binary Data
```
Content-Type: application/octet-stream
Content-Type: image/jpeg
Content-Type: application/pdf
```

### Caching Patterns

#### Cache-Control Headers
```
Cache-Control: public, max-age=3600
Cache-Control: private, no-cache
Cache-Control: no-store
```

#### ETag Implementation
```
ETag: "abc123"
If-None-Match: "abc123"
```

#### Last-Modified Headers
```
Last-Modified: Wed, 21 Oct 2015 07:28:00 GMT
If-Modified-Since: Wed, 21 Oct 2015 07:28:00 GMT
```

### Rate Limiting Patterns

#### Rate Limit Headers
```
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 999
X-RateLimit-Reset: 1625097600
```

#### Rate Limit Responses
```json
{
  "error": {
    "code": "RATE_LIMIT_EXCEEDED",
    "message": "Too many requests",
    "retry_after": 60
  }
}
```

#### Different Rate Limiting Strategies
- Per IP address
- Per API key
- Per user account
- Per endpoint
- Sliding window vs. fixed window

### Security Patterns

#### HTTPS Enforcement
- Redirect HTTP to HTTPS
- HSTS headers
- TLS configuration
- Certificate management

#### CORS Configuration
```javascript
Access-Control-Allow-Origin: https://example.com
Access-Control-Allow-Methods: GET, POST, PUT, DELETE
Access-Control-Allow-Headers: Content-Type, Authorization
```

#### Input Validation
- Parameter type validation
- Length and format checks
- SQL injection prevention
- XSS protection

#### Output Sanitization
- Remove sensitive data
- Sanitize error messages
- Prevent information leakage
- Mask PII (Personally Identifiable Information)

### Testing Patterns

#### API Testing Strategy
- Unit tests for individual endpoints
- Integration tests for workflows
- Load testing for performance
- Security testing for vulnerabilities

#### Test Documentation
```
## Testing

### Running Tests
```bash
npm test
```

### Test Coverage
- Endpoints: 100%
- Error scenarios: 95%
- Authentication: 100%
```

#### Example Test Cases
- Happy path scenarios
- Error conditions
- Edge cases
- Performance benchmarks

### Monitoring and Observability

#### Logging Patterns
- Structured logging (JSON format)
- Request/response logging
- Error tracking
- Performance metrics

#### Health Check Endpoints
```
GET /health
GET /health/ready
GET /health/live
```

#### Metrics Collection
- Request count and duration
- Error rates by type
- Resource utilization
- Business metrics

### Documentation Maintenance Patterns

#### Automated Documentation Updates
- CI/CD pipeline integration
- Scheduled documentation generation
- Version-controlled documentation
- Automated validation

#### Documentation Review Process
- Code review for documentation changes
- Technical writing review
- Accuracy verification
- User feedback incorporation

#### Documentation Analytics
- Page views and time on page
- Search queries and results
- User feedback and ratings
- Documentation feature requests

### Community and Collaboration Patterns

#### API Documentation Standards
- OpenAPI Specification compliance
- JSON Schema validation
- Markdown formatting standards
- Consistent terminology

#### Developer Experience
- Interactive API explorers
- Code generation tools
- SDK documentation
- Sample applications

#### Feedback Loops
- Developer forums
- Issue tracking
- Feature requests
- Bug reporting workflows