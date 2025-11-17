# gopsutil: Comprehensive System Monitoring Library for Go

## Overview

**gopsutil** is a cross-platform library for retrieving process and system utilization information in Go. It provides a simple, idiomatic Go API for accessing system metrics without requiring Cgo, making it ideal for system monitoring, performance analysis, and DevOps applications.

**Key Features:**
- **Cross-platform**: Supports Linux, Windows, macOS, FreeBSD, OpenBSD, Solaris, and AIX
- **No CGO Dependencies**: Pure Go implementation for easy deployment
- **Comprehensive Coverage**: CPU, memory, disk, network, process, and Docker metrics
- **Context Support**: Allows configuration of system paths and cancellation
- **Docker Integration**: Built-in support for container monitoring
- **Production Ready**: Used in major Go projects and monitoring tools

## Installation

### Basic Installation

```bash
go get github.com/shirou/gopsutil/v4
```

### Import Packages

```go
import (
    "github.com/shirou/gopsutil/v4/cpu"
    "github.com/shirou/gopsutil/v4/disk"
    "github.com/shirou/gopsutil/v4/host"
    "github.com/shirou/gopsutil/v4/load"
    "github.com/shirou/gopsutil/v4/mem"
    "github.com/shirou/gopsutil/v4/net"
    "github.com/shirou/gopsutil/v4/process"
)
```

## Platform Compatibility

| Feature | Linux | Windows | macOS | FreeBSD | OpenBSD | Solaris | AIX |
|---------|-------|---------|-------|---------|---------|---------|-----|
| Host Info | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| CPU Metrics | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Memory Stats | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Disk Usage | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Network I/O | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Process Info | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ |
| Docker Support | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |

## Host Information

### Basic Host Information

```go
package main

import (
    "fmt"
    "github.com/shirou/gopsutil/v4/host"
)

func main() {
    // Get basic host information
    hostInfo, err := host.Info()
    if err != nil {
        panic(err)
    }

    fmt.Printf("Hostname: %s\n", hostInfo.Hostname)
    fmt.Printf("Uptime: %d seconds\n", hostInfo.Uptime)
    fmt.Printf("OS: %s\n", hostInfo.OS)
    fmt.Printf("Platform: %s\n", hostInfo.Platform)
    fmt.Printf("Platform Family: %s\n", hostInfo.PlatformFamily)
    fmt.Printf("Platform Version: %s\n", hostInfo.PlatformVersion)
    fmt.Printf("Architecture: %s\n", hostInfo.KernelArch)
    fmt.Printf("Kernel Version: %s\n", hostInfo.KernelVersion)
}
```

### Host Temperature Sensors

```go
func getHostTemperatures() {
    temps, err := host.SensorsTemperatures()
    if err != nil {
        fmt.Printf("Error getting temperatures: %v\n", err)
        return
    }

    for _, temp := range temps {
        fmt.Printf("Sensor: %s, Temperature: %.2f°C\n", temp.SensorKey, temp.Temperature)
    }
}
```

## CPU Monitoring

### CPU Information

```go
package main

import (
    "fmt"
    "github.com/shirou/gopsutil/v4/cpu"
)

func main() {
    // Get CPU count
    physicalCores, err := cpu.Counts(false)
    if err != nil {
        panic(err)
    }

    logicalCores, err := cpu.Counts(true)
    if err != nil {
        panic(err)
    }

    fmt.Printf("Physical Cores: %d\n", physicalCores)
    fmt.Printf("Logical Cores: %d\n", logicalCores)

    // Get detailed CPU information
    cpuInfo, err := cpu.Info()
    if err != nil {
        panic(err)
    }

    for _, info := range cpuInfo {
        fmt.Printf("CPU %d: %s\n", info.CPU, info.ModelName)
        fmt.Printf("  Vendor ID: %s\n", info.VendorID)
        fmt.Printf("  Family: %s\n", info.Family)
        fmt.Printf("  Model: %s\n", info.Model)
        fmt.Printf("  Speed: %.2f MHz\n", info.Mhz)
        fmt.Printf("  Cache Size: %d KB\n", info.CacheSize)
        fmt.Printf("  Cores: %d\n", info.Cores)
    }
}
```

