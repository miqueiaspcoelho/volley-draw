from dataclasses import dataclass
from functools import lru_cache
import os


POSTGRESQL_PSYCOPG_SCHEME = "postgresql+psycopg://"
POSTGRESQL_DEFAULT_SCHEME = "postgresql://"
DEFAULT_DATABASE_URL = "postgresql+psycopg://postgres:postgres@localhost:5432/volley_draw"


def normalize_database_url(url: str) -> str:
    if url.startswith(POSTGRESQL_DEFAULT_SCHEME):
        return url.replace(POSTGRESQL_DEFAULT_SCHEME, POSTGRESQL_PSYCOPG_SCHEME, 1)
    return url


@dataclass(frozen=True)
class Settings:
    app_name: str = "Volley Draw"
    app_env: str = "local"
    debug: bool = False
    database_url: str = DEFAULT_DATABASE_URL
    draw_api_base_url: str = "https://apiteams-q4s3.onrender.com"
    draw_api_timeout: float = 20.0
    draw_api_verify_tls: bool = True
    session_secret: str = "dev-session-secret-change-me"
    session_cookie_secure: bool = False
    log_level: str = "INFO"


def _env(name: str, fallback: str) -> str:
    return os.getenv(name, fallback)


def _env_any(names: tuple[str, ...], fallback: str) -> str:
    for name in names:
        value = os.getenv(name)
        if value is not None:
            return value
    return fallback


def _env_bool(names: tuple[str, ...], fallback: bool) -> bool:
    default = "true" if fallback else "false"
    return _env_any(names, default).lower() == "true"


@lru_cache
def get_settings() -> Settings:
    return Settings(
        app_name=_env("VOLLEY_DRAW_APP_NAME", "Volley Draw"),
        app_env=_env("APP_ENV", "local"),
        debug=_env_bool(("DEBUG", "VOLLEY_DRAW_DEBUG"), False),
        database_url=normalize_database_url(os.getenv("DATABASE_URL", DEFAULT_DATABASE_URL)),
        draw_api_base_url=_env_any(("DRAW_API_URL", "VOLLEY_DRAW_API_BASE_URL"), "https://apiteams-q4s3.onrender.com").rstrip("/"),
        draw_api_timeout=float(_env_any(("DRAW_API_TIMEOUT", "VOLLEY_DRAW_API_TIMEOUT"), "20")),
        draw_api_verify_tls=os.getenv("VOLLEY_DRAW_API_VERIFY_TLS", "true").lower() == "true",
        session_secret=_env_any(("SECRET_KEY", "VOLLEY_DRAW_SESSION_SECRET"), "dev-session-secret-change-me"),
        session_cookie_secure=_env_bool(("SESSION_COOKIE_SECURE", "VOLLEY_DRAW_SESSION_COOKIE_SECURE"), False),
        log_level=_env("LOG_LEVEL", "INFO"),
    )
