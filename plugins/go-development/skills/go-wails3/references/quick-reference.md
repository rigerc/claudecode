# Wails 3 Quick Reference

## CLI Commands

### Installation
```bash
git clone https://github.com/wailsapp/wails.git
cd wails && git checkout v3-alpha
cd v3/cmd/wails3 && go install
wails3 doctor
```

### Project Management
```bash
wails3 init -n my-app -t react-ts    # Create new project
wails3 dev                           # Development mode
wails3 build                         # Production build
wails3 build -platform windows/amd64 # Platform-specific build
```

## Core Code Patterns

### Basic Application Structure
```go
package main

import (
    "embed"
    "github.com/wailsapp/wails/v3/pkg/application"
)

//go:embed assets
var assets embed.FS

func main() {
    app := application.New(application.Options{
        Name: "My App",
        Assets: application.AssetOptions{
            Handler: application.AssetFileServerFS(assets),
        },
    })

    app.Bind(&App{})
    app.NewWebviewWindow()
    app.Run()
}
```

### Method Binding
```go
type App struct {
    ctx *application.Context
}

func (a *App) Greet(name string) string {
    return fmt.Sprintf("Hello, %s!", name)
}

// In main.go:
app.Bind(&App{})
```

### Event System
```go
// Emit from Go
a.ctx.Events.Emit("my-event", data)

// Listen in Go
a.ctx.Events.On("frontend-event", func(event *application.WailsEvent) {
    // Handle event
})
```

```typescript
// TypeScript frontend
import { EventsOn, EventsEmit } from '../wailsjs/runtime/runtime';

// Listen for events
EventsOn('my-event', (data) => console.log(data));

// Emit events
EventsEmit('frontend-event', { action: 'test' });
```

### File Operations
```go
// Read file
data, err := os.ReadFile(path)

// File dialog
selectedFile, err := a.ctx.Runtime.OpenFileDialog(a.ctx, runtime.OpenDialogOptions{
    Title: "Select file",
    Filters: []runtime.FileFilter{{DisplayName: "Text Files", Pattern: "*.txt"}},
})
```

### Menu System
```go
menu := app.NewMenu()
fileMenu := menu.AddSubmenu("File")
newItem := fileMenu.Add("New")
newItem.SetAccelerator("CmdOrCtrl+N")
newItem.OnClick(func(*application.Context) { /* handle click */ })
app.SetMenu(menu)
```

### Theme Detection
```go
app.OnApplicationEvent(events.Common.ThemeChanged, func(event *application.ApplicationEvent) {
    isDark := event.Context().IsDarkMode()
    a.ctx.Events.Emit("theme:changed", isDark)
})
```

## Frontend Integration

### TypeScript Bindings
```typescript
import { Greet, ProcessData } from '../wailsjs/go/main/App';

const result = await Greet("World");
const processed = await ProcessData(["item1", "item2"]);
```

### React Hook Pattern
```tsx
import { useState, useEffect } from 'react';
import { EventsOn } from '../wailsjs/runtime/runtime';

function useWailsEvent(eventName: string) {
    const [data, setData] = useState(null);

    useEffect(() => {
        EventsOn(eventName, setData);
    }, [eventName]);

    return data;
}
```

## Configuration

### wails.json
```json
{
    "name": "my-app",
    "frontend": {
        "dir": "./frontend",
        "install": "npm install",
        "build": "npm run build"
    },
    "info": {
        "productName": "My App",
        "productVersion": "1.0.0"
    }
}
```

## Platform-Specific

### Windows
```go
Windows: application.WindowsOptions{
    WebviewIsTransparent: false,
    WindowIsResizable:    true,
}
```

### macOS
```go
Mac: application.MacOptions{
    TitleBar: macos.TitleBarOptions{
        TitlebarAppearsTransparent: true,
    },
}
```

### Linux
```go
Linux: application.LinuxOptions{
    Icon: []byte{}, // Window icon bytes
}
```

## Debugging

### Enable Debug Mode
```go
app := application.New(application.Options{
    Debug: true,
    Logger: logger.New(logger.Options{
        Level: logger.DEBUG,
    }),
})
```

### Common Issues
- **Methods not accessible**: Check capitalization (must be public)
- **Assets not loading**: Verify `//go:embed` directive
- **Events not firing**: Check listener registration
- **Build fails**: Run `wails3 doctor`

## Performance Tips

1. **Minimize Go-JS calls**: Batch operations
2. **Use streaming for large data**: Process in chunks
3. **Optimize assets**: Use lazy loading
4. **Leverage goroutines**: Background tasks
5. **Cache frequent data**: Reduce backend calls