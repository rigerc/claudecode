# Go Hass Anything: Comprehensive Guide

## Overview

**Go Hass Anything** is a powerful Go framework that enables you to create self-contained applications for Home Assistant integration via MQTT. This framework allows you to add custom sensors, controls, and automation to Home Assistant that aren't available through existing integrations.

**Key Features:**
- Write self-contained "apps" in Go that communicate with Home Assistant
- Support for multiple Home Assistant entity types (sensor, binary_sensor, switch, button, number, text, image, camera)
- Simple TOML configuration with optional BubbleTea UI for preferences
- Light on resources - runs anywhere Go runs
- Cross-platform support (embedded to server hardware)
- Event-driven or polling-based update mechanisms
- Single binary deployment

## Installation

### Prerequisites

- **Go 1.19+** for development
- **Mage** build system
- **MQTT Broker** (such as Mosquitto)
- **Home Assistant** with MQTT integration configured

### Development Setup

#### Option 1: Using DevContainer (Recommended)

1. Open the project in Visual Studio Code
2. Install the recommended DevContainer extension
3. Reopen in Container when prompted
4. The DevContainer includes Home Assistant and Mosquitto for testing

#### Option 2: Manual Setup

1. Clone the repository:
```bash
git clone https://github.com/joshuar/go-hass-anything.git
cd go-hass-anything
```

2. Install Mage:
```bash
go install github.com/magefile/mage@latest
```

3. Build the project:
```bash
mage -d build/magefiles -w . build:full
```

## Quick Start

### 1. Configure MQTT Connection

First, configure the connection to your MQTT broker:

```bash
go-hass-anything configure
```

This will guide you through setting up:
- MQTT broker address and port
- Authentication credentials (username/password)
- TLS settings (if required)
- Client identification

### 2. Create Your First App

Create a new file in the `apps/` directory with a `main.go` file:

```go
package main

import (
    "time"
    "github.com/joshuar/go-hass-anything/agent"
)

type MySystemApp struct{}

func (a *MySystemApp) Name() string {
    return "my_system"
}

func (a *MySystemApp) Configuration() agent.Configuration {
    return agent.Configuration{
        UniqueID: "my_system_app",
        Device: agent.Device{
            Name:        "My System",
            Identifiers: []string{"my_system"},
            Model:       "Custom App",
        },
    }
}

func (a *MySystemApp) States() []agent.State {
    return []agent.State{
        {
            EntityID:   "sensor.my_system_uptime",
            Name:       "System Uptime",
            State:      "42",
            Attributes: map[string]interface{}{"unit_of_measurement": "hours"},
        },
    }
}

func (a *MySystemApp) Subscriptions() []agent.Subscription {
    return nil // No subscriptions for this simple example
}

func (a *MySystemApp) Update(event agent.Event) error {
    // Handle updates from subscriptions if any
    return nil
}

func main() {
    app := &MySystemApp{}
    agent.Run(app)
}
```

### 3. Run the Agent

Start the Go Hass Anything agent:

```bash
go-hass-anything run
```

### 4. Reset Devices (Optional)

If you need to reset all devices and start fresh:

```bash
go-hass-anything clear
```

## Entity Types

Go Hass Anything supports the following Home Assistant entity types:

### Sensor
For numeric or string values:
```go
{
    EntityID: "sensor.cpu_temperature",
    Name:     "CPU Temperature",
    State:    "45.2",
    Attributes: map[string]interface{}{
        "unit_of_measurement": "°C",
        "device_class":       "temperature",
    },
}
```

### Binary Sensor
For on/off states:
```go
{
    EntityID:   "binary_sensor.is_online",
    Name:       "Is Online",
    State:      "on",
    Attributes: map[string]interface{}{
        "device_class": "connectivity",
    },
}
```

### Switch
For controllable switches:
```go
{
    EntityID:   "switch.my_lamp",
    Name:       "My Lamp",
    State:      "off",
    Attributes: map[string]interface{}{
        "icon": "mdi:lamp",
    },
}
```

### Button
For triggerable actions:
```go
{
    EntityID:   "button.restart_service",
    Name:       "Restart Service",
    State:      "",
    Attributes: map[string]interface{}{
        "icon": "mdi:restart",
    },
}
```

### Number
For numeric inputs:
```go
{
    EntityID:   "number.threshold_value",
    Name:       "Threshold Value",
    State:      "50",
    Attributes: map[string]interface{}{
        "min":      0,
        "max":      100,
        "step":     1,
        "unit_of_measurement": "%",
    },
}
```

### Text
For text input entities:
```go
{
    EntityID:   "text.custom_message",
    Name:       "Custom Message",
    State:      "Hello World",
    Attributes: map[string]interface{}{
        "max": 255,
    },
}
```

### Image
For image entities:
```go
{
    EntityID:   "image.screenshot",
    Name:       "Screenshot",
    State:      "/path/to/image.jpg",
    Attributes: map[string]interface{}{
        "url": "http://example.com/image.jpg",
    },
}
```

