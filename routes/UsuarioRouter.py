from fastapi import APIRouter, Form, Path, Request, status
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from models.Usuario import Usuario
from repositories.UsuarioRepo import UsuarioRepo
from util.templateFilters import formatarData


router = APIRouter()

templates = Jinja2Templates(directory="templates")


@router.on_event("startup")
async def startup_event():
    templates.env.filters["date"] = formatarData


@router.post(
    "/novousuario",
    tags=["Usuário"],
    summary="Novo usuário",
    response_class=JSONResponse,
)
async def postNovoUsuario(
    nome: str = Form(),
    senha: str = Form(),
):
    UsuarioRepo.inserir(Usuario(0, nome, senha))
    return {"nome": nome, "senha": senha}


@router.get(
    "/usuarios",
    tags=["Usuário"],
    summary="Consultar usuários",
    response_class=JSONResponse,
)
async def getUsuarios():
    usuarios = UsuarioRepo.obterTodos()
    return {"usuarios": usuarios}


@router.get(
    "/usuario/{id}",
    tags=["Usuário"],
    summary="Consultar um único usuário",
    response_class=JSONResponse,
)
async def getUsuario(id: int = Path(...)):
    usuario = UsuarioRepo.obterPorId(id)
    return {"usuario": usuario}


@router.put(
    "/atualizarUsuario",
    tags=["Usuário"],
    summary="Atualizar usuário",
    response_class=JSONResponse,
)
async def putAtualizarUsuario(
    id: int = Form(), nome: str = Form(), senha: str = Form()
):
    usuarioAtualizado = UsuarioRepo.alterar(Usuario(id, nome, senha))
    return {"usuarioAtualizado": usuarioAtualizado}


@router.delete(
    "/excluirusuario",
    tags=["Usuário"],
    summary="Excluir usuário",
    response_class=JSONResponse,
)
async def deleteExcluirUsuario(id: int = Form()):
    usuario = UsuarioRepo.excluir(id)
    return {"usuario": usuario}


@router.delete(
    "/excluirusuarios",
    tags=["Usuário"],
    summary="Excluir todos os usuários",
    response_class=JSONResponse,
)
async def deleteExcluirUsuarios():
    usuarios = UsuarioRepo.limparTabela()
    return {"usuarios": usuarios}
