# BubbleTea Basic Application Template

A minimal but complete BubbleTea application template that demonstrates core concepts and best practices.

## Features

- **Model-View-Update Architecture**: Clean separation of concerns
- **Keyboard Navigation**: Vim-style and arrow key support
- **Styling with Lip Gloss**: Beautiful, consistent styling
- **Error Handling**: Graceful error management
- **Terminal Compatibility**: Works across different terminals

## Quick Start

1. **Install Dependencies**:
   ```bash
   go mod tidy
   ```

2. **Run the Application**:
   ```bash
   go run .
   ```

3. **Build Binary**:
   ```bash
   go build -o basic-app
   ./basic-app
   ```

## Key Controls

| Control | Action |
|---------|--------|
| ↑ / k   | Move cursor up |
| ↓ / j   | Move cursor down |
| Enter   | Select current item |
| r       | Reset selection |
| q       | Quit application |
| Ctrl+C  | Force quit |

## Code Structure

```
.
├── main.go          # Main application logic
├── go.mod           # Go module definition
└── README.md        # This file
```

### Key Concepts Demonstrated

1. **Model Structure**:
   ```go
   type Model struct {
       choices  []string
       cursor   int
       selected int
       quiting  bool
   }
   ```

2. **Initialization**:
   ```go
   func initialModel() Model {
       return Model{ /* initial state */ }
   }
   ```

3. **Message Handling**:
   ```go
   func (m Model) Update(msg tea.Msg) (tea.Model, tea.Cmd) {
       switch msg := msg.(type) {
       case tea.KeyMsg:
           // Handle keyboard input
       }
       return m, nil
   }
   ```

4. **Rendering**:
   ```go
   func (m Model) View() string {
       // Build and return UI string
   }
   ```

5. **Styling**:
   ```go
   var titleStyle = lipgloss.NewStyle().
       Bold(true).
       Foreground(lipgloss.Color("62"))
   ```

## Extending the Template

### Adding New Features

1. **Add New State**:
   ```go
   type Model struct {
       // Existing fields...
       currentPage string
       loading     bool
       data        interface{}
   }
   ```

2. **Handle New Messages**:
   ```go
   type dataLoadedMsg struct {
       data interface{}
   }

   func (m Model) Update(msg tea.Msg) (tea.Model, tea.Cmd) {
       switch msg := msg.(type) {
       case dataLoadedMsg:
           m.data = msg.data
           m.loading = false
       }
       return m, nil
   }
   ```

3. **Create Commands**:
   ```go
   func loadData() tea.Cmd {
       return func() tea.Msg {
           // Load data asynchronously
           return dataLoadedMsg{data: result}
       }
   }
   ```

### Adding Components

1. **Import Bubbles**:
   ```go
   import "github.com/charmbracelet/bubbles/textinput"
   ```

2. **Add to Model**:
   ```go
   type Model struct {
       textInput textinput.Model
       // Other fields...
   }
   ```

3. **Initialize**:
   ```go
   func initialModel() Model {
       ti := textinput.New()
       ti.Placeholder = "Enter text..."
       ti.Focus()

       return Model{
           textInput: ti,
       }
   }
   ```

4. **Update Component**:
   ```go
   func (m Model) Update(msg tea.Msg) (tea.Model, tea.Cmd) {
       var cmd tea.Cmd
       m.textInput, cmd = m.textInput.Update(msg)
       return m, cmd
   }
   ```

## Best Practices

1. **Immutable Updates**: Always return new models rather than modifying in-place
2. **Error Handling**: Handle errors gracefully and provide user feedback
3. **Performance**: Use efficient string building and avoid unnecessary allocations
4. **Accessibility**: Use clear labels and provide keyboard navigation
5. **Testing**: Test models and components separately

## Advanced Topics

### Multiple Components

```go
type Model struct {
    textInput textinput.Model
    list      list.Model
    active    int // Track which component is focused
}
```

### Custom Messages

```go
type customMsg struct {
    data string
}

func sendCustomData(data string) tea.Cmd {
    return func() tea.Msg {
        return customMsg{data: data}
    }
}
```

### Async Operations

```go
func loadData() tea.Cmd {
    return func() tea.Msg {
        // Simulate network request
        time.Sleep(1 * time.Second)
        return dataLoadedMsg{items: result}
    }
}
```

## Deployment

### Cross-Platform Build

```bash
# Linux
GOOS=linux GOARCH=amd64 go build -o basic-app-linux

# macOS
GOOS=darwin GOARCH=amd64 go build -o basic-app-macos

# Windows
GOOS=windows GOARCH=amd64 go build -o basic-app.exe
```

### Distribution

Consider these distribution methods:

1. **GitHub Releases**: Upload binaries for different platforms
2. **Homebrew**: Create a formula for macOS
3. **Docker**: Containerize the application
4. **Snap**: Distribute as a snap package

## Resources

- [BubbleTea Documentation](https://github.com/charmbracelet/bubbletea)
- [Lip Gloss Styling](https://github.com/charmbracelet/lipgloss)
- [Bubbles Components](https://github.com/charmbracelet/bubbles)
- [Charm CLI Tools](https://charm.sh/)

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This template is provided as-is for educational and development purposes.