# BubbleTea Component Examples

## Text Input Component Examples

### Basic Text Input with Validation

```go
package main

import (
    "fmt"
    "github.com/charmbracelet/bubbles/textinput"
    tea "github.com/charmbracelet/bubbletea"
    "github.com/charmbracelet/lipgloss"
)

type Model struct {
    textInput textinput.Model
    error     string
    ready     bool
}

func initialModel() Model {
    ti := textinput.New()
    ti.Placeholder = "Enter your email..."
    ti.Focus()
    ti.CharLimit = 50
    ti.Width = 30

    // Add validation
    ti.Validate = func(s string) error {
        if s == "" {
            return fmt.Errorf("email is required")
        }
        if !strings.Contains(s, "@") {
            return fmt.Errorf("invalid email format")
        }
        return nil
    }

    return Model{
        textInput: ti,
    }
}

func (m Model) Update(msg tea.Msg) (tea.Model, tea.Cmd) {
    var cmd tea.Cmd

    switch msg := msg.(type) {
    case tea.KeyMsg:
        switch msg.Type {
        case tea.KeyEnter:
            if err := m.textInput.Validate(m.textInput.Value()); err != nil {
                m.error = err.Error()
                return m, nil
            }
            m.ready = true
            return m, tea.Quit
        case tea.KeyCtrlC:
            return m, tea.Quit
        }
    }

    m.textInput, cmd = m.textInput.Update(msg)
    return m, cmd
}

func (m Model) View() string {
    if m.ready {
        return fmt.Sprintf("Email submitted: %s\n", m.textInput.Value())
    }

    var s strings.Builder
    s.WriteString("Email Input:\n\n")
    s.WriteString(m.textInput.View())

    if m.error != "" {
        errorStyle := lipgloss.NewStyle().
            Foreground(lipgloss.Color("9")).
            Bold(true)
        s.WriteString("\n" + errorStyle.Render("Error: "+m.error))
    }

    s.WriteString("\n\nEnter to submit, Ctrl+C to quit")
    return s.String()
}
```

### Multi-Field Form with Tab Navigation

```go
type FormModel struct {
    nameInput  textinput.Model
    emailInput textinput.Model
    ageInput   textinput.Model
    current    int
    errors     map[string]string
}

func initialFormModel() FormModel {
    name := textinput.New()
    name.Placeholder = "Full name"
    name.CharLimit = 50
    name.Width = 30
    name.Focus()

    email := textinput.New()
    email.Placeholder = "Email address"
    email.CharLimit = 50
    email.Width = 30

    age := textinput.New()
    age.Placeholder = "Age"
    age.CharLimit = 3
    age.Width = 10
    age.Validate = func(s string) error {
        if s != "" {
            age, err := strconv.Atoi(s)
            if err != nil || age < 1 || age > 120 {
                return fmt.Errorf("invalid age")
            }
        }
        return nil
    }

    return FormModel{
        nameInput:  name,
        emailInput: email,
        ageInput:   age,
        current:    0,
        errors:     make(map[string]string),
    }
}

func (m FormModel) Update(msg tea.Msg) (tea.Model, tea.Cmd) {
    var cmd tea.Cmd

    switch msg := msg.(type) {
    case tea.KeyMsg:
        switch msg.Type {
        case tea.KeyTab, tea.KeyShiftTab:
            // Cycle through fields
            if msg.Type == tea.KeyTab {
                m.current = (m.current + 1) % 3
            } else {
                m.current = (m.current - 1 + 3) % 3
            }
            return m, m.updateFocus()

        case tea.KeyEnter:
            if m.validateForm() {
                return m, tea.Quit
            }
        case tea.KeyCtrlC:
            return m, tea.Quit
        }
    }

    // Update current field
    switch m.current {
    case 0:
        m.nameInput, cmd = m.nameInput.Update(msg)
    case 1:
        m.emailInput, cmd = m.emailInput.Update(msg)
    case 2:
        m.ageInput, cmd = m.ageInput.Update(msg)
    }

    return m, cmd
}

func (m FormModel) updateFocus() tea.Cmd {
    switch m.current {
    case 0:
        m.nameInput.Focus()
        m.emailInput.Blur()
        m.ageInput.Blur()
    case 1:
        m.nameInput.Blur()
        m.emailInput.Focus()
        m.ageInput.Blur()
    case 2:
        m.nameInput.Blur()
        m.emailInput.Blur()
        m.ageInput.Focus()
    }
    return nil
}

func (m FormModel) validateForm() bool {
    m.errors = make(map[string]string)

    if m.nameInput.Value() == "" {
        m.errors["name"] = "name is required"
    }

    if m.emailInput.Value() == "" {
        m.errors["email"] = "email is required"
    } else if !strings.Contains(m.emailInput.Value(), "@") {
        m.errors["email"] = "invalid email format"
    }

    if m.ageInput.Value() == "" {
        m.errors["age"] = "age is required"
    }

    return len(m.errors) == 0
}
```

