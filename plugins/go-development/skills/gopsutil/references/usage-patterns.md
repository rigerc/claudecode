# gopsutil Usage Patterns

## Performance Monitoring Pattern

```go
type SystemMonitor struct {
    interval time.Duration
    metrics  chan Metric
    stop     chan bool
}

type Metric struct {
    Timestamp time.Time
    CPU       float64
    Memory    float64
    Disk      float64
}

func NewSystemMonitor(interval time.Duration) *SystemMonitor {
    return &SystemMonitor{
        interval: interval,
        metrics:  make(chan Metric, 100),
        stop:     make(chan bool),
    }
}

func (sm *SystemMonitor) Start() {
    ticker := time.NewTicker(sm.interval)
    defer ticker.Stop()

    for {
        select {
        case <-ticker.C:
            sm.collectMetrics()
        case <-sm.stop:
            return
        }
    }
}

func (sm *SystemMonitor) collectMetrics() {
    var metric Metric
    metric.Timestamp = time.Now()

    if cpuPercent, err := cpu.Percent(time.Second, false); err == nil {
        metric.CPU = cpuPercent[0]
    }

    if vmem, err := mem.VirtualMemory(); err == nil {
        metric.Memory = vmem.UsedPercent
    }

    if usage, err := disk.Usage("/"); err == nil {
        metric.Disk = usage.UsedPercent
    }

    sm.metrics <- metric
}

func (sm *SystemMonitor) Stop() {
    close(sm.stop)
}
```

## Process Discovery Pattern

```go
type ProcessFilter struct {
    Name       string
    MinCPU     float64
    MinMemory  uint64
    ExactMatch bool
}

func FindProcesses(filter ProcessFilter) ([]*process.Process, error) {
    processes, err := process.Processes()
    if err != nil {
        return nil, err
    }

    var results []*process.Process

    for _, p := range processes {
        if filter.Matches(p) {
            results = append(results, p)
        }
    }

    return results, nil
}

func (f ProcessFilter) Matches(p *process.Process) bool {
    // Check process name
    if f.Name != "" {
        name, err := p.Name()
        if err != nil {
            return false
        }

        if f.ExactMatch {
            if name != f.Name {
                return false
            }
        } else {
            if !strings.Contains(strings.ToLower(name), strings.ToLower(f.Name)) {
                return false
            }
        }
    }

    // Check CPU usage
    if f.MinCPU > 0 {
        cpuPercent, err := p.CPUPercent()
        if err != nil || cpuPercent < f.MinCPU {
            return false
        }
    }

    // Check memory usage
    if f.MinMemory > 0 {
        memInfo, err := p.MemoryInfo()
        if err != nil || memInfo.RSS < f.MinMemory {
            return false
        }
    }

    return true
}
```

## Resource Anomaly Detection

```go
type ResourceAnomalyDetector struct {
    cpuThreshold    float64
    memoryThreshold float64
    diskThreshold   float64
    alertCallback   func(Alert)
}

type Alert struct {
    Type        string
    Metric      float64
    Threshold   float64
    Timestamp   time.Time
    Description string
}

func (rad *ResourceAnomalyDetector) CheckSystem() {
    // Check CPU
    if cpuPercent, err := cpu.Percent(time.Second, false); err == nil {
        if cpuPercent[0] > rad.cpuThreshold {
            rad.alertCallback(Alert{
                Type:        "CPU",
                Metric:      cpuPercent[0],
                Threshold:   rad.cpuThreshold,
                Timestamp:   time.Now(),
                Description: "High CPU usage detected",
            })
        }
    }

    // Check Memory
    if vmem, err := mem.VirtualMemory(); err == nil {
        if vmem.UsedPercent > rad.memoryThreshold {
            rad.alertCallback(Alert{
                Type:        "Memory",
                Metric:      vmem.UsedPercent,
                Threshold:   rad.memoryThreshold,
                Timestamp:   time.Now(),
                Description: "High memory usage detected",
            })
        }
    }

    // Check Disk
    if usage, err := disk.Usage("/"); err == nil {
        if usage.UsedPercent > rad.diskThreshold {
            rad.alertCallback(Alert{
                Type:        "Disk",
                Metric:      usage.UsedPercent,
                Threshold:   rad.diskThreshold,
                Timestamp:   time.Now(),
                Description: "High disk usage detected",
            })
        }
    }
}
```

