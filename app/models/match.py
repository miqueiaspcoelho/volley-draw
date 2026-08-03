from datetime import datetime
from decimal import Decimal

from sqlalchemy import DateTime, ForeignKey, Numeric, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from app.db.base import Base


class Match(Base):
    __tablename__ = "matches"

    id: Mapped[int] = mapped_column(primary_key=True)
    scheduled_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    status: Mapped[str] = mapped_column(String(30), nullable=False, default="draft")
    notes: Mapped[str | None] = mapped_column(Text)
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

    attendances: Mapped[list["Attendance"]] = relationship(
        back_populates="match",
        cascade="all, delete-orphan",
    )


class Attendance(Base):
    __tablename__ = "attendances"
    __table_args__ = (
        UniqueConstraint("match_id", "player_id", name="uq_attendances_match_player"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    match_id: Mapped[int] = mapped_column(ForeignKey("matches.id"), nullable=False)
    player_id: Mapped[int] = mapped_column(ForeignKey("players.id"), nullable=False)
    serving_snapshot: Mapped[Decimal] = mapped_column(Numeric(2, 1), nullable=False)
    passing_snapshot: Mapped[Decimal] = mapped_column(Numeric(2, 1), nullable=False)
    setting_snapshot: Mapped[Decimal] = mapped_column(Numeric(2, 1), nullable=False)
    attacking_snapshot: Mapped[Decimal] = mapped_column(Numeric(2, 1), nullable=False)
    blocking_snapshot: Mapped[Decimal] = mapped_column(Numeric(2, 1), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    match: Mapped[Match] = relationship(back_populates="attendances")
