---
name: backend-dev-guidelines
description: Use when creating Node.js/Express backend services with routes, controllers, databases, middleware, error tracking, or API patterns.
tags: [backend, nodejs, express, typescript, api, database, microservices]
---

# Backend Development Guidelines

Comprehensive backend development guide for Node.js/Express microservices covering routes, controllers, services, repositories, middleware, testing, and modern patterns.

## Quick Start

**New Express microservice:**
```bash
npm init -y
npm install express prisma zod @sentry/node
npm install -D @types/node typescript ts-node nodemon
```

**Basic route structure:**
```typescript
// src/routes/user.ts
import { Router } from 'express';

export const userRouter = Router();

userRouter.get('/users', async (req, res) => {
  // Route logic
});
```

## Expert Guidance

- **Architecture**: Layered (routes → controllers → services → repositories)
- **Database**: Prisma ORM with TypeScript
- **Validation**: Zod schemas for input validation
- **Error Handling**: Sentry integration for production monitoring
- **Testing**: Unit + integration tests
- **Configuration**: unifiedConfig for environment management
- **Middleware**: Auth, validation, error boundaries
- **BaseController**: Common patterns for route handlers

## Progressive Disclosure

Level 2 provides core patterns and examples. Level 3+ contains detailed implementation guides, testing strategies, and architectural patterns.

## See Also

- **references/architecture.md** - Service layering and patterns
- **references/database.md** - Prisma setup and migrations
- **references/error-handling.md** - Sentry integration and error boundaries
- **references/validation.md** - Zod schemas and validation patterns
- **references/testing.md** - Test strategies and examples
- **references/middleware.md** - Auth, validation, and security layers