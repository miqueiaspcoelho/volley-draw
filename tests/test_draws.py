from collections.abc import Generator
import json
from datetime import datetime
from decimal import Decimal

import httpx
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from app.auth import require_auth
from app.db.base import Base
from app.db.session import get_db
from app.main import create_app
from app.schemas.draw import DrawRequest
from app.schemas.player import PlayerCreate
from app.services.draw_api import DrawApiClient, DrawApiError, DrawApiRejectedError
from app.services.draws import DrawPayloadError, build_draw_payload, draw_match_teams, latest_draw_for_match
from app.services.matches import create_match, set_attendance
from app.services.players import create_player


@pytest.fixture()
def db_session() -> Generator[Session, None, None]:
    engine = create_engine("sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool)
    Base.metadata.create_all(engine)
    TestingSessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
    with TestingSessionLocal() as session:
        yield session
    Base.metadata.drop_all(engine)


@pytest.fixture()
def client(db_session: Session) -> Generator[TestClient, None, None]:
    app = create_app()

    def override_get_db() -> Generator[Session, None, None]:
        yield db_session

    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[require_auth] = lambda: None
    yield TestClient(app)


def seed_present_player(db: Session) -> int:
    player = create_player(
        db,
        PlayerCreate(
            name="Miqueias",
            serving=Decimal("5.0"),
            passing=Decimal("4.0"),
            setting=Decimal("3.0"),
            attacking=Decimal("5.0"),
            blocking=Decimal("4.0"),
        ),
    )
    match = create_match(db, datetime(2026, 8, 3, 20, 0))
    set_attendance(db, match.id, player.id, True)
    return match.id


def seed_present_players(db: Session, names: list[str]) -> int:
    match = create_match(db, datetime(2026, 8, 3, 20, 0))
    for name in names:
        player = create_player(
            db,
            PlayerCreate(
                name=name,
                serving=Decimal("5.0"),
                passing=Decimal("4.0"),
                setting=Decimal("3.0"),
                attacking=Decimal("5.0"),
                blocking=Decimal("4.0"),
            ),
        )
        set_attendance(db, match.id, player.id, True)
    return match.id


def test_draw_request_accepts_decimal_like_integer_strings() -> None:
    request = DrawRequest(players_per_team="2.0", range="2.0")

    assert request.players_per_team == 2
    assert request.range == 2

def test_build_draw_payload_uses_present_player_snapshots(db_session: Session) -> None:
    match_id = seed_present_player(db_session)

    payload = build_draw_payload(db_session, match_id, DrawRequest(players_per_team=6, range=2))

    assert payload.players_per_team == 6
    assert payload.players[0].name == "Miqueias"
    assert payload.players[0].serving == Decimal("5.0")


def test_build_draw_payload_includes_advanced_groups(db_session: Session) -> None:
    match_id = seed_present_players(db_session, ["Miqueias", "David", "Joao"])

    payload = build_draw_payload(
        db_session,
        match_id,
        DrawRequest(
            players_per_team=2,
            range=2,
            force_together=[["Miqueias", "David"]],
            force_apart=[["Miqueias", "Joao"]],
        ),
    )

    assert payload.force_together == [["Miqueias", "David"]]
    assert payload.force_apart == [["Miqueias", "Joao"]]


def test_build_draw_payload_rejects_absent_player_in_advanced_group(db_session: Session) -> None:
    match_id = seed_present_players(db_session, ["Miqueias", "David"])

    with pytest.raises(DrawPayloadError):
        build_draw_payload(
            db_session,
            match_id,
            DrawRequest(force_together=[["Miqueias", "Ausente"]]),
        )


def test_build_draw_payload_rejects_duplicate_player_in_advanced_group(db_session: Session) -> None:
    match_id = seed_present_players(db_session, ["Miqueias", "David"])

    with pytest.raises(DrawPayloadError):
        build_draw_payload(
            db_session,
            match_id,
            DrawRequest(force_apart=[["Miqueias", "Miqueias"]]),
        )


def test_build_draw_payload_rejects_match_without_players(db_session: Session) -> None:
    match = create_match(db_session, datetime(2026, 8, 3, 20, 0))

    with pytest.raises(DrawPayloadError):
        build_draw_payload(db_session, match.id, DrawRequest())


def test_draw_api_client_posts_payload_and_returns_response() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.url.path == "/api/drawteams"
        sent_payload = json.loads(request.content)
        assert sent_payload["players"][0]["serving"] == 5.0
        assert not isinstance(sent_payload["players"][0]["serving"], str)
        return httpx.Response(
            200,
            json={
                "success": True,
                "data": {"leftovers": [], "teams": [{"team_name": "Time 1", "players": []}]},
            },
        )

    payload = build_minimal_payload()
    client = DrawApiClient(httpx.Client(transport=httpx.MockTransport(handler), base_url="https://api.test"))

    response = client.draw_teams(payload)

    assert response["success"] is True


def test_draw_api_client_rejects_unsuccessful_response() -> None:
    http_client = httpx.Client(
        transport=httpx.MockTransport(lambda request: httpx.Response(200, json={"success": False})),
        base_url="https://api.test",
    )

    with pytest.raises(DrawApiRejectedError):
        DrawApiClient(http_client).draw_teams(build_minimal_payload())


def test_draw_route_returns_api_result(client: TestClient, db_session: Session, monkeypatch: pytest.MonkeyPatch) -> None:
    match_id = seed_present_player(db_session)

    monkeypatch.setattr(
        "app.services.draws.DrawApiClient.draw_teams",
        lambda self, payload: {"success": True, "data": {"leftovers": [], "teams": []}},
    )

    response = client.post(f"/matches/{match_id}/draw", json={"players_per_team": 6, "range": 2})

    assert response.status_code == 200
    assert response.json()["result"] == {"leftovers": [], "teams": []}
    assert latest_draw_for_match(db_session, match_id) is not None


def build_minimal_payload():
    from app.schemas.draw import DrawPayload, DrawPlayerPayload

    return DrawPayload(
        players_per_team=6,
        range=2,
        players=[
            DrawPlayerPayload(
                name="Miqueias",
                serving=Decimal("5.0"),
                passing=Decimal("4.0"),
                setting=Decimal("3.0"),
                attacking=Decimal("5.0"),
                blocking=Decimal("4.0"),
            )
        ],
    )


def test_draw_match_teams_persists_payload_response_and_result(db_session: Session, monkeypatch: pytest.MonkeyPatch) -> None:
    match_id = seed_present_player(db_session)
    response_payload = {
        "success": True,
        "data": {
            "leftovers": [],
            "teams": [
                {"team_name": "Time 1", "players": [{"name": "Miqueias", "overall": 4.2}]}
            ],
        },
    }
    monkeypatch.setattr(
        "app.services.draws.DrawApiClient.draw_teams",
        lambda self, payload: response_payload,
    )

    draw = draw_match_teams(db_session, match_id, DrawRequest(players_per_team=6, range=2))

    assert draw.id is not None
    assert draw.request_params["players_per_team"] == 6
    assert draw.request_payload["players"][0]["name"] == "Miqueias"
    assert draw.response_payload == response_payload
    assert draw.normalized_result == response_payload["data"]


def test_match_page_displays_latest_draw(client: TestClient, db_session: Session, monkeypatch: pytest.MonkeyPatch) -> None:
    match_id = seed_present_player(db_session)
    monkeypatch.setattr(
        "app.services.draws.DrawApiClient.draw_teams",
        lambda self, payload: {
            "success": True,
            "data": {
                "leftovers": [],
                "teams": [
                    {"team_name": "Time 1", "players": [{"name": "Miqueias", "overall": 4.2}]}
                ],
            },
        },
    )

    response = client.post(
        f"/partidas/{match_id}/sortear",
        data={"players_per_team": "6", "range": "2"},
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert "Resultado" in response.text
    assert "Time 1" in response.text
    assert "Miqueias" in response.text
    assert "WhatsApp" in response.text
    assert "* Miqueias" in response.text

def test_match_page_accepts_decimal_like_integer_form_values(client: TestClient, db_session: Session, monkeypatch: pytest.MonkeyPatch) -> None:
    match_id = seed_present_player(db_session)
    monkeypatch.setattr(
        "app.services.draws.DrawApiClient.draw_teams",
        lambda self, payload: {"success": True, "data": {"leftovers": [], "teams": []}},
    )

    response = client.post(
        f"/partidas/{match_id}/sortear",
        data={"players_per_team": "2.0", "range": "2.0"},
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert latest_draw_for_match(db_session, match_id).request_params["players_per_team"] == 2


def test_match_page_submits_advanced_groups(client: TestClient, db_session: Session, monkeypatch: pytest.MonkeyPatch) -> None:
    match_id = seed_present_players(db_session, ["Miqueias", "David", "Joao", "Pedro"])
    captured_payloads = []

    def draw(self, payload):
        captured_payloads.append(payload)
        return {"success": True, "data": {"leftovers": [], "teams": []}}

    monkeypatch.setattr("app.services.draws.DrawApiClient.draw_teams", draw)

    response = client.post(
        f"/partidas/{match_id}/sortear",
        data={
            "players_per_team": "2",
            "range": "2",
            "force_together_1": ["Miqueias", "David"],
            "force_apart_2": ["Joao", "Pedro"],
        },
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert captured_payloads[0].force_together == [["Miqueias", "David"]]
    assert captured_payloads[0].force_apart == [["Joao", "Pedro"]]
    assert latest_draw_for_match(db_session, match_id).request_payload["force_together"] == [["Miqueias", "David"]]


def test_match_page_displays_advanced_criteria_blocks(client: TestClient, db_session: Session) -> None:
    match_id = seed_present_players(
        db_session,
        ["Miqueias", "David", "Joao", "Pedro", "Ana", "Bia", "Caio"],
    )

    response = client.get(f"/partidas/{match_id}")

    assert response.status_code == 200
    assert "Criterios avancados" in response.text
    assert 'type="checkbox" name="force_together_1"' in response.text
    assert 'name="force_together_1"' in response.text
    assert 'type="checkbox" name="force_apart_2"' in response.text
    assert 'name="force_apart_2"' in response.text

def test_match_page_returns_502_when_draw_api_fails(client: TestClient, db_session: Session, monkeypatch: pytest.MonkeyPatch) -> None:
    match_id = seed_present_player(db_session)

    def fail_draw(self, payload):
        raise DrawApiError("certificate verify failed")

    monkeypatch.setattr("app.services.draws.DrawApiClient.draw_teams", fail_draw)

    response = client.post(
        f"/partidas/{match_id}/sortear",
        data={"players_per_team": "6", "range": "2"},
    )

    assert response.status_code == 502
    assert "Nao foi possivel chamar a API externa" in response.text


def test_match_page_shows_rejected_draw_message_without_htmx_error(client: TestClient, db_session: Session, monkeypatch: pytest.MonkeyPatch) -> None:
    match_id = seed_present_player(db_session)

    def reject_draw(self, payload):
        raise DrawApiRejectedError("Numero de jogadores insuficiente.")

    monkeypatch.setattr("app.services.draws.DrawApiClient.draw_teams", reject_draw)

    response = client.post(
        f"/partidas/{match_id}/sortear",
        data={"players_per_team": "6", "range": "2"},
    )

    assert response.status_code == 200
    assert "Numero de jogadores insuficiente" in response.text




