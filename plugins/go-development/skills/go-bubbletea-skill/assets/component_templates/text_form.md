# Multi-Field Text Form Template

## Description
A comprehensive form template with multiple text input fields, validation, error handling, and navigation.

## Features
- Multiple text input fields with different types
- Field validation with custom error messages
- Tab navigation between fields
- Submit and cancel functionality
- Password field support
- Auto-complete suggestions

## Implementation

```go
package main

import (
    "fmt"
    "strings"
    tea "github.com/charmbracelet/bubbletea"
    "github.com/charmbracelet/bubbles/textinput"
    "github.com/charmbracelet/lipgloss"
)

// Form field configuration
type FieldConfig struct {
    Label      string
    Name       string
    Placeholder string
    Required   bool
    Type       FieldType
    Validate   func(string) error
    Suggest    func(string) []string
}

type FieldType int

const (
    FieldText FieldType = iota
    FieldEmail
    FieldPassword
    FieldNumber
    FieldPhone
)

// Form model
type FormModel struct {
    fields    map[string]*Field
    order     []string
    current   int
    submitting bool
    errors    map[string]string
    onSubmit  func(map[string]string) tea.Cmd
    onCancel  tea.Cmd
    styles    FormStyles
}

type Field struct {
    input    textinput.Model
    config   FieldConfig
    showingSuggestions bool
    suggestions []string
    selectedSuggestion int
}

type FormStyles struct {
    Label      lipgloss.Style
    Input      lipgloss.Style
    Focused    lipgloss.Style
    Error      lipgloss.Style
    Button     lipgloss.Style
    Active     lipgloss.Style
    Title      lipgloss.Style
}

// Initialize form with default styles
func NewFormStyles() FormStyles {
    return FormStyles{
        Label: lipgloss.NewStyle().
            Foreground(lipgloss.Color("62")).
            Bold(true).
            MarginBottom(1),

        Input: lipgloss.NewStyle().
            Foreground(lipgloss.Color("255")).
            Background(lipgloss.Color("237")).
            Border(lipgloss.NormalBorder()).
            BorderForeground(lipgloss.Color("239")).
            Padding(0, 1),

        Focused: lipgloss.NewStyle().
            Foreground(lipgloss.Color("255")).
            Background(lipgloss.Color("237")).
            Border(lipgloss.NormalBorder()).
            BorderForeground(lipgloss.Color("62")).
            Padding(0, 1),

        Error: lipgloss.NewStyle().
            Foreground(lipgloss.Color("9")).
            MarginLeft(2).
            MarginBottom(1),

        Button: lipgloss.NewStyle().
            Foreground(lipgloss.Color("255")).
            Background(lipgloss.Color("62")).
            Padding(0, 2).
            MarginRight(1),

        Active: lipgloss.NewStyle().
            Foreground(lipgloss.Color("0")).
            Background(lipgloss.Color("205")).
            Padding(0, 2).
            MarginRight(1),

        Title: lipgloss.NewStyle().
            Foreground(lipgloss.Color("62")).
            Bold(true).
            MarginBottom(2),
    }
}

// Create new form
func NewForm(configs []FieldConfig, onSubmit func(map[string]string) tea.Cmd, onCancel tea.Cmd) FormModel {
    fields := make(map[string]*Field)
    order := make([]string, len(configs))

    for i, config := range configs {
        order[i] = config.Name

        ti := textinput.New()
        ti.Placeholder = config.Placeholder
        ti.CharLimit = 50
        ti.Width = 40

        // Configure input based on type
        switch config.Type {
        case FieldPassword:
            ti.EchoMode = textinput.EchoPassword
        case FieldEmail:
            ti.Validate = validateEmail
        case FieldNumber:
            ti.Validate = validateNumber
        case FieldPhone:
            ti.Validate = validatePhone
        }

        // Custom validation
        if config.Validate != nil {
            ti.Validate = config.Validate
        }

        // Enable suggestions if provided
        if config.Suggest != nil {
            ti.ShowSuggestions = true
            ti.KeyMap.AcceptSuggestion = key.NewBinding(
                key.WithKeys(tea.KeyTab, tea.KeyDown),
                key.WithHelp("tab/↓", "accept"),
            )
        }

        fields[config.Name] = &Field{
            input:  ti,
            config: config,
        }
    }

    // Focus first field
    if len(fields) > 0 {
        fields[order[0]].input.Focus()
    }

    return FormModel{
        fields:   fields,
        order:    order,
        current:  0,
        errors:   make(map[string]string),
        onSubmit: onSubmit,
        onCancel: onCancel,
        styles:   NewFormStyles(),
    }
}

// Update form state
func (m FormModel) Update(msg tea.Msg) (tea.Model, tea.Cmd) {
    var cmd tea.Cmd

    switch msg := msg.(type) {
    case tea.KeyMsg:
        switch msg.Type {
        case tea.KeyCtrlC, tea.KeyEscape:
            return m, m.onCancel

        case tea.KeyEnter:
            if m.validateAndSubmit() {
                return m, m.submitForm()
            }

        case tea.KeyTab, tea.KeyDown:
            if m.currentField().showingSuggestions {
                return m, m.selectSuggestion()
            }
            return m, m.nextField()

        case tea.KeyShiftTab, tea.KeyUp:
            if m.currentField().showingSuggestions {
                return m, m.previousSuggestion()
            }
            return m, m.previousField()

        case tea.KeyRight:
            if m.currentField().showingSuggestions {
                return m, m.nextSuggestion()
            }

        case tea.KeyLeft:
            if m.currentField().showingSuggestions {
                return m, m.previousSuggestion()
            }
        }
    }

    // Update current field
    currentField := m.currentField()
    newInput, inputCmd := currentField.input.Update(msg)
    currentField.input = newInput

    // Update suggestions if typing
    if msg, ok := msg.(tea.KeyMsg); ok && msg.Type == tea.KeyRunes {
        m.updateSuggestions()
    }

    return m, tea.Batch(cmd, inputCmd)
}

// Render form
func (m FormModel) View() string {
    var content strings.Builder

    // Title
    content.WriteString(m.styles.Title.Render("Application Form") + "\n\n")

    // Render all fields
    for _, name := range m.order {
        field := m.fields[name]

        // Label
        label := field.config.Label
        if field.config.Required {
            label += " *"
        }
        content.WriteString(m.styles.Label.Render(label))

        // Input field
        inputStyle := m.styles.Input
        if m.current == m.indexOf(name) {
            inputStyle = m.styles.Focused
        }

        content.WriteString(inputStyle.Render(field.input.View()))

        // Error message
        if errMsg, exists := m.errors[name]; exists {
            content.WriteString("\n" + m.styles.Error.Render("⚠ " + errMsg))
        }

        // Suggestions
        if field.showingSuggestions && len(field.suggestions) > 0 {
            content.WriteString(m.renderSuggestions(field))
        }

        content.WriteString("\n\n")
    }

    // Buttons
    content.WriteString(m.styles.Button.Render("Submit (Enter)"))
    content.WriteString(m.styles.Button.Render("Cancel (Esc)"))

    return content.String()
}

// Helper methods
func (m FormModel) currentField() *Field {
    return m.fields[m.order[m.current]]
}

func (m FormModel) indexOf(name string) int {
    for i, fieldName := range m.order {
        if fieldName == name {
            return i
        }
    }
    return -1
}

func (m FormModel) nextField() (tea.Model, tea.Cmd) {
    m.currentField().input.Blur()
    m.current = (m.current + 1) % len(m.order)
    m.currentField().input.Focus()
    return m, nil
}

func (m FormModel) previousField() (tea.Model, tea.Cmd) {
    m.currentField().input.Blur()
    m.current = (m.current - 1 + len(m.order)) % len(m.order)
    m.currentField().input.Focus()
    return m, nil
}

func (m FormModel) validateAndSubmit() bool {
    m.errors = make(map[string]string)

    for name, field := range m.fields {
        value := field.input.Value()

        // Required validation
        if field.config.Required && strings.TrimSpace(value) == "" {
            m.errors[name] = field.config.Label + " is required"
            continue
        }

        // Field-specific validation
        if value != "" && field.input.Validate != nil {
            if err := field.input.Validate(value); err != nil {
                m.errors[name] = err.Error()
            }
        }
    }

    return len(m.errors) == 0
}

func (m FormModel) submitForm() tea.Cmd {
    values := make(map[string]string)
    for name, field := range m.fields {
        values[name] = field.input.Value()
    }
    return m.onSubmit(values)
}

func (m FormModel) updateSuggestions() {
    field := m.currentField()
    if field.config.Suggest != nil {
        suggestions := field.config.Suggest(field.input.Value())
        field.suggestions = suggestions
        field.showingSuggestions = len(suggestions) > 0
        field.selectedSuggestion = 0
    }
}

func (m FormModel) selectSuggestion() (tea.Model, tea.Cmd) {
    field := m.currentField()
    if field.selectedSuggestion < len(field.suggestions) {
        field.input.SetValue(field.suggestions[field.selectedSuggestion])
        field.showingSuggestions = false
        field.selectedSuggestion = 0
    }
    return m, nil
}

func (m FormModel) nextSuggestion() (tea.Model, tea.Cmd) {
    field := m.currentField()
    if field.selectedSuggestion < len(field.suggestions)-1 {
        field.selectedSuggestion++
    }
    return m, nil
}

func (m FormModel) previousSuggestion() (tea.Model, tea.Cmd) {
    field := m.currentField()
    if field.selectedSuggestion > 0 {
        field.selectedSuggestion--
    }
    return m, nil
}

func (m FormModel) renderSuggestions(field *Field) string {
    var suggestions strings.Builder

    for i, suggestion := range field.suggestions {
        style := lipgloss.NewStyle().
            Foreground(lipgloss.Color("240")).
            MarginLeft(2).
            Padding(0, 1)

        if i == field.selectedSuggestion {
            style = style.
                Foreground(lipgloss.Color("255")).
                Background(lipgloss.Color("62")).
                Bold(true)
        }

        suggestions.WriteString(style.Render("• " + suggestion) + "\n")
    }

    return suggestions.String()
}

// Validation functions
func validateEmail(email string) error {
    if !strings.Contains(email, "@") {
        return fmt.Errorf("must contain @ symbol")
    }
    if !strings.Contains(email, ".") {
        return fmt.Errorf("must contain domain")
    }
    return nil
}

func validateNumber(num string) error {
    for _, r := range num {
        if r < '0' || r > '9' {
            return fmt.Errorf("must contain only numbers")
        }
    }
    return nil
}

func validatePhone(phone string) error {
    if len(phone) < 10 {
        return fmt.Errorf("must be at least 10 digits")
    }
    return nil
}
```

