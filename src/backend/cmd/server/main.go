package main

import (
	"log"
	"net/http"

	"knowledge-control/backend/config"
	"knowledge-control/backend/handlers"
)

func main() {
	cfg := config.Load()

	mux := http.NewServeMux()
	mux.HandleFunc("GET /health", handlers.Health)

	addr := ":" + cfg.Port
	log.Println("server started on", addr)
	log.Fatal(http.ListenAndServe(addr, handlers.CORS(cfg.CorsOrigin, mux)))
}
