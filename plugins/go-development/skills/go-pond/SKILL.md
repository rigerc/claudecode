---
name: go-pond
# IMPORTANT: Keep description on ONE line for Claude Code compatibility
# prettier-ignore
description: Use when implementing concurrent Go applications with Pond worker pool library for high-performance task management and goroutine control
---

# Go Pond

## Quick Start

Create a worker pool and submit tasks for concurrent execution:

```go
import "github.com/alitto/pond/v2"

pool := pond.NewPool(100)  // 100 max workers
for i := 0; i < 1000; i++ {
    i := i
    pool.Submit(func() {
        fmt.Printf("Task #%d\n", i)
    })
}
pool.StopAndWait()
```

## Core Principles

- **Automatic Scaling**: Workers created on-demand, removed when idle
- **Task Safety**: Panics captured and returned as errors
- **Context Support**: Tasks respect context cancellation
- **Flexible Submission**: Fire-and-forget, error-returning, or result-returning tasks

## Common Patterns

### Worker Pool with Results

Use ResultPool for tasks returning values:

```go
pool := pond.NewResultPool[string](10)
task := pool.Submit(func() string { return "result" })
result, err := task.Wait()
```

## Reference Files

For detailed documentation, see:
- [pond-library-guide.md](references/pond-library-guide.md) - Complete API reference and examples
- [patterns-examples.md](references/patterns-examples.md) - Advanced patterns and use cases

## Notes

- Always call StopAndWait() or pool.Stop().Wait() for graceful shutdown
- Use context for long-running tasks to support cancellation
- Monitor pool health with built-in metrics methods

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
