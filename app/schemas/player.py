from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field, field_validator


class PlayerBase(BaseModel):
    name: str = Field(min_length=1, max_length=120)
    nickname: str | None = Field(default=None, max_length=120)
    serving: Decimal
    passing: Decimal
    setting: Decimal
    attacking: Decimal
    blocking: Decimal

    @field_validator("name", "nickname")
    @classmethod
    def strip_text(cls, value: str | None) -> str | None:
        if value is None:
            return None
        stripped = value.strip()
        return stripped or None

    @field_validator("serving", "passing", "setting", "attacking", "blocking")
    @classmethod
    def validate_skill(cls, value: Decimal) -> Decimal:
        if value < Decimal("0") or value > Decimal("5"):
            raise ValueError("skill must be between 0 and 5")
        if value.as_tuple().exponent < -1:
            raise ValueError("skill must have at most one decimal place")
        return value


class PlayerCreate(PlayerBase):
    active: bool = True


class PlayerUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=120)
    nickname: str | None = Field(default=None, max_length=120)
    serving: Decimal | None = None
    passing: Decimal | None = None
    setting: Decimal | None = None
    attacking: Decimal | None = None
    blocking: Decimal | None = None
    active: bool | None = None

    _strip_text = field_validator("name", "nickname")(PlayerBase.strip_text.__func__)
    _validate_skill = field_validator(
        "serving",
        "passing",
        "setting",
        "attacking",
        "blocking",
    )(PlayerBase.validate_skill.__func__)


class PlayerActiveUpdate(BaseModel):
    active: bool


class PlayerRead(PlayerBase):
    id: int
    active: bool
    overall: Decimal

    model_config = ConfigDict(from_attributes=True)