## Table Component Examples

### Data Table with Sorting and Filtering

```go
type DataTableModel struct {
    table      table.Model
    data       []DataRow
    filtered   []DataRow
    sortColumn int
    ascending  bool
    filter     string
}

type DataRow struct {
    ID     int
    Name   string
    Email  string
    Status string
    Date   time.Time
}

func initialDataTableModel() DataTableModel {
    data := []DataRow{
        {1, "Alice Johnson", "alice@example.com", "Active", time.Now()},
        {2, "Bob Smith", "bob@example.com", "Inactive", time.Now().AddDate(0, -1, 0)},
        {3, "Charlie Brown", "charlie@example.com", "Active", time.Now().AddDate(0, -2, 0)},
    }

    columns := []table.Column{
        {Title: "ID", Width: 6},
        {Title: "Name", Width: 20},
        {Title: "Email", Width: 25},
        {Title: "Status", Width: 10},
        {Title: "Date", Width: 12},
    }

    t := table.New(
        table.WithColumns(columns),
        table.WithRows(dataToTableRows(data)),
        table.WithFocused(true),
        table.WithHeight(10),
    )

    // Add header click handlers
    t.KeyMap.LineUp = key.NewBinding(
        key.WithKeys("k", "up"),
        key.WithHelp("↑/k", "up"),
    )

    return DataTableModel{
        table:      t,
        data:       data,
        filtered:   data,
        sortColumn: 0,
        ascending:  true,
    }
}

func (m DataTableModel) Update(msg tea.Msg) (tea.Model, tea.Cmd) {
    var cmd tea.Cmd

    switch msg := msg.(type) {
    case tea.KeyMsg:
        switch msg.String() {
        case "ctrl+c", "q":
            return m, tea.Quit

        case "f":
            return m, m.promptForFilter()

        case "s":
            // Sort by current column
            m.sortData()

        case "r":
            // Reset filters and sorting
            m.filter = ""
            m.filtered = m.data
            m.updateTable()

        case "enter":
            // View details of selected row
            selected := m.table.SelectedRow()
            if len(selected) > 0 {
                return m, tea.Printf("Selected: %v", selected)
            }
        }
    }

    m.table, cmd = m.table.Update(msg)
    return m, cmd
}

func (m DataTableModel) sortData() {
    sort.Slice(m.filtered, func(i, j int) bool {
        switch m.sortColumn {
        case 0: // ID
            if m.ascending {
                return m.filtered[i].ID < m.filtered[j].ID
            }
            return m.filtered[i].ID > m.filtered[j].ID
        case 1: // Name
            if m.ascending {
                return m.filtered[i].Name < m.filtered[j].Name
            }
            return m.filtered[i].Name > m.filtered[j].Name
        // Add more cases for other columns
        }
        return false
    })

    m.ascending = !m.ascending
    m.updateTable()
}

func (m DataTableModel) filterData(term string) {
    if term == "" {
        m.filtered = m.data
    } else {
        m.filtered = nil
        for _, row := range m.data {
            if strings.Contains(strings.ToLower(row.Name), strings.ToLower(term)) ||
               strings.Contains(strings.ToLower(row.Email), strings.ToLower(term)) ||
               strings.Contains(strings.ToLower(row.Status), strings.ToLower(term)) {
                m.filtered = append(m.filtered, row)
            }
        }
    }
    m.updateTable()
}

func (m DataTableModel) updateTable() {
    rows := dataToTableRows(m.filtered)
    m.table.SetRows(rows)
}

func dataToTableRows(data []DataRow) []table.Row {
    var rows []table.Row
    for _, d := range data {
        rows = append(rows, table.Row{
            fmt.Sprintf("%d", d.ID),
            d.Name,
            d.Email,
            d.Status,
            d.Date.Format("2006-01-02"),
        })
    }
    return rows
}
```

