# Fyne Widget Reference

## Overview

Fyne provides a comprehensive set of widgets following Material Design principles. All widgets implement the `fyne.CanvasObject` interface.

## Basic Widgets

### Label

Display text with optional styling.

```go
widget.NewLabel("Hello World")
widget.NewLabelWithStyle("Styled", fyne.TextAlignCenter, fyne.TextStyleBold)
```

**Methods:**
- `SetText(string)` - Update label text
- `GetText() string` - Get current text
- `Wrapping` - Set text wrapping behavior

### Button

Clickable button with text and optional icon.

```go
widget.NewButton("Click Me", func() { /* handle click */ })
widget.NewButtonWithIcon("Save", theme.DocumentSaveIcon(), func() { /* save */ })
```

**Properties:**
- `Text` - Button text
- `Icon` - Button icon (optional)
- `Importance` - Button visual importance (widget.LowImportance, widget.MediumImportance, widget.HighImportance)
- `Disabled` - Enable/disable button

### Entry

Text input field for single-line or multi-line input.

```go
// Single line
entry := widget.NewEntry()
entry.SetPlaceHolder("Enter text here")

// Password
passwordEntry := widget.NewPasswordEntry()

// Multi-line
multilineEntry := widget.NewMultiLineEntry()
multilineEntry.Wrapping = fyne.TextWrapWord
```

**Properties:**
- `Text` - Current text content
- `PlaceHolder` - Placeholder text when empty
- `OnChanged` - Callback for text changes
- `Validator` - Input validation function
- `MultiLine` - Enable multi-line input
- `Password` - Hide text input for passwords
- `Wrapping` - Text wrapping behavior

## Choice Widgets

### Check

Boolean toggle with text label.

```go
check := widget.NewCheck("Enable notifications", func(checked bool) {
    fmt.Printf("Notifications: %t\n", checked)
})
```

**Properties:**
- `Checked` - Current boolean state
- `OnChanged` - Callback for state changes

### Radio Group

Single selection from multiple options.

```go
radio := widget.NewRadioGroup([]string{"Option 1", "Option 2", "Option 3"}, func(selected string) {
    fmt.Printf("Selected: %s\n", selected)
})
radio.SetSelected("Option 1")  // Set default selection
```

**Properties:**
- `Options` - Available options
- `Selected` - Currently selected option
- `Required` - Whether selection is required
- `OnChanged` - Callback for selection changes

### Select

Dropdown menu for selecting from options.

```go
select := widget.NewSelect([]string{"Choice 1", "Choice 2", "Choice 3"}, func(selected string) {
    fmt.Printf("Selected: %s\n", selected)
})
select.SetSelected("Choice 1")  // Set default
```

**Properties:**
- `Options` - Dropdown options
- `Selected` - Currently selected option
- `PlaceHolder` - Placeholder text when no selection
- `OnChanged` - Callback for selection changes

## Data Display Widgets

### List

Efficient vertical list for displaying large datasets.

```go
items := []string{"Item 1", "Item 2", "Item 3"}

list := widget.NewList(
    func() int { return len(items) },  // Length function
    func() fyne.CanvasObject { return widget.NewLabel("Template") },  // Create template
    func(i widget.ListItemID, o fyne.CanvasObject) {  // Update function
        label := o.(*widget.Label)
        label.SetText(items[i])
    },
)
```

**Methods:**
- `SetItemLoader(widget.ListItemLoader)` - Update data source
- `Select(id)` - Programmatically select item
- `UnselectAll()` - Clear selection
- `GetSelected() []int` - Get selected indices

### Table

Two-dimensional data display with efficient scrolling.

```go
data := [][]string{
    {"Name", "Age", "City"},
    {"Alice", "30", "New York"},
    {"Bob", "25", "San Francisco"},
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

**Methods:**
- `SetColumnWidth(width)` - Set column width
- `ShowRowAt(row)` - Scroll to specific row
- `ShowColumnAt(col)` - Scroll to specific column

### Tree

Hierarchical data display with expand/collapse functionality.

```go
data := map[string][]string{
    "": {"Documents", "Pictures"},
    "Documents": {"Work", "Personal"},
    "Work": {"Projects", "Reports"},
}

