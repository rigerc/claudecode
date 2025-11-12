# Bubbles Component API Reference

This document provides comprehensive API documentation for all Bubbles components, including methods, configuration options, and usage examples.

## Text Input (textinput)

### Initialization

```go
func New() textinput.Model
```

### Configuration Methods

```go
func (m *Model) SetValue(string)
func (m *Model) Value() string
func (m *Model) SetCursor(int)
func (m *Model) Cursor() int
func (m *Model) SetWidth(int)
func (m *Model) SetCharLimit(int)
func (m *Model) Focus()
func (m *Model) Blur()
func (m *Model) Focused() bool
func (m *Model) SetPlaceholder(string)
func (m *Model) SetEchoMode(EchoMode)
```

### Echo Modes

```go
const (
    EchoNormal    EchoMode = iota // Show characters
    EchoPassword                 // Hide characters
    EchoNone                      // No echo at all
)
```

### Validation

```go
func (m *Model) Validate func(string) error
```

### Key Bindings

```go
type KeyMap struct {
    CharacterDelete        key.Binding
    CharacterDeleteBackward key.Binding
    CharacterForward      key.Binding
    CharacterBackward     key.Binding
    DeleteAfterCursor     key.Binding
    DeleteBeforeCursor    key.Binding
    DeleteWordBackward    key.Binding
    DeleteWordForward     key.Binding
    EndOfInput            key.Binding
    GoToStartOfInput      key.Binding
    InsertNewline         key.Binding
    AcceptSuggestion      key.Binding
    NextSuggestion        key.Binding
    PreviousSuggestion    key.Binding
}
```

## Text Area (textarea)

### Initialization

```go
func New() textarea.Model
```

### Configuration

```go
func (m *Model) SetWidth(int)
func (m *Model) SetHeight(int)
func (m *Model) SetCursor(line, column int)
func (m *Model) Cursor() (line, column int)
func (m *Model) SetValue(string)
func (m *Model) Value() string
func (m *Model) Focus()
func (m *Model) Blur()
func (m *Model) Focused() bool
func (m *Model) SetCharLimit(int)
func (m *Model) ShowLineNumbers(bool)
func (m *Model) SetPlaceholder(string)
```

### Content Manipulation

```go
func (m *Model) InsertString(string)
func (m *Model) DeleteWordForward()
func (m *Model) DeleteWordBackward()
func (m *Model) DeleteLine()
func (m *Model) InsertLine(string)
func (m *Model) LineCount() int
func (m *Model) CurrentLine() int
func (m *Model) LineContent(int) string
```

## Spinner (spinner)

### Initialization

```go
func New() spinner.Model
```

### Configuration

```go
func (m *Model) Tick() tea.Cmd
func (m *Model) Style(lipgloss.Style)
func (m *Model) SpinnerStyle(lipgloss.Style)
func (m *Model) Start()
func (m *Model) Stop()
func (m *Model) Reset()
```

### Spinner Types

```go
const (
    Line       Spinner = iota
    Dot
    MiniDot
    Jump
    Points
    Pulse
    Globe
    Moon
    Pipe
    SimpleDots
    Arrow
    Dots9
    Star
    Ellipsis
    Hamburger
)
```

### Custom Spinner

```go
type Spinner struct {
    Frames []string
    FPS    time.Duration
}
```

## Progress (progress)

### Initialization

```go
func New(opts ...Option) progress.Model

func WithDefaultGradient() Option
func WithGradient(colors ...string) Option
func WithSolidColor(color string) Option
func WithWidth(width int) Option
func WithHeight(height int) Option
func WithoutPercentage() Option
```

### Configuration

```go
func (m *Model) SetPercent(float64) tea.Cmd
func (m *Model) Percent() float64
func (m *Model) Width() int
func (m *Model) Height() int
func (m *Model) ShowPercentage(bool)
```

### Styling

```go
func (m *Model) FullColor(color string)
func (m *Model) EmptyColor(color string)
func (m *Model) Full rune
func (m *Model) Empty rune
func (m *Model) Scale float64
```

## Table (table)

### Initialization

```go
func New(opts ...Option) table.Model

func WithColumns([]Column) Option
func WithRows([]Row) Option
func WithWidth(width int) Option
func WithHeight(height int) Option
func WithFocused(bool) Option
```

### Configuration

```go
func (m *Model) SetColumns([]Column)
func (m *Model) SetRows([]Row)
func (m *Model) Columns() []Column
func (m *Model) Rows() []Row
func (m *Model) SelectedRow() Row
func (m *Model) Cursor() int
func (m *Model) SetCursor(int)
func (m *Model) GoToTop()
func (m *Model) GoToBottom()
func (m *Model) Height() int
func (m *Model) Width() int
```

