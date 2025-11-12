# BubbleTea Performance Guide

This comprehensive guide covers performance optimization strategies, profiling techniques, and best practices for building high-performance BubbleTea applications.

## Performance Fundamentals

### Understanding the Render Loop

BubbleTea applications follow a render loop pattern:

```go
// Each frame: Message → Update → View → Render
// Performance impact: O(components × complexity)
```

### Key Performance Metrics

1. **Frame Time**: Time taken for one complete render cycle
2. **Memory Usage**: Total memory consumed by the application
3. **CPU Usage**: Processing time per frame
4. **Startup Time**: Time to initialize and display first frame

Target metrics:
- Frame Time: < 16ms (60 FPS) for interactive applications
- Memory: < 50MB for typical TUI applications
- CPU: < 10% per frame on modern hardware

## Component Optimization

### Efficient Text Rendering

```go
// BAD: Recomputing styles every frame
func (m Model) View() string {
    return lipgloss.NewStyle().
        Bold(true).
        Foreground(lipgloss.Color("62")).
        Render("Title")
}

// GOOD: Precompute styles
var titleStyle = lipgloss.NewStyle().
    Bold(true).
    Foreground(lipgloss.Color("62"))

func (m Model) View() string {
    return titleStyle.Render("Title")
}
```

### String Building Optimization

```go
// BAD: String concatenation in loops
func (m Model) renderList() string {
    var result string
    for _, item := range m.items {
        result += item + "\n" // Creates new string each time
    }
    return result
}

// GOOD: Use strings.Builder
func (m Model) renderList() string {
    var builder strings.Builder
    builder.Grow(len(m.items) * 20) // Pre-allocate capacity

    for _, item := range m.items {
        builder.WriteString(item)
        builder.WriteByte('\n')
    }
    return builder.String()
}
```

### Viewport for Large Content

```go
type Model struct {
    viewport viewport.Model
    content  string
}

func initialModel() Model {
    // Load large content (10,000 lines)
    content := generateLargeContent(10000)

    v := viewport.New(80, 24)
    v.SetContent(content)

    return Model{
        viewport: v,
        content:  content,
    }
}

func (m Model) View() string {
    // Only renders visible portion (~24 lines vs 10,000)
    return m.viewport.View()
}

func (m Model) Update(msg tea.Msg) (tea.Model, tea.Cmd) {
    var cmd tea.Cmd
    m.viewport, cmd = m.viewport.Update(msg)
    return m, cmd
}
```

### List Component Optimization

```go
// BAD: Loading all items at once
func loadAllItems() []list.Item {
    items := make([]list.Item, 100000) // 100K items!
    // ... load all items
    return items
}

// GOOD: Paginated loading
const PAGE_SIZE = 100

func loadPage(page int) []list.Item {
    offset := page * PAGE_SIZE
    items := make([]list.Item, PAGE_SIZE)
    // ... load only current page
    return items
}

type Model struct {
    list        list.Model
    currentPage int
    totalPages  int
    isLoading   bool
}

func (m Model) loadMoreItems() tea.Cmd {
    if m.currentPage >= m.totalPages-1 || m.isLoading {
        return nil
    }

    m.isLoading = true
    m.currentPage++

    return func() tea.Msg {
        newItems := loadPage(m.currentPage)
        return ItemsLoadedMsg{items: newItems}
    }
}
```

## Memory Management

### Data Structure Limits

```go
const (
    MAX_LIST_ITEMS    = 1000
    MAX_TABLE_ROWS   = 500
    MAX_HISTORY_SIZE  = 100
    MAX_LOG_ENTRIES   = 500
)

type Model struct {
    items    []Item
    history  []string
    logs     []LogEntry
}

func (m Model) addItem(item Item) (Model, tea.Cmd) {
    // Prevent unbounded growth
    if len(m.items) >= MAX_LIST_ITEMS {
        // Remove oldest items
        m.items = m.items[1:]
    }

    m.items = append(m.items, item)
    return m, nil
}
```

### Resource Cleanup

