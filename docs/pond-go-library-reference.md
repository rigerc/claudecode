# Pond Go Library Reference Guide

## Overview

Pond is a minimalistic and high-performance Go library for managing concurrent tasks using the worker pool pattern. It provides fine-grained control over goroutine execution and resource usage, allowing developers to build efficient concurrent applications with ease.

## Installation

```bash
go get -u github.com/alitto/pond/v2
```

## Quick Start

```go
package main

import (
    "fmt"
    "github.com/alitto/pond/v2"
)

func main() {
    // Create a pool with limited concurrency
    pool := pond.NewPool(100)

    // Submit 1000 tasks
    for i := 0; i < 1000; i++ {
        i := i
        pool.Submit(func() {
            fmt.Printf("Running task #%d\n", i)
        })
    }

    // Stop the pool and wait for all submitted tasks to complete
    pool.StopAndWait()
}
```

## Core Concepts

### Worker Pool

A worker pool manages a set of goroutines that execute tasks concurrently. Pond provides automatic scaling based on workload, creating workers on demand and removing them when idle.

### Task Submission

Tasks can be submitted to pools in various ways:
- **Fire-and-forget**: Submit without expecting a result
- **Error handling**: Submit and capture any errors
- **Result handling**: Submit and capture returned values
- **Context-aware**: Submit with cancellation support

### Task Groups

Task groups allow you to submit multiple related tasks and wait for all of them to complete, with optional error handling and context cancellation.

## API Reference

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

### Result Pools

Create pools that handle tasks returning specific types:

```go
// Pool for tasks returning strings
pool := pond.NewResultPool[string](10)

// Submit a task that returns a string
task := pool.Submit(func() string {
    return "Hello, World!"
})

result, err := task.Wait()
// result = "Hello, World!" and err = nil
```

### Task Submission

#### Basic Task Submission

```go
pool.Submit(func() {
    fmt.Println("Running task")
})
```

#### Task with Error Handling

```go
task := pool.SubmitErr(func() error {
    return errors.New("An error occurred")
})

err := task.Wait()
```

#### Task with Result and Error

```go
task := pool.SubmitErr(func() (string, error) {
    return "Hello, World!", nil
})

result, err := task.Wait()
```

#### Task with Context

```go
ctx, cancel := context.WithCancel(context.Background())
task := pool.SubmitErr(func() error {
    return doSomethingWithCtx(ctx)
})

err := task.Wait()
```

#### Non-blocking Task Submission

```go
task, ok := pool.TrySubmit(func() {
    // Do some work
})

if !ok {
    fmt.Println("Task submission failed because the queue is full")
}
```

### Default Pool

Use the global default pool for simple cases:

```go
err := pond.SubmitErr(func() error {
    fmt.Println("Running task in default pool")
    return nil
}).Wait()
```

### Task Groups

#### Basic Task Group

```go
group := pool.NewGroup()

for i := 0; i < 20; i++ {
    i := i
    group.Submit(func() {
        fmt.Printf("Running group task #%d\n", i)
    })
}

err := group.Wait()
```

#### Task Group with Context

```go
timeout, _ := context.WithTimeout(context.Background(), 5*time.Second)
group := pool.NewGroupContext(timeout)

for i := 0; i < 20; i++ {
    i := i
    group.Submit(func() {
        fmt.Printf("Running group task #%d\n", i)
    })
}

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
// results = ["Task #0", "Task #1", ..., "Task #19"] and err = nil
```

#### Task Group with Error Handling

```go
group := pool.NewGroup()

for i := 0; i < 20; i++ {
    i := i
    group.SubmitErr(func() error {
        if i == 10 {
            return errors.New("An error occurred")
        }
        fmt.Printf("Running group task #%d\n", i)
        return nil
    })
}

err := group.Wait() // Returns first error encountered
```

### Subpools

Create subpools with a fraction of parent pool's workers:

```go
pool := pond.NewPool(10)
subpool := pool.NewSubpool(5)

subpool.Submit(func() {
    fmt.Println("Running task in subpool")
})

subpool.StopAndWait()
```

### Pool Management

#### Dynamic Resizing

```go
pool := pond.NewPool(5)

// Submit tasks
for i := 0; i < 20; i++ {
    pool.Submit(func() {
        // Do some work
    })
}

// Increase pool size
pool.Resize(10)

// Decrease pool size
pool.Resize(5)
```

#### Graceful Shutdown

```go
// Stop and wait
pool.StopAndWait()

// Or separate stop and wait
pool.Stop().Wait()

// Or use channel for timeout
select {
case <-pool.Stop().Done():
    // Pool has stopped
case <-time.After(30 * time.Second):
    // Timeout occurred
}
```

### Panic Handling

Pond automatically captures panics and returns them as errors:

```go
pool := pond.NewPool(10)

task := pool.Submit(func() {
    panic("A panic occurred")
})

err := task.Wait()
if err != nil {
    fmt.Printf("Failed to run task: %v", err)
}
```

### Metrics and Monitoring

Monitor pool performance with built-in metrics:

