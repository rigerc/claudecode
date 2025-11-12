# Text Input Form Template

## Description
A complete form template using multiple textinput components with validation, navigation, and styling.

## Features
- Multiple text input fields with different types (text, email, password)
- Form validation with custom error messages
- Tab/Shift+Tab navigation between fields
- Submit and cancel functionality
- Consistent styling with Lip Gloss
- Focus management and visual indicators

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

// Form model
type Model struct {
    fields       []FieldConfig
    textInputs   []textinput.Model
    active       int
    errors       map[string]string
    submitted    bool
    submitButton string
    styles       FormStyles
}

type FieldConfig struct {
    Name        string
    Label       string
    Placeholder string
    Required    bool
    Type        InputType
    Validate    func(string) error
}

type InputType int

const (
    InputText InputType = iota
    InputEmail
    InputPassword
    InputNumber
)

type FormStyles struct {
    Label      lipgloss.Style
    Input      lipgloss.Style
    Focused    lipgloss.Style
    Error      lipgloss.Style
    Button     lipgloss.Style
    Title      lipgloss.Style
    Status     lipgloss.Style
}

// Create new form
func NewForm() Model {
    // Define form fields
    fields := []FieldConfig{
        {
            Name:        "username",
            Label:       "Username",
            Placeholder: "Enter username",
            Required:    true,
            Type:        InputText,
            Validate:    validateUsername,
        },
        {
            Name:        "email",
            Label:       "Email Address",
            Placeholder: "user@example.com",
            Required:    true,
            Type:        InputEmail,
            Validate:    validateEmail,
        },
        {
            Name:        "password",
            Label:       "Password",
            Placeholder: "Enter password",
            Required:    true,
            Type:        InputPassword,
            Validate:    validatePassword,
        },
        {
            Name:        "age",
            Label:       "Age",
            Placeholder: "25",
            Required:    false,
            Type:        InputNumber,
            Validate:    validateAge,
        },
    }

    // Create text inputs
    var textInputs []textinput.Model
    for _, field := range fields {
        ti := textinput.New()
        ti.Placeholder = field.Placeholder
        ti.CharLimit = 50
        ti.Width = 40

        // Configure based on type
        switch field.Type {
        case InputPassword:
            ti.EchoMode = textinput.EchoPassword
        case InputNumber:
            ti.Validate = validateNumber
        case InputEmail:
            ti.Validate = validateEmail
        }

        textInputs = append(textInputs, ti)
    }

    // Focus first input
    if len(textInputs) > 0 {
        textInputs[0].Focus()
    }

    // Initialize styles
    styles := FormStyles{
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

        Title: lipgloss.NewStyle().
            Foreground(lipgloss.Color("62")).
            Bold(true).
            MarginBottom(2),

        Status: lipgloss.NewStyle().
            Foreground(lipgloss.Color("46")).
            Bold(true).
            MarginTop(1),
    }

    return Model{
        fields:     fields,
        textInputs: textInputs,
        active:     0,
        errors:     make(map[string]string),
        styles:     styles,
    }
}

