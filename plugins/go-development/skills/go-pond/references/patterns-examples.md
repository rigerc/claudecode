# Pond Patterns and Examples

Advanced patterns for using the Pond library in real-world scenarios.

## MapReduce Pattern

Process data in parallel and aggregate results:

```go
func mapReduce(data []Input) Result {
    // Map phase
    mapPool := pond.NewResultPool[ProcessedData](10)
    mapGroup := mapPool.NewGroup()

    for _, item := range data {
        item := item
        mapGroup.Submit(func() ProcessedData {
            return processItem(item)
        })
    }

    results, err := mapGroup.Wait()
    if err != nil {
        log.Fatal(err)
    }

    // Reduce phase
    return reduceResults(results)
}
```

## Pipeline Pattern

Create multi-stage processing pipelines:

```go
func pipelineProcessor(input []RawData) []FinalResult {
    // Stage pools
    stage1 := pond.NewResultPool[ProcessedData](10)
    stage2 := pond.NewResultPool[FinalResult](10)

    // Communication channel
    results := make(chan ProcessedData, 100)

    // Stage 1: Process raw data
    for _, item := range input {
        item := item
        stage1.Submit(func() ProcessedData {
            result := processStage1(item)
            results <- result
            return result
        })
    }

    // Stage 2: Transform processed data
    for i := 0; i < len(input); i++ {
        stage2.Submit(func() FinalResult {
            item := <-results
            return processStage2(item)
        })
    }

    // Wait for stage 2 completion
    var finalResults []FinalResult
    for i := 0; i < len(input); i++ {
        task := stage2.SubmitErr(func() (FinalResult, error) {
            item := <-results
            return processStage2(item), nil
        })

        result, err := task.Wait()
        if err != nil {
            continue
        }
        finalResults = append(finalResults, result)
    }

    return finalResults
}
```

## Timeout Pattern

Handle tasks with timeouts gracefully:

```go
func processWithTimeout(tasks []Task) error {
    pool := pond.NewPool(10)
    taskTimeout := 5 * time.Second
    globalTimeout := 30 * time.Second

    var pondTasks []*pond.Task[any]

    // Submit all tasks with individual timeouts
    for _, task := range tasks {
        task := task
        pondTask := pool.SubmitErr(func() error {
            ctx, cancel := context.WithTimeout(context.Background(), taskTimeout)
            defer cancel()
            return executeTask(ctx, task)
        })
        pondTasks = append(pondTasks, pondTask)
    }

    // Wait for all tasks with global timeout
    done := make(chan struct{})
    go func() {
        for _, task := range pondTasks {
            task.Wait()
        }
        close(done)
    }()

    select {
    case <-done:
        return nil
    case <-time.After(globalTimeout):
        return fmt.Errorf("global timeout exceeded")
    }
}
```

## Worker Pool with Back-pressure

Implement back-pressure to prevent resource exhaustion:

```go
func processWithBackpressure(items []Item) error {
    // Bounded queue creates back-pressure
    pool := pond.NewPool(5, pond.WithQueueSize(20))
    defer pool.StopAndWait()

    resultChan := make(chan Result, len(items))
    errorChan := make(chan error, len(items))

    // Submit items
    for i, item := range items {
        i, item := i, item

        task, ok := pool.TrySubmit(func() {
            result, err := processItem(item)
            if err != nil {
                errorChan <- fmt.Errorf("item %d: %v", i, err)
                return
            }
            resultChan <- result
        })

        if !ok {
            return fmt.Errorf("queue full at item %d", i)
        }
    }

    // Collect results
    var results []Result
    var errors []error

    for i := 0; i < len(items); i++ {
        select {
        case result := <-resultChan:
            results = append(results, result)
        case err := <-errorChan:
            errors = append(errors, err)
        case <-time.After(10 * time.Second):
            return fmt.Errorf("timeout waiting for results")
        }
    }

    if len(errors) > 0 {
        return fmt.Errorf("encountered %d errors: %v", len(errors), errors[0])
    }

    return nil
}
```

## Context-Aware Task Group

Handle cancellation for groups of related tasks:

```go
func processBatchWithCancellation(batch Batch) error {
    pool := pond.NewPool(20)

    // Create context with timeout
    ctx, cancel := context.WithTimeout(context.Background(), 2*time.Minute)
    defer cancel()

    // Create task group with context
    group := pool.NewGroupContext(ctx)

    // Submit tasks
    for _, item := range batch.Items {
        item := item
        group.SubmitErr(func() error {
            return processItemWithContext(ctx, item)
        })
    }

    // Wait for completion or cancellation
    err := group.Wait()
    if err != nil {
        if ctx.Err() == context.DeadlineExceeded {
            return fmt.Errorf("batch processing timed out")
        }
        return fmt.Errorf("batch processing failed: %v", err)
    }

    return nil
}
```

