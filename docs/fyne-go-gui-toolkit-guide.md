# Fyne Go GUI Toolkit: Comprehensive Guide

## Overview

**Fyne** is a cross-platform GUI toolkit written in Go that enables developers to build beautiful, efficient applications for desktop, mobile, and web platforms. With its simple API and Material Design-inspired components, Fyne makes it easy to create native applications that run on Windows, macOS, Linux, Android, and iOS from a single codebase.

**Key Features:**
- **Cross-platform**: Single codebase compiles to Windows, macOS, Linux, Android, iOS, and Web
- **Pure Go**: No external dependencies or C bindings required
- **Material Design**: Built-in widgets follow Material Design principles
- **High Performance**: Efficient rendering with hardware acceleration
- **Widget Library**: Comprehensive set of UI components (buttons, forms, lists, tables, etc.)
- **Data Binding**: Reactive UI updates with built-in data binding
- **Theming**: Extensive theming and customization support
- **Responsive Layout**: Automatic adaptation to different screen sizes

## Installation and Setup

### Prerequisites

- **Go 1.16+** (for Go install commands)
- **Git** (for cloning repositories)
- **Docker** (optional, for cross-compilation)

### Basic Installation

Install the Fyne module and command-line tools:

```bash
# Install the Fyne module
go get fyne.io/fyne/v2@latest

# Install the Fyne command-line tool
go install fyne.io/tools/cmd/fyne@latest

# Install the demo application (optional)
go install fyne.io/demo@latest
demo
```

### Cross-Compilation Setup

For building applications on different platforms, install additional tools:

```bash
# Install fyne-cross for cross-compilation
go install github.com/fyne-io/fyne-cross@latest

# Clone and set up examples
git clone https://github.com/fyne-io/examples.git
cd examples
```

## Quick Start: Your First Fyne App

### Hello World Application

Create a minimal Fyne application:

```go
package main

import (
    "fyne.io/fyne/v2/app"
    "fyne.io/fyne/v2/widget"
)

func main() {
    // Create a new application
    a := app.New()

    // Create a new window
    w := a.NewWindow("Hello World")

    // Set window content
    w.SetContent(widget.NewLabel("Hello World!"))

    // Show and run the application
    w.ShowAndRun()
}
```

### Interactive Application

Create an application with user interaction:

```go
package main

import (
    "fyne.io/fyne/v2/app"
    "fyne.io/fyne/v2/container"
    "fyne.io/fyne/v2/widget"
)

func main() {
    a := app.New()
    w := a.NewWindow("Hello")

    // Create a label
    hello := widget.NewLabel("Hello Fyne!")

    // Create content container with vertical layout
    w.SetContent(container.NewVBox(
        hello,
        widget.NewButton("Hi!", func() {
            hello.SetText("Welcome :)")
        }),
    ))

    w.ShowAndRun()
}
```

## Core Concepts

### Application Lifecycle

1. **App Creation**: `app.New()` initializes the application
2. **Window Creation**: `a.NewWindow("Title")` creates windows
3. **Content Setup**: `w.SetContent()` sets UI content
4. **Display**: `w.ShowAndRun()` starts the event loop

### Widgets Overview

Fyne provides a comprehensive set of built-in widgets:

#### Basic Widgets

- **Label**: Display text
- **Button**: Clickable buttons
- **Entry**: Text input fields
- **Icon**: Display icons

#### Choice Widgets

- **Check**: Boolean toggle with label
- **RadioGroup**: Single selection from options
- **Select**: Dropdown selection menu

#### Data Display Widgets

- **List**: Efficient vertical list display
- **Table**: Two-dimensional data table
- **Tree**: Hierarchical data display
- **Progress Bar/Progress Bar Infinite**: Progress indication

#### Container Widgets

- **VBox**: Vertical layout container
- **HBox**: Horizontal layout container
- **Border**: Border layout with center content
- **Grid**: Grid layout container

## Widget Reference

### Labels and Text

#### Basic Label

```go
label := widget.NewLabel("Hello World")
```

#### Rich Text with Formatting

