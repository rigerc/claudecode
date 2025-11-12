# Bubbles Component Integration Patterns

This guide covers advanced patterns and best practices for integrating Bubbles components into BubbleTea applications, including component composition, state management, and complex user interactions.

## Component Architecture Patterns

### Single Component Model

```go
type Model struct {
    textInput textinput.Model
    // Application state
    value     string
    error     string
}

func initialModel() Model {
    ti := textinput.New()
    ti.Placeholder = "Enter text..."
    ti.Focus()

    return Model{
        textInput: ti,
    }
}

func (m Model) Update(msg tea.Msg) (tea.Model, tea.Cmd) {
    var cmd tea.Cmd

    // Always update the component first
    m.textInput, cmd = m.textInput.Update(msg)

    // Then handle component messages
    switch msg := msg.(type) {
    case textinput.BlurMsg:
        // Handle text input blur
        m.value = m.textInput.Value()

    case tea.KeyMsg:
        if msg.String() == "enter" {
            m.error = ""
            if err := validateInput(m.value); err != nil {
                m.error = err.Error()
            }
        }
    }

    return m, cmd
}
```

### Multi-Component Model

```go
type Model struct {
    textInput textinput.Model
    list      list.Model
    table     table.Model
    active    int // Track which component is focused
}

func initialModel() Model {
    // Initialize text input
    ti := textinput.New()
    ti.Placeholder = "Search..."
    ti.Focus()

    // Initialize list
    items := []list.Item{
        &TestItem{title: "Item 1"},
        &TestItem{title: "Item 2"},
    }
    l := list.New(items, list.NewDefaultDelegate(), 0, 0)

    // Initialize table
    t := table.New(
        table.WithColumns([]table.Column{
            {Title: "ID", Width: 10},
            {Title: "Name", Width: 20},
        }),
        table.WithFocused(false),
    )

    return Model{
        textInput: ti,
        list:      l,
        table:     t,
        active:    0, // Start with text input focused
    }
}

func (m Model) Update(msg tea.Msg) (tea.Model, tea.Cmd) {
    var cmd tea.Cmd

    // Handle component switching
    switch msg := msg.(type) {
    case tea.KeyMsg:
        switch msg.String() {
        case "tab":
            return m, m.cycleFocus()
        case "enter":
            return m, m.handleActiveComponentAction()
        }
    }

    // Update only the active component
    switch m.active {
    case 0:
        m.textInput, cmd = m.textInput.Update(msg)
    case 1:
        m.list, cmd = m.list.Update(msg)
    case 2:
        m.table, cmd = m.table.Update(msg)
    }

    return m, cmd
}

func (m Model) cycleFocus() tea.Cmd {
    // Blur current component
    switch m.active {
    case 0:
        m.textInput.Blur()
    case 1:
        m.list.Blur()
    case 2:
        m.table.Blur()
    }

    // Focus next component
    m.active = (m.active + 1) % 3

    switch m.active {
    case 0:
        m.textInput.Focus()
    case 1:
        m.list.Focus()
    case 2:
        m.table.Focus()
    }

    return nil
}
```

### Component Container Pattern

```go
type Component interface {
    tea.Model
    Focus()
    Blur()
    Focused() bool
}

type ComponentContainer struct {
    components []Component
    active     int
    styles     ContainerStyles
}

type ContainerStyles struct {
    Focused   lipgloss.Style
    Inactive  lipgloss.Style
    Border    lipgloss.Style
}

func (cc *ComponentContainer) AddComponent(c Component) {
    cc.components = append(cc.components, c)
}

func (cc *ComponentContainer) Update(msg tea.Msg) (tea.Model, tea.Cmd) {
    var cmd tea.Cmd

    // Handle navigation
    switch msg := msg.(type) {
    case tea.KeyMsg:
        switch msg.String() {
        case "tab":
            return cc.cycleFocus()
        }
    }

    // Update active component
    if cc.active < len(cc.components) {
        activeComponent := cc.components[cc.active]
        newComponent, componentCmd := activeComponent.Update(msg)
        cc.components[cc.active] = newComponent
        cmd = tea.Batch(cmd, componentCmd)
    }

    return cc, cmd
}

func (cc *ComponentContainer) cycleFocus() tea.Cmd {
    if cc.active < len(cc.components) {
        cc.components[cc.active].Blur()
    }

    cc.active = (cc.active + 1) % len(cc.components)
    cc.components[cc.active].Focus()

    return nil
}
```

