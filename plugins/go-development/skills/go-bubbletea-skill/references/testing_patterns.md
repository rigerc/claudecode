# BubbleTea Testing Patterns

This comprehensive guide covers testing strategies, patterns, and best practices for BubbleTea applications and components.

## Testing Fundamentals

### Unit Testing Components

**Basic Component Test:**

```go
package main

import (
    "testing"
    "github.com/charmbracelet/bubbles/textinput"
    tea "github.com/charmbracelet/bubbletea"
    "github.com/stretchr/testify/assert"
    "github.com/stretchr/testify/require"
)

func TestTextInputComponent(t *testing.T) {
    // Setup
    ti := textinput.New()
    ti.Placeholder = "Enter text..."
    ti.Focus()

    model := Model{
        textInput: ti,
    }

    // Test initial state
    assert.Equal(t, "", model.textInput.Value())
    assert.True(t, model.textInput.Focused())

    // Test character input
    msg := tea.KeyMsg{
        Type:  tea.KeyRunes,
        Runes: []rune("hello"),
    }

    newModel, cmd := model.Update(msg)
    assert.Equal(t, "hello", newModel.textInput.Value())
    assert.Nil(t, cmd) // No command should be returned

    // Test backspace
    backspaceMsg := tea.KeyMsg{Type: tea.KeyBackspace}
    newModel, cmd = newModel.Update(backspaceMsg)
    assert.Equal(t, "hell", newModel.textInput.Value())
    assert.Nil(t, cmd)
}

func TestModelInit(t *testing.T) {
    model := initialModel()
    cmd := model.Init()

    // Should return blink command for text input
    assert.NotNil(t, cmd)
}

func TestModelView(t *testing.T) {
    model := initialModel()
    view := model.View()

    assert.Contains(t, view, "Enter text...")
    assert.NotEmpty(t, view)
}
```

**List Component Testing:**

```go
func TestListComponent(t *testing.T) {
    items := []list.Item{
        &TestItem{id: 1, title: "Item 1"},
        &TestItem{id: 2, title: "Item 2"},
    }

    delegate := list.NewDefaultDelegate()
    l := list.New(items, delegate, 10, 20)

    model := ListModel{
        list: l,
    }

    // Test initial selection
    assert.Equal(t, 0, model.list.Cursor())

    // Test navigation
    downMsg := tea.KeyMsg{Type: tea.KeyDown}
    newModel, cmd := model.Update(downMsg)
    assert.Equal(t, 1, newModel.list.Cursor())
    assert.Nil(t, cmd)

    upMsg := tea.KeyMsg{Type: tea.KeyUp}
    newModel, cmd = newModel.Update(upMsg)
    assert.Equal(t, 0, newModel.list.Cursor())

    // Test selection
    selected := newModel.list.SelectedItem()
    require.NotNil(t, selected)
    assert.Equal(t, "Item 1", selected.Title())
}

type TestItem struct {
    id    int
    title string
}

func (t *TestItem) Title() string       { return t.title }
func (t *TestItem) Description() string { return "" }
func (t *TestItem) FilterValue() string { return t.title }
```

### Table-Driven Tests

```go
func TestTextInputValidation(t *testing.T) {
    tests := []struct {
        name      string
        input     string
        wantValid bool
        wantError string
    }{
        {
            name:      "valid email",
            input:     "test@example.com",
            wantValid: true,
        },
        {
            name:      "missing @",
            input:     "testexample.com",
            wantValid: false,
            wantError: "invalid email format",
        },
        {
            name:      "empty input",
            input:     "",
            wantValid: false,
            wantError: "email is required",
        },
    }

    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            model := initialModel()
            model.textInput.SetValue(tt.input)

            // Test validation
            err := model.textInput.Validate(model.textInput.Value())
            if tt.wantValid {
                assert.NoError(t, err)
            } else {
                assert.Error(t, err)
                assert.Contains(t, err.Error(), tt.wantError)
            }
        })
    }
}
```

## Integration Testing

### Multi-Component Integration Tests

