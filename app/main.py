import logging

from fastapi import Depends, FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates

from app.auth import require_auth
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.routers.auth_pages import router as auth_pages_router
from app.routers.draws import router as draws_router
from app.routers.history_pages import router as history_pages_router
from app.routers.match_pages import router as match_pages_router
from app.routers.player_pages import router as player_pages_router
from app.routers.players import router as players_router
from app.db.session import get_db

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

    @app.get("/health", tags=["health"], include_in_schema=False, response_model=None)
    def healthcheck(db: Session = Depends(get_db)) -> dict[str, str] | JSONResponse:
        try:
            db.execute(text("SELECT 1"))
        except SQLAlchemyError:
            return JSONResponse({"status": "unavailable"}, status_code=503)
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



