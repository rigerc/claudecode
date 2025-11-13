---
name: go-bubbletea-skill
description: Use when building terminal user interfaces (TUIs) with the BubbleTea framework in Go. Provides expertise in Model-View-Update pattern, component integration, Lip Gloss styling, performance optimization, and best practices for TUI development.
---

# Go BubbleTea TUI Development Expert

Expert assistance for building terminal user interfaces using the BubbleTea framework and Bubbles components in Go.

## When to Use This Skill

Use this skill when you need help with:

- Creating BubbleTea applications using the Model-View-Update pattern
- Implementing and configuring Bubbles components
- Styling TUI applications with Lip Gloss
- Component composition and state management
- Performance optimization and debugging
- Testing strategies for TUI applications
- Real-time dashboards and data visualization

## Quick Start

```go
type model struct{}

func (m model) Init() tea.Cmd { return nil }
func (m model) Update(msg tea.Msg) (tea.Model, tea.Cmd) {
    if msg.(tea.KeyMsg).String() == "q" { return m, tea.Quit }
    return m, nil
}
func (m model) View() string { return "Press q to quit" }

func main() { tea.NewProgram(model{}).Run() }
```

## Available Resources

See `references/` for comprehensive documentation:

- **component_examples.md**: Examples for all Bubbles components
- **styling_patterns.md**: Lip Gloss styling and theming
- **integration_patterns.md**: Component composition and architecture
- **performance_guide.md**: Optimization techniques and best practices
- **debugging_guide.md**: Debugging tools and troubleshooting
- **testing_patterns.md**: Testing strategies for TUI applications
