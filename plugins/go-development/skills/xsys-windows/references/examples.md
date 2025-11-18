# Windows System Programming Examples

## File Operations

### Reading and Writing Windows Files
```go
package main

import (
    "fmt"
    "golang.org/x/sys/windows"
    "unsafe"
)

func fileOperations() error {
    filename, err := windows.UTF16PtrFromString("example.txt")
    if err != nil {
        return fmt.Errorf("UTF16 conversion failed: %v", err)
    }

    // Create file for writing
    handle, err := windows.CreateFile(
        filename,
        windows.GENERIC_WRITE,
        0,
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
    data := []byte("Hello, Windows API!")
    var bytesWritten uint32
    err = windows.WriteFile(handle, data, &bytesWritten, nil)
    if err != nil {
        return fmt.Errorf("WriteFile failed: %v", err)
    }

    fmt.Printf("Written %d bytes\n", bytesWritten)

    // Reopen for reading
    handle, err = windows.CreateFile(
        filename,
        windows.GENERIC_READ,
        windows.FILE_SHARE_READ,
        nil,
        windows.OPEN_EXISTING,
        windows.FILE_ATTRIBUTE_NORMAL,
        0,
    )
    if err != nil {
        return fmt.Errorf("CreateFile (read) failed: %v", err)
    }
    defer windows.CloseHandle(handle)

    // Read data
    buffer := make([]byte, 1024)
    var bytesRead uint32
    err = windows.ReadFile(handle, buffer, &bytesRead, nil)
    if err != nil {
        return fmt.Errorf("ReadFile failed: %v", err)
    }

    fmt.Printf("Read %d bytes: %s\n", bytesRead, string(buffer[:bytesRead]))
    return nil
}
```

### File Information and Attributes
```go
func fileInformation() error {
    filename, err := windows.UTF16PtrFromString("example.txt")
    if err != nil {
        return err
    }

    // Get file attributes
    attrs, err := windows.GetFileAttributes(filename)
    if err != nil {
        return fmt.Errorf("GetFileAttributes failed: %v", err)
    }

    fmt.Printf("File attributes: 0x%08x\n", attrs)

    // Check if file is hidden
    if attrs&windows.FILE_ATTRIBUTE_HIDDEN != 0 {
        fmt.Println("File is hidden")
    }

    // Set file as read-only
    err = windows.SetFileAttributes(filename, windows.FILE_ATTRIBUTE_READONLY)
    if err != nil {
        return fmt.Errorf("SetFileAttributes failed: %v", err)
    }

    return nil
}
```

## Registry Operations

