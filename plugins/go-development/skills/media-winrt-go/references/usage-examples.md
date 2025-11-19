# Media WinRT Go - Usage Examples

## Complete Media Player Integration

```go
package main

import (
    "log"
    "github.com/dece2183/media-winrt-go/windows/media"
)

func main() {
    // Get system media transport controls
    controls, err := media.GetSystemMediaTransportControlsForCurrentView()
    if err != nil {
        log.Fatal(err)
    }

    // Enable controls
    controls.SetIsEnabled(true)

    // Get display updater for metadata
    updater, err := controls.GetDisplayUpdater()
    if err != nil {
        log.Fatal(err)
    }

    // Set media type
    updater.SetType(media.MediaPlaybackTypeMusic)

    // Set music properties
    musicProps, err := updater.GetMusicProperties()
    if err != nil {
        log.Fatal(err)
    }

    musicProps.SetTitle("Example Song")
    musicProps.SetArtist("Example Artist")
    musicProps.SetAlbum("Example Album")

    // Update the display
    updater.Update()

    // Set playback status
    controls.SetPlaybackStatus(media.MediaPlaybackStatusPlaying)

    // Clean up when done
    defer controls.SetPlaybackStatus(media.MediaPlaybackStatusStopped)
}
```

## Timeline Properties

```go
// Set timeline properties for seeking controls
timeline := media.NewSystemMediaTransportControlsTimelineProperties()
timeline.SetStartTime(time.Duration(0))
timeline.SetEndTime(time.Duration(180 * time.Second)) // 3 minutes
timeline.SetPosition(time.Duration(45 * time.Second)) // Currently at 45 seconds

controls.SetTimelineProperties(timeline)
```

## Button State Management

```go
// Enable/disable specific buttons
buttons := media.SystemMediaTransportControlsButton
controls.SetIsButtonEnabled(buttons.SystemMediaTransportControlsButtonPlay, true)
controls.SetIsButtonEnabled(buttons.SystemMediaTransportControlsButtonPause, true)
controls.SetIsButtonEnabled(buttons.SystemMediaTransportControlsButtonStop, true)
controls.SetIsButtonEnabled(buttons.SystemMediaTransportControlsButtonNext, false)
controls.SetIsButtonEnabled(buttons.SystemMediaTransportControlsButtonPrevious, false)
```

## Error Handling

The library uses standard Go error handling. Always check return values:

```go
controls, err := media.GetSystemMediaTransportControlsForCurrentView()
if err != nil {
    // Handle COM errors or initialization failures
    log.Printf("Failed to get media controls: %v", err)
    return
}
```

## Platform Requirements

- **Windows 10+**: Required for Windows Runtime APIs
- **CGO enabled**: Required for COM interface bindings
- **64-bit**: Recommended for better COM compatibility