```go
richText := widget.NewRichTextWithText("This is **bold** text and this is *italic*.")
```

### Buttons

#### Text Button

```go
button := widget.NewButton("Click Me", func() {
    fmt.Println("Button clicked!")
})
```

#### Icon Button

```go
import "fyne.io/fyne/v2/theme"

iconButton := widget.NewButtonWithIcon("Save", theme.DocumentSaveIcon(), func() {
    fmt.Println("Save action")
})
```

#### Button Importance

```go
importantButton := widget.NewButton("Delete", func() {})
importantButton.Importance = widget.HighImportance  // Red highlighting
```

### Text Input

#### Basic Entry

```go
entry := widget.NewEntry()
entry.SetPlaceHolder("Enter text here...")
entry.OnChanged = func(text string) {
    fmt.Println("Text changed:", text)
}
```

#### Password Entry

```go
passwordEntry := widget.NewPasswordEntry()
passwordEntry.SetPlaceHolder("Password")
```

#### Multi-line Entry

```go
multilineEntry := widget.NewMultiLineEntry()
multilineEntry.SetPlaceHolder("Enter description...")
multilineEntry.Wrapping = fyne.TextWrapWord
```

#### Entry with Validation

```go
import "regexp"

emailEntry := widget.NewEntry()
emailEntry.SetPlaceHolder("email@example.com")
emailEntry.Validator = func(text string) error {
    emailRegex := regexp.MustCompile(`^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$`)
    if !emailRegex.MatchString(text) {
        return fmt.Errorf("invalid email format")
    }
    return nil
}
```

### Choice Widgets

#### Checkbox

```go
checkbox := widget.NewCheck("Enable Feature", func(checked bool) {
    fmt.Println("Feature enabled:", checked)
})
```

#### Radio Group

```go
radio := widget.NewRadioGroup([]string{"Option 1", "Option 2", "Option 3"}, func(selected string) {
    fmt.Println("Selected:", selected)
})
```

#### Select Dropdown

```go
select := widget.NewSelect([]string{"Item 1", "Item 2", "Item 3"}, func(selected string) {
    fmt.Println("Selected:", selected)
})
```

### Data Display Widgets

#### List Widget

```go
items := []string{"Item 1", "Item 2", "Item 3", "Item 4", "Item 5"}

list := widget.NewList(
    func() int { return len(items) },  // Length function
    func() fyne.CanvasObject { return widget.NewLabel("Template") },  // Create template
    func(i widget.ListItemID, o fyne.CanvasObject) {  // Update function
        label := o.(*widget.Label)
        label.SetText(items[i])
    },
)
```

#### Table Widget

```go
// 2D data structure
data := [][]string{
    {"Name", "Age", "City"},
    {"Alice", "30", "New York"},
    {"Bob", "25", "San Francisco"},
    {"Charlie", "35", "Chicago"},
}

table := widget.NewTable(
    func() (int, int) { return len(data), len(data[0]) },  // Size function
    func() fyne.CanvasObject { return widget.NewLabel("Cell") },  // Create template
    func(i widget.TableCellID, o fyne.CanvasObject) {  // Update function
        label := o.(*widget.Label)
        label.SetText(data[i.Row][i.Col])
    },
)
```

#### Tree Widget

```go
// Hierarchical data structure
data := map[string][]string{
    "":        {"Documents", "Pictures", "Music"},
    "Documents": {"Work", "Personal", "Archive"},
    "Work":      {"Projects", "Reports"},
    "Pictures":  {"Vacation", "Family"},
}

tree := widget.NewTree(
    func(uid string) []string { return data[uid] },  // ChildUIDs function
    func(uid string) bool {  // IsBranch function
        children, ok := data[uid]
        return ok && len(children) > 0
    },
    func(branch bool) fyne.CanvasObject {  // CreateNode function
        return container.NewHBox(
            widget.NewIcon(theme.FolderIcon()),
            widget.NewLabel("Template"),
        )
    },
    func(uid string, branch bool, obj fyne.CanvasObject) {  // UpdateNode function
        c := obj.(*fyne.Container)
        icon := c.Objects[0].(*widget.Icon)
        label := c.Objects[1].(*widget.Label)

        label.SetText(uid)
        if branch {
            icon.SetResource(theme.FolderIcon())
        } else {
            icon.SetResource(theme.DocumentIcon())
        }
    },
)
```

