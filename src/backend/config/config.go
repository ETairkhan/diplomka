package config

import "os"

type Config struct {
	Env        string
	Port       string
	JWTSecret  string
	CorsOrigin string
}

func Load() Config {
	return Config{
		Env:        get("APP_ENV", "development"),
		Port:       get("APP_PORT", "8080"),
		JWTSecret:  get("JWT_SECRET", ""),
		CorsOrigin: get("CORS_ORIGINS", "http://localhost:5173"),
	}
}

func get(key, def string) string {
	value := os.Getenv(key)
	if value == "" {
		return def
	}
	return value
}