```go
type Model struct {
    conn   *sql.Conn
    file   *os.File
    timer  *time.Timer
    cache  map[string]interface{}
}

func (m Model) cleanup() {
    if m.conn != nil {
        m.conn.Close()
    }
    if m.file != nil {
        m.file.Close()
    }
    if m.timer != nil {
        m.timer.Stop()
    }
    m.cache = nil // Allow GC
}

func (m Model) Update(msg tea.Msg) (tea.Model, tea.Cmd) {
    switch msg := msg.(type) {
    case tea.QuitMsg:
        m.cleanup()
        return m, tea.Quit
    }
    return m, nil
}
```

### Efficient Caching

```go
type Cache struct {
    items map[string]CacheItem
    mutex sync.RWMutex
    max   int
}

type CacheItem struct {
    Data      interface{}
    ExpiresAt time.Time
    Access    time.Time
}

func NewCache(maxItems int) *Cache {
    return &Cache{
        items: make(map[string]CacheItem),
        max:   maxItems,
    }
}

func (c *Cache) Get(key string) (interface{}, bool) {
    c.mutex.RLock()
    defer c.mutex.RUnlock()

    item, exists := c.items[key]
    if !exists || time.Now().After(item.ExpiresAt) {
        return nil, false
    }

    // Update access time
    item.Access = time.Now()
    c.items[key] = item

    return item.Data, true
}

func (c *Cache) Set(key string, data interface{}, ttl time.Duration) {
    c.mutex.Lock()
    defer c.mutex.Unlock()

    // Remove expired items
    c.cleanup()

    // Evict if over capacity
    if len(c.items) >= c.max {
        c.evictLRU()
    }

    c.items[key] = CacheItem{
        Data:      data,
        ExpiresAt: time.Now().Add(ttl),
        Access:    time.Now(),
    }
}
```

## Rendering Optimization

### FPS Limiting

```go
func main() {
    // Limit to 30 FPS for better performance
    p := tea.NewProgram(
        initialModel(),
        tea.WithFPS(30), // ~33ms per frame
        tea.WithAltScreen(),
    )

    if _, err := p.Run(); err != nil {
        log.Fatal(err)
    }
}
```

### Conditional Rendering

```go
type Model struct {
    visibleContent string
    lastUpdate     time.Time
    updateInterval time.Duration
}

func (m Model) shouldUpdate() bool {
    return time.Since(m.lastUpdate) >= m.updateInterval
}

func (m Model) View() string {
    if !m.shouldUpdate() {
        return m.visibleContent // Return cached content
    }

    // Regenerate content
    content := m.generateContent()
    m.visibleContent = content
    m.lastUpdate = time.Now()

    return content
}
```

### Lazy Loading

```go
type LazyContent struct {
    content string
    loaded  bool
    loader  func() string
}

func NewLazyContent(loader func() string) *LazyContent {
    return &LazyContent{
        loader: loader,
    }
}

func (lc *LazyContent) Content() string {
    if !lc.loaded {
        lc.content = lc.loader()
        lc.loaded = true
    }
    return lc.content
}

// Usage in model
type Model struct {
    heavyContent *LazyContent
}

func initialModel() Model {
    return Model{
        heavyContent: NewLazyContent(func() string {
            // Expensive content generation
            return generateExpensiveContent()
        }),
    }
}

func (m Model) View() string {
    // Only generate when first needed
    return m.heavyContent.Content()
}
```

## Command Optimization

### Batch Operations

```go
// BAD: Multiple separate commands
func (m Model) loadAllData() tea.Cmd {
    return tea.Batch(
        loadUserData(),
        loadConfig(),
        loadPreferences(),
        loadTheme(),
    )
}

// GOOD: Batch related operations
func (m Model) loadAllData() tea.Cmd {
    return func() tea.Msg {
        var wg sync.WaitGroup
        var userData UserData
        var config Config
        var preferences Preferences
        var theme Theme

        var userErr, configErr, prefErr, themeErr error

        // Load concurrently
        wg.Add(4)

        go func() {
            defer wg.Done()
            userData, userErr = loadUserDataFromDB()
        }()

        go func() {
            defer wg.Done()
            config, configErr = loadConfigFromFile()
        }()

        go func() {
            defer wg.Done()
            preferences, prefErr = loadPreferences()
        }()

        go func() {
            defer wg.Done()
            theme, themeErr = loadTheme()
        }()

        wg.Wait()

        // Return combined result
        return DataLoadedMsg{
            UserData:     userData,
            Config:       config,
            Preferences: preferences,
            Theme:        theme,
            Errors:       []error{userErr, configErr, prefErr, themeErr},
        }
    }
}
```