### Progress Indicators

#### Standard Progress Bar

```go
progressBar := widget.NewProgressBar()
progressBar.SetValue(0.75)  // 75% complete
```

#### Infinite Progress Bar

```go
infiniteProgress := widget.NewProgressBarInfinite()
infiniteProgress.Start()

// Later, stop the animation
infiniteProgress.Stop()
```

## Layout Management

### Basic Layouts

#### Vertical Box (VBox)

```go
content := container.NewVBox(
    widget.NewLabel("First"),
    widget.NewLabel("Second"),
    widget.NewLabel("Third"),
)
```

#### Horizontal Box (HBox)

```go
content := container.NewHBox(
    widget.NewButton("Left", func() {}),
    widget.NewLabel("Center"),
    widget.NewButton("Right", func() {}),
)
```

#### Border Layout

```go
content := container.NewBorder(
    widget.NewLabel("Top"),     // top
    widget.NewLabel("Bottom"),  // bottom
    widget.NewLabel("Left"),    // left
    widget.NewLabel("Right"),   // right
    widget.NewLabel("Center"),  // center
)
```

#### Grid Layout

```go
content := container.NewGridWithColumns(2,
    widget.NewLabel("Name:"), widget.NewEntry(),
    widget.NewLabel("Email:"), widget.NewEntry(),
    widget.NewLabel("Phone:"), widget.NewEntry(),
)
```

### Advanced Layouts

#### Form Layout

```go
form := container.NewVBox(
    widget.NewCard("Personal Information", "", container.NewVBox(
        widget.NewLabel("Name:"),
        widget.NewEntry(),
        widget.NewLabel("Email:"),
        widget.NewEntry(),
    )),
    widget.NewCard("Preferences", "", container.NewVBox(
        widget.NewCheck("Enable notifications", nil),
        widget.NewCheck("Auto-save", nil),
    )),
)
```

#### Split Container

```go
split := container.NewHSplit(
    widget.NewLabel("Left Panel"),
    widget.NewLabel("Right Panel"),
)
split.Resize(fyne.NewSize(400, 300))
```

## Menus and Toolbars

### Application Menu

```go
import (
    "fyne.io/fyne/v2"
    "fyne.io/fyne/v2/dialog"
)

// Create menus
fileMenu := fyne.NewMenu("File",
    fyne.NewMenuItem("New", func() {
        fmt.Println("New file")
    }),
    fyne.NewMenuItem("Open", func() {
        fmt.Println("Open file")
    }),
    fyne.NewMenuItemSeparator(),
    fyne.NewMenuItem("Quit", func() {
        a.Quit()
    }),
)

editMenu := fyne.NewMenu("Edit",
    fyne.NewMenuItem("Cut", func() { fmt.Println("Cut") }),
    fyne.NewMenuItem("Copy", func() { fmt.Println("Copy") }),
    fyne.NewMenuItem("Paste", func() { fmt.Println("Paste") }),
)

helpMenu := fyne.NewMenu("Help",
    fyne.NewMenuItem("About", func() {
        dialog.ShowInformation("About", "My App v1.0", w)
    }),
)

// Set main menu
mainMenu := fyne.NewMainMenu(fileMenu, editMenu, helpMenu)
w.SetMainMenu(mainMenu)
```

### Toolbar

```go
toolbar := widget.NewToolbar(
    widget.NewToolbarAction(theme.DocumentCreateIcon(), func() {
        fmt.Println("New document")
    }),
    widget.NewToolbarAction(theme.FolderOpenIcon(), func() {
        fmt.Println("Open folder")
    }),
    widget.NewToolbarSeparator(),
    widget.NewToolbarAction(theme.ContentCutIcon(), func() {
        fmt.Println("Cut")
    }),
    widget.NewToolbarSpacer(),  // Pushes following items to the right
    widget.NewToolbarAction(theme.SettingsIcon(), func() {
        fmt.Println("Settings")
    }),
)

// Add toolbar to window
content := container.NewBorder(
    toolbar,  // top
    nil,      // bottom
    nil,      // left
    nil,      // right
    widget.NewLabel("Main content"),  // center
)
w.SetContent(content)
```

