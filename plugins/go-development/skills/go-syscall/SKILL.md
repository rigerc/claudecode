---
name: go-syscall
# IMPORTANT: Keep description on ONE line for Claude Code compatibility
# prettier-ignore
description: Use when working with Go syscalls, low-level system programming, and Windows APIs using syscall and golang.org/x/sys packages
---

# Go Syscall

Basic file operations using syscalls:

```go
package main
import ("fmt"; "syscall")
func main() {
    fd, err := syscall.Open("example.txt", syscall.O_CREAT|syscall.O_WRONLY, 0644)
    if err != nil { fmt.Printf("Error: %v\n", err); return }
    defer syscall.Close(fd)
    data := []byte("Hello, syscall!")
    _, err = syscall.Write(fd, data)
    if err != nil { fmt.Printf("Write error: %v\n", err) }
}
```

## Core Principles

- **Resource Management**: Always close handles with `defer`
- **Error Handling**: Check syscall returns, use `Errno` for system errors
- **Platform Specificity**: Use build tags for platform-specific code
- **Performance**: Prefer `RawSyscall` for non-interruptible operations

## Common Patterns

File I/O: `Open`, `Read`, `Write`, `Close`. Check `ENOENT` and `EACCES` errors.
Process operations: `ForkExec`, `StartProcess`, `Wait4`. Handle `EINTR` appropriately.

## Reference Files

- [references/api-reference.md](references/api-reference.md) - Complete API reference
- [references/examples.md](references/examples.md) - Practical examples
- [references/troubleshooting.md](references/troubleshooting.md) - Common issues

Prefer higher-level packages (`os`, `net`) over direct syscalls. Use `golang.org/x/sys/windows` for Windows APIs.