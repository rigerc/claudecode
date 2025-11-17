# Go Hass Anything API Reference

## Core Interfaces

### agent.App

The main interface that all apps must implement.

```go
type App interface {
    // Returns a unique identifier for this app
    Name() string

    // Returns device configuration and metadata
    Configuration() Configuration

    // Returns current state of all entities
    States() []State

    // Returns MQTT subscriptions for command handling
    Subscriptions() []Subscription

    // Handles incoming MQTT events and commands
    Update(event Event) error
}
```

#### Methods

##### Name() string
- **Returns**: Unique string identifier for the app
- **Purpose**: Used for logging and internal identification
- **Example**: `"cpu_monitor"`, `"network_ping"`

##### Configuration() Configuration
- **Returns**: Device and app configuration metadata
- **Purpose**: Defines how the app appears in Home Assistant
- **Structure**:
```go
type Configuration struct {
    UniqueID string
    Device   Device
}

type Device struct {
    Name         string
    Identifiers  []string
    Model        string
    Manufacturer string
    SwVersion    string
}
```

##### States() []State
- **Returns**: Array of entity states to publish to Home Assistant
- **Purpose**: Defines all entities this app manages
- **Called**: Periodically or when state changes

##### Subscriptions() []Subscription
- **Returns**: MQTT topics to subscribe to for commands
- **Purpose**: Enables two-way communication with Home Assistant
- **Example**: Switch controls, button presses

##### Update(event Event) error
- **Parameters**: Event containing MQTT message data
- **Returns**: Error if update fails
- **Purpose**: Process incoming commands and update internal state

### agent.PollingApp (Optional)

For apps that update at regular intervals.

```go
type PollingApp interface {
    App
    PollingInterval() time.Duration
}
```

#### PollingInterval() time.Duration
- **Returns**: Duration between automatic state updates
- **Example**: `30 * time.Second`, `5 * time.Minute`

### agent.EventsApp (Optional)

For apps that respond to external events.

```go
type EventsApp interface {
    App
    Events() <-chan Event
}
```

#### Events() <-chan Event
- **Returns**: Channel that delivers external events
- **Purpose**: Respond to system events, file changes, etc.

### agent.AppWithPreferences (Optional)

For apps with user-configurable settings.

```go
type AppWithPreferences interface {
    App
    Preferences() Preferences
}
```

#### Preferences() Preferences
- **Returns**: Map of user preferences with defaults
- **Purpose**: Enable BubbleTea UI for configuration

## Data Structures

### State

Represents a Home Assistant entity state.

```go
type State struct {
    EntityID   string                 // Home Assistant entity ID
    Name       string                 // Display name
    State      string                 // Current state value
    Attributes map[string]interface{} // Entity attributes
}
```

#### Entity ID Patterns

- `sensor.<device_name>_<sensor_name>`
- `binary_sensor.<device_name>_<sensor_name>`
- `switch.<device_name>_<switch_name>`
- `button.<device_name>_<button_name>`
- `number.<device_name>_<number_name>`
- `text.<device_name>_<text_name>`
- `image.<device_name>_<image_name>`
- `camera.<device_name>_<camera_name>`

#### Common Attributes

**Sensor Attributes:**
```go
Attributes: map[string]interface{}{
    "unit_of_measurement": "°C",
    "device_class":       "temperature",
    "state_class":        "measurement",
    "friendly_name":      "Temperature Sensor",
    "icon":               "mdi:thermometer",
}
```

**Binary Sensor Attributes:**
```go
Attributes: map[string]interface{}{
    "device_class": "motion",
    "friendly_name": "Motion Detector",
    "icon":         "mdi:motion-sensor",
}
```

**Switch Attributes:**
```go
Attributes: map[string]interface{}{
    "friendly_name": "Kitchen Light",
    "icon":          "mdi:lightbulb",
    "assumed_state": false,
}
```

### Subscription

Defines MQTT topic subscriptions for receiving commands.

```go
type Subscription struct {
    Topic   string
    Handler func(topic string, payload string) error
}
```

#### Topic Structure

Command topics follow the pattern: `go-hass/<device_name>/<entity_id>/set`

**Examples:**
- `go-hass/my_device/switch_kitchen_light/set`
- `go-hass/my_device/button_restart/set`
- `go-hass/my_device/number_brightness/set`

### Event

Represents an incoming MQTT event.

```go
type Event struct {
    Topic   string // MQTT topic
    Payload string // Message payload
    Time    time.Time
}
```

#### Common Payload Values

