# Bubbles Component Troubleshooting Guide

This comprehensive guide covers common issues, debugging techniques, and solutions for problems encountered when working with Bubbles components in BubbleTea applications.

## Common Issues and Solutions

### Component Not Receiving Input

**Symptoms:**
- Component doesn't respond to keyboard events
- Focus indicators not showing
- No visual feedback on user interaction

**Common Causes:**
1. Component not focused
2. Message routing conflicts
3. Component not properly integrated into Update loop

**Solutions:**

```go
// 1. Ensure component is focused
func (m Model) Update(msg tea.Msg) (tea.Model, tea.Cmd) {
    var cmd tea.Cmd

    // Update component first
    m.textInput, cmd = m.textInput.Update(msg)

    // Handle focus management
    switch msg := msg.(type) {
    case tea.KeyMsg:
        switch msg.String() {
        case "tab":
            // Switch focus between components
            m.activeComponent = (m.activeComponent + 1) % len(m.components)
            return m, m.updateFocus()
        }
    }

    return m, cmd
}

func (m Model) updateFocus() tea.Cmd {
    // Blur all components
    for i := range m.components {
        if component, ok := m.components[i].(Focuser); ok {
            component.Blur()
        }
    }

    // Focus active component
    if component, ok := m.components[m.activeComponent].(Focuser); ok {
        component.Focus()
    }

    return nil
}
```

**Debugging Steps:**
```go
// Add logging to track focus state
func (m Model) Update(msg tea.Msg) (tea.Model, tea.Cmd) {
    log.Printf("Active component: %d", m.activeComponent)
    log.Printf("Component focused: %v", m.textInput.Focused())

    // Handle message
    switch msg := msg.(type) {
    case tea.KeyMsg:
        log.Printf("Key pressed: %s", msg.String())
        // Process key event
    }

    return m, nil
}
```

### Styling Not Applying

**Symptoms:**
- Components appear with default styling
- Colors not displaying correctly
- Borders and padding not applied

**Common Causes:**
1. Style application order issues
2. Incorrect color values
3. Terminal color support limitations
4. Style inheritance conflicts

**Solutions:**

```go
// 1. Apply styles after component initialization
func (m Model) Init() tea.Cmd {
    // Initialize component
    ti := textinput.New()

    // Apply styles
    ti.Style = lipgloss.NewStyle().
        Foreground(lipgloss.Color("255")).
        Background(lipgloss.Color("237")).
        Border(lipgloss.NormalBorder()).
        BorderForeground(lipgloss.Color("62"))

    ti.CursorStyle = lipgloss.NewStyle().
        Background(lipgloss.Color("228"))

    m.textInput = ti
    return textinput.Blink
}

// 2. Use adaptive colors for better compatibility
func applyAdaptiveStyles(component *textinput.Model) {
    component.Style = lipgloss.NewStyle().
        Foreground(lipgloss.AdaptiveColor{
            Light: "0",   // Black for light terminals
            Dark:  "255", // White for dark terminals
        }).
        Background(lipgloss.AdaptiveColor{
            Light: "255", // White for light terminals
            Dark:  "235", // Dark gray for dark terminals
        })
}

// 3. Check terminal capabilities
func checkTerminalCapabilities() {
    renderer := lipgloss.DefaultRenderer()
    log.Printf("Color profile: %v", renderer.ColorProfile())
    log.Printf("Has dark background: %v", renderer.HasDarkBackground())

    if renderer.ColorProfile() == lipgloss.NoColor {
        log.Println("Warning: Terminal does not support colors")
    }
}
```

### Performance Issues

**Symptoms:**
- Slow rendering with large datasets
- High CPU usage
- Laggy interactions
- Memory usage growing over time

**Solutions:**

```go
// 1. Use pagination for large lists/tables
type PaginatedListModel struct {
    list        list.Model
    currentPage int
    pageSize    int
    totalCount  int
}

func (m PaginatedListModel) loadPage(page int) tea.Cmd {
    return func() tea.Msg {
        // Load only current page data
        start := page * m.pageSize
        end := start + m.pageSize
        if end > m.totalCount {
            end = m.totalCount
        }

        items := loadItemsFromDatabase(start, end)
        return ItemsLoadedMsg{items: items}
    }
}

// 2. Limit data structures
const MAX_ITEMS = 1000

func (m Model) addItem(item Item) Model {
    // Prevent unbounded growth
    if len(m.items) >= MAX_ITEMS {
        m.items = m.items[1:] // Remove oldest item
    }

    m.items = append(m.items, item)
    return m
}

// 3. Use viewport for large content
func (m Model) View() string {
    // Instead of rendering all content
    // return strings.Join(m.allLines, "\n")

    // Use viewport for efficient rendering
    return m.viewport.View()
}

// 4. Batch rapid updates
type DebouncedModel struct {
    debouncer *Debouncer
    filter    string
}

func (m DebouncedModel) Update(msg tea.Msg) (tea.Model, tea.Cmd) {
    switch msg := msg.(type) {
    case tea.KeyMsg:
        if msg.Type == tea.KeyRunes {
            m.filter += string(msg.Runes)
            m.debouncer.Trigger() // Debounce filter updates
        }
    }
    return m, nil
}
```

