from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.auth import require_auth
from app.db.session import get_db
from app.schemas.draw import DrawRequest
from app.services.draw_api import DrawApiError, DrawApiRejectedError
from app.services.draws import DrawPayloadError, draw_match_teams
from app.services.matches import MatchNotFoundError

router = APIRouter(prefix="/matches", tags=["draws"], dependencies=[Depends(require_auth)])


@router.post("/{match_id}/draw")
def draw_match(match_id: int, request: DrawRequest, db: Session = Depends(get_db)) -> dict:
    try:
        draw = draw_match_teams(db, match_id, request)
        return {
            "id": draw.id,
            "match_id": draw.match_id,
            "result": draw.normalized_result,
            "response": draw.response_payload,
        }
    except MatchNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    except DrawPayloadError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc
    except DrawApiRejectedError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc
    except DrawApiError as exc:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Nao foi possivel chamar a API externa de sorteio.",
        ) from exc

