# BubbleTea Styling Patterns with Lip Gloss

This reference provides comprehensive styling patterns and techniques for creating beautiful and consistent terminal user interfaces using Lip Gloss with BubbleTea applications.

## Color System and Palettes

### Consistent Color Palette

Define a comprehensive color palette for your application:

```go
package main

import "github.com/charmbracelet/lipgloss"

// Define color palette
var (
    // Primary colors
    primaryColor   = lipgloss.Color("62")    // Purple
    secondaryColor = lipgloss.Color("205")   // Pink

    // Neutral colors
    textColor      = lipgloss.Color("255")   // White
    mutedColor     = lipgloss.Color("240")   // Gray
    borderColor    = lipgloss.Color("239")   // Light gray

    // Status colors
    successColor   = lipgloss.Color("46")    // Green
    warningColor   = lipgloss.Color("226")   // Yellow
    errorColor     = lipgloss.Color("9")     // Red
    infoColor      = lipgloss.Color("69")    // Blue

    // Background colors
    background     = lipgloss.Color("235")   // Dark gray
    surface        = lipgloss.Color("237")   // Lighter gray
)

// Adaptive colors for better terminal compatibility
var (
    primaryAdaptive = lipgloss.AdaptiveColor{
        Light: "63",  // Purple for light terminals
        Dark:  "228", // Pink for dark terminals
    }

    surfaceAdaptive = lipgloss.AdaptiveColor{
        Light: "251", // Light gray for light terminals
        Dark:  "235", // Dark gray for dark terminals
    }
)
```

### Theme System

Create a theme system for consistent styling:

```go
type Theme struct {
    Name     string
    Primary  lipgloss.Color
    Secondary lipgloss.Color
    Success  lipgloss.Color
    Warning  lipgloss.Color
    Error    lipgloss.Color
    Info     lipgloss.Color
    Text     lipgloss.Color
    Muted    lipgloss.Color
    Border   lipgloss.Color
    Background lipgloss.Color
    Surface  lipgloss.Color
}

var themes = map[string]Theme{
    "default": {
        Name:     "Default",
        Primary:  lipgloss.Color("62"),
        Secondary: lipgloss.Color("205"),
        Success:  lipgloss.Color("46"),
        Warning:  lipgloss.Color("226"),
        Error:    lipgloss.Color("9"),
        Info:     lipgloss.Color("69"),
        Text:     lipgloss.Color("255"),
        Muted:    lipgloss.Color("240"),
        Border:   lipgloss.Color("239"),
        Background: lipgloss.Color("235"),
        Surface:  lipgloss.Color("237"),
    },
    "ocean": {
        Name:     "Ocean",
        Primary:  lipgloss.Color("38"),  // Cyan
        Secondary: lipgloss.Color("69"), // Blue
        Success:  lipgloss.Color("46"), // Green
        Warning:  lipgloss.Color("220"), // Gold
        Error:    lipgloss.Color("9"),  // Red
        Info:     lipgloss.Color("38"), // Cyan
        Text:     lipgloss.Color("255"), // White
        Muted:    lipgloss.Color("247"), // Light gray
        Border:   lipgloss.Color("30"), // Deep cyan
        Background: lipgloss.Color("17"), // Dark blue
        Surface:  lipgloss.Color("19"), // Navy
    },
    "forest": {
        Name:     "Forest",
        Primary:  lipgloss.Color("28"), // Green
        Secondary: lipgloss.Color("34"), // Light green
        Success:  lipgloss.Color("46"), // Bright green
        Warning:  lipgloss.Color("226"), // Yellow
        Error:    lipgloss.Color("9"), // Red
        Info:     lipgloss.Color("37"), // Light blue
        Text:     lipgloss.Color("255"), // White
        Muted:    lipgloss.Color("242"), // Light gray
        Border:   lipgloss.Color("22"), // Dark green
        Background: lipgloss.Color("22"), // Dark green
        Surface:  lipgloss.Color("23"), // Forest green
    },
}
```

## Base Style Definitions

### Reusable Base Styles

Create a comprehensive set of base styles:

