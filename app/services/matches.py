from datetime import datetime

from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.models import Attendance, Match, Player


class MatchNotFoundError(ValueError):
    pass


class PlayerUnavailableError(ValueError):
    pass


def list_matches(db: Session) -> list[Match]:
    statement = select(Match).order_by(Match.scheduled_at.desc())
    return list(db.scalars(statement))


def get_match(db: Session, match_id: int) -> Match:
    statement = (
        select(Match)
        .options(selectinload(Match.attendances))
        .where(Match.id == match_id)
    )
    match = db.scalar(statement)
    if match is None:
        raise MatchNotFoundError("match not found")
    return match


def create_match(db: Session, scheduled_at: datetime, notes: str | None = None) -> Match:
    match = Match(scheduled_at=scheduled_at, notes=notes or None, status="draft")
    db.add(match)
    db.commit()
    db.refresh(match)
    return match


def list_active_players(db: Session) -> list[Player]:
    statement = select(Player).where(Player.active.is_(True)).order_by(Player.name)
    return list(db.scalars(statement))


def set_attendance(db: Session, match_id: int, player_id: int, present: bool) -> Match:
    match = get_match(db, match_id)
    attendance = db.scalar(
        select(Attendance).where(
            Attendance.match_id == match_id,
            Attendance.player_id == player_id,
        )
    )

    if not present:
        if attendance is not None:
            db.delete(attendance)
            db.commit()
        return get_match(db, match.id)

    if attendance is None:
        player = db.get(Player, player_id)
        if player is None or not player.active:
            raise PlayerUnavailableError("player unavailable")
        db.add(
            Attendance(
                match_id=match_id,
                player_id=player_id,
                serving_snapshot=player.serving,
                passing_snapshot=player.passing,
                setting_snapshot=player.setting,
                attacking_snapshot=player.attacking,
                blocking_snapshot=player.blocking,
            )
        )
        db.commit()
    return get_match(db, match.id)


def present_player_ids(match: Match) -> set[int]:
    return {attendance.player_id for attendance in match.attendances}