## List Component Examples

### Advanced List with Search and Pagination

```go
type AdvancedListModel struct {
    list     list.Model
    items    []ListItem
    filtered []ListItem
    search   textinput.Model
    searching bool
}

type ListItem struct {
    ID          int
    Title       string
    Description string
    Category    string
    Tags        []string
}

func (i ListItem) Title() string { return i.Title }
func (i ListItem) Description() string { return i.Description }
func (i ListItem) FilterValue() string {
    return fmt.Sprintf("%s %s %s", i.Title, i.Description, strings.Join(i.Tags, " "))
}

func initialAdvancedListModel() AdvancedListModel {
    items := []ListItem{
        {1, "Task Management", "Create and manage tasks", "Productivity", []string{"todo", "tasks"}},
        {2, "Note Taking", "Write and organize notes", "Productivity", []string{"notes", "writing"}},
        {3, "Time Tracking", "Track time spent on projects", "Productivity", []string{"time", "tracking"}},
    }

    // Custom delegate
    delegate := list.NewDefaultDelegate()
    delegate.ShowDescription = true
    delegate.DescriptionStyle = lipgloss.NewStyle().
        Foreground(lipgloss.Color("240")).
        MarginLeft(1)

    l := list.New(itemsToItems(items), delegate, 0, 0)
    l.Title = "Applications"
    l.SetFilteringEnabled(true)
    l.SetShowStatusBar(true)
    l.SetShowPagination(true)
    l.SetShowHelp(true)

    // Search input
    search := textinput.New()
    search.Placeholder = "Search applications..."
    search.CharLimit = 50
    search.Width = 40

    return AdvancedListModel{
        list:     l,
        items:    items,
        filtered: items,
        search:   search,
    }
}

func (m AdvancedListModel) Update(msg tea.Msg) (tea.Model, tea.Cmd) {
    var cmd tea.Cmd

    switch msg := msg.(type) {
    case tea.KeyMsg:
        switch msg.String() {
        case "ctrl+c", "q":
            return m, tea.Quit

        case "/":
            m.searching = true
            m.search.Focus()
            return m, nil

        case tea.KeyEscape:
            if m.searching {
                m.searching = false
                m.search.Blur()
                m.search.SetValue("")
                m.list.ResetFilter()
                return m, nil
            }
        }
    }

    if m.searching {
        m.search, cmd = m.search.Update(msg)

        // Update list filter
        if m.search.Value() != "" {
            m.list.SetFilter(m.search.Value())
        } else {
            m.list.ResetFilter()
        }
    } else {
        m.list, cmd = m.list.Update(msg)
    }

    return m, cmd
}

func (m AdvancedListModel) View() string {
    var s strings.Builder

    if m.searching {
        s.WriteString("Search: " + m.search.View() + " (ESC to cancel)\n\n")
    }

    s.WriteString(m.list.View())
    return s.String()
}

func itemsToItems(items []ListItem) []list.Item {
    var listItems []list.Item
    for _, item := range items {
        listItems = append(listItems, item)
    }
    return listItems
}
```

## Progress Component Examples

