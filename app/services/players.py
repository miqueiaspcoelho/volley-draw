from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Player
from app.schemas.player import PlayerCreate, PlayerUpdate


class PlayerNotFoundError(ValueError):
    pass


class DuplicatePlayerNameError(ValueError):
    pass


def list_players(db: Session, active_only: bool = False) -> list[Player]:
    statement = select(Player).order_by(Player.name)
    if active_only:
        statement = statement.where(Player.active.is_(True))
    return list(db.scalars(statement))


def get_player(db: Session, player_id: int) -> Player:
    player = db.get(Player, player_id)
    if player is None:
        raise PlayerNotFoundError("player not found")
    return player


def create_player(db: Session, data: PlayerCreate) -> Player:
    _ensure_unique_name(db, data.name)
    player = Player(**data.model_dump())
    db.add(player)
    db.commit()
    db.refresh(player)
    return player


def update_player(db: Session, player_id: int, data: PlayerUpdate) -> Player:
    player = get_player(db, player_id)
    values = data.model_dump(exclude_unset=True)
    new_name = values.get("name")
    if new_name is not None and new_name != player.name:
        _ensure_unique_name(db, new_name, ignore_player_id=player.id)
    for field, value in values.items():
        setattr(player, field, value)
    db.commit()
    db.refresh(player)
    return player


def set_player_active(db: Session, player_id: int, active: bool) -> Player:
    player = get_player(db, player_id)
    player.active = active
    db.commit()
    db.refresh(player)
    return player


def calculate_overall(
    serving: Decimal,
    passing: Decimal,
    setting: Decimal,
    attacking: Decimal,
    blocking: Decimal,
) -> Decimal:
    return (serving + passing + setting + attacking + blocking) / Decimal("5")


def _ensure_unique_name(
    db: Session,
    name: str,
    ignore_player_id: int | None = None,
) -> None:
    statement = select(Player).where(Player.name == name)
    if ignore_player_id is not None:
        statement = statement.where(Player.id != ignore_player_id)
    if db.scalar(statement) is not None:
        raise DuplicatePlayerNameError("player name already exists")