### Component State Issues

**Symptoms:**
- Component state not updating correctly
- Lost focus or selection state
- Inconsistent behavior

**Solutions:**

```go
// 1. Ensure immutable updates
func (m Model) Update(msg tea.Msg) (tea.Model, tea.Cmd) {
    // Bad: modifying in place
    // m.counter++

    // Good: returning new model
    return m.withIncrementedCounter(), nil
}

func (m Model) withIncrementedCounter() Model {
    newModel := m
    newModel.counter++
    return newModel
}

// 2. Preserve component state when switching focus
func (m Model) updateFocus() tea.Cmd {
    // Save current state
    currentFocus := m.active

    // Update focus
    m.active = (m.active + 1) % len(m.components)

    // Apply focus changes
    for i, component := range m.components {
        if i == m.active {
            component.Focus()
        } else {
            component.Blur()
        }
    }

    return nil
}

// 3. Validate component state
func (m Model) validateState() error {
    if m.active < 0 || m.active >= len(m.components) {
        return fmt.Errorf("invalid active component: %d", m.active)
    }

    // Validate specific components
    if ti, ok := m.components["input"].(*textinput.Model); ok {
        if ti.Value() != m.expectedInput {
            return fmt.Errorf("input value mismatch")
        }
    }

    return nil
}
```

## Component-Specific Issues

### Text Input Problems

**Issue: Input not accepting characters**
```go
// Check if input is focused
if !m.textInput.Focused() {
    m.textInput.Focus()
}

// Check if text input is disabled
if m.textInput.EchoMode == textinput.EchoNone {
    // Input is completely hidden
}

// Check character limit
if m.textInput.CharLimit > 0 && len(m.textInput.Value()) >= m.textInput.CharLimit {
    // Input is at limit
}
```

**Issue: Validation not working**
```go
func (m Model) Update(msg tea.Msg) (tea.Model, tea.Cmd) {
    m.textInput, cmd := m.textInput.Update(msg)

    // Check validation results
    if m.textInput.Validate != nil {
        err := m.textInput.Validate(m.textInput.Value())
        if err != nil {
            m.error = err.Error()
            // Apply error styling
            m.textInput.Style = errorStyle
        } else {
            m.error = ""
            m.textInput.Style = normalStyle
        }
    }

    return m, cmd
}
```

### List Component Issues

**Issue: List not filtering correctly**
```go
// Ensure filtering is enabled
func (m Model) Init() tea.Cmd {
    l := list.New(items, delegate, width, height)
    l.SetFilteringEnabled(true) // Important!
    m.list = l
    return nil
}

// Debug filter state
func (m Model) debugFilter() {
    log.Printf("Filter enabled: %v", m.list.FilteringEnabled())
    log.Printf("Current filter: %q", m.list.Filter())
    log.Printf("Filtered items: %d", len(m.list.Items()))
}
```

**Issue: List selection not working**
```go
// Check list focus state
func (m Model) Update(msg tea.Msg) (tea.Model, tea.Cmd) {
    if !m.list.FilteringEnabled() {
        m.list.Focus() // Ensure list is focused
    }

    m.list, cmd = m.list.Update(msg)

    // Check selection state
    selected := m.list.SelectedItem()
    if selected != nil {
        log.Printf("Selected: %s", selected.Title())
    }

    return m, cmd
}
```

### Table Component Issues

**Issue: Table styling not applying**
```go
// Styles must be set after table creation
func (m Model) Init() tea.Cmd {
    t := table.New(
        table.WithColumns(columns),
        table.WithRows(rows),
        table.WithFocused(true),
    )

    // Apply styles
    t.SetStyles(table.Styles{
        Header:   headerStyle,
        Cell:     cellStyle,
        Selected: selectedStyle,
    })

    m.table = t
    return nil
}

// Check if styles are applied
func (m Model) debugTableStyles() {
    styles := m.table.Styles()
    log.Printf("Header style: %+v", styles.Header)
    log.Printf("Cell style: %+v", styles.Cell)
    log.Printf("Selected style: %+v", styles.Selected)
}
```

**Issue: Table cursor not moving**
```go
// Ensure table is focused
func (m Model) Update(msg tea.Msg) (tea.Model, tea.Cmd) {
    if !m.table.Focused() {
        m.table.Focus()
    }

    m.table, cmd = m.table.Update(msg)

    // Check cursor position
    log.Printf("Table cursor: %d", m.table.Cursor())
    log.Printf("Table focused: %v", m.table.Focused())

    return m, cmd
}
```

