package main

import (
    "fmt"
    "strings"
    tea "github.com/charmbracelet/bubbletea"
    "github.com/charmbracelet/bubbles/list"
    "github.com/charmbracelet/bubbles/textinput"
    "github.com/charmbracelet/lipgloss"
)

// Application item
type Item struct {
    id       int
    title    string
    category string
    tags     []string
    priority string
}

func (i Item) Title() string       { return i.title }
func (i Item) Description() string { return fmt.Sprintf("%s • %s", i.category, strings.Join(i.tags, ", ")) }
func (i Item) FilterValue() string {
    return strings.ToLower(i.title + " " + i.category + " " + strings.Join(i.tags, " "))
}

// Model
type Model struct {
    list         list.Model
    searchInput  textinput.Model
    items        []Item
    filtered     []Item
    categories   map[string][]Item
    showingHelp  bool
    listFocus    bool
    searchFocus  bool
    styles       AppStyles
}

type AppStyles struct {
    Title       lipgloss.Style
    Subtitle    lipgloss.Style
    Status      lipgloss.Style
    Help        lipgloss.Style
    Border      lipgloss.Style
}

// Initialize model
func initialModel() Model {
    // Sample data
    items := []Item{
        {id: 1, title: "Task Manager", category: "Productivity", tags: []string{"todo", "tasks"}, priority: "High"},
        {id: 2, title: "Note Taking App", category: "Productivity", tags: []string{"notes", "writing"}, priority: "Medium"},
        {id:3, title: "Weather Dashboard", category: "Utilities", tags: []string{"weather", "dashboard"}, priority: "Low"},
        {id:4, title: "Code Editor", category: "Development", tags: []string{"code", "editor", "IDE"}, priority: "High"},
        {id:5, title: "File Explorer", category: "Development", tags: []string{"files", "manager"}, priority: "Medium"},
        {id:6, title: "Music Player", category: "Entertainment", tags: []string{"music", "player"}, priority: "Low"},
        {id:7, title: "Video Player", category: "Entertainment", tags: []string{"video", "player", "media"}, priority: "Low"},
        {id:8, title: "System Monitor", category: "Utilities", tags: []string{"system", "monitor"}, priority: "High"},
    }

    // Create delegate
    delegate := list.NewDefaultDelegate()
    delegate.ShowDescription = true
    delegate.SetSpacing(1)
    delegate.UpdateFunc = func(msg tea.Msg, m list.Model) tea.Cmd {
        switch msg.(type) {
        case tea.KeyMsg:
            switch msg.String() {
            case "x":
                // Mark as completed (placeholder functionality)
                return nil
            case "d":
                // Delete item (placeholder functionality)
                return nil
            }
        }
        return nil
    }
    delegate.ShortHelpFunc = func() []key.Binding {
        return []key.Binding{
            key.NewBinding(key.WithKeys("x"), key.WithHelp("x", "complete")),
            key.NewBinding(key.WithKeys("d"), key.WithHelp("d", "delete")),
        }
    }

    // Create list
    l := list.New(itemsToItems(items), delegate, 0, 0)
    l.Title = "Application Library"
    l.SetFilteringEnabled(true)
    l.SetShowStatusBar(true)
    l.SetShowPagination(true)
    l.SetShowHelp(true)

    // Create search input
    search := textinput.New()
    search.Placeholder = "Search apps..."
    search.Width = 30
    search.CharLimit = 50

    // Create styles
    styles := createAppStyles()

    // Build categories map
    categories := make(map[string][]Item)
    for _, item := range items {
        categories[item.category] = append(categories[item.category], item)
    }

    return Model{
        list:        l,
        searchInput: search,
        items:       items,
        filtered:    items,
        categories: categories,
        listFocus:   true,
        styles:      styles,
    }
}

