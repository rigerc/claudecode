---
name: examples
description: Complete examples demonstrating API documentation generation from OpenAPI specs, Python docstrings, and TypeScript interfaces
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

# API Documentation Generator - Examples

## Example 1: OpenAPI Spec to Markdown

**Input (openapi.yaml):**
```yaml
openapi: 3.0.0
info:
  title: Task API
  version: 1.0.0
  description: Simple task management API

servers:
  - url: https://api.tasks.com/v1

paths:
  /tasks:
    get:
      summary: List all tasks
      tags:
        - Tasks
      parameters:
        - name: status
          in: query
          schema:
            type: string
            enum: [pending, completed, archived]
      responses:
        '200':
          description: Success
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: '#/components/schemas/Task'

    post:
      summary: Create a task
      tags:
        - Tasks
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              required:
                - title
              properties:
                title:
                  type: string
                  minLength: 1
                  maxLength: 200
                description:
                  type: string
                due_date:
                  type: string
                  format: date
      responses:
        '201':
          description: Created
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Task'
        '400':
          description: Validation error

components:
  schemas:
    Task:
      type: object
      properties:
        id:
          type: integer
        title:
          type: string
        description:
          type: string
        status:
          type: string
          enum: [pending, completed, archived]
        created_at:
          type: string
          format: date-time
```

**Output (docs/API.md):**
```markdown
# Task API Documentation

> **Base URL**: `https://api.tasks.com/v1`
> **Version**: 1.0.0

Simple task management API

## Table of Contents

- [Tasks](#tasks)
  - [List Tasks](#list-tasks)
  - [Create Task](#create-task)
- [Models](#models)

---

## Tasks

### List Tasks

Get all tasks with optional filtering.

**Endpoint**: `GET /tasks`

**Query Parameters**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| status | string | No | Filter by status (pending, completed, archived) |

**Response: 200 OK**

```json
[
  {
    "id": 1,
    "title": "Complete project",
    "description": "Finish the API documentation",
    "status": "pending",
    "created_at": "2024-12-16T10:00:00Z"
  }
]
```

---

### Create Task

Create a new task.

**Endpoint**: `POST /tasks`

**Request Body**

```json
{
  "title": "string (required, 1-200 chars)",
  "description": "string (optional)",
  "due_date": "string (optional, date format)"
}
```

**Field Validation**

| Field | Type | Required | Validation |
|-------|------|----------|------------|
| title | string | Yes | 1-200 characters |
| description | string | No | Any string |
| due_date | string | No | ISO 8601 date format |

**Response: 201 Created**

```json
{
  "id": 2,
  "title": "New task",
  "description": "Task description",
  "status": "pending",
  "created_at": "2024-12-16T11:00:00Z"
}
```

**Error Responses**

| Code | Description |
|------|-------------|
| 400 | Validation error |

---

## Models

### Task

```typescript
{
  id: number
  title: string
  description?: string
  status: 'pending' | 'completed' | 'archived'
  created_at: string (ISO 8601)
}
```
```

## Example 2: Python Docstrings to Markdown

**Input (api.py):**
```python
class UserAPI:
    """User management API."""

    def list_users(self, page: int = 1, limit: int = 20) -> List[User]:
        """
        Get paginated list of users.

        GET /api/users

        Args:
            page: Page number (default: 1)
            limit: Items per page (default: 20, max: 100)

        Returns:
            List of User objects

        Raises:
            ValidationError: If page or limit is invalid

        Example:
            >>> api.list_users(page=1, limit=10)
            [User(id=1, username='john'), ...]
        """
        pass

    def create_user(self, username: str, email: str) -> User:
        """
        Create new user.

        POST /api/users

        Args:
            username: Unique username (3-20 characters)
            email: Valid email address

        Returns:
            Created User object

        Raises:
            ValidationError: If validation fails
            ConflictError: If username exists

        Example:
            >>> api.create_user('john_doe', 'john@example.com')
            User(id=123, username='john_doe', email='john@example.com')
        """
        pass
```

**Output (docs/API.md):**
```markdown
# User API Documentation

## Users

### List Users

Get paginated list of users.

**Endpoint**: `GET /api/users`

**Parameters**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| page | integer | No | 1 | Page number |
| limit | integer | No | 20 | Items per page (max 100) |

**Returns**

List of User objects

**Errors**

| Error | Description |
|-------|-------------|
| ValidationError | If page or limit is invalid |

**Example**

```python
api.list_users(page=1, limit=10)
# Returns: [User(id=1, username='john'), ...]
```

---

### Create User

Create new user.

**Endpoint**: `POST /api/users`

**Parameters**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| username | string | Yes | Unique username (3-20 characters) |
| email | string | Yes | Valid email address |

**Returns**

Created User object

**Errors**

| Error | Description |
|-------|-------------|
| ValidationError | If validation fails |
| ConflictError | If username exists |

**Example**

```python
api.create_user('john_doe', 'john@example.com')
# Returns: User(id=123, username='john_doe', email='john@example.com')
```
```

## Example 3: TypeScript Interfaces to Markdown

**Input (types.ts):**
```typescript
/**
 * User creation request
 */
interface CreateUserRequest {
  /** Username (3-20 characters) */
  username: string;

  /** Email address */
  email: string;

  /** User role (optional, default: 'user') */
  role?: 'user' | 'admin' | 'moderator';
}

/**
 * User response object
 */
interface UserResponse {
  /** Unique user ID */
  id: number;

  /** Username */
  username: string;

  /** Email address */
  email: string;

  /** User role */
  role: string;

  /** Account creation timestamp */
  created_at: string;
}

/**
 * Create a new user
 *
 * @param data User creation data
 * @returns Promise resolving to created user
 * @throws {ValidationError} If validation fails
 * @throws {ConflictError} If username exists
 *
 * @example
 * const user = await createUser({
 *   username: 'john_doe',
 *   email: 'john@example.com'
 * });
 */
async function createUser(data: CreateUserRequest): Promise<UserResponse>
```

**Output (docs/API.md):**
```markdown
# API Documentation

## Types

### CreateUserRequest

User creation request

```typescript
{
  username: string          // Username (3-20 characters)
  email: string             // Email address
  role?: 'user' | 'admin' | 'moderator'  // User role (optional, default: 'user')
}
```

### UserResponse

User response object

```typescript
{
  id: number                // Unique user ID
  username: string          // Username
  email: string             // Email address
  role: string              // User role
  created_at: string        // Account creation timestamp
}
```

---

## Functions

### createUser

Create a new user

**Signature**

```typescript
async function createUser(data: CreateUserRequest): Promise<UserResponse>
```

**Parameters**

| Parameter | Type | Description |
|-----------|------|-------------|
| data | CreateUserRequest | User creation data |

**Returns**

Promise resolving to created user

**Throws**

| Error | Description |
|-------|-------------|
| ValidationError | If validation fails |
| ConflictError | If username exists |

**Example**

```typescript
const user = await createUser({
  username: 'john_doe',
  email: 'john@example.com'
});
```
```