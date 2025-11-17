package main

import (
    "fyne.io/fyne/v2/app"
    "fyne.io/fyne/v2/container"
    "fyne.io/fyne/v2/widget"
)

func main() {
    // Create new application
    myApp := app.New()

    // Set application metadata
    myApp.Settings().SetTheme(widget.DefaultTheme())  // Can use custom theme

    // Create main window
    myWindow := myApp.NewWindow("Hello Fyne!")
    myWindow.Resize(fyne.NewSize(400, 300))

    // Create welcome label
    welcomeLabel := widget.NewLabel("Welcome to Fyne!")
    welcomeLabel.TextStyle.Bold = true

    // Create description
    description := widget.NewLabel("This is a simple Fyne application template.")

    // Create interactive elements
    nameEntry := widget.NewEntry()
    nameEntry.SetPlaceHolder("Enter your name")

    greetingLabel := widget.NewLabel("Hello!")

    // Button with action
    greetButton := widget.NewButton("Say Hello", func() {
        if nameEntry.Text != "" {
            greetingLabel.SetText("Hello, " + nameEntry.Text + "!")
        } else {
            greetingLabel.SetText("Please enter your name first.")
        }
    })

    // Clear button
    clearButton := widget.NewButton("Clear", func() {
        nameEntry.SetText("")
        greetingLabel.SetText("Hello!")
    })

    // Create layout
    content := container.NewVBox(
        welcomeLabel,
        widget.NewSeparator(),
        description,
        widget.NewSeparator(),
        widget.NewLabel("Your Name:"),
        nameEntry,
        container.NewHBox(greetButton, clearButton),
        widget.NewSeparator(),
        greetingLabel,
    )

    // Alternative: Border layout
    // content := container.NewBorder(
    //     widget.NewLabel("Header"),           // top
    //     widget.NewLabel("Footer"),           // bottom
    //     widget.NewLabel("Left"),             // left
    //     widget.NewLabel("Right"),            // right
    //     container.NewVBox(welcomeLabel, nameEntry, greetingLabel), // center
    // )

    // Alternative: Grid layout
    // content := container.NewGridWithColumns(2,
    //     widget.NewLabel("Name:"), nameEntry,
    //     widget.NewLabel("Greeting:"), greetingLabel,
    //     greetButton, clearButton,
    // )

    // Set window content
    myWindow.SetContent(content)

    // Show and run application
    myWindow.ShowAndRun()
}

// Advanced template with menus and additional features:

/*
package main

import (
    "fyne.io/fyne/v2/app"
    "fyne.io/fyne/v2/container"
    "fyne.io/fyne/v2/dialog"
    "fyne.io/fyne/v2/theme"
    "fyne.io/fyne/v2/widget"
)

func main() {
    myApp := app.New()

    // Create main window
    myWindow := myApp.NewWindow("Advanced Fyne Template")
    myWindow.Resize(fyne.NewSize(600, 400))

    // Setup menus
    setupMenus(myApp, myWindow)

    // Create toolbar
    toolbar := createToolbar()

    // Create content
    content := createContent()

    // Set window content with toolbar
    myWindow.SetContent(container.NewBorder(
        toolbar,  // top
        nil,     // bottom
        nil,     // left
        nil,     // right
        content, // center
    ))

    myWindow.ShowAndRun()
}

func setupMenus(a fyne.App, w fyne.Window) {
    // File menu
    fileMenu := fyne.NewMenu("File",
        fyne.NewMenuItem("New", func() {
            dialog.ShowInformation("New", "New file created", w)
        }),
        fyne.NewMenuItem("Open", func() {
            dialog.ShowFileOpen(func(reader fyne.URIReadCloser, err error) {
                if err == nil && reader != nil {
                    defer reader.Close()
                    dialog.ShowInformation("Open", "File opened successfully", w)
                }
            }, w)
        }),
        fyne.NewMenuItemSeparator(),
        fyne.NewMenuItem("Quit", func() {
            a.Quit()
        }),
    )

    // Edit menu
    editMenu := fyne.NewMenu("Edit",
        fyne.NewMenuItem("Copy", func() {
            dialog.ShowInformation("Copy", "Copy action", w)
        }),
        fyne.NewMenuItem("Paste", func() {
            dialog.ShowInformation("Paste", "Paste action", w)
        }),
    )

    // Help menu
    helpMenu := fyne.NewMenu("Help",
        fyne.NewMenuItem("About", func() {
            dialog.ShowInformation("About", "Fyne Template v1.0", w)
        }),
    )

    mainMenu := fyne.NewMainMenu(fileMenu, editMenu, helpMenu)
    w.SetMainMenu(mainMenu)
}

func createToolbar() *widget.Toolbar {
    return widget.NewToolbar(
        widget.NewToolbarAction(theme.DocumentCreateIcon(), func() {
            // New file action
        }),
        widget.NewToolbarAction(theme.FolderOpenIcon(), func() {
            // Open file action
        }),
        widget.NewToolbarSeparator(),
        widget.NewToolbarAction(theme.ContentCutIcon(), func() {
            // Cut action
        }),
        widget.NewToolbarAction(theme.ContentCopyIcon(), func() {
            // Copy action
        }),
        widget.NewToolbarAction(theme.ContentPasteIcon(), func() {
            // Paste action
        }),
        widget.NewToolbarSeparator(),
        widget.NewToolbarSpacer(),
        widget.NewToolbarAction(theme.SettingsIcon(), func() {
            // Settings action
        }),
    )
}

func createContent() fyne.CanvasObject {
    // Create tabs
    tabs := container.NewAppTabs(
        container.NewTabItemWithIcon("Home", theme.HomeIcon(), createHomeTab()),
        container.NewTabItemWithIcon("Settings", theme.SettingsIcon(), createSettingsTab()),
        container.NewTabItemWithIcon("About", theme.InfoIcon(), createAboutTab()),
    )

    return tabs
}

func createHomeTab() fyne.CanvasObject {
    return container.NewVBox(
        widget.NewCard("Welcome", "Fyne Application Template",
            container.NewVBox(
                widget.NewLabel("This is a comprehensive Fyne application template."),
                widget.NewLabel("It demonstrates various Fyne features and patterns."),
            ),
        ),
        widget.NewCard("Features", "What's included",
            container.NewVBox(
                widget.NewLabel("• Cross-platform GUI toolkit"),
                widget.NewLabel("• Material Design components"),
                widget.NewLabel("• Menus and toolbars"),
                widget.NewLabel("• Tabbed interface"),
                widget.NewLabel("• Responsive layouts"),
            ),
        ),
    )
}

func createSettingsTab() fyne.CanvasObject {
    themeSelector := widget.NewSelect([]string{"Light", "Dark", "Custom"}, func(selected string) {
        // Handle theme selection
    })

    return container.NewVBox(
        widget.NewCard("Appearance", "Customize the look and feel",
            container.NewVBox(
                widget.NewLabel("Theme:"),
                themeSelector,
            ),
        ),
        widget.NewCard("Preferences", "Application settings",
            container.NewVBox(
                widget.NewCheck("Enable notifications", func(checked bool) {
                    // Handle notification setting
                }),
                widget.NewCheck("Auto-save", func(checked bool) {
                    // Handle auto-save setting
                }),
            ),
        ),
    )
}

func createAboutTab() fyne.CanvasObject {
    return container.NewVBox(
        widget.NewCard("About", "Application information",
            container.NewVBox(
                widget.NewLabel("Fyne Template Application"),
                widget.NewLabel("Version: 1.0.0"),
                widget.NewLabel("Built with Fyne v2"),
                widget.NewSeparator(),
                widget.NewLabel("A demonstration of Fyne capabilities"),
            ),
        ),
        widget.NewCard("Credits", "Acknowledgments",
            container.NewVBox(
                widget.NewLabel("Created with Fyne GUI toolkit"),
                widget.NewLabel("https://fyne.io/"),
                widget.NewSeparator(),
                widget.NewLabel("Icons provided by Material Design"),
            ),
        ),
    )
}
*/