// Update method
func (m Model) Update(msg tea.Msg) (tea.Model, tea.Cmd) {
    var cmd tea.Cmd

    switch msg := msg.(type) {
    case tea.KeyMsg:
        switch msg.String() {
        case "ctrl+c", "q":
            return m, tea.Quit

        case "/":
            m.showHelp = !m.showHelp
            if !m.showHelp {
                m.listFocus = true
                m.searchFocus = false
                m.searchInput.Blur()
            }

        case "f":
            if m.listFocus {
                m.listFocus = false
                m.searchFocus = true
                m.searchInput.Focus()
            }

        case "escape":
            if m.searchFocus {
                m.listFocus = true
                m.searchFocus = false
                m.searchInput.Blur()
                m.searchInput.SetValue("")
                m.list.ResetFilter()
            } else if m.listFocus {
                m.list.Blur()
                m.showHelp = true
                m.searchFocus = true
                m.searchInput.Focus()
            }

        case "tab":
            // Toggle focus between list and search
            if m.listFocus {
                m.listFocus = false
                m.searchFocus = true
                m.searchInput.Focus()
            } else {
                m.listFocus = true
                m.searchFocus = false
                m.searchInput.Blur()
            }

        case "c":
            // Show categories
            return m, tea.Printf("Categories: %v", m.getCategoryList())

        case "p":
            // Show priority summary
            return m, tea.Printf("Priority Summary: %s", m.getPrioritySummary())

        case "r":
            // Reset filter and focus
            m.list.SetFilter("")
            m.list.SetCursor(0)
            m.searchInput.SetValue("")
            m.filtered = m.items
            m.updateList()
            return m, nil
        }

    case tea.WindowSizeMsg:
        // Handle window resize
        if !m.showHelp {
            m.list.SetWidth(msg.Width)
            m.list.SetHeight(msg.Height - 6) // Account for search and help
        }

    // Update based on focus
    if m.searchFocus {
        m.searchInput, cmd = m.searchInput.Update(msg)

        // Auto-apply filter
        if msg, ok := msg.(tea.KeyMsg); ok && msg.Type == tea.KeyRunes {
            m.applyFilter(m.searchInput.Value())
        }
    } else if m.listFocus {
        // Handle item selection
        oldSelection := m.list.SelectedItem()
        m.list, cmd = m.list.Update(msg)

        newSelection := m.list.SelectedItem()
        if oldSelection != newSelection && newSelection != nil {
            // Item selection changed
            item := newSelection.(Item)
            cmd = tea.Printf("Selected: %s (%s)", item.title, item.category)
        }
    }

    return m, cmd
}

// View method
func (m Model) View() string {
    if m.showHelp {
        return m.renderHelp()
    }

    var content strings.Builder

    // Header
    content.WriteString(m.styles.Border.Render(
        m.styles.Title.Render("🚀 Interactive List Demo") + "\n" +
        m.styles.Subtitle.Render("Navigate, search, and interact with applications") + "\n\n" +
        m.renderStats() + "\n\n" +
        m.renderSearch() + "\n\n" +
        m.list.View(),
    ))

    return content.String()
}

// Render statistics
func (m Model) renderStats() string {
    totalItems := len(m.items)
    filteredItems := len(m.filtered)
    categories := len(m.categories)

    stats := fmt.Sprintf("📊 %d apps | 🔍 %d categories | 📝 %d visible",
        totalItems, categories, filteredItems)

    return m.styles.Status.Render(stats)
}

// Render search input
func (m Model) renderSearch() string {
    style := m.styles.Border
    if m.searchFocus {
        style = style.BorderForeground(lipgloss.Color("228")) // Yellow
    }

    return style.Render("Search: " + m.searchInput.View())
}

// Render help
func (m Model) renderHelp() string {
    helpContent := `🎯 Interactive List Help

Navigation:
  ↑/k or j/Down    • Move cursor up/down
  g or Home        • Go to top
  G or End         • Go to bottom
  Enter           • Select current item
  Tab             • Toggle between list and search
  f               • Focus search input
  /               • Toggle help

Search:
  /               • Toggle search mode
  Type to search   • Type to filter list items

Categories & Priority:
  c               • Show all categories
  p               • Show priority summary
  r               • Reset filter

List Actions:
  x               • Mark as completed (placeholder)
  d               • Delete item (placeholder)

Other:
  q or Ctrl+C     • Quit application`

    return m.styles.Border.Render(
        m.styles.Title.Render("Help") + "\n\n" +
        m.styles.Help.Render(helpContent),
    )
}

// Helper methods
func itemsToItems(items []Item) []list.Item {
    var result []list.Item
    for _, item := range items {
        result = append(result, item)
    }
    return result
}

func (m Model) applyFilter(searchTerm string) {
    if searchTerm == "" {
        m.filtered = m.items
        m.list.ResetFilter()
        return
    }

    m.filtered = nil
    term = strings.ToLower(searchTerm)

    for _, item := range m.items {
        if strings.Contains(item.FilterValue(), term) {
            m.filtered = append(m.filtered, item)
        }
    }

    m.updateList()
}

func (m Model) updateList() {
    m.list.SetItems(itemsToItems(m.filtered))
    m.list.SetCursor(0)
}

func (m Model) getPrioritySummary() string {
    highCount := 0
    mediumCount := 0
    lowCount := 0

    for _, item := range m.filtered {
        switch item.priority {
        case "High":
            highCount++
        case "Medium":
            mediumCount++
        case "Low":
            lowCount++
        }
    }

    return fmt.Sprintf("High: %d | Medium: %d | Low: %d", highCount, mediumCount, lowCount)
}

func (m Model) getCategoryList() string {
    categories := make([]string, 0, len(m.categories))
    for category := range m.categories {
        count := len(m.categories[category])
        categories = append(categories, fmt.Sprintf("%s (%d)", category, count))
    }

    return strings.Join(categories, ", ")
}

// Create styles
func createAppStyles() AppStyles {
    return AppStyles{
        Title: lipgloss.NewStyle().
            Bold(true).
            Foreground(lipgloss.Color("62")). // Purple
            MarginBottom(1),

        Subtitle: lipgloss.NewStyle().
            Foreground(lipgloss.Color("240")). // Gray
            MarginBottom(1).

        Status: lipgloss.NewStyle().
            Foreground(lipgloss.Color("46")). // Green
            MarginBottom(1),

        Help: lipgloss.NewStyle().
            Foreground(lipgloss.Color("255")).
            Background(lipgloss.Color("62")). // Purple
            Padding(2, 4),

        Border: lipgloss.NewStyle().
            Border(lipgloss.RoundedBorder()).
            BorderForeground(lipgloss.Color("62")). // Purple
            Padding(1, 2),
    }
}

// Main function
func main() {
    p := tea.NewProgram(
        initialModel(),
        tea.WithAltScreen(),
        tea.WithMouseCellMotion(),
    )

    if _, err := p.Run(); err != nil {
        fmt.Printf("Error: %v", err)
    }
}