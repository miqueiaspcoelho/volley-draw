from datetime import datetime

from pydantic import BaseModel, Field


class MatchCreate(BaseModel):
    scheduled_at: datetime
    notes: str | None = Field(default=None, max_length=1000)


class AttendanceUpdate(BaseModel):
    player_id: int
    present: bool
