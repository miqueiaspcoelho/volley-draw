from decimal import Decimal
from typing import Any

from pydantic import BaseModel, Field, field_serializer, field_validator


class DrawSettings(BaseModel):
    players_per_team: int = Field(default=6, ge=1)
    range: int = Field(default=2, ge=0)
    force_together: list[list[str]] = Field(default_factory=list)
    force_apart: list[list[str]] = Field(default_factory=list)

    @field_validator("players_per_team", "range", mode="before")
    @classmethod
    def parse_integer_fields(cls, value: Any) -> Any:
        if isinstance(value, str) and value:
            parsed = float(value)
            if parsed.is_integer():
                return int(parsed)
        return value


class DrawPlayerPayload(BaseModel):
    name: str
    serving: Decimal
    passing: Decimal
    setting: Decimal
    attacking: Decimal
    blocking: Decimal

    @field_serializer("serving", "passing", "setting", "attacking", "blocking")
    def serialize_skill(self, value: Decimal) -> float:
        return float(value)


class DrawPayload(DrawSettings):
    players: list[DrawPlayerPayload]


class DrawRequest(DrawSettings):
    @field_validator("force_together", "force_apart")
    @classmethod
    def strip_groups(cls, value: list[list[str]]) -> list[list[str]]:
        return [[name.strip() for name in group if name.strip()] for group in value if group]