- **Switch/Binary Sensor**: `"ON"`, `"OFF"`
- **Button**: Empty string `""` (trigger-only)
- **Number`: Numeric value as string `"50"`
- **Text**: Text value `"Hello World"`

## Entity Type Specifications

### Sensor (sensor.*)

For numeric or string measurements.

```go
{
    EntityID: "sensor.cpu_temperature",
    Name:     "CPU Temperature",
    State:    "45.2",
    Attributes: map[string]interface{}{
        "unit_of_measurement": "°C",
        "device_class":       "temperature",
        "state_class":        "measurement",
    },
}
```

**Supported Device Classes:**
- `temperature`, `humidity`, `pressure`
- `voltage`, `current`, `power`
- `signal_strength`, `battery`
- `duration`, `timestamp`

### Binary Sensor (binary_sensor.*)

For on/off or yes/no states.

```go
{
    EntityID: "binary_sensor.door_open",
    Name:     "Door Open",
    State:    "off",
    Attributes: map[string]interface{}{
        "device_class": "door",
    },
}
```

**Supported Device Classes:**
- `door`, `window`, `motion`
- `connectivity`, `presence`
- `battery_charging`, `pluggable`
- `lock`, `power`

### Switch (switch.*)

For controllable on/off devices.

```go
{
    EntityID: "switch.living_room_light",
    Name:     "Living Room Light",
    State:    "on",
    Attributes: map[string]interface{}{
        "icon": "mdi:lightbulb-outline",
    },
}
```

### Button (button.*)

For momentary action triggers.

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

### Number (number.*)

For numeric input controls.

```go
{
    EntityID: "number.brightness",
    Name:     "Brightness",
    State:    "75",
    Attributes: map[string]interface{}{
        "min":               0,
        "max":               100,
        "step":              1,
        "unit_of_measurement": "%",
        "mode":              "slider", // "slider" or "box"
    },
}
```

### Text (text.*)

For text input entities.

```go
{
    EntityID: "text.custom_message",
    Name:     "Custom Message",
    State:    "Hello World",
    Attributes: map[string]interface{}{
        "min": 1,
        "max": 255,
        "mode": "text", // "text" or "password"
    },
}
```

### Image (image.*)

For image entities.

```go
{
    EntityID: "image.screenshot",
    Name:     "Screenshot",
    State:    "/path/to/image.jpg",
    Attributes: map[string]interface{}{
        "url":          "http://example.com/image.jpg",
        "content_type": "image/jpeg",
    },
}
```

### Camera (camera.*)

For camera entities.

```go
{
    EntityID: "camera.front_door",
    Name:     "Front Door Camera",
    State:    "recording",
    Attributes: map[string]interface{}{
        "access_token": "secure_token_here",
        "stream_source": "rtsp://camera/stream",
    },
}
```

## MQTT Discovery

The framework automatically publishes MQTT discovery messages that Home Assistant uses to auto-configure entities.

### Discovery Topic Format

`homeassistant/<component>/<object_id>/<unique_id>/config`

**Example:**
`homeassistant/sensor/my_app_cpu_temperature/unique_id/config`

### Discovery Message Structure

```json
{
    "name": "CPU Temperature",
    "unique_id": "my_app_cpu_temperature",
    "state_topic": "go-hass/my_app/sensor_cpu_temperature/state",
    "device": {
        "name": "My App",
        "identifiers": ["my_app"],
        "model": "Custom Integration"
    },
    "unit_of_measurement": "°C",
    "device_class": "temperature"
}
```

## Configuration Options

### Agent Configuration

```toml
[mqtt]
broker = "localhost:1883"
username = ""
password = ""
client_id = "go-hass-anything"
discovery_prefix = "homeassistant"
state_prefix = "go-hass"
qos = 0
retain = false
clean_session = true

[agent]
apps_dir = "./apps"
log_level = "info"
update_interval = "30s"

[discovery]
enabled = true
ttl = "3600s"
```

### TLS Configuration

```toml
[mqtt.tls]
enabled = true
ca_cert = "/path/to/ca.crt"
client_cert = "/path/to/client.crt"
client_key = "/path/to/client.key"
insecure_skip_verify = false
```

### Connection Options

```toml
[mqtt.connection]
keep_alive = "60s"
ping_timeout = "10s"
write_timeout = "10s"
read_timeout = "30s"
max_reconnect_interval = "10m"
auto_reconnect = true
```

## Error Handling

### Common Error Types

```go
type AppError struct {
    Code    string
    Message string
    Cause   error
}

func (e *AppError) Error() string {
    if e.Cause != nil {
        return fmt.Sprintf("%s: %s (caused by: %v)", e.Code, e.Message, e.Cause)
    }
    return fmt.Sprintf("%s: %s", e.Code, e.Message)
}
```

### Error Codes

- `ERR_MQTT_CONNECTION`: Failed to connect to MQTT broker
- `ERR_CONFIG_INVALID`: Invalid configuration
- `ERR_STATE_UPDATE`: Failed to update entity state
- `ERR_SUBSCRIPTION`: Failed to subscribe to command topic
- `ERR_APP_PANIC`: App panicked during execution

### Error Handling Patterns

```go
func (a *MyApp) Update(event agent.Event) error {
    if err := a.handleCommand(event); err != nil {
        // Log error but don't crash the app
        log.Printf("Command failed: %v", err)
        return &agent.AppError{
            Code:    "ERR_COMMAND_FAILED",
            Message: "Failed to process command",
            Cause:   err,
        }
    }
    return nil
}
```

## Logging

### Log Levels

- `debug`: Detailed debugging information
- `info`: General information messages
- `warn`: Warning messages
- `error`: Error messages
- `fatal`: Fatal errors (causes app to exit)

### Logging in Apps

```go
import "log"

func (a *MyApp) Update(event agent.Event) error {
    log.Printf("Received command on topic %s: %s", event.Topic, event.Payload)
    // Your logic here
    return nil
}
```

### Structured Logging (Optional)

```go
import "github.com/sirupsen/logrus"

var logger = logrus.New()

func (a *MyApp) Update(event agent.Event) error {
    logger.WithFields(logrus.Fields{
        "topic":   event.Topic,
        "payload": event.Payload,
        "app":     a.Name(),
    }).Info("Processing command")
    return nil
}
```