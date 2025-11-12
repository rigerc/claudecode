# Bubbles Package Documentation

**Bubbles** is a comprehensive component library for building terminal user interfaces (TUIs) with Bubble Tea applications. It provides production-ready UI components that handle common patterns like text input, spinners, tables, progress bars, and more. Each component is a self-contained model that implements the Bubble Tea Model-View-Update pattern, making them easy to compose into larger applications.

## Table of Contents

1. [Installation](#installation)
2. [Overview](#overview)
3. [Core Components](#core-components)
4. [Component Reference](#component-reference)
5. [Styling with Lip Gloss](#styling-with-lip-gloss)
6. [Integration Patterns](#integration-patterns)
7. [Best Practices](#best-practices)
8. [Advanced Usage](#advanced-usage)
9. [Troubleshooting](#troubleshooting)

## Installation

```bash
go get github.com/charmbracelet/bubbles
# And also get the styling library
go get github.com/charmbracelet/lipgloss
```

## Overview

Bubbles components follow these principles:

- **Self-contained**: Each component manages its own state
- **Composable**: Components can be combined and nested
- **Customizable**: Extensive styling and behavior configuration
- **Bubble Tea compatible**: Implements the Model-View-Update pattern
- **Production ready**: Used in applications like Glow and other TUI projects

### Basic Pattern

All Bubbles components follow this basic structure:

```go
package main

import (
    "tea "github.com/charmbracelet/bubbletea"
    "github.com/charmbracelet/bubbles/[component]"
)

type Model struct {
    component [component].Model
    // other state...
}

func initialModel() Model {
    // Initialize component
    comp := [component].New()
    // Configure component
    comp.Focus()

    return Model{
        component: comp,
    }
}

func (m Model) Init() tea.Cmd {
    // Component may return a command (like blinking cursor)
    return m.component.Init()
}

func (m Model) Update(msg tea.Msg) (tea.Model, tea.Cmd) {
    var cmd tea.Cmd

    // Let component handle messages first
    m.component, cmd = m.component.Update(msg)

    // Handle component-specific messages
    switch msg := msg.(type) {
    case [component].SpecificMsg:
        // Handle component messages

    case tea.KeyMsg:
        // Handle key messages not consumed by component
    }

    return m, cmd
}

func (m Model) View() string {
    return m.component.View()
}
```

## Core Components

### Text Input (`textinput`)

Single-line text input field with unicode support, clipboard operations, and horizontal scrolling.

```go
package main

import (
    "fmt"
    tea "github.com/charmbracelet/bubbletea"
    "github.com/charmbracelet/bubbles/textinput"
)

type Model struct {
    textInput textinput.Model
    quiting   bool
}

func initialModel() Model {
    ti := textinput.New()
    ti.Placeholder = "Enter your name..."
    ti.Focus()
    ti.CharLimit = 50
    ti.Width = 30

    // Enable password mode
    // ti.EchoMode = textinput.EchoPassword
    // ti.EchoCharacter = '•'

    return Model{textInput: ti}
}

func (m Model) Init() tea.Cmd {
    return textinput.Blink // Blink cursor
}

func (m Model) Update(msg tea.Msg) (tea.Model, tea.Cmd) {
    var cmd tea.Cmd

    switch msg := msg.(type) {
    case tea.KeyMsg:
        switch msg.Type {
        case tea.KeyEnter, tea.KeyCtrlC:
            m.quiting = true
            return m, tea.Quit
        }
    }

    m.textInput, cmd = m.textInput.Update(msg)
    return m, cmd
}

func (m Model) View() string {
    if m.quiting {
        return fmt.Sprintf("Hello, %s!\n", m.textInput.Value())
    }
    return fmt.Sprintf("What's your name?\n\n%s", m.textInput.View())
}

func main() {
    p := tea.NewProgram(initialModel())
    if _, err := p.Run(); err != nil {
        fmt.Printf("Error: %v", err)
    }
}
```

#### Text Input Configuration

```go
ti := textinput.New()

// Basic configuration
ti.Placeholder = "Enter text..."
ti.Focus()
ti.Blur()

// Text limits
ti.CharLimit = 50          // Maximum characters
ti.Width = 30              // Visual width

// Echo modes
ti.EchoMode = textinput.EchoNormal    // Show text (default)
ti.EchoMode = textinput.EchoPassword  // Hide text
ti.EchoMode = textinput.EchoNone      // No echo at all
ti.EchoCharacter = '•'                // Character for password mode

// Cursor control
ti.CursorStyle = lipgloss.NewStyle().
    Background(lipgloss.Color("#7D56F4"))

// Value operations
value := ti.Value()
ti.SetValue("default value")
ti.SetValueFromCursor("new value")

// Position control
pos := ti.Cursor()
ti.SetCursor(5)    // Set cursor position
ti.CursorEnd()     // Move to end
ti.CursorStart()   // Move to start

// Selection
start, end := ti.Selection()
ti.SetSelection(2, 5)
ti.ClearSelection()
ti.SelectedText()

// Validation
ti.Validate = func(s string) error {
    if len(s) < 3 {
        return fmt.Errorf("too short")
    }
    return nil
}

// Autocomplete
ti.ShowSuggestions = true
ti.KeyMap.AcceptSuggestion = key.NewBinding(
    key.WithKeys(tea.KeyTab),
    key.WithHelp("tab", "accept"),
)
```

#### Text Input Key Bindings

```go
// Default keybindings include:
// - Arrow keys: Move cursor
// - Ctrl+A/End: Move to start/end
// - Ctrl+E: Move to end
// - Ctrl+K: Delete to end of line
// - Ctrl+U: Delete to start of line
// - Ctrl+W: Delete word backward
// - Alt+B/F: Move word backward/forward
// - Tab: Accept suggestion (if enabled)
// - Enter/Escape: Submit/Cancel

// Custom keybindings
ti.KeyMap.AcceptSuggestion = key.NewBinding(
    key.WithKeys("right"),
    key.WithHelp("→", "accept"),
)

ti.KeyMap.WordForward = key.NewBinding(
    key.WithKeys("ctrl+right", "alt+f"),
    key.WithHelp("ctrl+→", "next word"),
)
```

### Text Area (`textarea`)

Multi-line text input with vertical scrolling, line wrapping, and vim-style editing.

```go
package main

import (
    "github.com/charmbracelet/bubbles/textarea"
    tea "github.com/charmbracelet/bubbletea"
)

type Model struct {
    textarea textarea.Model
}

func initialModel() Model {
    ta := textarea.New()
    ta.Placeholder = "Write your story here..."
    ta.Focus()

    // Size configuration
    ta.SetWidth(80)
    ta.SetHeight(10)

    // Line configuration
    ta.ShowLineNumbers = true
    ta.CharLimit = 5000

    // Keybindings
    ta.KeyMap.InsertNewline.SetEnabled(false) // Disable enter key

    return Model{textarea: ta}
}

func (m Model) Init() tea.Cmd {
    return textarea.Blink
}

func (m Model) Update(msg tea.Msg) (tea.Model, tea.Cmd) {
    var cmd tea.Cmd
    m.textarea, cmd = m.textarea.Update(msg)
    return m, cmd
}

func (m Model) View() string {
    return m.textarea.View()
}
```

#### Text Area Features

```go
ta := textarea.New()

// Size and positioning
ta.SetWidth(60)
ta.SetHeight(20)
ta.SetCursor(10, 5)  // Line, column

// Line numbers
ta.ShowLineNumbers = true
ta.LineNumberStyle = lipgloss.NewStyle().
    Foreground(lipgloss.Color("245"))

// Content operations
content := ta.Value()
ta.SetValue("Initial content\nMulti-line")
ta.InsertString("Inserted text")
ta.DeleteWordBackward()
ta.DeleteWordForward()

// Line operations
ta.LineCount()          // Total lines
ta.CurrentLine()        // Current line number
ta.LineContent(5)       // Get line content
ta.InsertLine("New line")
ta.DeleteLine(3)        // Delete specific line

// Cursor operations
ta.CursorUp()
ta.CursorDown()
ta.CursorLeft()
ta.CursorRight()
ta.CursorBeginning()
ta.CursorEnd()
ta.WordBackward()
ta.WordForward()

// Character limits
ta.CharLimit = 10000
ta.SetCharLimit(5000)

// Keymap customization
ta.KeyMap.DeleteWordBackward = key.NewBinding(
    key.WithKeys("ctrl+w"),
    key.WithHelp("ctrl+w", "delete word"),
)

// Style customization
ta.PlaceholderStyle = lipgloss.NewStyle().
    Foreground(lipgloss.Color("240"))
ta.TextStyle = lipgloss.NewStyle().
    Foreground(lipgloss.Color("255"))
ta.CursorLineStyle = lipgloss.NewStyle().
    Background(lipgloss.Color("240"))

// Vim-like mode
ta.KeyMap.InsertNewline.SetEnabled(true)  // Enter inserts newline
ta.KeyMap.DeleteCharBackward = key.NewBinding(
    key.WithKeys("backspace"),
    key.WithHelp("⌫", "delete char"),
)
```

### Spinner (`spinner`)

Animated spinner for indicating loading states and background operations.

```go
package main

import (
    "time"
    "github.com/charmbracelet/bubbles/spinner"
    tea "github.com/charmbracelet/bubbletea"
    "github.com/charmbracelet/lipgloss"
)

type tickMsg time.Time

type Model struct {
    spinner  spinner.Model
    loading  bool
    progress float64
}

func initialModel() Model {
    s := spinner.New()
    s.Spinner = spinner.Dot
    s.Style = lipgloss.NewStyle().
        Foreground(lipgloss.Color("205"))

    return Model{
        spinner: s,
        loading: true,
    }
}

func (m Model) Init() tea.Cmd {
    return tea.Batch(
        m.spinner.Tick,
        tea.Tick(time.Millisecond*50, func(t time.Time) tea.Msg {
            return tickMsg(t)
        }),
    )
}

func (m Model) Update(msg tea.Msg) (tea.Model, tea.Cmd) {
    var cmd tea.Cmd

    switch msg := msg.(type) {
    case tea.KeyMsg:
        if msg.Type == tea.KeyCtrlC {
            return m, tea.Quit
        }

    case tickMsg:
        if m.loading {
            m.progress += 0.01
            if m.progress >= 1.0 {
                m.loading = false
                return m, tea.Quit
            }
            return m, tea.Tick(time.Millisecond*50, func(t time.Time) tea.Msg {
                return tickMsg(t)
            })
        }

    case spinner.TickMsg:
        m.spinner, cmd = m.spinner.Update(msg)
        return m, cmd
    }

    return m, nil
}

func (m Model) View() string {
    if m.loading {
        return fmt.Sprintf(
            "\n %s Loading... %.0f%%\n\n",
            m.spinner.View(),
            m.progress*100,
        )
    }
    return "\n ✓ Complete!\n"
}
```

#### Spinner Types and Configuration

```go
s := spinner.New()

// Available spinner types
s.Spinner = spinner.Dot
s.Spinner = spinner.Line
s.Spinner = spinner.MiniDot
s.Spinner = spinner.Jump
s.Spinner = spinner.Points
s.Spinner = spinner.Globe
s.Spinner = spinner.Moon
s.Spinner = spinner.Pipe
s.Spinner = spinner.SimpleDots
s.Spinner = spinner.Pulse
s.Spinner = spinner.Arrow
s.Spinner = spinner.Dots9
s.Spinner = spinner.Star
s.Spinner = spinner.Ellipsis
s.Spinner = spinner.Hamburger

// Custom spinner
customSpinner := spinner.Spinner{
    Frames: []string{"⣾ ", "⣽ ", "⣻ ", "⢿ "},
    FPS:    time.Second / 10, // 10 FPS
}
s.Spinner = customSpinner

// Styling
s.Style = lipgloss.NewStyle().
    Foreground(lipgloss.Color("62")).
    Bold(true)

s.SpinnerStyle = lipgloss.NewStyle().
    Foreground(lipgloss.Color("205"))

// Speed control
s.Spinner.FPS = time.Second / 20  // 20 FPS

// Lifecycle
s.Start()  // Start animation
s.Stop()   // Stop animation
s.Reset()  // Reset to first frame
```

### Progress Bar (`progress`)

Progress indicator with solid or gradient fills and percentage display.

```go
package main

import (
    "time"
    "github.com/charmbracelet/bubbles/progress"
    tea "github.com/charmbracelet/bubbletea"
)

type tickMsg time.Time

type Model struct {
    progress progress.Model
    percent  float64
    done     bool
}

func initialModel() Model {
    p := progress.New(
        progress.WithDefaultGradient(),
        progress.WithWidth(50),
        progress.WithoutPercentage(),
    )

    return Model{
        progress: p,
        percent:  0.0,
    }
}

func (m Model) Init() tea.Cmd {
    return tea.Tick(time.Millisecond*50, func(t time.Time) tea.Msg {
        return tickMsg(t)
    })
}

func (m Model) Update(msg tea.Msg) (tea.Model, tea.Cmd) {
    switch msg := msg.(type) {
    case tea.KeyMsg:
        if msg.Type == tea.KeyCtrlC {
            return m, tea.Quit
        }

    case tickMsg:
        if !m.done {
            m.percent += 0.005
            if m.percent >= 1.0 {
                m.done = true
                return m, tea.Quit
            }
            cmd := m.progress.SetPercent(m.percent)
            return m, tea.Batch(
                cmd,
                tea.Tick(time.Millisecond*50, func(t time.Time) tea.Msg {
                    return tickMsg(t)
                }),
            )
        }

    case progress.FrameMsg:
        var cmd tea.Cmd
        m.progress, cmd = m.progress.Update(msg)
        return m, cmd
    }

    return m, nil
}

func (m Model) View() string {
    if m.done {
        return "Download complete!\n"
    }
    return fmt.Sprintf(
        "Downloading... %s %.0f%%\n",
        m.progress.View(),
        m.percent*100,
    )
}
```

#### Progress Bar Configuration

```go
p := progress.New()

// Width and height
p = progress.WithWidth(60)(p)
p = progress.WithHeight(1)(p)  // For multi-line progress

// Gradient colors
p = progress.WithDefaultGradient()(p)
p = progress.WithGradient("#F25D94", "#F25D94")(p)
p = progress.WithSolidColor("#7D56F4")(p)

// Percentage display
p.ShowPercentage = true
p.PercentageStyle = lipgloss.NewStyle().
    Foreground(lipgloss.Color("255"))

// Full vs empty characters
p.Full = '█'
p.Empty = '░'
p.FullColor = "#7D56F4"
p.EmptyColor = "240"

// Custom rendering
p.Full = '='
p.Empty = '-'
p.Scale = 1.0  // Scale factor for characters

// Progress type
p.Percent = 0.75  // Directly set progress
p.SetPercent(0.5) // Method to set progress

// Getters
percent := p.Percent()
width := p.Width()
height := p.Height()

// Styling
p.ProgressStyle = lipgloss.NewStyle().
    Foreground(lipgloss.Color("205"))

p.EmptyStyle = lipgloss.NewStyle().
    Foreground(lipgloss.Color("240"))
```

### Table (`table`)

Scrollable table with column headers, row selection, and keyboard navigation.

```go
package main

import (
    "github.com/charmbracelet/bubbles/table"
    tea "github.com/charmbracelet/bubbletea"
    "github.com/charmbracelet/lipgloss"
)

type Model struct {
    table table.Model
}

func initialModel() Model {
    columns := []table.Column{
        {Title: "ID", Width: 10},
        {Title: "Name", Width: 25},
        {Title: "Email", Width: 35},
        {Title: "Status", Width: 15},
    }

    rows := []table.Row{
        {"1", "Alice Johnson", "alice@example.com", "Active"},
        {"2", "Bob Smith", "bob@example.com", "Inactive"},
        {"3", "Charlie Brown", "charlie@example.com", "Active"},
        {"4", "Diana Prince", "diana@example.com", "Pending"},
    }

    // Styling
    baseStyle := lipgloss.NewStyle().
        BorderStyle(lipgloss.NormalBorder()).
        BorderForeground(lipgloss.Color("240"))

    headerStyle := lipgloss.NewStyle().
        Bold(true).
        Foreground(lipgloss.Color("205")).
        Align(lipgloss.Center)

    selectedStyle := lipgloss.NewStyle().
        Foreground(lipgloss.Color("229")).
        Background(lipgloss.Color("62")).
        Bold(true)

    t := table.New(
        table.WithColumns(columns),
        table.WithRows(rows),
        table.WithFocused(true),
        table.WithHeight(7),
    )

    t.SetStyles(table.Styles{
        Header:   headerStyle,
        Selected: selectedStyle,
        Cell:     baseStyle,
    })

    return Model{table: t}
}

func (m Model) Init() tea.Cmd {
    return nil
}

func (m Model) Update(msg tea.Msg) (tea.Model, tea.Cmd) {
    var cmd tea.Cmd

    switch msg := msg.(type) {
    case tea.KeyMsg:
        switch msg.String() {
        case "q":
            return m, tea.Quit
        case "enter":
            selected := m.table.SelectedRow()
            return m, tea.Printf("Selected: %v", selected)
        }
    }

    m.table, cmd = m.table.Update(msg)
    return m, cmd
}

func (m Model) View() string {
    return baseStyle.Render(m.table.View()) +
           "\nPress q to quit, enter to select"
}
```

#### Table Configuration and Features

```go
// Column configuration
columns := []table.Column{
    {
        Title: "Name",
        Width: 25,
        // Custom alignment
    },
    {
        Title: "Description",
        Width: 40,
        // Optional custom rendering
    },
}

// Row operations
rows := []table.Row{
    {"1", "Item 1", "Description 1"},
    {"2", "Item 2", "Description 2"},
}

t := table.New(
    table.WithColumns(columns),
    table.WithRows(rows),
    table.WithFocused(true),
    table.WithHeight(10),
)

// Add rows dynamically
t.SetRows([]table.Row{
    {"3", "Item 3", "Description 3"},
})

// Append rows
t.AppendRow([]table.Row{{"4", "Item 4", "Description 4"}})
t.AppendRows([]table.Row{
    {"5", "Item 5", "Description 5"},
    {"6", "Item 6", "Description 6"},
})

// Row selection
selected := t.SelectedRow()
selectedIndex := t.Cursor()
t.SetCursor(2)  // Select row 3

// Scrolling
t.GotoTop()
t.GotoBottom()
t.SetRows(t.Rows()[5:15])  // Show rows 5-15

// Custom styles
t.SetStyles(table.Styles{
    Header: lipgloss.NewStyle().Bold(true),
    Cell:   lipgloss.NewStyle().Padding(0, 1),
    Selected: lipgloss.NewStyle().
        Background(lipgloss.Color("62")),
})

// Column-specific styles
t.WithColumnStyles([]lipgloss.Style{
    lipgloss.NewStyle().Align(lipgloss.Left),
    lipgloss.NewStyle().Align(lipgloss.Center),
    lipgloss.NewStyle().Align(lipgloss.Right),
})

// Borders
t.BorderStyle(lipgloss.NormalBorder())
t.Border(lipgloss.RoundedBorder())

// Getters
columns := t.Columns()
rows := t.Rows()
height := t.Height()
width := t.Width()
```

### List (`list`)

Feature-rich list with fuzzy filtering, pagination, and customizable item rendering.

```go
package main

import (
    "github.com/charmbracelet/bubbles/list"
    tea "github.com/charmbracelet/bubbletea"
    "github.com/charmbracelet/lipgloss"
)

type item struct {
    title, desc string
}

func (i item) Title() string       { return i.title }
func (i item) Description() string { return i.desc }
func (i item) FilterValue() string { return i.title }

type Model struct {
    list list.Model
}

func initialModel() Model {
    items := []list.Item{
        item{title: "Go", desc: "A statically typed, compiled language"},
        item{title: "Python", desc: "A high-level, interpreted language"},
        item{title: "Rust", desc: "A systems programming language"},
        item{title: "JavaScript", desc: "Dynamic scripting language"},
        item{title: "TypeScript", desc: "JavaScript with types"},
        item{title: "Java", desc: "Object-oriented programming language"},
    }

    // Custom delegate for item styling
    delegate := list.NewDefaultDelegate()
    delegate.ShowDescription = true
    delegate.DescriptionStyle = lipgloss.NewStyle().
        Foreground(lipgloss.Color("240"))

    l := list.New(items, delegate, 0, 0)
    l.Title = "Programming Languages"
    l.SetFilteringEnabled(true)
    l.SetShowStatusBar(true)
    l.SetShowPagination(true)
    l.SetShowHelp(true)

    // Styling
    l.Styles.Title = lipgloss.NewStyle().
        Bold(true).
        Foreground(lipgloss.Color("205"))

    l.Styles.StatusBar = lipgloss.NewStyle().
        Foreground(lipgloss.Color("240"))

    return Model{list: l}
}

func (m Model) Update(msg tea.Msg) (tea.Model, tea.Cmd) {
    switch msg := msg.(type) {
    case tea.KeyMsg:
        if msg.String() == "ctrl+c" {
            return m, tea.Quit
        }

    case tea.WindowSizeMsg:
        m.list.SetWidth(msg.Width)
        m.list.SetHeight(msg.Height - 4)  // Leave space for title
    }

    var cmd tea.Cmd
    m.list, cmd = m.list.Update(msg)
    return m, cmd
}

func (m Model) View() string {
    return "\n" + m.list.View()
}
```

#### List Features and Configuration

```go
// Basic setup
l := list.New(items, delegate, width, height)

// Title and status
l.Title = "My List"
l.SetShowTitle(true)
l.SetShowStatusBar(true)
l.SetShowPagination(true)
l.SetShowHelp(true)

// Filtering
l.SetFilteringEnabled(true)
l.FilterInput.Placeholder = "Search..."
l.FilterInput.SetValue("go")  // Pre-fill filter

// Pagination
l.Paginator.PerPage = 10
l.Paginator.ActiveDot = lipgloss.NewStyle().
    Foreground(lipgloss.Color("205")).Render("•")
l.Paginator.InactiveDot = lipgloss.NewStyle().
    Foreground(lipgloss.Color("240")).Render("•")

// Selection and navigation
l.SetItem(3)  // Select item at index 3
selected := l.SelectedItem()  // Get selected item
l.Select(2)   // Select by index

// Items
l.InsertItem(2, newItem)  // Insert at position
l.RemoveItem(1)           // Remove at position
l.SetItems(newItems)      // Replace all items

// Custom delegate
type customDelegate struct {
    list.DefaultDelegate
}

func (d customDelegate) Render(w io.Writer, m list.Model, index int, item list.Item) {
    // Custom rendering logic
    fmt.Fprintf(w, "→ %s", item.Title())
}

// Status messages
l.NewStatusMessage("Loading...")
l.StatusMessageLifetime = time.Second * 3

// Keybinding customization
l.KeyMap.CursorUp = key.NewBinding(
    key.WithKeys("k", "up"),
    key.WithHelp("↑/k", "up"),
)

l.KeyMap.Filter = key.NewBinding(
    key.WithKeys("/"),
    key.WithHelp("/", "filter"),
)

// Getters
items := l.Items()
width := l.Width()
height := l.Height()
filter := l.Filter()
```

### Paginator (`paginator`)

Pagination logic and rendering with dot-style or numeric page display.

```go
package main

import (
    "github.com/charmbracelet/bubbles/paginator"
    tea "github.com/charmbracelet/bubbletea"
    "github.com/charmbracelet/lipgloss"
)

type Model struct {
    paginator paginator.Model
    items     []string
}

func initialModel() Model {
    items := make([]string, 100)
    for i := range items {
        items[i] = fmt.Sprintf("Item %d", i+1)
    }

    p := paginator.New()
    p.Type = paginator.Dots
    p.PerPage = 5
    p.ActiveDot = lipgloss.NewStyle().
        Foreground(lipgloss.Color("205")).Render("●")
    p.InactiveDot = lipgloss.NewStyle().
        Foreground(lipgloss.Color("240")).Render("○")

    p.SetTotalPages(len(items))

    return Model{
        paginator: p,
        items:     items,
    }
}

func (m Model) Update(msg tea.Msg) (tea.Model, tea.Cmd) {
    var cmd tea.Cmd

    switch msg := msg.(type) {
    case tea.KeyMsg:
        switch msg.String() {
        case "q":
            return m, tea.Quit
        }
    }

    m.paginator, cmd = m.paginator.Update(msg)
    return m, cmd
}

func (m Model) View() string {
    start, end := m.paginator.GetSliceBounds(len(m.items))

    var content strings.Builder
    content.WriteString("Items:\n\n")

    for i, item := range m.items[start:end] {
        content.WriteString(fmt.Sprintf("  • %s\n", item))
    }

    content.WriteString("\n")
    content.WriteString(m.paginator.View())

    return content.String()
}
```

#### Paginator Types and Configuration

```go
p := paginator.New()

// Pagination types
p.Type = paginator.Dots          // ● ○ ○ ○
p.Type = paginator.Arabic        // 1 2 3 4
p.Type = paginator.ArabicCompact // 1/10

// Page configuration
p.PerPage = 10
p.SetTotalPages(15)  // Based on item count

// Navigation
p.NextPage()
p.PrevPage()
p.Page(3)  // Go to specific page
p.OnLastPage()
p.OnFirstPage()

// Custom separators and dots
p.ArabicSeparator = " / "
p.ActiveDot = lipgloss.NewStyle().
    Foreground(lipgloss.Color("205")).Render("●")
p.InactiveDot = lipgloss.NewStyle().
    Foreground(lipgloss.Color("240")).Render("○")

// Slice bounds
start, end := p.GetSliceBounds(totalItems)
items := allItems[start:end]

// Getters
page := p.Page()
totalPages := p.TotalPages()
perPage := p.PerPage()
onLastPage := p.OnLastPage()

// Keyboard controls (default)
// - Left/H: Previous page
// - Right/L: Next page
// - Home/G: First page
// - End/G: Last page
```

### Timer (`timer`)

Countdown timer with configurable interval and timeout handling.

```go
package main

import (
    "time"
    "github.com/charmbracelet/bubbles/timer"
    tea "github.com/charmbracelet/bubbletea"
    "github.com/charmbracelet/lipgloss"
)

type Model struct {
    timer timer.Model
    interval time.Duration
}

func initialModel() Model {
    // 30-second timer with 1-second intervals
    t := timer.NewWithInterval(30*time.Second, time.Second)

    // Styling
    t.Style = lipgloss.NewStyle().
        Foreground(lipgloss.Color("205")).
        Bold(true)

    t.TimeoutStyle = lipgloss.NewStyle().
        Foreground(lipgloss.Color("9")).
        Bold(true)

    return Model{
        timer: t,
        interval: time.Second,
    }
}

func (m Model) Init() tea.Cmd {
    return m.timer.Init()
}

func (m Model) Update(msg tea.Msg) (tea.Model, tea.Cmd) {
    switch msg := msg.(type) {
    case timer.TimeoutMsg:
        return m, tea.Quit  // Timer finished

    case timer.TickMsg:
        var cmd tea.Cmd
        m.timer, cmd = m.timer.Update(msg)
        return m, cmd

    case tea.KeyMsg:
        switch msg.String() {
        case "q", "ctrl+c":
            return m, tea.Quit
        case " ":
            // Toggle timer
            m.timer.Toggle()
        case "r":
            // Reset timer
            m.timer.Reset()
        }
    }

    return m, nil
}

func (m Model) View() string {
    return fmt.Sprintf(
        "\nTimer: %s\n\nSpace: Start/Stop | R: Reset | Q: Quit\n",
        m.timer.View(),
    )
}
```

#### Timer Configuration

```go
// Create timer
t := timer.New(60 * time.Second)  // Simple 60-second timer
t := timer.NewWithInterval(60*time.Second, time.Millisecond*500)

// Duration and interval
t.Timeout = 2 * time.Minute
t.Interval = time.Second

// Control
t.Start()      // Start timer
t.Stop()       // Stop timer
t.Toggle()     // Start/stop toggle
t.Reset()      // Reset to initial timeout

// State
t.Running()    // Is timer running?
t.Timedout()   // Has timer finished?

// Styling
t.Style = lipgloss.NewStyle().
    Foreground(lipgloss.Color("205"))

t.TimeoutStyle = lipgloss.NewStyle().
    Foreground(lipgloss.Color("9")).
    Bold(true)

// Time access
remaining := t.Timout() - time.Since(t.StartTime)
elapsed := time.Since(t.StartTime)
```

### Viewport (`viewport`)

Vertically scrollable content area with mouse wheel support.

```go
package main

import (
    "strings"
    "github.com/charmbracelet/bubbles/viewport"
    tea "github.com/charmbracelet/bubbletea"
)

type Model struct {
    viewport viewport.Model
    content  string
    ready    bool
}

func initialModel() Model {
    content := strings.Repeat("Hello, World! This is a long line that will wrap.\n", 50)
    return Model{
        content: content,
    }
}

func (m Model) Update(msg tea.Msg) (tea.Model, tea.Cmd) {
    switch msg := msg.(type) {
    case tea.KeyMsg:
        switch msg.String() {
        case "q", "ctrl+c":
            return m, tea.Quit
        case "r":
            m.viewport.GotoTop()
        }

    case tea.MouseMsg:
        // Handle mouse wheel scrolling
        if msg.Action == tea.MouseActionPress && msg.Button == tea.MouseButtonWheelUp {
            m.viewport.LineUp(3)
        } else if msg.Action == tea.MouseActionPress && msg.Button == tea.MouseButtonWheelDown {
            m.viewport.LineDown(3)
        }

    case tea.WindowSizeMsg:
        if !m.ready {
            m.viewport = viewport.New(msg.Width, msg.Height-2)  // Leave space for status
            m.viewport.SetContent(m.content)
            m.ready = true
        } else {
            m.viewport.Width = msg.Width
            m.viewport.Height = msg.Height - 2
        }
    }

    var cmd tea.Cmd
    m.viewport, cmd = m.viewport.Update(msg)
    return m, cmd
}

func (m Model) View() string {
    if !m.ready {
        return "Initializing..."
    }

    return m.viewport.View() +
           "\n↑/↓/PgUp/PgDn: Scroll | R: Top | Q: Quit"
}
```

#### Viewport Features

```go
v := viewport.New(width, height)

// Content management
v.SetContent("Long content here...")
content := v.GetContent()

// Size
v.Width = 80
v.Height = 24

// Navigation
v.GotoTop()
v.GotoBottom()
v.LineUp(1)      // Scroll up 1 line
v.LineDown(1)    // Scroll down 1 line
v.HalfViewUp()   // Scroll up half viewport
v.HalfViewDown() // Scroll down half viewport
v.GotoLine(50)   // Jump to line 50

// Position
line := v.YOffset()      // Current line offset
percent := v.ScrollPercent()  // Scroll position (0-1)
v.SetYOffset(10)        // Set specific offset

// Mouse support
v.KeyMap.PageUp = key.NewBinding(key.WithKeys("pgup"))
v.KeyMap.PageDown = key.NewBinding(key.WithKeys("pgdown"))
v.KeyMap.HalfPageUp = key.NewBinding(key.WithKeys("ctrl+u"))
v.KeyMap.HalfPageDown = key.NewBinding(key.WithKeys("ctrl+d"))

// Styling
v.Style = lipgloss.NewStyle().
    Border(lipgloss.NormalBorder()).
    BorderForeground(lipgloss.Color("240"))

// Custom key bindings
v.KeyMap.Up = key.NewBinding(
    key.WithKeys("k", "up"),
    key.WithHelp("↑/k", "scroll up"),
)
```

### File Picker (`filepicker`)

Navigate filesystem and select files with optional filtering.

```go
package main

import (
    "github.com/charmbracelet/bubbles/filepicker"
    tea "github.com/charmbracelet/bubbletea"
)

type Model struct {
    filepicker filepicker.Model
    selected   string
    quitting   bool
}

func initialModel() Model {
    fp := filepicker.New()

    // Configuration
    fp.CurrentDirectory = "."
    fp.ShowHidden = false
    fp.AutoHeight = true
    fp.AllowedTypes = []string{".go", ".md", ".txt"}

    // Styling
    fp.Styles.Selected = lipgloss.NewStyle().
        Background(lipgloss.Color("62")).
        Foreground(lipgloss.Color("230"))

    fp.Styles.Cursor = lipgloss.NewStyle().
        Background(lipgloss.Color("205"))

    return Model{filepicker: fp}
}

func (m Model) Init() tea.Cmd {
    return m.filepicker.Init()
}

func (m Model) Update(msg tea.Msg) (tea.Model, tea.Cmd) {
    switch msg := msg.(type) {
    case tea.KeyMsg:
        switch msg.String() {
        case "ctrl+c", "q":
            m.quitting = true
            return m, tea.Quit
        }
    }

    var cmd tea.Cmd
    m.filepicker, cmd = m.filepicker.Update(msg)

    // Check if file was selected
    if didSelect, path := m.filepicker.DidSelectFile(msg); didSelect {
        m.selected = path
        m.quitting = true
        return m, tea.Batch(
            tea.Printf("Selected: %s", path),
            cmd,
        )
    }

    // Check if directory was selected
    if didSelect, path := m.filepicker.DidSelectDisabledFile(msg); didSelect {
        return m, tea.Batch(
            tea.Printf("Can't select %s: disabled file type", path),
            cmd,
        )
    }

    return m, cmd
}

func (m Model) View() string {
    if m.quitting {
        if m.selected != "" {
            return fmt.Sprintf("Selected file: %s\n", m.selected)
        }
        return ""
    }

    return "\n" + m.filepicker.View() +
           "\n↑/↓: Navigate | Enter: Select | Q: Quit"
}
```

#### File Picker Configuration

```go
fp := filepicker.New()

// Basic configuration
fp.CurrentDirectory = "/home/user"
fp.ShowHidden = false
fp.AutoHeight = true

// File filtering
fp.AllowedTypes = []string{".go", ".md", ".txt"}
fp.DisabledTypes = []string{".exe", ".dll"}
fp.DirectoryAllowed = true  // Allow directory selection

// Navigation
fp.GoToCurrentDirectory()
fp.Cd("..")
fp.Cd("/path/to/directory")

// Path operations
path := fp.Path()
dir := fp.CurrentDirectory()
name := fp.CurrentSelected()

// Selection handling
if didSelect, path := fp.DidSelectFile(msg); didSelect {
    // File was selected
}

if didSelect, path := fp.DidSelectDirectory(msg); didSelect {
    // Directory was selected
}

if didSelect, path := fp.DidSelectDisabledFile(msg); didSelect {
    // Disabled file type was selected
}

// Styling
fp.Styles.Cursor = lipgloss.NewStyle().
    Background(lipgloss.Color("205"))

fp.Styles.Selected = lipgloss.NewStyle().
    Background(lipgloss.Color("62"))

fp.Styles.Directory = lipgloss.NewStyle().
    Foreground(lipgloss.Color("69")).
    Bold(true)

fp.Styles.File = lipgloss.NewStyle().
    Foreground(lipgloss.Color("255"))

fp.Styles.Disabled = lipgloss.NewStyle().
    Foreground(lipgloss.Color("240"))

// Key bindings
fp.KeyMap.Up = key.NewBinding(key.WithKeys("k", "up"))
fp.KeyMap.Down = key.NewBinding(key.WithKeys("j", "down"))
fp.KeyMap.Select = key.NewBinding(key.WithKeys("enter"))
fp.KeyMap.UpLevel = key.NewBinding(key.WithKeys("h", "left"))
```

### Key Bindings and Help (`key`, `help`)

Define and manage keybindings with help text.

```go
package main

import (
    "github.com/charmbracelet/bubbles/key"
    "github.com/charmbracelet/bubbles/help"
    tea "github.com/charmbracelet/bubbletea"
)

type keyMap struct {
    Up    key.Binding
    Down  key.Binding
    Left  key.Binding
    Right key.Binding
    Quit  key.Binding
    Help  key.Binding
    Enter key.Binding
}

func (k keyMap) ShortHelp() []key.Binding {
    return []key.Binding{k.Up, k.Down, k.Quit, k.Help}
}

func (k keyMap) FullHelp() [][]key.Binding {
    return [][]key.Binding{
        {k.Up, k.Down, k.Left, k.Right},
        {k.Enter, k.Help, k.Quit},
    }
}

type Model struct {
    keys   keyMap
    help   help.Model
    x, y   int
}

func initialModel() Model {
    keys := keyMap{
        Up: key.NewBinding(
            key.WithKeys("k", "up"),
            key.WithHelp("↑/k", "move up"),
            key.WithDisabled(),  // Initially disabled
        ),
        Down: key.NewBinding(
            key.WithKeys("j", "down"),
            key.WithHelp("↓/j", "move down"),
        ),
        Left: key.NewBinding(
            key.WithKeys("h", "left"),
            key.WithHelp("←/h", "move left"),
        ),
        Right: key.NewBinding(
            key.WithKeys("l", "right"),
            key.WithHelp("→/l", "move right"),
        ),
        Enter: key.NewBinding(
            key.WithKeys("enter"),
            key.WithHelp("enter", "confirm"),
        ),
        Help: key.NewBinding(
            key.WithKeys("?"),
            key.WithHelp("?", "toggle help"),
        ),
        Quit: key.NewBinding(
            key.WithKeys("q", "ctrl+c"),
            key.WithHelp("q", "quit"),
        ),
    }

    return Model{
        keys: keys,
        help: help.New(),
    }
}

func (m Model) Update(msg tea.Msg) (tea.Model, tea.Cmd) {
    switch msg := msg.(type) {
    case tea.KeyMsg:
        switch {
        case key.Matches(msg, m.keys.Quit):
            return m, tea.Quit

        case key.Matches(msg, m.keys.Help):
            m.help.ShowAll = !m.help.ShowAll

        case key.Matches(msg, m.keys.Up):
            m.y--
            m.keys.Up.SetEnabled(m.y > 0)  // Enable/disable based on state

        case key.Matches(msg, m.keys.Down):
            m.y++

        case key.Matches(msg, m.keys.Left):
            m.x--

        case key.Matches(msg, m.keys.Right):
            m.x++

        case key.Matches(msg, m.keys.Enter):
            return m, tea.Printf("Position: (%d, %d)", m.x, m.y)
        }
    }

    return m, nil
}

func (m Model) View() string {
    content := fmt.Sprintf("Position: (%d, %d)", m.x, m.y)

    return lipgloss.JoinVertical(
        lipgloss.Left,
        content,
        "\n",
        m.help.View(m.keys),
    )
}
```

#### Key Binding Features

```go
// Creating key bindings
k := key.NewBinding(
    key.WithKeys("ctrl+c", "q"),
    key.WithHelp("q", "quit"),
    key.WithDisabled(),  // Start disabled
    key.WithHelp("q", "quit (disabled)"),  // Disabled help text
)

// Matching key events
if key.Matches(msg, quitKey) {
    // Handle quit
}

// Enabling/disabling
k.SetEnabled(true)
k.SetEnabled(false)
k.Enabled()  // Check if enabled

// Help text
k.Help()     // Get help text
k.SetHelp("q", "quit")  // Update help text

// Keys
k.Keys()     // Get all keys for this binding

// Key groups
type keyGroup struct {
    movement  key.Binding
    selection key.Binding
    control   key.Binding
}

// Help configuration
helpModel := help.New()
helpModel.ShowAll = false  // Show only short help initially
helpModel.Width = 80

// Help styling
helpModel.Styles.ShortKey = lipgloss.NewStyle().
    Foreground(lipgloss.Color("240"))

helpModel.Styles.ShortDesc = lipgloss.NewStyle().
    Foreground(lipgloss.Color("240"))

helpModel.Styles.FullKey = lipgloss.NewStyle().
    Foreground(lipgloss.Color("205"))

helpModel.Styles.FullDesc = lipgloss.NewStyle().
    Foreground(lipgloss.Color("240"))

// Separator customization
helpModel.Styles.Separator = lipgloss.NewStyle().
    Foreground(lipgloss.Color("240")).
    SetString(" • ")
```

## Styling with Lip Gloss

Bubbles components use Lip Gloss for styling. Here are common styling patterns:

```go
import "github.com/charmbracelet/lipgloss"

// Color definitions
primaryColor := lipgloss.Color("62")      // Purple
secondaryColor := lipgloss.Color("205")   // Pink
accentColor := lipgloss.Color("226")      // Yellow
textColor := lipgloss.Color("255")        // White
mutedColor := lipgloss.Color("240")       // Gray

// Base styles
baseStyle := lipgloss.NewStyle().
    Foreground(textColor).
    Padding(1, 2)

primaryStyle := lipgloss.NewStyle().
    Foreground(textColor).
    Background(primaryColor).
    Bold(true).

mutedStyle := lipgloss.NewStyle().
    Foreground(mutedColor).

selectedStyle := lipgloss.NewStyle().
    Background(accentColor).
    Foreground(lipgloss.Color("16")).  // Black text
    Bold(true)

// Border styles
borderStyle := lipgloss.NewStyle().
    Border(lipgloss.RoundedBorder()).
    BorderForeground(primaryColor)

// Apply styles to components
ti.Style = baseStyle
ti.PlaceholderStyle = mutedStyle
ti.CursorStyle = primaryStyle

s.Style = primaryStyle
s.SpinnerStyle = secondaryStyle

t.SetStyles(table.Styles{
    Header:   primaryStyle,
    Selected: selectedStyle,
    Cell:     baseStyle,
})

l.Styles.Title = primaryStyle
l.Styles.Selected = selectedStyle
```

## Integration Patterns

### Multi-Component Layout

```go
type Model struct {
    textInput textinput.Model
    list      list.Model
    table     table.Model
    active    int  // 0=text, 1=list, 2=table
}

func (m Model) Update(msg tea.Msg) (tea.Model, tea.Cmd) {
    var cmd tea.Cmd

    switch msg := msg.(type) {
    case tea.KeyMsg:
        switch msg.String() {
        case "tab":
            m.active = (m.active + 1) % 3
            return m, nil
        case "shift+tab":
            m.active = (m.active - 1 + 3) % 3
            return m, nil
        }
    }

    // Update only active component
    switch m.active {
    case 0:
        m.textInput, cmd = m.textInput.Update(msg)
    case 1:
        m.list, cmd = m.list.Update(msg)
    case 2:
        m.table, cmd = m.table.Update(msg)
    }

    return m, cmd
}

func (m Model) View() string {
    textBorder := lipgloss.NormalBorder()
    if m.active == 0 {
        textBorder = lipgloss.RoundedBorder()
    }

    listBorder := lipgloss.NormalBorder()
    if m.active == 1 {
        listBorder = lipgloss.RoundedBorder()
    }

    tableBorder := lipgloss.NormalBorder()
    if m.active == 2 {
        tableBorder = lipgloss.RoundedBorder()
    }

    text := lipgloss.NewStyle().
        Border(textBorder).
        Padding(1).
        Render(m.textInput.View())

    list := lipgloss.NewStyle().
        Border(listBorder).
        Padding(1).
        Height(20).
        Render(m.list.View())

    table := lipgloss.NewStyle().
        Border(tableBorder).
        Padding(1).
        Render(m.table.View())

    return lipgloss.JoinVertical(
        lipgloss.Left,
        text,
        list,
        table,
    )
}
```

### Custom Component Messages

```go
type FormSubmitMsg string
type ValidationErrorMsg error

type FormModel struct {
    nameInput  textinput.Model
    emailInput textinput.Model
    errors     []string
}

func (m FormModel) Update(msg tea.Msg) (tea.Model, tea.Cmd) {
    var cmd tea.Cmd

    switch msg := msg.(type) {
    case tea.KeyMsg:
        if msg.Type == tea.KeyEnter {
            // Validate form
            if m.nameInput.Value() == "" {
                m.errors = append(m.errors, "Name is required")
                return m, nil
            }

            if m.emailInput.Value() == "" {
                m.errors = append(m.errors, "Email is required")
                return m, nil
            }

            // Form is valid, submit
            return m, func() tea.Msg {
                return FormSubmitMsg(m.nameInput.Value())
            }
        }
    case ValidationErrorMsg:
        m.errors = append(m.errors, msg.Error())
        return m, nil
    }

    // Update inputs
    m.nameInput, cmd = m.nameInput.Update(msg)
    return m, cmd
}

func (m FormModel) View() string {
    var view strings.Builder

    if len(m.errors) > 0 {
        errorStyle := lipgloss.NewStyle().
            Foreground(lipgloss.Color("9")).
            Bold(true)

        for _, err := range m.errors {
            view.WriteString(errorStyle.Render("Error: " + err + "\n"))
        }
    }

    view.WriteString("Name: " + m.nameInput.View() + "\n")
    view.WriteString("Email: " + m.emailInput.View() + "\n")
    view.WriteString("\nEnter to submit, Tab to switch fields")

    return view.String()
}
```

## Best Practices

### Component Initialization

```go
// Use factory functions for consistent initialization
func NewTextInput() textinput.Model {
    ti := textinput.New()
    ti.Placeholder = "Enter text..."
    ti.Style = baseStyle
    ti.CursorStyle = primaryStyle
    return ti
}

func NewTable() table.Model {
    return table.New(
        table.WithFocused(true),
        table.WithHeight(10),
    )
}
```

### State Management

```go
// Keep component state separate from application state
type AppState struct {
    user    User
    loading bool
    error   error
}

type Model struct {
    state   AppState
    input   textinput.Model
    table   table.Model
    spinner spinner.Model
}

// Update application state based on component messages
func (m Model) Update(msg tea.Msg) (tea.Model, tea.Cmd) {
    switch msg := msg.(type) {
    case UserDataLoadedMsg:
        m.state.user = msg.User
        m.state.loading = false
        // Update table with new data
        m.table.SetRows(userToTableRows(msg.User))

    case ErrorMsg:
        m.state.error = msg.Error
        m.state.loading = false
    }

    return m, nil
}
```

### Performance Optimization

```go
// Batch commands for better performance
func (m Model) Init() tea.Cmd {
    return tea.Batch(
        loadUserData(),
        loadConfig(),
        m.spinner.Tick,
    )
}

// Debounce rapid updates
type debouncedUpdateMsg struct{}
var updateTimer *time.Timer

func (m Model) scheduleUpdate() tea.Cmd {
    if updateTimer != nil {
        updateTimer.Stop()
    }

    updateTimer = time.AfterFunc(100*time.Millisecond, func() {
        p.Send(debouncedUpdateMsg{})
    })

    return nil
}
```

### Error Handling

```go
// Graceful error handling with fallbacks
func (m Model) handleComponentError(err error) (tea.Model, tea.Cmd) {
    m.state.error = err

    // Log error
    log.Printf("Component error: %v", err)

    // Maybe show user-friendly message
    return m, tea.Printf("An error occurred: %s", err.Error())
}

// Validation with proper error types
func validateEmail(email string) error {
    if !strings.Contains(email, "@") {
        return ValidationError{
            Field:   "email",
            Message: "must contain @ symbol",
        }
    }
    return nil
}
```

### Testing Components

```go
func TestTextInput(t *testing.T) {
    ti := textinput.New()

    // Test basic functionality
    ti.SetValue("hello")
    assert.Equal(t, "hello", ti.Value())

    // Test cursor movement
    ti.SetCursor(2)
    assert.Equal(t, 2, ti.Cursor())

    // Test input handling
    model := Model{textInput: ti}
    updatedModel, _ := model.Update(tea.KeyMsg{
        Type:  tea.KeyRunes,
        Runes: []rune("!"),
    })

    assert.Equal(t, "he!llo", updatedModel.textInput.Value())
}

func TestTableSelection(t *testing.T) {
    rows := []table.Row{
        {"1", "Alice"},
        {"2", "Bob"},
    }

    tbl := table.New(table.WithRows(rows))
    assert.Equal(t, 0, tbl.Cursor())

    // Test navigation
    tbl, _ = tbl.Update(tea.KeyMsg{Type: tea.KeyDown})
    assert.Equal(t, 1, tbl.Cursor())

    // Test selection
    selected := tbl.SelectedRow()
    assert.Equal(t, []string{"2", "Bob"}, selected)
}
```

## Advanced Usage

### Custom Component Creation

```go
// Custom component implementing Bubble Tea model
type CustomComponent struct {
    items    []string
    cursor   int
    selected map[int]struct{}
    width    int
}

func NewCustomComponent(items []string) CustomComponent {
    return CustomComponent{
        items:    items,
        selected: make(map[int]struct{}),
    }
}

func (c CustomComponent) Init() tea.Cmd {
    return nil
}

func (c CustomComponent) Update(msg tea.Msg) (CustomComponent, tea.Cmd) {
    switch msg := msg.(type) {
    case tea.KeyMsg:
        switch msg.Type {
        case tea.KeyUp:
            if c.cursor > 0 {
                c.cursor--
            }
        case tea.KeyDown:
            if c.cursor < len(c.items)-1 {
                c.cursor++
            }
        case tea.KeyEnter:
            c.selected[c.cursor] = struct{}{}
        }
    case tea.WindowSizeMsg:
        c.width = msg.Width
    }

    return c, nil
}

func (c CustomComponent) View() string {
    var view strings.Builder

    for i, item := range c.items {
        cursor := " "
        if i == c.cursor {
            cursor = ">"
        }

        selected := " "
        if _, ok := c.selected[i]; ok {
            selected = "✓"
        }

        view.WriteString(fmt.Sprintf("%s [%s] %s\n", cursor, selected, item))
    }

    return view.String()
}
```

### Component Composition

```go
// Composite component combining multiple bubbles
type FormBuilder struct {
    fields []textinput.Model
    labels []string
    errors []string
    focused int
}

func NewFormBuilder(fields, labels []string) FormBuilder {
    var inputs []textinput.Model

    for i, field := range fields {
        ti := textinput.New()
        ti.Placeholder = field
        ti.CharLimit = 50

        if i == 0 {
            ti.Focus()
        }

        inputs = append(inputs, ti)
    }

    return FormBuilder{
        fields:  inputs,
        labels:  labels,
        focused: 0,
    }
}

func (fb FormBuilder) Update(msg tea.Msg) (FormBuilder, tea.Cmd) {
    var cmd tea.Cmd

    switch msg := msg.(type) {
    case tea.KeyMsg:
        switch msg.Type {
        case tea.KeyTab:
            fb.fields[fb.focused].Blur()
            fb.focused = (fb.focused + 1) % len(fb.fields)
            fb.fields[fb.focused].Focus()

        case tea.KeyShiftTab:
            fb.fields[fb.focused].Blur()
            fb.focused = (fb.focused - 1 + len(fb.fields)) % len(fb.fields)
            fb.fields[fb.focused].Focus()

        case tea.KeyEnter:
            return fb, fb.validateAndSubmit()
        }
    }

    fb.fields[fb.focused], cmd = fb.fields[fb.focused].Update(msg)
    return fb, cmd
}

func (fb FormBuilder) validateAndSubmit() tea.Cmd {
    var values []string

    for _, field := range fb.fields {
        if field.Value() == "" {
            return func() tea.Msg {
                return ValidationErrorMsg("All fields are required")
            }
        }
        values = append(values, field.Value())
    }

    return func() tea.Msg {
        return FormSubmitMsg(values)
    }
}

func (fb FormBuilder) View() string {
    var view strings.Builder

    for i, field := range fb.fields {
        view.WriteString(fb.labels[i] + ": " + field.View() + "\n\n")
    }

    return view.String()
}
```

## Troubleshooting

### Common Issues

#### Component Not Receiving Input

```go
// Problem: Component not receiving key events
// Solution: Ensure component is focused or check message handling

// Make sure component is focused
ti.Focus()
// not focused.FBlur()

// Check message order - let component handle first
func (m Model) Update(msg tea.Msg) (tea.Model, tea.Cmd) {
    var cmd tea.Cmd

    // Update component first
    m.textInput, cmd = m.textInput.Update(msg)

    // Then handle application-level messages
    switch msg := msg.(type) {
    case tea.KeyMsg:
        if msg.Type == tea.KeyCtrlC {
            return m, tea.Quit
        }
        // Don't handle keys that component might need
    }

    return m, cmd
}
```

#### Styling Issues

```go
// Problem: Styles not applying
// Solution: Check color support and renderer

// Check color profile
fmt.Printf("Color profile: %v\n", lipgloss.DefaultRenderer().ColorProfile())

// Force specific color profile
renderer := lipgloss.NewRenderer(os.Stdout)
renderer.SetColorProfile(lipgloss.TrueColor)

// Use adaptive colors for better compatibility
style := lipgloss.NewStyle().
    Foreground(lipgloss.AdaptiveColor{Light: "63", Dark: "228"})
```

#### Performance Issues

```go
// Problem: Slow rendering
// Solution: Batch updates and limit frame rate

// Limit frame rate
p := tea.NewProgram(model, tea.WithFPS(30))

// Batch expensive operations
func (m Model) Update(msg tea.Msg) (tea.Model, tea.Cmd) {
    switch msg := msg.(type) {
    case tea.KeyMsg:
        if msg.Type == tea.KeyEnter {
            return m, tea.Batch(
                expensiveOperation1(),
                expensiveOperation2(),
                expensiveOperation3(),
            )
        }
    }
    return m, nil
}
```

#### Memory Leaks

```go
// Problem: Memory usage growing
// Solution: Clean up resources and limit data

// Clean up in quit
func (m Model) Update(msg tea.Msg) (tea.Model, tea.Cmd) {
    switch msg := msg.(type) {
    case tea.QuitMsg:
        if m.conn != nil {
            m.conn.Close()
        }
        if m.timer != nil {
            m.timer.Stop()
        }
    }
    return m, nil
}

// Limit data size
const MAX_ITEMS = 1000

func (m Model) AddItems(items []string) Model {
    if len(m.items) > MAX_ITEMS {
        m.items = m.items[len(m.items)-MAX_ITEMS:]
    }

    m.items = append(m.items, items...)
    return m
}
```

### Debugging

```go
// Enable logging
func main() {
    f, err := tea.LogToFile("debug.log", "debug")
    if err != nil {
        log.Fatal(err)
    }
    defer f.Close()

    p := tea.NewProgram(model)
    if _, err := p.Run(); err != nil {
        log.Fatal(err)
    }
}

// Debug messages
func (m Model) Update(msg tea.Msg) (tea.Model, tea.Cmd) {
    log.Printf("Received message: %T", msg)

    switch msg := msg.(type) {
    case tea.KeyMsg:
        log.Printf("Key pressed: %s", msg.String())
    }

    return m, nil
}

// Component state debugging
func (m Model) DebugState() string {
    return fmt.Sprintf(`
Cursor: %d
Value: %q
Focused: %v
Width: %d
CharLimit: %d
`, m.textInput.Cursor(), m.textInput.Value(),
   m.textInput.Focused(), m.textInput.Width(), m.textInput.CharLimit())
}
```

## Conclusion

Bubbles provides a comprehensive set of production-ready components for building sophisticated terminal user interfaces in Go. Each component follows the Bubble Tea Model-View-Update pattern, making them easy to integrate into applications while maintaining clean separation of concerns.

Key advantages include:

- **Consistency**: All components follow the same patterns and styling system
- **Flexibility**: Extensive customization options for appearance and behavior
- **Performance**: Optimized rendering and efficient state management
- **Accessibility**: Full keyboard navigation and mouse support where appropriate
- **Integration**: Seamless integration with Bubble Tea and Lip Gloss

When using Bubbles, remember to:

1. **Initialize components properly** with appropriate configuration
2. **Handle component messages** in your Update function
3. **Style consistently** using Lip Gloss
4. **Test thoroughly** including edge cases and error conditions
5. **Optimize for performance** by batching commands and limiting data

For more advanced usage, consider creating custom components that follow the same patterns, and leverage the styling system for consistent visual design across your application.

---

**Additional Resources:**

- [Bubbles GitHub Repository](https://github.com/charmbracelet/bubbles)
- [Bubble Tea Documentation](https://github.com/charmbracelet/bubbletea)
- [Lip Gloss Styling Guide](https://github.com/charmbracelet/lipgloss)
- [Charm Documentation](https://charm.sh/)