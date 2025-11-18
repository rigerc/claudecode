# Go Syscall Package: Complete Guide and Reference

## Overview

The `syscall` package provides Go's interface to low-level operating system primitives. It serves as the foundation for system-level operations in Go, offering direct access to underlying operating system calls. The package contains platform-specific functionality with details varying based on the operating system.

**Key Purpose**: Package syscall contains an interface to low-level operating system primitives. Its primary use is inside other packages that provide a more portable interface to the system, such as "os", "time", and "net".

## Quick Start

```go
package main

import (
    "fmt"
    "syscall"
)

func main() {
    // File operations
    fd, err := syscall.Open("example.txt", syscall.O_CREAT|syscall.O_WRONLY, 0644)
    if err != nil {
        fmt.Printf("Error opening file: %v\n", err)
        return
    }
    defer syscall.Close(fd)

    // Write to file
    data := []byte("Hello, syscall!")
    _, err = syscall.Write(fd, data)
    if err != nil {
        fmt.Printf("Error writing: %v\n", err)
        return
    }

    fmt.Println("File operations completed successfully")
}
```

## Core Components

### 1. System Call Functions

The package provides two main approaches for system calls:

#### Syscall Function
```go
func Syscall(trap, a1, a2, a3 uintptr) (r1, r2 uintptr, err Errno)
func Syscall6(trap, a1, a2, a3, a4, a5, a6 uintptr) (r1, r2 uintptr, err Errno)
```

#### RawSyscall Function
```go
func RawSyscall(trap, a1, a2, a3 uintptr) (r1, r2 uintptr, err Errno)
func RawSyscall6(trap, a1, a2, a3, a4, a5, a6 uintptr) (r1, r2 uintptr, err Errno)
```

**Difference**: `Syscall` can be interrupted by signals and automatically retries, while `RawSyscall` returns directly without signal handling.

### 2. File Operations

#### File Descriptors
```go
// Open file with flags and permissions
fd, err := syscall.Open("file.txt", syscall.O_RDONLY, 0)

// Read from file descriptor
buf := make([]byte, 1024)
n, err := syscall.Read(fd, buf)

// Write to file descriptor
data := []byte("Hello, World!")
n, err := syscall.Write(fd, data)

// Close file descriptor
err = syscall.Close(fd)

// Seek in file
offset, err := syscall.Seek(fd, 0, syscall.SEEK_SET)
```

#### File Flags
```go
// Common open flags
const (
    O_RDONLY int = syscall.O_RDONLY  // Read-only
    O_WRONLY int = syscall.O_WRONLY  // Write-only
    O_RDWR   int = syscall.O_RDWR    // Read-write
    O_CREAT  int = syscall.O_CREAT   // Create if not exists
    O_APPEND int = syscall.O_APPEND  // Append to file
    O_TRUNC  int = syscall.O_TRUNC   // Truncate file
)
```

### 3. Process Management

#### Process Creation
```go
// Fork and execute new process
pid, err := syscall.ForkExec("/bin/ls", []string{"ls"}, &syscall.ProcAttr{
    Files: []uintptr{0, 1, 2}, // stdin, stdout, stderr
    Env:  []string{"PATH=/usr/bin"},
})

// Start new process
attr := &syscall.ProcAttr{
    Files: []uintptr{0, 1, 2},
    Env:   os.Environ(),
}
pid, err := syscall.StartProcess("/bin/echo", []string{"echo", "hello"}, attr)

// Wait for process
var status syscall.WaitStatus
_, err := syscall.Wait4(pid, &status, 0, nil)
```

#### Process Signals
```go
// Send signal to process
err := syscall.Kill(pid, syscall.SIGTERM)

// Signal handling
signal := make(chan os.Signal, 1)
signal.Notify(signal, syscall.SIGINT, syscall.SIGTERM)
```

### 4. Network Operations

#### Socket Programming
```go
// Create socket
fd, err := syscall.Socket(syscall.AF_INET, syscall.SOCK_STREAM, 0)

// Bind to address
addr := &syscall.SockaddrInet4{Port: 8080}
copy(addr.Addr[:], net.ParseIP("127.0.0.1").To4())
err = syscall.Bind(fd, addr)

// Listen for connections
err = syscall.Listen(fd, 10)

// Accept connection
nfd, sa, err := syscall.Accept(fd)
defer syscall.Close(nfd)

// Connect to remote
remoteAddr := &syscall.SockaddrInet4{Port: 80, Addr: [4]byte{127, 0, 0, 1}}
err = syscall.Connect(fd, remoteAddr)
```

