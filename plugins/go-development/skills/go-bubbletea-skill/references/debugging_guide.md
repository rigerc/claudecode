# BubbleTea Debugging Guide

This comprehensive guide covers common issues, debugging techniques, and troubleshooting strategies for BubbleTea applications.

## Common Issues and Solutions

### Component Not Receiving Input

**Symptoms:**
- Component doesn't respond to keyboard/mouse events
- Focus indicators not showing
- Component appears frozen

**Common Causes:**
1. Component not focused
2. Message routing issues
3. Event handler conflicts

**Solutions:**

```go
// 1. Ensure component is focused
func (m Model) Update(msg tea.Msg) (tea.Model, tea.Cmd) {
    var cmd tea.Cmd

    switch msg := msg.(type) {
    case tea.KeyMsg:
        switch msg.String() {
        case "tab":
            // Toggle focus between components
            m.activeComponent = (m.activeComponent + 1) % 2
            return m, m.updateFocus()
        }
    }

    // Update active component first
    switch m.activeComponent {
    case 0:
        m.textInput, cmd = m.textInput.Update(msg)
        return m, cmd
    case 1:
        m.list, cmd = m.list.Update(msg)
        return m, cmd
    }

    return m, nil
}

func (m Model) updateFocus() tea.Cmd {
    switch m.activeComponent {
    case 0:
        m.textInput.Focus()
        m.list.Blur()
    case 1:
        m.textInput.Blur()
        m.list.Focus()
    }
    return nil
}
```

**Debugging Steps:**
1. Add logging to track message flow
2. Verify component focus state
3. Check message ordering in Update method

```go
func (m Model) Update(msg tea.Msg) (tea.Model, tea.Cmd) {
    log.Printf("Received message: %T", msg)
    log.Printf("Active component: %d", m.activeComponent)

    switch msg := msg.(type) {
    case tea.KeyMsg:
        log.Printf("Key pressed: %s", msg.String())
    }

    // ... rest of update logic
}
```

### Styling Issues

**Symptoms:**
- Colors not displaying correctly
- Borders not appearing
- Text formatting issues

**Common Causes:**
1. Terminal color support limitations
2. Incorrect color values
3. Style inheritance conflicts

**Solutions:**

```go
// 1. Check color profile and use adaptive colors
func (m Model) View() string {
    // Log color information for debugging
    renderer := lipgloss.DefaultRenderer()
    log.Printf("Color profile: %v", renderer.ColorProfile())
    log.Printf("Has dark background: %v", renderer.HasDarkBackground())

    // Use adaptive colors for better compatibility
    style := lipgloss.NewStyle().
        Foreground(lipgloss.AdaptiveColor{Light: "63", Dark: "228"}).
        Background(lipgloss.AdaptiveColor{Light: "251", Dark: "235"})

    return style.Render("Styled text")
}
```

**Force Color Profile:**

```go
func main() {
    // Force specific color profile for debugging
    renderer := lipgloss.NewRenderer(os.Stdout)
    renderer.SetColorProfile(lipgloss.TrueColor)
    renderer.SetHasDarkBackground(true)

    // Create program with custom renderer
    p := tea.NewProgram(
        initialModel(),
        tea.WithRenderer(renderer),
    )

    if _, err := p.Run(); err != nil {
        log.Fatal(err)
    }
}
```

### Performance Issues

**Symptoms:**
- Slow rendering
- High CPU usage
- Laggy interactions

**Common Causes:**
1. Large datasets in memory
2. Inefficient rendering loops
3. Blocking operations

**Solutions:**

