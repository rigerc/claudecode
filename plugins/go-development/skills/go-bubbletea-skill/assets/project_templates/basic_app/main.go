package main

import (
    "fmt"
    "os"
    tea "github.com/charmbracelet/bubbletea"
    "github.com/charmbracelet/lipgloss"
)

// Styles
var (
    titleStyle = lipgloss.NewStyle().
        Bold(true).
        Foreground(lipgloss.Color("62")).
        MarginTop(1).
        MarginBottom(2)

    subtitleStyle = lipgloss.NewStyle().
        Foreground(lipgloss.Color("240")).
        MarginBottom(1)

    buttonStyle = lipgloss.NewStyle().
        Foreground(lipgloss.Color("255")).
        Background(lipgloss.Color("62")).
        Padding(0, 2).
        MarginRight(1)

    activeButtonStyle = buttonStyle.
        Background(lipgloss.Color("205"))

    statusStyle = lipgloss.NewStyle().
        Foreground(lipgloss.Color("46")).
        Bold(true)
)

// Model holds the application state
type Model struct {
    choices  []string
    cursor   int
    selected int
    quiting  bool
}

// Initial model state
func initialModel() Model {
    return Model{
        choices: []string{
            "View Dashboard",
            "Manage Settings",
            "View Help",
            "Exit Application",
        },
        selected: -1,
    }
}

// Initialize the model
func (m Model) Init() tea.Cmd {
    return nil
}

// Update handles incoming messages
func (m Model) Update(msg tea.Msg) (tea.Model, tea.Cmd) {
    switch msg := msg.(type) {
    case tea.KeyMsg:
        switch msg.String() {
        case "ctrl+c", "q":
            m.quiting = true
            return m, tea.Quit

        case "up", "k":
            if m.cursor > 0 {
                m.cursor--
            }

        case "down", "j":
            if m.cursor < len(m.choices)-1 {
                m.cursor++
            }

        case "enter", " ":
            m.selected = m.cursor
            return m, m.handleSelection()

        case "r":
            // Reset selection
            m.selected = -1
        }
    }

    return m, nil
}

// View renders the UI
func (m Model) View() string {
    if m.quiting {
        return "Goodbye!\n"
    }

    // Title
    title := titleStyle.Render("🎯 BubbleTea Basic Application")

    // Subtitle
    subtitle := subtitleStyle.Render("Navigate with ↑/↓, select with Enter")

    // Menu
    var menu strings.Builder
    for i, choice := range m.choices {
        cursor := " "
        if m.cursor == i {
            cursor = "❯"
        }

        // Style the selected item
        choiceText := choice
        if m.selected == i {
            choiceText = statusStyle.Render("✓ " + choice)
        }

        menu.WriteString(fmt.Sprintf("%s %s\n", cursor, choiceText))
    }

    // Help text
    help := fmt.Sprintf("\n%s %s | %s %s | %s %s",
        lipgloss.NewStyle().Foreground(lipgloss.Color("240")).Render("↑/k"),
        lipgloss.NewStyle().Foreground(lipgloss.Color("240")).Render("up"),
        lipgloss.NewStyle().Foreground(lipgloss.Color("240")).Render("↓/j"),
        lipgloss.NewStyle().Foreground(lipgloss.Color("240")).Render("down"),
        lipgloss.NewStyle().Foreground(lipgloss.Color("240")).Render("enter"),
        lipgloss.NewStyle().Foreground(lipgloss.Color("240")).Render("select"),
    )

    help += fmt.Sprintf(" | %s %s | %s %s",
        lipgloss.NewStyle().Foreground(lipgloss.Color("240")).Render("q"),
        lipgloss.NewStyle().Foreground(lipgloss.Color("240")).Render("quit"),
        lipgloss.NewStyle().Foreground(lipgloss.Color("240")).Render("r"),
        lipgloss.NewStyle().Foreground(lipgloss.Color("240")).Render("reset"),
    )

    return title + "\n" + subtitle + "\n" + menu.String() + help
}

// Handle menu selection
func (m Model) handleSelection() tea.Cmd {
    switch m.choices[m.selected] {
    case "View Dashboard":
        return tea.Printf("Opening dashboard...")

    case "Manage Settings":
        return tea.Printf("Opening settings...")

    case "View Help":
        return tea.Printf("Opening help...")

    case "Exit Application":
        m.quiting = true
        return tea.Quit
    }
    return nil
}

// Message types for custom commands
type dashboardOpenMsg struct{}
type settingsOpenMsg struct{}
type helpOpenMsg struct{}

// Additional command handlers
func openDashboard() tea.Msg {
    return dashboardOpenMsg{}
}

func openSettings() tea.Msg {
    return settingsOpenMsg{}
}

func openHelp() tea.Msg {
    return helpOpenMsg{}
}

func main() {
    // Check terminal capabilities
    if err := checkTerminal(); err != nil {
        fmt.Printf("Terminal error: %v\n", err)
        os.Exit(1)
    }

    // Create and start the program
    p := tea.NewProgram(
        initialModel(),
        tea.WithAltScreen(),
        tea.WithMouseCellMotion(),
    )

    if _, err := p.Run(); err != nil {
        fmt.Printf("Error running program: %v\n", err)
        os.Exit(1)
    }
}

// Check terminal capabilities
func checkTerminal() error {
    // Verify color support
    if !lipgloss.DefaultRenderer().HasDarkBackground() {
        fmt.Println("Warning: Terminal background color detection failed")
    }

    // Check color profile
    profile := lipgloss.DefaultRenderer().ColorProfile()
    fmt.Printf("Color profile: %v\n", profile)

    return nil
}