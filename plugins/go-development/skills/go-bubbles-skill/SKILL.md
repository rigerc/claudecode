---
name: go-bubbles
description: This skill should be used when developers need help with the Bubbles component library for BubbleTea applications in Go. It provides expertise in implementing and configuring all Bubbles components including textinput, textarea, spinner, progress, table, list, paginator, timer, viewport, filepicker, and key bindings. The skill helps with component-specific usage patterns, styling with Lip Gloss, integration with BubbleTea applications, and troubleshooting common component issues. It serves as a comprehensive reference for building terminal user interfaces with the Bubbles component ecosystem.
---

# Go-Bubbles Component Library Expert

This skill transforms Claude into an expert assistant for the Go Bubbles component library, which provides production-ready UI components for building terminal user interfaces with BubbleTea applications.

## When to Use This Skill

Use this skill when developers need help with:

- **Component Implementation**: Setting up and configuring any Bubbles component
- **Component Styling**: Applying Lip Gloss styling to Bubbles components
- **Component Integration**: Integrating components into BubbleTea applications
- **Component Troubleshooting**: Debugging component behavior and interactions
- **Advanced Usage**: Customizing component behavior and creating extensions
- **Best Practices**: Following recommended patterns for component usage
- **Component Composition**: Combining multiple components effectively
- **Performance**: Optimizing component rendering and state management

## Core Components Coverage

### Text Input Components
- **textinput**: Single-line text input with validation and autocomplete
- **textarea**: Multi-line text input with vim-style editing

### Display Components
- **spinner**: Loading indicators with multiple animation styles
- **progress**: Progress bars with gradients and percentage display
- **table**: Data tables with headers, sorting, and selection
- **list**: Feature-rich lists with filtering and pagination

### Navigation Components
- **paginator**: Pagination controls with dot or numeric display
- **viewport**: Scrollable content areas with mouse support
- **filepicker**: File system navigation with filtering

### Utility Components
- **timer**: Countdown timers with configurable intervals
- **key**: Key binding definitions and management
- **help**: Help system generation and display

## Component Implementation Patterns

### Basic Component Setup

All Bubbles components follow this initialization pattern:

```go
func (m Model) Init() tea.Cmd {
    // Initialize components
    m.textInput = textinput.New()
    m.spinner = spinner.New()

    // Configure components
    m.textInput.Placeholder = "Enter text..."
    m.textInput.Focus()
    m.spinner.Spinner = spinner.Dot

    // Return initialization commands
    return tea.Batch(
        textinput.Blink,
        m.spinner.Tick,
    )
}
```

### Message Handling Pattern

```go
func (m Model) Update(msg tea.Msg) (tea.Model, tea.Cmd) {
    var cmd tea.Cmd

    // Update components first
    m.textInput, cmd = m.textInput.Update(msg)
    m.spinner, cmd = m.spinner.Update(msg)

    // Handle component-specific messages
    switch msg := msg.(type) {
    case textinput.BlurMsg:
        // Handle text input blur
    case spinner.TickMsg:
        // Handle spinner animation
    }

    return m, cmd
}
```

### Component Styling Pattern

```go
func (m Model) styleComponents() {
    // Text input styling
    m.textInput.Style = baseStyle
    m.textInput.CursorStyle = focusedStyle
    m.textInput.PlaceholderStyle = mutedStyle

    // Spinner styling
    m.spinner.Style = primaryColorStyle

    // Table styling
    m.table.SetStyles(table.Styles{
        Header: headerStyle,
        Selected: selectedStyle,
        Cell: cellStyle,
    })
}
```

## Available Resources

### Component Reference (`references/component_api.md`)
- Complete API documentation for all components
- Configuration options and methods
- Event handling patterns
- Usage examples

### Styling Patterns (`references/styling_guide.md`)
- Lip Gloss integration techniques
- Color schemes and theming
- Responsive design patterns
- Accessibility considerations