### Camera
For camera entities:
```go
{
    EntityID:   "camera.my_camera",
    Name:       "My Camera",
    State:      "recording",
    Attributes: map[string]interface{}{
        "access_token": "secure_token_here",
    },
}
```

## App Interfaces

### Core Interface (agent.App)

Every app must implement the `agent.App` interface:

```go
type App interface {
    Name() string
    Configuration() Configuration
    States() []State
    Subscriptions() []Subscription
    Update(event Event) error
}
```

#### Methods

- **Name()**: Returns a unique identifier for your app
- **Configuration()**: Defines the app's device configuration and metadata
- **States()**: Returns the current state of all entities managed by this app
- **Subscriptions()**: Returns MQTT topics to subscribe to for command handling
- **Update()**: Handles incoming MQTT messages and state changes

### Optional Interfaces

#### PollingApp (agent.PollingApp)

For apps that need to update at regular intervals:

```go
type PollingApp interface {
    App
    PollingInterval() time.Duration
}
```

#### EventsApp (agent.EventsApp)

For apps that respond to external events:

```go
type EventsApp interface {
    App
    Events() <-chan Event
}
```

#### AppWithPreferences (agent.AppWithPreferences)

For apps that support user preferences:

```go
type AppWithPreferences interface {
    App
    Preferences() Preferences
}
```

## Configuration

### Device Configuration

Define your app's device metadata:

```go
func (a *MyApp) Configuration() agent.Configuration {
    return agent.Configuration{
        UniqueID: "my_unique_app_id",
        Device: agent.Device{
            Name:         "My Custom Device",
            Identifiers:  []string{"my_device_v1"},
            Model:        "Custom Model",
            Manufacturer: "My Company",
            SwVersion:    "1.0.0",
        },
    }
}
```

### MQTT Topic Structure

The framework automatically handles MQTT topic creation:
- **State Topics**: `hass/<device>/<entity>/state`
- **Command Topics**: `hass/<device>/<entity>/set`
- **Availability Topics**: `hass/<device>/availability`

## Subscriptions and Commands

Handle incoming commands from Home Assistant:

```go
func (a *MyApp) Subscriptions() []agent.Subscription {
    return []agent.Subscription{
        {
            Topic:   "hass/my_device/switch_my_light/set",
            Handler: a.handleLightCommand,
        },
    }
}

func (a *MyApp) handleLightCommand(topic string, payload string) error {
    if payload == "ON" {
        // Turn light on
        return a.turnLightOn()
    } else if payload == "OFF" {
        // Turn light off
        return a.turnLightOff()
    }
    return nil
}

func (a *MyApp) Update(event agent.Event) error {
    // Handle the command and update state
    return nil
}
```

## Advanced Examples

### CPU Monitoring App

```go
package main

import (
    "time"
    "runtime"
    "github.com/joshuar/go-hass-anything/agent"
)

type CPUMonitorApp struct {
    lastUpdate time.Time
}

func (a *CPUMonitorApp) Name() string {
    return "cpu_monitor"
}

func (a *CPUMonitorApp) Configuration() agent.Configuration {
    return agent.Configuration{
        UniqueID: "cpu_monitor_app",
        Device: agent.Device{
            Name:        "CPU Monitor",
            Identifiers: []string{"cpu_monitor"},
            Model:       "System Monitor",
        },
    }
}

func (a *CPUMonitorApp) States() []agent.State {
    return []agent.State{
        {
            EntityID: "sensor.cpu_usage_percent",
            Name:     "CPU Usage",
            State:    "25.3",
            Attributes: map[string]interface{}{
                "unit_of_measurement": "%",
                "device_class":       "power_factor",
                "friendly_name":      "CPU Usage Percentage",
            },
        },
        {
            EntityID: "sensor.goroutines_count",
            Name:     "Goroutines",
            State:    "42",
            Attributes: map[string]interface{}{
                "unit_of_measurement": "count",
                "icon":                "mdi:counter",
            },
        },
    }
}

func (a *CPUMonitorApp) Subscriptions() []agent.Subscription {
    return nil // Read-only monitoring
}

func (a *CPUMonitorApp) Update(event agent.Event) error {
    a.lastUpdate = time.Now()
    return nil
}

func (a *CPUMonitorApp) PollingInterval() time.Duration {
    return 10 * time.Second // Update every 10 seconds
}

func main() {
    app := &CPUMonitorApp{lastUpdate: time.Now()}
    agent.Run(app)
}
```

### Network Ping Sensor App