```go
func TestFormSubmission(t *testing.T) {
    model := initialFormModel()

    // Fill name field
    nameInput := tea.KeyMsg{Type: tea.KeyRunes, Runes: []rune("John Doe")}
    model, _ = model.Update(nameInput)

    // Tab to email field
    tabMsg := tea.KeyMsg{Type: tea.KeyTab}
    model, _ = model.Update(tabMsg)

    // Fill email field
    emailInput := tea.KeyMsg{Type: tea.KeyRunes, Runes: []rune("john@example.com")}
    model, _ = model.Update(emailInput)

    // Submit form
    enterMsg := tea.KeyMsg{Type: tea.KeyEnter}
    newModel, cmd := model.Update(enterMsg)

    // Should return quit command on successful submission
    assert.NotNil(t, cmd)
    assert.Equal(t, tea.Quit(), cmd)
}

func TestComponentFocusNavigation(t *testing.T) {
    model := initialMultiComponentModel()

    // Initially focused on text input
    assert.True(t, model.textInput.Focused())
    assert.False(t, model.list.Focused())

    // Tab to switch focus
    tabMsg := tea.KeyMsg{Type: tea.KeyTab}
    model, _ = model.Update(tabMsg)

    assert.False(t, model.textInput.Focused())
    assert.True(t, model.list.Focused())
}
```

### Message Flow Testing

```go
func TestMessageFlow(t *testing.T) {
    model := initialModel()

    // Test custom message handling
    customMsg := CustomDataMsg{Data: "test data"}
    newModel, cmd := model.Update(customMsg)

    assert.Equal(t, "test data", newModel.data)
    assert.Nil(t, cmd)
}

func TestWindowResize(t *testing.T) {
    model := initialModel()

    resizeMsg := tea.WindowSizeMsg{
        Width:  100,
        Height: 50,
    }

    newModel, _ := model.Update(resizeMsg)
    assert.Equal(t, 100, newModel.width)
    assert.Equal(t, 50, newModel.height)
}
```

## Performance Testing

### Benchmarking

```go
func BenchmarkModelUpdate(b *testing.B) {
    model := initialModel()
    msg := tea.KeyMsg{Type: tea.KeyRunes, Runes: []rune("test")}

    b.ResetTimer()
    for i := 0; i < b.N; i++ {
        model.Update(msg)
    }
}

func BenchmarkModelView(b *testing.B) {
    model := initialModel()
    model.textInput.SetValue("benchmark test")

    b.ResetTimer()
    for i := 0; i < b.N; i++ {
        _ = model.View()
    }
}

func BenchmarkLargeList(b *testing.B) {
    // Create list with many items
    items := make([]list.Item, 10000)
    for i := 0; i < 10000; i++ {
        items[i] = &TestItem{id: i, title: fmt.Sprintf("Item %d", i)}
    }

    delegate := list.NewDefaultDelegate()
    l := list.New(items, delegate, 20, 40)

    b.ResetTimer()
    for i := 0; i < b.N; i++ {
        l.View()
    }
}
```

### Memory Testing

```go
func TestMemoryUsage(t *testing.T) {
    model := initialModel()

    // Get initial memory stats
    var m1 runtime.MemStats
    runtime.ReadMemStats(&m1)

    // Perform many operations
    for i := 0; i < 10000; i++ {
        msg := tea.KeyMsg{Type: tea.KeyRunes, Runes: []rune("test")}
        model, _ = model.Update(msg)
        model.View()
    }

    // Get final memory stats
    var m2 runtime.MemStats
    runtime.ReadMemStats(&m2)

    // Allow some memory growth but not excessive
    memoryGrowth := m2.Alloc - m1.Alloc
    maxAllowedGrowth := uint64(1024 * 1024) // 1MB

    assert.Less(t, memoryGrowth, maxAllowedGrowth,
        "Memory growth should be less than 1MB, was: %d bytes", memoryGrowth)
}
```

## End-to-End Testing

### Application Lifecycle Testing