## State Management Patterns

### State Machine Pattern

```go
type AppState int

const (
    StateLoading AppState = iota
    StateEditing
    StateViewing
    StateError
)

type Model struct {
    state    AppState
    input    textinput.Model
    table    table.Model
    error    string
}

func (m Model) Update(msg tea.Msg) (tea.Model, tea.Cmd) {
    switch m.state {
    case StateLoading:
        return m.updateLoading(msg)
    case StateEditing:
        return m.updateEditing(msg)
    case StateViewing:
        return m.updateViewing(msg)
    case StateError:
        return m.updateError(msg)
    }
    return m, nil
}

func (m Model) updateLoading(msg tea.Msg) (tea.Model, tea.Cmd) {
    switch msg := msg.(type) {
    case DataLoadedMsg:
        if msg.Error != nil {
            m.state = StateError
            m.error = msg.Error.Error()
        } else {
            m.state = StateViewing
            m.updateTable(msg.Data)
        }
    }
    return m, nil
}
```

### State Manager Pattern

```go
type StateManager struct {
    state map[string]interface{}
    mutex sync.RWMutex
}

func NewStateManager() *StateManager {
    return &StateManager{
        state: make(map[string]interface{}),
    }
}

func (sm *StateManager) Set(key string, value interface{}) {
    sm.mutex.Lock()
    defer sm.mutex.Unlock()
    sm.state[key] = value
}

func (sm *StateManager) Get(key string) (interface{}, bool) {
    sm.mutex.RLock()
    defer sm.mutex.RUnlock()
    value, exists := sm.state[key]
    return value, exists
}

// Usage in model
type Model struct {
    stateMgr *StateManager
}

func (m Model) Update(msg tea.Msg) (tea.Model, tea.Cmd) {
    switch msg := msg.(type) {
    case UserDataLoadedMsg:
        m.stateMgr.Set("user", msg.User)
        m.stateMgr.Set("loading", false)
    }
    return m, nil
}
```

### Redux-like Pattern

```go
type Action interface {
    Type() string
    Payload() interface{}
}

type Reducer func(state State, action Action) State

type State struct {
    User    *User
    Loading bool
    Error   string
}

func userReducer(state State, action Action) State {
    switch action.Type() {
    case "USER_LOADED":
        return State{
            User:    action.Payload().(*User),
            Loading: false,
        }
    case "USER_ERROR":
        return State{
            Error:   action.Payload().(string),
            Loading: false,
        }
    }
    return state
}

type Model struct {
    state    State
    reducer  Reducer
    dispatch func(Action)
}

func (m Model) Update(msg tea.Msg) (tea.Model, tea.Cmd) {
    switch msg := msg.(type) {
    case Action:
        m.state = m.reducer(m.state, msg)
    }
    return m, nil
}
```

## Communication Patterns

### Message Bus Pattern

```go
type EventBus struct {
    subscribers map[string][]chan tea.Msg
    mutex       sync.RWMutex
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

// Usage in components
type ComponentA struct {
    eventBus *EventBus
}

func (c ComponentA) Update(msg tea.Msg) (ComponentA, tea.Cmd) {
    switch msg := msg.(type) {
    case tea.KeyMsg:
        if msg.String() == "enter" {
            c.eventBus.Publish("data-submitted", DataSubmittedMsg{
                Data: c.getValue(),
            })
        }
    }
    return c, nil
}
```

### Component Communication

```go
type ComponentEventMsg struct {
    Source    string
    Target    string
    EventType string
    Data      interface{}
}

type Model struct {
    textInput textinput.Model
    list      list.Model
    eventChan chan ComponentEventMsg
}

func (m Model) Update(msg tea.Msg) (tea.Model, tea.Cmd) {
    // Handle component events
    if event, ok := msg.(ComponentEventMsg); ok {
        return m.handleComponentEvent(event)
    }

    // Update components and check for events
    oldTextValue := m.textInput.Value()
    m.textInput, _ = m.textInput.Update(msg)
    newTextValue := m.textInput.Value()

    if oldTextValue != newTextValue {
        return m, tea.Batch(
            func() tea.Msg {
                return ComponentEventMsg{
                    Source:    "textinput",
                    Target:    "list",
                    EventType: "filter-changed",
                    Data:      newTextValue,
                }
            },
        )
    }

    return m, nil
}

func (m Model) handleComponentEvent(event ComponentEventMsg) (Model, tea.Cmd) {
    switch event.Target {
    case "list":
        switch event.EventType {
        case "filter-changed":
            m.list.SetFilter(event.Data.(string))
        }
    }
    return m, nil
}
```

