# Wails Framework Guide

## Overview

Wails is a lightweight, fast framework for building cross-platform desktop applications using Go for the backend and web technologies for the frontend. It serves as a powerful alternative to Electron, offering native performance and a smaller footprint while leveraging the Go ecosystem and modern web frameworks.

## Key Features

- **Cross-platform**: Build applications for Windows, macOS, and Linux from a single codebase
- **Native Performance**: Compile to native binaries with minimal overhead
- **Go Backend**: Leverage Go's performance, concurrency, and extensive standard library
- **Web Frontend**: Use any web framework (React, Vue, Svelte, Angular, etc.)
- **Small Bundle Sizes**: Significantly smaller than Electron applications
- **Native Menus**: Support for native context menus and menu bars
- **Dialogs & Notifications**: Access to native system dialogs and notifications
- **File System Access**: Direct access to the local file system
- **Hot Reload**: Development mode with automatic reloading

## Architecture

Wails applications consist of three main components:

1. **Go Backend**: Handles business logic, system interactions, and data processing
2. **JavaScript Bridge**: Provides communication between frontend and backend
3. **Frontend**: Web-based user interface using any modern JavaScript framework

### Project Structure

```
my-wails-app/
├── main.go              # Main application entry point
├── app.go              # Application logic and struct definitions
├── wails.json          # Wails configuration file
├── embed.go            # Embedded frontend assets
├── frontend/           # Frontend application
│   ├── src/           # Source files
│   ├── public/        # Static assets
│   ├── package.json   # Frontend dependencies
│   └── ...            # Framework-specific files
├── build/             # Built application binaries
└── vendor/            # Go dependencies (if using modules)
```

## Installation and Setup

### Prerequisites

- **Go**: Version 1.18 or higher
- **Node.js**: Version 16 or higher (for frontend development)
- **System Dependencies**:
  - Windows: None required
  - macOS: Xcode Command Line Tools
  - Linux: GTK3, libwebkit2gtk, and other system libraries

### Installing Wails CLI

```bash
# Install the Wails CLI
go install github.com/wailsapp/wails/v2/cmd/wails@latest

# Verify installation
wails doctor
```

### Creating a New Project

```bash
# Create a new project with React TypeScript
wails init -n my-wails-app -t react-ts

# Create with Vue TypeScript
wails init -n my-wails-app -t vue-ts

# Create with Svelte TypeScript
wails init -n my-wails-app -t svelte-ts

# Navigate to project directory
cd my-wails-app
```

### Development Workflow

```bash
# Run in development mode with hot reload
wails dev

# Build for production
wails build

# Build with optimization flags
wails build -clean -upx -ldflags "-w -s"

# Build for specific platform
wails build -platform windows/amd64
wails build -platform darwin/amd64
wails build -platform linux/amd64
```

## Application Structure

### Main Application (main.go)

The main entry point configures and runs the Wails application:

```go
package main

import (
	"context"
	"embed"
	"fmt"
	"log"

	"github.com/wailsapp/wails/v2"
	"github.com/wailsapp/wails/v2/pkg/options"
	"github.com/wailsapp/wails/v2/pkg/options/assetserver"
)

//go:embed all:frontend/dist
var assets embed.FS

func main() {
	app := &App{}

	err := wails.Run(&options.App{
		Title:  "My Wails App",
		Width:  1024,
		Height: 768,
		AssetServer: &assetserver.Options{
			Assets: assets,
		},
		OnStartup:  app.startup,
		OnShutdown: app.shutdown,
		Bind: []interface{}{
			app,
		},
	})

	if err != nil {
		log.Fatal(err)
	}
}
```

### Application Logic (app.go)

Define your application's business logic and expose methods to the frontend:

```go
package main

import (
	"context"
	"fmt"
)

type App struct {
	ctx context.Context
}

func (a *App) startup(ctx context.Context) {
	a.ctx = ctx
}

func (a *App) shutdown(ctx context.Context) {
	// Cleanup code here
}

func (a *App) Greet(name string) string {
	return fmt.Sprintf("Hello %s!", name)
}

func (a *App) ProcessData(data []string) ([]string, error) {
	// Business logic here
	result := make([]string, len(data))
	for i, item := range range data {
		result[i] = strings.ToUpper(item)
	}
	return result, nil
}
```

## Frontend Integration

### Using Go Methods from JavaScript

Wails automatically generates JavaScript bindings for your Go methods:

```javascript
// Import generated bindings
import { Greet, ProcessData } from '../wailsjs/go/main/App';

// Use Go methods
async function handleGreeting() {
  try {
    const result = await Greet('World');
    console.log(result); // "Hello World!"
  } catch (err) {
    console.error(err);
  }
}

async function processData() {
  try {
    const data = ['item1', 'item2', 'item3'];
    const result = await ProcessData(data);
    console.log(result); // ['ITEM1', 'ITEM2', 'ITEM3']
  } catch (err) {
    console.error(err);
  }
}
```

### React Example

