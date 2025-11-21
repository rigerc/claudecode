package main

import (
	"embed"
	"log"

	"github.com/wailsapp/wails/v3/pkg/application"
)

//go:embed assets
var assets embed.FS

func main() {
	// Create a new application
	app := application.New(application.Options{
		Name:        "My Wails 3 App",
		Description: "A demonstration application",
		Assets: application.AssetOptions{
			Handler: application.AssetFileServerFS(assets),
		},
		Mac: application.MacOptions{
			ApplicationShouldTerminateAfterLastWindowClosed: true,
		},
	})

	// Create application instance
	appInstance := NewApp()

	// Bind methods to frontend
	app.Bind(appInstance)

	// Create main window
	main_window := app.NewWebviewWindowWithOptions(application.WebviewWindowOptions{
		Title:  "My App",
		Width:  1024,
		Height: 768,
	})

	// Register startup event
	app.OnStartup(func(ctx *application.Context) {
		appInstance.OnStartup(ctx)
	})

	err := app.Run()
	if err != nil {
		log.Fatal(err)
	}
}