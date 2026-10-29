"""Starts an embedded Postgres (pgserver) for local development/tests without Docker.

Usage: uv run python scripts/devdb.py  ->  prints a DATABASE_URL
"""

import sys
from pathlib import Path

import pgserver

DATA_DIR = Path(__file__).resolve().parent.parent / ".pgdata"


def main() -> None:
    server = pgserver.get_server(DATA_DIR, cleanup_mode=None)
    uri = server.get_uri().replace("postgresql://", "postgresql+psycopg://", 1)
    print(uri)
    sys.stdout.flush()


if __name__ == "__main__":
    main()
