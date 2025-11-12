# Data Table Template

## Description
A comprehensive table template with sorting, filtering, selection, and pagination features for displaying and interacting with tabular data.

## Features
- Dynamic column sorting (ascending/descending)
- Row selection with visual indicators
- Search and filtering capabilities
- Pagination for large datasets
- Custom cell styling and formatting
- Keyboard navigation (arrows, enter, escape)
- Export functionality
- Responsive design for different terminal sizes

## Implementation

```go
package main

import (
    "fmt"
    "sort"
    "strings"
    tea "github.com/charmbracelet/bubbletea"
    "github.com/charmbracelet/bubbles/table"
    "github.com/charmbracelet/bubbles/textinput"
    "github.com/charmbracelet/lipgloss"
)

// Data row structure
type DataRow struct {
    ID       int
    Name     string
    Email    string
    Role     string
    Status   string
    JoinDate string
    Active   bool
}

// Table model
type Model struct {
    table       table.Model
    data        []DataRow
    filtered    []DataRow
    searchInput textinput.Model
    sortColumn  int
    sortAscending bool
    selected    map[int]bool
    page        int
    pageSize    int
    totalPages  int
    showSearch  bool
    searchFocus bool
    styles      TableStyles
}

type TableStyles struct {
    Header     lipgloss.Style
    Cell       lipgloss.Style
    Selected   lipgloss.Style
    Status     lipgloss.Style
    Active     lipgloss.Style
    Inactive   lipgloss.Style
    Search     lipgloss.Style
    Pagination lipgloss.Style
    Border     lipgloss.Style
}

// Create new table model
func NewTableModel(data []DataRow) Model {
    // Define columns
    columns := []table.Column{
        {Title: "ID", Width: 6},
        {Title: "Name", Width: 20},
        {Title: "Email", Width: 25},
        {Title: "Role", Width: 15},
        {Title: "Status", Width: 12},
        {Title: "Join Date", Width: 12},
    }

    // Create table
    t := table.New(
        table.WithColumns(columns),
        table.WithRows([]table.Row{}),
        table.WithFocused(true),
        table.WithHeight(15),
    )

    // Create search input
    search := textinput.New()
    search.Placeholder = "Search..."
    search.Width = 30
    search.CharLimit = 50

    // Initialize styles
    styles := createTableStyles()

    return Model{
        table:       t,
        data:        data,
        filtered:    data,
        searchInput: search,
        sortColumn:  0,
        sortAscending: true,
        selected:    make(map[int]bool),
        page:        0,
        pageSize:    20,
        totalPages:  (len(data) + 19) / 20,
        showSearch:  false,
        searchFocus: false,
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

        case "f":
            m.showSearch = !m.showSearch
            if m.showSearch {
                m.searchInput.Focus()
                m.searchFocus = true
            } else {
                m.searchInput.Blur()
                m.searchFocus = false
            }

        case "escape":
            if m.showSearch {
                m.showSearch = false
                m.searchInput.Blur()
                m.searchFocus = false
                m.searchInput.SetValue("")
                m.applyFilter("")
            } else {
                // Clear selection
                m.selected = make(map[int]bool)
                m.updateTable()
            }

        case "s":
            if m.showSearch && m.searchFocus {
                return m, tea.Printf("Searching for: %s", m.searchInput.Value())
            } else {
                m.sortData()
            }

        case "r":
            m.resetSortAndFilter()

        case "enter":
            if m.showSearch && m.searchFocus {
                m.applyFilter(m.searchInput.Value())
            } else {
                m.toggleSelection()
            }

        case "space":
            m.toggleSelection()

        case "e":
            return m, m.exportSelection()

        case "a":
            m.selectAll()

        case "d":
            m.deselectAll()

        case "j", "down":
            if !m.showSearch || !m.searchFocus {
                m.moveCursor(1)
            }

        case "k", "up":
            if !m.showSearch || !m.searchFocus {
                m.moveCursor(-1)
            }

        case "ctrl+right":
            m.nextPage()

        case "ctrl+left":
            m.previousPage()

        case "ctrl+home":
            m.goToFirstPage()

        case "ctrl+end":
            m.goToLastPage()
        }

    case tea.WindowSizeMsg:
        m.resizeTable(msg.Width, msg.Height)
    }

    // Update search input
    if m.showSearch && m.searchFocus {
        m.searchInput, cmd = m.searchInput.Update(msg)
    }

    // Update table
    if !m.searchFocus {
        m.table, cmd = m.table.Update(msg)
    }

    return m, cmd
}

// View method
func (m Model) View() string {
    var content strings.Builder

    // Header
    content.WriteString(m.styles.Border.Render(
        m.styles.Header.Render("📊 Data Table") + "\n\n" +
        m.renderControls() + "\n\n" +
        m.renderSearch() + "\n\n" +
        m.renderTable() + "\n\n" +
        m.renderPagination(),
    ))

    return content.String()
}

// Render controls
func (m Model) renderControls() string {
    var controls strings.Builder

    // Search button
    searchBtn := "Search [f]"
    if m.showSearch {
        searchBtn = "Hide [f]"
    }

    // Sort button
    sortBtn := "Sort [s]"

    // Reset button
    resetBtn := "Reset [r]"

    // Selection buttons
    selectAllBtn := "Select All [a]"
    deselectAllBtn := "Deselect [d]"
    exportBtn := "Export [e]"

    controls.WriteString(searchBtn + " • " + sortBtn + " • " + resetBtn + " • ")
    controls.WriteString(selectAllBtn + " • " + deselectAllBtn + " • " + exportBtn)

    // Status information
    selectedCount := len(m.selected)
    totalCount := len(m.filtered)

    status := fmt.Sprintf("Showing %d of %d rows", totalCount, totalCount)
    if selectedCount > 0 {
        status += fmt.Sprintf(" • %d selected", selectedCount)
    }

    controls.WriteString("\n" + m.styles.Status.Render(status))

    return controls.String()
}

// Render search input
func (m Model) renderSearch() string {
    if !m.showSearch {
        return ""
    }

    return m.styles.Search.Render("Search: " + m.searchInput.View())
}

// Render table
func (m Model) renderTable() string {
    if len(m.filtered) == 0 {
        return "No data to display"
    }

    return m.table.View()
}

// Render pagination
func (m Model) renderPagination() string {
    if m.totalPages <= 1 {
        return ""
    }

    var pagination strings.Builder

    // Current page info
    pagination.WriteString(fmt.Sprintf("Page %d of %d", m.page+1, m.totalPages))

    // Navigation buttons
    navButtons := []string{}
    if m.page > 0 {
        navButtons = append(navButtons, "First [ctrl+home]")
        navButtons = append(navButtons, "Prev [ctrl+left]")
    }
    if m.page < m.totalPages-1 {
        navButtons = append(navButtons, "Next [ctrl+right]")
        navButtons = append(navButtons, "Last [ctrl+end]")
    }

    if len(navButtons) > 0 {
        pagination.WriteString(" • " + strings.Join(navButtons, " • "))
    }

    return m.styles.Pagination.Render(pagination.String())
}

// Helper methods
func (m Model) resizeTable(width, height int) {
    // Account for header and other UI elements
    availableHeight := height - 15 // Reserve space for header, search, pagination
    if availableHeight < 5 {
        availableHeight = 5
    }

    m.table.SetWidth(width - 4) // Account for border
    m.table.SetHeight(availableHeight)
}

func (m Model) moveCursor(direction int) {
    current := m.table.Cursor()
    newCursor := current + direction

    if newCursor >= 0 && newCursor < len(m.filtered) {
        m.table.SetCursor(newCursor)
    }
}

func (m Model) toggleSelection() {
    cursor := m.table.Cursor()
    if cursor >= 0 && cursor < len(m.filtered) {
        if m.selected[cursor] {
            delete(m.selected, cursor)
        } else {
            m.selected[cursor] = true
        }
        m.updateTable()
    }
}

func (m Model) selectAll() {
    m.selected = make(map[int]bool)
    for i := 0; i < len(m.filtered); i++ {
        m.selected[i] = true
    }
    m.updateTable()
}

func (m Model) deselectAll() {
    m.selected = make(map[int]bool)
    m.updateTable()
}

func (m Model) applyFilter(searchTerm string) {
    if searchTerm == "" {
        m.filtered = m.data
    } else {
        m.filtered = nil
        searchTerm = strings.ToLower(searchTerm)

        for _, row := range m.data {
            if m.matchesSearch(row, searchTerm) {
                m.filtered = append(m.filtered, row)
            }
        }
    }

    m.page = 0
    m.totalPages = (len(m.filtered) + m.pageSize - 1) / m.pageSize
    m.updateTable()
}

func (m Model) matchesSearch(row DataRow, searchTerm string) bool {
    searchFields := []string{
        fmt.Sprintf("%d", row.ID),
        strings.ToLower(row.Name),
        strings.ToLower(row.Email),
        strings.ToLower(row.Role),
        strings.ToLower(row.Status),
        strings.ToLower(row.JoinDate),
    }

    for _, field := range searchFields {
        if strings.Contains(field, searchTerm) {
            return true
        }
    }

    return false
}

func (m Model) sortData() {
    // Toggle sort direction if sorting same column
    if m.lastSortColumn == m.sortColumn {
        m.sortAscending = !m.sortAscending
    } else {
        m.sortAscending = true
        m.lastSortColumn = m.sortColumn
    }

    sort.Slice(m.filtered, func(i, j int) bool {
        return m.compareRows(i, j)
    })

    m.updateTable()
}

func (m Model) compareRows(i, j int) bool {
    rowI := m.filtered[i]
    rowJ := m.filtered[j]

    var valueI, valueJ string

    switch m.sortColumn {
    case 0: // ID
        valueI = fmt.Sprintf("%010d", rowI.ID)
        valueJ = fmt.Sprintf("%010d", rowJ.ID)
    case 1: // Name
        valueI = rowI.Name
        valueJ = rowJ.Name
    case 2: // Email
        valueI = rowI.Email
        valueJ = rowJ.Email
    case 3: // Role
        valueI = rowI.Role
        valueJ = rowJ.Role
    case 4: // Status
        valueI = rowI.Status
        valueJ = rowJ.Status
    case 5: // Join Date
        valueI = rowI.JoinDate
        valueJ = rowJ.JoinDate
    }

    if m.sortAscending {
        return valueI < valueJ
    }
    return valueI > valueJ
}

func (m Model) updateTable() {
    // Calculate page boundaries
    start := m.page * m.pageSize
    end := start + m.pageSize
    if end > len(m.filtered) {
        end = len(m.filtered)
    }

    // Convert data to table rows
    var rows []table.Row
    for i := start; i < end; i++ {
        if i < len(m.filtered) {
            rows = append(rows, m.dataRowToTableRow(m.filtered[i], i))
        }
    }

    m.table.SetRows(rows)
    m.table.SetCursor(0) // Reset cursor when page changes
}

func (m Model) dataRowToTableRow(row DataRow, index int) table.Row {
    rowStyle := m.styles.Cell
    if m.selected[index] {
        rowStyle = m.styles.Selected
    }

    statusStyle := rowStyle
    switch strings.ToLower(row.Status) {
    case "active":
        statusStyle = m.styles.Active
    case "inactive":
        statusStyle = m.styles.Inactive
    }

    return table.Row{
        fmt.Sprintf("%d", row.ID),
        row.Name,
        row.Email,
        row.Role,
        statusStyle.Render(row.Status),
        row.JoinDate,
    }
}

func (m Model) resetSortAndFilter() {
    m.sortColumn = 0
    m.sortAscending = true
    m.filtered = m.data
    m.page = 0
    m.totalPages = (len(m.data) + m.pageSize - 1) / m.pageSize
    m.selected = make(map[int]bool)
    m.searchInput.SetValue("")
    m.updateTable()
}

func (m Model) nextPage() {
    if m.page < m.totalPages-1 {
        m.page++
        m.updateTable()
    }
}

func (m Model) previousPage() {
    if m.page > 0 {
        m.page--
        m.updateTable()
    }
}

func (m Model) goToFirstPage() {
    m.page = 0
    m.updateTable()
}

func (m Model) goToLastPage() {
    m.page = m.totalPages - 1
    m.updateTable()
}

func (m Model) exportSelection() tea.Cmd {
    var selectedData []DataRow
    for index := range m.selected {
        if index < len(m.filtered) {
            selectedData = append(selectedData, m.filtered[index])
        }
    }

    if len(selectedData) == 0 {
        return tea.Printf("No rows selected for export")
    }

    // Format as CSV
    var csv strings.Builder
    csv.WriteString("ID,Name,Email,Role,Status,JoinDate,Active\n")
    for _, row := range selectedData {
        csv.WriteString(fmt.Sprintf("%d,%s,%s,%s,%s,%s,%t\n",
            row.ID, row.Name, row.Email, row.Role, row.Status, row.JoinDate, row.Active))
    }

    return tea.Printf("Exported %d rows:\n%s", len(selectedData), csv.String())
}

func createTableStyles() TableStyles {
    return TableStyles{
        Header: lipgloss.NewStyle().
            Bold(true).
            Foreground(lipgloss.Color("228")). // Yellow
            Background(lipgloss.Color("62")). // Purple
            Padding(0, 1).
            Align(lipgloss.Center),

        Cell: lipgloss.NewStyle().
            Foreground(lipgloss.Color("255")).
            Background(lipgloss.Color("237")). // Dark gray
            Padding(0, 1),

        Selected: lipgloss.NewStyle().
            Foreground(lipgloss.Color("0")).    // Black
            Background(lipgloss.Color("205")). // Pink
            Bold(true),

        Status: lipgloss.NewStyle().
            Padding(0, 1).

        Active: lipgloss.NewStyle().
            Foreground(lipgloss.Color("46")). // Green
            Bold(true),

        Inactive: lipgloss.NewStyle().
            Foreground(lipgloss.Color("240")). // Gray
            Italic(true),

        Search: lipgloss.NewStyle().
            Foreground(lipgloss.Color("228")). // Yellow
            MarginBottom(1),

        Pagination: lipgloss.NewStyle().
            Foreground(lipgloss.Color("62")). // Purple
            Bold(true),

        Border: lipgloss.NewStyle().
            Border(lipgloss.RoundedBorder()).
            BorderForeground(lipgloss.Color("62")), // Purple
            Padding(1, 2),
    }
}

// Sample data generation
func generateSampleData() []DataRow {
    return []DataRow{
        {1, "Alice Johnson", "alice@example.com", "Admin", "Active", "2023-01-15", true},
        {2, "Bob Smith", "bob@example.com", "User", "Active", "2023-02-20", true},
        {3, "Charlie Brown", "charlie@example.com", "User", "Inactive", "2023-03-10", false},
        {4, "Diana Prince", "diana@example.com", "Manager", "Active", "2023-01-25", true},
        {5, "Eve Wilson", "eve@example.com", "User", "Active", "2023-04-05", true},
        {6, "Frank Miller", "frank@example.com", "User", "Inactive", "2023-02-15", false},
        {7, "Grace Lee", "grace@example.com", "Admin", "Active", "2023-03-20", true},
        {8, "Henry Taylor", "henry@example.com", "Manager", "Active", "2023-04-10", true},
        {9, "Ivy Chen", "ivy@example.com", "User", "Active", "2023-01-30", true},
        {10, "Jack Davis", "jack@example.com", "User", "Inactive", "2023-05-15", false},
    }
}

// Main function
func main() {
    data := generateSampleData()
    model := NewTableModel(data)

    p := tea.NewProgram(model, tea.WithAltScreen())
    if _, err := p.Run(); err != nil {
        fmt.Printf("Error: %v", err)
    }
}
```

