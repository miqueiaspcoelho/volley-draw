from collections.abc import Generator
from datetime import datetime

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from app.db.base import Base
from app.db.session import get_db
from app.main import create_app
from app.models.draw import Draw
from app.services.matches import create_match


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


def seed_match_with_draw(db: Session) -> int:
    match = create_match(db, datetime(2026, 8, 3, 20, 0), notes="Quadra A")
    draw = Draw(
        match_id=match.id,
        request_params={"players_per_team": 2, "range": 2},
        request_payload={},
        response_payload={},
        normalized_result={
            "teams": [{"team_name": "Time 1", "players": [{"name": "Miqueias", "overall": 4.2}]}],
            "leftovers": [],
        },
    )
    db.add(draw)
    db.commit()
    return match.id


def test_history_page_lists_matches_and_draw_status(client: TestClient, db_session: Session) -> None:
    seed_match_with_draw(db_session)

    response = client.get("/historico")

    assert response.status_code == 200
    assert "Historico" in response.text
    assert "Partida #1" in response.text
    assert "Com sorteio" in response.text


def test_history_detail_displays_saved_draw_and_share_text(client: TestClient, db_session: Session) -> None:
    match_id = seed_match_with_draw(db_session)

    response = client.get(f"/historico/{match_id}")

    assert response.status_code == 200
    assert "Resultado salvo" in response.text
    assert "Time 1" in response.text
    assert "Miqueias" in response.text
    assert "* Miqueias" in response.text


def test_history_detail_returns_404_for_missing_match(client: TestClient) -> None:
    response = client.get("/historico/999")

    assert response.status_code == 404
    assert "Partida nao encontrada" in response.text
