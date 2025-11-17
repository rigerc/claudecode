# Go Hass Anything Troubleshooting Guide

## Common Issues and Solutions

### Connection Issues

#### MQTT Connection Failed
**Symptoms:**
- App exits immediately on startup
- Error messages about connection refused or timeout
- No entities appear in Home Assistant

**Common Causes:**
1. MQTT broker not running
2. Incorrect broker address or port
3. Firewall blocking connection
4. Authentication credentials wrong
5. TLS configuration issues

**Solutions:**

1. **Check MQTT Broker Status**
```bash
# Test connection with mosquitto clients
mosquitto_pub -h localhost -t test -m "hello"
mosquitto_sub -h localhost -t test

# Check if broker is running
sudo systemctl status mosquitto
# or
docker ps | grep mosquitto
```

2. **Verify Configuration**
```bash
# Test with go-hass-anything configure
go-hass-anything configure

# Manually test MQTT connection
telnet localhost 1883
```

3. **Check Network Connectivity**
```bash
# Test network path
ping mqtt-broker-hostname
traceroute mqtt-broker-hostname

# Check firewall rules
sudo ufw status
# or
sudo iptables -L
```

4. **Validate Authentication**
```bash
# Test credentials with mosquitto_pub
mosquitto_pub -h broker -u username -P password -t test -m "test"
```

#### TLS/SSL Connection Issues
**Symptoms:**
- Certificate validation errors
- Handshake failures
- Connection timeouts with TLS enabled

**Solutions:**

1. **Check Certificate Paths**
```bash
# Verify certificate files exist
ls -la /path/to/certs/
file /path/to/ca.crt
```

2. **Test TLS Connection**
```bash
# Test with openssl
openssl s_client -connect broker:8883 -CAfile ca.crt

# Test with mosquitto
mosquitto_pub -h broker -p 8883 --cafile ca.crt -t test -m "test"
```

3. **Verify Certificate Chain**
```bash
# Check certificate validity
openssl x509 -in ca.crt -text -noout
openssl verify -CAfile ca.crt client.crt
```

### Home Assistant Integration Issues

#### Entities Not Appearing
**Symptoms:**
- MQTT broker connection works
- No devices or entities in Home Assistant
- Discovery messages not being processed

**Common Causes:**
1. MQTT discovery disabled in Home Assistant
2. Incorrect discovery prefix
3. Entity ID conflicts
4. Invalid discovery message format

**Solutions:**

1. **Enable MQTT Discovery**
- Go to Home Assistant → Settings → Devices & Services → MQTT
- Ensure "Enable discovery" is turned on
- Check discovery prefix matches your configuration

2. **Monitor Discovery Topics**
```bash
# Watch for discovery messages
mosquitto_sub -h localhost -t "homeassistant/+/+/config" -v

# Check state topics
mosquitto_sub -h localhost -t "go-hass/+/+/state" -v
```

3. **Verify Discovery Message Format**
```bash
# Subscribe and inspect discovery messages
mosquitto_sub -h localhost -t "homeassistant/+/+/config" | jq .
```

4. **Check Home Assistant Logs**
```bash
# Check for MQTT processing errors
docker logs home-assistant | grep -i mqtt
```

#### Entity State Not Updating
**Symptoms:**
- Entities appear but show "unavailable"
- State values are stale or incorrect
- Manual state updates work but automatic updates don't

**Solutions:**

1. **Check State Topic Publishing**
```bash
# Monitor state updates
mosquitto_sub -h localhost -t "go-hass/#" -v
```

2. **Verify App is Running**
```bash
# Check process status
ps aux | grep go-hass-anything

# Enable debug logging
export GO_HASS_LOG_LEVEL=debug
go-hass-anything run
```

3. **Check Polling Intervals**
```go
// Ensure PollingInterval() returns reasonable duration
func (a *MyApp) PollingInterval() time.Duration {
    return 30 * time.Second // Not too fast, not too slow
}
```

### Application Runtime Issues

#### App Panics or Crashes
**Symptoms:**
- App exits unexpectedly
- Panic stack traces in logs
- Entities become unavailable after crash

**Solutions:**

1. **Enable Debug Logging**
```bash
export GO_HASS_LOG_LEVEL=debug
go-hass-anything run 2>&1 | tee app.log
```

2. **Add Panic Recovery**
```go
func main() {
    defer func() {
        if r := recover(); r != nil {
            log.Printf("App panicked: %v", r)
            log.Printf("Stack: %s", debug.Stack())
        }
    }()

    app := &MyApp{}
    agent.Run(app)
}
```

3. **Validate Input Data**
```go
func (a *MyApp) Update(event agent.Event) error {
    // Validate payload
    if event.Payload == "" {
        return fmt.Errorf("empty payload received")
    }

    // Additional validation as needed
    return nil
}
```

#### High Memory or CPU Usage
**Symptoms:**
- System becomes sluggish
- High resource consumption
- App becomes unresponsive

**Common Causes:**
1. Too frequent polling
2. Memory leaks in app code
3. Blocking operations in update loops
4. Large data structures growing unbounded

**Solutions:**