## Layout Patterns

### Tab-based Layout

```go
type TabModel struct {
    tabs       []string
    active     int
    components map[string]tea.Model
    styles     TabStyles
}

type TabStyles struct {
    Active     lipgloss.Style
    Inactive   lipgloss.Style
    Border     lipgloss.Style
}

func (m TabModel) Update(msg tea.Msg) (tea.Model, tea.Cmd) {
    var cmd tea.Cmd

    switch msg := msg.(type) {
    case tea.KeyMsg:
        switch msg.String() {
        case "ctrl+right", "tab":
            return m, m.switchTab(1)
        case "ctrl+left", "shift+tab":
            return m, m.switchTab(-1)
        }
    }

    // Update active component
    if activeComponent, ok := m.components[m.tabs[m.active]]; ok {
        newComponent, componentCmd := activeComponent.Update(msg)
        m.components[m.tabs[m.active]] = newComponent
        cmd = tea.Batch(cmd, componentCmd)
    }

    return m, cmd
}

func (m TabModel) switchTab(direction int) tea.Cmd {
    m.active = (m.active + direction + len(m.tabs)) % len(m.tabs)
    return nil
}

func (m TabModel) View() string {
    // Render tab headers
    var tabs strings.Builder
    for i, tab := range m.tabs {
        style := m.styles.Inactive
        if i == m.active {
            style = m.styles.Active
        }
        tabs.WriteString(style.Render(tab))
    }

    // Render active content
    var content string
    if activeComponent, ok := m.components[m.tabs[m.active]]; ok {
        content = activeComponent.View()
    }

    return lipgloss.JoinVertical(
        lipgloss.Left,
        tabs.String(),
        m.styles.Border.Render(content),
    )
}
```

### Split-screen Layout

```go
type SplitScreenModel struct {
    leftPanel  tea.Model
    rightPanel tea.Model
    ratio      float64 // 0.0-1.0, where 0.5 is equal split
    focused    string
    styles     SplitScreenStyles
}

type SplitScreenStyles struct {
    Border    lipgloss.Style
    Focused   lipgloss.Style
}

func (m SplitScreenModel) Update(msg tea.Msg) (tea.Model, tea.Cmd) {
    var cmd tea.Cmd

    switch msg := msg.(type) {
    case tea.KeyMsg:
        switch msg.String() {
        case "tab":
            // Toggle focus between panels
            if m.focused == "left" {
                m.focused = "right"
            } else {
                m.focused = "left"
            }
            return m, nil
        }
    }

    // Update focused panel
    switch m.focused {
    case "left":
        m.leftPanel, cmd = m.leftPanel.Update(msg)
    case "right":
        m.rightPanel, cmd = m.rightPanel.Update(msg)
    }

    return m, cmd
}

func (m SplitScreenModel) View() string {
    leftWidth := int(float64(m.width) * m.ratio)
    rightWidth := m.width - leftWidth - 1 // -1 for divider

    leftStyle := m.styles.Border
    rightStyle := m.styles.Border

    if m.focused == "left" {
        leftStyle = m.styles.Focused
    } else {
        rightStyle = m.styles.Focused
    }

    leftPanel := leftStyle.
        Width(leftWidth).
        Height(m.height).
        Render(m.leftPanel.View())

    rightPanel := rightStyle.
        Width(rightWidth).
        Height(m.height).
        Render(m.rightPanel.View())

    divider := "│"

    return lipgloss.JoinHorizontal(
        lipgloss.Left,
        leftPanel,
        divider,
        rightPanel,
    )
}
```

### Master-Detail Pattern