```go
var (
    // Text styles
    titleStyle = lipgloss.NewStyle().
        Bold(true).
        Foreground(textColor).
        MarginTop(1).
        MarginBottom(1)

    subtitleStyle = lipgloss.NewStyle().
        Foreground(mutedColor).
        MarginBottom(1)

    headerStyle = lipgloss.NewStyle().
        Bold(true).
        Foreground(primaryColor).
        Padding(0, 1)

    // Button styles
    buttonStyle = lipgloss.NewStyle().
        Foreground(textColor).
        Background(primaryColor).
        Padding(0, 2).
        Margin(0, 1)

    buttonActiveStyle = buttonStyle.
        Background(secondaryColor).
        Bold(true)

    buttonDisabledStyle = lipgloss.NewStyle().
        Foreground(mutedColor).
        Background(borderColor).
        Padding(0, 2).
        Margin(0, 1)

    // Input styles
    inputStyle = lipgloss.NewStyle().
        Foreground(textColor).
        Background(surface).
        Border(lipgloss.NormalBorder()).
        BorderForeground(borderColor).
        Padding(0, 1)

    inputFocusedStyle = inputStyle.
        BorderForeground(primaryColor)

    // Card/panel styles
    cardStyle = lipgloss.NewStyle().
        Border(lipgloss.RoundedBorder()).
        BorderForeground(borderColor).
        Padding(1, 2).
        Margin(1, 0)

    cardHeaderStyle = lipgloss.NewStyle().
        Bold(true).
        Foreground(primaryColor).
        MarginBottom(1)

    // Status styles
    successStyle = lipgloss.NewStyle().
        Foreground(successColor).
        Bold(true)

    warningStyle = lipgloss.NewStyle().
        Foreground(warningColor).
        Bold(true)

    errorStyle = lipgloss.NewStyle().
        Foreground(errorColor).
        Bold(true)

    infoStyle = lipgloss.NewStyle().
        Foreground(infoColor).
        Bold(true)

    // Muted text
    mutedStyle = lipgloss.NewStyle().
        Foreground(mutedColor)

    // Cursor/selection styles
    cursorStyle = lipgloss.NewStyle().
        Background(primaryColor).
        Foreground(lipgloss.Color("0"))

    selectedStyle = lipgloss.NewStyle().
        Background(primaryColor).
        Foreground(lipgloss.Color("0")).
        Bold(true)

    // Border styles
    borderStyle = lipgloss.NewStyle().
        Border(lipgloss.NormalBorder()).
        BorderForeground(borderColor)

    borderFocusedStyle = borderStyle.
        BorderForeground(primaryColor)
)
```

### Dynamic Style Functions

Create functions that generate styles dynamically:

```go
func getThemedStyle(theme Theme) *ThemedStyles {
    return &ThemedStyles{
        Title: lipgloss.NewStyle().
            Bold(true).
            Foreground(theme.Text).
            MarginTop(1).
            MarginBottom(1),

        Primary: lipgloss.NewStyle().
            Foreground(theme.Primary).
            Bold(true),

        PrimaryButton: lipgloss.NewStyle().
            Foreground(lipgloss.Color("0")).
            Background(theme.Primary).
            Padding(0, 2).
            Bold(true),

        SecondaryButton: lipgloss.NewStyle().
            Foreground(theme.Primary).
            Background(theme.Surface).
            Border(true, true, true, false).
            BorderForeground(theme.Primary).
            Padding(0, 2),

        Card: lipgloss.NewStyle().
            Border(lipgloss.RoundedBorder()).
            BorderForeground(theme.Border).
            Padding(1, 2).
            Margin(1, 0).
            Background(theme.Surface),

        Input: lipgloss.NewStyle().
            Foreground(theme.Text).
            Background(theme.Surface).
            Border(lipgloss.NormalBorder()).
            BorderForeground(theme.Border).
            Padding(0, 1),

        InputFocused: lipgloss.NewStyle().
            Foreground(theme.Text).
            Background(theme.Surface).
            Border(lipgloss.NormalBorder()).
            BorderForeground(theme.Primary).
            Padding(0, 1),
    }
}

type ThemedStyles struct {
    Title           lipgloss.Style
    Primary         lipgloss.Style
    PrimaryButton   lipgloss.Style
    SecondaryButton lipgloss.Style
    Card            lipgloss.Style
    Input           lipgloss.Style
    InputFocused    lipgloss.Style
}
```

## Component Styling Patterns

### Text Input Styling

Comprehensive text input styling:

```go
func styleTextInput(ti textinput.Model, focused bool) textinput.Model {
    if focused {
        ti.Style = inputFocusedStyle
        ti.PlaceholderStyle = lipgloss.NewStyle().
            Foreground(mutedColor)
        ti.CursorStyle = lipgloss.NewStyle().
            Background(primaryColor)
    } else {
        ti.Style = inputStyle
        ti.PlaceholderStyle = lipgloss.NewStyle().
            Foreground(mutedColor)
    }

    // Apply validation styling
    ti.Validate = func(s string) error {
        if s == "" {
            ti.TextStyle = errorStyle
            return fmt.Errorf("field is required")
        }
        ti.TextStyle = lipgloss.NewStyle().Foreground(textColor)
        return nil
    }

    return ti
}
```