1. **Optimize Polling Intervals**
```go
// Don't poll too frequently
func (a *MyApp) PollingInterval() time.Duration {
    return 60 * time.Second // Increase interval
}
```

2. **Monitor Resource Usage**
```bash
# Monitor memory usage
ps aux | grep go-hass-anything
top -p $(pgrep go-hass-anything)

# Check for memory leaks
valgrind --tool=memcheck ./go-hass-anything run
```

3. **Use Resource Limits**
```bash
# Run with memory limits
ulimit -m 1048576  # 1GB limit
./go-hass-anything run
```

4. **Profile the Application**
```go
import _ "net/http/pprof"

func main() {
    go func() {
        log.Println(http.ListenAndServe("localhost:6060", nil))
    }()

    app := &MyApp{}
    agent.Run(app)
}
```

### MQTT-Specific Issues

#### Message Not Delivered
**Symptoms:**
- Commands from Home Assistant don't work
- State updates not reaching Home Assistant
- One-way communication only

**Solutions:**

1. **Check QoS Settings**
```go
// Ensure QoS levels match between publisher and subscriber
token := client.Publish(topic, 1, false, payload) // Use QoS 1 for delivery
```

2. **Verify Topic Patterns**
```bash
# List all topics
mosquitto_sub -h localhost -t "#" -v | grep go-hass

# Check for typos in topic names
mosquitto_sub -h localhost -t "go-hass/+/+/set" -v
```

3. **Test Message Flow**
```bash
# Test publishing to state topic
mosquitto_pub -h localhost -t "go-hass/my_app/sensor_test/state" -m "25.5"

# Test subscribing to command topic
mosquitto_sub -h localhost -t "go-hass/my_app/switch_test/set" -v
```

#### Subscription Not Working
**Symptoms:**
- Home Assistant commands not received
- Switch/button controls don't work
- No subscription handlers being called

**Solutions:**

1. **Verify Subscription Handler**
```go
func (a *MyApp) Subscriptions() []agent.Subscription {
    return []agent.Subscription{
        {
            Topic: "go-hass/my_app/switch_test/set",
            Handler: func(topic string, payload string) error {
                log.Printf("Received command: %s = %s", topic, payload)
                return a.handleCommand(payload)
            },
        },
    }
}
```

2. **Check Topic Matching**
```bash
# Verify Home Assistant is publishing to expected topic
mosquitto_sub -h localhost -t "go-hass/#" -v
# Then toggle switch in Home Assistant
```

3. **Test Manually**
```bash
# Manually send command to test handler
mosquitto_pub -h localhost -t "go-hass/my_app/switch_test/set" -m "ON"
```

### Configuration Issues

#### Invalid TOML Configuration
**Symptoms:**
- Configuration errors on startup
- Default values being used instead of config
- Parsing errors in logs

**Solutions:**

1. **Validate TOML Syntax**
```bash
# Use toml linter
pip install toml-cli
toml-cli check config.toml

# Or use online TOML validator
```

2. **Check Required Fields**
```toml
[mqtt]
broker = "localhost:1883"  # Required
username = ""              # Optional
password = ""              # Optional

[agent]
apps_dir = "./apps"        # Required
log_level = "info"         # Required
```

3. **Use Environment Variables**
```bash
# Override config with environment variables
export MQTT_BROKER="remote-broker:1883"
export MQTT_USERNAME="user"
export MQTT_PASSWORD="pass"

go-hass-anything run
```

#### Entity Configuration Problems
**Symptoms:**
- Entities appear but with wrong attributes
- Missing icons or device classes
- Incorrect units or display options

**Solutions:**

1. **Validate Entity Attributes**
```go
{
    EntityID: "sensor.temperature",
    Name:     "Temperature",
    State:    "23.5",
    Attributes: map[string]interface{}{
        "unit_of_measurement": "°C",        // Correct unit
        "device_class":       "temperature", // Valid device class
        "state_class":        "measurement", // For statistics
        "friendly_name":      "Room Temperature", // User-friendly
        "icon":               "mdi:thermometer", // Material Design Icon
    },
}
```

