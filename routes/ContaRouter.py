from typing import Optional
from fastapi import APIRouter, Form, Path, Request, status
from fastapi.responses import JSONResponse, HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from models.Conta import Conta
from models.Usuario import Usuario
from repositories.ContaRepo import ContaRepo

from utils.templateFilters import formatarData


router = APIRouter()

templates = Jinja2Templates(directory="templates")


@router.on_event("startup")
async def startup_event():
    templates.env.filters["date"] = formatarData


@router.post(
    "/addConta",
    tags=["Conta"],
    summary="Nova conta",
    response_class=HTMLResponse,
)
async def postNovaConta(
    titulo: str = Form(), saldo: float = Form(), meta: str | None = Form(None)
):
    ContaRepo.inserir(Conta(0, Usuario, titulo, saldo, meta))
    return RedirectResponse("/configuracoes", status_code=status.HTTP_303_SEE_OTHER)


@router.get(
    "/addConta",
    tags=["Conta"],
    summary="Consultar contas",
    response_class=HTMLResponse,
)
async def getContas(request: Request):
    contas = ContaRepo.obterTodos()
    return templates.TemplateResponse("configuracoes.html", {"request": request, "contas": contas,})


@router.get(
    "/conta/{id}",
    tags=["Conta"],
    summary="Consultar uma única conta ",
    response_class=JSONResponse,
)
async def getConta(id: int = Path(...)):
    conta = ContaRepo.obterPorId(id)
    return {"conta": conta}


@router.put(
    "/atualizarconta",
    tags=["Conta"],
    summary="Atualizar conta",
    response_class=JSONResponse,
)
async def putAtualizarConta(
    id: int = Form(),
    titulo: str = Form(),
    saldo: float = Form(),
    meta: str | None = Form(None),
):
    contaAtualizada = ContaRepo.alterar(Conta(id, Usuario, titulo, saldo, meta))
    return {"contaAtualizada": contaAtualizada}


@router.delete(
    "/excluirConta",
    tags=["Conta"],
    summary="Excluir conta",
    response_class=HTMLResponse,
)
async def deleteExcluirConta(id: int = Form()):
    conta = ContaRepo.excluir(id)
    return RedirectResponse("/formConta", status_code=status.HTTP_303_SEE_OTHER)


@router.delete(
    "/excluircontas",
    tags=["Conta"],
    summary="Excluir todos as contas",
    response_class=JSONResponse,
)
async def deleteExcluirContas():
    contas = ContaRepo.limparTabela()
    return {"contas": contas}
