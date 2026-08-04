from datetime import datetime
from urllib.parse import parse_qs

from fastapi import APIRouter, Depends, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.auth import require_auth
from app.db.session import get_db
from app.schemas.draw import DrawRequest
from app.services.draw_api import DrawApiError, DrawApiRejectedError
from app.services.draws import DrawPayloadError, draw_match_teams, latest_draw_for_match
from app.services.sharing import format_whatsapp_draw
from app.services.matches import (
    MatchNotFoundError,
    PlayerUnavailableError,
    create_match,
    get_match,
    list_active_players,
    list_matches,
    present_player_ids,
    set_attendance,
)

templates = Jinja2Templates(directory="app/templates")
router = APIRouter(prefix="/partidas", tags=["match-pages"], dependencies=[Depends(require_auth)])


@router.get("", response_class=HTMLResponse)
def matches_page(request: Request, db: Session = Depends(get_db)) -> HTMLResponse:
    return _render_index(request, db)


@router.post("", response_class=HTMLResponse)
async def create_match_page(request: Request, db: Session = Depends(get_db)) -> HTMLResponse:
    form = _last_form_values(await _urlencoded_form(request))
    try:
        scheduled_at = datetime.fromisoformat(form.get("scheduled_at", ""))
        match = create_match(db, scheduled_at=scheduled_at, notes=form.get("notes") or None)
    except ValueError:
        return _render_index(request, db, error="Informe data e hora validas.", status_code=400)
    return RedirectResponse(f"/partidas/{match.id}", status_code=status.HTTP_303_SEE_OTHER)


@router.get("/{match_id}", response_class=HTMLResponse)
def match_detail_page(match_id: int, request: Request, db: Session = Depends(get_db)) -> HTMLResponse:
    return _render_detail(match_id, request, db)


@router.post("/{match_id}/presencas", response_class=HTMLResponse)
async def attendance_page(match_id: int, request: Request, db: Session = Depends(get_db)) -> HTMLResponse:
    form = _last_form_values(await _urlencoded_form(request))
    try:
        set_attendance(
            db,
            match_id=match_id,
            player_id=int(form.get("player_id", "0")),
            present=form.get("present") == "true",
        )
    except (MatchNotFoundError, PlayerUnavailableError, ValueError):
        return _render_detail(match_id, request, db, error="Nao foi possivel atualizar presenca.", status_code=400)
    return RedirectResponse(f"/partidas/{match_id}", status_code=status.HTTP_303_SEE_OTHER)



@router.post("/{match_id}/sortear", response_class=HTMLResponse)
async def draw_match_page(match_id: int, request: Request, db: Session = Depends(get_db)) -> HTMLResponse:
    form_values = await _urlencoded_form(request)
    form = _last_form_values(form_values)
    try:
        force_together, force_apart = _advanced_groups(form_values)
        draw_match_teams(
            db,
            match_id=match_id,
            request=DrawRequest(
                players_per_team=_form_int(form.get("players_per_team"), 6),
                range=_form_int(form.get("range"), 2),
                force_together=force_together,
                force_apart=force_apart,
            ),
        )
    except MatchNotFoundError:
        return _render_index(request, db, error="Partida nao encontrada.", status_code=404)
    except DrawPayloadError as exc:
        message = "Marque pelo menos um jogador presente." if str(exc) == "match has no present players" else str(exc)
        return _render_detail(match_id, request, db, error=message, status_code=200)
    except DrawApiRejectedError as exc:
        return _render_detail(match_id, request, db, error=str(exc), status_code=200)
    except DrawApiError:
        return _render_detail(match_id, request, db, error="Nao foi possivel chamar a API externa de sorteio.", status_code=502)
    except ValueError:
        return _render_detail(match_id, request, db, error="Parametros de sorteio invalidos.", status_code=200)
    return RedirectResponse(f"/partidas/{match_id}", status_code=status.HTTP_303_SEE_OTHER)

def _render_index(
    request: Request,
    db: Session,
    error: str | None = None,
    status_code: int = 200,
) -> HTMLResponse:
    return templates.TemplateResponse(
        request,
        "matches/index.html",
        {"app_name": "Volley Draw", "matches": list_matches(db), "error": error},
        status_code=status_code,
    )


def _render_detail(
    match_id: int,
    request: Request,
    db: Session,
    error: str | None = None,
    status_code: int = 200,
) -> HTMLResponse:
    try:
        match = get_match(db, match_id)
    except MatchNotFoundError:
        return _render_index(request, db, error="Partida nao encontrada.", status_code=404)
    active_players = list_active_players(db)
    present_ids = present_player_ids(match)
    present_players = [player for player in active_players if player.id in present_ids]
    suggested_players_per_team = min(6, len(present_ids)) if present_ids else 6
    latest_draw = latest_draw_for_match(db, match_id)
    return templates.TemplateResponse(
        request,
        "matches/detail.html",
        {
            "app_name": "Volley Draw",
            "match": match,
            "active_players": active_players,
            "present_ids": present_ids,
            "present_players": present_players,
            "latest_draw": latest_draw,
            "share_text": format_whatsapp_draw(match, latest_draw) if latest_draw else None,
            "suggested_players_per_team": suggested_players_per_team,
            "suggested_team_count": _team_count(len(present_ids), suggested_players_per_team),
            "error": error,
        },
        status_code=status_code,
    )


async def _urlencoded_form(request: Request) -> dict[str, list[str]]:
    body = (await request.body()).decode("utf-8")
    return parse_qs(body, keep_blank_values=True)


def _last_form_values(form: dict[str, list[str]]) -> dict[str, str]:
    return {key: values[-1] for key, values in form.items()}

def _form_int(value: str | None, default: int) -> int:
    if value is None or value == "":
        return default
    parsed = float(value)
    if not parsed.is_integer():
        raise ValueError
    return int(parsed)


def _advanced_groups(form: dict[str, list[str]]) -> tuple[list[list[str]], list[list[str]]]:
    return (
        _groups_from_fields(form, "force_together_"),
        _groups_from_fields(form, "force_apart_"),
    )


def _groups_from_fields(form: dict[str, list[str]], prefix: str) -> list[list[str]]:
    groups: list[list[str]] = []
    for key in sorted(form):
        if not key.startswith(prefix):
            continue
        group = [value.strip() for value in form[key] if value.strip()]
        if len(group) >= 2:
            groups.append(group)
    return groups


def _team_count(player_count: int, players_per_team: int) -> int:
    if player_count <= 0:
        return 1
    return max(1, (player_count + players_per_team - 1) // players_per_team)




