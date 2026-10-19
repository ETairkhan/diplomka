package backendtests

import (
	"net/http"
	"net/http/httptest"
	"strings"
	"testing"

	"knowledge-control/backend/handlers"
)

func TestHealth(t *testing.T) {
	req := httptest.NewRequest(http.MethodGet, "/health", nil)
	rec := httptest.NewRecorder()

	handlers.Health(rec, req)

	if rec.Code != http.StatusOK {
		t.Errorf("expected status 200, got %d", rec.Code)
	}
	if !strings.Contains(rec.Body.String(), "ok") {
		t.Errorf("unexpected body: %s", rec.Body.String())
	}
}

func TestCORSPreflight(t *testing.T) {
	handler := handlers.CORS("http://localhost:5173", http.HandlerFunc(handlers.Health))
	req := httptest.NewRequest(http.MethodOptions, "/health", nil)
	rec := httptest.NewRecorder()

	handler.ServeHTTP(rec, req)

	if rec.Code != http.StatusNoContent {
		t.Errorf("expected status 204, got %d", rec.Code)
	}
}