## Cached Resource Monitoring

```go
type CachedResourceMonitor struct {
    cacheDuration time.Duration
    lastUpdate    time.Time
    cached        *SystemInfo
    mutex         sync.RWMutex
}

type SystemInfo struct {
    CPU       []cpu.InfoStat
    Cores     int
    Host      *host.InfoStat
    updateMu  sync.Mutex
}

func NewCachedResourceMonitor(cacheDuration time.Duration) *CachedResourceMonitor {
    return &CachedResourceMonitor{
        cacheDuration: cacheDuration,
        cached:        &SystemInfo{},
    }
}

func (crm *CachedResourceMonitor) GetCPUInfo() ([]cpu.InfoStat, error) {
    crm.mutex.RLock()
    if time.Since(crm.lastUpdate) < crm.cacheDuration {
        defer crm.mutex.RUnlock()
        return crm.cached.CPU, nil
    }
    crm.mutex.RUnlock()

    crm.mutex.Lock()
    defer crm.mutex.Unlock()

    // Double-check after acquiring write lock
    if time.Since(crm.lastUpdate) < crm.cacheDuration {
        return crm.cached.CPU, nil
    }

    cpuInfo, err := cpu.Info()
    if err != nil {
        return nil, err
    }

    cores, err := cpu.Counts(true)
    if err != nil {
        return nil, err
    }

    hostInfo, err := host.Info()
    if err != nil {
        return nil, err
    }

    crm.cached.CPU = cpuInfo
    crm.cached.Cores = cores
    crm.cached.Host = hostInfo
    crm.lastUpdate = time.Now()

    return crm.cached.CPU, nil
}

func (crm *CachedResourceMonitor) GetHostInfo() (*host.InfoStat, error) {
    if _, err := crm.GetCPUInfo(); err != nil {
        return nil, err
    }
    crm.mutex.RLock()
    defer crm.mutex.RUnlock()
    return crm.cached.Host, nil
}
```

## Platform Abstraction Pattern

```go
type SystemMonitor interface {
    GetCPUUsage() (float64, error)
    GetMemoryUsage() (float64, error)
    GetLoadAverage() (*LoadAverage, error)
}

type LinuxMonitor struct{}

func (lm *LinuxMonitor) GetCPUUsage() (float64, error) {
    cpuPercent, err := cpu.Percent(time.Second, false)
    if err != nil {
        return 0, err
    }
    return cpuPercent[0], nil
}

func (lm *LinuxMonitor) GetMemoryUsage() (float64, error) {
    vmem, err := mem.VirtualMemory()
    if err != nil {
        return 0, err
    }
    return vmem.UsedPercent, nil
}

func (lm *LinuxMonitor) GetLoadAverage() (*LoadAverage, error) {
    load, err := load.Avg()
    if err != nil {
        return nil, err
    }
    return &LoadAverage{
        Load1:  load.Load1,
        Load5:  load.Load5,
        Load15: load.Load15,
    }, nil
}

type WindowsMonitor struct{}

func (wm *WindowsMonitor) GetCPUUsage() (float64, error) {
    cpuPercent, err := cpu.Percent(time.Second, false)
    if err != nil {
        return 0, err
    }
    return cpuPercent[0], nil
}

func (wm *WindowsMonitor) GetMemoryUsage() (float64, error) {
    vmem, err := mem.VirtualMemory()
    if err != nil {
        return 0, err
    }
    return vmem.UsedPercent, nil
}

func (wm *WindowsMonitor) GetLoadAverage() (*LoadAverage, error) {
    // Windows doesn't have load averages
    return &LoadAverage{}, nil
}

type LoadAverage struct {
    Load1, Load5, Load15 float64
}

func GetSystemMonitor() SystemMonitor {
    switch runtime.GOOS {
    case "linux":
        return &LinuxMonitor{}
    case "windows":
        return &WindowsMonitor{}
    default:
        return &LinuxMonitor{} // Default to Linux for other Unix-like systems
    }
}
```