### Debouncing

```go
type Debouncer struct {
    delay    time.Duration
    timer    *time.Timer
    callback func()
    mutex    sync.Mutex
}

func NewDebouncer(delay time.Duration, callback func()) *Debouncer {
    return &Debouncer{
        delay:    delay,
        callback: callback,
    }
}

func (d *Debouncer) Trigger() {
    d.mutex.Lock()
    defer d.mutex.Unlock()

    if d.timer != nil {
        d.timer.Stop()
    }

    d.timer = time.AfterFunc(d.delay, d.callback)
}

// Usage in model
type Model struct {
    debouncer *Debouncer
    filter    string
}

func initialModel() Model {
    return Model{
        debouncer: NewDebouncer(300*time.Millisecond, func() {
            // Send debounced update message
            p.Send(FilterUpdateMsg{})
        }),
    }
}

func (m Model) Update(msg tea.Msg) (tea.Model, tea.Cmd) {
    switch msg := msg.(type) {
    case tea.KeyMsg:
        if msg.Type == tea.KeyRunes {
            m.filter += string(msg.Runes)
            m.debouncer.Trigger() // Debounce filter updates
        }
    }
    return m, nil
}
```

## Profiling and Monitoring

### Performance Monitoring

```go
type PerformanceMonitor struct {
    frameCount    int
    lastFrame     time.Time
    frameTimes    []time.Duration
    maxSamples    int
    totalMemory   uint64
    lastGC        time.Time
}

func NewPerformanceMonitor() *PerformanceMonitor {
    return &PerformanceMonitor{
        frameTimes: make([]time.Duration, 0, 100),
        maxSamples: 100,
    }
}

func (pm *PerformanceMonitor) StartFrame() {
    pm.lastFrame = time.Now()
}

func (pm *PerformanceMonitor) EndFrame() {
    frameTime := time.Since(pm.lastFrame)
    pm.frameCount++

    pm.frameTimes = append(pm.frameTimes, frameTime)
    if len(pm.frameTimes) > pm.maxSamples {
        pm.frameTimes = pm.frameTimes[1:]
    }

    // Log slow frames
    if frameTime > 16*time.Millisecond { // > 60 FPS
        log.Printf("Slow frame: %v", frameTime)
    }

    // Check memory usage every 100 frames
    if pm.frameCount%100 == 0 {
        pm.checkMemory()
    }
}

func (pm *PerformanceMonitor) checkMemory() {
    var m runtime.MemStats
    runtime.ReadMemStats(&m)

    log.Printf("Memory: Alloc=%dKB, TotalAlloc=%dKB, Sys=%dKB",
        m.Alloc/1024, m.TotalAlloc/1024, m.Sys/1024)

    if m.Alloc > pm.totalMemory {
        pm.totalMemory = m.Alloc
    }
}

func (pm *PerformanceMonitor) GetStats() FrameStats {
    if len(pm.frameTimes) == 0 {
        return FrameStats{}
    }

    var total time.Duration
    max := time.Duration(0)
    min := time.Duration(^uint64(0) >> 1) // Max uint64

    for _, ft := range pm.frameTimes {
        total += ft
        if ft > max {
            max = ft
        }
        if ft < min {
            min = ft
        }
    }

    avg := total / time.Duration(len(pm.frameTimes))

    return FrameStats{
        FPS:      1000 / avg.Milliseconds(),
        Avg:      avg,
        Min:      min,
        Max:      max,
        Frames:   pm.frameCount,
    }
}

type FrameStats struct {
    FPS    float64
    Avg    time.Duration
    Min    time.Duration
    Max    time.Duration
    Frames int
}
```

### Benchmarking

