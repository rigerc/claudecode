# Wails 3 Complete Development Guide

## Installation and Setup

### Install Wails 3 CLI

```bash
# Clone and install from v3-alpha branch
git clone https://github.com/wailsapp/wails.git
cd wails
git checkout v3-alpha
cd v3/cmd/wails3
go install

# Verify installation
wails3 doctor
```

### System Dependencies

**Linux:**
```bash
sudo apt-get install libgtk-3-dev libwebkit2gtk-4.0-dev build-essential
```

**macOS:**
```bash
xcode-select --install
```

**Windows:** No additional dependencies required

## Project Structure

### Initialize New Project

```bash
# React TypeScript
wails3 init -n my-app -t react-ts

# Vue TypeScript
wails3 init -n my-app -t vue-ts

# Vanilla JavaScript
wails3 init -n my-app -t vanilla-js
```

### Directory Layout

```
my-app/
├── main.go              # Application entry point
├── app.go              # Business logic and method definitions
├── embed.go            # Frontend asset embedding
├── wails.json          # Configuration file
├── assets/             # Embedded frontend assets
├── frontend/           # Frontend source code
├── build/              # Build output
└── go.mod              # Go module file
```

## Core Application Structure

### main.go - Application Entry Point

```go
package main

import (
    "embed"
    "log"

    "github.com/wailsapp/wails/v3/pkg/application"
)

//go:embed assets
var assets embed.FS

func main() {
    app := application.New(application.Options{
        Name:        "My Wails 3 App",
        Description: "A desktop application",
        Assets: application.AssetOptions{
            Handler: application.AssetFileServerFS(assets),
        },
        Mac: application.MacOptions{
            ApplicationShouldTerminateAfterLastWindowClosed: true,
        },
    })

    // Create main window
    mainWindow := app.NewWebviewWindowWithOptions(application.WebviewWindowOptions{
        Title:  "My App",
        Width:  1024,
        Height: 768,
    })

    // Bind application methods
    appInstance := NewApp()
    app.Bind(appInstance)

    err := app.Run()
    if err != nil {
        log.Fatal(err)
    }
}
```

### app.go - Business Logic

```go
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
    ctx.Logger.Info("Application started")

    // Emit ready event
    ctx.Events.Emit("app:ready", map[string]interface{}{
        "timestamp": time.Now(),
        "version":   "1.0.0",
    })
}

func (a *App) Greet(name string) string {
    return fmt.Sprintf("Hello, %s! Welcome to Wails 3.", name)
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
```

## Event System

### Go Backend Events

```go
func (a *App) setupEvents() {
    // Listen for frontend events
    a.ctx.Events.On("frontend:request", func(event *application.WailsEvent) {
        a.ctx.Logger.Info("Received request from frontend:", event.Data)

        // Process and emit response
        a.ctx.Events.Emit("backend:response", map[string]interface{}{
            "status":  "success",
            "data":    "Request processed",
            "request": event.Data,
        })
    })

    // Listen for application events
    a.ctx.Application.On(events.Common.WindowFocus, func(event *application.WindowEvent) {
        a.ctx.Logger.Info("Window gained focus")
    })
}

func (a *App) NotifyUser(title, message string) {
    a.ctx.Events.Emit("user:notification", map[string]interface{}{
        "title":   title,
        "message": message,
        "time":    time.Now(),
    })
}
```

### Frontend Event Handling (TypeScript)

```typescript
import { EventsOn, EventsEmit } from '../wailsjs/runtime/runtime';

// Setup event listeners
export function setupEventListeners() {
    // Listen for notifications
    EventsOn('user:notification', (data) => {
        console.log('Notification:', data);
        showNotification(data.title, data.message);
    });

    // Listen for app ready
    EventsOn('app:ready', (data) => {
        console.log('App ready:', data);
        initializeApp(data);
    });

    // Listen for backend responses
    EventsOn('backend:response', (data) => {
        console.log('Backend response:', data);
        handleResponse(data);
    });
}

// Emit events to Go
export function sendRequest(action: string, payload: any) {
    EventsEmit('frontend:request', {
        action: action,
        payload: payload,
        timestamp: new Date().toISOString(),
    });
}
```

## System Integration

### Theme Detection

```go
func (a *App) setupThemeDetection(app *application.Application) {
    // Listen for theme changes
    app.OnApplicationEvent(events.Common.ThemeChanged, func(event *application.ApplicationEvent) {
        isDark := event.Context().IsDarkMode()

        a.ctx.Logger.Info("Theme changed:", isDark)
        a.ctx.Events.Emit("theme:changed", map[string]interface{}{
            "isDark": isDark,
        })
    })
}
```

