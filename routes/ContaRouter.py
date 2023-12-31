from fastapi import APIRouter, Depends, Form, HTTPException, Path, Request, status
from fastapi.responses import JSONResponse, HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from models.Conta import Conta
from models.Usuario import Usuario
from repositories.ContaRepo import ContaRepo
from repositories.UsuarioRepo import UsuarioRepo
from util.seguranca import validar_usuario_logado
from util.templateFilters import formatar_data
from util.validators import *

router = APIRouter()

templates = Jinja2Templates(directory="templates")


@router.on_event("startup")
async def startup_event():
    templates.env.filters["date"] = formatar_data


@router.post(
    "/addConta",
    tags=["Conta"],
    summary="Nova conta",
    response_class=HTMLResponse,
)
async def postNovaConta(
    request: Request,
    nome: str = Form(""),
    saldo: float = Form(""),
    descricao: str = Form(None),
    usuario: Usuario = Depends(validar_usuario_logado),
):
    if usuario:
        token = request.cookies.values().mapping["auth_token"]
        user = UsuarioRepo.obterUsuarioPorToken(token)
        ContaRepo.inserir(Conta(0, user.id, nome, saldo, descricao))
        return RedirectResponse("/configuracoes", status_code=status.HTTP_303_SEE_OTHER)
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)


@router.get("/carteira")
async def getTrans(
    request: Request, usuario: Usuario = Depends(validar_usuario_logado)
):
    if usuario:
        contas = ContaRepo.obterContaPorUsuario(usuario.id)
        saldo_contas = ContaRepo.obterSaldoContas(usuario.id)
        mensagem = "Carteira"
        pagina = "/carteira"
        return templates.TemplateResponse(
            "conta/carteira.html",
            {
                "request": request,
                "contas": contas,
                "saldo_contas": saldo_contas,
                "mensagem": mensagem,
                "usuario": usuario,
                "pagina": pagina,
            },
        )
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)


@router.post("/carteira/nova", response_class=HTMLResponse)
async def postNovaCarteira(
    request: Request,
    nome: str = Form(""),
    saldo: float = Form(""),
    usuario: Usuario = Depends(validar_usuario_logado),
):
    if usuario:
        nome = nome.strip()

        erros = {}

        is_not_empty(nome, "nome", erros)

        if len(erros) > 0:
            valores = {}
            valores["nome"] = nome
            valores["saldo"] = saldo
            return templates.TemplateResponse(
                "/conta/carteira.html",
                {
                    "request": request,
                    "usuario": usuario,
                    "erros": erros,
                    "valores": valores,
                },
            )

        ContaRepo.inserir(Conta(0, usuario.id, nome, saldo))
        return RedirectResponse("/carteira", status_code=status.HTTP_303_SEE_OTHER)
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)


@router.post("/carteira/excluir", response_class=HTMLResponse)
async def postExcluir(
    id: int = Form(""),
    usuario: Usuario = Depends(validar_usuario_logado),
):
    if usuario:
        ContaRepo.excluirContaTransacoes(id)
        return RedirectResponse("/carteira", status_code=status.HTTP_303_SEE_OTHER)
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
