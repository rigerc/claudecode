# Media WinRT Go - COM Interface Internals

## Understanding COM in Go Context

### What is COM?
Component Object Model (COM) is Microsoft's binary interface standard for software components. WinRT APIs are built on top of COM, and the media-winrt-go library provides Go bindings to these interfaces.

### COM Basics for Go Developers

```go
import (
    "golang.org/x/sys/windows/ole"
    "github.com/dece2183/media-winrt-go/windows/media"
)

// COM objects are reference counted
var controls *media.SystemMediaTransportControls

// Release when done (automatically handled by most library functions)
defer func() {
    if controls != nil {
        controls.Release()
    }
}()
```

## COM Interface Hierarchy

### SystemMediaTransportControls Interface
```go
// This represents the underlying COM interface
type ISystemMediaTransportControls interface {
    ole.IUnknown // Base COM interface

    // Methods correspond to COM interface methods
    GetIsEnabled() (bool, error)
    SetIsEnabled(enabled bool) error
    GetPlaybackStatus() (media.MediaPlaybackStatus, error)
    SetPlaybackStatus(status media.MediaPlaybackStatus) error
    // ... other methods
}
```

### GUID Identifiers
Each COM interface has a unique GUID (Globally Unique Identifier):

```go
// Example: Interface GUID (these are used internally)
var IID_ISystemMediaTransportControls = ole.NewGUID("{C1F9A4F5-3B2C-4A5B-9D7E-8F6E4A2C1B9D}")

// COM interfaces are identified by their GUIDs
interface, err := ole.CreateInstance(CLSID_SystemMediaTransportControls, IID_ISystemMediaTransportControls)
```

## Memory Management

### Reference Counting
COM objects use reference counting for memory management:

```go
// AddRef is called automatically when creating object
controls, err := media.GetSystemMediaTransportControlsForCurrentView()

// Release should be called when done (often automatic in Go wrappers)
defer controls.Release()

// Multiple references increase count
ref1 := controls
ref2 := controls // Both reference the same COM object
```

### Automatic vs Manual Management
The media-winrt-go library handles most COM management automatically:

```go
// Automatic: Go handles cleanup when object goes out of scope
func autoCleanup() {
    controls, _ := media.GetSystemMediaTransportControlsForCurrentView()
    controls.SetIsEnabled(true)
    // Go's garbage collector handles cleanup
}

// Manual: For fine-grained control
func manualCleanup() {
    controls, _ := media.GetSystemMediaTransportControlsForCurrentView()
    defer controls.Release() // Explicit cleanup

    controls.SetIsEnabled(true)
}
```

## Error Handling in COM

### HRESULT Values
COM methods return HRESULT values indicating success or failure:

```go
// Common HRESULT values
const (
    S_OK          = 0x00000000 // Success
    E_FAIL        = 0x80004005 // Unspecified error
    E_INVALIDARG  = 0x80070057 // Invalid argument
    E_ACCESSDENIED = 0x80070005 // Access denied
    E_NOTIMPL     = 0x80004001 // Not implemented
)

// Check for specific COM errors
if err != nil {
    if ole.IsEqual(err, ole.E_ACCESSDENIED) {
        // Handle access denied
    } else if ole.IsEqual(err, ole.E_NOTIMPL) {
        // Handle not implemented
    }
}
```

### OleError Type
COM errors in Go are typically returned as *ole.OleError:

```go
func handleCOMError(err error) {
    if oleErr, ok := err.(*ole.OleError); ok {
        fmt.Printf("COM Error Code: 0x%X\n", oleErr.Code())
        fmt.Printf("COM Error Description: %s\n", oleErr.Error())

        // Check specific error codes
        switch oleErr.Code() {
        case 0x80070005: // E_ACCESSDENIED
            fmt.Println("Access denied")
        case 0x80004001: // E_NOTIMPL
            fmt.Println("Not implemented")
        }
    }
}
```

## Thread Safety

### COM Apartment Threading Model
COM uses apartment threading - each thread belongs to a single-threaded apartment (STA) or multi-threaded apartment (MTA):

```go
// Initialize COM for multi-threaded use
func initCOM() error {
    return ole.CoInitializeEx(0, ole.COINIT_MULTITHREADED)
}

// Clean up COM when done
func cleanupCOM() {
    ole.CoUninitialize()
}
```

### Thread-Safe Usage
```go
type ThreadSafeMediaController struct {
    mu       sync.RWMutex
    controls *media.SystemMediaTransportControls
}

func (tsc *ThreadSafeMediaController) SetPlaybackStatus(status media.MediaPlaybackStatus) error {
    tsc.mu.Lock()
    defer tsc.mu.Unlock()
    return tsc.controls.SetPlaybackStatus(status)
}

func (tsc *ThreadSafeMediaController) GetPlaybackStatus() (media.MediaPlaybackStatus, error) {
    tsc.mu.RLock()
    defer tsc.mu.RUnlock()
    return tsc.controls.GetPlaybackStatus()
}
```