### Multi-Stage Progress Tracker

```go
type ProgressStage struct {
    Name     string
    Status   string // "pending", "running", "complete", "error"
    Progress float64
    Error    string
}

type ProgressTrackerModel struct {
    stages   []ProgressStage
    current  int
    progress progress.Model
    timer    *time.Timer
}

func initialProgressTrackerModel() ProgressTrackerModel {
    stages := []ProgressStage{
        {"Initializing", "pending", 0.0, ""},
        {"Loading Configuration", "pending", 0.0, ""},
        {"Connecting to Database", "pending", 0.0, ""},
        {"Fetching Data", "pending", 0.0, ""},
        {"Processing Data", "pending", 0.0, ""},
        {"Finalizing", "pending", 0.0, ""},
    }

    p := progress.New(
        progress.WithDefaultGradient(),
        progress.WithWidth(50),
        progress.WithoutPercentage(),
    )

    return ProgressTrackerModel{
        stages:   stages,
        progress: p,
    }
}

func (m ProgressTrackerModel) Init() tea.Cmd {
    return m.startNextStage()
}

func (m ProgressTrackerModel) startNextStage() tea.Cmd {
    if m.current >= len(m.stages) {
        return tea.Quit
    }

    // Set current stage to running
    m.stages[m.current].Status = "running"

    // Simulate stage work
    duration := time.Duration(2+m.current) * time.Second
    m.timer = time.AfterFunc(duration, func() {
        p.Send(stageCompleteMsg{})
    })

    // Start progress animation
    cmd := m.progress.SetPercent(0)
    return tea.Batch(
        cmd,
        tea.Tick(time.Millisecond*50, func(t time.Time) tea.Msg {
            return progressTickMsg{}
        }),
    )
}

func (m ProgressTrackerModel) Update(msg tea.Msg) (tea.Model, tea.Cmd) {
    switch msg := msg.(type) {
    case stageCompleteMsg:
        // Mark current stage as complete
        m.stages[m.current].Status = "complete"
        m.stages[m.current].Progress = 1.0

        m.current++
        return m, m.startNextStage()

    case progressTickMsg:
        if m.current < len(m.stages) && m.stages[m.current].Status == "running" {
            current := m.stages[m.current]
            if current.Progress < 1.0 {
                current.Progress += 0.02
                m.stages[m.current] = current

                var cmd tea.Cmd
                m.progress, cmd = m.progress.Update(msg)
                return m, cmd
            }
        }
        return m, nil

    case progress.FrameMsg:
        var cmd tea.Cmd
        m.progress, cmd = m.progress.Update(msg)
        return m, cmd
    }

    return m, nil
}

func (m ProgressTrackerModel) View() string {
    var s strings.Builder
    s.WriteString("Application Startup\n\n")

    // Show stages
    for i, stage := range m.stages {
        statusIcon := "○"
        statusColor := lipgloss.Color("240")

        switch stage.Status {
        case "running":
            statusIcon = "⟳"
            statusColor = lipgloss.Color("226")
        case "complete":
            statusIcon = "✓"
            statusColor = lipgloss.Color("46")
        case "error":
            statusIcon = "✗"
            statusColor = lipgloss.Color("9")
        }

        style := lipgloss.NewStyle().
            Foreground(statusColor).
            Bold(stage.Status == "running")

        stageText := fmt.Sprintf("%s %s", statusIcon, stage.Name)
        if stage.Status == "running" {
            stageText += fmt.Sprintf(" %d%%", int(stage.Progress*100))
        }

        s.WriteString(style.Render(stageText) + "\n")

        if stage.Error != "" {
            errorStyle := lipgloss.NewStyle().
                Foreground(lipgloss.Color("9")).
                MarginLeft(2)
            s.WriteString(errorStyle.Render("Error: "+stage.Error) + "\n")
        }
    }

    // Show progress bar for current stage
    if m.current < len(m.stages) && m.stages[m.current].Status == "running" {
        s.WriteString("\n" + m.stages[m.current].Name + "\n")
        s.WriteString(m.progress.View() + "\n")
    }

    return s.String()
}
```