### Reading and Writing Registry Values
```go
func registryOperations() error {
    var hKey windows.Handle

    // Open registry key
    pathUTF16, err := windows.UTF16PtrFromString("SOFTWARE\\MyApp")
    if err != nil {
        return err
    }

    err = windows.RegOpenKeyEx(
        windows.HKEY_LOCAL_MACHINE,
        pathUTF16,
        0,
        windows.KEY_READ|windows.KEY_WRITE,
        &hKey,
    )
    if err != nil {
        return fmt.Errorf("RegOpenKeyEx failed: %v", err)
    }
    defer windows.RegCloseKey(hKey)

    // Write a string value
    valueName, err := windows.UTF16PtrFromString("InstallPath")
    if err != nil {
        return err
    }

    valueData := []byte("C:\\Program Files\\MyApp\x00")
    err = windows.RegSetValueEx(
        hKey,
        valueName,
        0,
        windows.REG_SZ,
        &valueData[0],
        uint32(len(valueData)),
    )
    if err != nil {
        return fmt.Errorf("RegSetValueEx failed: %v", err)
    }

    // Read the value back
    var valueType uint32
    var dataSize uint32 = 256

    err = windows.RegQueryValueEx(
        hKey,
        valueName,
        nil,
        &valueType,
        nil,
        &dataSize,
    )
    if err != nil {
        return fmt.Errorf("RegQueryValueEx (size) failed: %v", err)
    }

    buffer := make([]byte, dataSize)
    err = windows.RegQueryValueEx(
        hKey,
        valueName,
        nil,
        &valueType,
        &buffer[0],
        &dataSize,
    )
    if err != nil {
        return fmt.Errorf("RegQueryValueEx (data) failed: %v", err)
    }

    if valueType == windows.REG_SZ {
        // Remove null terminator and convert to string
        installPath := windows.UTF16ToString((*[1 << 20]uint16)(unsafe.Pointer(&buffer[0]))[:dataSize/2])
        fmt.Printf("Install path: %s\n", installPath)
    }

    return nil
}

func enumerateRegistryValues() error {
    var hKey windows.Handle

    pathUTF16, err := windows.UTF16PtrFromString("SOFTWARE\\Microsoft\\Windows\\CurrentVersion")
    if err != nil {
        return err
    }

    err = windows.RegOpenKeyEx(
        windows.HKEY_LOCAL_MACHINE,
        pathUTF16,
        0,
        windows.KEY_READ,
        &hKey,
    )
    if err != nil {
        return fmt.Errorf("RegOpenKeyEx failed: %v", err)
    }
    defer windows.RegCloseKey(hKey)

    // Enumerate values
    i := uint32(0)
    valueName := make([]uint16, 256)
    nameLen := uint32(len(valueName))

    for {
        nameLen = uint32(len(valueName))
        err := windows.RegEnumValue(hKey, i, &valueName[0], &nameLen, nil, nil, nil, nil)
        if err != nil {
            if err == windows.ERROR_NO_MORE_ITEMS {
                break
            }
            return fmt.Errorf("RegEnumValue failed: %v", err)
        }

        valueNameStr := windows.UTF16ToString(valueName[:nameLen])
        fmt.Printf("Registry value: %s\n", valueNameStr)
        i++
    }

    return nil
}
```

## Process Management

### Creating and Managing Windows Processes
```go
func createWindowsProcess() error {
    // Prepare command line
    cmdLine, err := windows.UTF16PtrFromString("notepad.exe")
    if err != nil {
        return err
    }

    var startupInfo windows.StartupInfo
    startupInfo.Cb = uint32(unsafe.Sizeof(startupInfo))

    var processInfo windows.ProcessInformation

    // Create process
    err = windows.CreateProcess(
        nil,           // Application name
        cmdLine,       // Command line
        nil,           // Process security attributes
        nil,           // Thread security attributes
        false,         // Inherit handles
        0,             // Creation flags
        nil,           // Environment
        nil,           // Current directory
        &startupInfo,  // Startup information
        &processInfo,  // Process information
    )
    if err != nil {
        return fmt.Errorf("CreateProcess failed: %v", err)
    }

    fmt.Printf("Process created with PID: %d\n", processInfo.ProcessId)

    // Wait for process to exit
    var exitCode uint32
    for {
        err = windows.GetExitCodeProcess(processInfo.Process, &exitCode)
        if err != nil {
            return fmt.Errorf("GetExitCodeProcess failed: %v", err)
        }

        if exitCode != windows.STILL_ACTIVE {
            fmt.Printf("Process exited with code: %d\n", exitCode)
            break
        }

        fmt.Printf("Process %d is still running...\n", processInfo.ProcessId)
        time.Sleep(1 * time.Second)
    }

    // Clean up handles
    windows.CloseHandle(processInfo.Process)
    windows.CloseHandle(processInfo.Thread)

    return nil
}

func monitorProcess(pid uint32) error {
    // Open process handle
    handle, err := windows.OpenProcess(
        windows.PROCESS_QUERY_INFORMATION|windows.SYNCHRONIZE,
        false,
        pid,
    )
    if err != nil {
        return fmt.Errorf("OpenProcess failed: %v", err)
    }
    defer windows.CloseHandle(handle)

    // Wait for process exit with timeout
    _, err = windows.WaitForSingleObject(handle, windows.INFINITE)
    if err != nil {
        return fmt.Errorf("WaitForSingleObject failed: %v", err)
    }

    // Get exit code
    var exitCode uint32
    err = windows.GetExitCodeProcess(handle, &exitCode)
    if err != nil {
        return fmt.Errorf("GetExitCodeProcess failed: %v", err)
    }

    fmt.Printf("Process %d exited with code: %d\n", pid, exitCode)
    return nil
}
```

