from fastapi import Depends, FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.auth import require_auth
from app.core.config import get_settings
from app.routers.auth_pages import router as auth_pages_router
from app.routers.draws import router as draws_router
from app.routers.history_pages import router as history_pages_router
from app.routers.match_pages import router as match_pages_router
from app.routers.player_pages import router as player_pages_router
from app.routers.players import router as players_router

templates = Jinja2Templates(directory="app/templates")


def create_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(title=settings.app_name, debug=settings.debug)
    app.include_router(auth_pages_router)
    app.include_router(players_router)
    app.include_router(draws_router)
    app.include_router(history_pages_router)
    app.include_router(match_pages_router)
    app.include_router(player_pages_router)

    @app.get("/health", tags=["health"])
    def healthcheck() -> dict[str, str]:
        return {"status": "ok"}

    @app.get("/", response_class=HTMLResponse, dependencies=[Depends(require_auth)])
    def home(request: Request) -> HTMLResponse:
        return templates.TemplateResponse(
            request,
            "home.html",
            {"app_name": settings.app_name},
        )

    return app


app = create_app()