### Row Operations

```go
func (m *Model) AppendRow(Row)
func (m *Model) AppendRows([]Row)
func (m *Model) SetRows([]Row)
```

### Styling

```go
type Styles struct {
    Header   lipgloss.Style
    Cell     lipgloss.Style
    Selected lipgloss.Style
}

func (m *Model) SetStyles(Styles)
func (m *Model) WithColumnStyles([]lipgloss.Style)
```

### Column Configuration

```go
type Column struct {
    Title string
    Width int
}
```

## List (list)

### Initialization

```go
func New(items []Item, delegate Delegate, width, height int) Model
```

### Configuration

```go
func (m *Model) SetItems([]Item)
func (m *Model) Items() []Item
func (m *Model) SetDelegate(Delegate)
func (m *Model) SelectedItem() Item
func (m *Model) Index() int
func (m *Model) Cursor() int
func (m *Model) SetCursor(int)
func (m *Model) Select(int)
func (m *Model) SetShowStatusBar(bool)
func (m *Model) SetShowPagination(bool)
func (m *Model) SetShowHelp(bool)
func (m *Model) SetShowTitle(bool)
func (m *Model) SetFilteringEnabled(bool)
func (m *Model) SetFilter(string)
func (m *Model) Filter() string
func (m *Model) SetWidth(int)
func (m *Model) SetHeight(int)
func (m *Model) SetSize(width, height int)
```

### Status Messages

```go
func (m *Model) NewStatusMessage(string)
func (m *Model) StatusMessageLifetime() time.Duration
func (m *Model) SetStatusMessageLifetime(time.Duration)
```

### Item Interface

```go
type Item interface {
    Title() string
    Description() string
    FilterValue() string
}
```

### Delegate Configuration

```go
type Delegate interface {
    Update(msg tea.Msg, m Model) (Model, tea.Cmd)
    Render(m Model, index int, item Item) string
    Height() int
    Spacing() int
}

type DefaultDelegate struct {
    ShowDescription bool
    UpdateFunc      UpdateFunc
    HelpFunc        HelpFunc
    ShortHelpFunc   ShortHelpFunc
    FullHelpFunc    FullHelpFunc
}
```

## Paginator (paginator)

### Initialization

```go
func New() Model
```

### Configuration

```go
func (m *Model) SetTotalPages(int)
func (m *Model) TotalPages() int
func (m *Model) SetPage(int)
func (m *Model) Page() int
func (m *Model) OnLastPage() bool
func (m *Model) SetPerPage(int)
func (m *Model) PerPage() int
func (m *Model) SetType(Type)
func (m *Model) Type() Type
func (m *Model) GetSliceBounds(int) (start, end int)
```

### Types

```go
const (
    Dots Type = iota
    Arabic
    ArabicCompact
)
```

### Styling

```go
func (m *Model) ActiveDot lipgloss.Style
func (m *Model) InactiveDot lipgloss.Style
func (m *Model) ArabicSeparator string
```

## Timer (timer)

### Initialization

```go
func New(timeout time.Duration) Model
func NewWithInterval(timeout, interval time.Duration) Model
```

### Configuration

```go
func (m *Model) Init() tea.Cmd
func (m *Model) Update(msg tea.Msg) (Model, tea.Cmd)
func (m *Model) Start()
func (m *Model) Stop()
func (m *Model) Toggle()
func (m *Model) Reset()
func (m *Model) Running() bool
func (m *Model) Timedout() bool
func (m *Model) Timeout() time.Duration
func (m *Model) Interval() time.Duration
func (m *Model) View() string
```

### Styling

```go
func (m *Model) Style(lipgloss.Style)
func (m *Model) TimeoutStyle(lipgloss.Style)
```

## Viewport (viewport)

### Initialization

```go
func New(width, height int) Model
```

### Configuration

```go
func (m *Model) SetContent(string)
func (m *Model) GetContent() string
func (m *Model) SetSize(width, height int)
func (m *Model) Width() int
func (m *Model) Height() int
func (m *Model) GotoTop()
func (m *Model) GotoBottom()
func (m *Model) LineUp(int)
func (m *Model) LineDown(int)
func (m *Model) HalfViewUp()
func (m *Model) HalfViewDown()
func (m *Model) GotoLine(int)
func (m *Model) YOffset() int
func (m *Model) SetYOffset(int)
func (m *Model) ScrollPercent() float64
func (m *Model) AtTop() bool
func (m *Model) AtBottom() bool
func (m *Model) PastBottom() bool
func (m *Model) VisibleLineCount() int
func (m *Model) TotalLineCount() int
```