### Table Styling

Advanced table styling with themes:

```go
func styleTable(t table.Model, theme Theme) table.Model {
    t.SetStyles(table.Styles{
        Header: lipgloss.NewStyle().
            Bold(true).
            Foreground(theme.Primary).
            Background(theme.Surface).
            Padding(0, 1).
            Align(lipgloss.Center),

        Cell: lipgloss.NewStyle().
            Foreground(theme.Text).
            Background(theme.Surface).
            Padding(0, 1),

        Selected: lipgloss.NewStyle().
            Foreground(lipgloss.Color("0")).
            Background(theme.Primary).
            Bold(true),

        RowSeparator: lipgloss.NewStyle().
            Foreground(theme.Border),

        ColumnSeparator: lipgloss.NewStyle().
            Foreground(theme.Border),
    })

    // Style columns individually
    columnStyles := []lipgloss.Style{
        lipgloss.NewStyle().Align(lipgloss.Left),   // ID
        lipgloss.NewStyle().Align(lipgloss.Left),   // Name
        lipgloss.NewStyle().Align(lipgloss.Left),   // Email
        lipgloss.NewStyle().Align(lipgloss.Center), // Status
        lipgloss.NewStyle().Align(lipgloss.Right),  // Date
    }

    t.WithColumnStyles(columnStyles)

    return t
}
```

### List Styling

List component with custom delegate styling:

```go
func createStyledList(items []list.Item, theme Theme) list.Model {
    delegate := list.NewDefaultDelegate()

    // Style the delegate
    delegate.ShowDescription = true
    delegate.Styles.Title = lipgloss.NewStyle().
        Foreground(theme.Text).
        Bold(true)

    delegate.Styles.Description = lipgloss.NewStyle().
        Foreground(mutedColor).
        MarginLeft(2)

    delegate.Styles.NormalTitle = lipgloss.NewStyle().
        Foreground(theme.Text)

    delegate.Styles.SelectedTitle = lipgloss.NewStyle().
        Foreground(lipgloss.Color("0")).
        Background(theme.Primary).
        Bold(true)

    delegate.Styles.NormalDesc = lipgloss.NewStyle().
        Foreground(mutedColor)

    delegate.Styles.SelectedDesc = lipgloss.NewStyle().
        Foreground(lipgloss.Color("0")).
        Background(theme.Primary)

    // Create list
    l := list.New(items, delegate, 0, 0)

    // Style list components
    l.Styles.Title = lipgloss.NewStyle().
        Bold(true).
        Foreground(theme.Primary).
        MarginTop(1).
        MarginBottom(1)

    l.Styles.StatusBar = lipgloss.NewStyle().
        Foreground(mutedColor).
        Background(theme.Surface)

    l.Styles.PaginationStyle = lipgloss.NewStyle().
        Foreground(theme.Primary).
        Bold(true)

    l.Styles.HelpStyle = lipgloss.NewStyle().
        Foreground(mutedColor).
        MarginTop(1)

    return l
}
```

### Progress Bar Styling

Styled progress bars with themes:

```go
func createStyledProgress(theme Theme) progress.Model {
    // Custom gradient for theme
    gradient := []string{
        theme.Primary.String(),
        theme.Secondary.String(),
    }

    p := progress.New(
        progress.WithGradient(gradient...),
        progress.WithWidth(50),
        progress.WithDefaultScaled(),
    )

    // Style full/empty characters
    p.FullColor = theme.Primary
    p.EmptyColor = theme.Border

    // Percentage style
    p.PercentageStyle = lipgloss.NewStyle().
        Foreground(theme.Text).
        Bold(true)

    return p
}
```

### Spinner Styling

Styled spinners with themes:

```go
func createStyledSpinner(theme Theme) spinner.Model {
    s := spinner.New()

    // Choose spinner based on theme
    switch theme.Name {
    case "ocean":
        s.Spinner = spinner.Line
    case "forest":
        s.Spinner = spinner.Dot
    default:
        s.Spinner = spinner.Points
    }

    // Apply theme colors
    s.Style = lipgloss.NewStyle().
        Foreground(theme.Primary)

    return s
}
```

## Layout and Composition Patterns

### Responsive Layouts

Create responsive layouts that adapt to terminal size:

```go
type ResponsiveLayout struct {
    width  int
    height int
    theme  Theme
}

func (rl *ResponsiveLayout) LayoutComponents(components []string) string {
    if rl.width < 80 {
        // Mobile layout - vertical stack
        return rl.verticalLayout(components)
    } else if rl.width < 120 {
        // Tablet layout - two columns
        return rl.twoColumnLayout(components)
    } else {
        // Desktop layout - three columns
        return rl.threeColumnLayout(components)
    }
}

func (rl *ResponsiveLayout) verticalLayout(components []string) string {
    var content strings.Builder

    for _, component := range components {
        content.WriteString(
            lipgloss.NewStyle().
                Width(rl.width-4).
                Border(lipgloss.RoundedBorder()).
                BorderForeground(rl.theme.Border).
                Padding(1).
                Render(component) + "\n",
        )
    }

    return content.String()
}

func (rl *ResponsiveLayout) twoColumnLayout(components []string) string {
    // Split components into two columns
    colWidth := (rl.width - 6) / 2

    var leftCol, rightCol strings.Builder
    for i, component := range components {
        if i%2 == 0 {
            leftCol.WriteString(component + "\n")
        } else {
            rightCol.WriteString(component + "\n")
        }
    }

    leftPanel := lipgloss.NewStyle().
        Width(colWidth).
        Border(lipgloss.RoundedBorder()).
        BorderForeground(rl.theme.Border).
        Padding(1).
        Render(leftCol.String())

    rightPanel := lipgloss.NewStyle().
        Width(colWidth).
        Border(lipgloss.RoundedBorder()).
        BorderForeground(rl.theme.Border).
        Padding(1).
        MarginLeft(1).
        Render(rightCol.String())

    return lipgloss.JoinHorizontal(lipgloss.Left, leftPanel, rightPanel)
}
```

### Card-Based Layouts

Create reusable card components:

```go
func createCard(title, content string, theme Theme) string {
    cardHeader := lipgloss.NewStyle().
        Bold(true).
        Foreground(theme.Primary).
        Background(theme.Surface).
        Padding(0, 1).
        Render(title)

    cardContent := lipgloss.NewStyle().
        Foreground(theme.Text).
        Padding(1).
        Render(content)

    return lipgloss.JoinVertical(
        lipgloss.Left,
        cardHeader,
        cardContent,
    )
}

func createCardWithTitle(title, subtitle, content string, theme Theme) string {
    titleStyle := lipgloss.NewStyle().
        Bold(true).
        Foreground(theme.Primary).
        MarginBottom(1)

    subtitleStyle := lipgloss.NewStyle().
        Foreground(mutedColor).
        MarginBottom(2)

    contentStyle := lipgloss.NewStyle().
        Foreground(theme.Text)

    card := lipgloss.JoinVertical(
        lipgloss.Left,
        titleStyle.Render(title),
        subtitleStyle.Render(subtitle),
        contentStyle.Render(content),
    )

    return lipgloss.NewStyle().
        Border(lipgloss.RoundedBorder()).
        BorderForeground(theme.Border).
        Padding(2).
        Render(card)
}
```

### Status Indicators

Consistent status styling across components:

```go
func renderStatus(status string, theme Theme) string {
    switch strings.ToLower(status) {
    case "active", "online", "connected":
        return successStyle.Render("● " + status)
    case "warning", "pending", "partial":
        return warningStyle.Render("⚠ " + status)
    case "error", "offline", "failed":
        return errorStyle.Render("✗ " + status)
    case "info", "neutral", "idle":
        return infoStyle.Render("ℹ " + status)
    default:
        return mutedStyle.Render("○ " + status)
    }
}

func renderProgressBar(progress float64, width int, theme Theme) string {
    chars := int(float64(width) * progress)

    filled := strings.Repeat("█", chars)
    empty := strings.Repeat("░", width-chars)

    var color lipgloss.Color
    if progress >= 1.0 {
        color = successColor
    } else if progress >= 0.7 {
        color = primaryColor
    } else if progress >= 0.3 {
        color = warningColor
    } else {
        color = errorColor
    }

    filledStyle := lipgloss.NewStyle().Foreground(color)
    emptyStyle := lipgloss.NewStyle().Foreground(borderColor)

    return filledStyle.Render(filled) + emptyStyle.Render(empty)
}
```

## Accessibility and Color Blindness

### High Contrast Themes

Create themes optimized for accessibility:

```go
var highContrastTheme = Theme{
    Name:     "High Contrast",
    Primary:  lipgloss.Color("15"), // Bright white
    Secondary: lipgloss.Color("12"), // Bright blue
    Success:  lipgloss.Color("10"), // Bright green
    Warning:  lipgloss.Color("11"), // Bright yellow
    Error:    lipgloss.Color("9"),  // Bright red
    Info:     lipgloss.Color("14"), // Bright cyan
    Text:     lipgloss.Color("15"), // Bright white
    Muted:    lipgloss.Color("8"),  // Bright gray
    Border:   lipgloss.Color("7"),  // White
    Background: lipgloss.Color("0"), // Black
    Surface:  lipgloss.Color("8"),  // Dark gray
}

func getAccessibleStyles(theme Theme) *AccessibleStyles {
    return &AccessibleStyles{
        // High contrast buttons
        Button: lipgloss.NewStyle().
            Foreground(lipgloss.Color("0")).
            Background(theme.Primary).
            Padding(0, 2).
            Bold(true),

        // Clear indicators
        Selected: lipgloss.NewStyle().
            Background(theme.Primary).
            Foreground(lipgloss.Color("0")).
            Bold(true).

        // Clear focus indicators
        Focused: lipgloss.NewStyle().
            Border(lipgloss.NormalBorder()).
            BorderForeground(theme.Primary).
            Background(lipgloss.Color("8")),

        // Clear status indicators
        Status: map[string]lipgloss.Style{
            "active":  lipgloss.NewStyle().Foreground(successColor).Bold(true),
            "warning": lipgloss.NewStyle().Foreground(warningColor).Bold(true),
            "error":   lipgloss.NewStyle().Foreground(errorColor).Bold(true),
            "info":    lipgloss.NewStyle().Foreground(infoColor).Bold(true),
        },
    }
}

type AccessibleStyles struct {
    Button   lipgloss.Style
    Selected lipgloss.Style
    Focused  lipgloss.Style
    Status   map[string]lipgloss.Style
}
```

### Color Blindness Support

Create patterns that work for different types of color blindness:

```go
// Use patterns beyond just color
func renderAccessibleStatus(status string, icon string) string {
    switch strings.ToLower(status) {
    case "active", "online":
        return successStyle.Render("✓ " + icon + " " + status)
    case "warning", "pending":
        return warningStyle.Render("⚠ " + icon + " " + status)
    case "error", "offline":
        return errorStyle.Render("✗ " + icon + " " + status)
    default:
        return infoStyle.Render("ℹ " + icon + " " + status)
    }
}

// Use text indicators alongside colors
func renderAccessibleBadge(text string, color lipgloss.Color) string {
    style := lipgloss.NewStyle().
        Foreground(lipgloss.Color("0")).
        Background(color).
        Padding(0, 1).
        Bold(true)

    return style.Render("[" + text + "]")
}
```

## Advanced Styling Techniques

### Animated Effects

Create simple animations using text patterns:

```go
func renderAnimatedSpinner(frame int, text string) string {
    spinnerChars := []string{"⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"}
    char := spinnerChars[frame%len(spinnerChars)]

    spinnerStyle := lipgloss.NewStyle().
        Foreground(primaryColor).
        Bold(true)

    textStyle := lipgloss.NewStyle().
        Foreground(textColor)

    return spinnerStyle.Render(char) + " " + textStyle.Render(text)
}

func renderPulsingText(text string, intensity float64) string {
    color := lipgloss.Color(fmt.Sprintf("%d", int(205+intensity*50)))

    return lipgloss.NewStyle().
        Foreground(color).
        Bold(intensity > 0.5).
        Render(text)
}
```

### Complex Border Styles

Create custom border combinations:

```go
func createComplexBorders(theme Theme) map[string]lipgloss.Style {
    return map[string]lipgloss.Style{
        "default": lipgloss.NewStyle().
            Border(lipgloss.RoundedBorder()).
            BorderForeground(theme.Border),

        "focused": lipgloss.NewStyle().
            Border(lipgloss.DoubleBorder()).
            BorderForeground(theme.Primary).

        "error": lipgloss.NewStyle().
            Border(lipgloss.ThickBorder()).
            BorderForeground(theme.Error),

        "success": lipgloss.NewStyle().
            Border(lipgloss.NormalBorder()).
            BorderForeground(theme.Success),

        "subtitle": lipgloss.NewStyle().
            Border(lipgloss.NormalBorder()).
            BorderBottom(true).
            BorderForeground(theme.Border),
    }
}
```

These styling patterns provide a comprehensive foundation for creating beautiful, consistent, and accessible terminal user interfaces with BubbleTea and Lip Gloss. The patterns are designed to be reusable and adaptable to different application needs and design requirements.