## Usage Example

```go
func main() {
    // Load data from database or API
    data, err := loadUserData()
    if err != nil {
        log.Fatal(err)
    }

    model := NewTableModel(data)

    p := tea.NewProgram(model, tea.WithAltScreen())
    if _, err := p.Run(); err != nil {
        fmt.Printf("Error: %v", err)
    }
}

func loadUserData() ([]DataRow, error) {
    // Simulate database query
    return generateSampleData(), nil
}
```

## Customization Options

### Dynamic Column Configuration

```go
// Configure columns based on data type
func configureColumns(dataType string) []table.Column {
    switch dataType {
    case "users":
        return []table.Column{
            {Title: "ID", Width: 8},
            {Title: "Name", Width: 20},
            {Title: "Email", Width: 30},
            {Title: "Role", Width: 15},
            {Title: "Status", Width: 12},
            {Title: "Last Login", Width: 15},
        }
    case "products":
        return []table.Column{
            {Title: "SKU", Width: 12},
            {Title: "Name", Width: 25},
            {Title: "Price", Width: 10},
            {Title: "Stock", Width: 8},
            {Title: "Category", Width: 15},
        }
    default:
        return []table.Column{
            {Title: "ID", Width: 10},
            {Title: "Value", Width: 30},
        }
    }
}
```

