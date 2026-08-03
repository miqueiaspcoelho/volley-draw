from decimal import Decimal

from app.models import Attendance, Draw, Match, Player, User


def test_player_overall_is_calculated_from_skills() -> None:
    player = Player(
        name="Miqueias",
        serving=Decimal("5.0"),
        passing=Decimal("4.0"),
        setting=Decimal("3.0"),
        attacking=Decimal("5.0"),
        blocking=Decimal("4.0"),
    )

    assert player.overall == Decimal("4.2")


def test_initial_models_are_registered_in_metadata() -> None:
    table_names = {
        Player.__tablename__,
        Match.__tablename__,
        Attendance.__tablename__,
        Draw.__tablename__,
        User.__tablename__,
    }

    assert table_names == {"players", "matches", "attendances", "draws", "users"}


