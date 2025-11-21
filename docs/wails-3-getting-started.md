# Wails 3 Getting Started Guide

## Overview

Wails 3 is the next generation of the Wails framework for building cross-platform desktop applications using Go and web technologies. This version introduces significant improvements including a rewritten application model, enhanced event system, better developer experience, and improved performance.

## What's New in Wails 3

### Key Improvements

- **New Application Model**: Completely rewritten application architecture with better separation of concerns
- **Enhanced Event System**: Cross-platform event handling with OS-specific and platform-agnostic events
- **Dynamic Menu System**: Runtime menu updates and enhanced context menu support
- **Improved File Watching**: Built-in file system watcher with configurable patterns
- **Better Logging**: Enhanced logging system with structured output
- **Theme Support**: Native system theme detection and automatic application theming
- **Simplified API**: More intuitive and consistent API across all platforms
- **Plugin System**: Extensible plugin architecture for community contributions

## Prerequisites

### System Requirements

- **Go**: Version 1.21 or higher
- **Node.js**: Version 18 or higher (for frontend development)
- **Git**: For version control and dependency management

### Platform Dependencies

**Windows:**
- Windows 10 or higher
- No additional dependencies required

**macOS:**
- macOS 11 (Big Sur) or higher
- Xcode Command Line Tools: `xcode-select --install`

**Linux:**
- GTK3 development libraries
- WebKit2GTK
- GCC toolchain

```bash
# Ubuntu/Debian
sudo apt-get install libgtk-3-dev libwebkit2gtk-4.0-dev build-essential

# Fedora/CentOS
sudo dnf install gtk3-devel webkit2gtk3-devel gcc

# Arch Linux
sudo pacman -S gtk3 webkit2gtk base-devel
```

## Installation

### Installing Wails 3 CLI

The Wails 3 CLI is currently in v3-alpha. Here are the installation methods:

#### Method 1: Install from Source (Recommended for Development)

```bash
# Clone the Wails repository
git clone https://github.com/wailsapp/wails.git
cd wails

# Checkout the v3-alpha branch
git checkout v3-alpha

# Install the CLI
cd v3/cmd/wails3
go install

# Verify installation
wails3 version
```

#### Method 2: Using Go Install (When Available)

```bash
# This will be available when Wails 3 is officially released
go install github.com/wailsapp/wails/v3/cmd/wails3@latest
```

### Verifying Installation

```bash
wails3 doctor
```

This command will check your system and report any missing dependencies or configuration issues.

## Creating Your First Wails 3 Application

### Project Initialization

Wails 3 provides several templates for different frontend frameworks:

```bash
# Create a new project with React TypeScript
wails3 init -n my-wails-app -t react-ts

# Create with Vue TypeScript
wails3 init -n my-wails-app -t vue-ts

# Create with vanilla JavaScript
wails3 init -n my-wails-app -t vanilla-js

# Create with Svelte TypeScript
wails3 init -n my-wails-app -t svelte-ts
```

### Project Structure

Wails 3 introduces a cleaner project structure:

```
my-wails-app/
├── main.go              # Application entry point
├── app.go              # Application logic and methods
├── wails.json          # Wails configuration
├── embed.go            # Frontend asset embedding
├── assets/             # Frontend assets (embedded)
├── frontend/           # Frontend source code
│   ├── src/
│   ├── public/
│   ├── package.json
│   └── ...             # Framework-specific files
├── build/              # Build output
└── go.mod              # Go module definition
```

## Application Structure

### Main Application (main.go)

