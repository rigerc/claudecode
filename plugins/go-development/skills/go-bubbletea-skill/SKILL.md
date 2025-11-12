---
name: go-bubbletea
description: This skill should be used when developers need help building terminal user interfaces (TUIs) using the BubbleTea framework and Bubbles component library in Go. It provides expertise in the Model-View-Update pattern, component usage, styling with Lip Gloss, performance optimization, debugging, and best practices for creating sophisticated terminal applications. The skill assists with everything from basic form creation to complex real-time dashboards, helping developers write clean, efficient, and maintainable TUI applications.
---

# Go-BubbleTea TUI Development Expert

This skill transforms Claude into an expert assistant for Go developers building terminal user interfaces using the BubbleTea framework. It provides comprehensive knowledge of the Model-View-Update pattern, Bubbles components, styling with Lip Gloss, and best practices for creating sophisticated terminal applications.

## When to Use This Skill

Use this skill when developers need help with:

- Creating BubbleTea applications from scratch
- Implementing and configuring Bubbles components (textinput, textarea, spinner, progress, table, list, etc.)
- Styling TUI components with Lip Gloss
- Component composition and state management
- Performance optimization for complex applications
- Debugging BubbleTea applications and components
- Testing strategies for TUI applications
- Integration patterns and advanced architecture
- Real-time dashboards and data visualization
- File system navigation and external process integration

## Core Concepts and Patterns

### Model-View-Update Architecture

When implementing BubbleTea applications, follow the Elm Architecture pattern:

1. **Model** - Store application state as a struct
2. **Init()** - Return initial commands for startup
3. **Update()** - Handle messages and return new model + commands
4. **View()** - Render the model as a string

Always use immutable updates by returning new models rather than modifying in place.

### Message System

Leverage the message-passing system for:
- Keyboard and mouse input handling
- Timer-based operations
- External process execution
- Custom application events
- Component communication

Use `tea.Batch()` for concurrent operations and `tea.Sequence()` for sequential operations.

### Component Integration

Integrate Bubbles components following these patterns:

1. **Initialize** components in your model struct
2. **Update** components first in your Update method
3. **Handle** component-specific messages
4. **Style** consistently using Lip Gloss

## Available Resources

### Component Templates (`assets/component_templates/`)

Use these templates for common component implementations:

- `text_form.md` - Multi-field text input forms with validation
- `data_table.md` - Sortable and filterable data tables
- `file_explorer.md` - File system navigation with filtering
- `progress_tracker.md` - Multi-stage progress indicators
- `real_time_dashboard.md` - Live data visualization
- `interactive_list.md` - Advanced lists with search and pagination

### Project Boilerplate (`assets/project_templates/`)

Use these templates for project structure:

- `basic_app/` - Simple BubbleTea application structure
- `component_library/` - Reusable component organization
- `complex_dashboard/` - Multi-component dashboard architecture
- `cli_tool/` - Command-line tool with interactive elements

### Styling Resources (`references/styling_patterns.md`)

Consult styling patterns for:
- Consistent color schemes and themes
- Responsive layout techniques
- Border and spacing patterns
- Accessibility considerations

### Testing Strategies (`references/testing_patterns.md`)

Follow testing approaches for:
- Component unit tests
- Integration testing
- Performance benchmarking
- User interaction simulation

## Development Workflow

### 1. Application Structure

Always start with a clear model structure:

```go
type Model struct {
    // Component states
    textInput textinput.Model
    table     table.Model

    // Application state
    loading   bool
    data      []DataItem
    error     error

    // UI state
    active    int // Which component is focused
}
```

### 2. Component Integration Pattern

Follow this pattern for component integration:

```go
func (m Model) Update(msg tea.Msg) (tea.Model, tea.Cmd) {
    var cmd tea.Cmd

    // Update active component first
    switch m.active {
    case 0:
        m.textInput, cmd = m.textInput.Update(msg)
    case 1:
        m.table, cmd = m.table.Update(msg)
    }

    // Handle application-level messages
    switch msg := msg.(type) {
    case tea.KeyMsg:
        switch msg.Type {
        case tea.KeyTab:
            m.active = (m.active + 1) % 2
            return m, m.updateFocus()
        }
    }

    return m, cmd
}
```

### 3. Styling Approach

Use consistent styling patterns:

```go
var (
    // Define color palette
    primaryColor   = lipgloss.Color("62")    // Purple
    secondaryColor = lipgloss.Color("205")   // Pink
    accentColor    = lipgloss.Color("226")   // Yellow

    // Base styles
    baseStyle = lipgloss.NewStyle().
        Foreground(lipgloss.Color("255")).
        Padding(1, 2)

    // Component styles
    focusedStyle = baseStyle.
        Background(primaryColor).
        Bold(true)
)
```

### 4. Error Handling Pattern

Implement graceful error handling:

```go
type errorMsg struct{ err error }

func (e errorMsg) Error() string { return e.err.Error() }

func (m Model) Update(msg tea.Msg) (tea.Model, tea.Cmd) {
    switch msg := msg.(type) {
    case errorMsg:
        m.error = msg.err
        return m, nil // Continue running with error state
    }
    return m, nil
}

func (m Model) View() string {
    if m.error != nil {
        return errorStyle.Render("Error: " + m.error.Error())
    }
    // Normal view rendering
}
```

