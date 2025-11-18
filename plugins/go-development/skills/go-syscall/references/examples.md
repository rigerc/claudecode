# Go Syscall Examples

## File Operations

### File Copy with Error Handling
```go
package main

import (
    "fmt"
    "syscall"
)

func copyFile(src, dst string) error {
    // Open source file
    srcFd, err := syscall.Open(src, syscall.O_RDONLY, 0)
    if err != nil {
        if err == syscall.ENOENT {
            return fmt.Errorf("source file not found: %s", src)
        }
        return fmt.Errorf("open source failed: %v", err)
    }
    defer syscall.Close(srcFd)

    // Create destination file
    dstFd, err := syscall.Open(dst, syscall.O_WRONLY|syscall.O_CREAT|syscall.O_TRUNC, 0644)
    if err != nil {
        return fmt.Errorf("create destination failed: %v", err)
    }
    defer syscall.Close(dstFd)

    // Copy data with buffering
    buf := make([]byte, 32*1024) // 32KB buffer
    for {
        n, err := syscall.Read(srcFd, buf)
        if err != nil {
            return fmt.Errorf("read failed: %v", err)
        }
        if n == 0 {
            break // EOF
        }

        if _, err := syscall.Write(dstFd, buf[:n]); err != nil {
            return fmt.Errorf("write failed: %v", err)
        }
    }

    return nil
}
```

### File Information and Permissions
```go
func getFileStats(filename string) (*syscall.Stat_t, error) {
    var stat syscall.Stat_t
    err := syscall.Stat(filename, &stat)
    if err != nil {
        if err == syscall.ENOENT {
            return nil, fmt.Errorf("file does not exist: %s", filename)
        }
        return nil, fmt.Errorf("stat failed: %v", err)
    }
    return &stat, nil
}

func setFilePermissions(filename string, mode uint32) error {
    err := syscall.Chmod(filename, mode)
    if err != nil {
        return fmt.Errorf("chmod failed: %v", err)
    }
    return nil
}
```

## Process Management

### Process Creation and Monitoring
```go
package main

import (
    "fmt"
    "os"
    "syscall"
    "time"
)

func startCommand(command string, args []string) (int, error) {
    // Set up process attributes
    attr := &syscall.ProcAttr{
        Files: []uintptr{0, 1, 2}, // stdin, stdout, stderr
        Env:   os.Environ(),
        Sys:   &syscall.SysProcAttr{},
    }

    // Start process
    pid, err := syscall.ForkExec(command, args, attr)
    if err != nil {
        return 0, fmt.Errorf("fork/exec failed: %v", err)
    }

    return pid, nil
}

func waitForProcess(pid int) error {
    for {
        var status syscall.WaitStatus
        wpid, err := syscall.Wait4(pid, &status, 0, nil)
        if err != nil {
            return fmt.Errorf("wait4 failed: %v", err)
        }

        if wpid == pid {
            if status.Exited() {
                fmt.Printf("Process %d exited with status: %d\n", pid, status.ExitStatus())
                return nil
            }
            if status.Signaled() {
                fmt.Printf("Process %d killed by signal: %d\n", pid, status.Signal())
                return nil
            }
            break
        }
        time.Sleep(100 * time.Millisecond)
    }
    return nil
}
```

### Process Signal Handling
```go
func signalProcess(pid int, sig syscall.Signal) error {
    err := syscall.Kill(pid, sig)
    if err != nil {
        if err == syscall.ESRCH {
            return fmt.Errorf("process %d does not exist", pid)
        }
        return fmt.Errorf("kill failed: %v", err)
    }
    return nil
}

func gracefulShutdown(pid int) error {
    // Send SIGTERM first
    err := signalProcess(pid, syscall.SIGTERM)
    if err != nil {
        return err
    }

    // Wait a bit
    time.Sleep(5 * time.Second)

    // Check if process still exists
    err = syscall.Kill(pid, 0) // Signal 0 doesn't kill, just checks
    if err == nil {
        // Process still exists, send SIGKILL
        fmt.Printf("Process %d still running, sending SIGKILL\n", pid)
        return signalProcess(pid, syscall.SIGKILL)
    }

    return nil
}
```

## Network Operations

### TCP Server Using Syscalls
```go
package main

import (
    "fmt"
    "syscall"
)

func startTCPServer(port int) error {
    // Create socket
    fd, err := syscall.Socket(syscall.AF_INET, syscall.SOCK_STREAM, 0)
    if err != nil {
        return fmt.Errorf("socket creation failed: %v", err)
    }
    defer syscall.Close(fd)

    // Set SO_REUSEADDR
    if err := syscall.SetsockoptInt(fd, syscall.SOL_SOCKET, syscall.SO_REUSEADDR, 1); err != nil {
        return fmt.Errorf("setsockopt failed: %v", err)
    }

    // Bind to port
    addr := &syscall.SockaddrInet4{Port: port}
    if err := syscall.Bind(fd, addr); err != nil {
        return fmt.Errorf("bind failed: %v", err)
    }

    // Listen
    if err := syscall.Listen(fd, 10); err != nil {
        return fmt.Errorf("listen failed: %v", err)
    }

    fmt.Printf("Server listening on port %d\n", port)

    for {
        // Accept connection
        connFd, clientAddr, err := syscall.Accept(fd)
        if err != nil {
            fmt.Printf("accept failed: %v\n", err)
            continue
        }

        // Handle connection
        go handleConnection(connFd, clientAddr)
    }
}

func handleConnection(fd int, addr syscall.Sockaddr) {
    defer syscall.Close(fd)

    // Send welcome message
    welcome := []byte("Hello from syscall server!\n")
    if _, err := syscall.Write(fd, welcome); err != nil {
        fmt.Printf("write failed: %v\n", err)
        return
    }

    // Echo server loop
    buf := make([]byte, 1024)
    for {
        n, err := syscall.Read(fd, buf)
        if err != nil || n == 0 {
            break
        }

        // Echo back the data
        if _, err := syscall.Write(fd, buf[:n]); err != nil {
            fmt.Printf("echo write failed: %v\n", err)
            break
        }
    }

    fmt.Println("Client disconnected")
}
```

