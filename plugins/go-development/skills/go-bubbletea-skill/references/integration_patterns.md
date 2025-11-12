# BubbleTea Integration Patterns

This reference covers advanced integration patterns for building complex BubbleTea applications with multiple components, state management, and sophisticated user interactions.

## Component Composition Patterns

### Tab-Based Interface

```go
type TabModel struct {
    tabs       []string
    active     int
    components []tea.Model
    width      int
    height     int
}

type TabContent interface {
    tea.Model
    Update(msg tea.Msg) (tea.Model, tea.Cmd)
    View() string
    Resize(width, height int)
}

func NewTabModel() TabModel {
    return TabModel{
        tabs: []string{"Dashboard", "Settings", "Help"},
        active: 0,
        components: []tea.Model{
            NewDashboardModel(),
            NewSettingsModel(),
            NewHelpModel(),
        },
    }
}

func (m TabModel) Update(msg tea.Msg) (tea.Model, tea.Cmd) {
    var cmd tea.Cmd

    switch msg := msg.(type) {
    case tea.KeyMsg:
        switch msg.String() {
        case "ctrl+c", "q":
            return m, tea.Quit

        case "tab", "right":
            m.active = (m.active + 1) % len(m.tabs)
            m.resizeActiveComponent()

        case "shift+tab", "left":
            m.active = (m.active - 1 + len(m.tabs)) % len(m.tabs)
            m.resizeActiveComponent()

        case "1", "2", "3":
            index := int(msg.String()[0] - '1')
            if index < len(m.tabs) {
                m.active = index
                m.resizeActiveComponent()
            }
        }

    case tea.WindowSizeMsg:
        m.width = msg.Width
        m.height = msg.Height - 3 // Leave space for tabs
        m.resizeActiveComponent()
    }

    // Only update active component
    if m.active < len(m.components) {
        content := m.components[m.active].(TabContent)
        newContent, contentCmd := content.Update(msg)
        m.components[m.active] = newContent
        cmd = tea.Batch(cmd, contentCmd)
    }

    return m, cmd
}

func (m TabModel) resizeActiveComponent() {
    if m.active < len(m.components) {
        content := m.components[m.active].(TabContent)
        content.Resize(m.width, m.height)
        m.components[m.active] = content
    }
}

func (m TabModel) View() string {
    // Render tabs
    var tabs strings.Builder
    for i, tab := range m.tabs {
        var style lipgloss.Style
        if i == m.active {
            style = lipgloss.NewStyle().
                Foreground(lipgloss.Color("230")).
                Background(lipgloss.Color("62")).
                Padding(0, 2).
                Bold(true)
        } else {
            style = lipgloss.NewStyle().
                Foreground(lipgloss.Color("245")).
                Padding(0, 2)
        }

        tabs.WriteString(style.Render(tab))
        if i < len(m.tabs)-1 {
            tabs.WriteString(" ")
        }
    }

    // Render active content
    var content string
    if m.active < len(m.components) {
        content = m.components[m.active].(TabContent).View()
    }

    return lipgloss.JoinVertical(
        lipgloss.Left,
        tabs.String(),
        lipgloss.NewStyle().
            Height(m.height).
            Border(lipgloss.NormalBorder()).
            BorderForeground(lipgloss.Color("239")).
            Render(content),
    )
}
```

### Split-Panel Layout

