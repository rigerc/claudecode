# Windows System Programming Troubleshooting Guide

## Common Issues and Solutions

### 1. Handle Leaks

**Problem**: Windows handles not being released properly, causing resource leaks.

**Symptoms**:
- Application consuming increasing amounts of memory
- "Too many open handles" errors
- System performance degradation

**Solutions**:
```go
// Always use defer for cleanup
func safeFileOperation(filename string) error {
    filenamePtr, err := windows.UTF16PtrFromString(filename)
    if err != nil {
        return err
    }

    handle, err := windows.CreateFile(
        filenamePtr,
        windows.GENERIC_READ,
        windows.FILE_SHARE_READ,
        nil,
        windows.OPEN_EXISTING,
        windows.FILE_ATTRIBUTE_NORMAL,
        0,
    )
    if err != nil {
        return err
    }
    defer windows.CloseHandle(handle) // Guaranteed cleanup

    // Use handle...
    return nil
}

// For multiple handles, use named cleanup functions
func safeMultipleOperations() error {
    handles := make([]windows.Handle, 0)

    // Named cleanup function
    defer func() {
        for _, handle := range handles {
            windows.CloseHandle(handle)
        }
    }()

    // Add handles to slice as they're created
    handle1, err := createHandle1()
    if err != nil {
        return err
    }
    handles = append(handles, handle1)

    // Continue with operations...
    return nil
}
```

### 2. UTF-16 String Conversion Issues

**Problem**: Incorrect string encoding when working with Windows APIs.

**Symptoms**:
- File not found errors with valid paths
- Registry operations failing
- Garbled text output

**Solutions**:
```go
// Safe UTF-16 conversion
func safeUTF16Ptr(s string) (*uint16, error) {
    if len(s) == 0 {
        return nil, nil
    }
    ptr, err := windows.UTF16PtrFromString(s)
    if err != nil {
        return nil, fmt.Errorf("UTF16 conversion failed for '%s': %v", s, err)
    }
    return ptr, nil
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

// Usage pattern
func fileOperations(filename string) error {
    filenamePtr, err := safeUTF16Ptr(filename)
    if err != nil {
        return err
    }

    handle, err := windows.CreateFile(
        filenamePtr,
        windows.GENERIC_READ,
        windows.FILE_SHARE_READ,
        nil,
        windows.OPEN_EXISTING,
        windows.FILE_ATTRIBUTE_NORMAL,
        0,
    )
    if err != nil {
        return fmt.Errorf("CreateFile failed for '%s': %v", filename, err)
    }
    defer windows.CloseHandle(handle)

    return nil
}
```

### 3. Windows Error Handling

**Problem**: Not properly handling Windows-specific error codes.

**Solutions**:
```go
// Enhanced error handling
type WindowsError struct {
    Operation string
    Path      string
    ErrorCode windows.Errno
}

func (e *WindowsError) Error() string {
    return fmt.Sprintf("%s failed for %s: %s (0x%x)",
        e.Operation, e.Path, e.ErrorCode.Error(), uint32(e.ErrorCode))
}

func wrapWindowsError(operation, path string, err error) error {
    if err == nil {
        return nil
    }

    if errno, ok := err.(windows.Errno); ok {
        return &WindowsError{
            Operation: operation,
            Path:      path,
            ErrorCode: errno,
        }
    }

    return fmt.Errorf("%s failed for %s: %v", operation, path, err)
}

// Usage
func safeFileRead(filename string) ([]byte, error) {
    filenamePtr, err := safeUTF16Ptr(filename)
    if err != nil {
        return nil, err
    }

    handle, err := windows.CreateFile(
        filenamePtr,
        windows.GENERIC_READ,
        windows.FILE_SHARE_READ,
        nil,
        windows.OPEN_EXISTING,
        windows.FILE_ATTRIBUTE_NORMAL,
        0,
    )
    if err != nil {
        return nil, wrapWindowsError("CreateFile", filename, err)
    }
    defer windows.CloseHandle(handle)

    buffer := make([]byte, 4096)
    var bytesRead uint32
    err = windows.ReadFile(handle, buffer, &bytesRead, nil)
    if err != nil {
        return nil, wrapWindowsError("ReadFile", filename, err)
    }

    return buffer[:bytesRead], nil
}
```

### 4. Buffer Size Issues