```jsx
import React, { useState, useEffect } from 'react';
import { Greet } from '../wailsjs/go/main/App';

function App() {
  const [greeting, setGreeting] = useState('');
  const [name, setName] = useState('');

  const handleGreet = async () => {
    try {
      const result = await Greet(name);
      setGreeting(result);
    } catch (error) {
      console.error(error);
    }
  };

  return (
    <div>
      <h1>Wails React App</h1>
      <input
        type="text"
        value={name}
        onChange={(e) => setName(e.target.value)}
        placeholder="Enter your name"
      />
      <button onClick={handleGreet}>Greet</button>
      {greeting && <p>{greeting}</p>}
    </div>
  );
}

export default App;
```

## Configuration

### wails.json

The Wails configuration file controls various aspects of your application:

```json
{
  "$schema": "https://wails.io/schemas/config.v2.json",
  "name": "my-wails-app",
  "outputfilename": "my-wails-app",
  "frontend": {
    "dir": "./frontend",
    "install": "npm install",
    "build": "npm run build",
    "dev": "npm run dev",
    "package": {
      "manager": "npm"
    }
  },
  "author": {
    "name": "Your Name",
    "email": "your.email@example.com"
  },
  "info": {
    "companyName": "Your Company",
    "productName": "My Wails App",
    "productVersion": "1.0.0",
    "copyright": "Copyright © 2024 Your Name",
    "comments": "Built using Wails (https://wails.io)"
  },
  "nsisType": "multiple",
  "obfuscated": false,
  "garbleargs": "",
  "upx": false,
  "upxflags": "",
  "compressed": true,
  "runNonNativeBuildHooks": false,
  "useBuildDirectory": false,
  "generateBuildScript": false
}
```

## System Integration

### File System Operations

```go
import (
	"io/ioutil"
	"os"
	"path/filepath"
)

func (a *App) ReadFile(path string) (string, error) {
	data, err := ioutil.ReadFile(path)
	return string(data), err
}

func (a *App) WriteFile(path, content string) error {
	return ioutil.WriteFile(path, []byte(content), 0644)
}

func (a *App) GetHomeDir() (string, error) {
	home, err := os.UserHomeDir()
	return home, err
}

func (a *App) GetDocumentsDir() (string, error) {
	home, err := os.UserHomeDir()
	if err != nil {
		return "", err
	}

	switch a.ctx.(*runtime.Runtime).Environment.Platform {
	case runtime.Windows:
		return filepath.Join(home, "Documents"), nil
	case runtime.Darwin:
		return filepath.Join(home, "Documents"), nil
	case runtime.Linux:
		return filepath.Join(home, "Documents"), nil
	default:
		return home, nil
	}
}
```

### System Notifications

```go
import "github.com/wailsapp/wails/v2/pkg/runtime"

func (a *App) ShowNotification(title, message string) {
	runtime.EventsEmit(a.ctx, "notification", map[string]string{
		"title":   title,
		"message": message,
	})
}

func (a *App) ShowMessageDialog(title, message string) {
	runtime.MessageDialog(a.ctx, runtime.MessageDialogOptions{
		Type:          runtime.InfoDialog,
		Title:         title,
		Message:       message,
		Buttons:       []string{"OK"},
		DefaultButton: "OK",
	})
}
```

### Context Menus

```go
func (a *App) ShowContextMenu(x, y int) {
	runtime.MenuShowContextMenu(a.ctx, runtime.MenuShowContextMenuOptions{
		X: x,
		Y: y,
		Commands: []runtime.MenuCommand{
			{
				Label:   "Cut",
				Role:    runtime.CutRole,
				Enabled: true,
			},
			{
				Label:   "Copy",
				Role:    runtime.CopyRole,
				Enabled: true,
			},
			{
				Label:   "Paste",
				Role:    runtime.PasteRole,
				Enabled: true,
			},
			{
				Type:    runtime.Separator,
			},
			{
				Label:   "Custom Action",
				Enabled: true,
				Callback: func(*runtime.CallbackData) {
					fmt.Println("Custom action triggered")
				},
			},
		},
	})
}
```

## Advanced Features

### Custom Window Options

```go
err := wails.Run(&options.App{
	Title:  "Advanced Wails App",
	Width:  1200,
	Height: 800,
	MinWidth: 800,
	MinHeight: 600,
	MaxWidth: 1920,
	MaxHeight: 1080,
	WindowStartState: options.Maximised,
	AssetServer: &assetserver.Options{
		Assets: assets,
	},
	Windows: windows.Options{
		WebviewIsTransparent: false,
		WindowIsResizable:    true,
		WindowIsDecorated:    true,
		WindowAlwaysOnTop:    false,
		Theme:                options.System,
	},
	MacOS: macos.Options{
		TitleBar: macos.TitleBarOptions{
			TitlebarAppearsTransparent: true,
			HideTitle:                  false,
			HideTitleBar:               false,
			FullSizeContent:            false,
			UseToolbar:                 false,
			HideToolbarSeparator:       true,
		},
	},
	Linux: linux.Options{
		Icon: []byte{}, // Window icon bytes
	},
})
```