```go
type SplitPanelModel struct {
    leftPanel  tea.Model
    rightPanel tea.Model
    splitRatio float64 // 0.0-1.0, where 0.5 is equal split
    width      int
    height     int
    focused    string // "left" or "right"
}

func NewSplitPanelModel() SplitPanelModel {
    return SplitPanelModel{
        leftPanel:  NewFileExplorerModel(),
        rightPanel: NewContentModel(),
        splitRatio: 0.3, // 30% left, 70% right
        focused:    "left",
    }
}

func (m SplitPanelModel) Update(msg tea.Msg) (tea.Model, tea.Cmd) {
    var cmd tea.Cmd

    switch msg := msg.(type) {
    case tea.KeyMsg:
        switch msg.String() {
        case "ctrl+c", "q":
            return m, tea.Quit

        case "tab":
            // Toggle focus between panels
            if m.focused == "left" {
                m.focused = "right"
            } else {
                m.focused = "left"
            }
            return m, nil

        case "left":
            if m.focused == "right" {
                m.focused = "left"
            }

        case "right":
            if m.focused == "left" {
                m.focused = "right"
            }
        }

    case tea.WindowSizeMsg:
        m.width = msg.Width
        m.height = msg.Height
        m.resizePanels()
    }

    // Update focused panel
    var updateCmd tea.Cmd
    if m.focused == "left" {
        m.leftPanel, updateCmd = m.leftPanel.Update(msg)
    } else {
        m.rightPanel, updateCmd = m.rightPanel.Update(msg)
    }

    return m, tea.Batch(cmd, updateCmd)
}

func (m SplitPanelModel) resizePanels() {
    leftWidth := int(float64(m.width) * m.splitRatio)
    rightWidth := m.width - leftWidth - 1 // -1 for divider

    // Resize panels (assuming they implement Resizable interface)
    if left, ok := m.leftPanel.(Resizable); ok {
        left.Resize(leftWidth, m.height)
    }

    if right, ok := m.rightPanel.(Resizable); ok {
        right.Resize(rightWidth, m.height)
    }
}

func (m SplitPanelModel) View() string {
    leftWidth := int(float64(m.width) * m.splitRatio)
    rightWidth := m.width - leftWidth - 1

    leftContent := lipgloss.NewStyle().
        Width(leftWidth).
        Height(m.height).
        Border(lipgloss.RoundedBorder()).
        BorderForeground(func() lipgloss.Color {
            if m.focused == "left" {
                return lipgloss.Color("62")
            }
            return lipgloss.Color("239")
        }()).
        Render(m.leftPanel.(tea.Model).View())

    rightContent := lipgloss.NewStyle().
        Width(rightWidth).
        Height(m.height).
        Border(lipgloss.RoundedBorder()).
        BorderForeground(func() lipgloss.Color {
            if m.focused == "right" {
                return lipgloss.Color("62")
            }
            return lipgloss.Color("239")
        }()).
        Render(m.rightPanel.(tea.Model).View())

    // Divider
    divider := lipgloss.NewStyle().
        Width(1).
        Height(m.height).
        Background(lipgloss.Color("236")).
        Render(strings.Repeat("│", m.height))

    return lipgloss.JoinHorizontal(lipgloss.Left, leftContent, divider, rightContent)
}

// Interface for resizable components
type Resizable interface {
    Resize(width, height int)
}
```

### Master-Detail Pattern