**Problem**: Buffers too small for Windows API operations.

**Solutions**:
```go
// Use appropriate buffer sizes
const (
    MaxPathLength      = windows.MAX_PATH
    MaxComputerName    = windows.MAX_COMPUTERNAME_LENGTH + 1
    RegistryMaxValueName = 16383
    RegistryMaxValueData = 1048576 // 1MB
)

// Dynamic buffer allocation
func getDynamicBuffer(initialSize, maxSize uint32) ([]byte, error) {
    buffer := make([]byte, initialSize)

    // If initial size is insufficient, try larger sizes
    for size := initialSize; size <= maxSize; size *= 2 {
        buffer = make([]byte, size)
        // Try operation...
        if operationSucceedsWith(buffer) {
            return buffer, nil
        }
    }

    return nil, fmt.Errorf("buffer size %d insufficient", maxSize)
}

// Registry value reading with proper buffer sizing
func readRegistryValue(key windows.Handle, valueName string) ([]byte, uint32, error) {
    valueNamePtr, err := safeUTF16Ptr(valueName)
    if err != nil {
        return nil, 0, err
    }

    // First call to get required size
    var dataType uint32
    var dataSize uint32
    err = windows.RegQueryValueEx(key, valueNamePtr, nil, &dataType, nil, &dataSize)
    if err != nil && err != windows.ERROR_MORE_DATA {
        return nil, 0, fmt.Errorf("RegQueryValueEx (size) failed: %v", err)
    }

    // Allocate buffer with extra space for null terminator
    buffer := make([]byte, dataSize+1)
    err = windows.RegQueryValueEx(key, valueNamePtr, nil, &dataType, &buffer[0], &dataSize)
    if err != nil {
        return nil, 0, fmt.Errorf("RegQueryValueEx (data) failed: %v", err)
    }

    return buffer[:dataSize], dataType, nil
}
```

### 5. Process Creation Issues

**Problem**: Failing to create processes due to permissions or paths.

**Solutions**:
```go
func robustProcessCreation(executable string, args []string) error {
    // Validate executable exists
    if _, err := os.Stat(executable); os.IsNotExist(err) {
        return fmt.Errorf("executable not found: %s", executable)
    }

    // Build command line safely
    cmdLine := fmt.Sprintf(`"%s"`, executable)
    for _, arg := range args {
        cmdLine += fmt.Sprintf(` "%s"`, strings.ReplaceAll(arg, `"`, `""`))
    }

    cmdLinePtr, err := safeUTF16Ptr(cmdLine)
    if err != nil {
        return err
    }

    // Set up process attributes
    var startupInfo windows.StartupInfo
    startupInfo.Cb = uint32(unsafe.Sizeof(startupInfo))

    // Hide the window if it's a GUI application
    startupInfo.Flags |= windows.STARTF_USESHOWWINDOW
    startupInfo.ShowWindow = windows.SW_HIDE

    var processInfo windows.ProcessInformation

    // Create process with error handling
    err = windows.CreateProcess(
        nil,           // Use command line
        cmdLinePtr,    // Command line
        nil,           // Process security attributes
        nil,           // Thread security attributes
        false,         // Inherit handles
        windows.CREATE_NO_WINDOW, // Creation flags
        nil,           // Environment (inherit from parent)
        nil,           // Current directory
        &startupInfo,  // Startup information
        &processInfo,  // Process information
    )
    if err != nil {
        // Provide more helpful error messages
        switch err {
        case windows.ERROR_FILE_NOT_FOUND:
            return fmt.Errorf("executable not found: %s", executable)
        case windows.ERROR_ACCESS_DENIED:
            return fmt.Errorf("access denied - check permissions for: %s", executable)
        case windows.ERROR_INVALID_PARAMETER:
            return fmt.Errorf("invalid command line: %s", cmdLine)
        default:
            return fmt.Errorf("CreateProcess failed: %v", err)
        }
    }

    // Clean up handles
    defer windows.CloseHandle(processInfo.Process)
    defer windows.CloseHandle(processInfo.Thread)

    fmt.Printf("Process created successfully with PID: %d\n", processInfo.ProcessId)
    return nil
}
```

### 6. Registry Permission Issues

**Problem**: Access denied errors when accessing registry keys.

**Solutions**:
```go
func safeRegistryOperation() error {
    // Try with increasing access levels
    accessLevels := []uint32{
        windows.KEY_READ,
        windows.KEY_READ | windows.KEY_WRITE,
        windows.KEY_ALL_ACCESS,
    }

    var hKey windows.Handle
    var lastError error

    for _, access := range accessLevels {
        pathPtr, err := safeUTF16Ptr("SOFTWARE\\MyApp")
        if err != nil {
            return err
        }

        err = windows.RegOpenKeyEx(
            windows.HKEY_LOCAL_MACHINE,
            pathPtr,
            0,
            access,
            &hKey,
        )
        if err == nil {
            break // Success
        }
        lastError = err

        // If it's not an access error, don't retry
        if err != windows.ERROR_ACCESS_DENIED {
            return fmt.Errorf("RegOpenKeyEx failed: %v", err)
        }
    }

    if lastError != nil {
        return fmt.Errorf("failed to open registry key even with maximum access: %v", lastError)
    }
    defer windows.RegCloseKey(hKey)

    // Continue with registry operations...
    return nil
}

