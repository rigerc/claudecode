# gopsutil API Reference

## Package Overview

gopsutil is organized into separate packages for different system aspects:

- `cpu` - CPU information and usage
- `mem` - Memory statistics
- `disk` - Disk usage and I/O
- `net` - Network statistics
- `process` - Process information
- `host` - Host system information
- `load` - System load averages
- `docker` - Docker container monitoring

## CPU Package

### Core Functions

```go
// Get CPU usage percentage
func Percent(interval time.Duration, percpu bool) ([]float64, error)

// Get CPU times
func Times(percpu bool) ([]TimesStat, error)

// Get CPU information
func Info() ([]InfoStat, error)

// Get number of CPU cores
func Counts(logical bool) (int, error)
```

### Key Types

```go
type InfoStat struct {
    CPU         int32   `json:"cpu"`
    VendorID    string  `json:"vendor_id"`
    Family      string  `json:"family"`
    Model       string  `json:"model"`
    Stepping    string  `json:"stepping"`
    PhysicalID  string  `json:"physical_id"`
    CoreID      string  `json:"core_id"`
    Cores       int32   `json:"cores"`
    ModelName   string  `json:"model_name"`
    Mhz         float64 `json:"mhz"`
    CacheSize   int32   `json:"cache_size"`
    Flags       []string `json:"flags"`
    Microcode   string  `json:"microcode"`
}

type TimesStat struct {
    CPU       string  `json:"cpu"`
    User      float64 `json:"user"`
    System    float64 `json:"system"`
    Idle      float64 `json:"idle"`
    Nice      float64 `json:"nice"`
    Iowait    float64 `json:"iowait"`
    Irq       float64 `json:"irq"`
    Softirq   float64 `json:"softirq"`
    Steal     float64 `json:"steal"`
    Guest     float64 `json:"guest"`
    GuestNice float64 `json:"guest_nice"`
}
```

## Memory Package

### Core Functions

```go
// Get virtual memory statistics
func VirtualMemory() (*VirtualMemoryStat, error)

// Get swap memory statistics
func SwapMemory() (*SwapMemoryStat, error)
```

### Key Types

```go
type VirtualMemoryStat struct {
    Total              uint64  `json:"total"`
    Available          uint64  `json:"available"`
    Used               uint64  `json:"used"`
    UsedPercent        float64 `json:"used_percent"`
    Free               uint64  `json:"free"`
    Active             uint64  `json:"active"`
    Inactive           uint64  `json:"inactive"`
    Buffers            uint64  `json:"buffers"`
    Cached             uint64  `json:"cached"`
    Shared             uint64  `json:"shared"`
    Slab               uint64  `json:"slab"`
    Sreclaimable       uint64  `json:"sreclaimable"`
    Sunreclaim         uint64  `json:"sunreclaim"`
    PageTables         uint64  `json:"page_tables"`
    SwapCached         uint64  `json:"swap_cached"`
    CommitLimit        uint64  `json:"commit_limit"`
    CommittedAS        uint64  `json:"committed_as"`
    HighTotal          uint64  `json:"high_total"`
    HighFree           uint64  `json:"high_free"`
    LowTotal           uint64  `json:"low_total"`
    LowFree            uint64  `json:"low_free"`
    SwapTotal          uint64  `json:"swap_total"`
    SwapFree           uint64  `json:"swap_free"`
    Mapped             uint64  `json:"mapped"`
    VmallocTotal       uint64  `json:"vmalloc_total"`
    VmallocUsed        uint64  `json:"vmalloc_used"`
    VmallocChunk       uint64  `json:"vmalloc_chunk"`
    HugePagesTotal     uint64  `json:"huge_pages_total"`
    HugePagesFree      uint64  `json:"huge_pages_free"`
    HugePagesRsvd      uint64  `json:"huge_pages_rsvd"`
    HugePagesSurp      uint64  `json:"huge_pages_surp"`
    HugePageSize       uint64  `json:"huge_page_size"`
}
```

## Disk Package

### Core Functions

```go
// Get disk partition information
func Partitions(all bool) ([]PartitionStat, error)

// Get disk usage statistics
func Usage(path string) (*UsageStat, error)

// Get disk I/O counters
func IOCounters(perdisk bool) ([]IOCountersStat, error)
```

### Key Types