```go
type MasterDetailModel struct {
    master    list.Model
    detail    tea.Model
    selected  interface{}
    showDetail bool
    width     int
    height    int
}

func NewMasterDetailModel() MasterDetailModel {
    // Initialize master list
    items := []list.Item{
        &ListItem{ID: 1, Title: "Item 1", Description: "Description 1"},
        &ListItem{ID: 2, Title: "Item 2", Description: "Description 2"},
    }

    delegate := list.NewDefaultDelegate()
    delegate.ShowDescription = true

    master := list.New(items, delegate, 0, 0)
    master.Title = "Items"

    return MasterDetailModel{
        master: master,
        detail: NewEmptyDetailModel(),
    }
}

func (m MasterDetailModel) Update(msg tea.Msg) (tea.Model, tea.Cmd) {
    var cmd tea.Cmd

    switch msg := msg.(type) {
    case tea.KeyMsg:
        switch msg.String() {
        case "ctrl+c", "q":
            return m, tea.Quit

        case "enter":
            // Show detail for selected item
            if selected := m.master.SelectedItem(); selected != nil {
                m.selected = selected
                m.detail = NewDetailModel(selected.(*ListItem))
                m.showDetail = true
                m.resizeComponents()
            }

        case "escape":
            // Hide detail, return to master
            m.showDetail = false
            m.selected = nil

        case "f":
            // Toggle fullscreen detail
            if m.showDetail {
                m.showDetail = !m.showDetail
                m.resizeComponents()
            }
        }

    case tea.WindowSizeMsg:
        m.width = msg.Width
        m.height = msg.Height
        m.resizeComponents()
    }

    // Update components based on current view
    if m.showDetail {
        m.detail, cmd = m.detail.Update(msg)
    } else {
        // Handle list selection updates
        oldSelection := m.master.SelectedItem()
        m.master, cmd = m.master.Update(msg)
        newSelection := m.master.SelectedItem()

        // Auto-show detail if selection changed
        if oldSelection != newSelection && newSelection != nil && !m.showDetail {
            m.selected = newSelection
            m.detail = NewDetailModel(newSelection.(*ListItem))
            m.showDetail = true
            m.resizeComponents()
        }
    }

    return m, cmd
}

func (m MasterDetailModel) resizeComponents() {
    if m.showDetail {
        // Show both master and detail
        masterWidth := m.width / 3
        detailWidth := m.width - masterWidth - 1

        if list, ok := m.master.(Resizable); ok {
            list.Resize(masterWidth, m.height)
        }

        if detail, ok := m.detail.(Resizable); ok {
            detail.Resize(detailWidth, m.height)
        }
    } else {
        // Show only master
        if list, ok := m.master.(Resizable); ok {
            list.Resize(m.width, m.height)
        }
    }
}

func (m MasterDetailModel) View() string {
    if m.showDetail {
        masterWidth := m.width / 3
        detailWidth := m.width - masterWidth - 1

        masterView := lipgloss.NewStyle().
            Width(masterWidth).
            Height(m.height).
            Border(lipgloss.RoundedBorder()).
            BorderForeground(lipgloss.Color("62")).
            Render(m.master.View())

        detailView := lipgloss.NewStyle().
            Width(detailWidth).
            Height(m.height).
            Border(lipgloss.RoundedBorder()).
            BorderForeground(lipgloss.Color("205")).
            Render(m.detail.(tea.Model).View())

        return lipgloss.JoinHorizontal(lipgloss.Left, masterView, detailView)
    }

    return lipgloss.NewStyle().
        Width(m.width).
        Height(m.height).
        Border(lipgloss.RoundedBorder()).
        BorderForeground(lipgloss.Color("239")).
        Render(m.master.View())
}
```

## State Management Patterns

### Global State Manager

```go
type AppState struct {
    User        User
    Preferences Preferences
    Data        map[string]interface{}
    Errors      []string
}

type StateManager struct {
    state      AppState
    listeners  []chan AppState
    history    []AppState
    historyMax int
}

func NewStateManager() *StateManager {
    return &StateManager{
        state:      AppState{},
        listeners:  make([]chan AppState, 0),
        history:    make([]AppState, 0),
        historyMax: 50,
    }
}

func (sm *StateManager) UpdateState(updates func(AppState) AppState) {
    // Save current state to history
    sm.history = append(sm.history, sm.state)
    if len(sm.history) > sm.historyMax {
        sm.history = sm.history[1:]
    }

    // Apply updates
    sm.state = updates(sm.state)

    // Notify listeners
    for _, listener := range sm.listeners {
        go func(ch chan AppState) {
            ch <- sm.state
        }(listener)
    }
}

func (sm *StateManager) GetState() AppState {
    return sm.state
}

func (sm *StateManager) AddListener() chan AppState {
    ch := make(chan AppState, 1)
    sm.listeners = append(sm.listeners, ch)
    return ch
}

func (sm *StateManager) Undo() bool {
    if len(sm.history) == 0 {
        return false
    }

    sm.state = sm.history[len(sm.history)-1]
    sm.history = sm.history[:len(sm.history)-1]

    // Notify listeners
    for _, listener := range sm.listeners {
        go func(ch chan AppState) {
            ch <- sm.state
        }(listener)
    }

    return true
}

// Integration with BubbleTea
type StateAwareModel struct {
    manager *StateManager
    stateCh chan AppState
    // ... other model fields
}

func (m StateAwareModel) UpdateState(msg tea.Msg) (tea.Model, tea.Cmd) {
    switch msg := msg.(type) {
    case StateChangeMsg:
        m.manager.UpdateState(func(state AppState) AppState {
            return msg.State
        })

    case UserLoadedMsg:
        m.manager.UpdateState(func(state AppState) AppState {
            state.User = msg.User
            return state
        })
    }

    return m, nil
}
```

