from dataclasses import dataclass
from functools import lru_cache
import os


@dataclass(frozen=True)
class Settings:
    app_name: str = "Volley Draw"
    debug: bool = False
    database_url: str = "postgresql+psycopg://postgres:postgres@localhost:5432/volley_draw"
    draw_api_base_url: str = "https://apiteams-q4s3.onrender.com"
    draw_api_timeout: float = 20.0
    draw_api_verify_tls: bool = True
    session_secret: str = "dev-session-secret-change-me"
    session_cookie_secure: bool = False


@lru_cache
def get_settings() -> Settings:
    return Settings(
        app_name=os.getenv("VOLLEY_DRAW_APP_NAME", "Volley Draw"),
        debug=os.getenv("VOLLEY_DRAW_DEBUG", "false").lower() == "true",
        database_url=os.getenv(
            "DATABASE_URL",
            "postgresql+psycopg://postgres:postgres@localhost:5432/volley_draw",
        ),
        draw_api_base_url=os.getenv(
            "VOLLEY_DRAW_API_BASE_URL",
            "https://apiteams-q4s3.onrender.com",
        ).rstrip("/"),
        draw_api_timeout=float(os.getenv("VOLLEY_DRAW_API_TIMEOUT", "20")),
        draw_api_verify_tls=os.getenv("VOLLEY_DRAW_API_VERIFY_TLS", "true").lower() == "true",
        session_secret=os.getenv("VOLLEY_DRAW_SESSION_SECRET", "dev-session-secret-change-me"),
        session_cookie_secure=os.getenv("VOLLEY_DRAW_SESSION_COOKIE_SECURE", "false").lower() == "true",
    )
