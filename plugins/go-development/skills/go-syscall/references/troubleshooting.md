# Go Syscall Troubleshooting Guide

## Common Issues and Solutions

### 1. Handle Leaks

**Problem**: File descriptors, handles, or memory not being released properly.

**Symptoms**:
- "Too many open files" errors
- Memory usage increasing over time
- Process slowdown

**Solutions**:
```go
// Always use defer for cleanup
func safeFileOperation(filename string) error {
    fd, err := syscall.Open(filename, syscall.O_RDONLY, 0)
    if err != nil {
        return err
    }
    defer syscall.Close(fd) // Guaranteed cleanup

    // Use file descriptor
    return nil
}

// For memory-mapped files
func safeMemoryMap(filename string) error {
    fd, err := syscall.Open(filename, syscall.O_RDONLY, 0)
    if err != nil {
        return err
    }
    defer syscall.Close(fd)

    data, err := syscall.Mmap(fd, 0, 1024, syscall.PROT_READ, syscall.MAP_PRIVATE)
    if err != nil {
        return err
    }
    defer syscall.Munmap(data) // Always unmap

    return nil
}
```

### 2. Interrupted System Calls (EINTR)

**Problem**: System calls being interrupted by signals.

**Symptoms**:
- Operations failing intermittently
- EINTR errors appearing in logs

**Solutions**:
```go
// Retry wrapper for interruptible operations
func retryOnEINTR(fn func() error) error {
    for {
        err := fn()
        if err != syscall.EINTR {
            return err
        }
        // Call was interrupted, retry
    }
}

// Example usage
func safeRead(fd int, buf []byte) (int, error) {
    var n int
    var err error
    err = retryOnEINTR(func() error {
        var readErr error
        n, readErr = syscall.Read(fd, buf)
        return readErr
    })
    return n, err
}
```

### 3. Buffer Size Issues

**Problem**: Buffers too small for operations, leading to truncation or errors.

**Solutions**:
```go
// Use appropriate buffer sizes
const (
    DefaultReadBufferSize  = 64 * 1024  // 64KB
    DefaultWriteBufferSize = 64 * 1024  // 64KB
    PathBufferSize         = 4096       // For path operations
)

// Dynamic buffer sizing for Windows paths
func getWindowsPath(path string) ([]uint16, error) {
    // Use MAX_PATH + 1 for Windows paths
    buffer := make([]uint16, windows.MAX_PATH+1)
    return windows.UTF16FromString(path)
}
```

### 4. Unicode String Handling

**Problem**: Incorrect string encoding, especially on Windows.

**Symptoms**:
- Garbled text output
- File not found errors with valid paths
- Registry operations failing

**Solutions**:
```go
// Safe UTF-16 conversion
func safeUTF16Ptr(s string) (*uint16, error) {
    if len(s) == 0 {
        return nil, nil
    }
    return windows.UTF16PtrFromString(s)
}

// Convert back safely
func safeUTF16ToString(p []uint16) string {
    if len(p) == 0 {
        return ""
    }
    // Find null terminator
    for i, c := range p {
        if c == 0 {
            return windows.UTF16ToString(p[:i])
        }
    }
    return windows.UTF16ToString(p)
}
```

### 5. Permission Issues

**Problem**: Operations failing due to insufficient permissions.

**Solutions**:
```go
// Check permissions before operations
func checkFilePermissions(filename string) error {
    var stat syscall.Stat_t
    err := syscall.Stat(filename, &stat)
    if err != nil {
        if err == syscall.EACCES {
            return fmt.Errorf("permission denied: %s", filename)
        }
        return err
    }

    // Check read permissions
    if stat.Mode&0400 == 0 {
        return fmt.Errorf("no read permission: %s", filename)
    }

    return nil
}

// Use appropriate file permissions
func createFileWithPerms(filename string) error {
    fd, err := syscall.Open(filename, syscall.O_CREAT|syscall.O_WRONLY, 0644)
    if err != nil {
        return err
    }
    defer syscall.Close(fd)

    // File created with rw-r--r-- permissions
    return nil
}
```

## Platform-Specific Issues

### Linux/Unix Issues

#### 1. File Descriptor Limits
```go
// Check and handle file descriptor limits
func checkFdLimits() error {
    var rlimit syscall.Rlimit
    err := syscall.Getrlimit(syscall.RLIMIT_NOFILE, &rlimit)
    if err != nil {
        return err
    }

    fmt.Printf("File descriptor limit: %d (current), %d (max)\n", rlimit.Cur, rlimit.Max)

    if rlimit.Cur < 1024 {
        fmt.Println("Warning: Low file descriptor limit")
    }

    return nil
}
```

#### 2. Signal Handling
```go
// Proper signal handling for graceful shutdown
func setupSignalHandlers() {
    sigChan := make(chan os.Signal, 1)
    signal.Notify(sigChan, syscall.SIGINT, syscall.SIGTERM)

    go func() {
        sig := <-sigChan
        fmt.Printf("Received signal: %v\n", sig)
        cleanupAndExit()
    }()
}
```

### Windows Issues

