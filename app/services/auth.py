from __future__ import annotations

import base64
import hashlib
import hmac
import os
import time
from dataclasses import dataclass

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models import User

SESSION_COOKIE_NAME = "volley_draw_session"
SESSION_MAX_AGE = 60 * 60 * 24 * 30


class DuplicateUsernameError(ValueError):
    pass


@dataclass(frozen=True)
class AuthenticatedUser:
    id: int
    name: str
    username: str


def hash_pin(pin: str, salt: bytes | None = None) -> str:
    salt = salt or os.urandom(16)
    digest = hashlib.pbkdf2_hmac("sha256", pin.encode("utf-8"), salt, 120_000)
    return f"pbkdf2_sha256${base64.urlsafe_b64encode(salt).decode()}${base64.urlsafe_b64encode(digest).decode()}"


def verify_pin(pin: str, stored_hash: str) -> bool:
    try:
        algorithm, salt_text, digest_text = stored_hash.split("$", 2)
    except ValueError:
        return False
    if algorithm != "pbkdf2_sha256":
        return False
    salt = base64.urlsafe_b64decode(salt_text.encode())
    expected = base64.urlsafe_b64decode(digest_text.encode())
    actual = hashlib.pbkdf2_hmac("sha256", pin.encode("utf-8"), salt, 120_000)
    return hmac.compare_digest(actual, expected)


def create_user(db: Session, name: str, username: str, pin: str) -> User:
    clean_username = username.strip().lower()
    if db.scalar(select(User).where(User.username == clean_username)) is not None:
        raise DuplicateUsernameError("username already exists")
    user = User(name=name.strip(), username=clean_username, pin_hash=hash_pin(pin), active=True)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def authenticate_user(db: Session, username: str, pin: str) -> User | None:
    user = db.scalar(select(User).where(User.username == username.strip().lower(), User.active.is_(True)))
    if user is None or not verify_pin(pin, user.pin_hash):
        return None
    return user


def users_exist(db: Session) -> bool:
    return (db.scalar(select(func.count(User.id))) or 0) > 0


def get_active_user(db: Session, user_id: int) -> User | None:
    return db.scalar(select(User).where(User.id == user_id, User.active.is_(True)))


def make_session_token(user_id: int, secret: str, now: int | None = None) -> str:
    issued_at = now or int(time.time())
    payload = f"{user_id}.{issued_at}"
    signature = hmac.new(secret.encode("utf-8"), payload.encode("utf-8"), hashlib.sha256).hexdigest()
    return f"{payload}.{signature}"


def read_session_token(token: str | None, secret: str, max_age: int = SESSION_MAX_AGE) -> int | None:
    if not token:
        return None
    try:
        user_id_text, issued_at_text, signature = token.split(".", 2)
        issued_at = int(issued_at_text)
        user_id = int(user_id_text)
    except ValueError:
        return None
    payload = f"{user_id}.{issued_at}"
    expected = hmac.new(secret.encode("utf-8"), payload.encode("utf-8"), hashlib.sha256).hexdigest()
    if not hmac.compare_digest(signature, expected):
        return None
    if int(time.time()) - issued_at > max_age:
        return None
    return user_id