```go
type MasterDetailModel struct {
    master     list.Model
    detail     tea.Model
    selectedItem interface{}
    showDetail bool
    ratio      float64
}

func (m MasterDetailModel) Update(msg tea.Msg) (tea.Model, tea.Cmd) {
    var cmd tea.Cmd

    // Update master list
    oldSelection := m.master.SelectedItem()
    m.master, cmd = m.master.Update(msg)
    newSelection := m.master.SelectedItem()

    // Handle selection changes
    if oldSelection != newSelection && newSelection != nil {
        m.selectedItem = newSelection
        m.detail = createDetailModel(newSelection)
        m.showDetail = true
    }

    // Update detail if visible
    if m.showDetail {
        newDetail, detailCmd := m.detail.Update(msg)
        m.detail = newDetail
        cmd = tea.Batch(cmd, detailCmd)
    }

    return m, cmd
}

func (m MasterDetailModel) View() string {
    if m.showDetail {
        masterWidth := int(float64(m.width) * m.ratio)
        detailWidth := m.width - masterWidth - 1

        masterView := lipgloss.NewStyle().
            Width(masterWidth).
            Height(m.height).
            Border(lipgloss.RoundedBorder()).
            Render(m.master.View())

        detailView := lipgloss.NewStyle().
            Width(detailWidth).
            Height(m.height).
            Border(lipgloss.RoundedBorder()).
            Render(m.detail.View())

        return lipgloss.JoinHorizontal(
            lipgloss.Left,
            masterView,
            "│",
            detailView,
        )
    }

    return m.master.View()
}
```

## Advanced Integration Patterns

### Component Factories

```go
type ComponentFactory struct {
    theme Theme
    size  SizeConfig
}

type Theme struct {
    Primary   lipgloss.Color
    Secondary lipgloss.Color
    Success   lipgloss.Color
    Error     lipgloss.Color
}

type SizeConfig struct {
    Width  int
    Height int
}

func (cf *ComponentFactory) CreateTextInput(placeholder string) textinput.Model {
    ti := textinput.New()
    ti.Placeholder = placeholder
    ti.Width = cf.size.Width / 3
    ti.Focus()

    ti.Style = lipgloss.NewStyle().
        Foreground(lipgloss.Color("255")).
        Background(lipgloss.Color("237")).
        Border(lipgloss.NormalBorder()).
        BorderForeground(cf.theme.Primary)

    ti.CursorStyle = lipgloss.NewStyle().
        Background(cf.theme.Secondary)

    return ti
}

func (cf *ComponentFactory) CreateTable(columns []table.Column, rows []table.Row) table.Model {
    t := table.New(
        table.WithColumns(columns),
        table.WithRows(rows),
        table.WithFocused(true),
        table.WithHeight(cf.size.Height/2),
    )

    t.SetStyles(table.Styles{
        Header: lipgloss.NewStyle().
            Bold(true).
            Foreground(lipgloss.Color("255")).
            Background(cf.theme.Primary),

        Cell: lipgloss.NewStyle().
            Foreground(lipgloss.Color("255")),

        Selected: lipgloss.NewStyle().
            Foreground(lipgloss.Color("0")).
            Background(cf.theme.Secondary).
            Bold(true),
    })

    return t
}
```

### Component Decorators

```go
type ComponentDecorator struct {
    component tea.Model
    decorator DecoratorFunc
}

type DecoratorFunc func(string) string

func (cd *ComponentDecorator) Update(msg tea.Msg) (tea.Model, tea.Cmd) {
    newComponent, cmd := cd.component.Update(msg)
    cd.component = newComponent
    return cd, cmd
}

func (cd *ComponentDecorator) View() string {
    if cd.decorator != nil {
        return cd.decorator(cd.component.View())
    }
    return cd.component.View()
}

// Example decorators
func withBorder(borderStyle lipgloss.Style) DecoratorFunc {
    return func(content string) string {
        return borderStyle.Render(content)
    }
}

func withTitle(title string) DecoratorFunc {
    return func(content string) string {
        titleStyle := lipgloss.NewStyle().
            Bold(true).
            MarginBottom(1)
        return titleStyle.Render(title) + "\n" + content
    }
}

func withPadding(top, right, bottom, left int) DecoratorFunc {
    return func(content string) string {
        return lipgloss.NewStyle().
            Padding(top, right, bottom, left).
            Render(content)
    }
}

// Usage
func decorateComponent(component tea.Model) tea.Model {
    return &ComponentDecorator{
        component: component,
        decorator: composeDecorators(
            withBorder(lipgloss.RoundedBorder()),
            withPadding(1, 2, 1, 2),
        ),
    }
}

func composeDecorators(decorators ...DecoratorFunc) DecoratorFunc {
    return func(content string) string {
        for _, decorator := range decorators {
            content = decorator(content)
        }
        return content
    }
}
```

