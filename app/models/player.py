from datetime import datetime
from decimal import Decimal

from sqlalchemy import Boolean, CheckConstraint, DateTime, Numeric, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

from app.db.base import Base


class Player(Base):
    __tablename__ = "players"
    __table_args__ = (
        CheckConstraint("serving >= 0 AND serving <= 5", name="ck_players_serving_range"),
        CheckConstraint("passing >= 0 AND passing <= 5", name="ck_players_passing_range"),
        CheckConstraint("setting >= 0 AND setting <= 5", name="ck_players_setting_range"),
        CheckConstraint("attacking >= 0 AND attacking <= 5", name="ck_players_attacking_range"),
        CheckConstraint("blocking >= 0 AND blocking <= 5", name="ck_players_blocking_range"),
        UniqueConstraint("name", name="uq_players_name"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    nickname: Mapped[str | None] = mapped_column(String(120))
    serving: Mapped[Decimal] = mapped_column(Numeric(2, 1), nullable=False)
    passing: Mapped[Decimal] = mapped_column(Numeric(2, 1), nullable=False)
    setting: Mapped[Decimal] = mapped_column(Numeric(2, 1), nullable=False)
    attacking: Mapped[Decimal] = mapped_column(Numeric(2, 1), nullable=False)
    blocking: Mapped[Decimal] = mapped_column(Numeric(2, 1), nullable=False)
    active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    @property
    def overall(self) -> Decimal:
        return (
            self.serving
            + self.passing
            + self.setting
            + self.attacking
            + self.blocking
        ) / Decimal("5")
