import sentry_sdk
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.routing import APIRoute
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from slowapi.util import get_remote_address

from app.core.config import get_settings
from app.core.errors import install_error_handlers
from app.routers import accounts, categories, health, me, reports, transactions

API_VERSION = "3.0.0"


def _operation_id(route: APIRoute) -> str:
    # Gives the generated TypeScript client readable names (e.g. `list_accounts`).
    return route.name


def create_app() -> FastAPI:
    settings = get_settings()
    if settings.sentry_dsn:
        sentry_sdk.init(
            dsn=settings.sentry_dsn, environment=settings.environment, traces_sample_rate=0.1
        )

    app = FastAPI(
        title="Budget API",
        version=API_VERSION,
        description="API do Budget — controle financeiro pessoal e familiar.",
        generate_unique_id_function=_operation_id,
    )

    limiter = Limiter(
        key_func=get_remote_address,
        default_limits=[settings.rate_limit],
        enabled=settings.environment != "test",
    )
    app.state.limiter = limiter
    app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)  # type: ignore[arg-type]
    app.add_middleware(SlowAPIMiddleware)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_methods=["*"],
        allow_headers=["Authorization", "Content-Type", "X-Household-Id"],
        max_age=86400,
    )
    install_error_handlers(app)

    for module in (health, me, accounts, categories, transactions, reports):
        app.include_router(module.router)
    return app


app = create_app()