### Styling

```go
func (m *Model) Style(lipgloss.Style)
```

## File Picker (filepicker)

### Initialization

```go
func New() Model
```

### Configuration

```go
func (m *Model) Init() tea.Cmd
func (m *Model) Update(msg tea.Msg) (Model, tea.Cmd)
func (m *Model) CurrentDirectory() string
func (m *Model) Cd(string)
func (m *Model) CdUp()
func (m *Model) GoToCurrentDirectory()
func (m *Model) SetAllowedTypes([]string)
func (m *Model) SetDisabledTypes([]string)
func (m *Model) SetFileAllowed(bool)
func (m *Model) SetDirectoryAllowed(bool)
func (m *Model) SetShowHidden(bool)
func (m *Model) SetAutoHeight(bool)
```

### Selection Handling

```go
func (m *Model) DidSelectFile(msg tea.Msg) (bool, string)
func (m *Model) DidSelectDirectory(msg tea.Msg) (bool, string)
func (m *Model) DidSelectDisabledFile(msg tea.Msg) (bool, string)
func (m *Model) DidSelect(msg tea.Msg) (bool, string, bool, bool)
```

### Styling

```go
func (m *Model) Styles() Styles
func (m *Model) SetStyles(Styles)

type Styles struct {
    Cursor      lipgloss.Style
    Selected    lipgloss.Style
    Disabled    lipgloss.Style
    Directory   lipgloss.Style
    File        lipgloss.Style
    Symlink     lipgloss.Style
}
```

## Key Bindings (key)

### Binding Creation

```go
func NewBinding(opts ...Option) key.Binding

func WithKeys([]string) Option
func WithHelp(string, string) Option
func WithDisabled() Option
func WithEnabled() Option
func WithHelp(string) Option
```

### Binding Methods

```go
func (b *Binding) Keys() []string
func (b *Binding) Help() string
func (b *Binding) Enabled() bool
func (b *Binding) SetEnabled(bool)
func (b *Binding) Matches(tea.KeyMsg) bool
func (b *Binding) Unbind()
func (b *Binding) SetKeys([]string)
func (b *Binding) SetHelp(string, string)
```

### Key Matching

```go
func Matches(msg tea.KeyMsg, bindings ...key.Binding) bool
```

## Help (help)

### Initialization

```go
func New() Model
```

### Configuration

```go
func (m *Model) Update(msg tea.Msg) (Model, tea.Cmd)
func (m *Model) View(keyMap ShortHelp) string
func (m *Model) FullHelpView(keyMap FullHelp) string
func (m *Model) ShowAll(bool)
func (m *Model) ShowAll() bool
func (m *Model) Width(int)
func (m *Model) Filter(string)
func (m *Model) Filter() string
func (m *Model) SetMinWidth(int)
func (m *Model) SetMaxWidth(int)
func (m *Model) Separator(string)
```

### Help Interface

```go
type ShortHelp interface {
    ShortHelp() []key.Binding
}

type FullHelp interface {
    FullHelp() [][]key.Binding
}
```

### Styling

```go
func (m *Model) Styles() Styles
func (m *Model) SetStyles(Styles)

type Styles struct {
    ShortKey       lipgloss.Style
    ShortDesc      lipgloss.Style
    FullKey        lipgloss.Style
    FullDesc       lipgloss.Style
    FullSeparator  lipgloss.Style
    ELLIPSIS       lipgloss.Style
}
```

## Common Patterns

### Command Patterns

```go
// Blink cursor
textinput.Blink

// Tick animation
spinner.Tick

// Set progress percent
progress.SetPercent(0.75)

// Timer timeout
timer.Timeout

// Viewport line operations
viewport.LineUp(1)
viewport.LineDown(1)
viewport.GotoTop()
viewport.GotoBottom()
```

### Message Types

```go
// Spinner
type TickMsg time.Time

// Progress
type FrameMsg time.Time

// Timer
type TimeoutMsg time.Time
type TickMsg time.Time
```

### Style Application

```go
// Apply base style
component.Style = baseStyle

// Apply custom styling
component.SetStyles(Styles{
    Header: headerStyle,
    Selected: selectedStyle,
})

// Color theming
component.Style = lipgloss.NewStyle().
    Foreground(lipgloss.Color("62")).
    Background(lipgloss.Color("236"))
```

This API reference provides complete documentation for all Bubbles components, enabling developers to leverage the full capabilities of the component library for building sophisticated terminal user interfaces.