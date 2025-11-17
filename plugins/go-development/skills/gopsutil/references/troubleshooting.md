# gopsutil Troubleshooting Guide

## Common Issues and Solutions

### Permission Denied Errors

**Problem**: Getting permission denied errors when accessing system information.

**Symptoms**:
```
permission denied while trying to read /proc/cpuinfo
failed to get process info: permission denied
```

**Solutions**:
1. Run with elevated privileges:
```bash
sudo ./your-app
```

2. Check specific permissions:
```bash
# Check proc filesystem access
ls -la /proc/

# Check process access
ps aux | grep your-process
```

3. Use less privileged alternatives:
```go
// Use cached information instead of real-time
cpuInfo, _ := cpu.Info()
// Instead of frequently calling cpu.Percent()
```

### Platform-Specific Feature Not Available

**Problem**: Functions return errors or empty data on certain platforms.

**Symptoms**:
```
Load averages not available on Windows
Temperature sensors not found on macOS
```

**Solutions**:
1. Check platform compatibility before calling functions:
```go
if runtime.GOOS == "linux" {
    load, err := load.Avg()
    // Handle Linux-specific features
} else if runtime.GOOS == "windows" {
    // Use Windows alternatives
}
```

2. Use platform feature detection:
```go
func getLoadAverage() (float64, error) {
    if runtime.GOOS == "windows" {
        return 0, fmt.Errorf("load averages not available on Windows")
    }
    load, err := load.Avg()
    if err != nil {
        return 0, err
    }
    return load.Load1, nil
}
```

### High Resource Usage

**Problem**: gopsutil calls consuming excessive CPU or memory.

**Symptoms**:
- High CPU usage when monitoring frequently
- Memory leaks in long-running applications
- Slow response times

**Solutions**:
1. Implement caching for expensive operations:
```go
type CachedInfo struct {
    cpuInfo    []cpu.InfoStat
    lastUpdate time.Time
    mutex      sync.RWMutex
}

func (ci *CachedInfo) GetCPUInfo() ([]cpu.InfoStat, error) {
    ci.mutex.RLock()
    if time.Since(ci.lastUpdate) < 30*time.Second {
        defer ci.mutex.RUnlock()
        return ci.cpuInfo, nil
    }
    ci.mutex.RUnlock()

    ci.mutex.Lock()
    defer ci.mutex.Unlock()

    // Refresh cache
    info, err := cpu.Info()
    if err != nil {
        return nil, err
    }

    ci.cpuInfo = info
    ci.lastUpdate = time.Now()
    return ci.cpuInfo, nil
}
```

2. Use appropriate intervals:
```go
// Bad - too frequent
ticker := time.NewTicker(100 * time.Millisecond)

// Good - reasonable interval
ticker := time.NewTicker(5 * time.Second)
```

3. Limit scope of monitoring:
```go
// Monitor only specific metrics instead of everything
func monitorSpecific() {
    // Only monitor critical resources
    vmem, _ := mem.VirtualMemory()
    if vmem.UsedPercent > 80 {
        // Alert or take action
    }
}
```

### Context and Timeout Issues

**Problem**: Functions hanging or not respecting cancellation.

**Symptoms**:
- Application hangs on system calls
- Context cancellation not working
- Long delays in monitoring

**Solutions**:
1. Use context with timeouts:
```go
ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
defer cancel()

v, err := mem.VirtualMemoryWithContext(ctx)
if err == context.DeadlineExceeded {
    log.Println("Operation timed out")
    return
}
```

2. Implement graceful degradation:
```go
func getSystemInfoWithFallback() SystemInfo {
    ctx, cancel := context.WithTimeout(context.Background(), 2*time.Second)
    defer cancel()

    var info SystemInfo

    // Try with context
    if vmem, err := mem.VirtualMemoryWithContext(ctx); err == nil {
        info.MemoryUsage = vmem.UsedPercent
    } else {
        // Fallback to cached or default value
        info.MemoryUsage = 0
        log.Printf("Failed to get memory info: %v", err)
    }

    return info
}
```

### Docker Monitoring Issues

**Problem**: Docker container monitoring not working.

**Symptoms**:
```
failed to get docker id list
docker statistics not available
permission denied accessing docker socket
```

**Solutions**:
1. Check Docker daemon status:
```bash
docker info
docker ps
```

2. Verify Docker socket permissions:
```bash
ls -la /var/run/docker.sock
sudo usermod -aG docker $USER
```

3. Check if running inside container:
```go
func isInContainer() bool {
    if _, err := os.Stat("/.dockerenv"); err == nil {
        return true
    }
    return false
}

func monitorDockerSafely() {
    if !isInContainer() {
        containerIDs, err := docker.GetDockerIDList()
        if err != nil {
            log.Printf("Docker monitoring not available: %v", err)
            return
        }
        // Monitor containers
    }
}
```

### Memory Information Issues

**Problem**: Inconsistent memory information across platforms.

**Symptoms**:
- Different memory metrics on different OS
- Missing fields in memory structs
- Incorrect memory usage calculations

