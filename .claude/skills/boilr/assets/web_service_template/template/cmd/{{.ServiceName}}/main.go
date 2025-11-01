package main

import (
	"context"
	"fmt"
	"log"
	"net/http"
	"os"
	"os/signal"
	"syscall"
	"time"

	"{{.ModuleName}}/internal/server"
)

func main() {
	// Configuration
	port := {{.Port}}
	if envPort := os.Getenv("PORT"); envPort != "" {
		if p, err := strconv.Atoi(envPort); err == nil {
			port = p
		}
	}

	enableTLS := {{.EnableTLS}} == "true"
	if envTLS := os.Getenv("ENABLE_TLS"); envTLS != "" {
		enableTLS = envTLS == "true"
	}

	// Create server
	srv := server.New(port, enableTLS)

	// Start server in a goroutine
	go func() {
		log.Printf("Starting {{.ServiceName}} on port %d", port)
		var err error
		if enableTLS {
			err = srv.ListenAndServeTLS("server.crt", "server.key")
		} else {
			err = srv.ListenAndServe()
		}
		if err != nil && err != http.ErrServerClosed {
			log.Fatalf("Server failed to start: %v", err)
		}
	}()

	// Wait for interrupt signal to gracefully shutdown the server
	quit := make(chan os.Signal, 1)
	signal.Notify(quit, syscall.SIGINT, syscall.SIGTERM)
	<-quit

	log.Println("Shutting down server...")
	ctx, cancel := context.WithTimeout(context.Background(), 30*time.Second)
	defer cancel()

	if err := srv.Shutdown(ctx); err != nil {
		log.Fatalf("Server forced to shutdown: %v", err)
	}

	log.Println("Server exited")
}