---
name: formatting-guide
description: Guide for structuring and formatting API documentation, including best practices for clear and comprehensive docs
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

# API Documentation Generator - Formatting Guide

## Step 3: Structure Documentation

Organize documentation in a clear, navigable format:

```markdown
# API Documentation

> **Base URL**: `https://api.example.com/v1`
> **Version**: 1.0.0
> **Last Updated**: 2024-12-16

## Table of Contents

- [Authentication](#authentication)
- [Users](#users)
  - [List Users](#list-users)
  - [Get User](#get-user)
  - [Create User](#create-user)
  - [Update User](#update-user)
  - [Delete User](#delete-user)
- [Posts](#posts)
- [Error Codes](#error-codes)

---

## Authentication

All API requests require authentication using Bearer tokens.

### Headers

```http
Authorization: Bearer <your-api-token>
Content-Type: application/json
```

### Getting an API Token

1. Register for an account
2. Navigate to Settings > API Keys
3. Generate a new API key
4. Include in all requests

---

## Users

### List Users

Get a paginated list of all users.

**Endpoint**: `GET /api/users`

**Authentication**: Required

**Query Parameters**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `page` | integer | No | 1 | Page number |
| `limit` | integer | No | 20 | Items per page (max 100) |
| `role` | string | No | all | Filter by role (user, admin, moderator) |
| `search` | string | No | - | Search by username or email |

**Response: 200 OK**

```json
{
  "data": [
    {
      "id": 123,
      "username": "john_doe",
      "email": "john@example.com",
      "role": "user",
      "created_at": "2024-01-15T10:30:00Z"
    }
  ],
  "pagination": {
    "page": 1,
    "limit": 20,
    "total": 150,
    "total_pages": 8
  }
}
```

**Error Responses**

| Code | Description |
|------|-------------|
| 401 | Unauthorized - Invalid or missing token |
| 403 | Forbidden - Insufficient permissions |
| 422 | Validation error - Invalid parameters |

**Example Request**

```bash
curl -X GET "https://api.example.com/v1/users?page=1&limit=20" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

**Example Response**

```json
{
  "data": [...],
  "pagination": {...}
}
```

---

### Get User

Retrieve a specific user by ID.

**Endpoint**: `GET /api/users/{id}`

**Authentication**: Required

**Path Parameters**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `id` | integer | Yes | User ID |

**Response: 200 OK**

```json
{
  "id": 123,
  "username": "john_doe",
  "email": "john@example.com",
  "role": "user",
  "bio": "Software developer",
  "avatar_url": "https://example.com/avatars/123.jpg",
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-02-20T14:45:00Z"
}
```

**Error Responses**

| Code | Description |
|------|-------------|
| 404 | User not found |
| 401 | Unauthorized |

---

### Create User

Create a new user account.

**Endpoint**: `POST /api/users`

**Authentication**: Admin only

**Request Body**

```json
{
  "username": "string (required, 3-20 chars)",
  "email": "string (required, valid email)",
  "password": "string (required, min 8 chars)",
  "role": "string (optional, default: user)"
}
```

**Field Validation**

| Field | Type | Required | Validation |
|-------|------|----------|------------|
| username | string | Yes | 3-20 characters, alphanumeric + underscore |
| email | string | Yes | Valid email format |
| password | string | Yes | Minimum 8 characters, must include letter and number |
| role | string | No | One of: user, moderator, admin |

**Response: 201 Created**

```json
{
  "id": 124,
  "username": "new_user",
  "email": "new@example.com",
  "role": "user",
  "created_at": "2024-12-16T10:00:00Z"
}
```

**Error Responses**

| Code | Description |
|------|-------------|
| 400 | Validation error - Check error details |
| 409 | Conflict - Username or email already exists |
| 403 | Forbidden - Admin access required |

**Example Request**

```bash
curl -X POST "https://api.example.com/v1/users" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "new_user",
    "email": "new@example.com",
    "password": "SecurePass123"
  }'
```

---

## Error Codes

### Standard Error Response

All errors return a consistent format:

```json
{
  "error": {
    "code": "ERROR_CODE",
    "message": "Human-readable error message",
    "details": {
      "field": "username",
      "reason": "Already taken"
    }
  }
}
```

### HTTP Status Codes

| Code | Meaning | Common Causes |
|------|---------|---------------|
| 400 | Bad Request | Invalid input, validation failure |
| 401 | Unauthorized | Missing or invalid token |
| 403 | Forbidden | Insufficient permissions |
| 404 | Not Found | Resource doesn't exist |
| 409 | Conflict | Duplicate resource |
| 422 | Unprocessable Entity | Validation error |
| 429 | Too Many Requests | Rate limit exceeded |
| 500 | Internal Server Error | Server error |

### Error Codes

| Code | Description |
|------|-------------|
| `VALIDATION_ERROR` | Input validation failed |
| `AUTHENTICATION_REQUIRED` | Missing authentication |
| `INVALID_TOKEN` | Token is invalid or expired |
| `INSUFFICIENT_PERMISSIONS` | User lacks required permissions |
| `RESOURCE_NOT_FOUND` | Requested resource doesn't exist |
| `DUPLICATE_RESOURCE` | Resource already exists |
| `RATE_LIMIT_EXCEEDED` | Too many requests |

---

## Rate Limiting

- **Limit**: 100 requests per minute per API key
- **Headers**:
  - `X-RateLimit-Limit`: Total requests allowed
  - `X-RateLimit-Remaining`: Requests remaining
  - `X-RateLimit-Reset`: Timestamp when limit resets

When rate limit is exceeded:

```json
{
  "error": {
    "code": "RATE_LIMIT_EXCEEDED",
    "message": "Too many requests. Please try again in 60 seconds."
  }
}
```

---

## Versioning

API version is specified in the URL path:

- **Current**: `/v1/`
- **Deprecated**: `/v0/` (sunset date: 2025-06-30)

Breaking changes will result in a new version. Non-breaking changes are added to the current version.

---

## Changelog

### Version 1.0.0 (2024-12-16)
- Initial API release
- User management endpoints
- Authentication with Bearer tokens
```

## Step 4: Format for Clarity

Apply consistent formatting:

**Headers and Sections:**
- Use clear hierarchy (H1 for title, H2 for resources, H3 for endpoints)
- Include table of contents for navigation
- Group related endpoints together

**Tables:**
- Use tables for parameters, fields, and error codes
- Include Type, Required, Default, and Description columns
- Keep tables concise and scannable

**Code Blocks:**
- Syntax highlight JSON, bash, etc.
- Include complete, runnable examples
- Show both request and response

**Visual Clarity:**
- Use blockquotes for important notes
- Use badges/tags for HTTP methods (GET, POST, etc.)
- Use emoji sparingly for visual markers (⚠️ for warnings)
- Consistent spacing between sections

**Cross-References:**
- Link to related endpoints
- Reference error codes section
- Link to authentication section

## Step 5: Save to /docs/API.md

**Default Location:**
```
/docs/API.md
```

**Alternative Locations:**
```
/docs/api/README.md
/api-docs/API.md
/documentation/API.md
```

**File Organization:**

For large APIs, consider splitting:
```
/docs/
  ├── API.md              # Overview and quick start
  ├── authentication.md   # Auth details
  ├── users.md           # User endpoints
  ├── posts.md           # Post endpoints
  └── errors.md          # Error reference
```

## Best Practices

### Documentation Quality

1. **Be Comprehensive**: Document all endpoints, parameters, and responses
2. **Use Examples**: Include real, working examples
3. **Explain Errors**: Document all possible error responses
4. **Keep Updated**: Regenerate docs when API changes
5. **Add Context**: Explain business logic and use cases

### Organization

1. **Logical Grouping**: Group related endpoints together
2. **Consistent Naming**: Use consistent terminology
3. **Clear Navigation**: Include table of contents
4. **Searchable**: Use descriptive headers and keywords
5. **Version Control**: Note API version and changelog

### Formatting

1. **Markdown Standards**: Follow standard Markdown syntax
2. **Syntax Highlighting**: Use proper language tags for code blocks
3. **Tables for Structure**: Use tables for parameters and fields
4. **Consistent Style**: Maintain consistent formatting throughout
5. **Visual Hierarchy**: Use headers appropriately

### User Experience

1. **Quick Start**: Provide simple getting started example
2. **Authentication First**: Document auth requirements clearly
3. **Common Patterns**: Show typical usage patterns
4. **Troubleshooting**: Include common issues and solutions
5. **Links**: Cross-reference related sections