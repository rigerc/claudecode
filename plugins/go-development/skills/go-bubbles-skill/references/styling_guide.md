# Bubbles Component Styling Guide

This comprehensive guide covers styling patterns and techniques for customizing Bubbles components with Lip Gloss to create beautiful and consistent terminal user interfaces.

## Styling Fundamentals

### Basic Style Application

All Bubbles components can be styled using Lip Gloss styles:

```go
import "github.com/charmbracelet/lipgloss"

// Create a style
baseStyle := lipgloss.NewStyle().
    Foreground(lipgloss.Color("255")).
    Background(lipgloss.Color("62")).
    Padding(0, 2).
    Bold(true)

// Apply to component
component.Style = baseStyle
```

### Adaptive Colors

Use adaptive colors for better terminal compatibility:

```go
// Adaptive colors that work in light/dark terminals
adaptiveStyle := lipgloss.NewStyle().
    Foreground(lipgloss.AdaptiveColor{
        Light: "63",  // Purple for light backgrounds
        Dark:  "228", // Pink for dark backgrounds
    })
```

## Component-Specific Styling

### Text Input Styling

```go
// Text input styling
ti := textinput.New()

// Basic styling
ti.Style = lipgloss.NewStyle().
    Foreground(lipgloss.Color("255")).
    Background(lipgloss.Color("237")).
    Border(lipgloss.NormalBorder()).
    BorderForeground(lipgloss.Color("239")).
    Padding(0, 1)

// Focused state styling
ti.CursorStyle = lipgloss.NewStyle().
    Background(lipgloss.Color("62"))

// Placeholder styling
ti.PlaceholderStyle = lipgloss.NewStyle().
    Foreground(lipgloss.Color("240")).
    Italic(true)
```

#### Text Input Themes

```go
// Dark theme
func applyDarkTheme(ti *textinput.Model) {
    ti.Style = lipgloss.NewStyle().
        Foreground(lipgloss.Color("255")).
        Background(lipgloss.Color("237")).
        Border(lipgloss.RoundedBorder()).
        BorderForeground(lipgloss.Color("62")).
        Padding(0, 2)

    ti.CursorStyle = lipgloss.NewStyle().
        Foreground(lipgloss.Color("0")).
        Background(lipgloss.Color("228"))
}

// Light theme
func applyLightTheme(ti *textinput.Model) {
    ti.Style = lipgloss.NewStyle().
        Foreground(lipgloss.Color("0")).
        Background(lipgloss.Color("255")).
        Border(lipgloss.RoundedBorder()).
        BorderForeground(lipgloss.Color("99")).
        Padding(0, 2)

    ti.CursorStyle = lipgloss.NewStyle().
        Foreground(lipgloss.Color("255")).
        Background(lipgloss.Color("62"))
}
```

### Text Area Styling

```go
ta := textarea.New()

// Line numbers styling
ta.LineNumberStyle = lipgloss.NewStyle().
    Foreground(lipgloss.Color("240")).
    MarginRight(1)

// Content styling
ta.TextStyle = lipgloss.NewStyle().
    Foreground(lipgloss.Color("255"))

// Cursor line highlighting
ta.CursorLineStyle = lipgloss.NewStyle().
    Background(lipgloss.Color("236"))

// Placeholder styling
ta.PlaceholderStyle = lipgloss.NewStyle().
    Foreground(lipgloss.Color("240")).
    Italic(true)
```

### Table Styling

```go
// Table styling with themes
func styleTable(t *table.Model) {
    t.SetStyles(table.Styles{
        Header: lipgloss.NewStyle().
            Bold(true).
            Foreground(lipgloss.Color("228")).
            Background(lipgloss.Color("62")).
            Padding(0, 1).
            Align(lipgloss.Center),

        Cell: lipgloss.NewStyle().
            Foreground(lipgloss.Color("255")).
            Background(lipgloss.Color("237")).
            Padding(0, 1),

        Selected: lipgloss.NewStyle().
            Foreground(lipgloss.Color("0")).
            Background(lipgloss.Color("62")).
            Bold(true),
    })

    // Individual column styling
    columnStyles := []lipgloss.Style{
        lipgloss.NewStyle().Align(lipgloss.Left),   // Left-aligned
        lipgloss.NewStyle().Align(lipgloss.Center), // Center-aligned
        lipgloss.NewStyle().Align(lipgloss.Right),  // Right-aligned
    }
    t.WithColumnStyles(columnStyles)
}

// Border customization
func styleTableBorders(t *table.Model) {
    borderStyle := lipgloss.NewStyle().
        Border(lipgloss.RoundedBorder()).
        BorderForeground(lipgloss.Color("62"))

    t.BorderStyle(borderStyle.BorderStyle)
    t.BorderForeground(borderStyle.BorderForeground)
}
```