### 5. File System Operations

#### File Information
```go
// Get file status
var stat syscall.Stat_t
err := syscall.Stat("file.txt", &stat)

// File size
size := stat.Size

// File permissions
mode := stat.Mode

// File modification time
mtime := stat.Mtim

// Link operations
err := syscall.Symlink("target.txt", "link.txt")
err = syscall.Readlink("link.txt", buf)
```

#### Directory Operations
```go
// Create directory
err := syscall.Mkdir("newdir", 0755)

// Remove directory
err := syscall.Rmdir("newdir")

// Change permissions
err := syscall.Chmod("file.txt", 0644)

// Change owner
err = syscall.Chown("file.txt", uid, gid)
```

### 6. Memory Management

#### Memory Mapping
```go
// Map file into memory
fd, _ := syscall.Open("data.bin", syscall.O_RDWR, 0)
defer syscall.Close(fd)

data, err := syscall.Mmap(fd, 0, 1024, syscall.PROT_READ|syscall.PROT_WRITE, syscall.MAP_SHARED)
if err != nil {
    fmt.Printf("Mmap error: %v\n", err)
    return
}
defer syscall.Munmap(data)

// Use memory-mapped data
fmt.Printf("First byte: %d\n", data[0])
```

## Platform-Specific Considerations

### Unix/Linux Systems
```go
// Unix-specific syscalls
var rlimit syscall.Rlimit
err := syscall.Getrlimit(syscall.RLIMIT_NOFILE, &rlimit)

// Set resource limits
rlimit.Cur = 1000
rlimit.Max = 1000
err = syscall.Setrlimit(syscall.RLIMIT_NOFILE, &rlimit)

// Umask
oldMask := syscall.Umask(0022)
syscall.Umask(oldMask)
```

### Windows Systems
```go
// Windows-specific handle operations
handle, err := syscall.CreateFile(
    nil,
    syscall.GENERIC_READ,
    syscall.FILE_SHARE_READ,
    nil,
    syscall.OPEN_EXISTING,
    syscall.FILE_ATTRIBUTE_NORMAL,
    0,
)

// Windows registry operations (via syscall)
key, _, err := syscall.ModRegOpenKey(syscall.HKEY_LOCAL_MACHINE, "Software\\MyApp", syscall.KEY_READ)
```

## Error Handling

### Errno Type
```go
// Check for specific errors
fd, err := syscall.Open("nonexistent.txt", syscall.O_RDONLY, 0)
if err == syscall.ENOENT {
    fmt.Println("File does not exist")
} else if err == syscall.EACCES {
    fmt.Println("Permission denied")
} else if err != nil {
    fmt.Printf("Error: %v\n", err)
}
```

### Common Error Codes
```go
const (
    ENOENT Errno = syscall.ENOENT  // No such file or directory
    EACCES Errno = syscall.EACCES  // Permission denied
    EEXIST Errno = syscall.EEXIST  // File exists
    ENOTDIR Errno = syscall.ENOTDIR  // Not a directory
    EISDIR Errno = syscall.EISDIR    // Is a directory
    EPIPE  Errno = syscall.EPIPE     // Broken pipe
    EAGAIN Errno = syscall.EAGAIN    // Resource temporarily unavailable
)
```

## Advanced Examples

### Example 1: File Copy Using Syscalls

```go
func copyFile(src, dst string) error {
    // Open source file
    srcFd, err := syscall.Open(src, syscall.O_RDONLY, 0)
    if err != nil {
        return fmt.Errorf("open source: %v", err)
    }
    defer syscall.Close(srcFd)

    // Create destination file
    dstFd, err := syscall.Open(dst, syscall.O_WRONLY|syscall.O_CREAT|syscall.O_TRUNC, 0644)
    if err != nil {
        return fmt.Errorf("create destination: %v", err)
    }
    defer syscall.Close(dstFd)

    // Copy data
    buf := make([]byte, 32*1024) // 32KB buffer
    for {
        n, err := syscall.Read(srcFd, buf)
        if err != nil {
            return fmt.Errorf("read error: %v", err)
        }
        if n == 0 {
            break // EOF
        }

        if _, err := syscall.Write(dstFd, buf[:n]); err != nil {
            return fmt.Errorf("write error: %v", err)
        }
    }

    return nil
}
```

### Example 2: Simple TCP Server

```go
func simpleTCPServer(port int) error {
    // Create socket
    fd, err := syscall.Socket(syscall.AF_INET, syscall.SOCK_STREAM, 0)
    if err != nil {
        return fmt.Errorf("socket: %v", err)
    }
    defer syscall.Close(fd)

    // Set SO_REUSEADDR
    syscall.SetsockoptInt(fd, syscall.SOL_SOCKET, syscall.SO_REUSEADDR, 1)

    // Bind to port
    addr := &syscall.SockaddrInet4{Port: port}
    if err := syscall.Bind(fd, addr); err != nil {
        return fmt.Errorf("bind: %v", err)
    }

    // Listen
    if err := syscall.Listen(fd, 10); err != nil {
        return fmt.Errorf("listen: %v", err)
    }

    fmt.Printf("Server listening on port %d\n", port)

    for {
        // Accept connection
        connFd, sa, err := syscall.Accept(fd)
        if err != nil {
            fmt.Printf("accept error: %v\n", err)
            continue
        }

        // Handle connection
        go handleConnection(connFd, sa)
    }
}

func handleConnection(fd int, sa syscall.Sockaddr) {
    defer syscall.Close(fd)

    // Send welcome message
    welcome := []byte("Hello from syscall server!\n")
    syscall.Write(fd, welcome)

    // Simple echo server
    buf := make([]byte, 1024)
    for {
        n, err := syscall.Read(fd, buf)
        if err != nil || n == 0 {
            break
        }
        syscall.Write(fd, buf[:n])
    }
}
```

### Example 3: Process Monitoring

```go
func monitorProcess(pid int) error {
    for {
        var status syscall.WaitStatus
        _, err := syscall.Wait4(pid, &status, syscall.WNOHANG, nil)

        if err != nil {
            return fmt.Errorf("wait4: %v", err)
        }

        if status.Exited() {
            fmt.Printf("Process %d exited with status: %d\n", pid, status.ExitStatus())
            return nil
        }

        if status.Signaled() {
            fmt.Printf("Process %d killed by signal: %d\n", pid, status.Signal())
            return nil
        }

        if status.Stopped() {
            fmt.Printf("Process %d stopped by signal: %d\n", pid, status.StopSignal())
        }

        time.Sleep(100 * time.Millisecond)
    }
}
```

## Best Practices

### 1. Error Handling
```go
// Always check error returns
fd, err := syscall.Open("file.txt", syscall.O_RDONLY, 0)
if err != nil {
    // Handle specific errors
    if err == syscall.ENOENT {
        return fmt.Errorf("file not found")
    }
    return fmt.Errorf("open failed: %v", err)
}
defer syscall.Close(fd)
```

### 2. Resource Management
```go
// Always close file descriptors
fd, err := syscall.Open("file.txt", syscall.O_RDONLY, 0)
if err != nil {
    return err
}
defer syscall.Close(fd) // Ensure cleanup

// Always unmap memory
data, err := syscall.Mmap(fd, 0, size, syscall.PROT_READ, syscall.MAP_PRIVATE)
if err != nil {
    return err
}
defer syscall.Munmap(data)
```

### 3. Platform Compatibility
```go
// Use build constraints for platform-specific code
//go:build linux
func linuxSpecificOperation() error {
    return syscall.IoctlSetInt(fd, request, value)
}

//go:build windows
func windowsSpecificOperation() error {
    return windows.DeviceIoControl(handle, ioControlCode, nil, 0)
}
```

### 4. Performance Considerations
```go
// Use buffered operations for better performance
buf := make([]byte, 64*1024) // 64KB buffer
n, err := syscall.Read(fd, buf)

// Use RawSyscall for non-interruptible operations
r1, r2, err := syscall.RawSyscall(syscall.SYS_READ, uintptr(fd), uintptr(unsafe.Pointer(&buf[0])), uintptr(len(buf)))
```