### Integration Examples (`references/integration_patterns.md`)
- Component composition patterns
- State management strategies
- Message passing between components
- Multi-component layouts

### Troubleshooting Guide (`references/troubleshooting.md`)
- Common component issues and solutions
- Debugging techniques
- Performance optimization
- Platform-specific considerations

### Component Templates (`assets/templates/`)
- Ready-to-use component implementations
- Customization examples
- Integration boilerplate
- Style variations

## Component-Specific Expertise

### Text Input Expertise

**Configuration Options:**
- Validation functions with custom error messages
- Echo modes for password fields
- Character limits and width constraints
- Auto-complete with suggestion filtering
- Clipboard integration

**Common Patterns:**
```go
// Password input
ti.EchoMode = textinput.EchoPassword
ti.EchoCharacter = '•'

// Validation
ti.Validate = func(s string) error {
    if len(s) < 3 {
        return fmt.Errorf("too short")
    }
    return nil
}

// Auto-complete
ti.ShowSuggestions = true
ti.KeyMap.AcceptSuggestion = key.NewBinding(key.WithKeys(tea.KeyTab))
```

### Table Component Expertise

**Advanced Features:**
- Dynamic column sizing and sorting
- Row selection and filtering
- Custom cell rendering
- Keyboard navigation shortcuts
- Performance optimization for large datasets

**Implementation Patterns:**
```go
// Column configuration
columns := []table.Column{
    {Title: "Name", Width: 20},
    {Title: "Email", Width: 30},
}

// Styling
t.SetStyles(table.Styles{
    Header: headerStyle,
    Selected: selectedStyle,
})

// Row operations
t.SetRows(dataRows)
t.AppendRow(newRow)
t.SelectedRow()
```

### List Component Expertise

**Feature Rich Lists:**
- Fuzzy search and filtering
- Pagination with customizable controls
- Item selection and multi-selection
- Custom item rendering
- Status messages and help text

**Delegate Customization:**
```go
// Custom delegate
delegate := list.NewDefaultDelegate()
delegate.ShowDescription = true
delegate.SetSpacing(1)
delegate.UpdateFunc = ...

// List configuration
l := list.New(items, delegate, width, height)
l.SetFilteringEnabled(true)
l.SetShowStatusBar(true)
```

### Spinner Component Expertise

**Animation Styles:**
- 15+ built-in spinner types
- Custom frame sequences
- Speed control (FPS)
- Color theming

**Usage Patterns:**
```go
// Built-in types
s.Spinner = spinner.Dot
s.Spinner = spinner.Line
s.Spinner = spinner.Points

// Custom spinner
s.Spinner = spinner.Spinner{
    Frames: []string{"⠋", "⠙", "⠹", "⠸"},
    FPS:    time.Second / 10,
}

// Styling
s.Style = lipgloss.NewStyle().Foreground(lipgloss.Color("62"))
```

## Integration Best Practices

### Component Lifecycle Management

1. **Initialization**: Set up components in Init() method
2. **Message Handling**: Update components first, then handle messages
3. **Styling**: Apply consistent styles across components
4. **Resource Cleanup**: Clean up resources on application quit

### Performance Optimization

1. **Viewport Usage**: Use viewport for large content areas
2. **Data Limiting**: Limit list/table items to reasonable sizes
3. **Caching**: Cache expensive calculations and styling
4. **Frame Rate**: Limit frame rate with tea.WithFPS()

### Error Handling

1. **Validation**: Use built-in validation for input components
2. **Graceful Degradation**: Handle component failures gracefully
3. **User Feedback**: Provide clear error messages and recovery options
4. **Logging**: Log component issues for debugging

## Advanced Usage Scenarios

### Multi-Component Forms