// Run with elevated privileges if needed
func runAsAdminForRegistryAccess() error {
    // Check if running as administrator
    var token windows.Handle
    err := windows.OpenProcessToken(windows.CurrentProcess(), windows.TOKEN_QUERY, &token)
    if err != nil {
        return fmt.Errorf("OpenProcessToken failed: %v", err)
    }
    defer windows.CloseHandle(token)

    var tokenElevation windows.Token elevation
    var returnedLen uint32
    err = windows.GetTokenInformation(token, windows.TokenElevation,
        (*byte)(unsafe.Pointer(&tokenElevation)), uint32(unsafe.Sizeof(tokenElevation)), &returnedLen)
    if err != nil {
        return fmt.Errorf("GetTokenInformation failed: %v", err)
    }

    if !tokenElevation.TokenIsElevated {
        return fmt.Errorf("this operation requires administrator privileges")
    }

    return nil
}
```

### 7. Memory Management Issues

**Problem**: Memory leaks or access violations with virtual memory operations.

**Solutions**:
```go
func safeVirtualMemoryManagement() error {
    // Allocate memory
    address, err := windows.VirtualAlloc(
        0,
        1024*1024, // 1MB
        windows.MEM_COMMIT|windows.MEM_RESERVE,
        windows.PAGE_READWRITE,
    )
    if err != nil {
        return fmt.Errorf("VirtualAlloc failed: %v", err)
    }
    defer func() {
        // Ensure cleanup even if panic occurs
        if address != 0 {
            windows.VirtualFree(address, 0, windows.MEM_RELEASE)
        }
    }()

    // Validate address
    if address == 0 {
        return fmt.Errorf("VirtualAlloc returned NULL address")
    }

    // Safe memory access
    if address != 0 {
        // Convert to byte slice with bounds checking
        memory := (*[1 << 30]byte)(unsafe.Pointer(address))

        // Write data safely
        data := []byte("Hello, virtual memory!")
        if len(data) <= 1024*1024 {
            copy(memory[:len(data)], data)
        } else {
            return fmt.Errorf("data too large for allocated memory")
        }

        // Change protection
        var oldProtect uint32
        err = windows.VirtualProtect(
            address,
            uint32(len(data)),
            windows.PAGE_READONLY,
            &oldProtect,
        )
        if err != nil {
            return fmt.Errorf("VirtualProtect failed: %v", err)
        }

        fmt.Printf("Memory protection changed from 0x%x to 0x%x\n",
            oldProtect, windows.PAGE_READONLY)
    }

    return nil
}
```

## Debugging Techniques

### 1. Windows Event Log Integration
```go
func logToEventLog(source string, message string, eventType uint16) error {
    handle, err := windows.RegisterEventSource(nil, windows.StringToUTF16Ptr(source))
    if err != nil {
        return fmt.Errorf("RegisterEventSource failed: %v", err)
    }
    defer windows.DeregisterEventSource(handle)

    messages := []*uint16{
        windows.StringToUTF16Ptr(message),
    }

    err = windows.ReportEvent(
        handle,
        eventType,
        1, // Category
        1,  // Event ID
        nil, // User SID
        1,   // Number of strings
        0,   // Raw data size
        &messages[0],
        nil,
    )
    if err != nil {
        return fmt.Errorf("ReportEvent failed: %v", err)
    }

    return nil
}