## Memory Management

### Memory Mapping Example
```go
package main

import (
    "fmt"
    "syscall"
    "unsafe"
)

func memoryMapExample(filename string) error {
    // Open file
    fd, err := syscall.Open(filename, syscall.O_RDWR, 0)
    if err != nil {
        return fmt.Errorf("open failed: %v", err)
    }
    defer syscall.Close(fd)

    // Get file size
    fileInfo, err := syscall.Stat(filename, &syscall.Stat_t{})
    if err != nil {
        return fmt.Errorf("stat failed: %v", err)
    }
    size := fileInfo.Size

    // Map file into memory
    data, err := syscall.Mmap(fd, 0, int(size), syscall.PROT_READ|syscall.PROT_WRITE, syscall.MAP_SHARED)
    if err != nil {
        return fmt.Errorf("mmap failed: %v", err)
    }
    defer syscall.Munmap(data)

    // Use memory-mapped data
    fmt.Printf("File mapped at address: %p\n", &data[0])
    fmt.Printf("First 16 bytes: %x\n", data[:min(16, len(data))])

    // Modify data (will be reflected in file)
    if len(data) >= 4 {
        copy(data[:4], []byte("MODIFIED"))
    }

    return nil
}

func min(a, b int) int {
    if a < b {
        return a
    }
    return b
}
```

## Windows-Specific Examples

### Windows File Operations
```go
package main

import (
    "fmt"
    "golang.org/x/sys/windows"
    "unicode/utf16"
)

func createWindowsFile(filename string) error {
    // Convert to UTF-16
    filename16, err := windows.UTF16PtrFromString(filename)
    if err != nil {
        return fmt.Errorf("UTF16 conversion failed: %v", err)
    }

    // Create file
    handle, err := windows.CreateFile(
        filename16,
        windows.GENERIC_READ|windows.GENERIC_WRITE,
        windows.FILE_SHARE_READ,
        nil,
        windows.CREATE_ALWAYS,
        windows.FILE_ATTRIBUTE_NORMAL,
        0,
    )
    if err != nil {
        return fmt.Errorf("CreateFile failed: %v", err)
    }
    defer windows.CloseHandle(handle)

    // Write data
    data := []byte("Hello, Windows!")
    var bytesWritten uint32
    err = windows.WriteFile(handle, data, &bytesWritten, nil)
    if err != nil {
        return fmt.Errorf("WriteFile failed: %v", err)
    }

    fmt.Printf("Written %d bytes to %s\n", bytesWritten, filename)
    return nil
}
```

### Windows Registry Operations
```go
func readWindowsRegistry(keyPath, valueName string) (string, error) {
    // Open registry key
    var hKey windows.Handle
    pathUTF16, err := windows.UTF16PtrFromString(keyPath)
    if err != nil {
        return "", err
    }

    err = windows.RegOpenKeyEx(
        windows.HKEY_LOCAL_MACHINE,
        pathUTF16,
        0,
        windows.KEY_READ,
        &hKey,
    )
    if err != nil {
        return "", fmt.Errorf("RegOpenKeyEx failed: %v", err)
    }
    defer windows.RegCloseKey(hKey)

    // Query value size
    var valueType uint32
    var dataSize uint32
    valueUTF16, err := windows.UTF16PtrFromString(valueName)
    if err != nil {
        return "", err
    }

    err = windows.RegQueryValueEx(
        hKey,
        valueUTF16,
        nil,
        &valueType,
        nil,
        &dataSize,
    )
    if err != nil {
        return "", fmt.Errorf("RegQueryValueEx (size) failed: %v", err)
    }

    // Read value data
    buffer := make([]byte, dataSize)
    err = windows.RegQueryValueEx(
        hKey,
        valueUTF16,
        nil,
        &valueType,
        &buffer[0],
        &dataSize,
    )
    if err != nil {
        return "", fmt.Errorf("RegQueryValueEx (data) failed: %v", err)
    }

    // Convert UTF-16 to string
    if valueType == windows.REG_SZ {
        utf16Str := (*[1 << 20]uint16)(unsafe.Pointer(&buffer[0]))[:dataSize/2]
        return windows.UTF16ToString(utf16Str), nil
    }

    return string(buffer), nil
}
```

## Error Handling Patterns

### Robust Error Handling
```go
type SyscallError struct {
    Operation string
    Path      string
    Errno     syscall.Errno
}

func (e *SyscallError) Error() string {
    return fmt.Sprintf("%s failed for %s: %v", e.Operation, e.Path, e.Errno)
}

func robustFileOperation(filename string) error {
    fd, err := syscall.Open(filename, syscall.O_RDONLY, 0)
    if err != nil {
        if errno, ok := err.(syscall.Errno); ok {
            return &SyscallError{
                Operation: "Open",
                Path:      filename,
                Errno:     errno,
            }
        }
        return err
    }
    defer syscall.Close(fd)

    // Continue with file operations...
    return nil
}

// Handle interrupted syscalls
func retryOnEINTR(fn func() error) error {
    for {
        err := fn()
        if err != syscall.EINTR {
            return err
        }
        // System call was interrupted, retry
    }
}
```