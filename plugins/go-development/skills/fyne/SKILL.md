---
name: fyne
version: "1.0.0"
description: Use when developing cross-platform GUI applications in Go using the Fyne toolkit for desktop, mobile, and web applications.
author: Claude Code
keywords:
  - fyne
  - gui
  - cross-platform
  - desktop applications
  - mobile apps
  - material design
---

# Fyne GUI Toolkit Expert

Use when creating cross-platform graphical user interface applications in Go using the Fyne toolkit.

## When to Use

- Building desktop applications for Windows, macOS, Linux
- Creating mobile apps for Android and iOS
- Developing cross-platform GUI tools and utilities
- Implementing data binding and reactive UI patterns
- Creating responsive layouts with Material Design
- Building custom themes and widget components

## Core Expertise

- Cross-platform application development (desktop, mobile, web)
- Material Design widget library and layouts
- Event handling and user interaction patterns
- Data binding for reactive UI updates
- Custom theming and styling
- Application packaging and deployment

## Quick Reference

**Key Packages**: `app`, `widget`, `container`, `theme`, `data/binding`
**Platforms**: Windows, macOS, Linux, Android, iOS, Web (WASM)
**Install**: `go get fyne.io/fyne/v2 && go install fyne.io/tools/cmd/fyne@latest`

## Quick Start

1. **Install**: `go get fyne.io/fyne/v2 && go install fyne.io/tools/cmd/fyne@latest`
2. **Basic App**: `a := app.New(); w := a.NewWindow("Title"); w.SetContent(widget.NewLabel("Hello")); w.ShowAndRun()`
3. **Layout**: Use `container.NewVBox()`, `NewHBox()`, `NewBorder()` for widget arrangement
4. **Widgets**: Import `widget` package for buttons, labels, entries, etc.
5. **Build**: `go build -o myapp` for current platform, `fyne-cross` for cross-platform

## Common Patterns

- **Application Setup**: `app.New()` → `NewWindow()` → `SetContent()` → `ShowAndRun()`
- **Layout Management**: Use container widgets (VBox, HBox, Border, Grid)
- **Event Handling**: Pass callback functions to widget constructors
- **Data Binding**: Use `binding` package for reactive UI updates
- **Theming**: Implement `fyne.Theme` interface for custom styling
- **Testing**: Use `fyne.io/fyne/v2/test` package for unit tests

## References

- **[Quick Examples](references/quick-examples.md)**: Ready-to-use code snippets for common GUI patterns
- **[Widget Reference](references/widget-reference.md)**: Complete widget documentation with properties and methods
- **[Deployment Guide](references/deployment-guide.md)**: Cross-platform building for desktop, mobile, and web deployment