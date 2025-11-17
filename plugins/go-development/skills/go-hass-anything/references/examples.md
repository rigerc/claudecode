# Go Hass Anything Examples

## Table of Contents

1. [Simple Sensor App](#simple-sensor-app)
2. [System Monitor App](#system-monitor-app)
3. [Network Ping Monitor](#network-ping-monitor)
4. [Smart Switch Controller](#smart-switch-controller)
5. [File Watcher App](#file-watcher-app)
6. [Weather Station App](#weather-station-app)
7. [MQTT Bridge App](#mqtt-bridge-app)

## Simple Sensor App

A basic app that publishes static sensor data.

```go
package main

import (
    "github.com/joshuar/go-hass-anything/agent"
)

type SimpleSensorApp struct{}

func (a *SimpleSensorApp) Name() string {
    return "simple_sensor"
}

func (a *SimpleSensorApp) Configuration() agent.Configuration {
    return agent.Configuration{
        UniqueID: "simple_sensor_app",
        Device: agent.Device{
            Name:        "Simple Sensor Device",
            Identifiers: []string{"simple_sensor"},
            Model:       "Example App",
        },
    }
}

func (a *SimpleSensorApp) States() []agent.State {
    return []agent.State{
        {
            EntityID: "sensor.temperature",
            Name:     "Temperature",
            State:    "23.5",
            Attributes: map[string]interface{}{
                "unit_of_measurement": "°C",
                "device_class":       "temperature",
                "friendly_name":      "Room Temperature",
            },
        },
        {
            EntityID: "sensor.humidity",
            Name:     "Humidity",
            State:    "65.2",
            Attributes: map[string]interface{}{
                "unit_of_measurement": "%",
                "device_class":       "humidity",
                "friendly_name":      "Room Humidity",
            },
        },
    }
}

func (a *SimpleSensorApp) Subscriptions() []agent.Subscription {
    return nil
}

func (a *SimpleSensorApp) Update(event agent.Event) error {
    return nil
}

func main() {
    app := &SimpleSensorApp{}
    agent.Run(app)
}
```

## System Monitor App

An app that monitors system resources with polling.

```go
package main

import (
    "fmt"
    "runtime"
    "time"
    "github.com/joshuar/go-hass-anything/agent"
)

type SystemMonitorApp struct {
    startTime time.Time
}

func NewSystemMonitorApp() *SystemMonitorApp {
    return &SystemMonitorApp{
        startTime: time.Now(),
    }
}

func (a *SystemMonitorApp) Name() string {
    return "system_monitor"
}

func (a *SystemMonitorApp) Configuration() agent.Configuration {
    return agent.Configuration{
        UniqueID: "system_monitor_app",
        Device: agent.Device{
            Name:        "System Monitor",
            Identifiers: []string{"system_monitor"},
            Model:       "Resource Monitor",
            Manufacturer: "Go Hass Anything",
            SwVersion:   "1.0.0",
        },
    }
}

func (a *SystemMonitorApp) States() []agent.State {
    var m runtime.MemStats
    runtime.ReadMemStats(&m)

    uptime := time.Since(a.startTime)

    return []agent.State{
        {
            EntityID: "sensor.cpu_usage_percent",
            Name:     "CPU Usage",
            State:    "25.3", // In real app, calculate actual CPU usage
            Attributes: map[string]interface{}{
                "unit_of_measurement": "%",
                "device_class":       "power_factor",
                "friendly_name":      "CPU Usage",
                "icon":               "mdi:cpu-64-bit",
            },
        },
        {
            EntityID: "sensor.memory_usage_mb",
            Name:     "Memory Usage",
            State:    fmt.Sprintf("%.1f", float64(m.Alloc)/1024/1024),
            Attributes: map[string]interface{}{
                "unit_of_measurement": "MB",
                "friendly_name":      "Memory Usage",
                "icon":               "mdi:memory",
            },
        },
        {
            EntityID: "sensor.goroutines_count",
            Name:     "Goroutines",
            State:    fmt.Sprintf("%d", runtime.NumGoroutine()),
            Attributes: map[string]interface{}{
                "unit_of_measurement": "count",
                "friendly_name":      "Active Goroutines",
                "icon":               "mdi:counter",
            },
        },
        {
            EntityID: "sensor.uptime_hours",
            Name:     "Uptime",
            State:    fmt.Sprintf("%.1f", uptime.Hours()),
            Attributes: map[string]interface{}{
                "unit_of_measurement": "h",
                "device_class":       "duration",
                "friendly_name":      "System Uptime",
                "icon":               "mdi:timer",
            },
        },
    }
}

func (a *SystemMonitorApp) Subscriptions() []agent.Subscription {
    return nil
}

func (a *SystemMonitorApp) Update(event agent.Event) error {
    return nil
}

func (a *SystemMonitorApp) PollingInterval() time.Duration {
    return 30 * time.Second
}

func main() {
    app := NewSystemMonitorApp()
    agent.Run(app)
}
```

## Network Ping Monitor

An app that monitors network connectivity to multiple hosts.

```go
package main

import (
    "context"
    "fmt"
    "net"
    "sync"
    "time"
    "github.com/joshuar/go-hass-anything/agent"
)

type PingMonitorApp struct {
    hosts    []string
    status   map[string]bool
    lastPing map[string]time.Time
    mu       sync.RWMutex
}

func NewPingMonitorApp(hosts []string) *PingMonitorApp {
    return &PingMonitorApp{
        hosts:    hosts,
        status:   make(map[string]bool),
        lastPing: make(map[string]time.Time),
    }
}

func (a *PingMonitorApp) Name() string {
    return "ping_monitor"
}

func (a *PingMonitorApp) Configuration() agent.Configuration {
    return agent.Configuration{
        UniqueID: "ping_monitor_app",
        Device: agent.Device{
            Name:        "Network Ping Monitor",
            Identifiers: []string{"ping_monitor"},
            Model:       "Connectivity Monitor",
        },
    }
}

func (a *PingMonitorApp) States() []agent.State {
    a.mu.RLock()
    defer a.mu.RUnlock()

    var states []agent.State
    now := time.Now()

    for _, host := range a.hosts {
        isOnline := a.status[host]
        lastPing := a.lastPing[host]

        // Generate safe entity ID
        safeHost := fmt.Sprintf("%s", strings.ReplaceAll(host, ".", "_"))

        state := "off"
        if isOnline {
            state = "on"
        }

        attributes := map[string]interface{}{
            "device_class": "connectivity",
            "friendly_name": fmt.Sprintf("%s Connectivity", host),
        }

        if !lastPing.IsZero() {
            attributes["last_check"] = lastPing.Format(time.RFC3339)
            attributes["seconds_since_check"] = int(now.Sub(lastPing).Seconds())
        }

        states = append(states, agent.State{
            EntityID:   fmt.Sprintf("binary_sensor.%s_connectivity", safeHost),
            Name:       fmt.Sprintf("%s Connectivity", host),
            State:      state,
            Attributes: attributes,
        })
    }

    return states
}

func (a *PingMonitorApp) Subscriptions() []agent.Subscription {
    return nil
}

func (a *PingMonitorApp) Update(event agent.Event) error {
    return nil
}

func (a *PingMonitorApp) PollingInterval() time.Duration {
    return 60 * time.Second
}

func (a *PingMonitorApp) checkHost(host string) {
    ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
    defer cancel()

    // Try to connect to port 80 (commonly open)
    conn, err := net.DialTimeout("tcp", host+":80", 5*time.Second)

    a.mu.Lock()
    defer a.mu.Unlock()

    a.status[host] = (err == nil)
    a.lastPing[host] = time.Now()

    if conn != nil {
        conn.Close()
    }
}

func (a *PingMonitorApp) checkAllHosts() {
    var wg sync.WaitGroup

    for _, host := range a.hosts {
        wg.Add(1)
        go func(h string) {
            defer wg.Done()
            a.checkHost(h)
        }(host)
    }

    wg.Wait()
}

func main() {
    hosts := []string{
        "google.com",
        "github.com",
        "home-assistant.io",
        "8.8.8.8", // Google DNS
    }

    app := NewPingMonitorApp(hosts)

    // Perform initial check
    app.checkAllHosts()

    agent.Run(app)
}
```

## Smart Switch Controller

An app that controls smart switches via MQTT and responds to Home Assistant commands.

```go
package main

import (
    "fmt"
    "mqtt"
    "sync"
    "github.com/joshuar/go-hass-anything/agent"
)

type SmartSwitchApp struct {
    switches map[string]*SwitchState
    mu       sync.RWMutex
    mqttClient mqtt.Client
}

type SwitchState struct {
    Name    string
    State   bool
    Topic   string
    Icon    string
}

func NewSmartSwitchApp(mqttBroker string) *SmartSwitchApp {
    opts := mqtt.NewClientOptions().SetBroker(mqttBroker)
    client := mqtt.NewClient(opts)

    app := &SmartSwitchApp{
        switches: make(map[string]*SwitchState),
        mqttClient: client,
    }

    // Initialize switches
    app.switches["living_room"] = &SwitchState{
        Name:  "Living Room Light",
        State: false,
        Topic: "home/living_room/light",
        Icon:  "mdi:lightbulb",
    }

    app.switches["bedroom"] = &SwitchState{
        Name:  "Bedroom Light",
        State: false,
        Topic: "home/bedroom/light",
        Icon:  "mdi:lightbulb-outline",
    }

    return app
}

func (a *SmartSwitchApp) Name() string {
    return "smart_switch"
}

func (a *SmartSwitchApp) Configuration() agent.Configuration {
    return agent.Configuration{
        UniqueID: "smart_switch_app",
        Device: agent.Device{
            Name:        "Smart Switch Controller",
            Identifiers: []string{"smart_switch"},
            Model:       "MQTT Switch Controller",
        },
    }
}

func (a *SmartSwitchApp) States() []agent.State {
    a.mu.RLock()
    defer a.mu.RUnlock()

    var states []agent.State

    for id, sw := range a.switches {
        state := "off"
        if sw.State {
            state = "on"
        }

        states = append(states, agent.State{
            EntityID: fmt.Sprintf("switch.%s_light", id),
            Name:     sw.Name,
            State:    state,
            Attributes: map[string]interface{}{
                "icon":          sw.Icon,
                "friendly_name": sw.Name,
                "command_topic": sw.Topic + "/set",
            },
        })
    }

    return states
}

func (a *SmartSwitchApp) Subscriptions() []agent.Subscription {
    a.mu.RLock()
    defer a.mu.RUnlock()

    var subs []agent.Subscription

    for id, sw := range a.switches {
        topic := fmt.Sprintf("go-hass/smart_switch/switch_%s_light/set", id)
        subs = append(subs, agent.Subscription{
            Topic: topic,
            Handler: func(t string, p string) error {
                return a.handleSwitchCommand(id, p)
            },
        })
    }

    return subs
}

func (a *SmartSwitchApp) handleSwitchCommand(switchID string, payload string) error {
    a.mu.Lock()
    defer a.mu.Unlock()

    sw, exists := a.switches[switchID]
    if !exists {
        return fmt.Errorf("unknown switch: %s", switchID)
    }

    // Parse command
    newState := false
    if payload == "ON" {
        newState = true
    } else if payload == "OFF" {
        newState = false
    } else {
        return fmt.Errorf("invalid payload: %s", payload)
    }

    // Update local state
    sw.State = newState

    // Send command to actual device via MQTT
    command := "OFF"
    if newState {
        command = "ON"
    }

    token := a.mqttClient.Publish(sw.Topic+"/set", 0, false, command)
    if token.Wait() && token.Error() != nil {
        return fmt.Errorf("failed to send MQTT command: %w", token.Error())
    }

    return nil
}

func (a *SmartSwitchApp) Update(event agent.Event) error {
    // Commands are handled in Subscriptions, this is called after
    return nil
}

func main() {
    app := NewSmartSwitchApp("tcp://localhost:1883")

    // Connect to MQTT
    if token := app.mqttClient.Connect(); token.Wait() && token.Error() != nil {
        panic(fmt.Sprintf("Failed to connect to MQTT: %v", token.Error()))
    }
    defer app.mqttClient.Disconnect(250)

    agent.Run(app)
}
```

## File Watcher App

An app that monitors files and directories for changes.

```go
package main

import (
    "fmt"
    "os"
    "path/filepath"
    "strings"
    "time"
    "github.com/joshuar/go-hass-anything/agent"
)

type FileWatcherApp struct {
    watchPaths []string
    fileStates map[string]*FileState
}

type FileState struct {
    Path     string
    Size     int64
    ModTime  time.Time
    Exists   bool
    IsDir    bool
}

func NewFileWatcherApp(paths []string) *FileWatcherApp {
    return &FileWatcherApp{
        watchPaths: paths,
        fileStates: make(map[string]*FileState),
    }
}

func (a *FileWatcherApp) Name() string {
    return "file_watcher"
}

func (a *FileWatcherApp) Configuration() agent.Configuration {
    return agent.Configuration{
        UniqueID: "file_watcher_app",
        Device: agent.Device{
            Name:        "File Watcher",
            Identifiers: []string{"file_watcher"},
            Model:       "File System Monitor",
        },
    }
}

func (a *FileWatcherApp) States() []agent.State {
    var states []agent.State

    for i, path := range a.watchPaths {
        info, err := os.Stat(path)
        exists := err == nil

        // Generate safe entity ID
        safeName := fmt.Sprintf("path_%d", i)
        if i == 0 {
            safeName = "main_path"
        }

        var fileSizeStr string
        if exists && !info.IsDir() {
            fileSizeStr = fmt.Sprintf("%.1f", float64(info.Size())/1024) // KB
        } else if exists {
            fileSizeStr = "0"
        } else {
            fileSizeStr = "0"
        }

        // Binary sensor for existence
        existenceState := "off"
        if exists {
            existenceState = "on"
        }

        states = append(states, agent.State{
            EntityID: fmt.Sprintf("binary_sensor.%s_exists", safeName),
            Name:     fmt.Sprintf("%s Exists", path),
            State:    existenceState,
            Attributes: map[string]interface{}{
                "device_class":  "presence",
                "friendly_name": fmt.Sprintf("%s Exists", path),
                "file_path":     path,
            },
        })

        // Sensor for file size
        states = append(states, agent.State{
            EntityID: fmt.Sprintf("sensor.%s_size", safeName),
            Name:     fmt.Sprintf("%s Size", path),
            State:    fileSizeStr,
            Attributes: map[string]interface{}{
                "unit_of_measurement": "KB",
                "friendly_name":      fmt.Sprintf("%s Size", path),
                "file_path":          path,
                "icon":               "mdi:file",
            },
        })

        // Sensor for last modified time
        if exists {
            states = append(states, agent.State{
                EntityID: fmt.Sprintf("sensor.%s_last_modified", safeName),
                Name:     fmt.Sprintf("%s Last Modified", path),
                State:    info.ModTime().Format(time.RFC3339),
                Attributes: map[string]interface{}{
                    "device_class":  "timestamp",
                    "friendly_name": fmt.Sprintf("%s Last Modified", path),
                    "file_path":     path,
                    "icon":          "mdi:clock",
                },
            })
        }
    }

    return states
}

func (a *FileWatcherApp) Subscriptions() []agent.Subscription {
    return nil
}

func (a *FileWatcherApp) Update(event agent.Event) error {
    return nil
}

func (a *FileWatcherApp) PollingInterval() time.Duration {
    return 10 * time.Second
}

func main() {
    // Example: monitor home directory, log files, and config files
    paths := []string{
        os.Getenv("HOME"),
        "/var/log/syslog",
        "/etc/hosts",
    }

    // Expand ~ in paths
    for i, path := range paths {
        if strings.HasPrefix(path, "~/") {
            home := os.Getenv("HOME")
            paths[i] = filepath.Join(home, path[2:])
        }
    }

    app := NewFileWatcherApp(paths)
    agent.Run(app)
}
```

## Weather Station App

An app that simulates weather data (in real app, connect to weather API).

```go
package main

import (
    "fmt"
    "math/rand"
    "time"
    "github.com/joshuar/go-hass-anything/agent"
)

type WeatherStationApp struct {
    location string
    data     WeatherData
    rng      *rand.Rand
}

type WeatherData struct {
    Temperature    float64
    Humidity       float64
    Pressure       float64
    WindSpeed      float64
    WindDirection  string
    Condition      string
    LastUpdate     time.Time
}

func NewWeatherStationApp(location string) *WeatherStationApp {
    return &WeatherStationApp{
        location: location,
        data: WeatherData{
            Temperature:   20.0,
            Humidity:      50.0,
            Pressure:      1013.25,
            WindSpeed:     5.0,
            WindDirection: "N",
            Condition:     "partly_cloudy",
            LastUpdate:    time.Now(),
        },
        rng: rand.New(rand.NewSource(time.Now().UnixNano())),
    }
}

func (a *WeatherStationApp) Name() string {
    return "weather_station"
}

func (a *WeatherStationApp) Configuration() agent.Configuration {
    return agent.Configuration{
        UniqueID: "weather_station_app",
        Device: agent.Device{
            Name:        "Weather Station",
            Identifiers: []string{"weather_station"},
            Model:       "Simulated Weather",
            Manufacturer: "Go Hass Anything",
            SwVersion:   "1.0.0",
        },
    }
}

func (a *WeatherStationApp) States() []agent.State {
    return []agent.State{
        {
            EntityID: "sensor.temperature",
            Name:     "Temperature",
            State:    fmt.Sprintf("%.1f", a.data.Temperature),
            Attributes: map[string]interface{}{
                "unit_of_measurement": "°C",
                "device_class":       "temperature",
                "friendly_name":      fmt.Sprintf("%s Temperature", a.location),
                "icon":               "mdi:thermometer",
            },
        },
        {
            EntityID: "sensor.humidity",
            Name:     "Humidity",
            State:    fmt.Sprintf("%.1f", a.data.Humidity),
            Attributes: map[string]interface{}{
                "unit_of_measurement": "%",
                "device_class":       "humidity",
                "friendly_name":      fmt.Sprintf("%s Humidity", a.location),
                "icon":               "mdi:water-percent",
            },
        },
        {
            EntityID: "sensor.pressure",
            Name:     "Pressure",
            State:    fmt.Sprintf("%.1f", a.data.Pressure),
            Attributes: map[string]interface{}{
                "unit_of_measurement": "hPa",
                "device_class":       "pressure",
                "friendly_name":      fmt.Sprintf("%s Pressure", a.location),
                "icon":               "mdi:gauge",
            },
        },
        {
            EntityID: "sensor.wind_speed",
            Name:     "Wind Speed",
            State:    fmt.Sprintf("%.1f", a.data.WindSpeed),
            Attributes: map[string]interface{}{
                "unit_of_measurement": "km/h",
                "friendly_name":      fmt.Sprintf("%s Wind Speed", a.location),
                "icon":               "mdi:weather-windy",
            },
        },
        {
            EntityID: "sensor.wind_direction",
            Name:     "Wind Direction",
            State:    a.data.WindDirection,
            Attributes: map[string]interface{}{
                "friendly_name": fmt.Sprintf("%s Wind Direction", a.location),
                "icon":          "mdi:weather-windy-variant",
            },
        },
        {
            EntityID: "sensor.weather_condition",
            Name:     "Weather Condition",
            State:    a.data.Condition,
            Attributes: map[string]interface{}{
                "friendly_name": fmt.Sprintf("%s Weather", a.location),
                "icon":          "mdi:weather-cloudy",
            },
        },
        {
            EntityID: "sensor.last_update",
            Name:     "Last Update",
            State:    a.data.LastUpdate.Format(time.RFC3339),
            Attributes: map[string]interface{}{
                "device_class":  "timestamp",
                "friendly_name": fmt.Sprintf("%s Last Update", a.location),
                "icon":          "mdi:clock",
            },
        },
    }
}

func (a *WeatherStationApp) Subscriptions() []agent.Subscription {
    return nil
}

func (a *WeatherStationApp) Update(event agent.Event) error {
    return nil
}

func (a *WeatherStationApp) PollingInterval() time.Duration {
    return 5 * time.Minute
}

func (a *WeatherStationApp) updateWeatherData() {
    // Simulate weather changes (in real app, call weather API)
    a.data.Temperature += (a.rng.Float64()-0.5) * 2.0 // ±1°C change
    a.data.Humidity = max(20, min(100, a.data.Humidity+(a.rng.Float64()-0.5)*10))
    a.data.Pressure += (a.rng.Float64()-0.5) * 2.0
    a.data.WindSpeed = max(0, a.data.WindSpeed+(a.rng.Float64()-0.5)*3)

    directions := []string{"N", "NE", "E", "SE", "S", "SW", "W", "NW"}
    if a.rng.Float64() < 0.1 { // 10% chance to change direction
        a.data.WindDirection = directions[a.rng.Intn(len(directions))]
    }

    conditions := []string{"sunny", "partly_cloudy", "cloudy", "rainy", "stormy"}
    if a.rng.Float64() < 0.05 { // 5% chance to change condition
        a.data.Condition = conditions[a.rng.Intn(len(conditions))]
    }

    a.data.LastUpdate = time.Now()
}

func max(a, b float64) float64 { if a > b { return a }; return b }
func min(a, b float64) float64 { if a < b { return a }; return b }

func main() {
    app := NewWeatherStationApp("Home")

    // Initialize weather data
    app.updateWeatherData()

    agent.Run(app)
}
```

## MQTT Bridge App

An app that bridges MQTT topics between different systems.

```go
package main

import (
    "fmt"
    "mqtt"
    "sync"
    "github.com/joshuar/go-hass-anything/agent"
)

type MQTTBridgeApp struct {
    inputClient  mqtt.Client
    outputClient mqtt.Client
    mappings     []TopicMapping
    mu           sync.RWMutex
    messageCount int
}

type TopicMapping struct {
    InputTopic  string
    OutputTopic string
    Transform   func(string) string // Optional transform function
}

func NewMQTTBridgeApp(inputBroker, outputBroker string) *MQTTBridgeApp {
    inputOpts := mqtt.NewClientOptions().SetBroker(inputBroker)
    outputOpts := mqtt.NewClientOptions().SetBroker(outputBroker)

    return &MQTTBridgeApp{
        inputClient:  mqtt.NewClient(inputOpts),
        outputClient: mqtt.NewClient(outputOpts),
        mappings: []TopicMapping{
            {
                InputTopic:  "sensors/temperature",
                OutputTopic: "home/temperature",
                Transform:   nil, // Pass through
            },
            {
                InputTopic:  "sensors/humidity",
                OutputTopic: "home/humidity",
                Transform:   nil,
            },
            {
                InputTopic:  "controls/light/set",
                OutputTopic: "home/living_room/light/set",
                Transform:   nil,
            },
        },
    }
}

func (a *MQTTBridgeApp) Name() string {
    return "mqtt_bridge"
}

func (a *MQTTBridgeApp) Configuration() agent.Configuration {
    return agent.Configuration{
        UniqueID: "mqtt_bridge_app",
        Device: agent.Device{
            Name:        "MQTT Bridge",
            Identifiers: []string{"mqtt_bridge"},
            Model:       "Topic Bridge",
            Manufacturer: "Go Hass Anything",
        },
    }
}

func (a *MQTTBridgeApp) States() []agent.State {
    a.mu.RLock()
    count := a.messageCount
    a.mu.RUnlock()

    return []agent.State{
        {
            EntityID: "sensor.bridge_status",
            Name:     "Bridge Status",
            State:    "online",
            Attributes: map[string]interface{}{
                "device_class":  "connectivity",
                "friendly_name": "MQTT Bridge Status",
                "icon":          "mdi:lan-connect",
            },
        },
        {
            EntityID: "sensor.messages_bridged",
            Name:     "Messages Bridged",
            State:    fmt.Sprintf("%d", count),
            Attributes: map[string]interface{}{
                "unit_of_measurement": "count",
                "friendly_name":      "Total Messages Bridged",
                "icon":               "mdi:message-text-outline",
            },
        },
        {
            EntityID: "sensor.active_mappings",
            Name:     "Active Mappings",
            State:    fmt.Sprintf("%d", len(a.mappings)),
            Attributes: map[string]interface{}{
                "unit_of_measurement": "count",
                "friendly_name":      "Active Topic Mappings",
                "icon":               "diagram",
            },
        },
    }
}

func (a *MQTTBridgeApp) Subscriptions() []agent.Subscription {
    return nil // This app manages its own MQTT subscriptions
}

func (a *MQTTBridgeApp) Update(event agent.Event) error {
    return nil
}

func (a *MQTTBridgeApp) PollingInterval() time.Duration {
    return 10 * time.Second
}

func (a *MQTTBridgeApp) connectToBrokers() error {
    // Connect to input broker
    if token := a.inputClient.Connect(); token.Wait() && token.Error() != nil {
        return fmt.Errorf("failed to connect to input broker: %w", token.Error())
    }

    // Connect to output broker
    if token := a.outputClient.Connect(); token.Wait() && token.Error() != nil {
        return fmt.Errorf("failed to connect to output broker: %w", token.Error())
    }

    // Subscribe to input topics
    for _, mapping := range a.mappings {
        token := a.inputClient.Subscribe(mapping.InputTopic, 0, a.createMessageHandler(mapping))
        if token.Wait() && token.Error() != nil {
            return fmt.Errorf("failed to subscribe to %s: %w", mapping.InputTopic, token.Error())
        }
    }

    return nil
}

func (a *MQTTBridgeApp) createMessageHandler(mapping TopicMapping) mqtt.MessageHandler {
    return func(client mqtt.Client, msg mqtt.Message) {
        payload := string(msg.Payload())

        // Apply transformation if provided
        if mapping.Transform != nil {
            payload = mapping.Transform(payload)
        }

        // Publish to output topic
        token := a.outputClient.Publish(mapping.OutputTopic, 0, false, payload)
        if token.Wait() && token.Error() != nil {
            fmt.Printf("Failed to bridge message from %s to %s: %v\n",
                mapping.InputTopic, mapping.OutputTopic, token.Error())
            return
        }

        // Update message count
        a.mu.Lock()
        a.messageCount++
        a.mu.Unlock()

        fmt.Printf("Bridged: %s -> %s (%s)\n",
            mapping.InputTopic, mapping.OutputTopic, payload)
    }
}

func main() {
    inputBroker := "tcp://localhost:1883"
    outputBroker := "tcp://remote-broker:1883"

    app := NewMQTTBridgeApp(inputBroker, outputBroker)

    // Connect to both brokers
    if err := app.connectToBrokers(); err != nil {
        panic(fmt.Sprintf("Failed to setup MQTT bridge: %v", err))
    }

    // Ensure clean disconnect
    defer func() {
        a.inputClient.Disconnect(250)
        a.outputClient.Disconnect(250)
    }()

    agent.Run(app)
}
```

## Running the Examples

Each example can be compiled and run:

```bash
# Navigate to your go-hass-anything directory
cd /path/to/go-hass-anything

# Create apps directory if it doesn't exist
mkdir -p apps

# Copy an example to the apps directory
cp examples/system_monitor.go apps/system_monitor/main.go

# Build and run
mage build
./go-hass-anything run
```

## Best Practices in Examples

1. **Error Handling**: Always handle errors gracefully
2. **Thread Safety**: Use mutexes for shared state
3. **Resource Management**: Properly close connections and channels
4. **Configuration**: Make apps configurable through constructor parameters
5. **Logging**: Add logging for debugging and monitoring
6. **Testing**: Consider how you would test each component
7. **Documentation**: Include clear comments about entity purposes and attributes

These examples demonstrate various patterns and use cases for go-hass-anything applications. You can use them as starting points for your own custom integrations.