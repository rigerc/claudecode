---
name: go-hass-anything
version: "1.0.0"
description: Use when developing Go applications for Home Assistant integration via MQTT using the go-hass-anything framework. Expert guidance for creating sensors, switches, and custom entities.
author: Claude Code
keywords:
  - go-hass-anything
  - home assistant
  - mqtt
  - golang
  - home automation
---

# Go Hass Anything Development Expert

Use when developing Go applications that integrate with Home Assistant via MQTT using the go-hass-anything framework.

## When to Use

- Creating new Home Assistant integrations with Go
- Writing apps that send data to Home Assistant via MQTT
- Developing custom sensors, switches, or controls for Home Assistant
- Implementing polling or event-based home automation in Go
- Troubleshooting go-hass-anything applications

## Core Expertise

- App development using the agent.App interface
- Entity type configuration (sensor, binary_sensor, switch, button, etc.)
- MQTT integration and Home Assistant discovery
- TOML configuration and BubbleTea UI setup
- Cross-platform deployment and resource optimization
- Error handling and best practices

## Quick Reference

**Interface**: `agent.App` with methods: Name(), Configuration(), States(), Subscriptions(), Update()
**Build**: `mage build` (current), `mage build:arm` (Raspberry Pi), `mage build:arm64` (64-bit ARM)
**Run**: `go-hass-anything configure` → `go-hass-anything run`

## Quick Start

1. **Install**: `git clone https://github.com/joshuar/go-hass-anything.git && mage build`
2. **Configure**: `go-hass-anything configure` (sets up MQTT connection)
3. **Create App**: Implement `agent.App` interface with `Name()`, `Configuration()`, `States()`, `Subscriptions()`, `Update()` methods
4. **Run**: `go-hass-anything run` (apps in `apps/` directory auto-load)

## Common Patterns

- **Polling Apps**: Implement `PollingApp` interface with `PollingInterval()`
- **Event Apps**: Implement `EventsApp` interface with `Events()` channel
- **Preferences**: Use `AppWithPreferences` for user-configurable settings
- **Commands**: Handle MQTT subscriptions in `Subscriptions()` method

## References

- **[Getting Started Guide](references/getting-started.md)**: Setup, first app, entity types, and deployment
- **[API Reference](references/api-reference.md)**: Complete interface documentation and data structures
- **[Examples](references/examples.md)**: Complete app implementations for various use cases
- **[Troubleshooting](references/troubleshooting.md)**: Common issues and debugging techniques