The main entry point uses the new application model:

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

    // Create the main window
    main_window := app.NewWebviewWindowWithOptions(application.WebviewWindowOptions{
        Title:  "My App",
        Width:  1024,
        Height: 768,
    })

    // Start the application
    err := app.Run()

    if err != nil {
        log.Fatal(err)
    }
}
```

### Application Logic (app.go)

Define your application's business logic and methods:

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

    // Log application start
    ctx.Logger.Info("Application started")

    // Emit a custom event
    ctx.Events.Emit("app:ready", map[string]interface{}{
        "timestamp": time.Now(),
        "version":   "1.0.0",
    })
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

    // Process the data
    result := make([]string, len(data))
    for i, item := range data {
        result[i] = fmt.Sprintf("Processed: %s", item)
    }

    return result, nil
}
```

### Binding Methods to Frontend

Use the enhanced binding system to expose Go methods:

```go
func main() {
    app := application.New(application.Options{
        Name:        "My Wails 3 App",
        Description: "A demonstration application",
        Assets: application.AssetOptions{
            Handler: application.AssetFileServerFS(assets),
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
```

## Frontend Integration

### Using Go Methods from JavaScript

Wails 3 automatically generates TypeScript bindings for your Go methods:

```typescript
// Import generated bindings
import { Greet, GetCurrentTime, ProcessData } from '../wailsjs/go/main/App';

// Use Go methods in your frontend
class AppService {
    async greetUser(name: string): Promise<string> {
        try {
            const result = await Greet(name);
            return result;
        } catch (error) {
            console.error('Greeting failed:', error);
            throw error;
        }
    }

    async getCurrentTime(): Promise<string> {
        try {
            const time = await GetCurrentTime();
            return time;
        } catch (error) {
            console.error('Failed to get time:', error);
            throw error;
        }
    }

    async processData(items: string[]): Promise<string[]> {
        try {
            const result = await ProcessData(items);
            return result;
        } catch (error) {
            console.error('Data processing failed:', error);
            throw error;
        }
    }
}

export const appService = new AppService();
```

### Event Handling

Wails 3 provides a powerful event system for communication between frontend and backend:

#### Go Backend Events

```go
// Emit events from Go
func (a *App) NotifyUser(title, message string) {
    a.ctx.Events.Emit("user:notification", map[string]interface{}{
        "title":   title,
        "message": message,
        "time":    time.Now(),
    })
}

// Listen for frontend events
func (a *App) OnStartup(ctx *application.Context) {
    a.ctx = ctx

    // Listen for custom events from frontend
    ctx.Events.On("frontend:action", func(event *application.WailsEvent) {
        ctx.Logger.Info("Received action from frontend:", event.Data)

        // Process the action and emit response
        ctx.Events.Emit("backend:response", map[string]interface{}{
            "status":  "success",
            "message": "Action completed",
        })
    })
}
```

#### JavaScript Frontend Events

```typescript
import { EventsOn, EventsEmit } from '../wailsjs/runtime/runtime';

// Listen for events from Go
export function setupEventListeners() {
    // Listen for notifications
    EventsOn('user:notification', (data) => {
        console.log('Notification received:', data);
        showNotification(data.title, data.message);
    });

    // Listen for backend responses
    EventsOn('backend:response', (data) => {
        console.log('Backend response:', data);
        if (data.status === 'success') {
            showSuccessMessage(data.message);
        } else {
            showErrorMessage(data.message);
        }
    });
}

// Emit events to Go
export function triggerAction(action: string, payload: any) {
    EventsEmit('frontend:action', {
        action: action,
        payload: payload,
        timestamp: new Date().toISOString(),
    });
}
```

### React Example with Wails 3

