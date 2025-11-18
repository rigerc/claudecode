# Go Syscall API Reference

## Core Syscall Functions

### System Call Functions
```go
// Standard system call (can be interrupted by signals)
func Syscall(trap, a1, a2, a3 uintptr) (r1, r2 uintptr, err Errno)

// System call with 6 arguments
func Syscall6(trap, a1, a2, a3, a4, a5, a6 uintptr) (r1, r2 uintptr, err Errno)

// Raw system call (non-interruptible)
func RawSyscall(trap, a1, a2, a3 uintptr) (r1, r2 uintptr, err Errno)

// Raw system call with 6 arguments
func RawSyscall6(trap, a1, a2, a3, a4, a5, a6 uintptr) (r1, r2 uintptr, err Errno)
```

### File Operations
```go
// File descriptor operations
func Open(path string, mode int, perm uint32) (fd int, err error)
func Close(fd int) (err error)
func Read(fd int, p []byte) (n int, err error)
func Write(fd int, p []byte) (n int, err error)
func Seek(fd int, offset int64, whence int) (off int64, err error)

// File flags
const (
    O_RDONLY int = syscall.O_RDONLY
    O_WRONLY int = syscall.O_WRONLY
    O_RDWR   int = syscall.O_RDWR
    O_CREAT  int = syscall.O_CREAT
    O_APPEND int = syscall.O_APPEND
    O_TRUNC  int = syscall.O_TRUNC
)
```

### Process Management
```go
// Process creation and management
func ForkExec(argv0 string, argv []string, attr *ProcAttr) (pid int, err error)
func StartProcess(argv0 string, argv []string, attr *ProcAttr) (handle int, err error)
func Wait4(pid int, status *WaitStatus, options int, rusage *Rusage) (wpid int, err error)

// Process attributes
type ProcAttr struct {
    Dir   string    // Current working directory
    Env   []string  // Environment variables
    Files []uintptr // File descriptors
    Sys   *SysProcAttr // System-specific attributes
}

// Signal handling
func Kill(pid int, sig Signal) (err error)
func Getpid() (pid int)
func Getppid() (ppid int)
```

### Network Operations
```go
// Socket operations
func Socket(domain, typ, proto int) (fd, err error)
func Bind(fd int, sa Sockaddr) (err error)
func Connect(fd int, sa Sockaddr) (err error)
func Listen(fd int, n int) (err error)
func Accept(fd int) (nfd int, sa Sockaddr, err error)

// Socket types
const (
    AF_INET   = syscall.AF_INET
    AF_INET6  = syscall.AF_INET6
    AF_UNIX   = syscall.AF_UNIX
    SOCK_STREAM = syscall.SOCK_STREAM
    SOCK_DGRAM  = syscall.SOCK_DGRAM
)
```

### Memory Management
```go
// Memory mapping
func Mmap(fd int, offset int64, length int, prot int, flags int) (data []byte, err error)
func Munmap(b []byte) (err error)

// Memory protection
func Mprotect(b []byte, prot int) (err error)

// Memory allocation
func VirtualAlloc(address uintptr, size uintptr, alloctype uint32, protect uint32) (uintptr, error)
func VirtualFree(address uintptr, size uintptr, freetype uint32) error
```

## Error Handling

### Common Error Codes
```go
// Standard error codes
const (
    ENOENT Errno = syscall.ENOENT  // No such file or directory
    EACCES Errno = syscall.EACCES  // Permission denied
    EEXIST Errno = syscall.EEXIST  // File exists
    ENOTDIR Errno = syscall.ENOTDIR  // Not a directory
    EISDIR Errno = syscall.EISDIR    // Is a directory
    EAGAIN Errno = syscall.EAGAIN    // Resource temporarily unavailable
    EINTR  Errno = syscall.EINTR     // Interrupted system call
)

// Error handling pattern
if err != nil {
    if errno, ok := err.(syscall.Errno); ok {
        switch errno {
        case syscall.ENOENT:
            // Handle file not found
        case syscall.EACCES:
            // Handle permission denied
        default:
            // Handle other errors
        }
    }
}
```

## Windows-Specific APIs (golang.org/x/sys/windows)

### Windows Handles and Types
```go
type Handle uintptr

// Common Windows functions
func CloseHandle(handle Handle) (err error)
func CreateFile(name *uint16, access uint32, share uint32, sa *SecurityAttributes,
    createmode uint32, attrs uint32, templatefile Handle) (handle Handle, err error)
func ReadFile(handle Handle, buf []byte, done *uint32, overlapped *Overlapped) error
func WriteFile(handle Handle, buf []byte, done *uint32, overlapped *Overlapped) error
```

### Windows Registry Operations
```go
func RegOpenKeyEx(key Handle, subkey *uint16, options uint32, desiredAccess uint32, result *Handle) (regerrno error)
func RegQueryValueEx(key Handle, valueName *uint16, reserved *uint32, valtype *uint32, buf *byte, buflen *uint32) (regerrno error)
func RegCloseKey(key Handle) (regerrno error)

// Registry constants
const (
    HKEY_LOCAL_MACHINE Handle = 0x80000002
    HKEY_CURRENT_USER  Handle = 0x80000001
    KEY_READ           uint32 = 0x20019
    KEY_WRITE          uint32 = 0x20006
)
```

### Windows Process Management
```go
type ProcessInformation struct {
    Process   Handle
    Thread    Handle
    ProcessId uint32
    ThreadId  uint32
}

func CreateProcess(appName *uint16, commandLine *uint16, procSecurity *SecurityAttributes,
    threadSecurity *SecurityAttributes, inheritHandles bool, creationFlags uint32,
    env *uint16, currentDir *uint16, startupInfo *StartupInfo,
    outProcInfo *ProcessInformation) (err error)
```

## Platform-Specific Considerations

### Build Tags for Cross-Platform Code
```go
//go:build linux
func linuxSpecificOperation() error {
    return syscall.IoctlSetInt(fd, request, value)
}

//go:build windows
func windowsSpecificOperation() error {
    return windows.DeviceIoControl(handle, ioControlCode, nil, 0)
}

//go:build darwin
func macOSSpecificOperation() error {
    return syscall.Syscall(syscall.SYS_GETDIRENTRIES64, ...)
}
```

### File System Differences
```go
// Platform-specific file flags
const (
    // Unix-specific
    O_NONBLOCK = syscall.O_NONBLOCK
    O_CLOEXEC  = syscall.O_CLOEXEC

    // Windows-specific
    FILE_FLAG_OVERLAPPED     = 0x40000000
    FILE_FLAG_SEQUENTIAL_SCAN = 0x08000000
)
```

## Performance Considerations

### Buffer Sizes for I/O Operations
```go
// Optimal buffer sizes for different operations
const (
    OptimalReadBufferSize  = 64 * 1024  // 64KB for file reads
    OptimalWriteBufferSize = 64 * 1024  // 64KB for file writes
    SocketBufferSize       = 8 * 1024   // 8KB for socket operations
)
```

### Minimizing System Calls
```go
// Batch operations to reduce syscall overhead
func efficientFileWrite(fd int, data [][]byte) error {
    // Combine small writes
    buffer := make([]byte, 0, 4096)
    for _, chunk := range data {
        buffer = append(buffer, chunk...)
        if len(buffer) >= 4096 {
            _, err := syscall.Write(fd, buffer)
            if err != nil {
                return err
            }
            buffer = buffer[:0] // Reset buffer
        }
    }

    // Write remaining data
    if len(buffer) > 0 {
        _, err := syscall.Write(fd, buffer)
        return err
    }
    return nil
}
```