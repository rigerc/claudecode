---
name: frontend-dev-guidelines
description: Use when creating React/TypeScript applications with modern patterns including Suspense, lazy loading, TanStack Router, MUI v7 styling, or performance optimization.
tags: [frontend, react, typescript, suspense, performance, routing, mui]
---

# Frontend Development Guidelines

Modern React development guide covering Suspense, lazy loading, routing, styling, and performance optimization patterns.

## Quick Start

**New React project with TanStack:**
```bash
npm create react-app myapp --template typescript
cd myapp
npm install @tanstack/react-router @mui/material @tanstack/react-query
```

**Basic lazy component:**
```tsx
import { lazy } from 'react';

const LazyComponent = lazy(() => import('./HeavyComponent'));

function App() {
  return (
    <Suspense fallback={<div>Loading...</div>}>
      <LazyComponent />
    </Suspense>
  );
}
```

## Expert Guidance

- **Suspense**: Handle loading states for async components
- **Lazy Loading**: Code splitting with React.lazy()
- **TanStack Router**: Modern routing with proper type safety
- **MUI v7**: Material-UI component integration
- **Performance**: Bundle optimization and caching strategies
- **TypeScript**: Type safety and best practices
- **File Organization**: Features, components, and shared utilities

## Progressive Disclosure

Level 2 provides core patterns and examples. Level 3+ contains detailed implementation guides and architectural patterns.