### List Styling

```go
// Custom delegate styling
func createStyledList(items []list.Item) list.Model {
    delegate := list.NewDefaultDelegate()

    // Update delegate styles
    delegate.Styles.Title = lipgloss.NewStyle().
        Foreground(lipgloss.Color("228")).
        Bold(true)

    delegate.Styles.Description = lipgloss.NewStyle().
        Foreground(lipgloss.Color("240")).
        MarginLeft(2)

    // Selected item styling
    delegate.Styles.SelectedTitle = lipgloss.NewStyle().
        Foreground(lipgloss.Color("0")).
        Background(lipgloss.Color("62")).
        Bold(true)

    delegate.Styles.SelectedDesc = lipgloss.NewStyle().
        Foreground(lipgloss.Color("0")).
        Background(lipgloss.Color("62"))

    // Create list with custom delegate
    l := list.New(items, delegate, 0, 0)

    // Style list components
    l.Styles.Title = lipgloss.NewStyle().
        Bold(true).
        Foreground(lipgloss.Color("62")).
        MarginBottom(1)

    l.Styles.StatusBar = lipgloss.NewStyle().
        Foreground(lipgloss.Color("240")).
        Background(lipgloss.Color("236"))

    l.Styles.PaginationStyle = lipgloss.NewStyle().
        Foreground(lipgloss.Color("62")).
        Bold(true)

    l.Styles.HelpStyle = lipgloss.NewStyle().
        Foreground(lipgloss.Color("240")).
        MarginTop(1)

    return l
}
```

### Progress Bar Styling

```go
// Gradient progress bar
func styleProgressGradient(p *progress.Model) {
    p = progress.New(
        progress.WithGradient("#7D56F4", "#F25D94"),
        progress.WithWidth(50),
        progress.WithDefaultScaled(),
    )
}

// Solid color progress bar
func styleProgressSolid(p *progress.Model) {
    p = progress.New(
        progress.WithSolidColor("#7D56F4"),
        progress.WithWidth(50),
        progress.WithoutPercentage(),
    )
}

// Custom styling
func styleProgressCustom(p *progress.Model) {
    p.FullColor = "#7D56F4"
    p.EmptyColor = "#4A5568"
    p.Full = '█'
    p.Empty = '░'
    p.ShowPercentage = true
    p.PercentStyle = lipgloss.NewStyle().
        Foreground(lipgloss.Color("228")).
        Bold(true)
}
```

### Spinner Styling

```go
// Styled spinner
func styleSpinner(s *spinner.Model) {
    s.Spinner = spinner.Points
    s.Style = lipgloss.NewStyle().
        Foreground(lipgloss.Color("62")).
        Bold(true)
}

// Colorful spinner
func styleColorfulSpinner(s *spinner.Model) {
    colors := []lipgloss.Color{
        lipgloss.Color("205"), // Pink
        lipgloss.Color("228"), // Yellow
        lipgloss.Color("69"),  // Blue
        lipgloss.Color("46"),  // Green
    }

    s.Style = lipgloss.NewStyle().
        Foreground(colors[rand.Intn(len(colors))])
}
```

### Paginator Styling

```go
// Dots paginator
func stylePaginatorDots(p *paginator.Model) {
    p.Type = paginator.Dots
    p.ActiveDot = lipgloss.NewStyle().
        Foreground(lipgloss.Color("62")).
        Bold(true).
        Render("●")

    p.InactiveDot = lipgloss.NewStyle().
        Foreground(lipgloss.Color("240")).
        Render("○")
}

// Arabic paginator
func stylePaginatorArabic(p *paginator.Model) {
    p.Type = paginator.Arabic
    p.ArabicSeparator = " / "

    // Style is applied when rendering
    pageStyle := lipgloss.NewStyle().
        Foreground(lipgloss.Color("62")).
        Bold(true)
}
```

### Viewport Styling

```go
// Styled viewport
func styleViewport(v *viewport.Model) {
    v.Style = lipgloss.NewStyle().
        Border(lipgloss.RoundedBorder()).
        BorderForeground(lipgloss.Color("62")).
        Padding(1, 2)
}

// Code-like viewport
func styleCodeViewport(v *viewport.Model) {
    v.Style = lipgloss.NewStyle().
        Background(lipgloss.Color("236")).
        Foreground(lipgloss.Color("255")).
        Border(lipgloss.NormalBorder()).
        BorderForeground(lipgloss.Color("240"))
}
```

