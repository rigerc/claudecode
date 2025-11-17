---
name: gopsutil
version: "1.0.0"
description: Use when implementing system monitoring, performance analysis, or DevOps applications requiring cross-platform system metrics in Go.
author: Claude Code
keywords:
  - gopsutil
  - system monitoring
  - performance
  - devops
  - metrics
  - cross-platform
---

# gopsutil System Monitoring Expert

Use when developing Go applications that need to monitor system resources, processes, or performance metrics across different platforms.

## When to Use

- Creating system monitoring applications
- Building performance analysis tools
- Implementing health check systems
- Writing DevOps automation scripts
- Developing process management utilities
- Creating container monitoring solutions

## Core Expertise

- Cross-platform system metrics (CPU, memory, disk, network)
- Process monitoring and management
- Docker container statistics
- Performance data collection and analysis
- Platform-specific feature handling
- Resource usage optimization patterns

## Quick Reference

**Key Packages**: `cpu`, `mem`, `disk`, `net`, `process`, `host`, `load`, `docker`
**Platform Support**: Linux, Windows, macOS, FreeBSD, OpenBSD, Solaris, AIX
**Import**: `"github.com/shirou/gopsutil/v4/<package>"`

## Quick Start

1. **Install**: `go get github.com/shirou/gopsutil/v4`
2. **Basic Usage**: Get CPU usage with `cpu.Percent(time.Second, false)`
3. **Memory**: Use `mem.VirtualMemory()` for memory statistics
4. **Processes**: Use `process.Processes()` for process enumeration
5. **Platform Check**: Always check `runtime.GOOS` before using platform-specific features

## Common Patterns

- **Resource Monitoring**: Use `Percent()` for usage rates, `Info()` for detailed stats
- **Process Discovery**: Use `Processes()` with filtering for target identification
- **Continuous Monitoring**: Implement caching for expensive operations like `Info()`
- **Platform Handling**: Check `runtime.GOOS` before accessing platform-specific features
- **Error Patterns**: Handle missing features gracefully, not all metrics available everywhere

## References

- **[Quick Examples](references/quick-examples.md)**: Ready-to-use code snippets for common monitoring tasks
- **[API Reference](references/api-reference.md)**: Complete function and type documentation with platform compatibility
- **[Usage Patterns](references/usage-patterns.md)**: Advanced patterns for production monitoring applications
- **[Troubleshooting](references/troubleshooting.md)**: Common issues, platform-specific problems, and debugging techniques