## Interface Querying

### COM Interface Navigation
COM objects support interface querying to discover additional interfaces:

```go
// Query for additional interfaces
// This is typically handled by the library, but understanding helps with debugging
func queryInterface(unknown ole.IUnknown, iid *ole.GUID) (ole.IUnknown, error) {
    return unknown.QueryInterface(iid)
}
```

### Interface Casting
```go
// In Go, this is handled by type assertions
var unknown ole.IUnknown = controls

// Cast to specific interface type
if mediaControls, ok := unknown.(*media.SystemMediaTransportControls); ok {
    // Use mediaControls
}
```

## WinRT Specifics

### WinRT vs COM
WinRT is built on COM but adds additional abstractions:

```go
// WinRT properties vs COM methods
// COM style:
var enabled bool
err := controls.GetIsEnabled(&enabled)

// WinRT style (as exposed by Go library):
enabled, err := controls.GetIsEnabled()
```

### Async Operations
Many WinRT operations are asynchronous:

```go
// Async operations in WinRT are converted to synchronous Go calls
// The library handles the async/sync conversion internally
controls.SetPlaybackStatus(media.MediaPlaybackStatusPlaying) // Looks sync, but may be async internally
```

## Debugging COM Issues

### COM Error Codes
Common error patterns to watch for:

```go
func debugCOMError(err error) {
    if err == nil {
        return
    }

    fmt.Printf("COM Error: %v\n", err)

    if oleErr, ok := err.(*ole.OleError); ok {
        code := oleErr.Code()

        switch {
        case code == 0x80070005:
            fmt.Println("→ Access denied (check permissions)")
        case code == 0x800706F8:
            fmt.Println("→ Invalid thread (COM threading issue)")
        case code == 0x800706BE:
            fmt.Println("→ Remote procedure call failed")
        case code == 0x80004001:
            fmt.Println("→ Not implemented (feature unavailable)")
        case code == 0x80004002:
            fmt.Println("→ Interface not supported")
        case code == 0x8007000E:
            fmt.Println("→ Out of memory")
        case code == 0x80004003:
            fmt.Println("→ Invalid pointer")
        }
    }
}
```

### Memory Leak Detection
```go
// For debugging COM reference leaks
func trackReferences(obj ole.IUnknown) {
    // Add reference
    obj.AddRef()

    // Do work...

    // Release reference
    obj.Release()
}

// Common leak patterns to avoid:
func commonLeaks() {
    controls, _ := media.GetSystemMediaTransportControlsForCurrentView()

    // BAD: Creating objects in loops without releasing
    for i := 0; i < 1000; i++ {
        updater, _ := controls.GetDisplayUpdater()
        // updater not explicitly released - potential leak
    }

    // GOOD: Explicit cleanup
    for i := 0; i < 1000; i++ {
        updater, _ := controls.GetDisplayUpdater()
        defer updater.Release() // Or handle explicitly
    }
}
```

## Best Practices

### COM Initialization
```go
// Initialize once at application startup
func main() {
    // Initialize COM (often handled by library)
    if err := ole.CoInitializeEx(0, ole.COINIT_MULTITHREADED); err != nil {
        log.Fatal("COM initialization failed:", err)
    }
    defer ole.CoUninitialize()

    // Your application code
    runMediaApp()
}
```

### Resource Management
```go
// Pattern for proper resource management
func properResourceManagement() error {
    // Create object
    controls, err := media.GetSystemMediaTransportControlsForCurrentView()
    if err != nil {
        return err
    }
    defer controls.Release()

    // Use object
    controls.SetIsEnabled(true)

    // Nested objects also need cleanup
    updater, err := controls.GetDisplayUpdater()
    if err != nil {
        return err
    }
    defer updater.Release()

    // Work with nested object
    musicProps, err := updater.GetMusicProperties()
    if err != nil {
        return err
    }
    defer musicProps.Release()

    musicProps.SetTitle("Example")

    return nil
}
```

### Error Handling Strategy
```go
// Wrap COM errors with context
func wrapCOMError(operation string, err error) error {
    if err == nil {
        return nil
    }

    return fmt.Errorf("%s failed: %w", operation, err)
}

// Usage
err := wrapCOMError("set playback status", controls.SetPlaybackStatus(status))
if err != nil {
    log.Printf("Media control error: %v", err)
}
```

## Performance Considerations

1. **Avoid frequent interface queries**: Cache interface references
2. **Batch operations**: Update multiple properties before calling Update()
3. **Minimize cross-thread calls**: Keep COM operations on the same thread when possible
4. **Release promptly**: Don't hold onto COM objects longer than needed

## Platform Requirements

- **Windows 8.1+**: Minimum for WinRT APIs
- **Windows 10+**: Full feature support
- **CGO enabled**: Required for COM bindings
- **64-bit preferred**: Better COM support on 64-bit Windows