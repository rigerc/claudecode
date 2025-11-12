package main

import (
    "context"
    "fmt"
    "log"
    "os"

    "github.com/urfave/cli/v3"
)

func main() {
    cmd := &cli.Command{
        Name:        "{{.AppName}}",
        Description: "{{.Description}}",
        Usage:       "{{.Usage}}",
        {{if .Version}}
        Version:     "{{.Version}}",
        {{end}}
        {{if .Author}}
        Authors: []any{
            &cli.Author{
                Name:  "{{.Author}}",
                Email: "{{.Email}}",
            },
        },
        {{end}}
        Action: func(ctx context.Context, cmd *cli.Command) error {
            fmt.Println("Hello from {{.AppName}}!")
            return nil
        },
    }

    if err := cmd.Run(context.Background(), os.Args); err != nil {
        log.Fatal(err)
    }
}