from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.auth import require_auth
from app.db.session import get_db
from app.schemas.player import PlayerActiveUpdate, PlayerCreate, PlayerRead, PlayerUpdate
from app.services.players import (
    DuplicatePlayerNameError,
    PlayerNotFoundError,
    create_player,
    get_player,
    list_players,
    set_player_active,
    update_player,
)

router = APIRouter(prefix="/players", tags=["players"], dependencies=[Depends(require_auth)])


@router.get("", response_model=list[PlayerRead])
def index(active_only: bool = False, db: Session = Depends(get_db)) -> list[PlayerRead]:
    return list_players(db, active_only=active_only)


@router.post("", response_model=PlayerRead, status_code=status.HTTP_201_CREATED)
def create(data: PlayerCreate, db: Session = Depends(get_db)) -> PlayerRead:
    try:
        return create_player(db, data)
    except DuplicatePlayerNameError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc)) from exc


@router.get("/{player_id}", response_model=PlayerRead)
def show(player_id: int, db: Session = Depends(get_db)) -> PlayerRead:
    try:
        return get_player(db, player_id)
    except PlayerNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


@router.put("/{player_id}", response_model=PlayerRead)
def update(player_id: int, data: PlayerUpdate, db: Session = Depends(get_db)) -> PlayerRead:
    try:
        return update_player(db, player_id, data)
    except PlayerNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    except DuplicatePlayerNameError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc)) from exc


@router.patch("/{player_id}/active", response_model=PlayerRead)
def change_active(
    player_id: int,
    data: PlayerActiveUpdate,
    db: Session = Depends(get_db),
) -> PlayerRead:
    try:
        return set_player_active(db, player_id, data.active)
    except PlayerNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc

