package main

import (
    "fmt"
    "log"
    "os"
    "runtime"
    "time"

    "github.com/shirou/gopsutil/v4/cpu"
    "github.com/shirou/gopsutil/v4/disk"
    "github.com/shirou/gopsutil/v4/host"
    "github.com/shirou/gopsutil/v4/load"
    "github.com/shirou/gopsutil/v4/mem"
    "github.com/shirou/gopsutil/v4/net"
    "github.com/shirou/gopsutil/v4/process"
)

type SystemMonitor struct {
    interval time.Duration
    debug    bool
}

func NewSystemMonitor(interval time.Duration, debug bool) *SystemMonitor {
    return &SystemMonitor{
        interval: interval,
        debug:    debug,
    }
}

func (sm *SystemMonitor) printHeader() {
    fmt.Println("=== System Monitor ===")
    fmt.Printf("Platform: %s\n", runtime.GOOS)
    fmt.Printf("Architecture: %s\n", runtime.GOARCH)
    fmt.Println()
}

func (sm *SystemMonitor) getHostInfo() {
    info, err := host.Info()
    if err != nil {
        log.Printf("Error getting host info: %v", err)
        return
    }

    fmt.Println("=== Host Information ===")
    fmt.Printf("Hostname: %s\n", info.Hostname)
    fmt.Printf("OS: %s %s\n", info.OS, info.Platform)
    fmt.Printf("Platform Family: %s\n", info.PlatformFamily)
    fmt.Printf("Platform Version: %s\n", info.PlatformVersion)
    fmt.Printf("Uptime: %s\n", time.Duration(info.Uptime)*time.Second)
    fmt.Printf("Processes: %d\n", info.Procs)
    fmt.Println()
}

func (sm *SystemMonitor) getCPUInfo() {
    fmt.Println("=== CPU Information ===")

    // CPU usage
    cpuPercent, err := cpu.Percent(time.Second, false)
    if err != nil {
        log.Printf("Error getting CPU usage: %v", err)
    } else {
        fmt.Printf("CPU Usage: %.2f%%\n", cpuPercent[0])
    }

    // CPU details (cached, don't call too frequently)
    cpuInfo, err := cpu.Info()
    if err != nil {
        log.Printf("Error getting CPU info: %v", err)
    } else {
        cores, _ := cpu.Counts(true)
        fmt.Printf("CPU Cores: %d\n", cores)
        if len(cpuInfo) > 0 {
            fmt.Printf("CPU Model: %s\n", cpuInfo[0].ModelName)
            fmt.Printf("CPU Speed: %.2f MHz\n", cpuInfo[0].Mhz)
        }
    }
    fmt.Println()
}

func (sm *SystemMonitor) getMemoryInfo() {
    vmem, err := mem.VirtualMemory()
    if err != nil {
        log.Printf("Error getting memory info: %v", err)
        return
    }

    fmt.Println("=== Memory Information ===")
    fmt.Printf("Total Memory: %.2f GB\n", float64(vmem.Total)/1024/1024/1024)
    fmt.Printf("Available Memory: %.2f GB\n", float64(vmem.Available)/1024/1024/1024)
    fmt.Printf("Used Memory: %.2f GB (%.2f%%)\n",
        float64(vmem.Used)/1024/1024/1024, vmem.UsedPercent)
    fmt.Printf("Free Memory: %.2f GB\n", float64(vmem.Free)/1024/1024/1024)

    if vmem.SwapTotal > 0 {
        fmt.Printf("Swap Total: %.2f GB\n", float64(vmem.SwapTotal)/1024/1024/1024)
        fmt.Printf("Swap Used: %.2f GB (%.2f%%)\n",
            float64(vmem.SwapUsed)/1024/1024/1024,
            float64(vmem.Used)/vmem.SwapTotal*100)
    }
    fmt.Println()
}

func (sm *SystemMonitor) getDiskInfo() {
    partitions, err := disk.Partitions(false)
    if err != nil {
        log.Printf("Error getting disk partitions: %v", err)
        return
    }

    fmt.Println("=== Disk Information ===")
    for _, partition := range partitions {
        fmt.Printf("Device: %s\n", partition.Device)
        fmt.Printf("Mountpoint: %s\n", partition.Mountpoint)
        fmt.Printf("Filesystem: %s\n", partition.Fstype)

        usage, err := disk.Usage(partition.Mountpoint)
        if err != nil {
            log.Printf("Error getting disk usage: %v", err)
            continue
        }

        fmt.Printf("  Total: %.2f GB\n", float64(usage.Total)/1024/1024/1024)
        fmt.Printf("  Free: %.2f GB\n", float64(usage.Free)/1024/1024/1024)
        fmt.Printf("  Used: %.2f GB (%.2f%%)\n",
            float64(usage.Used)/1024/1024/1024, usage.UsedPercent)
        fmt.Println()
    }
}