## Usage Example

```go
func main() {
    // Form configuration
    configs := []FieldConfig{
        {
            Label:      "Full Name",
            Name:       "name",
            Placeholder: "Enter your full name",
            Required:   true,
            Type:       FieldText,
            Validate: func(name string) error {
                if len(strings.TrimSpace(name)) < 2 {
                    return fmt.Errorf("name must be at least 2 characters")
                }
                return nil
            },
        },
        {
            Label:      "Email Address",
            Name:       "email",
            Placeholder: "you@example.com",
            Required:   true,
            Type:       FieldEmail,
        },
        {
            Label:      "Password",
            Name:       "password",
            Placeholder: "Enter password",
            Required:   true,
            Type:       FieldPassword,
            Validate: func(pw string) error {
                if len(pw) < 8 {
                    return fmt.Errorf("password must be at least 8 characters")
                }
                return nil
            },
        },
        {
            Label:      "Phone",
            Name:       "phone",
            Placeholder: "(555) 123-4567",
            Required:   false,
            Type:       FieldPhone,
        },
    }

    // Submit handler
    onSubmit := func(values map[string]string) tea.Cmd {
        return tea.Printf("Form submitted: %+v", values)
    }

    // Cancel handler
    onCancel := tea.Quit

    // Create form
    form := NewForm(configs, onSubmit, onCancel)

    // Start program
    p := tea.NewProgram(form)
    if _, err := p.Run(); err != nil {
        fmt.Printf("Error: %v", err)
    }
}
```

## Customization Options

- **Field Types**: Text, Email, Password, Number, Phone
- **Validation**: Built-in and custom validation functions
- **Auto-complete**: Dynamic suggestions with keyboard navigation
- **Styling**: Customizable colors, borders, and spacing
- **Navigation**: Tab, Arrow keys, and custom key bindings
- **Error Handling**: Per-field error messages with styling

## Best Practices

1. **Always validate required fields**
2. **Provide clear error messages**
3. **Use consistent styling across fields**
4. **Implement keyboard navigation**
5. **Handle edge cases (empty input, special characters)**
6. **Consider accessibility with clear labels and help text**