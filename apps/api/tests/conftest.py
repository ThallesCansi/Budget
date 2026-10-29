import os
import time
import uuid
from collections.abc import Callable, Iterator
from typing import Any

import jwt
import pytest
from alembic.config import Config
from cryptography.hazmat.primitives.asymmetric import ec
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, text

from alembic import command

ISSUER = "http://supabase.test/auth/v1"
_PRIVATE_KEY = ec.generate_private_key(ec.SECP256R1())


def _database_url() -> str:
    """TEST_DATABASE_URL (CI) or an embedded Postgres via pgserver (local, no Docker)."""
    if url := os.environ.get("TEST_DATABASE_URL"):
        return url
    import pgserver

    data_dir = os.path.join(os.path.dirname(__file__), "..", ".pgdata")
    server = pgserver.get_server(data_dir, cleanup_mode=None)
    admin = server.get_uri().replace("postgresql://", "postgresql+psycopg://", 1)
    engine = create_engine(admin, isolation_level="AUTOCOMMIT")
    with engine.connect() as conn:
        conn.execute(text("DROP DATABASE IF EXISTS budget_test WITH (FORCE)"))
        conn.execute(text("CREATE DATABASE budget_test"))
    engine.dispose()
    return admin.replace("/postgres?", "/budget_test?", 1)


@pytest.fixture(scope="session", autouse=True)
def database() -> str:
    url = _database_url()
    os.environ.update(
        DATABASE_URL=url,
        ENVIRONMENT="test",
        SUPABASE_URL="http://supabase.test",
        CRON_SECRET="test-cron-secret",
    )
    from app.core.config import get_settings

    get_settings.cache_clear()
    cfg = Config(os.path.join(os.path.dirname(__file__), "..", "alembic.ini"))
    cfg.set_main_option("script_location", os.path.join(os.path.dirname(__file__), "..", "alembic"))
    command.upgrade(cfg, "head")
    return url


class StaticKeyVerifier:
    def verify(self, token: str) -> dict[str, Any]:
        from app.core.errors import Unauthorized

        try:
            return jwt.decode(
                token,
                _PRIVATE_KEY.public_key(),
                algorithms=["ES256"],
                audience="authenticated",
                issuer=ISSUER,
                options={"require": ["exp", "sub"]},
            )
        except jwt.PyJWTError as exc:
            raise Unauthorized() from exc


def make_token(
    user_id: uuid.UUID,
    *,
    email: str = "ana@example.com",
    name: str = "Ana Souza",
    expires_in: int = 3600,
    key: Any = None,
) -> str:
    now = int(time.time())
    claims = {
        "sub": str(user_id),
        "email": email,
        "aud": "authenticated",
        "iss": ISSUER,
        "iat": now,
        "exp": now + expires_in,
        "user_metadata": {"full_name": name},
    }
    return jwt.encode(claims, key or _PRIVATE_KEY, algorithm="ES256")


@pytest.fixture
def client(database: str) -> Iterator[TestClient]:
    from app.core.db import get_engine, get_sessionmaker
    from app.core.security import get_token_verifier
    from app.main import create_app
    from app.models import Base

    app = create_app()
    app.dependency_overrides[get_token_verifier] = StaticKeyVerifier
    with TestClient(app) as test_client:
        yield test_client

    tables = ", ".join(t.name for t in Base.metadata.sorted_tables)
    with get_engine().begin() as conn:
        conn.execute(text(f"TRUNCATE {tables} CASCADE"))
    get_sessionmaker.cache_clear()


AuthFactory = Callable[..., dict[str, str]]


@pytest.fixture
def auth() -> AuthFactory:
    """`auth()` -> headers for a fresh user; `auth(user_id)` -> headers for that user."""

    def factory(user_id: uuid.UUID | None = None, **kwargs: Any) -> dict[str, str]:
        return {"Authorization": f"Bearer {make_token(user_id or uuid.uuid4(), **kwargs)}"}

    return factory