```go
func BenchmarkModelUpdate(b *testing.B) {
    model := initialModel()
    msg := tea.KeyMsg{Type: tea.KeyRunes, Runes: []rune("test")}

    b.ResetTimer()
    b.ReportAllocs()

    for i := 0; i < b.N; i++ {
        model.Update(msg)
    }
}

func BenchmarkModelView(b *testing.B) {
    model := initialModel()
    model.textInput.SetValue("benchmark test")

    b.ResetTimer()
    b.ReportAllocs()

    for i := 0; i < b.N; i++ {
        _ = model.View()
    }
}

func BenchmarkLargeListView(b *testing.B) {
    items := make([]list.Item, 10000)
    for i := 0; i < 10000; i++ {
        items[i] = &TestItem{title: fmt.Sprintf("Item %d", i)}
    }

    delegate := list.NewDefaultDelegate()
    l := list.New(items, delegate, 20, 40)

    b.ResetTimer()
    b.ReportAllocs()

    for i := 0; i < b.N; i++ {
        l.View()
    }
}
```

## Advanced Optimization Techniques

### Object Pooling

```go
type ObjectPool[T any] struct {
    pool   sync.Pool
    create func() T
}

func NewObjectPool[T any](create func() T) *ObjectPool[T] {
    return &ObjectPool[T]{
        pool:   sync.Pool{},
        create: create,
    }
}

func (op *ObjectPool[T]) Get() T {
    if obj := op.pool.Get(); obj != nil {
        return obj.(T)
    }
    return op.create()
}

func (op *ObjectPool[T]) Put(obj T) {
    op.pool.Put(obj)
}

// Usage for string builders
var stringBuilderPool = NewObjectPool(func() strings.Builder {
    return strings.Builder{}
})

func fastStringJoin(items []string) string {
    builder := stringBuilderPool.Get()
    defer stringBuilderPool.Put(builder)

    builder.Reset()
    builder.Grow(estimateSize(items))

    for _, item := range items {
        builder.WriteString(item)
    }

    return builder.String()
}
```

### SIMD-Optimized Rendering

```go
import "github.com/klauspost/cpuid/v2"

func optimizedStringRendering(data []string) string {
    if !cpuid.CPU.Supports(cpuid.AVX2) {
        // Fall back to standard rendering
        return strings.Join(data, "\n")
    }

    // Use SIMD-optimized implementation
    // This would require assembly or specialized libraries
    return simdStringJoin(data, "\n")
}
```

### Streaming for Large Datasets

```go
type StreamingListModel struct {
    stream   <-chan Item
    buffer   []Item
    maxSize  int
    active   bool
}

func NewStreamingListModel() *StreamingListModel {
    return &StreamingListModel{
        maxSize: 1000,
        buffer:  make([]Item, 0, 1000),
    }
}

func (s *StreamingListModel) StartStream() tea.Cmd {
    s.active = true
    return func() tea.Msg {
        return StreamStartedMsg{}
    }
}

func (s *StreamingListModel) processStream() tea.Cmd {
    return func() tea.Msg {
        if !s.active {
            return nil
        }

        select {
        case item, ok := <-s.stream:
            if !ok {
                return StreamEndedMsg{}
            }

            s.buffer = append(s.buffer, item)
            if len(s.buffer) > s.maxSize {
                s.buffer = s.buffer[1:] // Remove oldest
            }

            return ItemReceivedMsg{item: item}

        default:
            // No new items, check again soon
            return tea.Tick(100*time.Millisecond, func(t time.Time) tea.Msg {
                return CheckStreamMsg{}
            })
        }
    }
}
```

## Performance Checklist

### Before Optimization

1. **Profile First**: Measure before optimizing
2. **Identify Bottlenecks**: Find the actual performance issues
3. **Set Targets**: Define acceptable performance metrics

### During Development

1. **Limit Data Sizes**: Use pagination and streaming
2. **Reuse Objects**: Use object pools and caching
3. **Avoid Allocations**: Pre-allocate where possible
4. **Batch Operations**: Group related work together

### Before Release

1. **Run Benchmarks**: Ensure performance targets are met
2. **Test on Low-End Hardware**: Verify performance on slower machines
3. **Monitor Memory**: Check for memory leaks
4. **Profile in Production**: Monitor real-world performance

### Common Performance Pitfalls

1. **String Concatenation in Loops**: Use strings.Builder
2. **Unbounded Data Structures**: Implement limits and cleanup
3. **Inefficient Rendering**: Cache computed styles and content
4. **Blocking Operations**: Use commands for long-running tasks
5. **Excessive Logging**: Keep logging minimal in production

This performance guide provides comprehensive strategies for building high-performance BubbleTea applications that can handle complex interactions while maintaining smooth user experience.