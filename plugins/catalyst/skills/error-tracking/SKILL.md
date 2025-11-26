---
name: error-tracking
description: Use when adding Sentry v8 error tracking and performance monitoring to your project services, creating controllers, or instrumenting cron jobs. ALL ERRORS MUST BE CAPTURED TO SENTRY.
tags: [error-tracking, sentry, monitoring, performance, debugging]
---

# Error Tracking Skill

Comprehensive Sentry v8 error tracking and performance monitoring for project services with enforced error capture rules.

## Quick Start

**Add Sentry to project:**
```bash
npm install @sentry/node
```

**Error tracking setup:**
```typescript
import * as Sentry from '@sentry/node';

Sentry.init({
  dsn: process.env.SENTRY_DSN,
  environment: process.env.NODE_ENV
});
```

## Expert Guidance

- **Error Capture**: ALL errors must be sent to Sentry (no console.error alone)
- **Performance**: Spans and metrics for monitoring
- **Controllers**: Sentry instrumentation for route handlers
- **Cron Jobs**: Workflow error tracking
- **Database**: Query performance monitoring
- **Integrations**: SystemActionQueueProcessor and patterns

## Critical Rule

**🚨 ALL ERRORS MUST BE CAPTURED TO SENTRY** - Never use console.error without Sentry capture.

## Progressive Disclosure

Level 2 provides core patterns. Level 3+ contains detailed implementation guides and testing strategies.