```go
func TestApplicationLifecycle(t *testing.T) {
    model := initialModel()

    // Test initialization
    cmd := model.Init()
    assert.NotNil(t, cmd)

    // Test normal operation
    msg := tea.KeyMsg{Type: tea.KeyRunes, Runes: []rune("hello")}
    model, cmd = model.Update(msg)
    assert.Equal(t, "hello", model.textInput.Value())

    // Test quit
    quitMsg := tea.KeyMsg{Type: tea.KeyCtrlC}
    newModel, quitCmd := model.Update(quitMsg)
    assert.Equal(t, tea.Quit(), quitCmd)
}
```

### Integration with External Systems

```go
func TestAPIIntegration(t *testing.T) {
    // Mock HTTP server
    server := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        w.Header().Set("Content-Type", "application/json")
        w.WriteHeader(http.StatusOK)
        fmt.Fprint(w, `{"message": "success"}`)
    }))
    defer server.Close()

    model := APICallModel{
        baseURL: server.URL,
    }

    // Simulate API call
    cmd := model.makeAPICall()
    require.NotNil(t, cmd)

    // Execute the command
    p := tea.NewProgram(model)
    p.Start()
}
```

## Test Utilities and Helpers

### Test Helper Functions

```go
// Helper to create test key messages
func testKey(keyType tea.KeyType, runes ...rune) tea.KeyMsg {
    if len(runes) > 0 {
        return tea.KeyMsg{
            Type:  tea.KeyRunes,
            Runes: runes,
        }
    }
    return tea.KeyMsg{Type: keyType}
}

// Helper to simulate typing text
func typeText(model Model, text string) Model {
    for _, r := range text {
        msg := testKey(tea.KeyRunes, r)
        model, _ = model.Update(msg)
    }
    return model
}

// Helper to simulate component navigation
func navigateToComponent(model MultiComponentModel, target int) MultiComponentModel {
    for model.activeComponent != target {
        tabMsg := testKey(tea.KeyTab)
        model, _ = model.Update(tabMsg)
    }
    return model
}

// Assertion helpers
func assertNoError(t *testing.T, err error) {
    t.Helper()
    assert.NoError(t, err)
}

func assertEqual(t *testing.T, expected, actual interface{}) {
    t.Helper()
    assert.Equal(t, expected, actual)
}

func assertContains(t *testing.T, container, content string) {
    t.Helper()
    assert.Contains(t, container, content)
}
```

### Mock Components

```go
// Mock text input for testing
type MockTextInput struct {
    value   string
    focused bool
}

func NewMockTextInput() MockTextInput {
    return MockTextInput{
        focused: false,
    }
}

func (m MockTextInput) Update(msg tea.Msg) (MockTextInput, tea.Cmd) {
    switch msg := msg.(type) {
    case tea.KeyMsg:
        switch msg.Type {
        case tea.KeyRunes:
            m.value += string(msg.Runes)
        case tea.KeyBackspace:
            if len(m.value) > 0 {
                m.value = m.value[:len(m.value)-1]
            }
        }
    }
    return m, nil
}

func (m MockTextInput) Value() string { return m.value }
func (m MockTextInput) Focus() { m.focused = true }
func (m MockTextInput) Blur() { m.focused = false }
func (m MockTextInput) Focused() bool { return m.focused }

func (m MockTextInput) View() string {
    if m.focused {
        return "[" + m.value + "]"
    }
    return "(" + m.value + ")"
}
```

### Test Fixtures

```go
// Common test data
func createTestItems(count int) []list.Item {
    items := make([]list.Item, count)
    for i := 0; i < count; i++ {
        items[i] = &TestItem{
            id:    i,
            title: fmt.Sprintf("Test Item %d", i),
        }
    }
    return items
}

func createTestModel() Model {
    ti := textinput.New()
    ti.SetValue("test value")

    items := createTestItems(5)
    delegate := list.NewDefaultDelegate()
    l := list.New(items, delegate, 10, 20)

    return Model{
        textInput: ti,
        list:      l,
    }
}
```

## Property-Based Testing