```typescript
// Frontend theme handling
EventsOn('theme:changed', (data) => {
    const isDark = data.isDark;

    if (isDark) {
        document.body.classList.add('dark-theme');
        document.body.classList.remove('light-theme');
    } else {
        document.body.classList.add('light-theme');
        document.body.classList.remove('dark-theme');
    }

    localStorage.setItem('theme', isDark ? 'dark' : 'light');
});
```

### File Operations

```go
func (a *App) ReadFile(path string) (string, error) {
    data, err := os.ReadFile(path)
    if err != nil {
        return "", fmt.Errorf("failed to read file: %w", err)
    }
    return string(data), nil
}

func (a *App) WriteFile(path, content string) error {
    return os.WriteFile(path, []byte(content), 0644)
}

func (a *App) OpenFileDialog() (string, error) {
    selectedFile, err := a.ctx.Runtime.OpenFileDialog(a.ctx, runtime.OpenDialogOptions{
        Title: "Select a file",
        Filters: []runtime.FileFilter{
            {DisplayName: "Text Files", Pattern: "*.txt"},
            {DisplayName: "All Files", Pattern: "*.*"},
        },
    })
    return selectedFile, err
}
```

### Menu System

```go
func (a *App) setupMenus(app *application.Application) {
    menu := app.NewMenu()

    // File menu
    fileMenu := menu.AddSubmenu("File")

    newItem := fileMenu.Add("New")
    newItem.SetAccelerator("CmdOrCtrl+N")
    newItem.OnClick(func(*application.Context) {
        a.ctx.Events.Emit("menu:new", nil)
    })

    saveItem := fileMenu.Add("Save")
    saveItem.SetAccelerator("CmdOrCtrl+S")
    saveItem.SetEnabled(false)
    saveItem.OnClick(func(*application.Context) {
        a.ctx.Events.Emit("menu:save", nil)
    })

    fileMenu.AddSeparator()

    quitItem := fileMenu.Add("Quit")
    quitItem.SetAccelerator("CmdOrCtrl+Q")
    quitItem.OnClick(func(*application.Context) {
        app.Quit()
    })

    // Set application menu
    app.SetMenu(menu)
}

// Update menu dynamically
func (a *App) updateMenuState(hasUnsavedChanges bool) {
    // This would be implemented based on your menu structure
    a.ctx.Events.Emit("menu:update", map[string]interface{}{
        "saveEnabled": hasUnsavedChanges,
    })
}
```

## Frontend Integration

### React Component Example

```tsx
import React, { useState, useEffect } from 'react';
import { Greet, ProcessData, GetSystemInfo } from '../wailsjs/go/main/App';
import { setupEventListeners, sendRequest } from './events';

function App() {
    const [message, setMessage] = useState('');
    const [systemInfo, setSystemInfo] = useState<any>(null);
    const [isLoading, setIsLoading] = useState(false);

    useEffect(() => {
        // Setup event listeners
        setupEventListeners();

        // Load system info
        loadSystemInfo();
    }, []);

    const loadSystemInfo = async () => {
        try {
            const info = await GetSystemInfo();
            setSystemInfo(info);
        } catch (error) {
            console.error('Failed to load system info:', error);
        }
    };

    const handleGreet = async (name: string) => {
        setIsLoading(true);
        try {
            const result = await Greet(name);
            setMessage(result);

            // Notify backend
            sendRequest('greet_completed', { name, result });
        } catch (error) {
            console.error('Greeting failed:', error);
            setMessage('Error: ' + error.message);
        } finally {
            setIsLoading(false);
        }
    };

    const handleProcessData = async () => {
        const testData = ['item1', 'item2', 'item3'];
        try {
            const result = await ProcessData(testData);
            console.log('Processed data:', result);
            setMessage('Data processed: ' + result.join(', '));
        } catch (error) {
            console.error('Processing failed:', error);
        }
    };

    return (
        <div className="app">
            <h1>Wails 3 Application</h1>

            {systemInfo && (
                <div className="system-info">
                    <h3>System Information</h3>
                    <p>Platform: {systemInfo.platform}</p>
                    <p>Architecture: {systemInfo.arch}</p>
                    <p>Build: {systemInfo.build}</p>
                </div>
            )}

            <div className="greeting-section">
                <input
                    type="text"
                    placeholder="Enter your name"
                    onKeyDown={(e) => {
                        if (e.key === 'Enter' && e.currentTarget.value) {
                            handleGreet(e.currentTarget.value);
                        }
                    }}
                    disabled={isLoading}
                />
                <button
                    onClick={() => {
                        const input = document.querySelector('input') as HTMLInputElement;
                        if (input.value) {
                            handleGreet(input.value);
                        }
                    }}
                    disabled={isLoading}
                >
                    {isLoading ? 'Processing...' : 'Greet'}
                </button>
            </div>

            {message && (
                <div className="message">
                    <p>{message}</p>
                </div>
            )}

            <button onClick={handleProcessData}>
                Process Test Data
            </button>
        </div>
    );
}

export default App;
```

