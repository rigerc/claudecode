# Go Hass Anything Getting Started Guide

## Prerequisites

- **Go 1.19+** installed for development
- **MQTT Broker** (Mosquitto recommended)
- **Home Assistant** with MQTT integration enabled
- **Mage** build system (`go install github.com/magefile/mage@latest`)

## Initial Setup

### 1. Project Setup

```bash
git clone https://github.com/joshuar/go-hass-anything.git
cd go-hass-anything

# Install dependencies
go mod tidy

# Build the project
mage -d build/magefiles -w . build:full
```

### 2. MQTT Configuration

Configure the connection to your MQTT broker:

```bash
go-hass-anything configure
```

This will prompt for:
- MQTT broker address (e.g., `localhost:1883`)
- Username and password (if required)
- TLS settings (if using secure connection)
- Client identification details

### 3. Home Assistant Setup

Ensure MQTT integration is enabled in Home Assistant:

1. Go to **Settings** → **Devices & Services**
2. Click **+ Add Integration**
3. Search for and select **MQTT**
4. Configure with your broker details
5. Enable **Enable discovery** if not already on

## Creating Your First App

### Basic App Structure

Create a new file in `apps/yourapp/main.go`:

```go
package main

import (
    "github.com/joshuar/go-hass-anything/agent"
)

type YourApp struct{}

func (a *YourApp) Name() string {
    return "your_app_unique_id"
}

func (a *YourApp) Configuration() agent.Configuration {
    return agent.Configuration{
        UniqueID: "your_app_unique_id",
        Device: agent.Device{
            Name:        "Your App Device",
            Identifiers: []string{"your_app_device"},
            Model:       "Custom Integration",
        },
    }
}

func (a *YourApp) States() []agent.State {
    return []agent.State{
        {
            EntityID: "sensor.your_sensor",
            Name:     "Your Sensor",
            State:    "42",
            Attributes: map[string]interface{}{
                "unit_of_measurement": "units",
                "friendly_name":      "Your Custom Sensor",
            },
        },
    }
}

func (a *YourApp) Subscriptions() []agent.Subscription {
    return nil // No commands to handle
}

func (a *YourApp) Update(event agent.Event) error {
    // Handle incoming commands if any
    return nil
}

func main() {
    app := &YourApp{}
    agent.Run(app)
}
```

### Running Your App

```bash
# Start the go-hass-anything agent
go-hass-anything run
```

Your entities should automatically appear in Home Assistant via MQTT discovery!

## Entity Types Reference

### Sensor (Numeric/String Values)

```go
{
    EntityID: "sensor.temperature",
    Name:     "Temperature",
    State:    "23.5",
    Attributes: map[string]interface{}{
        "unit_of_measurement": "°C",
        "device_class":       "temperature",
        "state_class":        "measurement",
    },
}
```

### Binary Sensor (On/Off States)

```go
{
    EntityID: "binary_sensor.motion_detected",
    Name:     "Motion Detected",
    State:    "on",
    Attributes: map[string]interface{}{
        "device_class": "motion",
    },
}
```

### Switch (Controllable Power)

```go
{
    EntityID: "switch.my_light",
    Name:     "My Light",
    State:    "off",
    Attributes: map[string]interface{}{
        "icon": "mdi:lightbulb",
    },
}
```

### Button (Action Trigger)

```go
{
    EntityID: "button.restart_service",
    Name:     "Restart Service",
    State:    "",
    Attributes: map[string]interface{}{
        "icon": "mdi:restart",
    },
}
```

## Common Interfaces

### Polling Apps

For apps that update at regular intervals:

```go
type PollingApp interface {
    App
    PollingInterval() time.Duration
}

func (a *YourApp) PollingInterval() time.Duration {
    return 30 * time.Second // Update every 30 seconds
}
```

### Event-Driven Apps

For apps that respond to external events:

```go
type EventsApp interface {
    App
    Events() <-chan Event
}

func (a *YourApp) Events() <-chan Event {
    eventChan := make(chan Event)
    go func() {
        // Generate events based on external triggers
        for {
            // Your event generation logic here
            eventChan <- Event{Type: "custom_event", Data: "..."}
            time.Sleep(time.Minute)
        }
    }()
    return eventChan
}
```

### Apps with Preferences

For apps that support user configuration:

```go
type AppWithPreferences interface {
    App
    Preferences() Preferences
}

func (a *YourApp) Preferences() Preferences {
    return Preferences{
        "update_interval": "30s",
        "threshold_value": "50",
        "debug_mode":      "false",
    }
}
```

## Building and Deployment

### Build for Current Platform

```bash
mage build
```

### Cross-Compile

```bash
# ARM (Raspberry Pi 3/4)
mage build:arm

# ARM64 (Raspberry Pi 4 64-bit, ARM servers)
mage build:arm64

# Windows
mage build:windows

# macOS
mage build:darwin
```

### Container Deployment

```dockerfile
FROM golang:1.19-alpine AS builder
WORKDIR /app
COPY . .
RUN mage build

FROM alpine:latest
RUN apk --no-cache add ca-certificates tzdata
COPY --from=builder /app/go-hass-anything /usr/local/bin/
COPY config.toml /etc/go-hass-anything/config.toml
CMD ["go-hass-anything", "run"]
```

## Configuration File

Create a `config.toml` file:

```toml
[mqtt]
broker = "localhost:1883"
username = "your_username"
password = "your_password"
client_id = "go-hass-anything"
discovery_prefix = "homeassistant"
state_prefix = "go-hass"

[agent]
apps_dir = "./apps"
log_level = "info"
```

## Troubleshooting

### Common Issues

1. **Entities Not Appearing**
   - Check MQTT broker connection
   - Verify Home Assistant MQTT discovery is enabled
   - Check log output for errors

2. **Connection Refused**
   - Ensure MQTT broker is running
   - Check firewall settings
   - Verify broker address and port

3. **Authentication Failed**
   - Double-check username/password
   - Verify user has permissions to publish/subscribe

### Debug Mode

Enable debug logging:

```bash
export GO_HASS_LOG_LEVEL=debug
go-hass-anything run
```

### MQTT Topic Inspection

Use an MQTT client like `mosquitto_sub` to inspect topics:

```bash
# Monitor discovery messages
mosquitto_sub -h localhost -t "homeassistant/+/+/config"

# Monitor state updates
mosquitto_sub -h localhost -t "go-hass/+/+/state"
```

## Next Steps

- Explore the [API Reference](api-reference.md) for detailed interface documentation
- Check [Examples](examples.md) for complete app implementations
- Review [Best Practices](best-practices.md) for production-ready code