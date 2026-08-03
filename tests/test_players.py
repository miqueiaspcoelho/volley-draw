from collections.abc import Generator
from decimal import Decimal

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from app.db.base import Base
from app.db.session import get_db
from app.main import create_app
from app.schemas.player import PlayerCreate, PlayerUpdate
from app.services.players import (
    DuplicatePlayerNameError,
    create_player,
    list_players,
    set_player_active,
    update_player,
)


@pytest.fixture()
def db_session() -> Generator[Session, None, None]:
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
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


def player_data(name: str = "Miqueias") -> PlayerCreate:
    return PlayerCreate(
        name=name,
        nickname=None,
        serving=Decimal("5.0"),
        passing=Decimal("4.0"),
        setting=Decimal("3.0"),
        attacking=Decimal("5.0"),
        blocking=Decimal("4.0"),
    )


def test_create_player_persists_and_calculates_overall(db_session: Session) -> None:
    player = create_player(db_session, player_data())

    assert player.id is not None
    assert player.active is True
    assert player.overall == Decimal("4.2")


def test_create_player_rejects_duplicate_name(db_session: Session) -> None:
    create_player(db_session, player_data("David"))

    with pytest.raises(DuplicatePlayerNameError):
        create_player(db_session, player_data("David"))


def test_update_player_changes_notes_and_active_status(db_session: Session) -> None:
    player = create_player(db_session, player_data("Jean"))

    updated = update_player(
        db_session,
        player.id,
        PlayerUpdate(serving=Decimal("1.0"), active=False),
    )

    assert updated.serving == Decimal("1.0")
    assert updated.active is False
    assert updated.overall == Decimal("3.4")


def test_set_player_active_toggles_without_deleting(db_session: Session) -> None:
    player = create_player(db_session, player_data("Paulo"))

    inactive = set_player_active(db_session, player.id, False)

    assert inactive.id == player.id
    assert inactive.active is False


def test_list_players_can_filter_active_only(db_session: Session) -> None:
    active = create_player(db_session, player_data("Ativo"))
    inactive = create_player(db_session, player_data("Inativo"))
    set_player_active(db_session, inactive.id, False)

    players = list_players(db_session, active_only=True)

    assert [player.id for player in players] == [active.id]


def test_player_schema_rejects_invalid_skill_range() -> None:
    with pytest.raises(ValueError):
        player_data().model_copy(update={"serving": Decimal("5.1")}).model_validate(
            {
                **player_data().model_dump(),
                "serving": Decimal("5.1"),
            }
        )


def test_player_schema_rejects_more_than_one_decimal() -> None:
    with pytest.raises(ValueError):
        PlayerCreate(**{**player_data().model_dump(), "serving": Decimal("4.25")})


def test_create_player_route_returns_created_player(client: TestClient) -> None:
    response = client.post("/players", json={**player_data("Route").model_dump(mode="json")})

    assert response.status_code == 201
    assert response.json()["name"] == "Route"
    assert response.json()["overall"] == "4.2"


def test_active_route_deactivates_player(client: TestClient) -> None:
    created = client.post("/players", json={**player_data("Toggle").model_dump(mode="json")})

    response = client.patch(f"/players/{created.json()['id']}/active", json={"active": False})

    assert response.status_code == 200
    assert response.json()["active"] is False
