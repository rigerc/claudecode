---
name: zerolog
# IMPORTANT: Keep description on ONE line for Claude Code compatibility
# prettier-ignore
description: Use when implementing high-performance zero-allocation JSON logging with Zerolog in Go applications
---

# Zerolog Expert

## Quick Start

High-performance structured logging with zero allocations:

```go
package main

import (
    "os"
    "github.com/rs/zerolog/log"
)

func main() {
    // Global logger setup
    log.Logger = zerolog.New(os.Stdout).With().Timestamp().Logger()

    // Structured logging
    log.Info().
        Str("user", "alice").
        Int("items", 5).
        Msg("Processing complete")
}
```

## Core Principles

- **Zero Allocations**: Direct JSON writing without memory overhead
- **Structured Logging**: Key-value pairs for machine-parseable output
- **Performance First**: Optimized for high-throughput systems
- **Type Safety**: Strongly-typed field methods avoid reflection

## Common Patterns

Production logging with sampling, HTTP middleware with hlog package, custom object marshaling for complex types.

## Reference Files

- [getting-started.md](references/getting-started.md) - Complete setup guide
- [performance-guide.md](references/performance-guide.md) - Optimization patterns
- [production-deployment.md](references/production-deployment.md) - Production best practices

## Notes

Prefer typed field methods, use sampling for high-volume logs, integrate with context for request tracing.

<!--
PROGRESSIVE DISCLOSURE GUIDELINES:
- Keep this file ~50 lines total (max ~150 lines)
- Use 1-2 code blocks only (recommend 1)
- Keep description <200 chars for Level 1 efficiency
- Move detailed docs to references/ for Level 3 loading
- This is Level 2 - quick reference ONLY, not a manual

LLM WORKFLOW (when editing this file):
1. Write/edit SKILL.md
2. Format (if formatter available)
3. Run: claude-skills-cli validate <path>
4. If multi-line description warning: run claude-skills-cli doctor <path>
5. Validate again to confirm
-->
