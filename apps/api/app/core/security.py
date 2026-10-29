from dataclasses import dataclass
from functools import lru_cache
from typing import Annotated, Any, Protocol
from uuid import UUID

import jwt
from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.core.config import get_settings
from app.core.errors import Unauthorized


@dataclass(frozen=True, slots=True)
class CurrentUser:
    id: UUID
    email: str | None
    full_name: str | None
    avatar_url: str | None


class TokenVerifier(Protocol):
    def verify(self, token: str) -> dict[str, Any]: ...


class SupabaseTokenVerifier:
    """Verifies Supabase access tokens (asymmetric keys via JWKS, HS256 fallback)."""

    def __init__(self) -> None:
        settings = get_settings()
        self._settings = settings
        self._jwks = jwt.PyJWKClient(settings.jwks_url, cache_keys=True, lifespan=3600)

    def verify(self, token: str) -> dict[str, Any]:
        settings = self._settings
        try:
            if jwt.get_unverified_header(token).get("alg") == "HS256":
                if not settings.supabase_jwt_secret:
                    raise Unauthorized()
                key: Any = settings.supabase_jwt_secret
                algorithms = ["HS256"]
            else:
                key = self._jwks.get_signing_key_from_jwt(token)
                algorithms = ["ES256", "RS256"]
            return jwt.decode(
                token,
                key,
                algorithms=algorithms,
                audience=settings.jwt_audience,
                issuer=settings.jwt_issuer,
                options={"require": ["exp", "sub"]},
            )
        except (jwt.PyJWTError, jwt.PyJWKClientError) as exc:
            raise Unauthorized() from exc


@lru_cache
def get_token_verifier() -> TokenVerifier:
    return SupabaseTokenVerifier()


_bearer = HTTPBearer(auto_error=False)


def get_current_user(
    credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(_bearer)],
    verifier: Annotated[TokenVerifier, Depends(get_token_verifier)],
) -> CurrentUser:
    if credentials is None:
        raise Unauthorized("Autenticação necessária.")
    claims = verifier.verify(credentials.credentials)
    metadata = claims.get("user_metadata") or {}
    try:
        user_id = UUID(claims["sub"])
    except ValueError as exc:
        raise Unauthorized() from exc
    return CurrentUser(
        id=user_id,
        email=claims.get("email"),
        full_name=metadata.get("full_name") or metadata.get("name"),
        avatar_url=metadata.get("avatar_url") or metadata.get("picture"),
    )