```go
package main

import (
    "context"
    "net"
    "time"
    "github.com/joshuar/go-hass-anything/agent"
)

type PingSensorApp struct {
    target    string
    isOnline  bool
    lastCheck time.Time
}

func NewPingSensorApp(target string) *PingSensorApp {
    return &PingSensorApp{
        target: target,
    }
}

func (a *PingSensorApp) Name() string {
    return "ping_sensor"
}

func (a *PingSensorApp) Configuration() agent.Configuration {
    return agent.Configuration{
        UniqueID: "ping_sensor_app",
        Device: agent.Device{
            Name:        "Network Ping Sensor",
            Identifiers: []string{"ping_sensor"},
            Model:       "Connectivity Monitor",
        },
    }
}

func (a *PingSensorApp) States() []agent.State {
    state := "off"
    if a.isOnline {
        state = "on"
    }

    return []agent.State{
        {
            EntityID: "binary_sensor." + a.target + "_connectivity",
            Name:     a.target + " Connectivity",
            State:    state,
            Attributes: map[string]interface{}{
                "device_class": "connectivity",
                "friendly_name": a.target + " is Online",
                "last_check":   a.lastCheck.Format(time.RFC3339),
            },
        },
    }
}

func (a *PingSensorApp) Subscriptions() []agent.Subscription {
    return nil
}

func (a *PingSensorApp) Update(event agent.Event) error {
    return nil
}

func (a *PingSensorApp) PollingInterval() time.Duration {
    return 30 * time.Second
}

func (a *PingSensorApp) checkConnectivity() {
    ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
    defer cancel()

    conn, err := net.DialTimeout("tcp", a.target+":80", 5*time.Second)
    a.isOnline = (err == nil)
    a.lastCheck = time.Now()

    if conn != nil {
        conn.Close()
    }
}

func main() {
    app := NewPingSensorApp("google.com")
    agent.Run(app)
}
```

## Best Practices

### 1. Error Handling

Always handle errors gracefully:

```go
func (a *MyApp) Update(event agent.Event) error {
    if err := someOperation(); err != nil {
        // Log the error but don't crash the app
        return fmt.Errorf("operation failed: %w", err)
    }
    return nil
}
```

### 2. Resource Management

Be mindful of resource usage:

```go
func (a *MyApp) PollingInterval() time.Duration {
    // Don't poll too frequently to avoid resource waste
    return 30 * time.Second
}
```

### 3. Configuration Validation

Validate your configuration early:

```go
func (a *MyApp) Configuration() agent.Configuration {
    config := agent.Configuration{
        UniqueID: "my_app",
        // ... other config
    }

    if config.UniqueID == "" {
        panic("UniqueID cannot be empty")
    }

    return config
}
```

### 4. Thread Safety

Ensure your app is thread-safe when handling concurrent updates:

```go
type MyApp struct {
    mu     sync.RWMutex
    state  string
}

func (a *MyApp) States() []agent.State {
    a.mu.RLock()
    defer a.mu.RUnlock()

    return []agent.State{
        {
            EntityID: "sensor.my_state",
            State:    a.state,
        },
    }
}

func (a *MyApp) Update(event agent.Event) error {
    a.mu.Lock()
    defer a.mu.Unlock()

    a.state = event.Payload
    return nil
}
```

## Deployment

### Binary Deployment

The framework builds everything into a single binary:

```bash
# Build for current platform
mage build

# Cross-compile for ARM (Raspberry Pi)
mage build:arm

# Cross-compile for ARM64
mage build:arm64
```

### Container Deployment

Use the provided Dockerfile:

```dockerfile
FROM golang:1.19-alpine AS builder
WORKDIR /app
COPY . .
RUN mage build

FROM alpine:latest
RUN apk --no-cache add ca-certificates
COPY --from=builder /app/go-hass-anything /usr/local/bin/
CMD ["go-hass-anything", "run"]
```

### Systemd Service

Create a systemd service for automatic startup:

```ini
[Unit]
Description=Go Hass Anything
After=network.target

[Service]
Type=simple
User=gohass
WorkingDirectory=/opt/go-hass-anything
ExecStart=/opt/go-hass-anything/go-hass-anything run
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```

## Troubleshooting

### Common Issues

1. **MQTT Connection Failed**
   - Verify MQTT broker is running
   - Check network connectivity
   - Validate authentication credentials

2. **Entities Not Appearing in Home Assistant**
   - Ensure MQTT integration is enabled in Home Assistant
   - Check discovery topics are being published
   - Verify device configuration

3. **High CPU/Memory Usage**
   - Optimize polling intervals
   - Check for memory leaks in your app
   - Monitor resource usage with system tools

### Debug Logging

Enable debug logging for troubleshooting:

```bash
# Set log level
export GO_HASS_LOG_LEVEL=debug
go-hass-anything run
```

## Related Projects

- **Go Hass Agent**: A complete system monitoring solution that uses Go Hass Anything under the hood
- **Home Assistant MQTT Discovery**: The MQTT discovery specification that powers the automatic entity creation

## License

Go Hass Anything is licensed under the MIT License. See the LICENSE file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

## Support

- **GitHub Issues**: [Report bugs and request features](https://github.com/joshuar/go-hass-anything/issues)
- **Documentation**: [Check the repository wiki](https://github.com/joshuar/go-hass-anything/wiki)

---

*This guide covers Go Hass Anything framework for creating custom Home Assistant integrations using Go and MQTT.*