## When to Use syscall vs Higher-Level Packages

### Use syscall for:
- **Performance-critical code** requiring direct system access
- **Specialized operations** not available in standard libraries
- **Low-level utilities** and system tools
- **Platform-specific features** requiring fine control

### Use higher-level packages for:
- **File I/O**: Use `os` package instead of direct file syscalls
- **Network programming**: Use `net` package instead of socket syscalls
- **Process management**: Use `os/exec` for process execution
- **General applications**: Most applications should use higher-level abstractions

## Integration with golang.org/x/sys

The `golang.org/x/sys` package provides enhanced system call support and is the recommended alternative for many use cases:

```go
// Preferred for newer code
import "golang.org/x/sys/unix"

// Instead of
import "syscall"

// Example: Enhanced socket operations
fd, err := unix.Socket(unix.AF_INET, unix.SOCK_STREAM|unix.SOCK_NONBLOCK, 0)
```

**Benefits of golang.org/x/sys:**
- More comprehensive system call coverage
- Better platform support
- Regular updates
- Modern Go idioms

## Common Pitfalls and Gotchas

### 1. Signal Handling
```go
// Syscall functions can be interrupted by signals
// Use proper error handling for EINTR
for {
    n, err := syscall.Read(fd, buf)
    if err == syscall.EINTR {
        continue // Retry on interrupt
    }
    if err != nil {
        return err
    }
    break
}
```

### 2. Thread Safety
```go
// Many syscalls are not thread-safe
// Use proper synchronization in concurrent code
var mu sync.Mutex

func safeSyscall() {
    mu.Lock()
    defer mu.Unlock()
    syscall.SomeGlobalStateOperation()
}
```

### 3. Memory Management
```go
// Be careful with memory pointers in syscalls
// Always use proper types and checks
data := []byte("hello")
ptr := uintptr(unsafe.Pointer(&data[0]))
defer runtime.KeepAlive(data) // Prevent GC
```

## Debugging and Troubleshooting

### 1. Using Strace/Ltrace
```bash
# Trace system calls
strace -f -o trace.log ./yourprogram

# Trace library calls
ltrace -f -o ltrace.log ./yourprogram
```

### 2. Error Investigation
```go
// Get detailed error information
if err != nil {
    fmt.Printf("Error: %v\n", err)
    fmt.Printf("Error type: %T\n", err)

    if errno, ok := err.(syscall.Errno); ok {
        fmt.Printf("Errno value: %d\n", errno)
        fmt.Printf("Errno string: %s\n", errno.Error())
    }
}
```

### 3. Resource Leaks
```go
// Monitor file descriptor usage
func checkFdUsage() {
    var rlimit syscall.Rlimit
    syscall.Getrlimit(syscall.RLIMIT_NOFILE, &rlimit)
    fmt.Printf("File descriptor limit: %d\n", rlimit.Cur)
}
```

## References and Resources

### Official Documentation
- [pkg.go.dev/syscall](https://pkg.go.dev/syscall) - Official package documentation
- [golang.org/x/sys](https://pkg.go.dev/golang.org/x/sys) - Enhanced system package
- [Go syscall source](https://cs.opensource.google/go/go/+/refs/tags/go1.21.5:src/syscall/) - Source code

### Related Tools
- `strace` - Linux system call tracer
- `ltrace` - Library call tracer
- `dtrace` - System tracing (macOS/BSD)
- `procmon` - Process monitoring (Windows)

### Books and Articles
- "The Go Programming Language" - Chapter on Systems Programming
- "Linux System Programming" - Comprehensive system call reference
- "Windows System Programming" - Windows-specific system calls

## Conclusion

The `syscall` package provides powerful low-level access to operating system primitives, making it essential for:

- **System programming** and utilities
- **Performance-critical applications** requiring fine control
- **Platform-specific functionality** not available elsewhere
- **Educational purposes** for understanding system interactions

While powerful, syscall programming requires careful attention to:
- **Error handling** and edge cases
- **Resource management** and cleanup
- **Platform differences** and compatibility
- **Security considerations** with direct system access

For most applications, prefer higher-level packages like `os`, `net`, and `exec`. Use `syscall` only when you need specific low-level functionality not available elsewhere, and consider `golang.org/x/sys` for enhanced system call support.