## Data Binding

### Basic Data Binding

```go
import "fyne.io/fyne/v2/data/binding"

// Create bound data
boundString := binding.NewString()
boundString.Set("Initial value")

// Bind to widgets
entry := widget.NewEntryWithData(boundString)
label := widget.NewLabelWithData(boundString)

// Programmatically update
boundString.Set("New value")
```

### Advanced Data Binding

```go
// Different data types
boundString := binding.NewString()
boundInt := binding.NewInt()
boundFloat := binding.NewFloat()
boundBool := binding.NewBool()

// Type conversion bindings
intEntry := widget.NewEntryWithData(binding.IntToString(boundInt))
floatEntry := widget.NewEntryWithData(binding.FloatToString(boundFloat))
boolLabel := widget.NewLabelWithData(binding.BoolToString(boundBool))
boolCheck := widget.NewCheckWithData("Enable", boundBool)

// Listen for changes
boundString.AddListener(binding.NewDataListener(func() {
    val, _ := boundString.Get()
    fmt.Println("String changed to:", val)
}))
```

## Custom Themes

### Basic Theme Implementation

```go
import (
    "image/color"
    "fyne.io/fyne/v2"
    "fyne.io/fyne/v2/theme"
)

type customTheme struct{}

func (m customTheme) Color(name fyne.ThemeColorName, variant fyne.ThemeVariant) color.Color {
    switch name {
    case theme.ColorNameBackground:
        return color.RGBA{R: 30, G: 30, B: 46, A: 255}  // Dark blue background
    case theme.ColorNameButton:
        return color.RGBA{R: 137, G: 180, B: 250, A: 255}  // Light blue buttons
    case theme.ColorNameForeground:
        return color.RGBA{R: 205, G: 214, B: 244, A: 255}  // Light text
    case theme.ColorNamePrimary:
        return color.RGBA{R: 203, G: 166, B: 247, A: 255}  // Purple accent
    default:
        return theme.DefaultTheme().Color(name, variant)
    }
}

func (m customTheme) Font(style fyne.TextStyle) fyne.Resource {
    return theme.DefaultTheme().Font(style)
}

func (m customTheme) Icon(name fyne.ThemeIconName) fyne.Resource {
    return theme.DefaultTheme().Icon(name)
}

func (m customTheme) Size(name fyne.ThemeSizeName) float32 {
    switch name {
    case theme.SizeNamePadding:
        return 8
    case theme.SizeNameText:
        return 14
    default:
        return theme.DefaultTheme().Size(name)
    }
}

// Apply theme
a := app.New()
a.Settings().SetTheme(&customTheme{})
```

### Theme Switching

```go
// Theme selector
themeSelector := widget.NewSelect(
    []string{"Light", "Dark", "Custom"},
    func(selected string) {
        switch selected {
        case "Light":
            a.Settings().SetTheme(theme.LightTheme())
        case "Dark":
            a.Settings().SetTheme(theme.DarkTheme())
        case "Custom":
            a.Settings().SetTheme(&customTheme{})
        }
    },
)
```

## Multi-window Applications

```go
package main

import (
    "fyne.io/fyne/v2"
    "fyne.io/fyne/v2/app"
    "fyne.io/fyne/v2/widget"
)

func main() {
    a := app.New()

    // Main window
    w1 := a.NewWindow("Main Window")
    w1.SetContent(widget.NewLabel("Main Application"))

    // Secondary window
    w2 := a.NewWindow("Secondary Window")
    w2.SetContent(widget.NewLabel("Additional Window"))
    w2.Resize(fyne.NewSize(300, 200))

    // Show both windows
    w1.Show()
    w2.Show()

    a.Run()
}
```

## Advanced Features

### Goroutines and UI Updates