### Spinner Issues

**Issue: Spinner not animating**
```go
func (m Model) Init() tea.Cmd {
    s := spinner.New()

    // Must return Tick command for animation
    m.spinner = s
    return s.Tick
}

func (m Model) Update(msg tea.Msg) (tea.Model, tea.Cmd) {
    var cmd tea.Cmd

    switch msg := msg.(type) {
    case spinner.TickMsg:
        // Important: must update spinner with TickMsg
        m.spinner, cmd = m.spinner.Update(msg)
        return m, cmd
    }

    return m, nil
}
```

**Issue: Spinner not visible**
```go
// Check spinner styling
func (m Model) styleSpinner() {
    // Ensure foreground color is set
    m.spinner.Style = lipgloss.NewStyle().
        Foreground(lipgloss.Color("62")).
        Bold(true)

    // Check if spinner is running
    if !m.loading {
        m.spinner.Stop()
    } else {
        m.spinner.Start()
    }
}
```

## Debugging Techniques

### Component State Inspection

```go
func (m Model) debugComponentStates() {
    log.Printf("=== COMPONENT DEBUG INFO ===")

    // Text input state
    log.Printf("TextInput:")
    log.Printf("  Value: %q", m.textInput.Value())
    log.Printf("  Focused: %v", m.textInput.Focused())
    log.Printf("  Cursor: %d", m.textInput.Cursor())
    log.Printf("  Width: %d", m.textInput.Width())
    log.Printf("  CharLimit: %d", m.textInput.CharLimit())

    // List state
    log.Printf("List:")
    log.Printf("  Total items: %d", len(m.list.Items()))
    log.Printf("  Selected: %d", m.list.Index())
    log.Printf("  Filter: %q", m.list.Filter())
    log.Printf("  Filtering enabled: %v", m.list.FilteringEnabled())

    // Table state
    log.Printf("Table:")
    log.Printf("  Rows: %d", len(m.table.Rows()))
    log.Printf("  Cursor: %d", m.table.Cursor())
    log.Printf("  Height: %d", m.table.Height())
}
```

### Message Flow Tracing

```go
func (m Model) Update(msg tea.Msg) (tea.Model, tea.Cmd) {
    log.Printf("=== MESSAGE FLOW ===")
    log.Printf("Message type: %T", msg)

    switch msg := msg.(type) {
    case tea.KeyMsg:
        log.Printf("Key event:")
        log.Printf("  Type: %v", msg.Type)
        log.Printf("  String: %s", msg.String())
        log.Printf("  Runes: %v", msg.Runes)

    case tea.MouseMsg:
        log.Printf("Mouse event:")
        log.Printf("  Action: %v", msg.Action)
        log.Printf("  Button: %v", msg.Button)
        log.Printf("  Position: (%d, %d)", msg.X, msg.Y)

    case tea.WindowSizeMsg:
        log.Printf("Window resize:")
        log.Printf("  Width: %d", msg.Width)
        log.Printf("  Height: %d", msg.Height)
    }

    // Update components
    m.textInput, cmd = m.textInput.Update(msg)

    log.Printf("=== COMPONENT UPDATE ===")
    log.Printf("TextInput value: %q", m.textInput.Value())

    return m, cmd
}
```

### Performance Profiling

```go
type PerformanceMonitor struct {
    updateCount int
    totalUpdate time.Duration
    lastUpdate  time.Time
}

func (pm *PerformanceMonitor) startUpdate() {
    pm.lastUpdate = time.Now()
}

func (pm *PerformanceMonitor) endUpdate() {
    duration := time.Since(pm.lastUpdate)
    pm.totalUpdate += duration
    pm.updateCount++

    // Log slow updates
    if duration > 16*time.Millisecond { // > 60 FPS
        log.Printf("Slow update: %v", duration)
    }

    // Log average every 100 updates
    if pm.updateCount%100 == 0 {
        avg := pm.totalUpdate / time.Duration(pm.updateCount)
        log.Printf("Average update time: %v", avg)
    }
}

func (m Model) Update(msg tea.Msg) (tea.Model, tea.Cmd) {
    m.perfMonitor.startUpdate()
    defer m.perfMonitor.endUpdate()

    // Update logic here
    return m, nil
}
```

### Memory Usage Tracking

```go
func (m Model) checkMemoryUsage() {
    var memStats runtime.MemStats
    runtime.ReadMemStats(&memStats)

    log.Printf("=== MEMORY USAGE ===")
    log.Printf("Alloc: %d KB", memStats.Alloc/1024)
    log.Printf("TotalAlloc: %d KB", memStats.TotalAlloc/1024)
    log.Printf("Sys: %d KB", memStats.Sys/1024)
    log.Printf("NumGC: %d", memStats.NumGC)

    // Check for potential memory leaks
    if memStats.Alloc > 100*1024*1024 { // > 100MB
        log.Printf("WARNING: High memory usage detected")
    }
}
```