### CPU Usage Monitoring

```go
func getCPUUsage() {
    // Get CPU usage percentages for all cores
    percent, err := cpu.Percent(time.Second, false)
    if err != nil {
        panic(err)
    }
    fmt.Printf("Total CPU Usage: %.2f%%\n", percent[0])

    // Get CPU usage for individual cores
    percentPerCore, err := cpu.Percent(time.Second, true)
    if err != nil {
        panic(err)
    }
    for i, p := range percentPerCore {
        fmt.Printf("Core %d Usage: %.2f%%\n", i, p)
    }

    // Get CPU time statistics
    times, err := cpu.Times(true)
    if err != nil {
        panic(err)
    }
    for i, t := range times {
        fmt.Printf("CPU %d:\n", i)
        fmt.Printf("  User: %f\n", t.User)
        fmt.Printf("  System: %f\n", t.System)
        fmt.Printf("  Idle: %f\n", t.Idle)
    }
}
```

## Memory Monitoring

### Virtual Memory Statistics

```go
package main

import (
    "fmt"
    "github.com/shirou/gopsutil/v4/mem"
)

func main() {
    // Get virtual memory statistics
    vmem, err := mem.VirtualMemory()
    if err != nil {
        panic(err)
    }

    fmt.Printf("Total Memory: %d MB\n", vmem.Total/1024/1024)
    fmt.Printf("Available Memory: %d MB\n", vmem.Available/1024/1024)
    fmt.Printf("Used Memory: %d MB\n", vmem.Used/1024/1024)
    fmt.Printf("Free Memory: %d MB\n", vmem.Free/1024/1024)
    fmt.Printf("Memory Usage: %.2f%%\n", vmem.UsedPercent)

    // Memory breakdown
    fmt.Printf("Active Memory: %d MB\n", vmem.Active/1024/1024)
    fmt.Printf("Inactive Memory: %d MB\n", vmem.Inactive/1024/1024)
    fmt.Printf("Buffers: %d MB\n", vmem.Buffers/1024/1024)
    fmt.Printf("Cached: %d MB\n", vmem.Cached/1024/1024)
    fmt.Printf("Swap Total: %d MB\n", vmem.SwapTotal/1024/1024)
    fmt.Printf("Swap Free: %d MB\n", vmem.SwapFree/1024/1024)
}
```

### Swap Memory

```go
func getSwapMemory() {
    swap, err := mem.SwapMemory()
    if err != nil {
        panic(err)
    }

    fmt.Printf("Swap Total: %d MB\n", swap.Total/1024/1024)
    fmt.Printf("Swap Used: %d MB\n", swap.Used/1024/1024)
    fmt.Printf("Swap Free: %d MB\n", swap.Free/1024/1024)
    fmt.Printf("Swap Usage: %.2f%%\n", swap.UsedPercent)
    fmt.Printf("Swap In: %d MB\n", swap.SwapIn/1024/1024)
    fmt.Printf("Swap Out: %d MB\n", swap.SwapOut/1024/1024)
}
```

## Disk Monitoring

### Disk Usage Statistics