## Development Workflow

### Development Mode

```bash
# Start with hot reload
wails3 dev

# Start with specific frontend port
wails3 dev -frontend-port 3001

# Start with verbose logging
wails3 dev -v

# Skip automatic frontend build
wails3 dev -skip-frontend-build
```

### Production Build

```bash
# Standard build
wails3 build

# Build for specific platform
wails3 build -platform windows/amd64
wails3 build -platform darwin/arm64
wails3 build -platform linux/amd64

# Optimized build
wails3 build -clean -upx -ldflags "-w -s"

# Build for all platforms
wails3 build -all-platforms
```

### Configuration (wails.json)

```json
{
    "$schema": "https://wails.io/schemas/config.v3.json",
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
        "productName": "My Wails 3 App",
        "productVersion": "1.0.0",
        "copyright": "Copyright © 2024 Your Name",
        "comments": "Built using Wails 3"
    },
    "assetdir": "./assets",
    "obfuscated": false,
    "upx": false,
    "compressed": true
}
```

## Advanced Features

### File Watching

```go
func (a *App) setupFileWatcher(app *application.Application) {
    watcher := app.NewFileWatcher(application.FileWatcherOptions{
        Paths: []string{"./config", "./data"},
        Patterns: []string{"*.json", "*.yaml"},
        IgnorePatterns: []string{"*.tmp", "*.log"},
    })

    watcher.OnChange(func(path string) {
        a.ctx.Logger.Info("File changed:", path)
        a.ctx.Events.Emit("file:changed", map[string]interface{}{
            "path": path,
            "timestamp": time.Now(),
        })
    })

    watcher.Start()
}
```

### Logging

```go
import "github.com/wailsapp/wails/v3/pkg/logger"

func (a *App) setupLogging(app *application.Application) {
    app.SetLogger(logger.New(logger.Options{
        Level:  logger.INFO,
        Output: logger.FileOutput("app.log"),
        Format: logger.JSONFormat,
    }))
}
```

### Error Handling Best Practices

```go
func (a *App) SafeOperation(input string) (string, error) {
    // Validate input
    if input == "" {
        return "", errors.New("input cannot be empty")
    }
    if len(input) > 1000 {
        return "", errors.New("input too long")
    }

    // Process with error handling
    result, err := a.processInput(input)
    if err != nil {
        a.ctx.Logger.Error("Processing failed", map[string]interface{}{
            "input": input,
            "error": err.Error(),
        })
        return "", fmt.Errorf("processing failed: %w", err)
    }

    return result, nil
}
```

## Deployment

### Cross-Platform Build Script

```bash
#!/bin/bash

# Build for all platforms
PLATFORMS=(
    "windows/amd64"
    "windows/arm64"
    "darwin/amd64"
    "darwin/arm64"
    "linux/amd64"
    "linux/arm64"
)

for platform in "${PLATFORMS[@]}"; do
    echo "Building for $platform..."
    wails3 build -platform "$platform" -clean
done

echo "All builds completed!"
```

### Package Signing (Windows/macOS)

```bash
# Windows (requires certificate)
wails3 build -platform windows/amd64 -sign

# macOS (requires Apple Developer account)
wails3 build -platform darwin/amd64 -sign
```

## Troubleshooting

### Common Issues

1. **Build fails**: Run `wails3 doctor` to check dependencies
2. **Frontend not loading**: Verify asset embedding in embed.go
3. **Methods not accessible**: Check method binding and capitalization
4. **Events not firing**: Verify event listener registration

### Debug Mode

```go
app := application.New(application.Options{
    Name:        "Debug App",
    Description: "Debug mode enabled",
    Debug:       true,
    Logger: logger.New(logger.Options{
        Level:  logger.DEBUG,
        Output: logger.ConsoleOutput,
    }),
})
```

This comprehensive guide covers all aspects of Wails 3 development, from basic setup to advanced features and deployment.