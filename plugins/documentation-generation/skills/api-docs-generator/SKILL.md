---
name: api-docs-generator
description: Use to generate comprehensive API documentation from OpenAPI specs, code docstrings, JSDoc/TSDoc comments, and Markdown annotations. Use when creating or updating API documentation from various source formats.
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

# API Documentation Generator

## Quick Start

Generate API documentation from various sources:

```
"Generate API docs from openapi.yaml and save to /docs/API.md"
"Create API documentation from these Python docstrings"
"Document this REST API and save to docs folder"
```

## How It Works

1. **Parse source format** - OpenAPI, docstrings, JSDoc, or Markdown
2. **Extract API details** - endpoints, parameters, responses, examples
3. **Generate documentation** - well-formatted Markdown
4. **Save to location** - `/docs/API.md` or specified path

## Supported Sources

- OpenAPI/Swagger specs (YAML/JSON)
- Python/JavaScript/TypeScript docstrings
- JSDoc/TSDoc comments
- Inline Markdown documentation

See [detailed guide](references/detailed-guide.md) for comprehensive examples and advanced usage.