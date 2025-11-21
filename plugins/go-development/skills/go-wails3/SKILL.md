---
name: go-wails3
# prettier-ignore
description: Use for Wails 3 desktop app development with Go backend and web frontend. Expert guidance on project setup, event system, menus, themes, and cross-platform deployment.
---

# Go Wails3

## Quick Start

```go
app := application.New(application.Options{
    Name: "My App",
    Assets: application.AssetOptions{
        Handler: application.AssetFileServerFS(assets),
    },
})

app.Bind(&App{})
app.NewWebviewWindow()
app.Run()
```

## Core Principles

- **Event-Driven Architecture**: Use Go events for frontend-backend communication
- **Asset Embedding**: Embed frontend assets using `//go:embed`
- **Platform Abstraction**: Write once, deploy to Windows/macOS/Linux

## Common Patterns

### Method Binding

Expose Go methods to frontend with `app.Bind()`. Public methods become JavaScript functions automatically.

### Event Communication

Use `ctx.Events.Emit()` from Go and `EventsOn()` in frontend for real-time messaging.

## Reference Files

- [references/complete-guide.md](references/complete-guide.md) - Complete development guide
- [references/quick-reference.md](references/quick-reference.md) - Quick syntax and commands
- [assets/](assets/) - Project templates and examples

## Notes

- Requires Wails v3-alpha: `git checkout v3-alpha && go install`
- Frontend builds automatically during development
- Use `wails3 dev` for hot reload

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