### Custom Cell Formatting

```go
func (m Model) dataRowToTableRow(row DataRow, index int) table.Row {
    // Custom cell styling based on data values
    idStyle := m.styles.Cell
    nameStyle := m.styles.Cell
    if row.Active {
        nameStyle = nameStyle.Bold(true)
    }

    priceStyle := m.styles.Cell
    if row.Price > 1000 {
        priceStyle = priceStyle.Foreground(lipgloss.Color("46")) // Green for high value
    }

    return table.Row{
        idStyle.Render(fmt.Sprintf("%d", row.ID)),
        nameStyle.Render(row.Name),
        priceStyle.Render(fmt.Sprintf("$%.2f", row.Price)),
    }
}
```

### Advanced Filtering

```go
type FilterCriteria struct {
    Role    string
    Status  string
    DateRange struct {
        Start time.Time
        End   time.Time
    }
}

func (m Model) applyAdvancedFilter(filter FilterCriteria) {
    m.filtered = nil

    for _, row := range m.data {
        if m.matchesAdvancedFilter(row, filter) {
            m.filtered = append(m.filtered, row)
        }
    }

    m.updateTable()
}

func (m Model) matchesAdvancedFilter(row DataRow, filter FilterCriteria) bool {
    // Filter by role
    if filter.Role != "" && row.Role != filter.Role {
        return false
    }

    // Filter by status
    if filter.Status != "" && row.Status != filter.Status {
        return false
    }

    // Filter by date range
    if !filter.DateRange.Start.IsZero() {
        rowDate, _ := time.Parse("2006-01-02", row.JoinDate)
        if rowDate.Before(filter.DateRange.Start) || rowDate.After(filter.DateRange.End) {
            return false
        }
    }

    return true
}
```

