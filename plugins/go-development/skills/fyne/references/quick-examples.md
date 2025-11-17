# Fyne Quick Examples

## Basic Application

```go
package main

import (
    "fyne.io/fyne/v2/app"
    "fyne.io/fyne/v2/widget"
)

func main() {
    a := app.New()
    w := a.NewWindow("Hello")

    w.SetContent(widget.NewLabel("Hello Fyne!"))
    w.ShowAndRun()
}
```

## Interactive Application

```go
package main

import (
    "fyne.io/fyne/v2/app"
    "fyne.io/fyne/v2/container"
    "fyne.io/fyne/v2/widget"
)

func main() {
    a := app.New()
    w := a.NewWindow("Interactive")

    hello := widget.NewLabel("Hello Fyne!")
    w.SetContent(container.NewVBox(
        hello,
        widget.NewButton("Hi!", func() {
            hello.SetText("Welcome :)")
        }),
    ))

    w.ShowAndRun()
}
```

## Layout Examples

### Vertical Layout

```go
func verticalLayout() fyne.CanvasObject {
    return container.NewVBox(
        widget.NewLabel("First"),
        widget.NewLabel("Second"),
        widget.NewLabel("Third"),
    )
}
```

### Horizontal Layout

```go
func horizontalLayout() fyne.CanvasObject {
    return container.NewHBox(
        widget.NewButton("Left", func() {}),
        widget.NewLabel("Center"),
        widget.NewButton("Right", func() {}),
    )
}
```

### Border Layout

```go
func borderLayout() fyne.CanvasObject {
    return container.NewBorder(
        widget.NewLabel("Top"),     // top
        widget.NewLabel("Bottom"),  // bottom
        widget.NewLabel("Left"),    // left
        widget.NewLabel("Right"),   // right
        widget.NewLabel("Center"),  // center
    )
}
```

### Grid Layout

```go
func gridLayout() fyne.CanvasObject {
    return container.NewGridWithColumns(2,
        widget.NewLabel("Name:"), widget.NewEntry(),
        widget.NewLabel("Email:"), widget.NewEntry(),
        widget.NewLabel("Phone:"), widget.NewEntry(),
    )
}
```

## Form Controls

### Entry Widget

```go
func entryExample() fyne.CanvasObject {
    nameEntry := widget.NewEntry()
    nameEntry.SetPlaceHolder("Enter your name")

    passwordEntry := widget.NewPasswordEntry()
    passwordEntry.SetPlaceHolder("Password")

    multilineEntry := widget.NewMultiLineEntry()
    multilineEntry.SetPlaceHolder("Enter description...")

    return container.NewVBox(
        widget.NewLabel("Name:"), nameEntry,
        widget.NewLabel("Password:"), passwordEntry,
        widget.NewLabel("Description:"), multilineEntry,
    )
}
```

### Choice Widgets

```go
func choiceWidgets() fyne.CanvasObject {
    checkbox := widget.NewCheck("Enable notifications", nil)
    radio := widget.NewRadioGroup([]string{"Option 1", "Option 2"}, nil)
    select := widget.NewSelect([]string{"Choice 1", "Choice 2", "Choice 3"}, nil)

    return container.NewVBox(
        checkbox,
        radio,
        select,
    )
}
```

### Button Variants

```go
func buttonExamples() fyne.CanvasObject {
    import "fyne.io/fyne/v2/theme"

    return container.NewVBox(
        widget.NewButton("Standard", func() {}),
        widget.NewButtonWithIcon("With Icon", theme.HomeIcon(), func() {}),
        func() fyne.CanvasObject {
            btn := widget.NewButton("Important", func() {})
            btn.Importance = widget.HighImportance
            return btn
        }(),
        func() fyne.CanvasObject {
            btn := widget.NewButton("Disabled", func() {})
            btn.Disable()
            return btn
        }(),
    )
}
```

## Data Display

### List Widget

```go
func listExample() fyne.CanvasObject {
    items := []string{"Item 1", "Item 2", "Item 3", "Item 4", "Item 5"}

    list := widget.NewList(
        func() int { return len(items) },
        func() fyne.CanvasObject { return widget.NewLabel("Template") },
        func(i widget.ListItemID, o fyne.CanvasObject) {
            label := o.(*widget.Label)
            label.SetText(items[i])
        },
    )

    return list
}
```

### Table Widget

```go
func tableExample() fyne.CanvasObject {
    data := [][]string{
        {"Name", "Age", "City"},
        {"Alice", "30", "New York"},
        {"Bob", "25", "San Francisco"},
    }

    table := widget.NewTable(
        func() (int, int) { return len(data), len(data[0]) },
        func() fyne.CanvasObject { return widget.NewLabel("Cell") },
        func(i widget.TableCellID, o fyne.CanvasObject) {
            label := o.(*widget.Label)
            label.SetText(data[i.Row][i.Col])
        },
    )

    return table
}
```

### Progress Bar