## Memory Management

### Virtual Memory Operations
```go
func memoryManagement() error {
    // Allocate virtual memory
    address, err := windows.VirtualAlloc(
        0,                      // Let system decide address
        1024*1024,             // 1MB
        windows.MEM_COMMIT|windows.MEM_RESERVE,
        windows.PAGE_READWRITE,
    )
    if err != nil {
        return fmt.Errorf("VirtualAlloc failed: %v", err)
    }
    defer windows.VirtualFree(address, 0, windows.MEM_RELEASE)

    fmt.Printf("Allocated memory at address: 0x%x\n", address)

    // Write to allocated memory
    data := []byte("Hello, virtual memory!")
    copy((*[1 << 30]byte)(unsafe.Pointer(address))[:len(data)], data)

    // Change memory protection
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

    fmt.Printf("Memory protection changed from 0x%x to 0x%x\n", oldProtect, windows.PAGE_READONLY)
    return nil
}
```

## Cryptography

### Data Protection
```go
func dataProtection() error {
    // Data to protect
    sensitiveData := []byte("This is sensitive information")

    var dataBlob windows.DataBlob
    dataBlob.Data = &sensitiveData[0]
    dataBlob.Size = uint32(len(sensitiveData))

    // Protect data
    var encryptedBlob windows.DataBlob
    err := windows.CryptProtectData(
        &dataBlob,
        windows.StringToUTF16Ptr("My Protected Data"),
        nil,
        nil,
        nil,
        windows.CRYPTPROTECT_UI_FORBIDDEN,
        &encryptedBlob,
    )
    if err != nil {
        return fmt.Errorf("CryptProtectData failed: %v", err)
    }
    defer windows.LocalFree(windows.Handle(encryptedBlob.Data))

    fmt.Printf("Data protected. Encrypted size: %d bytes\n", encryptedBlob.Size)

    // Unprotect data
    var decryptedBlob windows.DataBlob
    err = windows.CryptUnprotectData(
        &encryptedBlob,
        nil,
        nil,
        nil,
        nil,
        windows.CRYPTPROTECT_UI_FORBIDDEN,
        &decryptedBlob,
    )
    if err != nil {
        return fmt.Errorf("CryptUnprotectData failed: %v", err)
    }
    defer windows.LocalFree(windows.Handle(decryptedBlob.Data))

    decryptedData := (*[1 << 30]byte)(unsafe.Pointer(decryptedBlob.Data))[:decryptedBlob.Size:decryptedBlob.Size]
    fmt.Printf("Decrypted data: %s\n", string(decryptedData))

    return nil
}
```

### Certificate Operations
```go
func certificateOperations() error {
    // Open certificate store
    store, err := windows.CertOpenStore(
        windows.CERT_STORE_PROV_SYSTEM,
        0,
        0,
        windows.CERT_SYSTEM_STORE_CURRENT_USER,
        windows.StringToUTF16Ptr("MY"),
    )
    if err != nil {
        return fmt.Errorf("CertOpenStore failed: %v", err)
    }
    defer windows.CertCloseStore(store, 0)

    // Enumerate certificates
    var certContext *windows.CertContext
    certCount := 0

    for {
        certContext, err = windows.CertEnumCertificatesInStore(store, certContext)
        if err != nil {
            if err == syscall.Errno(windows.CRYPT_E_NOT_FOUND) {
                break // No more certificates
            }
            return fmt.Errorf("CertEnumCertificatesInStore failed: %v", err)
        }

        certCount++

        // Get certificate subject name
        subjectName := windows.UTF16ToString((*[1 << 20]uint16)(unsafe.Pointer(certContext.Subject))[:certContext.SubjectLen/2])
        fmt.Printf("Certificate %d: %s\n", certCount, subjectName)

        // Get certificate issuer name
        issuerName := windows.UTF16ToString((*[1 << 20]uint16)(unsafe.Pointer(certContext.Issuer))[:certContext.IssuerLen/2])
        fmt.Printf("  Issuer: %s\n", issuerName)
    }

    fmt.Printf("Found %d certificates\n", certCount)
    return nil
}
```