### Component Communication

```go
// Message types for component communication
type ComponentEventMsg struct {
    Source    string
    Target    string
    EventType string
    Data      interface{}
}

type NavigationMsg struct {
    From string
    To   string
    Data interface{}
}

type DataUpdateMsg struct {
    Component string
    Field     string
    Value     interface{}
}

// Event bus pattern
type EventBus struct {
    subscribers map[string][]chan tea.Msg
    mutex      sync.RWMutex
}

func NewEventBus() *EventBus {
    return &EventBus{
        subscribers: make(map[string][]chan tea.Msg),
    }
}

func (eb *EventBus) Subscribe(eventType string) chan tea.Msg {
    eb.mutex.Lock()
    defer eb.mutex.Unlock()

    ch := make(chan tea.Msg, 10)
    eb.subscribers[eventType] = append(eb.subscribers[eventType], ch)
    return ch
}

func (eb *EventBus) Publish(eventType string, msg tea.Msg) {
    eb.mutex.RLock()
    defer eb.mutex.RUnlock()

    if subscribers, ok := eb.subscribers[eventType]; ok {
        for _, ch := range subscribers {
            go func(c chan tea.Msg) {
                c <- msg
            }(ch)
        }
    }
}

// Integrated model with event bus
type EventDrivenModel struct {
    eventBus *EventBus
    components map[string]tea.Model
    eventChans map[string]chan tea.Msg
    // ... other fields
}

func (m EventDrivenModel) Update(msg tea.Msg) (tea.Model, tea.Cmd) {
    var cmd tea.Cmd

    switch msg := msg.(type) {
    case tea.KeyMsg:
        // Handle global key events
        switch msg.String() {
        case "ctrl+c", "q":
            return m, tea.Quit
        }

    case ComponentEventMsg:
        // Route events to target components
        if target, ok := m.components[msg.Target]; ok {
            newTarget, targetCmd := target.Update(msg)
            m.components[msg.Target] = newTarget
            cmd = tea.Batch(cmd, targetCmd)
        }

    default:
        // Update all components
        for name, component := range m.components {
            newComponent, componentCmd := component.Update(msg)
            m.components[name] = newComponent
            cmd = tea.Batch(cmd, componentCmd)
        }
    }

    return m, cmd
}
```

## Data Flow Patterns

### Repository Pattern

```go
type Repository[T any] interface {
    GetAll() ([]T, error)
    GetByID(id string) (T, error)
    Create(item T) error
    Update(id string, item T) error
    Delete(id string) error
    Find(predicate func(T) bool) ([]T, error)
}

type DataLoadedMsg[T any] struct {
    Data []T
    Error error
}

type DataUpdatedMsg[T any] struct {
    Item T
    Error error
}

type RepositoryModel[T any] struct {
    repo     Repository[T]
    items    []T
    loading  bool
    error    error
    selected T
}

func (m RepositoryModel[T]) Init() tea.Cmd {
    return m.loadData()
}

func (m RepositoryModel[T]) loadData() tea.Cmd {
    return func() tea.Msg {
        data, err := m.repo.GetAll()
        return DataLoadedMsg[T]{Data: data, Error: err}
    }
}

func (m RepositoryModel[T]) Update(msg tea.Msg) (tea.Model, tea.Cmd) {
    var cmd tea.Cmd

    switch msg := msg.(type) {
    case DataLoadedMsg[T]:
        m.loading = false
        m.error = msg.Error
        m.items = msg.Data

    case DataUpdatedMsg[T]:
        if msg.Error != nil {
            m.error = msg.Error
        } else {
            // Update item in collection
            for i, item := range m.items {
                if m.getItemID(item) == m.getItemID(msg.Item) {
                    m.items[i] = msg.Item
                    break
                }
            }
        }

    case RefreshDataMsg:
        m.loading = true
        return m, m.loadData()
    }

    return m, cmd
}

func (m RepositoryModel[T]) getItemID(item T) string {
    // This would be implemented by specific types
    return ""
}
```

