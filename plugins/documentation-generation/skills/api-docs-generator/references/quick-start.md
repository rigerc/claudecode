---
name: quick-start
description: Quick start guide for API documentation generation including overview, source format identification, and information extraction
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

# API Documentation Generator - Quick Start

## Overview

Automatically generate clean, comprehensive API documentation from multiple source formats and save to `/docs/API.md`. Supports OpenAPI/Swagger specifications, Python/JavaScript/TypeScript docstrings, JSDoc/TSDoc comments, and inline Markdown documentation.

## Quick Start

Provide API source code or specifications and specify the output location:

```
"Generate API docs from openapi.yaml and save to /docs/API.md"
"Create API documentation from these Python docstrings"
"Document this REST API and save to docs folder"
```

The skill will:
1. Parse the source format (OpenAPI, docstrings, JSDoc, etc.)
2. Extract endpoints, parameters, responses, and examples
3. Generate well-formatted Markdown documentation
4. Save to `/docs/API.md` or specified location

## Step 1: Identify Source Format

Recognize and parse different documentation sources:

### OpenAPI/Swagger Specifications

**YAML Format:**
```yaml
openapi: 3.0.0
info:
  title: User API
  version: 1.0.0
paths:
  /users/{id}:
    get:
      summary: Get user by ID
      parameters:
        - name: id
          in: path
          required: true
          schema:
            type: integer
      responses:
        '200':
          description: Successful response
```

**JSON Format:**
```json
{
  "openapi": "3.0.0",
  "info": {
    "title": "User API",
    "version": "1.0.0"
  },
  "paths": {
    "/users/{id}": {
      "get": {
        "summary": "Get user by ID"
      }
    }
  }
}
```

### Python Docstrings

**Function Documentation:**
```python
def create_user(username: str, email: str, role: str = "user") -> dict:
    """
    Create a new user account.

    Args:
        username (str): The desired username (3-20 characters)
        email (str): User's email address
        role (str, optional): User role. Defaults to "user".

    Returns:
        dict: Created user object with id, username, email, and role

    Raises:
        ValueError: If username is already taken
        ValidationError: If email format is invalid

    Example:
        >>> create_user("john_doe", "john@example.com")
        {'id': 123, 'username': 'john_doe', 'email': 'john@example.com', 'role': 'user'}
    """
    pass
```

**Class Documentation:**
```python
class UserAPI:
    """
    User management API endpoints.

    This class provides RESTful endpoints for user CRUD operations.
    All endpoints require authentication except for registration.

    Attributes:
        base_url (str): Base URL for all user endpoints
        timeout (int): Request timeout in seconds
    """

    def get_user(self, user_id: int) -> User:
        """
        Retrieve user by ID.

        GET /api/users/{user_id}

        Args:
            user_id: Unique user identifier

        Returns:
            User object with all details

        Raises:
            NotFoundError: If user doesn't exist
            AuthError: If not authenticated
        """
        pass
```

### JSDoc/TSDoc Comments

**JavaScript/TypeScript:**
```typescript
/**
 * Create a new user account
 *
 * @route POST /api/users
 * @param {Object} userData - User registration data
 * @param {string} userData.username - Desired username (3-20 chars)
 * @param {string} userData.email - Email address
 * @param {string} [userData.role=user] - User role
 * @returns {Promise<User>} Created user object
 * @throws {ValidationError} If input validation fails
 * @throws {ConflictError} If username already exists
 *
 * @example
 * const user = await createUser({
 *   username: 'john_doe',
 *   email: 'john@example.com'
 * });
 */
async function createUser(userData: CreateUserDto): Promise<User> {
  // implementation
}

/**
 * User API endpoints
 * @namespace UserAPI
 */

/**
 * Get user by ID
 *
 * @memberof UserAPI
 * @function getUser
 * @param {number} id - User ID
 * @returns {Promise<User>} User object
 */
```

### Inline Markdown Comments

```javascript
/*
# User Management API

## Create User
**POST** `/api/users`

Creates a new user account.

### Request Body
```json
{
  "username": "string",
  "email": "string",
  "role": "string (optional)"
}
```

### Response
**200 OK**
```json
{
  "id": 123,
  "username": "john_doe",
  "email": "john@example.com",
  "role": "user"
}
```

### Errors
- `400` - Validation error
- `409` - Username already exists
*/
```

## Step 2: Extract API Information

For each endpoint/function, extract:

**Core Information:**
- **Method**: GET, POST, PUT, DELETE, PATCH
- **Path**: /api/users, /api/users/{id}
- **Summary**: Brief description
- **Description**: Detailed explanation
- **Authentication**: Required auth type
- **Tags/Categories**: Grouping for organization

**Parameters:**
- **Path parameters**: {id}, {slug}
- **Query parameters**: ?page=1&limit=10
- **Header parameters**: Authorization, Content-Type
- **Request body**: Schema, required fields, types

**Responses:**
- **Success responses**: 200, 201, 204
- **Error responses**: 400, 401, 403, 404, 500
- **Response schemas**: JSON structure
- **Examples**: Sample requests and responses

**Additional Details:**
- **Deprecation warnings**
- **Rate limiting**
- **Versioning**
- **Security requirements**