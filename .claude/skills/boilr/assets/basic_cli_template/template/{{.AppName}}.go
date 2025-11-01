package main

import (
	"flag"
	"fmt"
	"log"
	"os"
)

var (
	versionFlag = flag.Bool("version", false, "Show version information")
	helpFlag    = flag.Bool("help", false, "Show help information")
)

const (
	appName    = "{{.AppName}}"
	appVersion = "{{.Version}}"
	appDesc    = "{{.Description}}"
	appAuthor  = "{{.Author}}"
)

func main() {
	flag.Parse()

	if *versionFlag {
		fmt.Printf("%s %s\n", appName, appVersion)
		fmt.Printf("%s\n", appDesc)
		if appAuthor != "" {
			fmt.Printf("Author: %s\n", appAuthor)
		}
		os.Exit(0)
	}

	if *helpFlag || len(os.Args) == 1 {
		printUsage()
		os.Exit(0)
	}

	if len(flag.Args()) < 1 {
		fmt.Println("Error: No command specified")
		fmt.Println("Use -help for usage information")
		os.Exit(1)
	}

	command := flag.Args()[0]
	switch command {
	case "hello":
		fmt.Printf("Hello from %s!\n", appName)
	case "version":
		fmt.Printf("%s %s\n", appName, appVersion)
	default:
		log.Printf("Unknown command: %s", command)
		os.Exit(1)
	}
}

func printUsage() {
	fmt.Printf("%s - %s\n", appName, appDesc)
	fmt.Println()
	fmt.Println("Usage:")
	fmt.Printf("  %s [options] <command>\n", os.Args[0])
	fmt.Println()
	fmt.Println("Options:")
	fmt.Println("  -version  Show version information")
	fmt.Println("  -help     Show this help message")
	fmt.Println()
	fmt.Println("Commands:")
	fmt.Println("  hello     Say hello")
	fmt.Println("  version   Show version")
}