### Component Composition DSL

```go
type Builder struct {
    components []tea.Model
    layout     LayoutFunc
    styles     map[string]lipgloss.Style
}

type LayoutFunc func([]tea.Model) string

func NewBuilder() *Builder {
    return &Builder{
        styles: make(map[string]lipgloss.Style),
    }
}

func (b *Builder) AddComponent(component tea.Model) *Builder {
    b.components = append(b.components, component)
    return b
}

func (b *Builder) WithLayout(layout LayoutFunc) *Builder {
    b.layout = layout
    return b
}

func (b *Builder) WithStyle(name string, style lipgloss.Style) *Builder {
    b.styles[name] = style
    return b
}

func (b *Builder) Build() tea.Model {
    return &CompositeModel{
        components: b.components,
        layout:     b.layout,
        styles:     b.styles,
    }
}

// Layout functions
func HorizontalLayout(components []tea.Model) string {
    var views []string
    for _, component := range components {
        views = append(views, component.View())
    }
    return lipgloss.JoinHorizontal(lipgloss.Left, views...)
}

func VerticalLayout(components []tea.Model) string {
    var views []string
    for _, component := range components {
        views = append(views, component.View())
    }
    return lipgloss.JoinVertical(lipgloss.Left, views...)
}

// Usage
func buildComplexUI() tea.Model {
    return NewBuilder().
        AddComponent(createHeader()).
        AddComponent(createContent()).
        AddComponent(createFooter()).
        WithLayout(VerticalLayout).
        WithStyle("header", lipgloss.NewStyle().Bold(true)).
        Build()
}
```

## Performance Optimization

### Lazy Loading Components

```go
type LazyComponent struct {
    factory    func() tea.Model
    component  tea.Model
    loaded     bool
    loading    bool
}

func NewLazyComponent(factory func() tea.Model) *LazyComponent {
    return &LazyComponent{
        factory: factory,
    }
}

func (lc *LazyComponent) ensureLoaded() {
    if !lc.loaded {
        lc.loading = true
        lc.component = lc.factory()
        lc.loaded = true
        lc.loading = false
    }
}

func (lc *LazyComponent) Update(msg tea.Msg) (tea.Model, tea.Cmd) {
    if lc.loading {
        return lc, nil
    }

    lc.ensureLoaded()
    return lc.component.Update(msg)
}

func (lc *LazyComponent) View() string {
    if lc.loading {
        return "Loading..."
    }

    lc.ensureLoaded()
    return lc.component.View()
}
```

### Component Pooling

```go
type ComponentPool[T tea.Model] struct {
    pool   sync.Pool
    create func() T
}

func NewComponentPool[T tea.Model](create func() T) *ComponentPool[T] {
    return &ComponentPool[T]{
        pool:   sync.Pool{},
        create: create,
    }
}

func (cp *ComponentPool[T]) Get() T {
    if component := cp.pool.Get(); component != nil {
        return component.(T)
    }
    return cp.create()
}

func (cp *ComponentPool[T]) Put(component T) {
    // Reset component state if needed
    cp.pool.Put(component)
}

// Usage
var (
    textInputPool = NewComponentPool(func() textinput.Model {
        ti := textinput.New()
        ti.Placeholder = "Enter text..."
        return ti
    })
)

func getReusableTextInput() textinput.Model {
    ti := textInputPool.Get()
    ti.Focus()
    return ti
}

func returnTextInput(ti textinput.Model) {
    ti.Blur()
    ti.SetValue("")
    textInputPool.Put(ti)
}
```

These integration patterns provide a comprehensive foundation for building complex, maintainable BubbleTea applications using the Bubbles component library. They demonstrate how to structure applications for scalability, performance, and maintainability while leveraging the full power of the component ecosystem.