#### 1. Registry Access
```go
// Check registry access rights
func checkRegistryAccess() error {
    var hKey windows.Handle
    err := windows.RegOpenKeyEx(
        windows.HKEY_LOCAL_MACHINE,
        windows.StringToUTF16Ptr("SOFTWARE"),
        0,
        windows.KEY_READ,
        &hKey,
    )
    if err != nil {
        if err == windows.ERROR_ACCESS_DENIED {
            fmt.Println("Run as administrator for registry access")
        }
        return err
    }
    windows.RegCloseKey(hKey)
    return nil
}
```

#### 2. DLL Loading Issues
```go
// Safe DLL loading with error checking
func loadDLL(name string) (*windows.LazyDLL, error) {
    dll := windows.NewLazyDLL(name)

    // Test if DLL loads
    if err := dll.Load(); err != nil {
        return nil, fmt.Errorf("failed to load %s: %v", name, err)
    }

    return &dll, nil
}
```

## Debugging Techniques

### 1. Logging System Calls
```go
// Enable detailed syscall logging
func logSyscall(operation string, err error) {
    if err != nil {
        if errno, ok := err.(syscall.Errno); ok {
            log.Printf("%s failed: errno=%d, error=%s", operation, errno, errno.Error())

            // Get system error message
            var msg [256]uint16
            windows.FormatMessage(
                windows.FORMAT_MESSAGE_FROM_SYSTEM|windows.FORMAT_MESSAGE_IGNORE_INSERTS,
                0,
                uint32(errno),
                0,
                &msg[0],
                256,
                nil,
            )
            systemError := windows.UTF16ToString(msg[:])
            log.Printf("System error: %s", systemError)
        } else {
            log.Printf("%s failed: %v", operation, err)
        }
    } else {
        log.Printf("%s succeeded", operation)
    }
}
```

### 2. Performance Monitoring
```go
// Measure syscall performance
func measureSyscallPerformance(operation string, fn func() error) error {
    start := time.Now()
    err := fn()
    duration := time.Since(start)

    log.Printf("%s took %v", operation, duration)
    if duration > time.Second {
        log.Printf("Warning: %s took unusually long", operation)
    }

    return err
}

// Usage
err := measureSyscallPerformance("file read", func() error {
    _, err := syscall.Read(fd, buf)
    return err
})
```

### 3. Resource Usage Tracking
```go
// Track file descriptor usage
type FdTracker struct {
    fds map[int]string // fd -> description
    mu  sync.Mutex
}

func NewFdTracker() *FdTracker {
    return &FdTracker{fds: make(map[int]string)}
}

func (t *FdTracker) Add(fd int, desc string) {
    t.mu.Lock()
    defer t.mu.Unlock()
    t.fds[fd] = desc
    log.Printf("Added fd %d: %s (total: %d)", fd, desc, len(t.fds))
}

func (t *FdTracker) Remove(fd int) {
    t.mu.Lock()
    defer t.mu.Unlock()
    if desc, exists := t.fds[fd]; exists {
        delete(t.fds, fd)
        log.Printf("Removed fd %d: %s (total: %d)", fd, desc, len(t.fds))
    }
}
```

## Testing Strategies

### 1. Mock Syscalls for Testing
```go
// Interface for testing
type FileOperations interface {
    Open(path string, mode int, perm uint32) (int, error)
    Close(fd int) error
    Read(fd int, buf []byte) (int, error)
    Write(fd int, buf []byte) (int, error)
}

// Real implementation
type RealFileOps struct{}

func (r *RealFileOps) Open(path string, mode int, perm uint32) (int, error) {
    return syscall.Open(path, mode, perm)
}

// Mock implementation for tests
type MockFileOps struct {
    Files map[string][]byte
}

func (m *MockFileOps) Open(path string, mode int, perm uint32) (int, error) {
    if _, exists := m.Files[path]; !exists {
        return -1, syscall.ENOENT
    }
    return 1, nil // Mock file descriptor
}
```

### 2. Error Injection Testing
```go
// Test error handling paths
func testErrorHandling(t *testing.T) {
    tests := []struct {
        name    string
        error   error
        wantErr string
    }{
        {"file not found", syscall.ENOENT, "file not found"},
        {"permission denied", syscall.EACCES, "permission denied"},
        {"bad file descriptor", syscall.EBADF, "bad file descriptor"},
    }

    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            err := handleSyscallError(tt.error)
            if err == nil {
                t.Fatal("expected error")
            }
            if !strings.Contains(err.Error(), tt.wantErr) {
                t.Errorf("error = %v, want %v", err, tt.wantErr)
            }
        })
    }
}
```

## Best Practices Checklist

### Before Using Syscalls
- [ ] Verify higher-level packages don't already provide the functionality
- [ ] Check if the operation is platform-specific and needs build tags
- [ ] Consider error handling requirements
- [ ] Plan for resource cleanup

### During Implementation
- [ ] Use `defer` for all cleanup operations
- [ ] Handle `EINTR` appropriately
- [ ] Use appropriate buffer sizes
- [ ] Convert strings correctly for the platform
- [ ] Check return values properly

### Testing and Validation
- [ ] Test error paths
- [ ] Verify resource cleanup
- [ ] Test on target platforms
- [ ] Monitor for handle/memory leaks
- [ ] Performance test critical paths