```go
// 1. Use viewport for large content
type Model struct {
    viewport viewport.Model
    content  string
}

func (m Model) View() string {
    // Only renders visible portion
    return m.viewport.View()
}

// 2. Limit frame rate
func main() {
    p := tea.NewProgram(
        initialModel(),
        tea.WithFPS(30), // Limit to 30 FPS
    )
    p.Run()
}

// 3. Batch rapid updates
type Model struct {
    pendingUpdates bool
    updateTimer    *time.Timer
}

func (m Model) scheduleUpdate() tea.Cmd {
    if m.updateTimer != nil {
        m.updateTimer.Stop()
    }

    m.updateTimer = time.AfterFunc(100*time.Millisecond, func() {
        p.Send(updateMsg{})
    })

    return nil
}
```

### Memory Leaks

**Symptoms:**
- Memory usage grows over time
- Application becomes slower
- Eventually crashes

**Common Causes:**
1. Unclosed resources
2. Unbounded data structures
3. Goroutine leaks

**Solutions:**

```go
// 1. Clean up resources on quit
func (m Model) Update(msg tea.Msg) (tea.Model, tea.Cmd) {
    switch msg := msg.(type) {
    case tea.QuitMsg:
        // Clean up resources
        if m.conn != nil {
            m.conn.Close()
        }
        if m.file != nil {
            m.file.Close()
        }
        if m.timer != nil {
            m.timer.Stop()
        }
    }
    return m, nil
}

// 2. Limit data structure sizes
const MAX_ITEMS = 1000

func (m Model) AddItems(items []string) Model {
    // Prevent unbounded growth
    if len(m.items)+len(items) > MAX_ITEMS {
        // Remove oldest items
        excess := (len(m.items) + len(items)) - MAX_ITEMS
        m.items = m.items[excess:]
    }

    m.items = append(m.items, items...)
    return m
}
```

## Debugging Techniques

### Logging and Monitoring

**Enable Comprehensive Logging:**

```go
func main() {
    // Enable logging to file
    f, err := tea.LogToFile("debug.log", "debug")
    if err != nil {
        log.Fatal(err)
    }
    defer f.Close()

    // Log program startup
    log.Printf("Starting application with terminal: %s", os.Getenv("TERM"))
    log.Printf("Color support: %v", lipgloss.DefaultRenderer().ColorProfile())

    p := tea.NewProgram(initialModel())
    if _, err := p.Run(); err != nil {
        log.Printf("Application error: %v", err)
    }
}
```

**Component-Specific Debugging:**

```go
func (m Model) Update(msg tea.Msg) (tea.Model, tea.Cmd) {
    // Log all incoming messages
    log.Printf("Update called with message type: %T", msg)

    switch msg := msg.(type) {
    case tea.KeyMsg:
        log.Printf("Key event - Type: %v, String: %s, Runes: %v",
            msg.Type, msg.String(), msg.Runes)

    case tea.MouseMsg:
        log.Printf("Mouse event - Action: %v, Button: %v, Position: (%d, %d)",
            msg.Action, msg.Button, msg.X, msg.Y)

    case tea.WindowSizeMsg:
        log.Printf("Window resized - Width: %d, Height: %d", msg.Width, msg.Height)
    }

    // Log component states before update
    log.Printf("Before update - TextInput focused: %v, List cursor: %d",
        m.textInput.Focused(), m.list.Cursor())

    // Perform update
    newModel, cmd := m.performUpdate(msg)

    // Log component states after update
    log.Printf("After update - TextInput focused: %v, List cursor: %d",
        newModel.textInput.Focused(), newModel.list.Cursor())

    return newModel, cmd
}
```

**Performance Monitoring:**

