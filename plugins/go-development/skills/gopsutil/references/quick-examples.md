# gopsutil Quick Examples

## Basic System Information

```go
import (
    "fmt"
    "runtime"
    "github.com/shirou/gopsutil/v4/cpu"
    "github.com/shirou/gopsutil/v4/mem"
    "github.com/shirou/gopsutil/v4/host"
)

func main() {
    // CPU usage
    cpuPercent, _ := cpu.Percent(time.Second, false)
    fmt.Printf("CPU Usage: %.2f%%\n", cpuPercent[0])

    // Memory usage
    vmem, _ := mem.VirtualMemory()
    fmt.Printf("Memory Usage: %.2f%%\n", vmem.UsedPercent)

    // Host info
    info, _ := host.Info()
    fmt.Printf("OS: %s %s\n", info.OS, info.Platform)
    fmt.Printf("Uptime: %v\n", time.Duration(info.Uptime)*time.Second)

    fmt.Printf("Platform: %s\n", runtime.GOOS)
}
```

## Process Monitoring

```go
import (
    "fmt"
    "github.com/shirou/gopsutil/v4/process"
)

func findProcessByName(name string) (*process.Process, error) {
    processes, _ := process.Processes()
    for _, p := range processes {
        procName, _ := p.Name()
        if procName == name {
            return p, nil
        }
    }
    return nil, fmt.Errorf("process %s not found", name)
}

func getProcessStats(pid int32) error {
    p, err := process.NewProcess(pid)
    if err != nil {
        return err
    }

    name, _ := p.Name()
    cpuPercent, _ := p.CPUPercent()
    memInfo, _ := p.MemoryInfo()

    fmt.Printf("Process: %s (PID: %d)\n", name, pid)
    fmt.Printf("CPU: %.2f%%\n", cpuPercent)
    fmt.Printf("Memory: %d MB\n", memInfo.RSS/1024/1024)
    return nil
}
```

## Disk Usage

```go
import "github.com/shirou/gopsutil/v4/disk"

func getDiskUsage(path string) {
    usage, _ := disk.Usage(path)
    fmt.Printf("Path: %s\n", path)
    fmt.Printf("Total: %.2f GB\n", float64(usage.Total)/1024/1024/1024)
    fmt.Printf("Free: %.2f GB\n", float64(usage.Free)/1024/1024/1024)
    fmt.Printf("Used: %.2f%%\n", usage.UsedPercent)
}

func listDiskPartitions() {
    partitions, _ := disk.Partitions(false)
    for _, p := range partitions {
        fmt.Printf("Device: %s, Mount: %s, FS: %s\n",
            p.Device, p.Mountpoint, p.Fstype)
    }
}
```

## Network Statistics

```go
import "github.com/shirou/gopsutil/v4/net"

func getNetworkStats() {
    counters, _ := net.IOCounters(true)
    for _, counter := range counters {
        fmt.Printf("Interface: %s\n", counter.Name)
        fmt.Printf("  Sent: %d bytes\n", counter.BytesSent)
        fmt.Printf("  Received: %d bytes\n", counter.BytesRecv)
        fmt.Printf("  Sent Packets: %d\n", counter.PacketsSent)
        fmt.Printf("  Received Packets: %d\n", counter.PacketsRecv)
    }
}

func listNetworkInterfaces() {
    interfaces, _ := net.Interfaces()
    for _, iface := range interfaces {
        fmt.Printf("Interface: %s, MTU: %d\n", iface.Name, iface.MTU)
        fmt.Printf("  Hardware Addr: %s\n", iface.HardwareAddr)
        fmt.Printf("  Flags: %s\n", iface.Flags)
    }
}
```

## Docker Container Monitoring

```go
import "github.com/shirou/gopsutil/v4/docker"

func monitorDockerContainers() {
    containerIDs, _ := docker.GetDockerIDList()
    fmt.Printf("Found %d containers\n", len(containerIDs))

    for _, id := range containerIDs {
        stats, _ := docker.GetCgroupStats(id)
        if stats.CpuStats != nil {
            fmt.Printf("Container %s CPU: %.2f%%\n", id,
                float64(stats.CpuStats.CpuUsage.TotalUsage))
        }
        if stats.MemoryStats != nil {
            fmt.Printf("Container %s Memory: %d bytes\n", id,
                stats.MemoryStats.Usage)
        }
    }
}
```