## Spinner Component Examples

### Multi-Process Loading Indicator

```go
type LoadingProcess struct {
    Name     string
    Complete bool
    Error    string
}

type MultiSpinnerModel struct {
    processes []LoadingProcess
    spinners  []spinner.Model
    current   int
    done      bool
}

func initialMultiSpinnerModel() MultiSpinnerModel {
    processes := []LoadingProcess{
        {"Loading user data", false, ""},
        {"Loading preferences", false, ""},
        {"Connecting to services", false, ""},
        {"Preparing interface", false, ""},
    }

    var spinners []spinner.Model
    spinnerTypes := []spinner.Spinner{
        spinner.Dot,
        spinner.Line,
        spinner.MiniDot,
        spinner.Jump,
    }

    colors := []lipgloss.Color{
        lipgloss.Color("205"), // Pink
        lipgloss.Color("69"),  // Blue
        lipgloss.Color("226"), // Yellow
        lipgloss.Color("46"),  // Green
    }

    for i, process := range processes {
        s := spinner.New()
        s.Spinner = spinnerTypes[i%len(spinnerTypes)]
        s.Style = lipgloss.NewStyle().
            Foreground(colors[i%len(colors)])
        spinners = append(spinners, s)
    }

    return MultiSpinnerModel{
        processes: processes,
        spinners:  spinners,
        current:   0,
    }
}

func (m MultiSpinnerModel) Init() tea.Cmd {
    return m.startNextProcess()
}

func (m MultiSpinnerModel) startNextProcess() tea.Cmd {
    if m.current >= len(m.processes) {
        m.done = true
        return tea.Quit
    }

    // Simulate process with random duration
    duration := time.Duration(1+rand.Intn(3)) * time.Second

    return tea.Tick(duration, func(t time.Time) tea.Msg {
        // Random chance of error
        if rand.Float32() < 0.1 { // 10% chance of error
            return processErrorMsg{
                index: m.current,
                error: "simulated error occurred",
            }
        }
        return processCompleteMsg{index: m.current}
    })
}

func (m MultiSpinnerModel) Update(msg tea.Msg) (tea.Model, tea.Cmd) {
    switch msg := msg.(type) {
    case processCompleteMsg:
        if msg.index < len(m.processes) {
            m.processes[msg.index].Complete = true
            m.current++
            return m, m.startNextProcess()
        }

    case processErrorMsg:
        if msg.index < len(m.processes) {
            m.processes[msg.index].Error = msg.error
            m.current++
            return m, m.startNextProcess()
        }

    case spinner.TickMsg:
        // Update all incomplete spinners
        for i := range m.spinners {
            if !m.processes[i].Complete && m.processes[i].Error == "" {
                var cmd tea.Cmd
                m.spinners[i], cmd = m.spinners[i].Update(msg)
                if cmd != nil {
                    return m, cmd
                }
            }
        }
    }

    return m, nil
}

func (m MultiSpinnerModel) View() string {
    if m.done {
        return "\n✓ All processes completed successfully!\n"
    }

    var s strings.Builder
    s.WriteString("\nStarting application...\n\n")

    for i, process := range m.processes {
        var status string
        var style lipgloss.Style

        if process.Complete {
            status = "✓ Complete"
            style = lipgloss.NewStyle().Foreground(lipgloss.Color("46"))
        } else if process.Error != "" {
            status = "✗ " + process.Error
            style = lipgloss.NewStyle().Foreground(lipgloss.Color("9"))
        } else {
            status = m.spinners[i].View() + " " + process.Name
            style = m.spinners[i].Style
        }

        s.WriteString(style.Render(status) + "\n")
    }

    return s.String()
}
```

These component examples demonstrate common patterns and advanced usage scenarios for BubbleTea applications. Each example shows proper error handling, styling, and interaction patterns that can be adapted for specific use cases.