### Cache Layer

```go
type CacheItem struct {
    Data      interface{}
    ExpiresAt time.Time
}

type Cache struct {
    items map[string]CacheItem
    mutex sync.RWMutex
    ttl   time.Duration
}

func NewCache(ttl time.Duration) *Cache {
    return &Cache{
        items: make(map[string]CacheItem),
        ttl:   ttl,
    }
}

func (c *Cache) Set(key string, data interface{}) {
    c.mutex.Lock()
    defer c.mutex.Unlock()

    c.items[key] = CacheItem{
        Data:      data,
        ExpiresAt: time.Now().Add(c.ttl),
    }
}

func (c *Cache) Get(key string) (interface{}, bool) {
    c.mutex.RLock()
    defer c.mutex.RUnlock()

    item, exists := c.items[key]
    if !exists || time.Now().After(item.ExpiresAt) {
        return nil, false
    }

    return item.Data, true
}

func (c *Cache) Cleanup() {
    c.mutex.Lock()
    defer c.mutex.Unlock()

    for key, item := range c.items {
        if time.Now().After(item.ExpiresAt) {
            delete(c.items, key)
        }
    }
}

// Cached repository wrapper
type CachedRepository[T any] struct {
    repo  Repository[T]
    cache *Cache
}

func NewCachedRepository[T any](repo Repository[T], ttl time.Duration) *CachedRepository[T] {
    return &CachedRepository[T]{
        repo:  repo,
        cache: NewCache(ttl),
    }
}

func (c *CachedRepository[T]) GetAll() ([]T, error) {
    key := "all_items"
    if data, exists := c.cache.Get(key); exists {
        return data.([]T), nil
    }

    items, err := c.repo.GetAll()
    if err == nil {
        c.cache.Set(key, items)
    }

    return items, err
}
```

## Advanced UI Patterns

### Context Menus

```go
type ContextMenuModel struct {
    visible  bool
    x, y     int
    options  []ContextOption
    selected int
}

type ContextOption struct {
    Text  string
    Action tea.Cmd
    Icon  string
}

func NewContextMenuModel() ContextMenuModel {
    return ContextMenuModel{
        visible: false,
        options: make([]ContextOption, 0),
    }
}

func (m ContextMenuModel) Show(x, y int, options []ContextOption) tea.Cmd {
    m.visible = true
    m.x = x
    m.y = y
    m.options = options
    m.selected = 0
    return nil
}

func (m ContextMenuModel) Hide() tea.Cmd {
    m.visible = false
    return nil
}

func (m ContextMenuModel) Update(msg tea.Msg) (tea.Model, tea.Cmd) {
    var cmd tea.Cmd

    switch msg := msg.(type) {
    case tea.KeyMsg:
        if !m.visible {
            return m, nil
        }

        switch msg.String() {
        case "escape":
            return m, m.Hide()

        case "enter":
            if m.selected < len(m.options) {
                return m, tea.Batch(m.options[m.selected].Action, m.Hide())
            }

        case "up":
            if m.selected > 0 {
                m.selected--
            }

        case "down":
            if m.selected < len(m.options)-1 {
                m.selected++
            }
        }
    }

    return m, cmd
}

func (m ContextMenuModel) View() string {
    if !m.visible {
        return ""
    }

    // Calculate menu dimensions
    maxText := 0
    for _, option := range m.options {
        if len(option.Text) > maxText {
            maxText = len(option.Text)
        }
    }

    menuWidth := maxText + 4 // padding + icon space
    menuHeight := len(m.options)

    // Render menu items
    var items strings.Builder
    for i, option := range m.options {
        style := lipgloss.NewStyle().
            Width(menuWidth).
            Padding(0, 1).
            Background(lipgloss.Color("236"))

        if i == m.selected {
            style = style.
                Background(lipgloss.Color("62")).
                Foreground(lipgloss.Color("230")).
                Bold(true)
        }

        item := fmt.Sprintf("%s %s", option.Icon, option.Text)
        items.WriteString(style.Render(item))
    }

    menu := lipgloss.NewStyle().
        Border(lipgloss.RoundedBorder()).
        BorderForeground(lipgloss.Color("62")).
        Background(lipgloss.Color("236")).
        Render(items.String())

    return lipgloss.Place(
        m.x+menuWidth, m.y+menuHeight,
        m.x, m.y,
        menu,
        lipgloss.WithWhitespaceChars(" "),
        lipgloss.WithWhitespaceForeground(lipgloss.Color("236")),
    )
}
```

