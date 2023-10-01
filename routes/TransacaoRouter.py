from fastapi import APIRouter, Depends, Form, HTTPException, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from models.Transacao import Transacao
from models.Usuario import Usuario
from repositories.TransacaoRepo import TransacaoRepo
from repositories.UsuarioRepo import UsuarioRepo
from util.seguranca import validar_usuario_logado
from util.templateFilters import formatarData

router = APIRouter(prefix="/transacao")

templates = Jinja2Templates(directory="templates")


@router.on_event("startup")
async def startup_event():
    templates.env.filters["date"] = formatarData


@router.get(
    "/listagem",
    tags=["Transações"],
    summary="Exibir a listagem das transações da tabela.",
    response_class=HTMLResponse,
)
async def getListagem(
    request: Request,
    mensagem="Transações",
    pagina="/transacoes",
    usuario: Usuario = Depends(validar_usuario_logado),
):
    if usuario:
        token = request.cookies.values().mapping["auth_token"]
        user = UsuarioRepo.obterUsuarioPorToken(token)
        transacoes = TransacaoRepo.obterTransacaoPorUsuario(user.id)
        return templates.TemplateResponse(
            "transacoes/transacoes.html",
            {
                "request": request,
                "transacoes": transacoes,
                "mensagem": mensagem,
                "pagina": pagina,
                "usuario": usuario,
            },
        )
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)


@router.get("/transacoes")
async def getTrans(request: Request):
    mensagem = "Transações"
    usuario = ""
    pagina = "/transacoes"
    return templates.TemplateResponse(
        "transacoes/transacoes.html",
        {
            "request": request,
            "mensagem": mensagem,
            "usuario": usuario,
            "pagina": pagina,
        },
    )