```go
package main

import (
    "image/color"
    "time"
    "fyne.io/fyne/v2"
    "fyne.io/fyne/v2/app"
    "fyne.io/fyne/v2/canvas"
)

func main() {
    a := app.New()
    w := a.NewWindow("Clock")

    // Create clock display
    clock := canvas.NewText(time.Now().Format(time.TimeOnly), color.NRGBA{G: 0xff, A: 0xff})
    clock.TextStyle.Monospace = true
    clock.TextSize = 32
    w.SetContent(clock)

    // Update clock in goroutine
    go func() {
        ticker := time.NewTicker(time.Second)
        for range ticker.C {
            fyne.Do(func() {  // Safe UI update
                clock.Text = time.Now().Format(time.TimeOnly)
                clock.Refresh()
            })
        }
    }()

    w.ShowAndRun()
}
```

### File Dialogs

```go
import "fyne.io/fyne/v2/dialog"

// Open file dialog
dialog.ShowFileOpen(func(reader fyne.URIReadCloser, err error) {
    if err == nil && reader != nil {
        defer reader.Close()
        // Process file
        fmt.Println("File opened:", reader.URI().Path())
    }
}, w)

// Save file dialog
dialog.ShowFileSave(func(writer fyne.URIWriteCloser, err error) {
    if err == nil && writer != nil {
        defer writer.Close()
        // Save file
        fmt.Println("File saved to:", writer.URI().Path())
    }
}, w)

// Directory dialog
dialog.ShowFolderOpen(func(uri fyne.ListableURI, err error) {
    if err == nil && uri != nil {
        fmt.Println("Directory selected:", uri.Path())
    }
}, w)
```

### Confirmation and Information Dialogs

```go
// Information dialog
dialog.ShowInformation("Success", "Operation completed successfully", w)

// Error dialog
dialog.ShowError("An error occurred", w)

// Confirmation dialog
dialog.ShowConfirm("Confirm", "Are you sure you want to delete this item?", func(confirmed bool) {
    if confirmed {
        fmt.Println("User confirmed")
    } else {
        fmt.Println("User cancelled")
    }
}, w)

// Custom dialog
content := widget.NewEntry()
dialog.ShowCustom("Custom Dialog", "OK", content, func() {
    fmt.Println("User entered:", content.Text)
}, w)
```

## Building and Deployment

### Building for Current Platform

```bash
# Build for current platform
go build -o myapp

# Run the application
./myapp
```

### Cross-Compilation with Fyne Tools

```bash
# Install fyne-cross if not already installed
go install github.com/fyne-io/fyne-cross@latest

# Build for Linux
fyne-cross linux -name myapp

# Build for Windows
fyne-cross windows -name myapp

# Build for macOS
fyne-cross darwin -name myapp

# Build for ARM (Raspberry Pi)
fyne-cross linux -arch arm64 -name myapp

# Build with specific output directory
fyne-cross linux -output ./builds/myapp

# Build specific example
fyne-cross linux -output bugs ./cmd/bugs
```

### Mobile Development

#### Android

```bash
# Install Android requirements
# (Android Studio, SDK, NDK)

# Build Android APK
fyne package -os android

# Install to connected device
fyne install -os android
```

#### iOS

```bash
# Install Xcode and iOS requirements

# Build iOS app
fyne package -os ios

# Install to connected device/simulator
fyne install -os ios
```

### Web Assembly (WASM)

```bash
# Enable GOOS=js and GOARCH=wasm
GOOS=js GOARCH=wasm go build -o main.wasm

# Copy necessary support files
cp "$(go env GOROOT)/misc/wasm/wasm_exec.js" .
```

## Testing Fyne Applications

### Unit Testing with Test App

```go
package main

import (
    "testing"
    "fyne.io/fyne/v2/test"
    "fyne.io/fyne/v2/widget"
)

func TestButtonTap(t *testing.T) {
    button := widget.NewButton("Test", func() {
        // Button action
    })

    // Test button tap
    test.Tap(button)

    // Verify state
    if button.Text != "Test" {
        t.Errorf("Expected button text 'Test', got '%s'", button.Text)
    }
}

func TestWindowContent(t *testing.T) {
    app := test.NewApp()
    window := app.NewWindow("Test")

    label := widget.NewLabel("Hello")
    window.SetContent(label)

    // Test window content
    content := window.Content()
    if content != label {
        t.Error("Window content does not match expected label")
    }
}
```

