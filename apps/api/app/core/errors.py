from typing import Any

from fastapi import FastAPI, HTTPException, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse


class AppError(Exception):
    """Domain error rendered as `{"error": {"code", "message", "details"}}`."""

    def __init__(
        self,
        message: str,
        *,
        code: str = "bad_request",
        status_code: int = status.HTTP_400_BAD_REQUEST,
        details: Any = None,
    ) -> None:
        super().__init__(message)
        self.message = message
        self.code = code
        self.status_code = status_code
        self.details = details


class NotFound(AppError):
    def __init__(self, what: str = "Recurso") -> None:
        super().__init__(
            f"{what} não encontrado(a).", code="not_found", status_code=status.HTTP_404_NOT_FOUND
        )


class Unauthorized(AppError):
    def __init__(self, message: str = "Sessão inválida ou expirada.") -> None:
        super().__init__(message, code="unauthorized", status_code=status.HTTP_401_UNAUTHORIZED)


class Forbidden(AppError):
    def __init__(self, message: str = "Você não tem permissão para isso.") -> None:
        super().__init__(message, code="forbidden", status_code=status.HTTP_403_FORBIDDEN)


def _body(code: str, message: str, details: Any = None) -> dict[str, Any]:
    return {"error": {"code": code, "message": message, "details": details}}


def install_error_handlers(app: FastAPI) -> None:
    @app.exception_handler(AppError)
    async def _app_error(_: Request, exc: AppError) -> JSONResponse:
        return JSONResponse(_body(exc.code, exc.message, exc.details), exc.status_code)

    @app.exception_handler(RequestValidationError)
    async def _validation(_: Request, exc: RequestValidationError) -> JSONResponse:
        details = [
            {"field": ".".join(str(p) for p in err["loc"][1:]), "message": err["msg"]}
            for err in exc.errors()
        ]
        return JSONResponse(
            _body("validation_error", "Dados inválidos.", details),
            status.HTTP_422_UNPROCESSABLE_CONTENT,
        )

    @app.exception_handler(HTTPException)
    async def _http(_: Request, exc: HTTPException) -> JSONResponse:
        return JSONResponse(
            _body("http_error", str(exc.detail)), exc.status_code, headers=exc.headers
        )