```go
pool.RunningWorkers()    // Current number of running workers
pool.SubmittedTasks()    // Total tasks submitted
pool.WaitingTasks()      // Current tasks in queue
pool.SuccessfulTasks()   // Total successful tasks
pool.FailedTasks()       // Total tasks that panicked
pool.CompletedTasks()    // Total completed tasks
pool.DroppedTasks()      // Total dropped tasks (queue full)
```

## Migration from v1 to v2

### Import Path

```go
// Old:
import "github.com/alitto/pond"

// New:
import "github.com/alitto/pond/v2"
```

### Pool Initialization

```go
// Old:
pond.New(100, 1000)

// New:
pond.NewPool(100)
```

### Method Names

```go
// Old:
pool.Group()
pool.GroupContext()

// New:
pool.NewGroup()
pool.NewGroupContext()
```

### Options

```go
// Old:
pond.Context(customCtx)

// New:
pond.WithContext(customCtx)

// Deprecated in v2:
// - pond.MinWorkers (automatic scaling)
// - pond.IdleTimeout (immediate cleanup)
// - pond.PanicHandler (errors returned by Wait())
// - pond.Strategy (automatic scaling)
```

## Best Practices

### 1. Choose Appropriate Pool Size

```go
// For CPU-bound tasks
pool := pond.NewPool(runtime.NumCPU())

// For I/O-bound tasks
pool := pond.NewPool(100) // Higher concurrency
```

### 2. Use Context for Long-running Tasks

```go
ctx, cancel := context.WithTimeout(context.Background(), 30*time.Second)
defer cancel()

task := pool.SubmitErr(func() error {
    return longRunningTask(ctx)
})

err := task.Wait()
```

### 3. Handle Errors Gracefully

```go
for i := 0; i < taskCount; i++ {
    task := pool.SubmitErr(taskFunc)

    go func(t *pond.Task[any]) {
        if err := t.Wait(); err != nil {
            log.Printf("Task failed: %v", err)
        }
    }(task)
}
```

### 4. Use Bounded Queues for Back-pressure

```go
pool := pond.NewPool(10, pond.WithQueueSize(100))
```

### 5. Monitor Pool Health

```go
go func() {
    ticker := time.NewTicker(10 * time.Second)
    defer ticker.Stop()

    for range ticker.C {
        log.Printf("Pool stats - Running: %d, Waiting: %d, Success: %d, Failed: %d",
            pool.RunningWorkers(),
            pool.WaitingTasks(),
            pool.SuccessfulTasks(),
            pool.FailedTasks())
    }
}()
```

## Common Patterns

### MapReduce Pattern

```go
// Map phase
mapPool := pond.NewResultPool[string](10)
mapGroup := mapPool.NewGroup()

for _, item := range items {
    item := item
    mapGroup.Submit(func() string {
        return processItem(item)
    })
}

results, err := mapGroup.Wait()

// Reduce phase
finalResult := reduceResults(results)
```

### Pipeline Pattern

```go
// Stage 1
stage1 := pond.NewResultPool[ProcessedData](10)
// Stage 2
stage2 := pond.NewResultPool[FinalResult](10)

// Connect stages with channels
results := make(chan ProcessedData, 100)

// Submit stage 1 tasks
for _, item := range input {
    item := item
    stage1.Submit(func() ProcessedData {
        result := processStage1(item)
        results <- result
        return result
    })
}

// Submit stage 2 tasks
for i := 0; i < len(input); i++ {
    stage2.Submit(func() FinalResult {
        item := <-results
        return processStage2(item)
    })
}
```

### Worker Pool with Timeout

```go
pool := pond.NewPool(10)
timeout := 5 * time.Second

tasks := make([]*pond.Task[any], 0)

for i := 0; i < 100; i++ {
    task := pool.SubmitErr(func() error {
        ctx, cancel := context.WithTimeout(context.Background(), timeout)
        defer cancel()
        return doWorkWithTimeout(ctx)
    })
    tasks = append(tasks, task)
}

// Wait for all tasks with timeout
done := make(chan struct{})
go func() {
    for _, task := range tasks {
        task.Wait()
    }
    close(done)
}()

select {
case <-done:
    // All tasks completed
case <-time.After(30 * time.Second):
    // Global timeout
}
```

## Performance Considerations

- **Memory Usage**: Each worker consumes stack space. Monitor memory usage with large pools.
- **Context Switching**: Too many workers can cause excessive context switching.
- **Queue Size**: Large queues can consume significant memory for pending tasks.
- **GC Pressure**: Frequent task submission can create garbage collection pressure.

## Troubleshooting

### Tasks Not Executing

Check if pool is stopped or context cancelled:

```go
if pool.RunningWorkers() == 0 {
    log.Println("Pool is stopped")
}
```

### High Memory Usage

Reduce pool size or use bounded queues:

```go
pool := pond.NewPool(50, pond.WithQueueSize(1000))
```

### Task Timeout

Use context with timeout:

```go
ctx, cancel := context.WithTimeout(context.Background(), 30*time.Second)
defer cancel()

task := pool.SubmitErr(func() error {
    return doWork(ctx)
})
```

## References

- [GitHub Repository](https://github.com/alitto/pond)
- [GoDoc](https://pkg.go.dev/github.com/alitto/pond/v2)
- [Examples and Patterns](https://github.com/alitto/pond/tree/main/examples)