**Solutions**:
1. Use platform-specific memory info:
```go
func getDetailedMemoryInfo() {
    if runtime.GOOS == "windows" {
        ex := mem.NewExWindows()
        v, err := ex.VirtualMemory()
        if err == nil {
            fmt.Printf("Virtual Available: %d\n", v.VirtualAvail)
            fmt.Printf("Virtual Total: %d\n", v.VirtualTotal)
        }
    } else if runtime.GOOS == "linux" {
        ex := mem.NewExLinux()
        v, err := ex.VirtualMemory()
        if err == nil {
            fmt.Printf("Active: %d\n", v.Active)
            fmt.Printf("Inactive: %d\n", v.Inactive)
        }
    }
}
```

2. Handle missing gracefully:
```go
func getMemorySummary() map[string]interface{} {
    summary := make(map[string]interface{})

    vmem, err := mem.VirtualMemory()
    if err != nil {
        log.Printf("Error getting memory info: %v", err)
        return summary
    }

    summary["total"] = vmem.Total
    summary["used"] = vmem.Used
    summary["free"] = vmem.Free

    // Optional fields
    if vmem.Active > 0 {
        summary["active"] = vmem.Active
    }
    if vmem.Inactive > 0 {
        summary["inactive"] = vmem.Inactive
    }

    return summary
}
```

### Process Monitoring Issues

**Problem**: Process enumeration or information retrieval failures.

**Symptoms**:
```
failed to get processes
process not found
access denied reading process information
```

**Solutions**:
1. Handle race conditions:
```go
func safeGetProcess(pid int32) (*process.Process, error) {
    p, err := process.NewProcess(pid)
    if err != nil {
        return nil, err
    }

    // Check if process still exists
    exists, err := process.PidExists(pid)
    if err != nil || !exists {
        return nil, fmt.Errorf("process %d not found", pid)
    }

    return p, nil
}
```

2. Filter by permissions:
```go
func getAccessibleProcesses() ([]*process.Process, error) {
    allProcesses, err := process.Processes()
    if err != nil {
        return nil, err
    }

    var accessible []*process.Process
    for _, p := range allProcesses {
        if _, err := p.Name(); err == nil {
            accessible = append(accessible, p)
        }
    }

    return accessible, nil
}
```

3. Use appropriate process filters:
```go
func getProcessesByUser(username string) ([]*process.Process, error) {
    processes, err := process.Processes()
    if err != nil {
        return nil, err
    }

    var userProcesses []*process.Process
    for _, p := range processes {
        if pUsername, err := p.Username(); err == nil && pUsername == username {
            userProcesses = append(userProcesses, p)
        }
    }

    return userProcesses, nil
}
```

## Debug Mode Implementation

```go
type DebugMonitor struct {
    debug     bool
    logFile   *os.File
    logger    *log.Logger
}

func NewDebugMonitor(debug bool) *DebugMonitor {
    dm := &DebugMonitor{debug: debug}

    if debug {
        logFile, err := os.OpenFile("gopsutil-debug.log", os.O_CREATE|os.O_APPEND|os.O_WRONLY, 0644)
        if err != nil {
            log.Printf("Failed to open debug log: %v", err)
        } else {
            dm.logFile = logFile
            dm.logger = log.New(logFile, "DEBUG: ", log.LstdFlags|log.Lshortfile)
        }
    }

    return dm
}

func (dm *DebugMonitor) DebugLog(format string, v ...interface{}) {
    if dm.debug && dm.logger != nil {
        dm.logger.Printf(format, v...)
    }
}

func (dm *DebugMonitor) GetCPUWithDebug() []float64 {
    start := time.Now()
    dm.DebugLog("Starting CPU measurement")

    cpuPercent, err := cpu.Percent(time.Second, false)
    duration := time.Since(start)

    if err != nil {
        dm.DebugLog("CPU measurement failed: %v", err)
        return nil
    }

    dm.DebugLog("CPU measurement completed in %v: %v", duration, cpuPercent)
    return cpuPercent
}
```

## Health Check Implementation

```go
type HealthChecker struct {
    checks map[string]func() error
}

func NewHealthChecker() *HealthChecker {
    hc := &HealthChecker{
        checks: make(map[string]func() error),
    }

    hc.addDefaultChecks()
    return hc
}

func (hc *HealthChecker) addDefaultChecks() {
    hc.checks["memory"] = func() error {
        _, err := mem.VirtualMemory()
        return err
    }

    hc.checks["cpu"] = func() error {
        _, err := cpu.Percent(time.Second, false)
        return err
    }

    hc.checks["disk"] = func() error {
        _, err := disk.Usage("/")
        return err
    }

    if runtime.GOOS != "windows" {
        hc.checks["load"] = func() error {
            _, err := load.Avg()
            return err
        }
    }
}

func (hc *HealthChecker) CheckAll() map[string]error {
    results := make(map[string]error)

    for name, check := range hc.checks {
        if err := check(); err != nil {
            results[name] = err
        }
    }

    return results
}

func (hc *HealthChecker) IsHealthy() bool {
    results := hc.CheckAll()
    return len(results) == 0
}
```

## Best Practices Summary

1. **Always check errors** - gopsutil functions can fail due to permissions or missing features
2. **Use caching** - Expensive operations like `cpu.Info()` should be cached
3. **Respect platform differences** - Not all features are available everywhere
4. **Implement timeouts** - Use context to prevent hanging calls
5. **Handle gracefully** - Provide fallbacks when features aren't available
6. **Monitor resource usage** - Don't monitor too frequently to avoid performance impact
7. **Use appropriate permissions** - Some operations require elevated privileges
8. **Test on target platforms** - Behavior can vary significantly between OS