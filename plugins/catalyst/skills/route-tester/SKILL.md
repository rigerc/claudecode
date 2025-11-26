---
name: route-tester
description: Use when testing authenticated routes using cookie-based JWT authentication or validating API endpoints with test-auth-route.js patterns.
tags: [testing, authentication, api, routes, jwt, cookies]
---

# Route Tester Skill

Test authenticated routes using cookie-based JWT authentication with automated testing patterns.

## Quick Start

**Basic route test:**
```bash
node scripts/test-auth-route.js http://localhost:3000/api/endpoint
```

**POST with data:**
```bash
node scripts/test-auth-route.js \
  http://localhost:3000/api/submit \
  POST \
  '{"data":"test"}'
```

## Expert Guidance

- **Authentication**: Cookie-based JWT testing patterns
- **test-auth-route.js**: Automated authentication testing tool
- **Endpoints**: GET, POST, PUT, DELETE operations
- **Data Validation**: Request/response verification
- **Error Testing**: Authentication failure scenarios

## Progressive Disclosure

Level 2 provides core patterns and examples. Level 3+ contains detailed testing strategies and authentication debugging.