```go
func progressExample() fyne.CanvasObject {
    progressBar := widget.NewProgressBar()
    progressBar.SetValue(0.75)  // 75% complete

    infiniteProgress := widget.NewProgressBarInfinite()
    infiniteProgress.Start()

    return container.NewVBox(
        progressBar,
        infiniteProgress,
    )
}
```

## Menus and Toolbars

### Application Menu

```go
func setupMenu(a fyne.App, w fyne.Window) {
    fileMenu := fyne.NewMenu("File",
        fyne.NewMenuItem("New", func() { /* new file */ }),
        fyne.NewMenuItem("Open", func() { /* open file */ }),
        fyne.NewMenuItemSeparator(),
        fyne.NewMenuItem("Quit", func() { a.Quit() }),
    )

    helpMenu := fyne.NewMenu("Help",
        fyne.NewMenuItem("About", func() { /* about dialog */ }),
    )

    mainMenu := fyne.NewMainMenu(fileMenu, helpMenu)
    w.SetMainMenu(mainMenu)
}
```

### Toolbar

```go
import "fyne.io/fyne/v2/theme"

func toolbarExample() fyne.CanvasObject {
    return widget.NewToolbar(
        widget.NewToolbarAction(theme.DocumentCreateIcon(), func() { /* new */ }),
        widget.NewToolbarAction(theme.FolderOpenIcon(), func() { /* open */ }),
        widget.NewToolbarSeparator(),
        widget.NewToolbarAction(theme.ContentCutIcon(), func() { /* cut */ }),
        widget.NewToolbarSpacer(),
        widget.NewToolbarAction(theme.SettingsIcon(), func() { /* settings */ }),
    )
}
```

## Data Binding

### Basic Binding

```go
import "fyne.io/fyne/v2/data/binding"

func dataBindingExample() fyne.CanvasObject {
    // Create bound data
    boundString := binding.NewString()
    boundString.Set("Initial value")

    // Bind to widgets
    entry := widget.NewEntryWithData(boundString)
    label := widget.NewLabelWithData(boundString)

    // Programmatically update
    button := widget.NewButton("Update", func() {
        boundString.Set("New value")
    })

    return container.NewVBox(entry, label, button)
}
```

### Type Conversions

```go
func typeConversions() fyne.CanvasObject {
    boundInt := binding.NewInt()
    boundFloat := binding.NewFloat()
    boundBool := binding.NewBool()

    // Convert to string for display
    intEntry := widget.NewEntryWithData(binding.IntToString(boundInt))
    floatEntry := widget.NewEntryWithData(binding.FloatToString(boundFloat))
    boolLabel := widget.NewLabelWithData(binding.BoolToString(boundBool))
    boolCheck := widget.NewCheckWithData("Enable", boundBool)

    return container.NewVBox(
        intEntry, floatEntry, boolLabel, boolCheck,
    )
}
```

## Custom Themes

```go
import "image/color"

type customTheme struct{}

func (m customTheme) Color(name fyne.ThemeColorName, variant fyne.ThemeVariant) color.Color {
    switch name {
    case theme.ColorNameBackground:
        return color.RGBA{R: 30, G: 30, B: 46, A: 255}
    case theme.ColorNameButton:
        return color.RGBA{R: 137, G: 180, B: 250, A: 255}
    case theme.ColorNameForeground:
        return color.RGBA{R: 205, G: 214, B: 244, A: 255}
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

func applyTheme(a fyne.App) {
    a.Settings().SetTheme(&customTheme{})
}
```

## Dialogs

```go
import "fyne.io/fyne/v2/dialog"

func dialogExamples(w fyne.Window) {
    // Information dialog
    dialog.ShowInformation("Success", "Operation completed!", w)

    // Error dialog
    dialog.ShowError("An error occurred", w)

    // Confirmation dialog
    dialog.ShowConfirm("Confirm", "Are you sure?", func(confirmed bool) {
        if confirmed {
            // User confirmed
        }
    }, w)

    // File dialog
    dialog.ShowFileOpen(func(reader fyne.URIReadCloser, err error) {
        if err == nil && reader != nil {
            defer reader.Close()
            // Process file
        }
    }, w)

    // File save dialog
    dialog.ShowFileSave(func(writer fyne.URIWriteCloser, err error) {
        if err == nil && writer != nil {
            defer writer.Close()
            // Save file
        }
    }, w)
}
```

## Multiple Windows

```go
func multiWindowExample(a fyne.App) {
    // Main window
    w1 := a.NewWindow("Main")
    w1.SetContent(widget.NewLabel("Main Application"))
    w1.Show()

    // Secondary window
    w2 := a.NewWindow("Secondary")
    w2.SetContent(widget.NewLabel("Additional Window"))
    w2.Resize(fyne.NewSize(300, 200))
    w2.Show()

    a.Run()
}
```

## Async Operations

```go
import "fyne.io/fyne/v2/canvas"

func asyncExample() fyne.CanvasObject {
    // Create text for clock display
    clock := canvas.NewText(time.Now().Format(time.TimeOnly), color.NRGBA{G: 0xff, A: 0xff})
    clock.TextStyle.Monospace = true
    clock.TextSize = 32

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

    return clock
}
```