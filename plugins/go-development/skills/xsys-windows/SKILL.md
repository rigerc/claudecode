---
name: xsys-windows
# IMPORTANT: Keep description on ONE line for Claude Code compatibility
# prettier-ignore
description: Use when working with Windows system programming, Windows APIs, and Windows-specific functionality using golang.org/x/sys/windows package
---

# Xsys Windows

## Quick Start

Basic Windows file operations using golang.org/x/sys/windows:

```go
package main
import ("fmt"; "golang.org/x/sys/windows")
func main() {
    filename, _ := windows.UTF16PtrFromString("test.txt")
    handle, err := windows.CreateFile(filename, windows.GENERIC_WRITE,
        0, nil, windows.CREATE_ALWAYS, windows.FILE_ATTRIBUTE_NORMAL, 0)
    if err != nil { fmt.Printf("Error: %v\n", err); return }
    defer windows.CloseHandle(handle)
    data := []byte("Hello Windows!")
    var written uint32
    windows.WriteFile(handle, data, &written, nil)
}
```

## Core Principles

- **Handle Management**: Always close Windows handles with `defer windows.CloseHandle()`
- **UTF-16 Strings**: Convert strings to UTF-16 for Windows API calls
- **Error Handling**: Check `windows.Errno` for Windows-specific errors
- **Security**: Use proper security descriptors and access control

## Common Patterns

File operations: `CreateFile`, `ReadFile`, `WriteFile`, `CloseHandle`.
Registry access: `RegOpenKeyEx`, `RegQueryValueEx`, `RegCloseKey`.
Process management: `CreateProcess`, `OpenProcess`, `TerminateProcess`.

## Reference Files

- [references/windows-api.md](references/windows-api.md) - Complete Windows API reference
- [references/examples.md](references/examples.md) - Windows-specific examples
- [references/troubleshooting.md](references/troubleshooting.md) - Common Windows issues

## Notes

Use UTF-16 string conversions for Windows APIs. Handle Windows-specific error codes. Use `golang.org/x/sys/windows` for enhanced Windows functionality.

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
