package server

import (
	"encoding/json"
	"fmt"
	"net/http"
	"strconv"
	"time"

	"github.com/gorilla/mux"
)

type Server struct {
	router *mux.Router
	port   int
	tls    bool
}

type HealthResponse struct {
	Status    string    `json:"status"`
	Service   string    `json:"service"`
	Timestamp time.Time `json:"timestamp"`
	Port      int       `json:"port"`
}

type InfoResponse struct {
	Service     string   `json:"service"`
	Description string   `json:"description"`
	Version     string   `json:"version"`
	Endpoints   []string `json:"endpoints"`
	Port        int      `json:"port"`
}

func New(port int, enableTLS bool) *Server {
	s := &Server{
		router: mux.NewRouter(),
		port:   port,
		tls:    enableTLS,
	}

	s.setupRoutes()
	return s
}

func (s *Server) setupRoutes() {
	s.router.HandleFunc("/", s.handleHome).Methods("GET")
	s.router.HandleFunc("/health", s.handleHealth).Methods("GET")
	s.router.HandleFunc("/api/v1/info", s.handleInfo).Methods("GET")
}

func (s *Server) handleHome(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "text/plain")
	fmt.Fprintf(w, "Welcome to {{.ServiceName}}!\n")
	fmt.Fprintf(w, "{{.Description}}\n")
}

func (s *Server) handleHealth(w http.ResponseWriter, r *http.Request) {
	response := HealthResponse{
		Status:    "ok",
		Service:   "{{.ServiceName}}",
		Timestamp: time.Now().UTC(),
		Port:      s.port,
	}

	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(response)
}

func (s *Server) handleInfo(w http.ResponseWriter, r *http.Request) {
	response := InfoResponse{
		Service:     "{{.ServiceName}}",
		Description: "{{.Description}}",
		Version:     "1.0.0",
		Endpoints: []string{
			"/",
			"/health",
			"/api/v1/info",
		},
		Port: s.port,
	}

	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(response)
}

func (s *Server) ListenAndServe() error {
	return http.ListenAndServe(fmt.Sprintf(":%d", s.port), s.router)
}

func (s *Server) ListenAndServeTLS(certFile, keyFile string) error {
	return http.ListenAndServeTLS(fmt.Sprintf(":%d", s.port), certFile, keyFile, s.router)
}

func (s *Server) Shutdown(ctx context.Context) error {
	// Note: In a real implementation, you'd store the http.Server instance
	// to properly shutdown. This is a simplified example.
	return nil
}