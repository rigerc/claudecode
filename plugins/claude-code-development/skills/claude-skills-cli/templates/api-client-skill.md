---
name: api-client-helper
description: Creating and configuring API client code for REST services. Use when working with HTTP requests, API authentication, or client libraries.
allowed-tools: Read, Write, Edit, Grep, Glob
---

# API Client Helper

## Overview
Creating and configuring API client code for REST services, including authentication, error handling, and request/response processing.

## When to Use
Use this skill when:
- Setting up API client connections
- Configuring authentication for APIs
- Handling HTTP requests and responses
- Implementing error handling for API calls
- Working with API documentation and integration
- Creating client libraries or wrappers

## Instructions
1. **Analyze API Requirements**: Examine API documentation and identify endpoints, authentication, and data formats
2. **Choose HTTP Library**: Select appropriate client library based on language and requirements
3. **Configure Authentication**: Set up API keys, OAuth, or other auth mechanisms
4. **Implement Client Code**: Create functions for API interactions
5. **Add Error Handling**: Handle network errors, API errors, and edge cases
6. **Test Integration**: Verify connectivity and functionality

## HTTP Libraries by Language

### Python
- **requests**: Simple, synchronous HTTP client
- **httpx**: Async/await support, HTTP/2
- **aiohttp**: Async HTTP client/server

### JavaScript/Node.js
- **axios**: Promise-based, request/response interceptors
- **fetch**: Native browser API, available in Node.js 18+
- **got**: Modern, powerful HTTP client

### Go
- **net/http**: Standard library HTTP client
- **resty**: Simple HTTP and REST client library

### Java
- **OkHttp**: Efficient HTTP client
- **Apache HttpClient**: Feature-rich HTTP client
- **Spring RestTemplate**: Spring framework client

## Authentication Patterns

### API Key Authentication
```python
import requests

headers = {
    'Authorization': 'Bearer YOUR_API_KEY',
    'Content-Type': 'application/json'
}
response = requests.get('https://api.example.com/data', headers=headers)
```

### OAuth 2.0
```python
import requests

token = get_oauth_token()  # Implement OAuth flow
headers = {'Authorization': f'Bearer {token}'}
response = requests.get('https://api.example.com/data', headers=headers)
```

### Basic Authentication
```python
import requests
from requests.auth import HTTPBasicAuth

response = requests.get('https://api.example.com/data',
                        auth=HTTPBasicAuth('username', 'password'))
```

## Error Handling Patterns

### Network Errors
- Connection timeouts
- DNS resolution failures
- SSL/TLS errors

### HTTP Status Codes
- 2xx: Success responses
- 4xx: Client errors (bad request, unauthorized, etc.)
- 5xx: Server errors

### API-Specific Errors
- Rate limiting
- Invalid requests
- Service unavailable

## Examples

### Example 1: Simple GET Client
**User request**: "Create a client to fetch user data from the GitHub API"
**Workflow**:
1. Analyze GitHub API documentation
2. Set up authentication with personal access token
3. Implement function to fetch user data
4. Add error handling for rate limits and invalid users
5. Test with sample requests

### Example 2: POST Request Client
**User request**: "Build a client to submit data to a REST API endpoint"
**Workflow**:
1. Examine API endpoint documentation
2. Configure authentication headers
3. Implement POST request function
4. Add request validation and error handling
5. Test with sample data

### Example 3: Async API Client
**User request**: "Create an async client to handle multiple API calls concurrently"
**Workflow**:
1. Choose async HTTP library (httpx/aiohttp)
2. Implement async request functions
3. Set up concurrent request handling
4. Add error handling and retry logic
5. Test with multiple simultaneous requests

## Best Practices
- Store credentials securely (environment variables, secret managers)
- Implement retry logic for transient failures
- Add request/response logging for debugging
- Use appropriate timeouts for network requests
- Validate input data before sending requests
- Handle API rate limiting gracefully
- Document API integration clearly

## Troubleshooting
### Issue: Authentication failures
**Solution**: Verify API key format, check token expiration, ensure correct auth method

### Issue: Rate limiting
**Solution**: Implement exponential backoff, respect rate limit headers

### Issue: SSL/TLS errors
**Solution**: Update certificates, verify API endpoint security

### Issue: Invalid JSON responses
**Solution**: Add response validation, handle malformed data gracefully

For more examples, see [API client examples](references/api-examples.md).