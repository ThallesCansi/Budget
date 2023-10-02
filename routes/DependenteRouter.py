from fastapi import APIRouter, Depends, Form, HTTPException, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from models.Dependente import Dependente
from models.Usuario import Usuario
from repositories.DependenteRepo import DependenteRepo
from repositories.UsuarioRepo import UsuarioRepo
from util.seguranca import validar_usuario_logado
from util.templateFilters import formatar_data

router = APIRouter(prefix="/dependente")

templates = Jinja2Templates(directory="templates")


@router.on_event("startup")
async def startup_event():
    templates.env.filters["date"] = formatar_data


@router.post(
    "/adicionar",
    tags=["Dependente"],
    summary="Inserir um novo dependente à tabela para um usuário do sistema.",
    response_class=HTMLResponse,
)
async def postAdicionar(
    request: Request,
    nome: str = Form(""),
    usuario: Usuario = Depends(validar_usuario_logado),
):
    if usuario:
        token = request.cookies.values().mapping["auth_token"]
        user = UsuarioRepo.obterUsuarioPorToken(token)
        DependenteRepo.inserir(Dependente(0, user.id, nome))
        return RedirectResponse("/dependentes", status_code=status.HTTP_303_SEE_OTHER)
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
