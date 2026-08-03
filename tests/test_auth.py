from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from app.db.base import Base
from app.db.session import get_db
from app.main import create_app
from app.services.auth import create_user, hash_pin, verify_pin


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


def test_pin_hash_verification() -> None:
    stored_hash = hash_pin("123456")

    assert verify_pin("123456", stored_hash)
    assert not verify_pin("000000", stored_hash)


def test_protected_page_redirects_when_user_exists(client: TestClient, db_session: Session) -> None:
    create_user(db_session, name="Miqueias", username="miq", pin="123456")

    response = client.get("/jogadores", follow_redirects=False)

    assert response.status_code == 303
    assert response.headers["location"] == "/login"


def test_login_allows_access_to_protected_page(client: TestClient, db_session: Session) -> None:
    create_user(db_session, name="Miqueias", username="miq", pin="123456")

    login = client.post(
        "/login",
        data={"username": "miq", "pin": "123456"},
        follow_redirects=False,
    )
    response = client.get("/jogadores")

    assert login.status_code == 303
    assert response.status_code == 200
    assert "Jogadores" in response.text


def test_invalid_login_shows_error(client: TestClient, db_session: Session) -> None:
    create_user(db_session, name="Miqueias", username="miq", pin="123456")

    response = client.post("/login", data={"username": "miq", "pin": "000000"})

    assert response.status_code == 200
    assert "Usuario ou PIN invalidos" in response.text


def test_invalid_session_cookie_redirects_to_login(client: TestClient, db_session: Session) -> None:
    create_user(db_session, name="Miqueias", username="miq", pin="123456")
    client.cookies.set("volley_draw_session", "invalid")

    response = client.get("/partidas", follow_redirects=False)

    assert response.status_code == 303
    assert response.headers["location"] == "/login"


def test_logout_clears_session_and_redirects(client: TestClient, db_session: Session) -> None:
    create_user(db_session, name="Miqueias", username="miq", pin="123456")
    client.post("/login", data={"username": "miq", "pin": "123456"})

    logout = client.post("/logout", follow_redirects=False)
    protected = client.get("/jogadores", follow_redirects=False)

    assert logout.status_code == 303
    assert logout.headers["location"] == "/login"
    assert protected.status_code == 303
