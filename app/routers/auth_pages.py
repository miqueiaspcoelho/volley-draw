from urllib.parse import parse_qs

from fastapi import APIRouter, Depends, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.db.session import get_db
from app.services.auth import SESSION_COOKIE_NAME, SESSION_MAX_AGE, authenticate_user, make_session_token


templates = Jinja2Templates(directory="app/templates")
router = APIRouter(tags=["auth-pages"])


@router.get("/login", response_class=HTMLResponse)
def login_page(request: Request) -> HTMLResponse:
    return _render_login(request)


@router.post("/login", response_class=HTMLResponse)
async def login_submit(request: Request, db: Session = Depends(get_db)) -> HTMLResponse:
    form = await _urlencoded_form(request)
    user = authenticate_user(db, form.get("username", ""), form.get("pin", ""))
    if user is None:
        return _render_login(request, error="Usuario ou PIN invalidos.", status_code=200)
    settings = get_settings()
    response = RedirectResponse("/", status_code=status.HTTP_303_SEE_OTHER)
    response.set_cookie(
        SESSION_COOKIE_NAME,
        make_session_token(user.id, settings.session_secret),
        max_age=SESSION_MAX_AGE,
        httponly=True,
        samesite="lax",
        secure=settings.session_cookie_secure,
    )
    return response


@router.post("/logout")
def logout_submit() -> RedirectResponse:
    response = RedirectResponse("/login", status_code=status.HTTP_303_SEE_OTHER)
    response.delete_cookie(SESSION_COOKIE_NAME)
    return response


def _render_login(request: Request, error: str | None = None, status_code: int = 200) -> HTMLResponse:
    return templates.TemplateResponse(
        request,
        "auth/login.html",
        {"app_name": "Volley Draw", "error": error},
        status_code=status_code,
    )


async def _urlencoded_form(request: Request) -> dict[str, str]:
    body = (await request.body()).decode("utf-8")
    parsed = parse_qs(body, keep_blank_values=True)
    return {key: values[-1] for key, values in parsed.items()}
