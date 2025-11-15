---
name: charmlog
# IMPORTANT: Keep description on ONE line for Claude Code compatibility
# prettier-ignore
description: Use for beautiful, minimal, and colorful logging in Go applications with Charmbracelet Log
---

# Charmbracelet Log Expert

## Quick Start

Beautiful colored logging with structured key-value pairs:

```go
package main

import "github.com/charmbracelet/log"

func main() {
    // Simple structured logging
    log.Info("Server started", "port", 8080, "env", "dev")

    // Different log levels
    log.Debug("Debug info")
    log.Warn("Warning message")
    log.Error("Error occurred")
}
```

## Core Principles

- **Minimal API**: Simple, intuitive interface for quick adoption
- **Beautiful Output**: Colorful terminal output using Lip Gloss
- **Structured Logging**: Key-value pairs for organized data
- **Multiple Formats**: Text, JSON, and logfmt output options

## Common Patterns

CLI applications with colored console output, development logging with timestamps, production JSON logging for log aggregation.

## Reference Files

- [getting-started.md](references/getting-started.md) - Complete setup guide
- [styling-guide.md](references/styling-guide.md) - Custom color schemes and styles
- [production-guide.md](references/production-guide.md) - Production deployment patterns

## Notes

Perfect for CLI tools, TUI applications, and developer tools that value beautiful terminal output alongside structured logging capabilities.

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