```go
type PerformanceMonitor struct {
    lastRender    time.Time
    renderCount   int
    totalRender   time.Duration
    maxRenderTime time.Duration
}

func (pm *PerformanceMonitor) StartRender() {
    pm.lastRender = time.Now()
}

func (pm *PerformanceMonitor) EndRender() {
    duration := time.Since(pm.lastRender)
    pm.renderCount++
    pm.totalRender += duration

    if duration > pm.maxRenderTime {
        pm.maxRenderTime = duration
    }

    // Log slow renders
    if duration > 16*time.Millisecond { // > 60 FPS
        log.Printf("Slow render detected: %v", duration)
    }

    // Log average every 100 renders
    if pm.renderCount%100 == 0 {
        avg := pm.totalRender / time.Duration(pm.renderCount)
        log.Printf("Performance - Avg: %v, Max: %v, Count: %d",
            avg, pm.maxRenderTime, pm.renderCount)
    }
}

// Use in model
func (m Model) View() string {
    m.perfMonitor.StartRender()
    defer m.perfMonitor.EndRender()

    // ... render logic
}
```

### State Inspection

**Add State Dumps:**

```go
func (m Model) DebugState() string {
    var debug strings.Builder

    debug.WriteString("=== MODEL STATE ===\n")
    debug.WriteString(fmt.Sprintf("Active Component: %d\n", m.activeComponent))
    debug.WriteString(fmt.Sprintf("Loading: %v\n", m.loading))
    debug.WriteString(fmt.Sprintf("Error: %s\n", m.error))

    debug.WriteString("\n=== TEXT INPUT ===\n")
    debug.WriteString(fmt.Sprintf("Value: %q\n", m.textInput.Value()))
    debug.WriteString(fmt.Sprintf("Focused: %v\n", m.textInput.Focused()))
    debug.WriteString(fmt.Sprintf("Cursor: %d\n", m.textInput.Cursor()))
    debug.WriteString(fmt.Sprintf("Width: %d\n", m.textInput.Width()))

    debug.WriteString("\n=== LIST ===\n")
    debug.WriteString(fmt.Sprintf("Total Items: %d\n", len(m.list.Items())))
    debug.WriteString(fmt.Sprintf("Selected: %d\n", m.list.Cursor()))
    debug.WriteString(fmt.Sprintf("Filter: %q\n", m.list.Filter()))

    return debug.String()
}

// Add debug keybinding
func (m Model) Update(msg tea.Msg) (tea.Model, tea.Cmd) {
    switch msg := msg.(type) {
    case tea.KeyMsg:
        if msg.String() == "F12" {
            log.Printf("STATE DUMP:\n%s", m.DebugState())
            return m, tea.Printf("State dumped to debug log")
        }
    }
    // ... rest of update
}
```

**Visual State Indicators:**

```go
func (m Model) View() string {
    var view strings.Builder

    // Add debug overlay in development
    if os.Getenv("DEBUG") == "1" {
        debugOverlay := lipgloss.NewStyle().
            Background(lipgloss.Color("52")).
            Foreground(lipgloss.Color("255")).
            Padding(0, 1).
            Render(fmt.Sprintf("DEBUG: %s | Focused: %d",
                time.Now().Format("15:04:05"), m.activeComponent))

        view.WriteString(lipgloss.Place(
            80, 1,
            lipgloss.Right, lipgloss.Top,
            debugOverlay,
        ))
    }

    view.WriteString(m.renderMainContent())
    return view.String()
}
```

## Troubleshooting Checklist

### Before Seeking Help

1. **Enable Debug Logging:**
   ```bash
   DEBUG=1 go run main.go 2>&1 | tee debug.log
   ```

2. **Check Terminal Compatibility:**
   ```go
   log.Printf("TERM: %s", os.Getenv("TERM"))
   log.Printf("COLORTERM: %s", os.Getenv("COLORTERM"))
   log.Printf("Color profile: %v", lipgloss.DefaultRenderer().ColorProfile())
   ```

3. **Verify Component States:**
   ```go
   log.Printf("Component focused: %v", m.textInput.Focused())
   log.Printf("Component value: %q", m.textInput.Value())
   ```

4. **Check Message Flow:**
   ```go
   func (m Model) Update(msg tea.Msg) (tea.Model, tea.Cmd) {
       log.Printf("Message: %T, Value: %+v", msg, msg)
       // ... handle message
   }
   ```

### Common Debugging Commands