```go
package main

import (
    "fmt"
    "strconv"
    "github.com/shirou/gopsutil/v4/disk"
)

func main() {
    // Get disk partitions
    partitions, err := disk.Partitions(false)
    if err != nil {
        panic(err)
    }

    for _, partition := range partitions {
        fmt.Printf("Device: %s\n", partition.Device)
        fmt.Printf("Mountpoint: %s\n", partition.Mountpoint)
        fmt.Printf("Filesystem: %s\n", partition.Fstype)
        fmt.Printf("Options: %s\n", partition.Opts)

        // Get disk usage for this partition
        usage, err := disk.Usage(partition.Mountpoint)
        if err != nil {
            fmt.Printf("Error getting usage: %v\n", err)
            continue
        }

        fmt.Printf("  Total: %s\n", formatBytes(usage.Total))
        fmt.Printf("  Free: %s\n", formatBytes(usage.Free))
        fmt.Printf("  Used: %s\n", formatBytes(usage.Used))
        fmt.Printf("  Usage: %.2f%%\n", usage.UsedPercent)

        // Show inodes (Linux/Unix)
        if usage.InodesTotal > 0 {
            fmt.Printf("  Inodes Total: %d\n", usage.InodesTotal)
            fmt.Printf("  Inodes Free: %d\n", usage.InodesFree)
            fmt.Printf("  Inodes Used: %d\n", usage.InodesUsed)
            fmt.Printf("  Inodes Usage: %.2f%%\n", usage.InodesUsedPercent)
        }
    }
}

func formatBytes(bytes uint64) string {
    const unit = 1024
    if bytes < unit {
        return fmt.Sprintf("%d B", bytes)
    }
    div, exp := int64(unit), 0
    for n := bytes / unit; n >= unit; n /= unit {
        div *= unit
        exp++
    }
    return fmt.Sprintf("%.1f %ciB", float64(bytes)/float64(div), "KMGTPE"[exp])
}
```

### Disk I/O Statistics

```go
func getDiskIOStats() {
    ioStats, err := disk.IOCounters()
    if err != nil {
        panic(err)
    }

    for device, stats := range ioStats {
        fmt.Printf("Device: %s\n", device)
        fmt.Printf("  Read Count: %d\n", stats.ReadCount)
        fmt.Printf("  Write Count: %d\n", stats.WriteCount)
        fmt.Printf("  Read Bytes: %s\n", formatBytes(stats.ReadBytes))
        fmt.Printf("  Write Bytes: %s\n", formatBytes(stats.WriteBytes))
        fmt.Printf("  Read Time: %d ms\n", stats.ReadTime)
        fmt.Printf("  Write Time: %d ms\n", stats.WriteTime)
        fmt.Printf("  I/O Time: %d ms\n", stats.IoTime)

        // Linux-specific fields
        if stats.SerialNumber != "" {
            fmt.Printf("  Serial Number: %s\n", stats.SerialNumber)
        }
        if stats.Label != "" {
            fmt.Printf("  Label: %s\n", stats.Label)
        }
    }
}
```

## Network Monitoring

### Network I/O Statistics

```go
package main

import (
    "fmt"
    "github.com/shirou/gopsutil/v4/net"
)

func main() {
    // Get network I/O counters
    ioStats, err := net.IOCounters(true)
    if err != nil {
        panic(err)
    }

    for _, stats := range ioStats {
        fmt.Printf("Interface: %s\n", stats.Name)
        fmt.Printf("  Bytes Sent: %s\n", formatBytes(stats.BytesSent))
        fmt.Printf("  Bytes Received: %s\n", formatBytes(stats.BytesRecv))
        fmt.Printf("  Packets Sent: %d\n", stats.PacketsSent)
        fmt.Printf("  Packets Received: %d\n", stats.PacketsRecv)
        fmt.Printf("  Err In: %d\n", stats.Errin)
        fmt.Printf("  Err Out: %d\n", stats.Errout)
        fmt.Printf("  Drop In: %d\n", stats.Dropin)
        fmt.Printf("  Drop Out: %d\n", stats.Dropout)
    }
}

// Reuse the formatBytes function from disk example
func formatBytes(bytes uint64) string {
    const unit = 1024
    if bytes < unit {
        return fmt.Sprintf("%d B", bytes)
    }
    div, exp := int64(unit), 0
    for n := bytes / unit; n >= unit; n /= unit {
        div *= unit
        exp++
    }
    return fmt.Sprintf("%.1f %ciB", float64(bytes)/float64(div), "KMGTPE"[exp])
}
```

### Network Interface Information

```go
func getNetworkInterfaces() {
    interfaces, err := net.Interfaces()
    if err != nil {
        panic(err)
    }

    for _, iface := range interfaces {
        fmt.Printf("Interface: %s\n", iface.Name)
        fmt.Printf("  MTU: %d\n", iface.MTU)
        fmt.Printf("  Hardware Addr: %s\n", iface.HardwareAddr)
        fmt.Printf("  Flags: %s\n", iface.Flags)

        for _, addr := range iface.Addrs {
            fmt.Printf("  Address: %s\n", addr.Addr)
            fmt.Printf("    Netmask: %s\n", addr.Netmask.String())
        }
    }
}
```

