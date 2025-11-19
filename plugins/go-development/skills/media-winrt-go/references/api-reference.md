# Media WinRT Go - API Reference

## SystemMediaTransportControls

### Core Functions

#### `GetSystemMediaTransportControlsForCurrentView()`
```go
controls, err := media.GetSystemMediaTransportControlsForCurrentView()
```
Returns the current view's SystemMediaTransportControls instance.

### Properties

#### `IsEnabled`
```go
controls.SetIsEnabled(true)  // Enable system media controls
controls.SetIsEnabled(false) // Disable system media controls
```
Controls whether the system media transport controls are enabled.

#### `PlaybackStatus`
```go
controls.SetPlaybackStatus(media.MediaPlaybackStatusPlaying)
controls.SetPlaybackStatus(media.MediaPlaybackStatusPaused)
controls.SetPlaybackStatus(media.MediaPlaybackStatusStopped)
controls.SetPlaybackStatus(media.MediaPlaybackStatusClosed)
```
Sets the current playback status of the media.

### Button Controls

#### Available Buttons
```go
const (
    SystemMediaTransportControlsButtonPlay        = 0
    SystemMediaTransportControlsButtonPause       = 1
    SystemMediaTransportControlsButtonStop        = 2
    SystemMediaTransportControlsButtonRecord      = 3
    SystemMediaTransportControlsButtonFastForward = 4
    SystemMediaTransportControlsButtonRewind      = 5
    SystemMediaTransportControlsButtonNext        = 6
    SystemMediaTransportControlsButtonPrevious    = 7
    SystemMediaTransportControlsButtonChannelUp   = 8
    SystemMediaTransportControlsButtonChannelDown = 9
)
```

#### Button Enable/Disable
```go
controls.SetIsButtonEnabled(media.SystemMediaTransportControlsButtonPlay, true)
controls.SetIsButtonEnabled(media.SystemMediaTransportControlsButtonPause, true)
controls.SetIsButtonEnabled(media.SystemMediaTransportControlsButtonStop, true)
```
Controls which buttons are enabled in the system media UI.

## SystemMediaTransportControlsDisplayUpdater

### Getting the Updater
```go
updater, err := controls.GetDisplayUpdater()
```

### Media Types
```go
updater.SetType(media.MediaPlaybackTypeMusic)
updater.SetType(media.MediaPlaybackTypeVideo)
updater.SetType(media.MediaPlaybackTypeImage)
updater.SetType(media.MediaPlaybackTypeUnknown)
```

### Music Properties
```go
musicProps, err := updater.GetMusicProperties()
musicProps.SetTitle("Song Title")
musicProps.SetArtist("Artist Name")
musicProps.SetAlbum("Album Name")
musicProps.SetTrackNumber(5)
musicProps.SetGenre("Pop")
```

### Video Properties
```go
videoProps, err := updater.GetVideoProperties()
videoProps.SetTitle("Video Title")
videoProps.SetSubtitle("Episode Title")
videoProps.SetSeasonNumber(2)
videoProps.SetEpisodeNumber(5)
```

### Image Properties
```go
imageProps, err := updater.GetImageProperties()
imageProps.SetTitle("Image Title")
imageProps.SetSubtitle("Image Subtitle")
```

### Thumbnail Support
```go
// Set thumbnail from file path
thumbnail, err := updater.GetThumbnail()
thumbnail.SetFromFilePath("path/to/thumbnail.jpg")

// Apply updates
updater.Update()
```

## Timeline Properties

### Creating Timeline
```go
timeline := media.NewSystemMediaTransportControlsTimelineProperties()
```

### Setting Timeline Values
```go
timeline.SetStartTime(time.Duration(0))                    // Start position
timeline.SetEndTime(time.Duration(180 * time.Second))     // Total duration
timeline.SetPosition(time.Duration(45 * time.Second))     // Current position
timeline.SetMinSeekTime(time.Duration(0))                 // Minimum seek position
timeline.SetMaxSeekTime(time.Duration(180 * time.Second)) // Maximum seek position

controls.SetTimelineProperties(timeline)
```

## Event Handlers

### Button Pressed Event
```go
// Register for button press events
controls.AddButtonPressedHandler(func(button media.SystemMediaTransportControlsButton) {
    switch button {
    case media.SystemMediaTransportControlsButtonPlay:
        // Handle play button
        startPlayback()
    case media.SystemMediaTransportControlsButtonPause:
        // Handle pause button
        pausePlayback()
    case media.SystemMediaTransportControlsButtonStop:
        // Handle stop button
        stopPlayback()
    }
})
```

## Constants

### MediaPlaybackStatus Enum
```go
const (
    MediaPlaybackStatusClosed  = 0
    MediaPlaybackStatusOpened  = 1
    MediaPlaybackStatusPlaying = 2
    MediaPlaybackStatusPaused  = 3
    MediaPlaybackStatusStopped = 4
)
```

### MediaPlaybackType Enum
```go
const (
    MediaPlaybackTypeUnknown = 0
    MediaPlaybackTypeMusic   = 1
    MediaPlaybackTypeVideo   = 2
    MediaPlaybackTypeImage   = 3
)
```

## Error Types

### Common Errors
- **COM initialization failures**: Happen when COM runtime isn't properly initialized
- **Access denied**: May occur when trying to access system media controls without proper permissions
- **Not supported**: Some features may not be available on older Windows versions
- **Invalid arguments**: Providing invalid values to API functions

### Error Handling Pattern
```go
if err != nil {
    // Check for specific error types
    if ole.IsEqual(err, E_ACCESSDENIED) {
        log.Println("Access denied - check permissions")
    } else if ole.IsEqual(err, E_NOTIMPL) {
        log.Println("Feature not supported on this Windows version")
    } else {
        log.Printf("Unexpected error: %v", err)
    }
    return err
}
```