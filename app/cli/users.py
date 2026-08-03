from __future__ import annotations

import argparse
import getpass

from app.db.session import SessionLocal
from app.services.auth import DuplicateUsernameError, create_user


def main() -> None:
    parser = argparse.ArgumentParser(description="Gerencia usuarios locais do Volley Draw.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    create_parser = subparsers.add_parser("create", help="Cria um usuario ativo com PIN.")
    create_parser.add_argument("username")
    create_parser.add_argument("name")
    create_parser.add_argument("--pin", default=None)

    args = parser.parse_args()
    if args.command == "create":
        pin = args.pin or getpass.getpass("PIN: ")
        with SessionLocal() as db:
            try:
                user = create_user(db, name=args.name, username=args.username, pin=pin)
            except DuplicateUsernameError as exc:
                raise SystemExit("Usuario ja existe.") from exc
        print(f"Usuario criado: {user.username}")


if __name__ == "__main__":
    main()