func (sm *SystemMonitor) getNetworkInfo() {
    interfaces, err := net.Interfaces()
    if err != nil {
        log.Printf("Error getting network interfaces: %v", err)
        return
    }

    fmt.Println("=== Network Information ===")
    for _, iface := range interfaces {
        fmt.Printf("Interface: %s\n", iface.Name)
        fmt.Printf("  MTU: %d\n", iface.MTU)
        fmt.Printf("  Hardware Addr: %s\n", iface.HardwareAddr)
        fmt.Printf("  Flags: %v\n", iface.Flags)

        ioCounters, err := net.IOCountersByName(iface.Name)
        if err == nil && len(ioCounters) > 0 {
            counter := ioCounters[0]
            fmt.Printf("  Bytes Sent: %s\n", formatBytes(counter.BytesSent))
            fmt.Printf("  Bytes Received: %s\n", formatBytes(counter.BytesRecv))
            fmt.Printf("  Packets Sent: %d\n", counter.PacketsSent)
            fmt.Printf("  Packets Received: %d\n", counter.PacketsRecv)
        }
        fmt.Println()
    }
}

func (sm *SystemMonitor) getProcessInfo() {
    processes, err := process.Processes()
    if err != nil {
        log.Printf("Error getting processes: %v", err)
        return
    }

    fmt.Println("=== Process Information ===")
    fmt.Printf("Total Processes: %d\n", len(processes))

    // Show top 5 processes by memory usage
    fmt.Println("\nTop 5 Processes by Memory Usage:")
    for i := 0; i < 5 && i < len(processes); i++ {
        p := processes[i]
        name, _ := p.Name()
        memInfo, _ := p.MemoryInfo()
        pid := p.Pid

        if memInfo != nil {
            fmt.Printf("%d. PID %-8d %s (RSS: %s)\n",
                i+1, pid, name, formatBytes(memInfo.RSS))
        }
    }
    fmt.Println()
}

func (sm *SystemMonitor) getLoadAverage() {
    if runtime.GOOS == "windows" {
        fmt.Println("=== Load Average ===")
        fmt.Println("Load averages not available on Windows")
        fmt.Println()
        return
    }

    avg, err := load.Avg()
    if err != nil {
        log.Printf("Error getting load average: %v", err)
        return
    }

    fmt.Println("=== Load Average ===")
    fmt.Printf("1 min: %.2f\n", avg.Load1)
    fmt.Printf("5 min: %.2f\n", avg.Load5)
    fmt.Printf("15 min: %.2f\n", avg.Load15)

    misc, err := load.Misc()
    if err == nil {
        fmt.Printf("Running Processes: %d\n", misc.ProcsRunning)
        fmt.Printf("Total Processes: %d\n", misc.ProcsTotal)
    }
    fmt.Println()
}

func (sm *SystemMonitor) monitorContinuously() {
    ticker := time.NewTicker(sm.interval)
    defer ticker.Stop()

    sm.printHeader()

    count := 0
    for {
        select {
        case <-ticker.C:
            count++
            fmt.Printf("\n=== Monitoring Cycle %d - %s ===\n",
                count, time.Now().Format("2006-01-02 15:04:05"))

            sm.getQuickStats()

            if count >= 10 { // Limit to 10 cycles
                fmt.Println("Monitoring completed")
                return
            }
        }
    }
}

func (sm *SystemMonitor) getQuickStats() {
    // Only get essential metrics for continuous monitoring
    if cpuPercent, err := cpu.Percent(time.Second, false); err == nil {
        fmt.Printf("CPU: %.2f%%\n", cpuPercent[0])
    }

    if vmem, err := mem.VirtualMemory(); err == nil {
        fmt.Printf("Memory: %.2f%% (%.2f GB used / %.2f GB total)\n",
            vmem.UsedPercent,
            float64(vmem.Used)/1024/1024/1024,
            float64(vmem.Total)/1024/1024/1024)
    }

    if runtime.GOOS != "windows" {
        if load, err := load.Avg(); err == nil {
            fmt.Printf("Load: %.2f, %.2f, %.2f\n", load.Load1, load.Load5, load.Load15)
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
    return fmt.Sprintf("%.1f %cB", float64(bytes)/float64(div), "KMGTPE"[exp])
}

func main() {
    // Parse command line arguments
    interval := 10 * time.Second
    continuous := false
    debug := false

    if len(os.Args) > 1 {
        switch os.Args[1] {
        case "-c", "--continuous":
            continuous = true
        case "-d", "--debug":
            debug = true
        case "-h", "--help":
            fmt.Println("Usage: system-monitor [options]")
            fmt.Println("Options:")
            fmt.Println("  -c, --continuous    Run in continuous mode")
            fmt.Println("  -d, --debug         Enable debug logging")
            fmt.Println("  -h, --help          Show this help")
            os.Exit(0)
        }

        if len(os.Args) > 2 {
            switch os.Args[2] {
            case "-c", "--continuous":
                continuous = true
            case "-d", "--debug":
                debug = true
            }
        }
    }

    monitor := NewSystemMonitor(interval, debug)

    if debug {
        log.Printf("Starting system monitor (debug mode)")
        log.Printf("Interval: %v, Continuous: %t", interval, continuous)
    }

    if continuous {
        monitor.monitorContinuously()
    } else {
        monitor.printHeader()
        monitor.getHostInfo()
        monitor.getCPUInfo()
        monitor.getMemoryInfo()
        monitor.getDiskInfo()
        monitor.getNetworkInfo()
        monitor.getProcessInfo()
        monitor.getLoadAverage()
    }
}