## Error Recovery Strategies

### Component Resilience

```go
type ResilientModel struct {
    components map[string]tea.Model
    errors     map[string]error
    retries    map[string]int
    maxRetries int
}

func (m ResilientModel) Update(msg tea.Msg) (tea.Model, tea.Cmd) {
    for name, component := range m.components {
        // Safely update each component
        func() {
            defer func() {
                if r := recover(); r != nil {
                    log.Printf("Component %s panicked: %v", name, r)
                    m.errors[name] = fmt.Errorf("panic: %v", r)
                    m.retries[name]++

                    if m.canRetry(name) {
                        m.components[name] = m.createComponent(name)
                    }
                }
            }()

            m.components[name], _ = component.Update(msg)
        }()
    }

    return m, nil
}

func (m ResilientModel) canRetry(name string) bool {
    return m.retries[name] < m.maxRetries
}
```

### Graceful Degradation

```go
type GracefulModel struct {
    primary     textinput.Model
    fallback    textinput.Model
    usingFallback bool
}

func (m GracefulModel) Update(msg tea.Msg) (tea.Model, tea.Cmd) {
    var cmd tea.Cmd

    if m.usingFallback {
        m.fallback, cmd = m.fallback.Update(msg)
    } else {
        defer func() {
            if r := recover(); r != nil {
                log.Printf("Primary component failed, switching to fallback: %v", r)
                m.usingFallback = true
                m.fallback = createFallbackInput()
            }
        }()

        m.primary, cmd = m.primary.Update(msg)
    }

    return m, cmd
}

func createFallbackInput() textinput.Model {
    ti := textinput.New()
    ti.Placeholder = "Simple input (fallback mode)"
    ti.CharLimit = 50
    return ti
}
```

## Platform-Specific Issues

### Windows Terminal

**Issue: Color support on Windows**
```go
// Check Windows-specific settings
func checkWindowsTerminal() {
    if runtime.GOOS == "windows" {
        // Enable virtual terminal processing
        cmd := exec.Command("cmd", "/c", "echo")
        cmd.SysProcAttr = &syscall.SysProcAttr{
            HideWindow:    true,
            CreationFlags: syscall.CREATE_NEW_PROCESS_GROUP,
        }

        // Use Windows Terminal or ConEmu for better support
        if os.Getenv("WT_SESSION") == "" {
            log.Println("Warning: Use Windows Terminal for best experience")
        }
    }
}
```

### macOS Terminal

**Issue: Input lag on macOS**
```go
// Adjust for macOS terminal behavior
func (m Model) Update(msg tea.Msg) (tea.Model, tea.Cmd) {
    if runtime.GOOS == "darwin" {
        // macOS specific handling
        switch msg := msg.(type) {
        case tea.KeyMsg:
            // Handle special macOS key combinations
            if msg.String() == "cmd+c" {
                return m, tea.Quit
            }
        }
    }

    return m, nil
}
```

## Testing Troubleshooting

### Component Testing Issues

**Issue: Tests not behaving as expected**
```go
func TestTextInputBehavior(t *testing.T) {
    // Ensure test environment is set up correctly
    ti := textinput.New()

    // Test focus state
    require.True(t, ti.Focused(), "Text input should be focused by default")

    // Test input handling
    msg := tea.KeyMsg{
        Type:  tea.KeyRunes,
        Runes: []rune("hello"),
    }

    newTi, _ := ti.Update(msg)
    assert.Equal(t, "hello", newTi.Value(), "Text input should accept characters")

    // Test backspace
    backspaceMsg := tea.KeyMsg{Type: tea.KeyBackspace}
    newTi, _ = newTi.Update(backspaceMsg)
    assert.Equal(t, "hell", newTi.Value(), "Backspace should remove last character")
}
```

### Integration Testing Issues

**Issue: Integration tests not passing**
```go
func TestFormIntegration(t *testing.T) {
    model := NewFormModel()

    // Test component initialization
    require.NotNil(t, model.textInput, "Text input should be initialized")
    require.NotNil(t, model.list, "List should be initialized")

    // Test focus management
    initialFocus := model.getFocusedComponent()
    assert.NotNil(t, initialFocus, "One component should be focused")

    // Test navigation
    tabMsg := tea.KeyMsg{Type: tea.KeyTab}
    newModel, _ := model.Update(tabMsg)
    newFocus := newModel.getFocusedComponent()
    assert.NotEqual(t, initialFocus, newFocus, "Tab should change focused component")
}
```

This troubleshooting guide provides comprehensive solutions for common issues encountered when working with Bubbles components. Use these techniques systematically to identify, diagnose, and resolve problems in your BubbleTea applications.