```go
type FormModel struct {
    fields    map[string]textinput.Model
    active    int
    validator FormValidator
}

func (m FormModel) Update(msg tea.Msg) (tea.Model, tea.Cmd) {
    // Update active field
    field := m.fields[m.fieldOrder[m.active]]
    field, cmd := field.Update(msg)
    m.fields[m.fieldOrder[m.active]] = field

    // Handle navigation
    switch msg := msg.(type) {
    case tea.KeyMsg:
        switch msg.String() {
        case "tab":
            m.cycleFocus()
        case "enter":
            return m, m.validateAndSubmit()
        }
    }

    return m, cmd
}
```

### Data Tables with Sorting

```go
type SortableTableModel struct {
    table      table.Model
    data       []DataRow
    sortColumn int
    ascending  bool
}

func (m SortableTableModel) sortData() {
    sort.Slice(m.data, func(i, j int) bool {
        // Sorting logic based on sortColumn and ascending flag
        return m.compareRows(m.data[i], m.data[j])
    })

    // Update table with sorted data
    m.updateTableRows()
}
```

### Custom Component Extensions

```go
// Extend existing components
type EnhancedTextInput struct {
    textinput.Model
    history []string
    index   int
}

func (e *EnhancedTextInput) Update(msg tea.Msg) (EnhancedTextInput, tea.Cmd) {
    // Handle custom functionality
    switch msg := msg.(type) {
    case tea.KeyMsg:
        if msg.String() == "up" {
            return e.navigateHistory(-1), nil
        }
    }

    // Delegate to base component
    newModel, cmd := e.Model.Update(msg)
    e.Model = newModel
    return e, cmd
}
```

## Common Troubleshooting Solutions

### Component Not Receiving Input

**Issue**: Component doesn't respond to keyboard events

**Solution**: Ensure component focus and proper message routing
```go
// Check focus
if !m.textInput.Focused() {
    m.textInput.Focus()
}

// Update component first in Update method
m.textInput, cmd = m.textInput.Update(msg)
```

### Performance Issues

**Issue**: Slow rendering with large lists/tables

**Solution**: Use pagination and limit data size
```go
const MAX_ITEMS = 1000

func (m Model) filterData(query string) {
    if len(m.data) > MAX_ITEMS {
        m.data = m.data[:MAX_ITEMS]
    }
}
```

### Styling Problems

**Issue**: Styles not applying consistently

**Solution**: Use adaptive colors and check terminal capabilities
```go
style := lipgloss.NewStyle().
    Foreground(lipgloss.AdaptiveColor{Light: "63", Dark: "228"})
```

## Testing Strategies

### Component Unit Tests

```go
func TestTextInputValidation(t *testing.T) {
    ti := textinput.New()
    ti.Validate = func(s string) error {
        if len(s) < 3 {
            return fmt.Errorf("too short")
        }
        return nil
    }

    // Test valid input
    err := ti.Validate("hello")
    assert.NoError(t, err)

    // Test invalid input
    err = ti.Validate("hi")
    assert.Error(t, err)
}
```

### Integration Tests

```go
func TestFormSubmission(t *testing.T) {
    model := NewFormModel()

    // Fill form
    model = fillForm(model)

    // Submit
    newModel, cmd := model.Update(tea.KeyMsg{Type: tea.KeyEnter})

    assert.NotNil(t, cmd)
    assert.Equal(t, tea.Quit(), cmd)
}
```

## Development Workflow

### Component Development Steps

1. **Setup**: Initialize component with default configuration
2. **Configuration**: Apply custom settings and styling
3. **Integration**: Add to model with proper message handling
4. **Testing**: Write unit tests for component behavior
5. **Styling**: Apply consistent styling with Lip Gloss
6. **Documentation**: Document custom behavior and configuration

### Debugging Component Issues

1. **Enable Logging**: Add debug logging for component messages
2. **Check State**: Verify component state at key points
3. **Test in Isolation**: Create minimal reproduction cases
4. **Profile Performance**: Use profiling tools for performance issues
5. **Validate Input**: Check for invalid or edge case inputs

This skill provides comprehensive expertise for leveraging the Bubbles component library to create sophisticated, performant terminal user interfaces in Go.