2. **Check Device Class Validity**
- See [Home Assistant Device Classes](https://www.home-assistant.io/docs/configuration/device_class/)
- Ensure device class matches entity type
- Some device classes only work with specific entity types

3. **Verify Entity ID Format**
```go
// Valid formats:
"sensor.temperature"           // Good
"sensor.room_temperature"     // Good
"sensor.room_temperature_1"   // Good
"sensor.Room-Temperature"     // Bad (uppercase)
"sensor room temperature"     // Bad (spaces)
```

### Performance Issues

#### Slow Startup
**Symptoms:**
- App takes long time to start
- Entities appear slowly in Home Assistant
- Initial connection delays

**Solutions:**

1. **Optimize Initialization**
```go
func NewApp() *MyApp {
    app := &MyApp{
        // Initialize with reasonable defaults
        data: make(map[string]string),
    }

    // Load configuration asynchronously if possible
    go app.loadConfig()

    return app
}
```

2. **Reduce Connection Timeouts**
```toml
[mqtt.connection]
connect_timeout = "10s"   # Reduce from default
keep_alive = "30s"        # More frequent pings
```

3. **Prefer Lazy Loading**
```go
func (a *MyApp) States() []agent.State {
    // Don't load all data upfront
    return []agent.State{
        { /* first state */ },
        // Load others as needed
    }
}
```

#### High Network Traffic
**Symptoms:**
- Excessive MQTT messages
- Network congestion
- Rate limiting from broker

**Solutions:**

1. **Batch State Updates**
```go
func (a *MyApp) States() []agent.State {
    // Return all states at once instead of frequent individual updates
    states := make([]agent.State, 0)

    for _, sensor := range a.sensors {
        states = append(states, sensor.GetState())
    }

    return states
}
```

2. **Use Appropriate QoS Levels**
```go
// Use QoS 0 for frequent sensor data
token := client.Publish(topic, 0, false, payload)

// Use QoS 1 for critical commands
token := client.Publish(commandTopic, 1, false, command)
```

3. **Implement Rate Limiting**
```go
type RateLimitedApp struct {
    lastUpdate time.Time
    minInterval time.Duration
}

func (a *RateLimitedApp) shouldUpdate() bool {
    now := time.Now()
    if now.Sub(a.lastUpdate) < a.minInterval {
        return false
    }
    a.lastUpdate = now
    return true
}
```

## Debugging Tools and Techniques

### Enable Debug Logging

```bash
# Set log level environment variable
export GO_HASS_LOG_LEVEL=debug

# Run with debug output
go-hass-anything run 2>&1 | tee debug.log

# Filter specific log levels
go-hass-anything run 2>&1 | grep -E "(DEBUG|ERROR|WARN)"
```

### Monitor MQTT Traffic

```bash
# Monitor all go-hass traffic
mosquitto_sub -h localhost -t "go-hass/#" -v

# Monitor discovery messages
mosquitto_sub -h localhost -t "homeassistant/+/+/config" -v

# Monitor specific device
mosquitto_sub -h localhost -t "go-hass/my_device/#" -v

# Monitor commands from Home Assistant
mosquitto_sub -h localhost -t "go-hass/+/+/set" -v
```

### Test with MQTT Client Tools

```bash
# Test publishing states
mosquitto_pub -h localhost -t "go-hass/test/sensor_temp/state" -m "25.5"

# Test command handling
mosquitto_sub -h localhost -t "go-hass/test/switch_light/set" -v &
mosquitto_pub -h localhost -t "go-hass/test/switch_light/set" -m "ON"

# Test discovery
mosquitto_pub -h localhost -t "homeassistant/sensor/test/temp/config" -m '{
    "name": "Test Temperature",
    "unique_id": "test_temp",
    "state_topic": "go-hass/test/sensor_temp/state",
    "unit_of_measurement": "°C"
}'
```

### Use Go Profiling

```go
import (
    _ "net/http/pprof"
    "net/http"
    "log"
)

func main() {
    // Start pprof server
    go func() {
        log.Println(http.ListenAndServe("localhost:6060", nil))
    }()

    app := &MyApp{}
    agent.Run(app)
}
```

Then analyze with:
```bash
# Get CPU profile
go tool pprof http://localhost:6060/debug/pprof/profile

# Get heap profile
go tool pprof http://localhost:6060/debug/pprof/heap

# View goroutines
go tool pprof http://localhost:6060/debug/pprof/goroutine
```

### Validate Home Assistant Integration

1. **Check Developer Tools**
- Go to Home Assistant → Developer Tools → States
- Search for your entities
- Check attributes and state values

2. **Check MQTT Integration**
- Go to Settings → Devices & Services → MQTT
- Review configuration
- Check device list for your devices

3. **Check System Logs**
- Go to Settings → System → Logs
- Look for MQTT-related errors
- Check for device discovery issues

## Getting Help

### Community Resources
- [Go Hass Anything GitHub Issues](https://github.com/joshuar/go-hass-anything/issues)
- [Home Assistant Community Forums](https://community.home-assistant.io/)
- [MQTT Documentation](https://mqtt.org/)

### Creating Bug Reports

When reporting issues, include:

1. **Environment Information**
```bash
go version
uname -a
go-hass-anything version  # if available
```

2. **Configuration**
- MQTT broker type and version
- Home Assistant version
- Network setup (Docker, native, etc.)

3. **Logs**
- Full startup logs
- Debug output with `GO_HASS_LOG_LEVEL=debug`
- MQTT broker logs if relevant

4. **Minimal Reproducible Example**
- Simplest app that reproduces the issue
- Configuration files
- Steps to reproduce

### Performance Monitoring

Monitor your app's performance with these metrics:

```bash
# Monitor CPU usage
top -p $(pgrep go-hass-anything)

# Monitor memory usage
watch -n 1 'ps aux | grep go-hass-anything'

# Monitor network connections
netstat -an | grep 1883

# Monitor MQTT message rate
mosquitto_sub -h localhost -t "#" -v | wc -l
```

This troubleshooting guide should help resolve most common issues with Go Hass Anything applications. For specific problems not covered here, please check the GitHub issues or create a new one with detailed information about your setup.