### Network Connections

```go
func getNetworkConnections() {
    connections, err := net.Connections("all")
    if err != nil {
        panic(err)
    }

    for _, conn := range connections {
        fmt.Printf("PID: %d\n", conn.Pid)
        fmt.Printf("  Family: %s\n", conn.Family)
        fmt.Printf("  Type: %s\n", conn.Type)
        fmt.Printf("  Local: %s:%d\n", conn.Laddr.IP, conn.Laddr.Port)
        fmt.Printf("  Remote: %s:%d\n", conn.Raddr.IP, conn.Raddr.Port)
        fmt.Printf("  Status: %s\n", conn.Status)
        fmt.Printf("  PID: %d\n", conn.Pid)
    }
}
```

## Process Management

### Process Information

```go
package main

import (
    "fmt"
    "github.com/shirou/gopsutil/v4/process"
)

func main() {
    // Get current process
    currentProc, err := process.NewProcess(int32(os.Getpid()))
    if err != nil {
        panic(err)
    }

    // Get basic process information
    name, err := currentProc.Name()
    if err != nil {
        panic(err)
    }
    fmt.Printf("Process Name: %s\n", name)

    pid := currentProc.Pid
    fmt.Printf("PID: %d\n", pid)

    ppid, err := currentProc.Ppid()
    if err != nil {
        panic(err)
    }
    fmt.Printf("Parent PID: %d\n", ppid)

    exe, err := currentProc.Exe()
    if err != nil {
        panic(err)
    }
    fmt.Printf("Executable: %s\n", exe)

    cmdline, err := currentProc.Cmdline()
    if err != nil {
        panic(err)
    }
    fmt.Printf("Command Line: %s\n", cmdline)

    cwd, err := currentProc.Cwd()
    if err != nil {
        panic(err)
    }
    fmt.Printf("Working Directory: %s\n", cwd)
}
```

### Process Resource Usage

```go
func getProcessResources(p *process.Process) {
    // CPU usage
    cpuPercent, err := p.CPUPercent()
    if err != nil {
        panic(err)
    }
    fmt.Printf("CPU Usage: %.2f%%\n", cpuPercent)

    // CPU times
    cpuTimes, err := p.Times()
    if err != nil {
        panic(err)
    }
    fmt.Printf("CPU Times - User: %.2f, System: %.2f\n", cpuTimes.User, cpuTimes.System)

    // Memory information
    memInfo, err := p.MemoryInfo()
    if err != nil {
        panic(err)
    }
    fmt.Printf("Memory - RSS: %s, VMS: %s\n",
        formatBytes(memInfo.RSS), formatBytes(memInfo.VMS))

    memPercent, err := p.MemoryPercent()
    if err != nil {
        panic(err)
    }
    fmt.Printf("Memory Usage: %.2f%%\n", memPercent)

    // Number of threads
    numThreads, err := p.NumThreads()
    if err != nil {
        panic(err)
    }
    fmt.Printf("Number of Threads: %d\n", numThreads)

    // File descriptors (Linux/Unix)
    numFDs, err := p.NumFDs()
    if err == nil {
        fmt.Printf("File Descriptors: %d\n", numFDs)
    }
}
```

### Process Management Operations

```go
func processOperations() {
    // Find processes by name
    processes, err := process.Processes()
    if err != nil {
        panic(err)
    }

    fmt.Println("Running processes:")
    for _, p := range processes {
        name, _ := p.Name()
        fmt.Printf("PID %d: %s\n", p.Pid, name)
    }

    // Find specific process
    targetPid := int32(1) // Example: init process
    proc, err := process.NewProcess(targetPid)
    if err != nil {
        fmt.Printf("Process %d not found\n", targetPid)
        return
    }

    // Check if process is running
    running, err := proc.IsRunning()
    if err != nil {
        panic(err)
    }
    fmt.Printf("Process %d is running: %t\n", targetPid, running)

    // Get parent and children
    parent, err := proc.Parent()
    if err == nil {
        fmt.Printf("Parent PID: %d\n", parent.Pid)
    }

    children, err := proc.Children()
    if err == nil {
        fmt.Printf("Children: ")
        for _, child := range children {
            fmt.Printf("%d ", child.Pid)
        }
        fmt.Println()
    }
}
```