## Performance Optimizations

### Lazy Loading for Large Datasets

```go
type LazyDataTable struct {
    table     table.Model
    data      []DataRow
    pageSize  int
    currentPage int
    totalRows  int
}

func (m *LazyDataTable) loadPage(page int) tea.Cmd {
    return func() tea.Msg {
        start := page * m.pageSize
        limit := m.pageSize

        data, total := m.loadFromDatabase(start, limit)
        return PageLoadedMsg{
            page:     page,
            data:     data,
            total:    total,
            pageSize: m.pageSize,
        }
    }
}
```

### Efficient Search Implementation

```go
type SearchIndex struct {
    index map[string][]int // field -> row indices
}

func (m Model) buildSearchIndex() {
    m.searchIndex = make(map[string][]int)

    for i, row := range m.data {
        // Index each field for faster searching
        m.searchIndex["id"] = append(m.searchIndex["id"], i)
        m.searchIndex["name"] = append(m.searchIndex["name"], i)
        m.searchIndex["email"] = append(m.searchIndex["email"], i)
        // ... index other fields
    }
}

func (m Model) fastSearch(term string) []int {
    var results []int
    added := make(map[int]bool)

    for field, indices := range m.searchIndex {
        if strings.Contains(strings.ToLower(field), strings.ToLower(term)) {
            for _, idx := range indices {
                if !added[idx] {
                    results = append(results, idx)
                    added[idx] = true
                }
            }
        }
    }

    return results
}
```

## Best Practices

1. **Implement proper pagination** for large datasets to maintain performance
2. **Use consistent styling** across all columns and rows
3. **Provide clear visual feedback** for sorting, filtering, and selection states
4. **Implement keyboard shortcuts** for common operations
5. **Add proper error handling** for data loading and filtering operations
6. **Include export functionality** for data portability
7. **Use type-safe data structures** to maintain data integrity
8. **Test with various dataset sizes** to ensure performance remains acceptable