// Usage
func debugOperation() {
    err := someWindowsOperation()
    if err != nil {
        logToEventLog("MyGoApp", fmt.Sprintf("Operation failed: %v", err),
            windows.EVENTLOG_ERROR_TYPE)
    } else {
        logToEventLog("MyGoApp", "Operation completed successfully",
            windows.EVENTLOG_INFORMATION_TYPE)
    }
}
```

### 2. Performance Monitoring
```go
func measureWindowsOperation(operation string, fn func() error) error {
    start := time.Now()

    // Get initial handle count (approximate)
    initialTime := start.Unix()

    err := fn()

    duration := time.Since(start)

    // Log performance metrics
    logMessage := fmt.Sprintf("%s took %v", operation, duration)
    if duration > time.Second {
        logMessage += " - SLOW OPERATION"
        logToEventLog("PerformanceMonitor", logMessage, windows.EVENTLOG_WARNING_TYPE)
    } else {
        fmt.Println(logMessage)
    }

    return err
}

// Usage
func withPerformanceMonitoring() error {
    return measureWindowsOperation("file read", func() error {
        // Your Windows API operation here
        return readFileOperation()
    })
}
```

### 3. Resource Usage Tracking
```go
type ResourceTracker struct {
    initialHandles uint32
    peakHandles    uint32
    operations     []string
    mu             sync.Mutex
}

func NewResourceTracker() *ResourceTracker {
    // Get initial process handle count (approximate)
    return &ResourceTracker{
        initialHandles: 0, // Would need to use performance counters for accurate count
        operations:     make([]string, 0),
    }
}

func (rt *ResourceTracker) TrackOperation(op string) {
    rt.mu.Lock()
    defer rt.mu.Unlock()
    rt.operations = append(rt.operations, op)
}

func (rt *ResourceTracker) GetReport() string {
    rt.mu.Lock()
    defer rt.mu.Unlock()

    report := fmt.Sprintf("Tracked %d operations:\n", len(rt.operations))
    for i, op := range rt.operations {
        report += fmt.Sprintf("%d: %s\n", i+1, op)
    }

    return report
}

// Usage
func withResourceTracking() error {
    tracker := NewResourceTracker()
    defer fmt.Println(tracker.GetReport())

    tracker.TrackOperation("Opening file")
    // ... operation ...

    tracker.TrackOperation("Reading registry")
    // ... operation ...

    return nil
}
```

## Testing Strategies

### 1. Mock Windows APIs for Testing
```go
// Interface for testing
type WindowsAPI interface {
    CreateFile(name *uint16, access uint32, share uint32, sa *windows.SecurityAttributes,
        createmode uint32, attrs uint32, templatefile windows.Handle) (windows.Handle, error)
    CloseHandle(handle windows.Handle) error
    ReadFile(handle windows.Handle, buf []byte, done *uint32, overlapped *windows.Overlapped) error
    WriteFile(handle windows.Handle, buf []byte, done *uint32, overlapped *windows.Overlapped) error
}

// Real implementation
type RealWindowsAPI struct{}

func (r *RealWindowsAPI) CreateFile(name *uint16, access uint32, share uint32, sa *windows.SecurityAttributes,
    createmode uint32, attrs uint32, templatefile windows.Handle) (windows.Handle, error) {
    return windows.CreateFile(name, access, share, sa, createmode, attrs, templatefile)
}

func (r *RealWindowsAPI) CloseHandle(handle windows.Handle) error {
    return windows.CloseHandle(handle)
}

func (r *RealWindowsAPI) ReadFile(handle windows.Handle, buf []byte, done *uint32, overlapped *windows.Overlapped) error {
    return windows.ReadFile(handle, buf, done, overlapped)
}

func (r *RealWindowsAPI) WriteFile(handle windows.Handle, buf []byte, done *uint32, overlapped *windows.Overlapped) error {
    return windows.WriteFile(handle, buf, done, overlapped)
}

// Mock implementation for testing
type MockWindowsAPI struct {
    Files map[string][]byte
    Handles map[windows.Handle]string
    nextHandle windows.Handle
}

func NewMockWindowsAPI() *MockWindowsAPI {
    return &MockWindowsAPI{
        Files: make(map[string][]byte),
        Handles: make(map[windows.Handle]string),
        nextHandle: 1000,
    }
}