```go
import "github.com/leanovate/gopter"

func TestTextInputProperties(t *testing.T) {
    properties := gopter.NewProperties(nil)

    // Property: Text input should maintain input order
    properties.Property("input order preserved", gopter.ForAll(
        func(input string) bool {
            model := initialModel()
            model = typeText(model, input)
            return model.textInput.Value() == input
        },
        gopter.GenAlphaString(),
    ))

    // Property: Backspace should remove last character
    properties.Property("backspace removes last", gopter.ForAll(
        func(input string) bool {
            if len(input) == 0 {
                return true
            }

            model := initialModel()
            model = typeText(model, input)

            backspace := testKey(tea.KeyBackspace)
            model, _ = model.Update(backspace)

            return model.textInput.Value() == input[:len(input)-1]
        },
        gopter.GenAlphaString(),
    ))

    properties.TestingRun(t)
}
```

## Test Configuration

### Test Setup

```go
func TestMain(m *testing.M) {
    // Setup test environment
    lipgloss.SetColorProfile(lipgloss.TrueColor)

    // Run tests
    code := m.Run()

    // Cleanup
    os.Exit(code)
}
```

### Test Flags

```go
var (
    verbose     = flag.Bool("verbose", false, "Enable verbose test output")
    longRunning = flag.Bool("long", false, "Run long-running tests")
)

func init() {
    flag.Parse()
}

func TestLongRunningFeature(t *testing.T) {
    if !*longRunning {
        t.Skip("Skipping long-running test. Use -long flag to run.")
    }

    // Long-running test logic
}
```

## Coverage and Quality

### Coverage Analysis

```go
// Test to ensure all message types are handled
func TestMessageCoverage(t *testing.T) {
    model := initialModel()

    // Test all possible message types
    messageTypes := []tea.Msg{
        tea.KeyMsg{Type: tea.KeyEnter},
        tea.KeyMsg{Type: tea.KeyCtrlC},
        tea.KeyMsg{Type: tea.KeyRunes, Runes: []rune("test")},
        tea.MouseMsg{},
        tea.WindowSizeMsg{Width: 80, Height: 24},
        CustomDataMsg{Data: "test"},
    }

    for _, msg := range messageTypes {
        assert.NotPanics(t, func() {
            model.Update(msg)
        }, "Should not panic when handling message type: %T", msg)
    }
}
```

### Regression Testing

```go
func TestRegressionCases(t *testing.T) {
    tests := []struct {
        name     string
        setup    func() Model
        messages []tea.Msg
        want     func(Model) bool
    }{
        {
            name: "issue #123: text input cursor out of bounds",
            setup: func() Model {
                m := initialModel()
                m.textInput.SetValue("test")
                return m
            },
            messages: []tea.Msg{
                tea.KeyMsg{Type: tea.KeyHome},
                tea.KeyMsg{Type: tea.KeyLeft}, // Should not go negative
            },
            want: func(m Model) bool {
                return m.textInput.Cursor() >= 0
            },
        },
    }

    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            model := tt.setup()

            for _, msg := range tt.messages {
                model, _ = model.Update(msg)
            }

            assert.True(t, tt.want(model), "Regression test failed: %s", tt.name)
        })
    }
}
```

## Continuous Integration

### GitHub Actions Test Configuration

```yaml
# .github/workflows/test.yml
name: Test

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest

    strategy:
      matrix:
        go-version: [1.19, 1.20, 1.21]

    steps:
    - uses: actions/checkout@v3

    - name: Set up Go
      uses: actions/setup-go@v3
      with:
        go-version: ${{ matrix.go-version }}

    - name: Cache dependencies
      uses: actions/cache@v3
      with:
        path: ~/go/pkg/mod
        key: ${{ runner.os }}-go-${{ matrix.go-version }}-${{ hashFiles('**/go.sum') }}

    - name: Install dependencies
      run: go mod download

    - name: Run tests
      run: go test -v -race -coverprofile=coverage.out ./...

    - name: Upload coverage
      uses: codecov/codecov-action@v3
      with:
        file: ./coverage.out

    - name: Run benchmarks
      run: go test -bench=. -benchmem ./...
```

This comprehensive testing guide provides patterns and strategies for ensuring BubbleTea applications are reliable, performant, and maintainable through effective testing practices.