### File Picker Styling

```go
// Styled file picker
func styleFilePicker(fp *filepicker.Model) {
    styles := filepicker.Styles{
        Cursor: lipgloss.NewStyle().
            Background(lipgloss.Color("62")).
            Bold(true),

        Selected: lipgloss.NewStyle().
            Background(lipgloss.Color("205")).
            Bold(true),

        Directory: lipgloss.NewStyle().
            Foreground(lipgloss.Color("69")).
            Bold(true),

        File: lipgloss.NewStyle().
            Foreground(lipgloss.Color("255")),

        Disabled: lipgloss.NewStyle().
            Foreground(lipgloss.Color("240")),

        Symlink: lipgloss.NewStyle().
            Foreground(lipgloss.Color("228")).
            Italic(true),
    }

    fp.SetStyles(styles)
}
```

### Timer Styling

```go
// Styled timer
func styleTimer(t *timer.Model) {
    t.Style = lipgloss.NewStyle().
        Foreground(lipgloss.Color("228")).
        Bold(true)

    t.TimeoutStyle = lipgloss.NewStyle().
        Foreground(lipgloss.Color("9")).
        Bold(true)
}
```

## Theme Systems

### Color Palettes

```go
// Define consistent color palette
type ColorPalette struct {
    Primary     lipgloss.Color
    Secondary   lipgloss.Color
    Accent      lipgloss.Color
    Success     lipgloss.Color
    Warning     lipgloss.Color
    Error       lipgloss.Color
    Text        lipgloss.Color
    Muted       lipgloss.Color
    Border      lipgloss.Color
    Background  lipgloss.Color
    Surface     lipgloss.Color
}

// Predefined themes
var DarkTheme = ColorPalette{
    Primary:     lipgloss.Color("62"),  // Purple
    Secondary:   lipgloss.Color("205"), // Pink
    Accent:      lipgloss.Color("226"), // Yellow
    Success:     lipgloss.Color("46"),  // Green
    Warning:     lipgloss.Color("208"), // Orange
    Error:       lipgloss.Color("9"),   // Red
    Text:        lipgloss.Color("255"), // White
    Muted:       lipgloss.Color("240"), // Gray
    Border:      lipgloss.Color("239"), // Light gray
    Background:  lipgloss.Color("235"), // Dark gray
    Surface:     lipgloss.Color("237"), // Medium gray
}

var LightTheme = ColorPalette{
    Primary:     lipgloss.Color("63"),  // Light purple
    Secondary:   lipgloss.Color("228"), // Light pink
    Accent:      lipgloss.Color("226"), // Yellow
    Success:     lipgloss.Color("46"),  // Green
    Warning:     lipgloss.Color("208"), // Orange
    Error:       lipgloss.Color("9"),   // Red
    Text:        lipgloss.Color("0"),   // Black
    Muted:       lipgloss.Color("245"), // Light gray
    Border:      lipgloss.Color("244"), // Medium gray
    Background:  lipgloss.Color("255"), // White
    Surface:     lipgloss.Color("250"), // Very light gray
}
```

### Theme Application

```go
// Apply theme to all components
func applyTheme(components *Components, theme ColorPalette) {
    // Text input
    components.TextInput.Style = lipgloss.NewStyle().
        Foreground(theme.Text).
        Background(theme.Surface).
        Border(lipgloss.NormalBorder()).
        BorderForeground(theme.Border)

    components.TextInput.CursorStyle = lipgloss.NewStyle().
        Foreground(theme.Background).
        Background(theme.Primary)

    // Table
    components.Table.SetStyles(table.Styles{
        Header: lipgloss.NewStyle().
            Foreground(theme.Text).
            Background(theme.Primary).
            Bold(true),

        Cell: lipgloss.NewStyle().
            Foreground(theme.Text).
            Background(theme.Surface),

        Selected: lipgloss.NewStyle().
            Foreground(theme.Background).
            Background(theme.Primary).
            Bold(true),
    })

    // List
    components.List.Styles.Title = lipgloss.NewStyle().
        Foreground(theme.Primary).
        Bold(true)

    // Progress
    components.Progress.FullColor = theme.Primary.String()
    components.Progress.EmptyColor = theme.Border.String()

    // Spinner
    components.Spinner.Style = lipgloss.NewStyle().
        Foreground(theme.Primary)
}
```

## Advanced Styling Techniques

### Dynamic Styling Based on State

