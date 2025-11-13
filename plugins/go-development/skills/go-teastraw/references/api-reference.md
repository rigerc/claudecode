# Teastraw API Reference

## TestRunner Creation

### NewTestRunner
```go
func NewTestRunner(opts ...Option) (*TestRunner, error)
```
Creates a new TestRunner instance with specified configuration options.

### Configuration Options

#### WithInitialTermSize
```go
func WithInitialTermSize(width, height int) Option
```
Set initial terminal dimensions for the test runner.

#### WithCommand
```go
func WithCommand(cmd *exec.Cmd) Option
```
Specify the command to execute for the TUI application.

#### WithTimeout
```go
func WithTimeout(duration time.Duration) Option
```
Set default timeout for operations.

#### WithEnv
```go
func WithEnv(env []string) Option
```
Set environment variables for the test.

## Screen Operations

### WaitFor
```go
func (r *TestRunner) WaitFor(condition func([]byte) bool, opts ...WaitOption) ([]byte, error)
```
Waits for a condition to be met on the terminal screen.

**Parameters:**
- `condition`: Function that receives screen content and returns true when condition is met
- `opts`: Wait configuration options

### Wait Options

#### WithDuration
```go
func WithDuration(duration time.Duration) WaitOption
```
Set maximum wait time for the condition.

#### WithInterval
```go
func WithInterval(duration time.Duration) WaitOption
```
Set check interval for polling the condition.

### Send
```go
func (r *TestRunner) Send(input []byte) error
```
Sends keyboard input to the running TUI application.

### Screen
```go
func (r *TestRunner) Screen() ([]byte, error)
```
Returns the current terminal screen content.

### Cleanup
```go
func (r *TestRunner) Cleanup() error
```
Cleans up test runner resources and terminates the application.

## Validation Helpers

### RequireEqualSubtest
```go
func RequireEqualSubtest(t *testing.T, screen []byte, testName string)
```
Validates that screen content matches the expected golden file.

**Golden File Format:**
Golden files should be placed in `testdata/` directory with `.golden` extension.

## Special Key Sequences

### Arrow Keys
- Up: `\x1b[A` or `{27, 91, 65}`
- Down: `\x1b[B` or `{27, 91, 66}`
- Right: `\x1b[C` or `{27, 91, 67}`
- Left: `\x1b[D` or `{27, 91, 68}`

### Control Keys
- Ctrl+C: `{3}`
- Ctrl+D: `{4}`
- Ctrl+Z: `{26}`
- Enter: `{13}`
- Tab: `{9}`
- Backspace: `{127}`
- Escape: `{27}`

### Function Keys
- F1: `\x1bOP` or `{27, 79, 80}`
- F2: `\x1bOQ` or `{27, 79, 81}`
- F3: `\x1bOR` or `{27, 79, 82}`