```tsx
import React, { useState, useEffect } from 'react';
import { appService } from './services/appService';
import { setupEventListeners, triggerAction } from './events';

function App() {
    const [message, setMessage] = useState('');
    const [currentTime, setCurrentTime] = useState('');
    const [notifications, setNotifications] = useState<any[]>([]);

    useEffect(() => {
        // Setup event listeners
        setupEventListeners();

        // Load initial time
        loadCurrentTime();
    }, []);

    const loadCurrentTime = async () => {
        try {
            const time = await appService.getCurrentTime();
            setCurrentTime(time);
        } catch (error) {
            console.error('Failed to load time:', error);
        }
    };

    const handleGreet = async (name: string) => {
        try {
            const greeting = await appService.greetUser(name);
            setMessage(greeting);

            // Trigger an action in Go
            triggerAction('greet_completed', { name, greeting });
        } catch (error) {
            console.error('Greeting failed:', error);
        }
    };

    const handleProcessData = async () => {
        const testData = ['item1', 'item2', 'item3'];
        try {
            const result = await appService.processData(testData);
            console.log('Processed data:', result);
        } catch (error) {
            console.error('Data processing failed:', error);
        }
    };

    return (
        <div className="app">
            <h1>Wails 3 React Application</h1>

            <div className="time-display">
                <p>Current Time: {currentTime}</p>
                <button onClick={loadCurrentTime}>Refresh Time</button>
            </div>

            <div className="greeting-section">
                <input
                    type="text"
                    placeholder="Enter your name"
                    onKeyDown={(e) => {
                        if (e.key === 'Enter' && e.currentTarget.value) {
                            handleGreet(e.currentTarget.value);
                        }
                    }}
                />
                <button onClick={() => {
                    const input = document.querySelector('input') as HTMLInputElement;
                    if (input.value) {
                        handleGreet(input.value);
                    }
                }}>
                    Greet
                </button>
                {message && <p className="message">{message}</p>}
            </div>

            <div className="data-processing">
                <button onClick={handleProcessData}>Process Test Data</button>
            </div>

            <div className="notifications">
                <h3>Notifications</h3>
                {notifications.map((notification, index) => (
                    <div key={index} className="notification">
                        <strong>{notification.title}</strong>: {notification.message}
                    </div>
                ))}
            </div>
        </div>
    );
}

export default App;
```

## Advanced Features

### System Theme Detection

Wails 3 provides built-in theme detection that works across all platforms:

#### Go Backend Theme Handling

```go
import (
    "github.com/wailsapp/wails/v3/pkg/application"
    "github.com/wailsapp/wails/v3/pkg/events"
)

func (a *App) OnStartup(ctx *application.Context) {
    a.ctx = ctx

    // Listen for system theme changes
    app.OnApplicationEvent(events.Common.ThemeChanged, func(event *application.ApplicationEvent) {
        if event.Context().IsDarkMode() {
            ctx.Logger.Info("System switched to dark mode")
            ctx.Events.Emit("theme:changed", { "isDark": true })
        } else {
            ctx.Logger.Info("System switched to light mode")
            ctx.Events.Emit("theme:changed", { "isDark": false })
        }
    })
}
```

#### JavaScript Theme Handling

```typescript
// Listen for theme changes
EventsOn('theme:changed', (data) => {
    const isDark = data.isDark;

    if (isDark) {
        document.body.classList.add('dark-theme');
        document.body.classList.remove('light-theme');
    } else {
        document.body.classList.add('light-theme');
        document.body.classList.remove('dark-theme');
    }

    // Save theme preference
    localStorage.setItem('theme', isDark ? 'dark' : 'light');
});

// Apply saved theme on load
function applySavedTheme() {
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme === 'dark') {
        document.body.classList.add('dark-theme');
    } else {
        document.body.classList.add('light-theme');
    }
}
```

### Dynamic Menu System

Wails 3 allows runtime menu updates and enhanced menu management:

```go
func (a *App) setupMenus(app *application.Application) {
    // Create main menu bar
    menu := app.NewMenu()

    // File menu
    fileMenu := menu.AddSubmenu("File")

    newItem := fileMenu.Add("New")
    newItem.SetAccelerator("CmdOrCtrl+N")
    newItem.OnClick(func(*application.Context) {
        a.ctx.Logger.Info("New file requested")
        a.ctx.Events.Emit("menu:new-file", nil)
    })

    saveItem := fileMenu.Add("Save")
    saveItem.SetAccelerator("CmdOrCtrl+S")
    saveItem.SetEnabled(false) // Initially disabled
    saveItem.OnClick(func(*application.Context) {
        a.ctx.Logger.Info("Save requested")
        a.ctx.Events.Emit("menu:save", nil)
    })

    // Edit menu
    editMenu := menu.AddSubmenu("Edit")
    undoItem := editMenu.Add("Undo")
    undoItem.SetAccelerator("CmdOrCtrl+Z")

    // Set the application menu
    app.SetMenu(menu)

    // Example of updating menu items dynamically
    app.OnApplicationEvent(events.Common.FileModified, func(event *application.ApplicationEvent) {
        saveItem.SetEnabled(true)
        saveItem.SetLabel("Save *")
        menu.Update() // Apply changes
    })
}
```

### File Watching

Wails 3 includes a built-in file watcher for development:

```go
func (a *App) setupFileWatcher(app *application.Application) {
    // Watch configuration files for changes
    watcher := app.NewFileWatcher(application.FileWatcherOptions{
        Paths: []string{"./config", "./data"},
        Patterns: []string{"*.json", "*.yaml", "*.toml"},
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

### Enhanced Logging

Wails 3 provides structured logging with multiple output options:

```go
import (
    "github.com/wailsapp/wails/v3/pkg/application"
    "github.com/wailsapp/wails/v3/pkg/logger"
)

func (a *App) setupLogging(app *application.Application) {
    // Configure logging
    app.SetLogger(logger.New(logger.Options{
        Level:    logger.INFO,
        Output:   logger.FileOutput("app.log"),
        Format:   logger.JSONFormat,
    }))

    // Log different levels
    a.ctx.Logger.Debug("Debug message")
    a.ctx.Logger.Info("Info message")
    a.ctx.Logger.Warn("Warning message")
    a.ctx.Logger.Error("Error message")

    // Structured logging
    a.ctx.Logger.Info("User action", map[string]interface{}{
        "action": "login",
        "user_id": 123,
        "timestamp": time.Now(),
    })
}
```

## Development Workflow

### Running in Development Mode

```bash
# Start development server with hot reload
wails3 dev

# Start with specific frontend port
wails3 dev -frontend-port 3001

# Start with verbose logging
wails3 dev -v

# Start without automatic frontend building
wails3 dev -skip-frontend-build
```

### Building for Production

```bash
# Standard build
wails3 build

# Build for specific platform
wails3 build -platform windows/amd64
wails3 build -platform darwin/arm64
wails3 build -platform linux/amd64

# Build with optimization
wails3 build -clean -upx -ldflags "-w -s"

# Build with custom output directory
wails3 build -output ./dist/myapp

# Build for all platforms
wails3 build -all-platforms
```

### File Watcher Tool

Use the built-in file watcher for development automation:

```bash
# Watch current directory
wails3 tool watcher

# Watch with custom configuration
wails3 tool watcher -config watcher.json

# Watch with specific patterns
wails3 tool watcher -include "*.go,*.js,*.ts" -ignore "*.tmp"

# Example watcher.json configuration
{
    "watch": ["./src", "./config"],
    "ignore": ["node_modules", "*.tmp"],
    "patterns": ["*.go", "*.js", "*.ts", "*.json"],
    "command": "wails3 build",
    "debounce": "500ms"
}
```

## Configuration

### Wails Configuration (wails.json)

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
        "comments": "Built using Wails 3 (https://wails.io)"
    },
    "assetdir": "./assets",
    "obfuscated": false,
    "garbleargs": "",
    "upx": false,
    "upxflags": "",
    "compressed": true,
    "runNonNativeBuildHooks": false,
    "useBuildDirectory": false,
    "generateBuildScript": false,
    "logger": {
        "level": "info",
        "output": "app.log",
        "format": "json"
    }
}
```