## System Information

### Getting System Information
```go
func getSystemInfo() error {
    // Get OS version information
    var versionInfo windows.Osversioninfoex
    versionInfo.OsversioninfoexSize = uint32(unsafe.Sizeof(versionInfo))

    err := windows.GetVersionEx(&versionInfo)
    if err != nil {
        return fmt.Errorf("GetVersionEx failed: %v", err)
    }

    fmt.Printf("Windows Version: %d.%d Build %d\n",
        versionInfo.MajorVersion,
        versionInfo.MinorVersion,
        versionInfo.BuildNumber)

    // Get computer name
    var computerName [windows.MAX_COMPUTERNAME_LENGTH + 1]uint16
    var size uint32 = windows.MAX_COMPUTERNAME_LENGTH + 1

    err = windows.GetComputerName(&computerName[0], &size)
    if err != nil {
        return fmt.Errorf("GetComputerName failed: %v", err)
    }

    fmt.Printf("Computer Name: %s\n", windows.UTF16ToString(computerName[:size]))

    // Get system directory
    var systemDir [windows.MAX_PATH + 1]uint16
    systemDirLen := windows.GetSystemDirectory(&systemDir[0], windows.MAX_PATH+1)
    if systemDirLen == 0 {
        return fmt.Errorf("GetSystemDirectory failed")
    }

    fmt.Printf("System Directory: %s\n", windows.UTF16ToString(systemDir[:systemDirLen]))

    // Get Windows directory
    var windowsDir [windows.MAX_PATH + 1]uint16
    windowsDirLen := windows.GetWindowsDirectory(&windowsDir[0], windows.MAX_PATH+1)
    if windowsDirLen == 0 {
        return fmt.Errorf("GetWindowsDirectory failed")
    }

    fmt.Printf("Windows Directory: %s\n", windows.UTF16ToString(windowsDir[:windowsDirLen]))

    // Get current time
    var systemTime windows.Systemtime
    windows.GetSystemTime(&systemTime)

    fmt.Printf("System Time: %04d-%02d-%02d %02d:%02d:%02d\n",
        systemTime.Year, systemTime.Month, systemTime.Day,
        systemTime.Hour, systemTime.Minute, systemTime.Second)

    return nil
}
```

## Event Logging

### Writing to Windows Event Log
```go
func eventLogging() error {
    // Register event source
    sourceName := "MyGoApplication"
    handle, err := windows.RegisterEventSource(nil, windows.StringToUTF16Ptr(sourceName))
    if err != nil {
        return fmt.Errorf("RegisterEventSource failed: %v", err)
    }
    defer windows.DeregisterEventSource(handle)

    // Log informational event
    infoMessage := "Application started successfully"
    messages := []*uint16{
        windows.StringToUTF16Ptr(infoMessage),
    }

    err = windows.ReportEvent(
        handle,
        windows.EVENTLOG_INFORMATION_TYPE,
        1, // Category
        1001, // Event ID
        nil, // User SID
        1, // Number of strings
        0, // Raw data size
        &messages[0],
        nil,
    )
    if err != nil {
        return fmt.Errorf("ReportEvent (info) failed: %v", err)
    }

    fmt.Println("Informational event logged")

    // Log error event
    errorMessage := "An error occurred during operation"
    errorMessages := []*uint16{
        windows.StringToUTF16Ptr(errorMessage),
    }

    err = windows.ReportEvent(
        handle,
        windows.EVENTLOG_ERROR_TYPE,
        1, // Category
        2001, // Event ID
        nil, // User SID
        1, // Number of strings
        0, // Raw data size
        &errorMessages[0],
        nil,
    )
    if err != nil {
        return fmt.Errorf("ReportEvent (error) failed: %v", err)
    }

    fmt.Println("Error event logged")
    return nil
}
```