## Error Handling Pattern

```go
type SafeResourceMonitor struct {
    defaultCPU     float64
    defaultMemory  float64
    errorCallback  func(error)
}

func (srm *SafeResourceMonitor) GetSafeCPUUsage() float64 {
    if cpuPercent, err := cpu.Percent(time.Second, false); err == nil {
        return cpuPercent[0]
    } else {
        srm.errorCallback(fmt.Errorf("failed to get CPU usage: %w", err))
        return srm.defaultCPU
    }
}

func (srm *SafeResourceMonitor) GetSafeMemoryUsage() float64 {
    if vmem, err := mem.VirtualMemory(); err == nil {
        return vmem.UsedPercent
    } else {
        srm.errorCallback(fmt.Errorf("failed to get memory usage: %w", err))
        return srm.defaultMemory
    }
}

func (srm *SafeResourceMonitor) GetProcessesSafely() []*process.Process {
    processes, err := process.Processes()
    if err != nil {
        srm.errorCallback(fmt.Errorf("failed to get processes: %w", err))
        return nil
    }
    return processes
}
```

## Background Monitoring Pattern

```go
type BackgroundMonitor struct {
    interval       time.Duration
    metrics        map[string]float64
    callbacks      map[string]func(float64)
    stopChan       chan struct{}
    metricsMutex   sync.RWMutex
    callbacksMutex sync.RWMutex
}

func NewBackgroundMonitor(interval time.Duration) *BackgroundMonitor {
    return &BackgroundMonitor{
        interval:  interval,
        metrics:   make(map[string]float64),
        callbacks: make(map[string]func(float64)),
        stopChan:  make(chan struct{}),
    }
}

func (bm *BackgroundMonitor) AddCallback(name string, callback func(float64)) {
    bm.callbacksMutex.Lock()
    defer bm.callbacksMutex.Unlock()
    bm.callbacks[name] = callback
}

func (bm *BackgroundMonitor) GetMetric(name string) (float64, bool) {
    bm.metricsMutex.RLock()
    defer bm.metricsMutex.RUnlock()
    value, exists := bm.metrics[name]
    return value, exists
}

func (bm *BackgroundMonitor) Start() {
    ticker := time.NewTicker(bm.interval)
    defer ticker.Stop()

    for {
        select {
        case <-ticker.C:
            bm.collectMetrics()
        case <-bm.stopChan:
            return
        }
    }
}

func (bm *BackgroundMonitor) Stop() {
    close(bm.stopChan)
}

func (bm *BackgroundMonitor) collectMetrics() {
    // Collect CPU
    if cpuPercent, err := cpu.Percent(time.Second, false); err == nil {
        bm.setMetric("cpu", cpuPercent[0])
    }

    // Collect Memory
    if vmem, err := mem.VirtualMemory(); err == nil {
        bm.setMetric("memory", vmem.UsedPercent)
    }

    // Collect Load Average (Linux only)
    if runtime.GOOS == "linux" {
        if load, err := load.Avg(); err == nil {
            bm.setMetric("load1", load.Load1)
            bm.setMetric("load5", load.Load5)
            bm.setMetric("load15", load.Load15)
        }
    }
}

func (bm *BackgroundMonitor) setMetric(name string, value float64) {
    bm.metricsMutex.Lock()
    bm.metrics[name] = value
    bm.metricsMutex.Unlock()

    // Notify callbacks
    bm.callbacksMutex.RLock()
    if callback, exists := bm.callbacks[name]; exists {
        go callback(value)
    }
    bm.callbacksMutex.RUnlock()
}
```