## Dynamic Load Balancing

Adjust pool size based on workload:

```go
func adaptiveProcessing(dataStream <-chan Data) {
    // Start with conservative pool size
    pool := pond.NewPool(5)
    defer pool.StopAndWait()

    ticker := time.NewTicker(10 * time.Second)
    defer ticker.Stop()

    go func() {
        for {
            select {
            case data := <-dataStream:
                pool.Submit(func() {
                    processData(data)
                })
            case <-ticker.C:
                // Adjust pool size based on queue length
                waiting := pool.WaitingTasks()
                if waiting > 50 {
                    // Scale up
                    current := pool.RunningWorkers()
                    if current < 50 {
                        pool.Resize(current + 10)
                    }
                } else if waiting < 5 {
                    // Scale down
                    current := pool.RunningWorkers()
                    if current > 5 {
                        pool.Resize(current - 5)
                    }
                }
            }
        }
    }()
}
```

## Error Collection Pattern

Collect all errors from a group of tasks:

```go
func processWithErrorCollection(items []Item) ([]Result, error) {
    pool := pond.NewPool(10)
    group := pool.NewGroup()

    resultChan := make(chan Result, len(items))
    errorChan := make(chan error, len(items))

    // Submit tasks
    for i, item := range items {
        i, item := i, item
        group.Submit(func() {
            result, err := processItem(item)
            if err != nil {
                errorChan <- fmt.Errorf("item %d: %v", i, err)
                return
            }
            resultChan <- result
        })
    }

    // Wait for completion
    if err := group.Wait(); err != nil {
        return nil, fmt.Errorf("task group failed: %v", err)
    }

    // Close channels
    close(resultChan)
    close(errorChan)

    // Collect results
    var results []Result
    var errors []error

    for result := range resultChan {
        results = append(results, result)
    }

    for err := range errorChan {
        errors = append(errors, err)
    }

    // Return results with aggregated errors if any
    if len(errors) > 0 {
        return results, fmt.Errorf("encountered %d errors, first: %v", len(errors), errors[0])
    }

    return results, nil
}
```

## Resource Pool Pattern

Manage limited resources with Pond:

```go
type ResourcePool struct {
    pool *pond.Pool
    resources chan Resource
}

func NewResourcePool(maxResources, maxConcurrency int) *ResourcePool {
    rp := &ResourcePool{
        pool:      pond.NewPool(maxConcurrency),
        resources: make(chan Resource, maxResources),
    }

    // Initialize resources
    for i := 0; i < maxResources; i++ {
        rp.resources <- createResource(i)
    }

    return rp
}

func (rp *ResourcePool) Execute(task func(Resource) error) error {
    taskResult := rp.pool.SubmitErr(func() error {
        // Acquire resource
        resource := <-rp.resources
        defer func() { rp.resources <- resource }()

        // Execute task with resource
        return task(resource)
    })

    return taskResult.Wait()
}

func (rp *ResourcePool) Close() {
    rp.pool.StopAndWait()
    close(rp.resources)
}
```

## Monitoring and Metrics

Comprehensive pool monitoring:

```go
func monitorPool(pool *pond.Pool) {
    ticker := time.NewTicker(30 * time.Second)
    defer ticker.Stop()

    for {
        select {
        case <-ticker.C:
            stats := PoolStats{
                RunningWorkers: pool.RunningWorkers(),
                SubmittedTasks: pool.SubmittedTasks(),
                WaitingTasks:   pool.WaitingTasks(),
                Successful:     pool.SuccessfulTasks(),
                Failed:         pool.FailedTasks(),
                Completed:      pool.CompletedTasks(),
                Dropped:        pool.DroppedTasks(),
            }

            log.Printf("Pool Stats: %+v", stats)

            // Alert on high failure rate
            if stats.Failed > 0 && stats.Completed > 0 {
                failureRate := float64(stats.Failed) / float64(stats.Completed)
                if failureRate > 0.1 { // 10% failure rate
                    log.Printf("WARNING: High failure rate: %.2f%%", failureRate*100)
                }
            }
        }
    }
}

type PoolStats struct {
    RunningWorkers int64
    SubmittedTasks uint64
    WaitingTasks   uint64
    Successful     uint64
    Failed         uint64
    Completed      uint64
    Dropped        uint64
}
```