## DLL Loading

### Loading and Using DLL Functions
```go
func dllOperations() error {
    // Load kernel32.dll
    kernel32 := windows.NewLazyDLL("kernel32.dll")

    // Get GetTickCount function
    getTickCount := kernel32.NewProc("GetTickCount")

    // Call the function
    tickCount, _, _ := getTickCount.Call()
    fmt.Printf("System tick count: %d\n", tickCount)

    // Load user32.dll
    user32 := windows.NewLazyDLL("user32.dll")

    // Get MessageBox function
    messageBox := user32.NewProc("MessageBoxW")

    // Call MessageBox
    title, _ := windows.UTF16PtrFromString("Hello")
    message, _ := windows.UTF16PtrFromString("Hello from Go!")
    ret, _, _ := messageBox.Call(
        0,
        uintptr(unsafe.Pointer(message)),
        uintptr(unsafe.Pointer(title)),
        0, // MB_OK
    )
    fmt.Printf("MessageBox returned: %d\n", ret)

    return nil
}

// Alternative: Using direct DLL loading
func directDLLLoading() error {
    // Load DLL
    handle, err := windows.LoadLibrary("advapi32.dll")
    if err != nil {
        return fmt.Errorf("LoadLibrary failed: %v", err)
    }
    defer windows.FreeLibrary(handle)

    // Get function address
    procAddr, err := windows.GetProcAddress(handle, "GetUserNameW")
    if err != nil {
        return fmt.Errorf("GetProcAddress failed: %v", err)
    }

    // Prepare buffer for username
    buffer := make([]uint16, 256)
    size := uint32(len(buffer))

    // Call function directly
    ret, _, _ := windows.Syscall(
        procAddr,
        3,
        uintptr(unsafe.Pointer(&buffer[0])),
        uintptr(unsafe.Pointer(&size)),
        0,
    )

    if ret == 0 {
        return fmt.Errorf("GetUserNameW failed")
    }

    username := windows.UTF16ToString(buffer[:size])
    fmt.Printf("Current user: %s\n", username)

    return nil
}
```

## Windows Services

### Service Management
```go
func serviceManagement() error {
    // Open service control manager
    manager, err := windows.OpenSCManager(nil, nil, windows.SC_MANAGER_CONNECT|windows.SC_MANAGER_ENUMERATE_SERVICE)
    if err != nil {
        return fmt.Errorf("OpenSCManager failed: %v", err)
    }
    defer windows.CloseServiceHandle(manager)

    // Enumerate services
    var bytesNeeded, servicesReturned, resumeHandle uint32
    var serviceType, serviceState uint32 = windows.SERVICE_WIN32, windows.SERVICE_STATE_ALL

    // First call to get required buffer size
    windows.EnumServicesStatusEx(
        manager,
        windows.SC_ENUM_PROCESS_INFO,
        serviceType,
        serviceState,
        nil, // Buffer
        0,   // Buffer size
        &bytesNeeded,
        &servicesReturned,
        &resumeHandle,
        nil,
    )

    if bytesNeeded == 0 {
        return fmt.Errorf("EnumServicesStatusEx failed to get buffer size")
    }

    // Allocate buffer
    buffer := make([]byte, bytesNeeded)
    servicesReturned = 0
    resumeHandle = 0

    // Second call to get actual data
    err = windows.EnumServicesStatusEx(
        manager,
        windows.SC_ENUM_PROCESS_INFO,
        serviceType,
        serviceState,
        &buffer[0],
        bytesNeeded,
        nil,
        &servicesReturned,
        &resumeHandle,
        nil,
    )
    if err != nil {
        return fmt.Errorf("EnumServicesStatusEx failed: %v", err)
    }

    fmt.Printf("Found %d services\n", servicesReturned)

    // Parse service information (simplified)
    offset := 0
    for i := 0; i < int(servicesReturned); i++ {
        // This is a simplified example - actual parsing is more complex
        if offset+4 > len(buffer) {
            break
        }
        // Process service information here
        offset += 100 // Move to next service record
    }

    return nil
}
```