### Widget Testing

```go
func TestEntryValidation(t *testing.T) {
    entry := widget.NewEntry()

    // Test empty entry
    if entry.Text != "" {
        t.Error("Entry should start empty")
    }

    // Test text input
    test.Type(entry, "test input")

    if entry.Text != "test input" {
        t.Errorf("Expected 'test input', got '%s'", entry.Text)
    }
}
```

## Performance Optimization

### Efficient List Implementation

```go
// For large datasets, use efficient caching
list := widget.NewList(
    func() int { return len(largeDataset) },
    func() fyne.CanvasObject {
        // Create reusable template
        return container.NewVBox(
            widget.NewIcon(theme.DocumentIcon()),
            widget.NewLabel("Template"),
        )
    },
    func(i widget.ListItemID, o fyne.CanvasObject) {
        // Efficiently update existing objects
        c := o.(*fyne.Container)
        label := c.Objects[1].(*widget.Label)
        label.SetText(largeDataset[i])
    },
)
```

### Resource Management

```go
// Preload and cache resources
var cachedIcon fyne.Resource

func getCachedIcon() fyne.Resource {
    if cachedIcon == nil {
        cachedIcon = theme.HomeIcon()
    }
    return cachedIcon
}

// Use cached icon
icon := widget.NewIcon(getCachedIcon())
```

## Troubleshooting

### Common Issues

#### Build Errors

```bash
# Ensure Go version is up to date
go version

# Clean module cache
go clean -modcache

# Update dependencies
go mod tidy
go mod download
```

#### Cross-Compilation Issues

```bash
# Check required compilers
go tool dist list

# Install missing compilers (Ubuntu/Debian)
sudo apt-get install gcc-aarch64-linux-gnu gcc-x86-64-linux-gnu

# Set environment variables
export CGO_ENABLED=1
export CC=aarch64-linux-gnu-gcc  # for ARM64
```

#### Runtime Issues

```bash
# Enable debug logging
export FYNE_DEBUG=1

# Check for missing libraries (Linux)
ldd ./myapp

# Install missing GUI libraries
sudo apt-get install libgl1-mesa-glx libx11-6
```

### Getting Help

- **Documentation**: [https://docs.fyne.io](https://docs.fyne.io)
- **GitHub Repository**: [https://github.com/fyne-io/fyne](https://github.com/fyne-io/fyne)
- **Community Forum**: [https://forum.fyne.io](https://forum.fyne.io)
- **Discord**: [https://discord.gg/6QryBwD](https://discord.gg/6QryBwD)

## Best Practices

1. **Use Appropriate Layouts**: Choose the right container for your UI structure
2. **Implement Proper Data Binding**: Use reactive patterns for dynamic UIs
3. **Test Thoroughly**: Leverage Fyne's testing package
4. **Optimize for Performance**: Use efficient patterns for large datasets
5. **Follow Material Design**: Leverage built-in theming and design principles
6. **Handle Errors Gracefully**: Implement proper error handling and user feedback
7. **Use Responsive Design**: Ensure your app works on different screen sizes
8. **Document Your Code**: Add comments and documentation for complex UI logic

## Next Steps

- Explore the **[Fyne Demo Application](https://github.com/fyne-io/fyne-demo)** for comprehensive examples
- Check out **[Fyne Examples Repository](https://github.com/fyne-io/examples)** for specific implementations
- Read the **[Official Documentation](https://docs.fyne.io)** for detailed API reference
- Join the **[Community](https://forum.fyne.io)** for support and discussions
- Contribute to the **[Open Source Project](https://github.com/fyne-io/fyne)**

---

This comprehensive guide covers the essential aspects of Fyne GUI development with Go. From basic setup to advanced features like theming, data binding, and cross-platform deployment, you now have the knowledge to create beautiful, cross-platform applications using the Fyne toolkit.