func (m *MockWindowsAPI) CreateFile(name *uint16, access uint32, share uint32, sa *windows.SecurityAttributes,
    createmode uint32, attrs uint32, templatefile windows.Handle) (windows.Handle, error) {

    filename := windows.UTF16ToString((*[1 << 20]uint16)(unsafe.Pointer(name))[:256])

    if createmode == windows.CREATE_ALWAYS || createmode == windows.CREATE_NEW {
        m.Files[filename] = []byte{}
    }

    handle := m.nextHandle
    m.nextHandle++
    m.Handles[handle] = filename

    return handle, nil
}

func (m *MockWindowsAPI) CloseHandle(handle windows.Handle) error {
    delete(m.Handles, handle)
    return nil
}

func (m *MockWindowsAPI) ReadFile(handle windows.Handle, buf []byte, done *uint32, overlapped *windows.Overlapped) error {
    filename, exists := m.Handles[handle]
    if !exists {
        return windows.ERROR_INVALID_HANDLE
    }

    data := m.Files[filename]
    n := copy(buf, data)
    *done = uint32(n)

    return nil
}

func (m *MockWindowsAPI) WriteFile(handle windows.Handle, buf []byte, done *uint32, overlapped *windows.Overlapped) error {
    filename, exists := m.Handles[handle]
    if !exists {
        return windows.ERROR_INVALID_HANDLE
    }

    m.Files[filename] = append(m.Files[filename], buf...)
    *done = uint32(len(buf))

    return nil
}
```

### 2. Error Injection Testing
```go
func testWindowsErrorHandling(t *testing.T) {
    tests := []struct {
        name    string
        error   error
        wantErr string
    }{
        {"file not found", windows.ERROR_FILE_NOT_FOUND, "file not found"},
        {"access denied", windows.ERROR_ACCESS_DENIED, "access denied"},
        {"invalid handle", windows.ERROR_INVALID_HANDLE, "invalid handle"},
        {"out of memory", windows.ERROR_NOT_ENOUGH_MEMORY, "not enough memory"},
    }

    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            wrapped := wrapWindowsError("TestOperation", "test.txt", tt.error)
            if wrapped == nil {
                t.Fatal("expected error")
            }
            if !strings.Contains(strings.ToLower(wrapped.Error()), strings.ToLower(tt.wantErr)) {
                t.Errorf("error = %v, want %v", wrapped, tt.wantErr)
            }
        })
    }
}
```

## Platform-Specific Considerations

### Windows Version Compatibility
```go
func checkWindowsVersion() error {
    var versionInfo windows.Osversioninfoex
    versionInfo.OsversioninfoexSize = uint32(unsafe.Sizeof(versionInfo))

    err := windows.GetVersionEx(&versionInfo)
    if err != nil {
        return fmt.Errorf("GetVersionEx failed: %v", err)
    }

    // Check minimum Windows version requirements
    if versionInfo.MajorVersion < 6 {
        return fmt.Errorf("Windows Vista or later required (found %d.%d)",
            versionInfo.MajorVersion, versionInfo.MinorVersion)
    }

    // Specific version checks
    if versionInfo.MajorVersion == 10 && versionInfo.BuildNumber >= 22000 {
        fmt.Println("Running on Windows 11 or later")
    } else if versionInfo.MajorVersion == 10 {
        fmt.Println("Running on Windows 10")
    } else if versionInfo.MajorVersion == 6 && versionInfo.MinorVersion >= 1 {
        fmt.Println("Running on Windows 7/8/8.1")
    }

    return nil
}
```

## Best Practices Checklist

### Before Using Windows APIs
- [ ] Check Windows version compatibility
- [ ] Validate string encodings (UTF-16)
- [ ] Plan for proper handle management
- [ ] Consider security implications
- [ ] Test error handling paths

### During Implementation
- [ ] Always use `defer` for handle cleanup
- [ ] Convert strings to UTF-16 properly
- [ ] Check all Windows API return values
- [ ] Use appropriate buffer sizes
- [ ] Handle Windows-specific error codes

### Testing and Validation
- [ ] Test on different Windows versions
- [ ] Verify resource cleanup
- [ ] Test error handling paths
- [ ] Monitor for handle/memory leaks
- [ ] Use mocks for unit testing