```go
// Style based on validation state
func styleTextInputValidation(ti *textinput.Model, isValid bool) {
    if isValid {
        ti.Style = lipgloss.NewStyle().
            Foreground(lipgloss.Color("255")).
            Background(lipgloss.Color("237")).
            Border(lipgloss.NormalBorder()).
            BorderForeground(lipgloss.Color("46")) // Green border
    } else {
        ti.Style = lipgloss.NewStyle().
            Foreground(lipgloss.Color("255")).
            Background(lipgloss.Color("237")).
            Border(lipgloss.NormalBorder()).
            BorderForeground(lipgloss.Color("9")) // Red border
    }
}
```

### Conditional Styling

```go
// Style based on focus state
func styleComponentFocus(component interface{}, focused bool) {
    switch c := component.(type) {
    case *textinput.Model:
        if focused {
            c.Style = lipgloss.NewStyle().
                Border(lipgloss.NormalBorder()).
                BorderForeground(lipgloss.Color("62")) // Highlighted
        } else {
            c.Style = lipgloss.NewStyle().
                Border(lipgloss.NormalBorder()).
                BorderForeground(lipgloss.Color("239")) // Dimmed
        }
    }
}
```

### Animated Effects

```go
// Pulsing effect for loading states
func createPulsingStyle(baseColor lipgloss.Color) lipgloss.Style {
    return lipgloss.NewStyle().
        Foreground(baseColor).
        Bold(true)
}

func applyPulsingAnimation(style lipgloss.Style, intensity float64) lipgloss.Style {
    // Adjust opacity/brightness based on intensity
    color := style.GetForeground()
    return style.Foreground(color)
}
```

### Responsive Design

```go
// Adjust styling based on terminal width
func responsiveStyle(width int) lipgloss.Style {
    if width < 80 {
        // Small terminal
        return lipgloss.NewStyle().
            Width(width-4).
            Padding(0, 1)
    } else if width < 120 {
        // Medium terminal
        return lipgloss.NewStyle().
            Width(width-8).
            Padding(0, 2)
    } else {
        // Large terminal
        return lipgloss.NewStyle().
            Width(100).
            Padding(0, 3).
            MarginLeft((width-100)/2) // Center
    }
}
```

## Accessibility Considerations

### High Contrast Styling

```go
// High contrast theme
var HighContrastTheme = ColorPalette{
    Primary:     lipgloss.Color("15"), // Bright white
    Secondary:   lipgloss.Color("12"), // Bright blue
    Success:     lipgloss.Color("10"), // Bright green
    Warning:     lipgloss.Color("11"), // Bright yellow
    Error:       lipgloss.Color("9"),  // Bright red
    Text:        lipgloss.Color("15"), // Bright white
    Muted:       lipgloss.Color("8"),  // Bright gray
    Border:      lipgloss.Color("7"),  // White
    Background:  lipgloss.Color("0"),  // Black
    Surface:     lipgloss.Color("8"),  // Dark gray
}
```

### Focus Indicators

```go
// Clear focus indicators
func addFocusIndicator(style lipgloss.Style) lipgloss.Style {
    return style.
        Border(lipgloss.NormalBorder()).
        BorderForeground(lipgloss.Color("62")). // Highlight color
        Bold(true)
}
```

### Color Blindness Support

```go
// Use patterns beyond just color
func createAccessibleStatus(status string) string {
    switch strings.ToLower(status) {
    case "active":
        return "✓ Active"  // Icon + text
    case "warning":
        return "⚠ Warning" // Icon + text
    case "error":
        return "✗ Error"   // Icon + text
    default:
        return "○ " + status
    }
}
```

## Best Practices

### Consistent Styling

1. **Use a Color Palette**: Define colors once and reuse throughout
2. **Create Style Functions**: Reuse common styling patterns
3. **Theme Support**: Support light/dark themes with adaptive colors
4. **Accessibility**: Ensure good contrast and keyboard navigation

### Performance Considerations

1. **Precompute Styles**: Create styles at startup, not in loops
2. **Reuse Styles**: Store frequently used styles in variables
3. **Avoid Over-styling**: Don't apply styles unnecessarily
4. **Profile Rendering**: Monitor rendering performance

### Maintenance

1. **Document Customization**: Keep notes on styling decisions
2. **Test on Multiple Terminals**: Ensure compatibility
3. **Version Control**: Track style changes in version control
4. **User Feedback**: Collect feedback on visual appearance

This styling guide provides comprehensive patterns and techniques for creating beautiful, consistent, and accessible terminal user interfaces with Bubbles components.