### Process I/O Statistics

```go
func getProcessIO(p *process.Process) {
    ioStats, err := p.IOCounters()
    if err != nil {
        // I/O counters not available on all platforms
        return
    }

    fmt.Printf("I/O Statistics:\n")
    fmt.Printf("  Read Count: %d\n", ioStats.ReadCount)
    fmt.Printf("  Write Count: %d\n", ioStats.WriteCount)
    fmt.Printf("  Read Bytes: %s\n", formatBytes(ioStats.ReadBytes))
    fmt.Printf("  Write Bytes: %s\n", formatBytes(ioStats.WriteBytes))
}
```

## System Load Monitoring

### Load Average (Linux/Unix)

```go
package main

import (
    "fmt"
    "github.com/shirou/gopsutil/v4/load"
)

func getSystemLoad() {
    // Get load averages (1, 5, 15 minutes)
    loadAvg, err := load.Avg()
    if err != nil {
        panic(err)
    }

    fmt.Printf("Load Average - 1 min: %.2f, 5 min: %.2f, 15 min: %.2f\n",
        loadAvg.Load1, loadAvg.Load5, loadAvg.Load15)

    // Get system-specific load stats (misc)
    misc, err := load.Misc()
    if err != nil {
        panic(err)
    }

    fmt.Printf("Procs Running: %d\n", misc.ProcsRunning)
    fmt.Printf("Procs Total: %d\n", misc.ProcsTotal)
    fmt.Printf("Procs Blocked: %d\n", misc.ProcsBlocked)
}
```

## Docker Container Monitoring

### Docker Container Statistics

```go
package main

import (
    "fmt"
    "github.com/shirou/gopsutil/v4/docker"
)

func monitorDockerContainers() {
    // Get list of Docker container IDs
    containerIDs, err := docker.GetDockerIDList()
    if err != nil {
        fmt.Printf("Error getting Docker containers: %v\n", err)
        return
    }

    for _, containerID := range containerIDs {
        fmt.Printf("Container ID: %s\n", containerID)

        // Get container statistics
        stats, err := docker.GetCgroupStats(containerID)
        if err != nil {
            fmt.Printf("Error getting container stats: %v\n", err)
            continue
        }

        // CPU statistics
        if stats.CpuStats != nil {
            fmt.Printf("  CPU Usage: %.2f%%\n", stats.CpuStats.CpuUsage.TotalUsage)
            fmt.Printf("  System CPU Usage: %.2f%%\n", stats.CpuStats.SystemCpuUsage)
        }

        // Memory statistics
        if stats.MemoryStats != nil {
            fmt.Printf("  Memory Usage: %s\n", formatBytes(stats.MemoryStats.Usage))
            fmt.Printf("  Memory Limit: %s\n", formatBytes(stats.MemoryStats.Limit))
        }

        // Network statistics
        if stats.Networks != nil {
            for iface, netStats := range stats.Networks {
                fmt.Printf("  Interface %s:\n", iface)
                fmt.Printf("    Rx Bytes: %s\n", formatBytes(netStats.RxBytes))
                fmt.Printf("    Tx Bytes: %s\n", formatBytes(netStats.TxBytes))
            }
        }
    }
}
```

### Docker Cgroup CPU Statistics

```go
func getDockerCgroupCPU() {
    user, system, err := docker.CgroupCPU()
    if err != nil {
        panic(err)
    }

    fmt.Printf("Docker CPU - User: %d, System: %d\n", user, system)
}
```

### Docker Cgroup Memory Statistics

```go
func getDockerCgroupMemory() {
    stats, err := docker.CgroupMem()
    if err != nil {
        panic(err)
    }

    fmt.Printf("Docker Memory Stats: %+v\n", stats)
}
```

