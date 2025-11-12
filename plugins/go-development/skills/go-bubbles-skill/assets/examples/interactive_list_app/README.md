# Interactive List App with Bubbles

A comprehensive example demonstrating advanced Bubbles component integration, featuring an interactive list with search, filtering, and sophisticated UI.

## Features

### Core Functionality
- **Interactive List**: Navigate through a collection of applications
- **Search & Filter**: Real-time text filtering with instant results
- **Multi-Component Integration**: Seamless switching between list and search input
- **Help System**: Contextual help with keyboard shortcuts
- **Visual Feedback**: Status indicators and progress information

### Advanced Features
- **Category Management**: Organize items by categories
- **Priority System**: Display priority summaries
- **Keyboard Navigation**: Vim-style and standard keyboard shortcuts
- **Responsive Design**: Adapts to different terminal sizes
- **Styling**: Beautiful Lip Gloss-based theming

### Component Showcase
- **List Component**: Advanced delegate customization
- **Text Input Component**: Search input with validation
- **Style Integration**: Consistent visual design across components
- **State Management**: Complex focus and selection handling

## Installation

```bash
go mod tidy
go run .
```

Or build and run:

```bash
go build -o interactive-list
./interactive-list
```

## Controls

### Navigation
- `↑/k` or `j/↓`: Move cursor up/down
- `g` or `Home`: Go to top of list
- `G` or `End`: Go to bottom of list
- `Enter`: Select current item
- `Tab`: Toggle between list and search input

### Search & Filtering
- `f`: Focus search input
- `/`: Toggle help mode
- `Escape`: Return to previous focus
- Type in search box to filter list items

### Application Features
- `c`: Show all categories
- `p`: Show priority summary
- `r`: Reset filter and return to top

### System
- `q` or `Ctrl+C`: Quit application

## Architecture

### Component Structure
```
Model
├── List Component
├── Text Input Component (Search)
├── State Management
│   ├── Focus tracking
│   ├── Item data
│   └── Filter state
└── Styling System
    ├── Lip Gloss styles
    └── Color themes
```

### Data Flow
1. **Initialization**: Create components and load data
2. **Message Handling**: Process keyboard events and component updates
3. **Filtering**: Apply search filter to data in real-time
4. **Rendering**: Combine components into final UI

### State Management Patterns
- **Focus Management**: Track which component has keyboard focus
- **Selection Tracking**: Monitor list item selection state
- **Filter State**: Maintain search filter and filtered data
- **Component Coordination**: Handle message passing between components

## Key Learnings

### Component Integration
```go
// Focus switching pattern
func (m Model) switchFocus() Model {
    if m.listFocus {
        m.list.Blur()
        m.searchInput.Focus()
        m.searchFocus = true
    } else {
        m.searchInput.Blur()
        m.list.Focus()
        m.listFocus = true
    }
    return m
}
```

### Real-time Filtering
```go
func (m Model) applyFilter(searchTerm string) {
    m.filtered = nil
    term = strings.ToLower(searchTerm)

    for _, item := range m.items {
        if strings.Contains(item.FilterValue(), term) {
            m.filtered = append(m.filtered, item)
        }
    }
    m.updateList()
}
```

### Component Styling
```go
// Consistent styling across components
func createAppStyles() AppStyles {
    return AppStyles{
        Title: lipgloss.NewStyle().
            Bold(true).
            Foreground(lipgloss.Color("62")),
        // ... other styles
    }
}
```

## Extending the Application

### Adding New Features
1. **New Item Types**: Extend the Item struct with additional fields
2. **Enhanced Search**: Implement fuzzy search with ranking
3. **Data Persistence**: Add save/load functionality
4. **Keyboard Shortcuts**: Create custom key bindings
5. **Export Features**: Implement data export capabilities

### Component Customization
1. **Custom Delegate**: Modify list appearance and behavior
2. **Input Validation**: Add search input validation
3. **Theme System**: Implement multiple color schemes
4. **Animation**: Add visual effects for interactions

### Performance Optimizations
1. **Lazy Loading**: Load data in chunks for large datasets
2. **Search Indexing**: Pre-build search index for faster filtering
3. **View Caching**: Cache rendered output for better performance
4. **Memory Management**: Limit data size to prevent memory leaks

## Best Practices Demonstrated

### Component Usage
- **Initialization**: Proper component setup with configuration
- **Message Handling**: Coordinated message passing between components
- **State Management**: Clear separation of concerns in state management
- **Styling**: Consistent visual design using Lip Gloss

### Performance
- **Efficient Filtering**: Optimized search algorithm for large datasets
- **Responsive Design**: Handle terminal resize events properly
- **Memory Usage**: Maintain reasonable memory footprint

### User Experience
- **Keyboard Navigation**: Full keyboard accessibility
- **Visual Feedback**: Clear indicators for user actions
- **Help System**: Comprehensive help with keyboard shortcuts
- **Error Handling**: Graceful error handling and recovery

This example serves as a comprehensive reference for building sophisticated applications with Bubbles components, demonstrating advanced patterns and best practices for creating interactive terminal user interfaces.