### Runtime Events

```go
import "github.com/wailsapp/wails/v2/pkg/runtime"

func (a *App) startup(ctx context.Context) {
	a.ctx = ctx

	// Listen for window events
	runtime.EventsOn(ctx, "windowFocusLost", func(data ...interface{}) {
		fmt.Println("Window lost focus")
	})

	runtime.EventsOn(ctx, "windowFocusGained", func(data ...interface{}) {
		fmt.Println("Window gained focus")
	})
}

func (a *App) EmitCustomEvent(event string, data interface{}) {
	runtime.EventsEmit(a.ctx, event, data)
}
```

### File Dialogs

```go
func (a *App) OpenFileDialog() (string, error) {
	dialogOptions := runtime.OpenDialogOptions{
		DefaultDirectory:           "",
		DefaultFilename:            "",
		Title:                      "Select a file",
		Filters: []runtime.FileFilter{
			{
				DisplayName: "Text Files (*.txt)",
				Pattern:     "*.txt",
			},
			{
				DisplayName: "All Files (*.*)",
				Pattern:     "*.*",
			},
		},
	}

	selectedFile, err := runtime.OpenFileDialog(a.ctx, dialogOptions)
	return selectedFile, err
}

func (a *App) SaveFileDialog(defaultName string) (string, error) {
	dialogOptions := runtime.SaveDialogOptions{
		DefaultFilename: defaultName,
		Title:           "Save file",
		Filters: []runtime.FileFilter{
			{
				DisplayName: "Text Files (*.txt)",
				Pattern:     "*.txt",
			},
		},
	}

	selectedFile, err := runtime.SaveFileDialog(a.ctx, dialogOptions)
	return selectedFile, err
}
```

## Deployment

### Building for Production

```bash
# Standard build
wails build

# Build with compression
wails build -upx

# Build with linker flags for smaller binaries
wails build -ldflags "-w -s"

# Clean build (removes previous build artifacts)
wails build -clean

# Build without UPX compression
wails build -upx=false
```

### Platform-Specific Builds

```bash
# Windows
wails build -platform windows/amd64
wails build -platform windows/arm64

# macOS
wails build -platform darwin/amd64
wails build -platform darwin/arm64

# Linux
wails build -platform linux/amd64
wails build -platform linux/arm64
```

### Windows Installer Configuration

```json
{
  "Info": {
    "companyName": "My Company",
    "productName": "My Wails App",
    "productVersion": "1.0.0",
    "copyright": "Copyright © 2024 My Company",
    "comments": "Built using Wails (https://wails.io)"
  },
  "nsisType": "multiple"
}
```

## Best Practices

### Performance Optimization

1. **Minimize Go-JavaScript calls**: Reduce the frequency of backend calls
2. **Use streaming for large data**: Stream large files or datasets
3. **Optimize asset loading**: Use code splitting and lazy loading
4. **Leverage Go concurrency**: Use goroutines for background tasks

### Security Considerations

1. **Validate input**: Sanitize all user inputs in Go
2. **Use HTTPS**: For network requests
3. **Secure file access**: Validate file paths and permissions
4. **Obfuscate sensitive code**: Use garble for production builds

### Error Handling

```go
func (a *App) SafeOperation(data string) (string, error) {
	if data == "" {
		return "", errors.New("data cannot be empty")
	}

	// Business logic here
	result := strings.ToUpper(data)
	return result, nil
}
```

### Logging

```go
import (
	"log"
	"os"
)

func (a *App) InitializeLogging() error {
	file, err := os.OpenFile("app.log", os.O_CREATE|os.O_WRONLY|os.O_APPEND, 0666)
	if err != nil {
		return err
	}

	log.SetOutput(file)
	log.Println("Application started")
	return nil
}
```

## Troubleshooting

### Common Issues

1. **Build fails**: Check system dependencies with `wails doctor`
2. **Frontend not loading**: Verify asset embedding and path configuration
3. **Go methods not accessible**: Check struct binding and method capitalization
4. **Hot reload not working**: Ensure development server is running

### Debugging

```go
import "github.com/wailsapp/wails/v2/pkg/runtime"

func (a *App) DebugMode() bool {
	return runtime.Environment(a.ctx).BuildType == "debug"
}

func (a *App) LogToFrontend(message string) {
	runtime.EventsEmit(a.ctx, "log", message)
}
```

## Resources

- **Official Documentation**: https://wails.io/docs/
- **GitHub Repository**: https://github.com/wailsapp/wails
- **Community Discord**: https://discord.gg/VUnjxRG
- **Example Projects**: https://github.com/wailsapp/wails/tree/master/examples

## Conclusion

Wails provides an excellent framework for building cross-platform desktop applications by combining the power and performance of Go with the flexibility of modern web technologies. Its lightweight nature, native integration, and extensive tooling make it a compelling choice for developers looking to create desktop applications with web technologies.