// Update method
func (m Model) Update(msg tea.Msg) (tea.Model, tea.Cmd) {
    var cmd tea.Cmd

    switch msg := msg.(type) {
    case tea.KeyMsg:
        switch msg.String() {
        case "ctrl+c", "esc":
            return m, tea.Quit

        case "tab":
            return m, m.nextField()

        case "shift+tab":
            return m, m.previousField()

        case "enter":
            if m.validateForm() {
                m.submitted = true
                return m, m.submitForm()
            }

        case "down":
            if m.active < len(m.textInputs)-1 {
                return m, m.nextField()
            }

        case "up":
            if m.active > 0 {
                return m, m.previousField()
            }
        }

    // Update active text input
    if m.active >= 0 && m.active < len(m.textInputs) {
        m.textInputs[m.active], cmd = m.textInputs[m.active].Update(msg)
    }

    return m, cmd
}

// View method
func (m Model) View() string {
    if m.submitted {
        return m.styles.Status.Render("✓ Form submitted successfully!") + "\n" +
               m.styles.Title.Render("Submitted Values:") + "\n" +
               m.renderSubmittedValues()
    }

    var content strings.Builder

    // Title
    content.WriteString(m.styles.Title.Render("📝 Registration Form") + "\n\n")

    // Render fields
    for i, field := range m.fields {
        // Label
        label := field.Label
        if field.Required {
            label += " *"
        }

        content.WriteString(m.styles.Label.Render(label))

        // Input field
        inputStyle := m.styles.Input
        if i == m.active {
            inputStyle = m.styles.Focused
        }

        content.WriteString(inputStyle.Render(m.textInputs[i].View()))

        // Error message
        if errMsg, exists := m.errors[field.Name]; exists {
            content.WriteString("\n" + m.styles.Error.Render("⚠ " + errMsg))
        }

        content.WriteString("\n\n")
    }

    // Buttons
    content.WriteString(m.styles.Button.Render("Submit (Enter)"))
    content.WriteString(m.styles.Button.Render("Cancel (Esc)"))

    return content.String()
}

// Helper methods
func (m Model) nextField() tea.Model {
    // Blur current field
    m.textInputs[m.active].Blur()

    // Move to next field
    m.active = (m.active + 1) % len(m.textInputs)

    // Focus new field
    m.textInputs[m.active].Focus()

    return m
}

func (m Model) previousField() tea.Model {
    // Blur current field
    m.textInputs[m.active].Blur()

    // Move to previous field
    m.active = (m.active - 1 + len(m.textInputs)) % len(m.textInputs)

    // Focus new field
    m.textInputs[m.active].Focus()

    return m
}

func (m Model) validateForm() bool {
    m.errors = make(map[string]string)

    for i, field := range m.fields {
        value := m.textInputs[i].Value()

        // Required validation
        if field.Required && strings.TrimSpace(value) == "" {
            m.errors[field.Name] = field.Label + " is required"
            continue
        }

        // Field-specific validation
        if value != "" && field.Validate != nil {
            if err := field.Validate(value); err != nil {
                m.errors[field.Name] = err.Error()
            }
        }
    }

    return len(m.errors) == 0
}

func (m Model) submitForm() tea.Cmd {
    values := make(map[string]string)
    for i, field := range m.fields {
        values[field.Name] = m.textInputs[i].Value()
    }

    return tea.Printf("Form submitted: %+v", values)
}

func (m Model) renderSubmittedValues() string {
    var content strings.Builder

    for i, field := range m.fields {
        value := m.textInputs[i].Value()
        content.WriteString(fmt.Sprintf("%s: %s\n", field.Label, value))
    }

    return content.String()
}

// Validation functions
func validateUsername(username string) error {
    if len(strings.TrimSpace(username)) < 3 {
        return fmt.Errorf("username must be at least 3 characters")
    }

    if len(username) > 20 {
        return fmt.Errorf("username must be less than 20 characters")
    }

    // Check for valid characters
    for _, r := range username {
        if !((r >= 'a' && r <= 'z') || (r >= 'A' && r <= 'Z') || (r >= '0' && r <= '9') || r == '_') {
            return fmt.Errorf("username can only contain letters, numbers, and underscores")
        }
    }

    return nil
}

func validateEmail(email string) error {
    if !strings.Contains(email, "@") {
        return fmt.Errorf("must contain @ symbol")
    }

    if !strings.Contains(email, ".") {
        return fmt.Errorf("must contain domain")
    }

    // Basic email format validation
    parts := strings.Split(email, "@")
    if len(parts) != 2 {
        return fmt.Errorf("invalid email format")
    }

    if len(parts[0]) == 0 || len(parts[1]) == 0 {
        return fmt.Errorf("invalid email format")
    }

    return nil
}

func validatePassword(password string) error {
    if len(password) < 8 {
        return fmt.Errorf("password must be at least 8 characters")
    }

    if len(password) > 50 {
        return fmt.Errorf("password must be less than 50 characters")
    }

    // Check for complexity
    hasUpper := false
    hasLower := false
    hasNumber := false
    hasSpecial := false

    for _, r := range password {
        switch {
        case r >= 'A' && r <= 'Z':
            hasUpper = true
        case r >= 'a' && r <= 'z':
            hasLower = true
        case r >= '0' && r <= '9':
            hasNumber = true
        case strings.ContainsRune("!@#$%^&*()_+-=[]{}|;':, r):
            hasSpecial = true
        }
    }

    if !hasUpper {
        return fmt.Errorf("password must contain at least one uppercase letter")
    }

    if !hasLower {
        return fmt.Errorf("password must contain at least one lowercase letter")
    }

    if !hasNumber {
        return fmt.Errorf("password must contain at least one number")
    }

    if !hasSpecial {
        return fmt.Errorf("password must contain at least one special character")
    }

    return nil
}

func validateAge(age string) error {
    if age == "" {
        return nil // Optional field
    }

    for _, r := range age {
        if r < '0' || r > '9' {
            return fmt.Errorf("age must contain only numbers")
        }
    }

    ageNum := 0
    for _, r := range age {
        ageNum = ageNum*10 + int(r-'0')
    }

    if ageNum < 1 || ageNum > 120 {
        return fmt.Errorf("age must be between 1 and 120")
    }

    return nil
}

func validateNumber(number string) error {
    if number == "" {
        return nil // Optional field
    }

    for _, r := range number {
        if r < '0' || r > '9' {
            return fmt.Errorf("must contain only numbers")
        }
    }

    return nil
}

// Main function
func main() {
    p := tea.NewProgram(NewForm(), tea.WithAltScreen())
    if _, err := p.Run(); err != nil {
        fmt.Printf("Error: %v", err)
    }
}
```

## Usage Example

```go
func main() {
    form := NewForm()

    p := tea.NewProgram(form, tea.WithAltScreen())
    if _, err := p.Run(); err != nil {
        fmt.Printf("Error: %v", err)
    }
}
```

## Customization Options

### Adding New Field Types

```go
// Phone field type
const (
    InputPhone InputType = iota + 1
)

// Add phone validation
func validatePhone(phone string) error {
    // Remove formatting characters
    cleaned := strings.ReplaceAll(strings.ReplaceAll(strings.ReplaceAll(phone, "(", ""), ")", ""), "-", "")

    if len(cleaned) != 10 {
        return fmt.Errorf("must be 10 digits")
    }

    for _, r := range cleaned {
        if r < '0' || r > '9' {
            return fmt.Errorf("must contain only numbers")
        }
    }

    return nil
}

// Add phone field to form
{
    Name:        "phone",
    Label:       "Phone",
    Placeholder: "(555) 123-4567",
    Required:    false,
    Type:        InputPhone,
    Validate:    validatePhone,
}
```

### Custom Styling

```go
// Custom color scheme
func createDarkTheme() FormStyles {
    return FormStyles{
        Label: lipgloss.NewStyle().
            Foreground(lipgloss.Color("228")). // Yellow
            Bold(true).
            MarginBottom(1),

        Input: lipgloss.NewStyle().
            Foreground(lipgloss.Color("255")).
            Background(lipgloss.Color("236")).
            Border(lipgloss.RoundedBorder()).
            BorderForeground(lipgloss.Color("62")). // Purple
            Padding(0, 1),

        Focused: lipgloss.NewStyle().
            Foreground(lipgloss.Color("255")).
            Background(lipgloss.Color("236")).
            Border(lipgloss.RoundedBorder()).
            BorderForeground(lipgloss.Color("205")). // Pink
            Padding(0, 1),

        Error: lipgloss.NewStyle().
            Foreground(lipgloss.Color("9")). // Red
            MarginLeft(2).
            MarginBottom(1),

        Button: lipgloss.NewStyle().
            Foreground(lipgloss.Color("0")).    // Black
            Background(lipgloss.Color("62")). // Purple
            Padding(0, 2).
            MarginRight(1),
    }
}
```

### Advanced Features

```go
// Auto-save functionality
type AutoSaveModel struct {
    Model
    autoSaveInterval time.Duration
    lastSave        time.Time
}

func (m AutoSaveModel) Init() tea.Cmd {
    return tea.Tick(m.autoSaveInterval, func(t time.Time) tea.Msg {
        return AutoSaveMsg{}
    })
}

func (m AutoSaveModel) Update(msg tea.Msg) (tea.Model, tea.Cmd) {
    switch msg.(type) {
    case tea.KeyMsg:
        // Update form as usual
        newModel, cmd := m.Model.Update(msg)
        m.Model = newModel
        return m, cmd

    case AutoSaveMsg:
        return m.autoSave()

    default:
        return m.Model.Update(msg)
    }
}

func (m AutoSaveModel) autoSave() tea.Cmd {
    values := make(map[string]string)
    for i, field := range m.fields {
        values[field.Name] = m.textInputs[i].Value()
    }

    // Save to file or API
    return tea.Printf("Auto-saved: %+v", values)
}
```

## Best Practices

1. **Always validate input**: Use both client-side and server-side validation
2. **Provide clear error messages**: Help users understand what went wrong
3. **Use consistent styling**: Apply the same visual design across all fields
4. **Implement proper focus management**: Ensure smooth keyboard navigation
5. **Handle edge cases**: Empty input, special characters, maximum lengths
6. **Provide visual feedback**: Use colors and indicators to show state
7. **Test thoroughly**: Include validation, navigation, and edge case testing