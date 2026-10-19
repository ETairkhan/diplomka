package config

import "os"

type Config struct {
	Env        string
	Port       string
	JWTSecret  string
	CorsOrigin string
	SpeechURL  string
	LlmURL     string
}

// Load reads settings from environment variables (see .env.example).
func Load() Config {
	return Config{
		Env:        get("APP_ENV", "development"),
		Port:       get("APP_PORT", "8080"),
		JWTSecret:  get("JWT_SECRET", ""),
		CorsOrigin: get("CORS_ORIGINS", "http://localhost:5173"),
		SpeechURL:  get("SPEECH_SERVICE_URL", "http://localhost:8001"),
		LlmURL:     get("LLM_SERVICE_URL", "http://localhost:8002"),
	}
}

func get(key, def string) string {
	value := os.Getenv(key)
	if value == "" {
		return def
	}
	return value
}