## Advanced Usage

### Context Support for Custom Paths

```go
package main

import (
    "context"
    "fmt"
    "github.com/shirou/gopsutil/v4/common"
    "github.com/shirou/gopsutil/v4/mem"
)

func main() {
    // Create context with custom /proc path
    ctx := context.WithValue(context.Background(),
        common.EnvKey,
        common.EnvMap{
            common.HostProcEnvKey: "/myproc",  // Custom proc path
        })

    // Use context for system calls
    v, err := mem.VirtualMemoryWithContext(ctx)
    if err != nil {
        panic(err)
    }

    fmt.Printf("Memory with custom proc path: %v\n", v)
}
```

### Platform-Specific Extensions

```go
func platformSpecificExtensions() {
    // Windows-specific memory information
    if runtime.GOOS == "windows" {
        ex := mem.NewExWindows()
        v, err := ex.VirtualMemory()
        if err != nil {
            panic(err)
        }
        fmt.Printf("Windows Virtual Memory: %+v\n", v)
    }

    // Linux-specific memory information
    if runtime.GOOS == "linux" {
        ex := mem.NewExLinux()
        v, err := ex.VirtualMemory()
        if err != nil {
            panic(err)
        }
        fmt.Printf("Linux Virtual Memory: %+v\n", v)
    }
}
```

### Continuous Monitoring

```go
func continuousMonitoring() {
    ticker := time.NewTicker(5 * time.Second)
    defer ticker.Stop()

    for {
        select {
        case <-ticker.C:
            // Get CPU usage
            cpuPercent, err := cpu.Percent(time.Second, false)
            if err == nil {
                fmt.Printf("CPU: %.2f%%\n", cpuPercent[0])
            }

            // Get memory usage
            vmem, err := mem.VirtualMemory()
            if err == nil {
                fmt.Printf("Memory: %.2f%%\n", vmem.UsedPercent)
            }

            fmt.Println("---")
        }
    }
}
```

## Error Handling and Best Practices

### Robust Error Handling

```go
func safeGetSystemInfo() {
    // Always check for errors
    if v, err := mem.VirtualMemory(); err == nil {
        fmt.Printf("Memory: %.2f%%\n", v.UsedPercent)
    } else {
        fmt.Printf("Error getting memory info: %v\n", err)
    }

    // Handle platform-specific features
    if runtime.GOOS == "linux" {
        if load, err := load.Avg(); err == nil {
            fmt.Printf("Load: %.2f, %.2f, %.2f\n", load.Load1, load.Load5, load.Load15)
        }
    }
}
```

### Performance Considerations

```go
func efficientMonitoring() {
    // Cache expensive operations
    var cachedCPUInfo []cpu.InfoStat
    var cacheTime time.Time
    const cacheDuration = 30 * time.Second

    // Use single goroutine for monitoring
    go func() {
        ticker := time.NewTicker(5 * time.Second)
        defer ticker.Stop()

        for range ticker.C {
            // Refresh CPU info cache if needed
            if time.Since(cacheTime) > cacheDuration {
                if info, err := cpu.Info(); err == nil {
                    cachedCPUInfo = info
                    cacheTime = time.Now()
                }
            }

            // Use cached data where possible
            if len(cachedCPUInfo) > 0 {
                fmt.Printf("CPU Cores: %d\n", len(cachedCPUInfo))
            }
        }
    }()
}
```

## Common Use Cases

### System Health Monitor

```go
type SystemHealth struct {
    CPUUsage    float64
    MemoryUsage float64
    DiskUsage   float64
    LoadAvg1    float64
    Uptime      uint64
    Healthy     bool
}

func getSystemHealth() SystemHealth {
    var health SystemHealth

    // CPU usage
    if cpuPercent, err := cpu.Percent(time.Second, false); err == nil {
        health.CPUUsage = cpuPercent[0]
    }

    // Memory usage
    if vmem, err := mem.VirtualMemory(); err == nil {
        health.MemoryUsage = vmem.UsedPercent
    }

    // Disk usage (root partition)
    if usage, err := disk.Usage("/"); err == nil {
        health.DiskUsage = usage.UsedPercent
    }

    // Load average
    if load, err := load.Avg(); err == nil {
        health.LoadAvg1 = load.Load1
    }

    // Uptime
    if info, err := host.Info(); err == nil {
        health.Uptime = info.Uptime
    }

    // Determine health status
    health.Healthy = health.CPUUsage < 80.0 &&
                   health.MemoryUsage < 80.0 &&
                   health.DiskUsage < 80.0 &&
                   health.LoadAvg1 < float64(runtime.NumCPU())

    return health
}
```

