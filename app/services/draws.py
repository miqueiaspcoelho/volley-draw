from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Attendance, Draw, Player
from app.schemas.draw import DrawPayload, DrawPlayerPayload, DrawRequest
from app.services.draw_api import DrawApiClient
from app.services.matches import MatchNotFoundError, get_match


class DrawPayloadError(ValueError):
    pass


def build_draw_payload(db: Session, match_id: int, request: DrawRequest) -> DrawPayload:
    match = get_match(db, match_id)
    if not match.attendances:
        raise DrawPayloadError("match has no present players")

    players_by_id = {
        player.id: player
        for player in db.scalars(
            select(Player).where(Player.id.in_([item.player_id for item in match.attendances]))
        )
    }
    players = [_attendance_payload(attendance, players_by_id) for attendance in match.attendances]
    return DrawPayload(players=players, **request.model_dump())


def draw_match_teams(
    db: Session,
    match_id: int,
    request: DrawRequest,
    client: DrawApiClient | None = None,
) -> Draw:
    payload = build_draw_payload(db, match_id, request)
    response = (client or DrawApiClient()).draw_teams(payload)
    draw = Draw(
        match_id=match_id,
        request_params=request.model_dump(mode="json"),
        request_payload=payload.model_dump(mode="json"),
        response_payload=response,
        normalized_result=response.get("data", {}),
    )
    db.add(draw)
    db.commit()
    db.refresh(draw)
    return draw


def latest_draw_for_match(db: Session, match_id: int) -> Draw | None:
    return db.scalar(
        select(Draw)
        .where(Draw.match_id == match_id)
        .order_by(Draw.created_at.desc(), Draw.id.desc())
    )


def _attendance_payload(attendance: Attendance, players_by_id: dict[int, Player]) -> DrawPlayerPayload:
    player = players_by_id.get(attendance.player_id)
    if player is None:
        raise MatchNotFoundError("attendance player not found")
    return DrawPlayerPayload(
        name=player.name,
        serving=attendance.serving_snapshot,
        passing=attendance.passing_snapshot,
        setting=attendance.setting_snapshot,
        attacking=attendance.attacking_snapshot,
        blocking=attendance.blocking_snapshot,
    )
