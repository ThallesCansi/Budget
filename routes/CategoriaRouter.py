from fastapi import APIRouter, Depends, Form, HTTPException, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from models.Categoria import Categoria
from models.Usuario import Usuario
from repositories.CategoriaRepo import CategoriaRepo
from repositories.UsuarioRepo import UsuarioRepo
from util.seguranca import validar_usuario_logado
from util.templateFilters import formatar_data


router = APIRouter(prefix="/categoria")

templates = Jinja2Templates(directory="templates")


@router.on_event("startup")
async def startup_event():
    templates.env.filters["date"] = formatar_data


@router.post(
    "/adicionar",
    tags=["Categoria"],
    summary="Inserir uma nova categoria à tabela para um usuário do sistema.",
    response_class=HTMLResponse,
)
async def postNovaCategoria(
    request: Request,
    nome: str = Form(""),
    tipo: str = Form(""),
    usuario: Usuario = Depends(validar_usuario_logado),
):
    if usuario:
        token = request.cookies.values().mapping["auth_token"]
        user = UsuarioRepo.obterUsuarioPorToken(token)
        CategoriaRepo.inserir(
            Categoria(
                0,
                user.id,
                nome,
                tipo,
            )
        )
        return RedirectResponse("/configuracoes", status.HTTP_303_SEE_OTHER)
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

@router.post("/excluir", response_class=HTMLResponse)
async def postExcluir(
    id: int = Form(""),
    usuario: Usuario = Depends(validar_usuario_logado),
):
    if usuario:
        CategoriaRepo.excluir(id)
        return RedirectResponse("/configuracoes", status_code=status.HTTP_303_SEE_OTHER)
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)