### Process Discovery

```go
func findProcessesByName(name string) ([]*process.Process, error) {
    var results []*process.Process

    processes, err := process.Processes()
    if err != nil {
        return nil, err
    }

    for _, p := range processes {
        procName, err := p.Name()
        if err != nil {
            continue
        }

        if strings.Contains(strings.ToLower(procName), strings.ToLower(name)) {
            results = append(results, p)
        }
    }

    return results, nil
}
```

## Troubleshooting

### Common Issues

1. **Permission Denied**: Some metrics require elevated privileges
   ```bash
   # Run with appropriate permissions
   sudo ./your-app
   ```

2. **Missing Features**: Not all features are available on all platforms
   ```go
   // Check platform compatibility
   if runtime.GOOS != "linux" {
       fmt.Println("This feature is only available on Linux")
       return
   }
   ```

3. **Context Cancellation**: Handle cancelled operations gracefully
   ```go
   ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
   defer cancel()

   v, err := mem.VirtualMemoryWithContext(ctx)
   if err == context.DeadlineExceeded {
       fmt.Println("Operation timed out")
       return
   }
   ```

### Debug Mode

```go
// Enable debug logging
func debugMode() {
    log.SetFlags(log.LstdFlags | log.Lshortfile)
    log.Printf("Debug: Starting system monitoring")
}
```

## Integration Examples

### Export to Prometheus

```go
func exportToPrometheus() {
    cpuPercent, _ := cpu.Percent(time.Second, false)
    vmem, _ := mem.VirtualMemory()

    fmt.Printf("# HELP cpu_usage_percent CPU usage percentage\n")
    fmt.Printf("# TYPE cpu_usage_percent gauge\n")
    fmt.Printf("cpu_usage_percent %.2f\n", cpuPercent[0])

    fmt.Printf("# HELP memory_usage_percent Memory usage percentage\n")
    fmt.Printf("# TYPE memory_usage_percent gauge\n")
    fmt.Printf("memory_usage_percent %.2f\n", vmem.UsedPercent)
}
```

### JSON Export

```go
func exportToJSON() (map[string]interface{}, error) {
    data := make(map[string]interface{})

    if vmem, err := mem.VirtualMemory(); err == nil {
        data["memory"] = map[string]interface{}{
            "total":       vmem.Total,
            "used":        vmem.Used,
            "free":        vmem.Free,
            "usedPercent": vmem.UsedPercent,
        }
    }

    if cpuPercent, err := cpu.Percent(time.Second, false); err == nil {
        data["cpu"] = map[string]interface{}{
            "usage": cpuPercent[0],
        }
    }

    if hostInfo, err := host.Info(); err == nil {
        data["host"] = map[string]interface{}{
            "hostname": hostInfo.Hostname,
            "uptime":   hostInfo.Uptime,
            "os":       hostInfo.OS,
            "platform": hostInfo.Platform,
        }
    }

    return data, nil
}
```

## Resources

- **GitHub Repository**: [https://github.com/shirou/gopsutil](https://github.com/shirou/gopsutil)
- **Documentation**: [https://pkg.go.dev/github.com/shirou/gopsutil](https://pkg.go.dev/github.com/shirou/gopsutil)
- **Examples**: [https://github.com/shirou/gopsutil/tree/master/examples](https://github.com/shirou/gopsutil/tree/master/examples)

---

This comprehensive guide covers the essential aspects of gopsutil for system monitoring in Go. From basic CPU and memory monitoring to advanced process management and Docker container statistics, gopsutil provides everything needed to build robust system monitoring applications with a clean, cross-platform API.