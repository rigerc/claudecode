# Pond Library Complete Guide

This guide provides comprehensive documentation for the Pond Go worker pool library.

## Installation

```bash
go get -u github.com/alitto/pond/v2
```

## Core API Reference

### Pool Creation

#### Basic Pool
```go
pool := pond.NewPool(10) // 10 max concurrent workers
```

#### Pool with Bounded Queue
```go
pool := pond.NewPool(1, pond.WithQueueSize(10))
```

#### Pool with Custom Context
```go
customCtx, cancel := context.WithCancel(context.Background())
pool := pond.NewPool(10, pond.WithContext(customCtx))
```

#### Non-blocking Pool
```go
pool := pond.NewPool(1, pond.WithQueueSize(10), pond.WithNonBlocking(true))
```

### Task Submission Patterns

#### Fire-and-forget Tasks
```go
pool.Submit(func() {
    fmt.Println("Running task")
})
```

#### Tasks with Error Handling
```go
task := pool.SubmitErr(func() error {
    return errors.New("An error occurred")
})

err := task.Wait()
```

#### Tasks with Results
```go
pool := pond.NewResultPool[string](10)
task := pool.Submit(func() string {
    return "Hello, World!"
})

result, err := task.Wait()
```

#### Tasks with Context
```go
ctx, cancel := context.WithCancel(context.Background())
task := pool.SubmitErr(func() error {
    return doSomethingWithCtx(ctx)
})

err := task.Wait()
```

#### Non-blocking Submission
```go
task, ok := pool.TrySubmit(func() {
    // Do some work
})

if !ok {
    fmt.Println("Queue full")
}
```

### Task Groups

#### Basic Task Group
```go
group := pool.NewGroup()

for i := 0; i < 20; i++ {
    i := i
    group.Submit(func() {
        fmt.Printf("Task #%d\n", i)
    })
}

err := group.Wait()
```

#### Task Group with Context
```go
timeout, _ := context.WithTimeout(context.Background(), 5*time.Second)
group := pool.NewGroupContext(timeout)

// Submit tasks...
err := group.Wait() // Waits for completion or timeout
```

#### Task Group with Results
```go
pool := pond.NewResultPool[string](10)
group := pool.NewGroup()

for i := 0; i < 20; i++ {
    i := i
    group.Submit(func() string {
        return fmt.Sprintf("Task #%d", i)
    })
}

results, err := group.Wait()
```

### Pool Management

#### Dynamic Resizing
```go
pool := pond.NewPool(5)
pool.Resize(10) // Increase workers
pool.Resize(5)  // Decrease workers
```

#### Graceful Shutdown
```go
pool.StopAndWait()

// Or separate stop and wait
pool.Stop().Wait()

// Or with timeout
select {
case <-pool.Stop().Done():
    // Pool stopped
case <-time.After(30 * time.Second):
    // Timeout
}
```

### Metrics and Monitoring
```go
pool.RunningWorkers()    // Current running workers
pool.SubmittedTasks()    // Total tasks submitted
pool.WaitingTasks()      // Current tasks in queue
pool.SuccessfulTasks()   // Total successful tasks
pool.FailedTasks()       // Total tasks that panicked
pool.CompletedTasks()    // Total completed tasks
pool.DroppedTasks()      // Total dropped tasks
```

### Subpools
```go
pool := pond.NewPool(10)
subpool := pool.NewSubpool(5)

subpool.Submit(func() {
    fmt.Println("Subpool task")
})

subpool.StopAndWait()
```

### Panic Handling
```go
task := pool.Submit(func() {
    panic("Something went wrong")
})

err := task.Wait()
// err contains the panic information
```

### Default Pool
```go
err := pond.SubmitErr(func() error {
    fmt.Println("Default pool task")
    return nil
}).Wait()
```

## Migration from v1 to v2

### Import Path
```go
// Old: import "github.com/alitto/pond"
// New: import "github.com/alitto/pond/v2"
```

### Pool Initialization
```go
// Old: pond.New(100, 1000)
// New: pond.NewPool(100)
```

### Method Names
```go
// Old: pool.Group(), pool.GroupContext()
// New: pool.NewGroup(), pool.NewGroupContext()
```

### Options
```go
// Old: pond.Context(customCtx)
// New: pond.WithContext(customCtx)
```

## Best Practices

1. **Pool Size**: Use `runtime.NumCPU()` for CPU-bound tasks, higher values for I/O-bound tasks
2. **Context**: Always use context for long-running tasks
3. **Error Handling**: Check errors from `task.Wait()`
4. **Shutdown**: Always call `StopAndWait()` for graceful shutdown
5. **Monitoring**: Use metrics to monitor pool health