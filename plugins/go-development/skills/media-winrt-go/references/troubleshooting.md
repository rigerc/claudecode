# Media WinRT Go - Troubleshooting Guide

## Common Issues and Solutions

### 1. COM Initialization Failures

**Problem**: `GetSystemMediaTransportControlsForCurrentView()` returns COM initialization errors

**Symptoms**:
- `CoInitializeEx` errors
- `E_NOTINITIALIZED` errors
- Runtime panics with COM-related messages

**Solutions**:

```go
// Ensure COM is initialized (usually handled by the library)
import "golang.org/x/sys/windows/ole"

// Manual COM initialization (if needed)
func initCOM() error {
    return ole.CoInitializeEx(0, ole.COINIT_MULTITHREADED)
}
```

**Best Practices**:
- Run on Windows with proper COM support
- Avoid multiple COM initializations in the same thread
- Use `ole.CoUninitialize()` when done (rarely needed in Go)

### 2. Access Denied Errors

**Problem**: `E_ACCESSDENIED` when accessing system media controls

**Causes**:
- Insufficient permissions
- Running in restricted environment
- Windows policy restrictions

**Solutions**:
```go
if err != nil && ole.IsEqual(err, ole.E_ACCESSDENIED) {
    log.Println("Access denied - running as administrator may help")
    // Fallback to alternative media integration
}
```

### 3. Media Controls Not Appearing

**Problem**: System media controls don't show up in Windows UI

**Debugging Steps**:

```go
// Check if controls are enabled
enabled, err := controls.GetIsEnabled()
if err != nil {
    log.Printf("Error getting enabled state: %v", err)
} else if !enabled {
    log.Println("Controls are disabled - enabling...")
    controls.SetIsEnabled(true)
}

// Verify playback status is set
status, err := controls.GetPlaybackStatus()
if err != nil {
    log.Printf("Error getting playback status: %v", err)
} else {
    log.Printf("Current playback status: %d", status)
}
```

**Required Conditions**:
1. `IsEnabled` must be `true`
2. `PlaybackStatus` must be set (not `Closed`)
3. Media metadata should be provided via `DisplayUpdater`

### 4. Thumbnail Images Not Loading

**Problem**: Media thumbnails don't appear in system UI

**Common Causes**:
- Invalid file paths
- Unsupported image formats
- File access permissions

**Solution**:
```go
// Use absolute paths
thumbnailPath, err := filepath.Abs("thumbnail.jpg")
if err != nil {
    log.Printf("Error getting absolute path: %v", err)
    return
}

// Verify file exists
if _, err := os.Stat(thumbnailPath); os.IsNotExist(err) {
    log.Println("Thumbnail file does not exist")
    return
}

thumbnail, err := updater.GetThumbnail()
if err != nil {
    log.Printf("Error getting thumbnail: %v", err)
    return
}

err = thumbnail.SetFromFilePath(thumbnailPath)
if err != nil {
    log.Printf("Error setting thumbnail: %v", err)
    return
}
```

### 5. Timeline Not Updating

**Problem**: Seek bar doesn't update or shows incorrect values

**Debug Timeline Properties**:
```go
timeline, err := controls.GetTimelineProperties()
if err != nil {
    log.Printf("Error getting timeline: %v", err)
    return
}

log.Printf("Timeline - Start: %v, End: %v, Position: %v",
    timeline.GetStartTime(),
    timeline.GetEndTime(),
    timeline.GetPosition())
```

**Common Issues**:
- Timeline not set at all
- Invalid time values (negative or extremely large)
- Timeline properties not updated when media position changes

**Solution**:
```go
// Update timeline regularly during playback
func updateTimeline(position time.Duration, duration time.Duration) {
    timeline := media.NewSystemMediaTransportControlsTimelineProperties()
    timeline.SetStartTime(0)
    timeline.SetEndTime(duration)
    timeline.SetPosition(position)
    timeline.SetMinSeekTime(0)
    timeline.SetMaxSeekTime(duration)

    controls.SetTimelineProperties(timeline)
}
```

### 6. Button Events Not Firing

**Problem**: Button press handlers don't receive events

**Debugging**:
```go
// Test button state
buttons := []media.SystemMediaTransportControlsButton{
    media.SystemMediaTransportControlsButtonPlay,
    media.SystemMediaTransportControlsButtonPause,
    media.SystemMediaTransportControlsButtonStop,
}

for _, button := range buttons {
    enabled, err := controls.GetIsButtonEnabled(button)
    if err != nil {
        log.Printf("Error checking button %d: %v", button, err)
    } else {
        log.Printf("Button %d enabled: %v", button, enabled)
    }
}
```

**Ensure**:
- Buttons are enabled via `SetIsButtonEnabled()`
- Event handlers are properly registered
- Application has focus (some Windows UI restrictions)

### 7. Memory Leaks

**Problem**: Increasing memory usage over time

**Best Practices**:
```go
// Release COM objects when done (if using raw COM interfaces)
defer func() {
    if controls != nil {
        controls.Release()
    }
    if updater != nil {
        updater.Release()
    }
}()
```

**Note**: The library should handle most COM object cleanup automatically.

### 8. Cross-Platform Issues

**Problem**: Code doesn't work on non-Windows systems

**Solution**: Add build constraints and runtime checks:
```go
// +build windows

package main

import (
    "runtime"
    "github.com/dece2183/media-winrt-go/windows/media"
)

func initMediaControls() (*media.SystemMediaTransportControls, error) {
    if runtime.GOOS != "windows" {
        return nil, fmt.Errorf("media-winrt-go is Windows-only")
    }

    return media.GetSystemMediaTransportControlsForCurrentView()
}
```

## Debug Tools

### Logging All Errors
```go
func logIfError(prefix string, err error) {
    if err != nil {
        log.Printf("%s: %v", prefix, err)
        // Print COM error codes for debugging
        if comErr, ok := err.(*ole.OleError); ok {
            log.Printf("COM Error Code: 0x%X", comErr.Code())
        }
    }
}
```

### State Inspection
```go
func inspectControls(controls *media.SystemMediaTransportControls) {
    log.Println("=== Media Controls State ===")

    if enabled, err := controls.GetIsEnabled(); err == nil {
        log.Printf("Enabled: %v", enabled)
    }

    if status, err := controls.GetPlaybackStatus(); err == nil {
        log.Printf("Status: %d", status)
    }

    log.Println("===========================")
}
```

## Performance Considerations

1. **Frequent Updates**: Avoid updating timeline properties too frequently (limit to ~10-30 Hz)
2. **Metadata Changes**: Only update metadata when it actually changes
3. **Thumbnail Loading**: Cache thumbnails to avoid repeated disk I/O
4. **Event Handlers**: Keep event handlers lightweight and non-blocking

## Windows Version Compatibility

- **Windows 10/11**: Full support
- **Windows 8.1**: Limited support (some features may not work)
- **Windows 7/earlier**: Not supported (WinRT APIs not available)

Use runtime version checks if needed:
```go
func isWindows10OrLater() bool {
    major, _, _ := windows.RtlGetVersion()
    return major >= 10
}
```