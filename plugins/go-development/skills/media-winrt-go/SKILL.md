---
name: media-winrt-go
# IMPORTANT: Keep description on ONE line for Claude Code compatibility
# prettier-ignore
description: Use when implementing Windows media player integration - SystemMediaTransportControls for media playback control on Windows
---

# Media WinRT Go

## Quick Start

```go
import "github.com/dece2183/media-winrt-go/windows/media"

// Get system media transport controls
controls, err := media.GetSystemMediaTransportControlsForCurrentView()
if err != nil {
    log.Fatal(err)
}

// Set playback status
controls.SetPlaybackStatus(media.MediaPlaybackStatusPlaying)
```

## Core Principles

- Windows Runtime: Uses COM interfaces for Windows media APIs
- System Integration: Integrates with Windows system media controls
- Async Operations: File operations are asynchronous by nature

## Common Patterns

### Media Control Integration

Initialize SystemMediaTransportControls and manage media state integration with Windows system UI.

## Reference Files

For detailed documentation, see:
- [references/usage-examples.md](references/usage-examples.md) - Complete integration examples
- [references/api-reference.md](references/api-reference.md) - Comprehensive API documentation
- [references/troubleshooting.md](references/troubleshooting.md) - Common issues and solutions
- [references/advanced-patterns.md](references/advanced-patterns.md) - Advanced integration patterns
- [references/com-internals.md](references/com-internals.md) - COM interface details and debugging

## Notes

- Windows-only (requires Windows 10+)
- Uses COM interfaces via ole.IUnknown
- Not considered stable (no tagged releases)

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
