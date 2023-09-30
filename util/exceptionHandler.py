from fastapi import Depends, FastAPI, HTTPException, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
import logging

from models.Usuario import Usuario
from util.seguranca import validar_usuario_logado


templates = Jinja2Templates(directory="templates")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def configurar(app: FastAPI):
    @app.exception_handler(401)
    async def unauthorized_exception_handler(request: Request, _):
        returnUrl = f"?returnUrl={request.url.path}"
        return RedirectResponse(f"/entrar{returnUrl}", status_code=status.HTTP_302_FOUND)

    @app.exception_handler(403)
    async def forbidden_exception_handler(request: Request, _):
        returnUrl = f"?returnUrl={request.url.path}&status=403"
        return RedirectResponse(f"/entrar{returnUrl}", status_code=status.HTTP_302_FOUND)

    @app.exception_handler(404)
    async def page_not_found_exception_handler(request: Request, _):
        return templates.TemplateResponse("main/notfound.html", {"request": request})

    @app.exception_handler(HTTPException)
    async def http_exception_handler(
        request: Request,
        ex: HTTPException,
        usuario: Usuario = Depends(validar_usuario_logado),
    ):
        logger.error(f"Ocorreu uma exceção não tratada: {ex}")
        return templates.TemplateResponse(
            "main/erro.html",
            {"request": request, "detail": "Erro na requisição HTTP."},
            status_code=ex.status_code,
        )

    # @app.exception_handler(RequestValidationError)
    # async def request_validation_error(request: Request, exc: RequestValidationError):
    #     erros = {}
    #     errors = exc.errors()
    #     for erro in errors:
    #         campo, mensagem = erro["loc"], erro["msg"]
    #         campo_isolado = campo[1:] if campo[0] in ("body", "query", "path") else campo
    #         campo_isolado = ".".join(campo_isolado)
    #         erros[campo_isolado] = mensagem
        
    #     return JSONResponse({"ok": False, "erros": erros, "returnUrl": request.url.path}, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)

    @app.exception_handler(Exception)
    async def general_exception_handler(request: Request, ex: Exception):
        logger.error(f"Ocorreu uma exceção não tratada: {ex}")
        return templates.TemplateResponse(
            "main/erro.html",
            {"request": request, "detail": "Erro interno do servidor."},
            status_code=500,
        )