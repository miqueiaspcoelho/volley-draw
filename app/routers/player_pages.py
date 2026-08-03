from decimal import Decimal, InvalidOperation
from urllib.parse import parse_qs

from fastapi import APIRouter, Depends, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from pydantic import ValidationError
from sqlalchemy.orm import Session

from app.auth import require_auth
from app.db.session import get_db
from app.schemas.player import PlayerCreate, PlayerUpdate
from app.services.players import (
    DuplicatePlayerNameError,
    PlayerNotFoundError,
    create_player,
    get_player,
    list_players,
    set_player_active,
    update_player,
)

templates = Jinja2Templates(directory="app/templates")
router = APIRouter(prefix="/jogadores", tags=["player-pages"], dependencies=[Depends(require_auth)])

SKILL_FIELDS = ("serving", "passing", "setting", "attacking", "blocking")


@router.get("", response_class=HTMLResponse)
def players_page(request: Request, db: Session = Depends(get_db)) -> HTMLResponse:
    return _render_page(request, db)


@router.post("", response_class=HTMLResponse)
async def create_player_page(request: Request, db: Session = Depends(get_db)) -> HTMLResponse:
    values = await _form_values(request)
    try:
        data = PlayerCreate(**values)
        create_player(db, data)
    except (ValidationError, DuplicatePlayerNameError, ValueError) as exc:
        return _render_page(request, db, values=values, error=_error_message(exc), status_code=400)
    return _redirect_players()


@router.get("/{player_id}/editar", response_class=HTMLResponse)
def edit_player_page(player_id: int, request: Request, db: Session = Depends(get_db)) -> HTMLResponse:
    try:
        player = get_player(db, player_id)
    except PlayerNotFoundError:
        return _render_page(request, db, error="Jogador nao encontrado.", status_code=404)
    return _render_page(request, db, editing=player)


@router.post("/{player_id}", response_class=HTMLResponse)
async def update_player_page(player_id: int, request: Request, db: Session = Depends(get_db)) -> HTMLResponse:
    values = await _form_values(request)
    try:
        data = PlayerUpdate(**values)
        update_player(db, player_id, data)
    except PlayerNotFoundError:
        return _render_page(request, db, values=values, error="Jogador nao encontrado.", status_code=404)
    except (ValidationError, DuplicatePlayerNameError, ValueError) as exc:
        editing = None
        try:
            editing = get_player(db, player_id)
        except PlayerNotFoundError:
            pass
        return _render_page(request, db, editing=editing, values=values, error=_error_message(exc), status_code=400)
    return _redirect_players()


@router.post("/{player_id}/ativo", response_class=HTMLResponse)
async def toggle_player_active_page(player_id: int, request: Request, db: Session = Depends(get_db)) -> HTMLResponse:
    form = await _urlencoded_form(request)
    active = form.get("active") == "true"
    try:
        set_player_active(db, player_id, active)
    except PlayerNotFoundError:
        return _render_page(request, db, error="Jogador nao encontrado.", status_code=404)
    return _redirect_players()


def _render_page(
    request: Request,
    db: Session,
    values: dict | None = None,
    editing: object | None = None,
    error: str | None = None,
    status_code: int = 200,
) -> HTMLResponse:
    return templates.TemplateResponse(
        request,
        "players/index.html",
        {
            "app_name": "Volley Draw",
            "players": list_players(db),
            "values": values or {},
            "editing": editing,
            "error": error,
        },
        status_code=status_code,
    )


def _redirect_players() -> RedirectResponse:
    return RedirectResponse("/jogadores", status_code=status.HTTP_303_SEE_OTHER)


async def _form_values(request: Request) -> dict:
    form = await _urlencoded_form(request)
    values = {
        "name": form.get("name"),
        "nickname": form.get("nickname"),
        "active": form.get("active") == "true",
    }
    for field in SKILL_FIELDS:
        values[field] = _decimal_or_raw(form.get(field))
    return values


async def _urlencoded_form(request: Request) -> dict[str, str]:
    body = (await request.body()).decode("utf-8")
    parsed = parse_qs(body, keep_blank_values=True)
    return {key: values[-1] for key, values in parsed.items()}


def _decimal_or_raw(value: object) -> Decimal | object:
    try:
        return Decimal(str(value))
    except (InvalidOperation, TypeError):
        return value


def _error_message(exc: Exception) -> str:
    if isinstance(exc, DuplicatePlayerNameError):
        return "Ja existe jogador com esse nome."
    return "Confira os campos informados. Notas devem ir de 0 a 5 com uma casa decimal."

