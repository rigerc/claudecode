package main

import (
	"context"
	"fmt"
	"time"

	"github.com/wailsapp/wails/v3/pkg/application"
)

type App struct {
	ctx *application.Context
}

func NewApp() *App {
	return &App{}
}

func (a *App) OnStartup(ctx *application.Context) {
	a.ctx = ctx

	// Log application start
	ctx.Logger.Info("Application started")

	// Emit a custom event
	ctx.Events.Emit("app:ready", map[string]interface{}{
		"timestamp": time.Now(),
		"version":   "1.0.0",
	})

	// Setup event listeners
	a.setupEvents()
}

func (a *App) Greet(name string) string {
	return fmt.Sprintf("Hello, %s! Welcome to Wails 3.", name)
}

func (a *App) GetCurrentTime() string {
	return time.Now().Format("2006-01-02 15:04:05")
}

func (a *App) ProcessData(data []string) ([]string, error) {
	if len(data) == 0 {
		return nil, fmt.Errorf("no data provided")
	}

	result := make([]string, len(data))
	for i, item := range data {
		result[i] = fmt.Sprintf("Processed: %s", item)
	}

	return result, nil
}

func (a *App) GetSystemInfo() map[string]interface{} {
	return map[string]interface{}{
		"platform": a.ctx.Environment.Platform,
		"arch":     a.ctx.Environment.Architecture,
		"build":    a.ctx.Environment.BuildType,
	}
}

func (a *App) setupEvents() {
	// Listen for frontend events
	a.ctx.Events.On("frontend:action", func(event *application.WailsEvent) {
		a.ctx.Logger.Info("Received action from frontend:", event.Data)

		// Process the action and emit response
		a.ctx.Events.Emit("backend:response", map[string]interface{}{
			"status":  "success",
			"message": "Action completed",
		})
	})
}