## Performance Optimization

### Efficient Rendering

- Use `viewport.Model` for large content areas
- Limit frame rate with `tea.WithFPS(30)`
- Batch UI updates using debouncing
- Only render changed components

### Memory Management

- Limit data structures (max 1000 items in lists/tables)
- Clean up resources on quit
- Use streaming for large datasets
- Implement pagination for navigation

### Command Optimization

- Batch related operations with `tea.Batch()`
- Use background commands for heavy computation
- Implement debouncing for rapid updates
- Cache expensive computations

## Common Issues and Solutions

### Component Not Receiving Input

**Problem**: Component doesn't respond to key events
**Solution**: Ensure proper focus management and message routing

```go
// Make sure component is focused
ti.Focus()
// not focused.FBlur()

// Check message order - let component handle first
func (m Model) Update(msg tea.Msg) (tea.Model, tea.Cmd) {
    var cmd tea.Cmd
    // Update component first
    m.textInput, cmd = m.textInput.Update(msg)
    // Then handle application messages
    return m, cmd
}
```

### Styling Issues

**Problem**: Styles not applying consistently
**Solution**: Check color support and use adaptive colors

```go
// Use adaptive colors for better compatibility
style := lipgloss.NewStyle().
    Foreground(lipgloss.AdaptiveColor{Light: "63", Dark: "228"})
```

### Performance Problems

**Problem**: Slow rendering with large datasets
**Solution**: Use viewport and limit data size

```go
// Use viewport for large content
type Model struct {
    viewport viewport.Model
}

func (m Model) View() string {
    return m.viewport.View() // Only renders visible portion
}
```

## Testing Strategy

### Component Testing

```go
func TestTextInputComponent(t *testing.T) {
    ti := textinput.New()
    model := Model{textInput: ti}

    // Test input handling
    msg := tea.KeyMsg{Type: tea.KeyRunes, Runes: []rune("hello")}
    newModel, _ := model.Update(msg)

    assert.Equal(t, "hello", newModel.textInput.Value())
}
```

### Integration Testing

```go
func TestFormSubmission(t *testing.T) {
    m := initialModel()

    // Fill form
    m = fillFormStep1(t, m)
    m = fillFormStep2(t, m)

    // Test submission
    newModel, cmd := m.Update(tea.KeyMsg{Type: tea.KeyEnter})

    assert.NotNil(t, cmd) // Should return submission command
}
```

## Advanced Patterns

### Multi-Component Communication

Use custom messages for component communication:

```go
type FormSubmitMsg struct {
    Values map[string]string
}

type ValidationErrorMsg struct {
    Field   string
    Message string
}
```

### External Process Integration

```go
func (m Model) Update(msg tea.Msg) (tea.Model, tea.Cmd) {
    switch msg := msg.(type) {
    case tea.KeyMsg:
        if msg.String() == "e" {
            cmd := exec.Command("vim", "file.txt")
            return m, tea.ExecProcess(cmd, func(err error) tea.Msg {
                return editorFinishedMsg{err: err}
            })
        }
    }
    return m, nil
}
```

### Real-time Data Updates

```go
func (m Model) Init() tea.Cmd {
    return tea.Batch(
        tea.Tick(time.Second, func(t time.Time) tea.Msg {
            return dataUpdateMsg{}
        }),
        loadInitialData(),
    )
}
```

## Resource Usage Guidelines

### When to Load References

Load `references/styling_patterns.md` when:
- Need specific styling examples
- Creating consistent themes
- Troubleshooting visual issues

Load `references/testing_patterns.md` when:
- Writing unit tests for components
- Creating integration tests
- Performance testing

Load `references/integration_patterns.md` when:
- Building complex multi-component applications
- Implementing component communication
- Designing application architecture

### When to Use Templates

Use `assets/component_templates/` when:
- Creating standard component patterns
- Need boilerplate for common UI elements
- Building reusable component libraries

Use `assets/project_templates/` when:
- Starting new BubbleTea projects
- Need project structure guidance
- Setting up development environment

## Debugging Checklist

Before asking for help, verify:

1. **Component Focus**: Is the intended component focused?
2. **Message Flow**: Are messages being routed correctly?
3. **State Updates**: Is the model being updated immutably?
4. **Style Application**: Are styles using correct color values?
5. **Performance**: Is the app using viewport for large content?
6. **Resources**: Are resources being cleaned up properly?

## Best Practices Summary

1. **Immutable Updates**: Always return new models
2. **Component Lifecycle**: Init → Update → View
3. **Focus Management**: Track and update component focus
4. **Error Handling**: Graceful degradation with error states
5. **Performance**: Limit data size and use efficient rendering
6. **Testing**: Test components and integration separately
7. **Styling**: Use consistent color schemes and adaptive colors
8. **Resources**: Clean up on quit and limit memory usage

This skill provides comprehensive expertise for building sophisticated, maintainable terminal user interfaces using BubbleTea and the Go ecosystem.