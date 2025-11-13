---
name: go-bubbles-skill
description: Use when working with the Bubbles component library for BubbleTea applications in Go. Provides expertise in implementing textinput, textarea, spinner, progress, table, list, paginator, timer, viewport, filepicker, and key bindings with Lip Gloss styling.
---

# Go Bubbles Component Library Expert

Expert assistance for the Bubbles component library, providing production-ready UI components for BubbleTea terminal applications.

## When to Use This Skill

Use this skill when you need help with:

- Implementing and configuring Bubbles components
- Styling components with Lip Gloss
- Integrating components into BubbleTea applications
- Troubleshooting component behavior and performance
- Creating custom component extensions
- Component composition and state management

## Quick Start

```go
import (
    "github.com/charmbracelet/bubbles/textinput"
    tea "github.com/charmbracelet/bubbletea"
)

func (m Model) Init() tea.Cmd {
    m.textInput = textinput.New()
    m.textInput.Placeholder = "Enter text..."
    m.textInput.Focus()
    return textinput.Blink
}

func (m Model) Update(msg tea.Msg) (tea.Model, tea.Cmd) {
    var cmd tea.Cmd
    m.textInput, cmd = m.textInput.Update(msg)
    return m, cmd
}
```

## Available Resources

See `references/` for comprehensive documentation:

- **component_api.md**: Complete API documentation for all components
- **styling_guide.md**: Lip Gloss integration and theming patterns
- **integration_patterns.md**: Component composition and state management
- **troubleshooting.md**: Common issues, debugging, and performance optimization