### Environment-Specific Configuration

You can use environment-specific configuration files:

- `wails.json` - Base configuration
- `wails.dev.json` - Development overrides
- `wails.prod.json` - Production overrides

Example `wails.dev.json`:
```json
{
    "logger": {
        "level": "debug",
        "output": "console"
    },
    "obfuscated": false,
    "upx": false
}
```

## Best Practices

### Performance Optimization

1. **Minimize Go-JavaScript calls**: Batch operations when possible
2. **Use streams for large data**: Process large files in chunks
3. **Optimize asset loading**: Use lazy loading for large assets
4. **Leverage Go concurrency**: Use goroutines for background tasks
5. **Cache frequently accessed data**: Reduce backend calls

### Security Considerations

1. **Validate all inputs**: Sanitize data in Go before processing
2. **Use secure file operations**: Validate file paths and permissions
3. **Implement proper error handling**: Avoid exposing sensitive information
4. **Use HTTPS for network requests**: Encrypt all communications
5. **Obfuscate sensitive code**: Use garble for production builds

### Code Organization

```
src/
├── main.go              # Application entry point
├── app.go              # Main application logic
├── handlers/           # Event handlers
│   ├── file.go
│   └── menu.go
├── services/           # Business logic
│   ├── data.go
│   └── api.go
├── models/            # Data structures
│   └── user.go
└── utils/             # Utility functions
    ├── logger.go
    └── helpers.go
```

### Error Handling

```go
func (a *App) SafeOperation(data string) (string, error) {
    if data == "" {
        return "", errors.New("data cannot be empty")
    }

    // Validate data
    if len(data) > 1000 {
        return "", errors.New("data too long")
    }

    // Process data
    result := strings.ToUpper(data)
    return result, nil
}

// In frontend
async function performOperation(input: string): Promise<string> {
    try {
        const result = await SafeOperation(input);
        return result;
    } catch (error) {
        console.error('Operation failed:', error);
        throw new Error(`Operation failed: ${error.message}`);
    }
}
```

## Troubleshooting

### Common Issues

1. **Build fails**: Run `wails3 doctor` to check dependencies
2. **Frontend not loading**: Verify asset embedding and paths
3. **Methods not accessible**: Check method binding and capitalization
4. **Hot reload not working**: Ensure development server is running
5. **Events not firing**: Verify event listener registration

### Debug Mode

Enable debug mode for detailed logging:

```go
app := application.New(application.Options{
    Name:        "Debug App",
    Description: "Debug mode enabled",
    Debug:       true, // Enable debug mode
    Logger: logger.New(logger.Options{
        Level:  logger.DEBUG,
        Output: logger.ConsoleOutput,
    }),
})
```

### Performance Profiling

Use Go's built-in profiling tools:

```go
import _ "net/http/pprof"

func main() {
    // Start pprof server
    go func() {
        log.Println(http.ListenAndServe("localhost:6060", nil))
    }()

    // Rest of application...
}
```

Then access profiling data at `http://localhost:6060/debug/pprof/`

## Resources

- **Official Documentation**: https://v3alpha.wails.io/
- **GitHub Repository**: https://github.com/wailsapp/wails/
- **Community Discord**: https://discord.gg/wails
- **Example Projects**: https://github.com/wailsapp/wails/tree/master/examples
- **Migration Guide**: https://v3alpha.wails.io/docs/migration

## Conclusion

Wails 3 represents a significant evolution in desktop application development, combining Go's performance with modern web technologies. The new application model, enhanced event system, and improved developer experience make it an excellent choice for building cross-platform desktop applications.

Key advantages of Wails 3:
- Native performance with small bundle sizes
- Rich event system for responsive applications
- Modern development workflow with hot reload
- Cross-platform consistency
- Strong Go ecosystem integration
- Active community and regular updates

Start building your next desktop application with Wails 3 and experience the power of Go combined with modern web technologies!