```go
type PartitionStat struct {
    Device     string `json:"device"`
    Mountpoint string `json:"mountpoint"`
    Fstype     string `json:"fstype"`
    Opts       string `json:"opts"`
}

type UsageStat struct {
    Path              string  `json:"path"`
    Fstype            string  `json:"fstype"`
    Total             uint64  `json:"total"`
    Free              uint64  `json:"free"`
    Used              uint64  `json:"used"`
    UsedPercent       float64 `json:"used_percent"`
    InodesTotal       uint64  `json:"inodes_total"`
    InodesUsed        uint64  `json:"inodes_used"`
    InodesFree        uint64  `json:"inodes_free"`
    InodesUsedPercent float64 `json:"inodes_used_percent"`
}

type IOCountersStat struct {
    Name       string `json:"name"`
    ReadCount  uint64 `json:"read_count"`
    WriteCount uint64 `json:"write_count"`
    ReadBytes  uint64 `json:"read_bytes"`
    WriteBytes uint64 `json:"write_bytes"`
    ReadTime   uint64 `json:"read_time"`
    WriteTime  uint64 `json:"write_time"`
    Iotime     uint64 `json:"io_time"`
    SerialNumber string `json:"serial_number"`
    Label        string `json:"label"`
}
```

## Network Package

### Core Functions

```go
// Get network I/O counters
func IOCounters(pernic bool) ([]IOCountersStat, error)

// Get network interface information
func Interfaces() ([]NetInterfaceStat, error)

// Get network connections
func Connections(kind string) ([]ConnectionStat, error)
```

### Key Types

```go
type IOCountersStat struct {
    Name      string `json:"name"`
    BytesSent uint64 `json:"bytes_sent"`
    BytesRecv uint64 `json:"bytes_recv"`
    PacketsSent uint64 `json:"packets_sent"`
    PacketsRecv uint64 `json:"packets_recv"`
    Errin     uint64 `json:"errin"`
    Errout    uint64 `json:"errout"`
    Dropin    uint64 `json:"dropin"`
    Dropout   uint64 `json:"dropout"`
}

type NetInterfaceStat struct {
    Name        string `json:"name"`
    MTU         int    `json:"mtu"`
    HardwareAddr string `json:"hardware_addr"`
    Flags       []string `json:"flags"`
    Addrs       []Addr `json:"addrs"`
}
```

## Process Package

### Core Functions

```go
// Create new process instance
func NewProcess(pid int32) (*Process, error)

// Get all processes
func Processes() ([]*Process, error)

// Find process by PID
func PidExists(pid int32) (bool, error)
```

### Process Methods

```go
// Basic process information
func (p *Process) Name() (string, error)
func (p *Process) Pid() int32
func (p *Process) Ppid() (int32, error)
func (p *Process) Cmdline() (string, error)
func (p *Process) Exe() (string, error)
func (p *Process) Cwd() (string, error)

// Resource usage
func (p *Process) CPUPercent() (float64, error)
func (p *Process) MemoryInfo() (*MemoryInfoStat, error)
func (p *Process) MemoryPercent() (float32, error)
func (p *Process) CreateTime() (int64, error)
func (p *Process) NumThreads() (int32, error)

// Process management
func (p *Process) Terminate() error
func (p *Process) Kill() error
func (p *Process) Suspend() error
func (p *Process) Resume() error

// Process relationships
func (p *Process) Parent() (*Process, error)
func (p *Process) Children() ([]*Process, error)
func (p *Process) IsRunning() (bool, error)
```

## Host Package

### Core Functions

```go
// Get host information
func Info() (*InfoStat, error)

// Get boot time
func BootTime() (uint64, error)

// Get uptime
func Uptime() (uint64, error)

// Get temperature sensors
func SensorsTemperatures() ([]TemperatureStat, error)
```

## Load Package

### Core Functions

```go
// Get system load averages
func Avg() (*AvgStat, error)

// Get miscellaneous load statistics
func Misc() (*MiscStat, error)
```

## Context Support

Most functions support context for cancellation and custom paths:

```go
// Example with context
ctx := context.WithValue(context.Background(),
    common.EnvKey, common.EnvMap{common.HostProcEnvKey: "/custom/proc"},
)

mem.VirtualMemoryWithContext(ctx)
cpu.PercentWithContext(time.Second, false, ctx)
```

## Platform Compatibility

| Feature | Linux | Windows | macOS | FreeBSD |
|---------|-------|---------|-------|---------|
| CPU Info | ✅ | ✅ | ✅ | ✅ |
| Memory | ✅ | ✅ | ✅ | ✅ |
| Disk Usage | ✅ | ✅ | ✅ | ✅ |
| Network I/O | ✅ | ✅ | ✅ | ✅ |
| Process Info | ✅ | ✅ | ✅ | ✅ |
| Load Average | ✅ | ❌ | ✅ | ✅ |
| Temperature Sensors | ✅ | ❌ | ❌ | ✅ |