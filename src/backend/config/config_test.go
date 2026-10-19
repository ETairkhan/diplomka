package config

import "testing"

func TestLoadDefaultPort(t *testing.T) {
	t.Setenv("APP_PORT", "")
	cfg := Load()
	if cfg.Port != "8080" {
		t.Errorf("expected port 8080, got %s", cfg.Port)
	}
}

func TestLoadFromEnv(t *testing.T) {
	t.Setenv("APP_PORT", "9000")
	cfg := Load()
	if cfg.Port != "9000" {
		t.Errorf("expected port 9000, got %s", cfg.Port)
	}
}
