from datetime import datetime

from app.models.draw import Draw
from app.models.match import Match
from app.services.sharing import format_whatsapp_draw


def test_format_whatsapp_draw_uses_team_list_pattern() -> None:
    match = Match(id=1, scheduled_at=datetime(2026, 8, 3, 20, 0), notes=None)
    draw = Draw(
        match_id=1,
        request_params={},
        request_payload={},
        response_payload={},
        normalized_result={
            "teams": [
                {"team_name": "Time 1", "players": [{"name": "David"}, {"name": "Daniel conv lucas l"}]},
                {"team_name": "Time 2", "players": [{"name": "Arthur conv cesar"}]},
            ],
            "leftovers": [],
        },
    )

    assert format_whatsapp_draw(match, draw) == "Time 1\n\n* David\n* Daniel conv lucas l\n\nTime 2\n\n* Arthur conv cesar"


def test_format_whatsapp_draw_includes_match_notes_when_present() -> None:
    match = Match(id=1, scheduled_at=datetime(2026, 8, 3, 20, 0), notes="Quadra A")
    draw = Draw(
        match_id=1,
        request_params={},
        request_payload={},
        response_payload={},
        normalized_result={"teams": [{"team_name": "Time 1", "players": [{"name": "David"}]}]},
    )

    assert format_whatsapp_draw(match, draw).startswith("Quadra A - 03/08/2026 20:00")
