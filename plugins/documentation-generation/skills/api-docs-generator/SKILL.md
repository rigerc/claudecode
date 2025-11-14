---
name: api-docs-generator
description: Use to generate API documentation from OpenAPI specs, docstrings, or comments. Supports multiple source formats.
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

See `references/` for focused documentation:
- **[quick-start.md](references/quick-start.md)** - Getting started and source format identification
- **[formatting-guide.md](references/formatting-guide.md)** - Documentation structure and formatting best practices
- **[examples.md](references/examples.md)** - Complete code examples and generated outputs
- **[patterns.md](references/patterns.md)** - Common API patterns and design guidelines
- **[troubleshooting.md](references/troubleshooting.md)** - Issues, performance, and optimization