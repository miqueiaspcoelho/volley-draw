import httpx

from app.core.config import get_settings
from app.schemas.draw import DrawPayload


class DrawApiError(RuntimeError):
    pass


class DrawApiRejectedError(ValueError):
    pass


class DrawApiClient:
    def __init__(self, http_client: httpx.Client | None = None) -> None:
        self.settings = get_settings()
        self.http_client = http_client

    def draw_teams(self, payload: DrawPayload) -> dict:
        close_client = self.http_client is None
        client = self.http_client or httpx.Client(
            base_url=self.settings.draw_api_base_url,
            timeout=self.settings.draw_api_timeout,
            verify=self.settings.draw_api_verify_tls,
        )
        try:
            response = client.post("/api/drawteams", json=payload.model_dump(mode="json"))
            if 400 <= response.status_code < 500:
                raise DrawApiRejectedError(_api_error_message(response))
            response.raise_for_status()
            data = response.json()
        except DrawApiRejectedError:
            raise
        except httpx.HTTPError as exc:
            raise DrawApiError(f"draw api request failed: {exc}") from exc
        except ValueError as exc:
            raise DrawApiError("draw api returned invalid json") from exc
        finally:
            if close_client:
                client.close()

        if not isinstance(data, dict) or data.get("success") is not True:
            raise DrawApiRejectedError("API externa recusou o sorteio.")
        return data


def _api_error_message(response: httpx.Response) -> str:
    try:
        data = response.json()
    except ValueError:
        return "API externa recusou o sorteio."
    if isinstance(data, dict):
        return str(data.get("message") or data.get("error") or "API externa recusou o sorteio.")
    return "API externa recusou o sorteio."
