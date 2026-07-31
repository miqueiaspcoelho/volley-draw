from dataclasses import dataclass
from functools import lru_cache
import os


@dataclass(frozen=True)
class Settings:
    app_name: str = "Volley Draw"
    debug: bool = False


@lru_cache
def get_settings() -> Settings:
    return Settings(
        app_name=os.getenv("VOLLEY_DRAW_APP_NAME", "Volley Draw"),
        debug=os.getenv("VOLLEY_DRAW_DEBUG", "false").lower() == "true",
    )
