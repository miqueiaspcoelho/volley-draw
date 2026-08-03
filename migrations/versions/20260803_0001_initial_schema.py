"""initial schema

Revision ID: 20260803_0001
Revises:
Create Date: 2026-08-03 00:01:00
"""
from collections.abc import Sequence

from alembic import op
import sqlalchemy as sa

revision: str = "20260803_0001"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "matches",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("scheduled_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("status", sa.String(length=30), nullable=False),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "players",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=120), nullable=False),
        sa.Column("nickname", sa.String(length=120), nullable=True),
        sa.Column("serving", sa.Numeric(2, 1), nullable=False),
        sa.Column("passing", sa.Numeric(2, 1), nullable=False),
        sa.Column("setting", sa.Numeric(2, 1), nullable=False),
        sa.Column("attacking", sa.Numeric(2, 1), nullable=False),
        sa.Column("blocking", sa.Numeric(2, 1), nullable=False),
        sa.Column("active", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.CheckConstraint("serving >= 0 AND serving <= 5", name="ck_players_serving_range"),
        sa.CheckConstraint("passing >= 0 AND passing <= 5", name="ck_players_passing_range"),
        sa.CheckConstraint("setting >= 0 AND setting <= 5", name="ck_players_setting_range"),
        sa.CheckConstraint("attacking >= 0 AND attacking <= 5", name="ck_players_attacking_range"),
        sa.CheckConstraint("blocking >= 0 AND blocking <= 5", name="ck_players_blocking_range"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name", name="uq_players_name"),
    )
    op.create_table(
        "attendances",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("match_id", sa.Integer(), nullable=False),
        sa.Column("player_id", sa.Integer(), nullable=False),
        sa.Column("serving_snapshot", sa.Numeric(2, 1), nullable=False),
        sa.Column("passing_snapshot", sa.Numeric(2, 1), nullable=False),
        sa.Column("setting_snapshot", sa.Numeric(2, 1), nullable=False),
        sa.Column("attacking_snapshot", sa.Numeric(2, 1), nullable=False),
        sa.Column("blocking_snapshot", sa.Numeric(2, 1), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["match_id"], ["matches.id"]),
        sa.ForeignKeyConstraint(["player_id"], ["players.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("match_id", "player_id", name="uq_attendances_match_player"),
    )
    op.create_table(
        "draws",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("match_id", sa.Integer(), nullable=False),
        sa.Column("request_params", sa.JSON(), nullable=False),
        sa.Column("request_payload", sa.JSON(), nullable=False),
        sa.Column("response_payload", sa.JSON(), nullable=False),
        sa.Column("normalized_result", sa.JSON(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["match_id"], ["matches.id"]),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table("draws")
    op.drop_table("attendances")
    op.drop_table("players")
    op.drop_table("matches")