### Modal Dialogs

```go
type ModalModel struct {
    visible bool
    title   string
    content string
    type    ModalType
}

type ModalType int

const (
    ModalInfo ModalType = iota
    ModalWarning
    ModalError
    ModalConfirmation
)

func NewModalModel() ModalModel {
    return ModalModel{
        visible: false,
    }
}

func (m ModalModel) Show(title, content string, modalType ModalType) tea.Cmd {
    m.visible = true
    m.title = title
    m.content = content
    m.type = modalType
    return nil
}

func (m ModalModel) Hide() tea.Cmd {
    m.visible = false
    return nil
}

func (m ModalModel) Update(msg tea.Msg) (tea.Model, tea.Cmd) {
    switch msg := msg.(type) {
    case tea.KeyMsg:
        if m.visible {
            switch msg.String() {
            case "enter", " ":
                if m.type == ModalConfirmation {
                    return m, tea.Batch(m.confirmAction(), m.Hide())
                } else {
                    return m, m.Hide()
                }
            case "escape":
                return m, m.Hide()
            }
        }
    }

    return m, nil
}

func (m ModalModel) confirmAction() tea.Cmd {
    return func() tea.Msg {
        return ModalConfirmedMsg{}
    }
}

func (m ModalModel) View() string {
    if !m.visible {
        return ""
    }

    // Style based on modal type
    var borderColor lipgloss.Color
    var icon string

    switch m.type {
    case ModalInfo:
        borderColor = lipgloss.Color("69")
        icon = "ℹ"
    case ModalWarning:
        borderColor = lipgloss.Color("226")
        icon = "⚠"
    case ModalError:
        borderColor = lipgloss.Color("9")
        icon = "✗"
    case ModalConfirmation:
        borderColor = lipgloss.Color("62")
        icon = "?"
    }

    titleStyle := lipgloss.NewStyle().
        Bold(true).
        Foreground(borderColor).
        MarginBottom(1)

    contentStyle := lipgloss.NewStyle().
        Foreground(lipgloss.Color("255")).
        MarginBottom(2)

    instructionStyle := lipgloss.NewStyle().
        Foreground(lipgloss.Color("240")).
        Italic(true)

    title := titleStyle.Render(icon + " " + m.title)
    content := contentStyle.Render(m.content)
    instruction := instructionStyle.Render("Press Enter to " + m.getInstructionText() + ", ESC to close")

    modal := lipgloss.JoinVertical(
        lipgloss.Center,
        title,
        content,
        instruction,
    )

    return lipgloss.Place(
        80, 24,
        lipgloss.Center, lipgloss.Center,
        lipgloss.NewStyle().
            Border(lipgloss.RoundedBorder()).
            BorderForeground(borderColor).
            Padding(2, 4).
            Render(modal),
        lipgloss.WithWhitespaceChars(" "),
        lipgloss.WithWhitespaceForeground(lipgloss.Color("0")),
    )
}

func (m ModalModel) getInstructionText() string {
    switch m.type {
    case ModalConfirmation:
        return "confirm"
    default:
        return "close"
    }
}
```

These integration patterns provide sophisticated approaches to building complex BubbleTea applications with multiple components, state management, and advanced user interactions. They demonstrate how to create maintainable, scalable terminal user interfaces that handle real-world application complexity.