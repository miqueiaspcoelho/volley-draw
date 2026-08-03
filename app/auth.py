from fastapi import Depends, HTTPException, Request, status
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.db.session import get_db
from app.services.auth import SESSION_COOKIE_NAME, get_active_user, read_session_token


def require_auth(request: Request, db: Session = Depends(get_db)) -> None:
    settings = get_settings()
    user_id = read_session_token(request.cookies.get(SESSION_COOKIE_NAME), settings.session_secret)
    if user_id is None or get_active_user(db, user_id) is None:
        raise HTTPException(status_code=status.HTTP_303_SEE_OTHER, headers={"Location": "/login"})