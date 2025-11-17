package main

import (
    "github.com/joshuar/go-hass-anything/agent"
)

type {{.AppName}} struct {
    // Add your app's fields here
    // Example: lastUpdate time.Time
}

func New{{.AppName}}() *{{.AppName}} {
    return &{{.AppName}}{
        // Initialize your app's fields here
    }
}

func (a *{{.AppName}}) Name() string {
    return "{{.AppID}}"
}

func (a *{{.AppName}}) Configuration() agent.Configuration {
    return agent.Configuration{
        UniqueID: "{{.AppID}}_app",
        Device: agent.Device{
            Name:        "{{.AppName}} Device",
            Identifiers: []string{"{{.AppID}}"},
            Model:       "Custom Integration",
            Manufacturer: "Go Hass Anything",
        },
    }
}

func (a *{{.AppName}}) States() []agent.State {
    return []agent.State{
        // Add your entities here
        // Example:
        // {
        //     EntityID: "sensor.{{.AppID}}_temperature",
        //     Name:     "Temperature",
        //     State:    "20.0",
        //     Attributes: map[string]interface{}{
        //         "unit_of_measurement": "°C",
        //         "device_class":       "temperature",
        //     },
        // },
    }
}

func (a *{{.AppName}}) Subscriptions() []agent.Subscription {
    return []agent.Subscription{
        // Add your command subscriptions here
        // Example:
        // {
        //     Topic: "go-hass/{{.AppID}}/switch_light/set",
        //     Handler: func(topic string, payload string) error {
        //         return a.handleLightCommand(payload)
        //     },
        // },
    }
}

func (a *{{.AppName}}) Update(event agent.Event) error {
    // Handle incoming commands here
    return nil
}

// Optional: Implement PollingApp for periodic updates
// func (a *{{.AppName}}) PollingInterval() time.Duration {
//     return 30 * time.Second
// }

// Optional: Implement EventsApp for event-driven updates
// func (a *{{.AppName}}) Events() <-chan agent.Event {
//     eventChan := make(chan agent.Event)
//     go func() {
//         // Generate events as needed
//     }()
//     return eventChan
// }

func main() {
    app := New{{.AppName}}()
    agent.Run(app)
}