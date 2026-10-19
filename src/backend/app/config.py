import os


class Settings:
    def __init__(self):
        self.env = os.getenv("APP_ENV", "development")
        self.secret_key = os.getenv("SECRET_KEY", "")
        self.cors_origins = os.getenv("CORS_ORIGINS", "http://localhost:5173").split(",")
        self.speech_url = os.getenv("SPEECH_SERVICE_URL", "http://localhost:8001")
        self.llm_url = os.getenv("LLM_SERVICE_URL", "http://localhost:8002")


settings = Settings()
