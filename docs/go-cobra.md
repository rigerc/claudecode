# Cobra: Modern CLI Applications in Go

Cobra is a powerful library for creating command-line interfaces (CLIs) in Go. It provides a simple interface for building complex CLI applications with subcommands, flags, and automatic help generation.

## Table of Contents

- [Quick Start](#quick-start)
- [Core Concepts](#core-concepts)
- [Commands](#commands)
- [Flags](#flags)
- [Arguments and Validation](#arguments-and-validation)
- [Command Lifecycle Hooks](#command-lifecycle-hooks)
- [Completion](#completion)
- [Configuration with Viper](#configuration-with-viper)
- [Best Practices](#best-practices)
- [Examples](#examples)

## Quick Start

### Installation

```bash
go get -u github.com/spf13/cobra@latest
```

### Minimal Example

```go
package main

import (
	"fmt"
	"github.com/spf13/cobra"
	"os"
)

func main() {
	var rootCmd = &cobra.Command{
		Use:   "myapp",
		Short: "A brief description of your application",
		Long:  `A longer description that spans multiple lines`,
		Run: func(cmd *cobra.Command, args []string) {
			fmt.Println("Hello from myapp!")
		},
	}

	if err := rootCmd.Execute(); err != nil {
		fmt.Fprintln(os.Stderr, err)
		os.Exit(1)
	}
}
```

### Recommended Project Structure

```
myapp/
├── main.go              # Entry point
├── cmd/
│   ├── root.go         # Root command definition
│   ├── version.go      # Version subcommand
│   └── serve.go        # Serve subcommand
└── go.mod
```

**main.go:**
```go
package main

import "myapp/cmd"

func main() {
	cmd.Execute()
}
```

**cmd/root.go:**
```go
package cmd

import (
	"fmt"
	"os"
	"github.com/spf13/cobra"
)

var rootCmd = &cobra.Command{
	Use:   "myapp",
	Short: "A brief description",
}

func Execute() {
	if err := rootCmd.Execute(); err != nil {
		fmt.Fprintln(os.Stderr, err)
		os.Exit(1)
	}
}

func init() {
	// Add subcommands here
	rootCmd.AddCommand(versionCmd)
}
```

## Core Concepts

### Commands

A command represents an action that your CLI can perform. Commands can have:
- **Subcommands**: Nested commands (e.g., `git commit`, `git push`)
- **Flags**: Options that modify behavior
- **Arguments**: Positional parameters
- **Aliases**: Alternative names for the command

### Command Structure

```go
var myCmd = &cobra.Command{
	Use:   "mycmd [flags]",          // How to use this command
	Short: "Brief description",       // Shown in help
	Long:  "Detailed description",    // Shown in extended help
	Example: "myapp mycmd --flag",    // Usage examples
	Aliases: []string{"mc"},          // Alternative names
	Args: cobra.MinimumNArgs(1),      // Argument validation
	Run: func(cmd *cobra.Command, args []string) {
		// Command logic here
	},
}
```

## Commands

### Creating Commands

```go
var serveCmd = &cobra.Command{
	Use:   "serve",
	Short: "Start the server",
	Long:  `Start the HTTP server on the specified port`,
	Run: func(cmd *cobra.Command, args []string) {
		fmt.Println("Server starting...")
	},
}
```

### Adding Subcommands

```go
func init() {
	rootCmd.AddCommand(serveCmd)
	rootCmd.AddCommand(versionCmd)
	rootCmd.AddCommand(configCmd)
}
```

### Nested Subcommands

```go
var echoCmd = &cobra.Command{
	Use:   "echo",
	Short: "Echo commands",
}

var echoTimesCmd = &cobra.Command{
	Use:   "times [string]",
	Short: "Echo multiple times",
	Args:  cobra.MinimumNArgs(1),
	Run: func(cmd *cobra.Command, args []string) {
		times, _ := cmd.Flags().GetInt("times")
		for i := 0; i < times; i++ {
			fmt.Println(args[0])
		}
	},
}

func init() {
	rootCmd.AddCommand(echoCmd)
	echoCmd.AddCommand(echoTimesCmd)
	echoTimesCmd.Flags().IntP("times", "t", 1, "times to echo")
}
```

## Flags

Flags modify command behavior. Cobra supports two types of flags:
- **Local flags**: Available only to a specific command
- **Persistent flags**: Available to the command and all subcommands

### Local Flags

```go
func init() {
	// String flag
	serveCmd.Flags().StringP("port", "p", "8080", "Port to run server on")

	// Boolean flag
	serveCmd.Flags().BoolP("verbose", "v", false, "Enable verbose output")

	// Integer flag
	serveCmd.Flags().IntP("timeout", "t", 30, "Request timeout in seconds")
}
```

### Persistent Flags

```go
func init() {
	// Available to all commands
	rootCmd.PersistentFlags().StringVar(&cfgFile, "config", "", "config file path")
	rootCmd.PersistentFlags().BoolVar(&verbose, "verbose", false, "verbose output")
}
```

### Binding Flags to Variables

```go
var (
	port    string
	verbose bool
)

func init() {
	serveCmd.Flags().StringVarP(&port, "port", "p", "8080", "Port number")
	serveCmd.Flags().BoolVarP(&verbose, "verbose", "v", false, "Verbose output")
}
```

### Required Flags

```go
func init() {
	serveCmd.Flags().StringP("host", "h", "", "Host address (required)")
	serveCmd.MarkFlagRequired("host")
}
```

### Flag Validation

```go
func init() {
	// Mutually exclusive flags
	cmd.Flags().BoolVar(&outputJSON, "json", false, "Output in JSON")
	cmd.Flags().BoolVar(&outputYAML, "yaml", false, "Output in YAML")
	cmd.MarkFlagsMutuallyExclusive("json", "yaml")

	// Required together
	cmd.Flags().StringVar(&username, "username", "", "Username")
	cmd.Flags().StringVar(&password, "password", "", "Password")
	cmd.MarkFlagsRequiredTogether("username", "password")

	// One of required
	cmd.Flags().String("format", "", "Output format")
	cmd.Flags().String("template", "", "Output template")
	cmd.MarkFlagsOneRequired("format", "template")
}
```

### Flag Types

```go
// String flags
cmd.Flags().String("name", "", "description")
cmd.Flags().StringP("name", "n", "", "description")  // with shorthand

// Boolean flags
cmd.Flags().Bool("verbose", false, "description")
cmd.Flags().BoolP("verbose", "v", false, "description")

// Integer flags
cmd.Flags().Int("count", 0, "description")
cmd.Flags().IntP("count", "c", 0, "description")

// String slice flags
cmd.Flags().StringSlice("tags", []string{}, "description")

// Duration flags
cmd.Flags().Duration("timeout", 30*time.Second, "description")
```

### Accessing Flag Values

```go
Run: func(cmd *cobra.Command, args []string) {
	// Method 1: Using bound variables
	fmt.Println("Port:", port)

	// Method 2: Using flag lookup
	host, _ := cmd.Flags().GetString("host")
	verbose, _ := cmd.Flags().GetBool("verbose")
	timeout, _ := cmd.Flags().GetInt("timeout")

	fmt.Println("Host:", host)
	fmt.Println("Verbose:", verbose)
	fmt.Println("Timeout:", timeout)
}
```

## Arguments and Validation

### Argument Validators

Cobra provides built-in validators for positional arguments:

```go
// No arguments
Args: cobra.NoArgs

// Exactly N arguments
Args: cobra.ExactArgs(2)

// Minimum N arguments
Args: cobra.MinimumNArgs(1)

// Maximum N arguments
Args: cobra.MaximumNArgs(3)

// Range of arguments
Args: cobra.RangeArgs(2, 4)
```

### Custom Validation

```go
var myCmd = &cobra.Command{
	Use:   "mycmd [color]",
	Short: "Do something with a color",
	Args: func(cmd *cobra.Command, args []string) error {
		// First validate count
		if err := cobra.MinimumNArgs(1)(cmd, args); err != nil {
			return err
		}

		// Custom validation
		validColors := map[string]bool{
			"red": true, "green": true, "blue": true,
		}
		if !validColors[args[0]] {
			return fmt.Errorf("invalid color: %s", args[0])
		}
		return nil
	},
	Run: func(cmd *cobra.Command, args []string) {
		fmt.Printf("Color: %s\n", args[0])
	},
}
```

### Valid Arguments

```go
var getCmd = &cobra.Command{
	Use:       "get [resource]",
	Short:     "Get resources",
	ValidArgs: []string{"pod", "node", "service", "deployment"},
	Args:      cobra.ExactArgs(1),
	Run: func(cmd *cobra.Command, args []string) {
		fmt.Printf("Getting %s...\n", args[0])
	},
}
```

## Command Lifecycle Hooks

Commands support pre and post execution hooks:

```go
var rootCmd = &cobra.Command{
	Use: "app",

	// Runs before all other hooks (inherited by children)
	PersistentPreRun: func(cmd *cobra.Command, args []string) {
		fmt.Println("PersistentPreRun: Setup")
	},

	// Runs before Run (not inherited)
	PreRun: func(cmd *cobra.Command, args []string) {
		fmt.Println("PreRun: Validate")
	},

	// Main command logic
	Run: func(cmd *cobra.Command, args []string) {
		fmt.Println("Run: Execute")
	},

	// Runs after Run (not inherited)
	PostRun: func(cmd *cobra.Command, args []string) {
		fmt.Println("PostRun: Cleanup")
	},

	// Runs after all other hooks (inherited by children)
	PersistentPostRun: func(cmd *cobra.Command, args []string) {
		fmt.Println("PersistentPostRun: Final cleanup")
	},
}
```

**Execution Order:**
1. `PersistentPreRun` (parent, then current)
2. `PreRun` (current only)
3. `Run` (current only)
4. `PostRun` (current only)
5. `PersistentPostRun` (current, then parent)

### Error Handling

```go
var myCmd = &cobra.Command{
	Use:  "mycmd",
	RunE: func(cmd *cobra.Command, args []string) error {
		if err := doSomething(); err != nil {
			return fmt.Errorf("failed to do something: %w", err)
		}
		return nil
	},
}
```

Use `RunE` instead of `Run` to return errors. Cobra will handle error printing and exit codes.

## Completion

Cobra provides automatic shell completion for Bash, Zsh, Fish, and PowerShell.

### Generating Completion Scripts

```go
var completionCmd = &cobra.Command{
	Use:   "completion [bash|zsh|fish|powershell]",
	Short: "Generate completion script",
	Long: `To load completions:

Bash:
  $ source <(yourprogram completion bash)

Zsh:
  $ source <(yourprogram completion zsh)

Fish:
  $ yourprogram completion fish | source

PowerShell:
  PS> yourprogram completion powershell | Out-String | Invoke-Expression
`,
	DisableFlagsInUseLine: true,
	ValidArgs:             []string{"bash", "zsh", "fish", "powershell"},
	Args:                  cobra.ExactArgs(1),
	Run: func(cmd *cobra.Command, args []string) {
		switch args[0] {
		case "bash":
			cmd.Root().GenBashCompletion(os.Stdout)
		case "zsh":
			cmd.Root().GenZshCompletion(os.Stdout)
		case "fish":
			cmd.Root().GenFishCompletion(os.Stdout, true)
		case "powershell":
			cmd.Root().GenPowerShellCompletionWithDesc(os.Stdout)
		}
	},
}
```

### Custom Completions

#### Static Completions

```go
var getCmd = &cobra.Command{
	Use:       "get [resource]",
	ValidArgs: []string{"pod", "node", "service"},
	Run: func(cmd *cobra.Command, args []string) {
		// ...
	},
}
```

#### Dynamic Completions

```go
var statusCmd = &cobra.Command{
	Use:   "status [release]",
	Short: "Show release status",
	ValidArgsFunction: func(cmd *cobra.Command, args []string, toComplete string) ([]string, cobra.ShellCompDirective) {
		if len(args) != 0 {
			return nil, cobra.ShellCompDirectiveNoFileComp
		}
		// Return list of releases from cluster
		releases := getReleases(toComplete)
		return releases, cobra.ShellCompDirectiveNoFileComp
	},
}
```

#### Flag Completions

```go
func init() {
	cmd.Flags().String("output", "", "Output format")
	cmd.RegisterFlagCompletionFunc("output", func(cmd *cobra.Command, args []string, toComplete string) ([]string, cobra.ShellCompDirective) {
		return []string{"json", "yaml", "table"}, cobra.ShellCompDirectiveDefault
	})

	// File completions
	cmd.Flags().String("config", "", "Config file")
	cmd.MarkFlagFilename("config", "yaml", "yml", "json")

	// Directory completions
	cmd.Flags().String("output-dir", "", "Output directory")
	cmd.MarkFlagDirname("output-dir")
}
```

## Configuration with Viper

Cobra integrates seamlessly with Viper for configuration management.

```go
package cmd

import (
	"fmt"
	"os"
	"github.com/spf13/cobra"
	"github.com/spf13/viper"
)

var cfgFile string

var rootCmd = &cobra.Command{
	Use:   "myapp",
	Short: "My application",
}

func Execute() error {
	return rootCmd.Execute()
}

func init() {
	cobra.OnInitialize(initConfig)

	rootCmd.PersistentFlags().StringVar(&cfgFile, "config", "", "config file (default is $HOME/.myapp.yaml)")
	rootCmd.PersistentFlags().String("author", "", "Author name")
	rootCmd.PersistentFlags().Bool("debug", false, "Enable debug mode")

	// Bind flags to viper
	viper.BindPFlag("author", rootCmd.PersistentFlags().Lookup("author"))
	viper.BindPFlag("debug", rootCmd.PersistentFlags().Lookup("debug"))

	// Set defaults
	viper.SetDefault("author", "John Doe")
	viper.SetDefault("debug", false)
}

func initConfig() {
	if cfgFile != "" {
		viper.SetConfigFile(cfgFile)
	} else {
		home, err := os.UserHomeDir()
		cobra.CheckErr(err)

		viper.AddConfigPath(home)
		viper.AddConfigPath(".")
		viper.SetConfigType("yaml")
		viper.SetConfigName(".myapp")
	}

	viper.AutomaticEnv()

	if err := viper.ReadInConfig(); err == nil {
		fmt.Fprintln(os.Stderr, "Using config file:", viper.ConfigFileUsed())
	}
}
```

**Priority Order (highest to lowest):**
1. Command-line flags
2. Environment variables
3. Config file
4. Default values

## Best Practices

### 1. Organize Commands in Separate Files

```
cmd/
├── root.go          # Root command and initialization
├── serve.go         # Serve command
├── db.go            # Database commands
└── db_migrate.go    # Database migration subcommand
```

### 2. Use Command Groups

```go
func init() {
	// Database commands group
	dbCmd := &cobra.Command{
		Use:   "db",
		Short: "Database operations",
	}
	dbCmd.AddCommand(dbMigrateCmd)
	dbCmd.AddCommand(dbSeedCmd)

	rootCmd.AddCommand(dbCmd)
}
```

### 3. Provide Help and Examples

```go
var myCmd = &cobra.Command{
	Use:   "deploy [app]",
	Short: "Deploy an application",
	Long: `Deploy deploys the specified application to the cluster.

It will build, push, and deploy your application with the
configured settings.`,
	Example: `  # Deploy an application
  myapp deploy webapp

  # Deploy with custom port
  myapp deploy webapp --port 8080

  # Deploy in debug mode
  myapp deploy webapp --debug`,
	Run: func(cmd *cobra.Command, args []string) {
		// ...
	},
}
```

### 4. Handle Errors Gracefully

```go
var myCmd = &cobra.Command{
	Use:  "process",
	RunE: func(cmd *cobra.Command, args []string) error {
		if err := validate(); err != nil {
			return fmt.Errorf("validation failed: %w", err)
		}

		if err := process(); err != nil {
			return fmt.Errorf("processing failed: %w", err)
		}

		return nil
	},
}
```

### 5. Use Context for Cancellation

```go
var serverCmd = &cobra.Command{
	Use:   "serve",
	Short: "Start server",
	RunE: func(cmd *cobra.Command, args []string) error {
		ctx := cmd.Context()

		server := &http.Server{
			Addr: ":8080",
		}

		// Handle graceful shutdown
		go func() {
			<-ctx.Done()
			server.Shutdown(context.Background())
		}()

		return server.ListenAndServe()
	},
}
```

### 6. Version Information

```go
var (
	version = "dev"
	commit  = "none"
	date    = "unknown"
)

var versionCmd = &cobra.Command{
	Use:   "version",
	Short: "Print version information",
	Run: func(cmd *cobra.Command, args []string) {
		fmt.Printf("Version: %s\n", version)
		fmt.Printf("Commit: %s\n", commit)
		fmt.Printf("Built: %s\n", date)
	},
}
```

### 7. Disable Flag Sorting

```go
func init() {
	// Keep flags in order they were defined
	rootCmd.Flags().SortFlags = false
}
```

### 8. Hidden Commands (for internal use)

```go
var debugCmd = &cobra.Command{
	Use:    "debug",
	Short:  "Debug commands (internal use)",
	Hidden: true,
	Run: func(cmd *cobra.Command, args []string) {
		// Debug logic
	},
}
```

## Examples

### Complete CLI Application

```go
package main

import (
	"fmt"
	"os"
	"time"

	"github.com/spf13/cobra"
	"github.com/spf13/viper"
)

var (
	cfgFile string
	verbose bool
)

// Root command
var rootCmd = &cobra.Command{
	Use:   "myapp",
	Short: "A modern CLI application",
	Long:  `MyApp is a powerful CLI tool built with Cobra`,
}

// Serve command
var serveCmd = &cobra.Command{
	Use:   "serve",
	Short: "Start the HTTP server",
	Long:  `Start the HTTP server on the specified port`,
	RunE: func(cmd *cobra.Command, args []string) error {
		port, _ := cmd.Flags().GetString("port")
		fmt.Printf("Starting server on port %s...\n", port)
		// Server logic here
		return nil
	},
}

// Database command group
var dbCmd = &cobra.Command{
	Use:   "db",
	Short: "Database operations",
}

var dbMigrateCmd = &cobra.Command{
	Use:   "migrate",
	Short: "Run database migrations",
	RunE: func(cmd *cobra.Command, args []string) error {
		fmt.Println("Running migrations...")
		// Migration logic here
		return nil
	},
}

// Version command
var versionCmd = &cobra.Command{
	Use:   "version",
	Short: "Print version information",
	Run: func(cmd *cobra.Command, args []string) {
		fmt.Println("myapp version 1.0.0")
	},
}

func init() {
	cobra.OnInitialize(initConfig)

	// Persistent flags
	rootCmd.PersistentFlags().StringVar(&cfgFile, "config", "", "config file (default is $HOME/.myapp.yaml)")
	rootCmd.PersistentFlags().BoolVarP(&verbose, "verbose", "v", false, "verbose output")

	// Serve command flags
	serveCmd.Flags().StringP("port", "p", "8080", "Port to listen on")
	serveCmd.Flags().Int("timeout", 30, "Request timeout in seconds")

	// Build command tree
	rootCmd.AddCommand(serveCmd)
	rootCmd.AddCommand(dbCmd)
	rootCmd.AddCommand(versionCmd)

	dbCmd.AddCommand(dbMigrateCmd)
}

func initConfig() {
	if cfgFile != "" {
		viper.SetConfigFile(cfgFile)
	} else {
		home, err := os.UserHomeDir()
		cobra.CheckErr(err)

		viper.AddConfigPath(home)
		viper.SetConfigType("yaml")
		viper.SetConfigName(".myapp")
	}

	viper.AutomaticEnv()

	if err := viper.ReadInConfig(); err == nil && verbose {
		fmt.Fprintln(os.Stderr, "Using config file:", viper.ConfigFileUsed())
	}
}

func main() {
	if err := rootCmd.Execute(); err != nil {
		fmt.Fprintln(os.Stderr, err)
		os.Exit(1)
	}
}
```

### Git-style CLI

```go
// git clone <url>
var cloneCmd = &cobra.Command{
	Use:   "clone [url]",
	Short: "Clone a repository",
	Args:  cobra.ExactArgs(1),
	RunE: func(cmd *cobra.Command, args []string) error {
		url := args[0]
		depth, _ := cmd.Flags().GetInt("depth")
		branch, _ := cmd.Flags().GetString("branch")

		fmt.Printf("Cloning %s (depth: %d, branch: %s)\n", url, depth, branch)
		return nil
	},
}

func init() {
	cloneCmd.Flags().IntP("depth", "d", 0, "Clone depth")
	cloneCmd.Flags().StringP("branch", "b", "main", "Branch to clone")
	rootCmd.AddCommand(cloneCmd)
}
```

### kubectl-style Plugin

```go
// For kubectl plugin: kubectl-myplugin
var rootCmd = &cobra.Command{
	Use: "kubectl-myplugin",
	Annotations: map[string]string{
		cobra.CommandDisplayNameAnnotation: "kubectl myplugin",
	},
	Short: "My kubectl plugin",
}

var subCmd = &cobra.Command{
	Use:   "list",
	Short: "List resources",
	Run: func(cmd *cobra.Command, args []string) {
		fmt.Println("Listing resources...")
	},
}

func init() {
	rootCmd.AddCommand(subCmd)
}
```

## Common Patterns

### Interactive Prompts (with survey)

```go
import "github.com/AlecAivazis/survey/v2"

var deployCmd = &cobra.Command{
	Use:   "deploy",
	Short: "Deploy application",
	RunE: func(cmd *cobra.Command, args []string) error {
		var environment string
		prompt := &survey.Select{
			Message: "Select environment:",
			Options: []string{"development", "staging", "production"},
		}
		survey.AskOne(prompt, &environment)

		fmt.Printf("Deploying to %s...\n", environment)
		return nil
	},
}
```

### Progress Bars (with progressbar)

```go
import "github.com/schollz/progressbar/v3"

var downloadCmd = &cobra.Command{
	Use:   "download [url]",
	Short: "Download a file",
	Args:  cobra.ExactArgs(1),
	RunE: func(cmd *cobra.Command, args []string) error {
		bar := progressbar.Default(100)
		for i := 0; i < 100; i++ {
			bar.Add(1)
			time.Sleep(50 * time.Millisecond)
		}
		return nil
	},
}
```

### Colored Output (with fatih/color)

```go
import "github.com/fatih/color"

var statusCmd = &cobra.Command{
	Use:   "status",
	Short: "Check status",
	Run: func(cmd *cobra.Command, args []string) {
		color.Green("✓ Service is running")
		color.Yellow("⚠ Warning: High memory usage")
		color.Red("✗ Database connection failed")
	},
}
```

## Troubleshooting

### Common Issues

**1. Flags Not Recognized**
- Ensure flags are defined in `init()` before `Execute()` is called
- Check flag names for typos
- Verify you're using the correct command reference

**2. Subcommands Not Working**
- Make sure `AddCommand()` is called in `init()`
- Check command `Use` field matches expected invocation

**3. Persistent Flags Not Available**
- Persistent flags must be defined on parent commands
- Use `PersistentFlags()` instead of `Flags()`

**4. Completion Not Working**
- Generate and source completion script
- Check shell-specific instructions
- Ensure `ValidArgsFunction` or `ValidArgs` is defined

## Resources

- **Official Documentation**: https://github.com/spf13/cobra
- **User Guide**: https://github.com/spf13/cobra/blob/main/site/content/user_guide.md
- **Cobra Generator**: https://github.com/spf13/cobra-cli
- **Viper (Configuration)**: https://github.com/spf13/viper
- **Examples**: https://github.com/spf13/cobra/tree/main/doc

## Related Libraries

- **Viper**: Configuration management
- **pflag**: POSIX/GNU-style flags (used internally by Cobra)
- **survey**: Interactive prompts
- **color**: Terminal colors
- **progressbar**: Progress indicators
- **tablewriter**: ASCII table output

---

*This documentation covers Cobra v1.9+. For the latest updates, refer to the official repository.*