tree := widget.NewTree(
    func(uid string) []string { return data[uid] },  // Children function
    func(uid string) bool {  // IsBranch function
        children, ok := data[uid]
        return ok && len(children) > 0
    },
    func(branch bool) fyne.CanvasObject {  // Create template
        return container.NewHBox(
            widget.NewIcon(theme.FolderIcon()),
            widget.NewLabel("Template"),
        )
    },
    func(uid string, branch bool, obj fyne.CanvasObject) {  // Update function
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

**Methods:**
- `OpenBranch(uid)` - Expand branch
- `CloseBranch(uid)` - Collapse branch
- `ToggleBranch(uid)` - Toggle branch expansion
- `IsBranchOpen(uid)` - Check if branch is open

## Progress Indicators

### ProgressBar

Horizontal progress bar showing completion percentage.

```go
progress := widget.NewProgressBar()
progress.SetValue(0.75)  // 75% complete
```

**Properties:**
- `Value` - Current value (0.0 to 1.0)
- `TextFormatter` - Function to format display text

### ProgressBarInfinite

Indeterminate progress indicator for ongoing operations.

```go
infinite := widget.NewProgressBarInfinite()
infinite.Start()  // Start animation
infinite.Stop()   // Stop animation
```

## Rich Text

### RichText

Display formatted text with markdown support.

```go
richText := widget.NewRichTextWithText("This is **bold** and *italic* text.")

// Programmatically add content
richText.ParseMarkdown("## Header\n- List item\n- Another item")
```

**Properties:**
- `Segments` - Text segments with styling
- `Wrapping` - Text wrapping behavior

## Icon Widget

Display icons from theme resources or custom resources.

```go
// Theme icon
icon := widget.NewIcon(theme.HomeIcon())

// Custom icon (requires fyne.Resource)
customIcon := widget.NewIcon(myCustomIcon)
```

## Form Controls

### Card

Material Design card with optional title and content.

```go
card := widget.NewCard("Title", "Subtitle", widget.NewLabel("Content"))
card.SetContent(widget.NewVBox(/* widgets */))
```

### Accordion

Expandable sections similar to accordion interface.

```go
accordion := widget.NewAccordion(
    widget.NewAccordionItem("Section 1", widget.NewLabel("Content 1")),
    widget.NewAccordionItem("Section 2", widget.NewLabel("Content 2")),
)
```

## Toolbar

Horizontal row of tool buttons and controls.

```go
toolbar := widget.NewToolbar(
    widget.NewToolbarAction(theme.DocumentCreateIcon(), func() { /* new */ }),
    widget.NewToolbarSeparator(),
    widget.NewToolbarAction(theme.ContentCopyIcon(), func() { /* copy */ }),
    widget.NewToolbarSpacer(),
    widget.NewToolbarAction(theme.SettingsIcon(), func() { /* settings */ }),
)
```

**Toolbar Elements:**
- `NewToolbarAction(resource, callback)` - Action button
- `NewToolbarSeparator()` - Visual separator
- `NewToolbarSpacer()` - Flexible spacer

## Split Container

Resizable split view with draggable divider.

```go
split := container.NewHSplit(
    widget.NewLabel("Left"),
    widget.NewLabel("Right"),
)
split.SetRatio(0.3)  // 30% left, 70% right
```

## Pop-up Menus

### Popup Menu

Context menu that appears on right-click or button press.

```go
popupMenu := widget.NewPopUpMenu(
    fyne.CurrentApp().Driver().CanvasForObject(button),
    fyne.NewMenu("",  // Empty title for context menu
        fyne.NewMenuItem("Cut", func() { /* cut */ }),
        fyne.NewMenuItem("Copy", func() { /* copy */ }),
        fyne.NewMenuItem("Paste", func() { /* paste */ }),
    ),
)
```

## Tab Container

Tabbed interface for organizing content.

```go
tabs := container.NewAppTabs(
    container.NewTabItem("Tab 1", widget.NewLabel("Content 1")),
    container.NewTabItemWithIcon("Tab 2", theme.HomeIcon(), widget.NewLabel("Content 2")),
)

// Programmatically select tab
tabs.SelectTabIndex(1)
```

## Common Properties

All widgets share common interface methods:

- `Show()` - Make widget visible
- `Hide()` - Hide widget
- `Enable()` - Enable widget
- `Disable()` - Disable widget
- `Refresh()` - Redraw widget
- `Resize(size)` - Set widget size
- `Move(position)` - Set widget position
- `MinSize()` - Get minimum size

## Event Handling

### Click Events

```go
button := widget.NewButton("Click me", func() {
    fmt.Println("Button clicked!")
})
```

### Text Change Events

```go
entry := widget.NewEntry()
entry.OnChanged = func(text string) {
    fmt.Printf("Text changed to: %s\n", text)
}
```

### Selection Events

```go
select := widget.NewSelect([]string{"A", "B", "C"}, func(selected string) {
    fmt.Printf("Selected: %s\n", selected)
})
```

### Keyboard Shortcuts

```go
canvas := fyne.CurrentApp().Driver().CanvasForObject(window)
canvas.SetOnTypedKey(func(e *fyne.KeyEvent) {
    switch e.Name {
    case fyne.KeyEscape:
        fmt.Println("Escape pressed")
    case fyne.KeyEnter:
        fmt.Println("Enter pressed")
    }
})
```

## Widget Styling

### Custom Colors

```go
label := widget.NewLabel("Colored text")
label.Importance = widget.HighImportance  // Apply theme color importance
```

### Text Styling

```go
boldLabel := widget.NewLabelWithStyle("Bold", fyne.TextAlignCenter, fyne.TextStyleBold)
italicLabel := widget.NewLabelWithStyle("Italic", fyne.TextAlignLeft, fyne.TextStyleItalic)
```

### Icon Styling

```go
icon := widget.NewIcon(theme.HomeIcon())
icon.Resize(fyne.NewSize(32, 32))  // Custom size
```

## Testing Widgets

```go
import "fyne.io/fyne/v2/test"

func TestButtonClick(t *testing.T) {
    clicked := false
    button := widget.NewButton("Test", func() { clicked = true })

    test.Tap(button)

    if !clicked {
        t.Error("Button was not clicked")
    }
}
```