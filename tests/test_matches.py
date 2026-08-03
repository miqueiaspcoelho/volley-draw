from collections.abc import Generator
from datetime import datetime
from decimal import Decimal

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from app.db.base import Base
from app.db.session import get_db
from app.main import create_app
from app.schemas.player import PlayerCreate
from app.services.matches import create_match, get_match, list_active_players, set_attendance
from app.services.players import create_player, set_player_active


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
    yield TestClient(app)


def make_player(db: Session, name: str, active: bool = True) -> int:
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
    if not active:
        set_player_active(db, player.id, False)
    return player.id


def test_create_match_and_toggle_attendance(db_session: Session) -> None:
    player_id = make_player(db_session, "Miqueias")
    match = create_match(db_session, datetime(2026, 8, 3, 20, 0), "Quadra 1")

    with_attendance = set_attendance(db_session, match.id, player_id, True)
    assert len(with_attendance.attendances) == 1
    assert with_attendance.attendances[0].serving_snapshot == Decimal("5.0")

    without_attendance = set_attendance(db_session, match.id, player_id, False)
    assert without_attendance.attendances == []


def test_list_active_players_excludes_inactive(db_session: Session) -> None:
    active_id = make_player(db_session, "Ativo")
    make_player(db_session, "Inativo", active=False)

    players = list_active_players(db_session)

    assert [player.id for player in players] == [active_id]


def test_matches_pages_create_match_and_mark_presence(client: TestClient, db_session: Session) -> None:
    make_player(db_session, "David")

    created = client.post(
        "/partidas",
        data={"scheduled_at": "2026-08-03T20:00", "notes": "Quadra 1"},
        follow_redirects=True,
    )
    assert created.status_code == 200
    assert "Partida #1" in created.text
    assert "David" in created.text

    marked = client.post(
        "/partidas/1/presencas",
        data={"player_id": "1", "present": "true"},
        follow_redirects=True,
    )
    assert "Presentes (1)" in marked.text

    match = get_match(db_session, 1)
    assert len(match.attendances) == 1
