from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.auth import require_auth
from app.db.session import get_db
from app.services.draws import latest_draw_for_match
from app.services.matches import MatchNotFoundError, get_match, list_matches
from app.services.sharing import format_whatsapp_draw


templates = Jinja2Templates(directory="app/templates")
router = APIRouter(prefix="/historico", tags=["history-pages"], dependencies=[Depends(require_auth)])


@router.get("", response_class=HTMLResponse)
def history_page(request: Request, db: Session = Depends(get_db)) -> HTMLResponse:
    matches = list_matches(db)
    latest_draws = {match.id: latest_draw_for_match(db, match.id) for match in matches}
    return templates.TemplateResponse(
        request,
        "history/index.html",
        {"app_name": "Volley Draw", "matches": matches, "latest_draws": latest_draws},
    )


@router.get("/{match_id}", response_class=HTMLResponse)
def history_detail_page(match_id: int, request: Request, db: Session = Depends(get_db)) -> HTMLResponse:
    try:
        match = get_match(db, match_id)
    except MatchNotFoundError:
        return templates.TemplateResponse(
            request,
            "history/index.html",
            {
                "app_name": "Volley Draw",
                "matches": list_matches(db),
                "latest_draws": {},
                "error": "Partida nao encontrada.",
            },
            status_code=404,
        )
    latest_draw = latest_draw_for_match(db, match_id)
    return templates.TemplateResponse(
        request,
        "history/detail.html",
        {
            "app_name": "Volley Draw",
            "match": match,
            "latest_draw": latest_draw,
            "share_text": format_whatsapp_draw(match, latest_draw) if latest_draw else None,
        },
    )