```go
// Add debug keybindings
func (m Model) debugKeybindings() map[string]func(Model) (Model, tea.Cmd) {
    return map[string]func(Model) (Model, tea.Cmd){
        "F1": func(m Model) (Model, tea.Cmd) {
            return m, tea.Printf("Active: %d, Items: %d",
                m.activeComponent, len(m.list.Items()))
        },
        "F2": func(m Model) (Model, tea.Cmd) {
            return m, tea.Printf("State: %+v", m)
        },
        "F3": func(m Model) (Model, tea.Cmd) {
            log.Printf("Full state dump:\n%s", m.DebugState())
            return m, tea.Printf("State logged")
        },
        "F4": func(m Model) (Model, tea.Cmd) {
            // Force render
            return m, tea.WindowSizeMsg{Width: 80, Height: 24}
        },
    }
}
```

### Performance Analysis

**Profile Rendering:**

```go
type ProfilingModel struct {
    renderTimes []time.Duration
    lastRender  time.Time
}

func (m ProfilingModel) startProfile() {
    m.lastRender = time.Now()
}

func (m ProfilingModel) endProfile() {
    duration := time.Since(m.lastRender)
    m.renderTimes = append(m.renderTimes, duration)

    // Keep last 100 samples
    if len(m.renderTimes) > 100 {
        m.renderTimes = m.renderTimes[1:]
    }

    // Calculate statistics
    var total time.Duration
    max := time.Duration(0)
    for _, t := range m.renderTimes {
        total += t
        if t > max {
            max = t
        }
    }
    avg := total / time.Duration(len(m.renderTimes))

    // Log performance issues
    if avg > 16*time.Millisecond {
        log.Printf("Performance warning - Average render: %v (max: %v)", avg, max)
    }
}
```

**Memory Usage Monitoring:**

```go
func logMemoryUsage() {
    var m runtime.MemStats
    runtime.ReadMemStats(&m)

    log.Printf("Memory - Alloc: %d KB, TotalAlloc: %d KB, Sys: %d KB",
        m.Alloc/1024, m.TotalAlloc/1024, m.Sys/1024)
    log.Printf("GC - NumGC: %d, PauseTotal: %v", m.NumGC, m.PauseTotal)
}
```

## Error Recovery Strategies

### Graceful Degradation

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
                }
            }()

            newComponent, cmd := component.Update(msg)
            m.components[name] = newComponent
            // Handle cmd
        }()
    }

    return m, nil
}

func (m ResilientModel) canRetry(name string) bool {
    return m.retries[name] < m.maxRetries
}

func (m ResilientModel) resetComponent(name string) tea.Cmd {
    if m.canRetry(name) {
        log.Printf("Resetting component %s (attempt %d)", name, m.retries[name]+1)
        m.components[name] = m.createComponent(name)
        m.retries[name]++
        return nil
    }

    log.Printf("Component %s exceeded max retries", name)
    return tea.Quit
}
```

### State Validation

```go
func (m Model) validateState() error {
    // Validate invariants
    if m.activeComponent < 0 || m.activeComponent >= 2 {
        return fmt.Errorf("invalid active component: %d", m.activeComponent)
    }

    if m.textInput == (textinput.Model{}) {
        return fmt.Errorf("text input not initialized")
    }

    if len(m.list.Items()) > 0 && m.list.Cursor() >= len(m.list.Items()) {
        return fmt.Errorf("list cursor out of bounds")
    }

    return nil
}

func (m Model) Update(msg tea.Msg) (tea.Model, tea.Cmd) {
    defer func() {
        if err := m.validateState(); err != nil {
            log.Printf("State validation error: %v", err)
        }
    }()

    // ... update logic
}
```

This debugging guide provides comprehensive strategies for identifying, diagnosing, and resolving common issues in BubbleTea applications. Use these techniques systematically to maintain healthy and performant terminal user interfaces.