from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from app.db.base import Base
from app.db.session import get_db
from app.main import create_app


@pytest.fixture()
def client() -> Generator[TestClient, None, None]:
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(engine)
    TestingSessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
    session = TestingSessionLocal()
    app = create_app()

    def override_get_db() -> Generator[Session, None, None]:
        yield session

    app.dependency_overrides[get_db] = override_get_db
    try:
        yield TestClient(app)
    finally:
        session.close()
        Base.metadata.drop_all(engine)


def test_players_page_renders_form_and_empty_list(client: TestClient) -> None:
    response = client.get("/jogadores")

    assert response.status_code == 200
    assert "Novo jogador" in response.text
    assert "Nenhum jogador cadastrado" in response.text


def test_players_page_creates_and_lists_player(client: TestClient) -> None:
    response = client.post(
        "/jogadores",
        data={
            "name": "Miqueias",
            "nickname": "Miq",
            "serving": "5.0",
            "passing": "4.0",
            "setting": "3.0",
            "attacking": "5.0",
            "blocking": "4.0",
            "active": "true",
        },
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert "Miqueias" in response.text
    assert "4.2" in response.text


def test_players_page_shows_validation_error(client: TestClient) -> None:
    response = client.post(
        "/jogadores",
        data={
            "name": "Erro",
            "serving": "5.5",
            "passing": "4.0",
            "setting": "3.0",
            "attacking": "5.0",
            "blocking": "4.0",
            "active": "true",
        },
    )

    assert response.status_code == 400
    assert "Confira os campos" in response.text


def test_players_page_edits_and_deactivates_player(client: TestClient) -> None:
    created = client.post(
        "/jogadores",
        data={
            "name": "David",
            "serving": "4.0",
            "passing": "4.0",
            "setting": "3.0",
            "attacking": "4.0",
            "blocking": "5.0",
            "active": "true",
        },
        follow_redirects=True,
    )
    assert created.status_code == 200

    edit_page = client.get("/jogadores/1/editar")
    assert "Editar jogador" in edit_page.text

    updated = client.post(
        "/jogadores/1",
        data={
            "name": "David Lima",
            "serving": "4.0",
            "passing": "4.0",
            "setting": "3.0",
            "attacking": "4.0",
            "blocking": "5.0",
            "active": "true",
        },
        follow_redirects=True,
    )
    assert "David Lima" in updated.text

    inactive = client.post("/jogadores/1/ativo", data={"active": "false"}, follow_redirects=True)
    assert "Inativo" in inactive.text
