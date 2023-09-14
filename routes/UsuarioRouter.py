from fastapi import APIRouter, Form, Request, status
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from models.Usuario import Usuario
from repositories.UsuarioRepo import UsuarioRepo
from utils.templateFilters import formatarData

router = APIRouter()

templates = Jinja2Templates(directory="templates")

tags_metadata = [
    {
        "name": "users",
        "description": "Operações com os Usuários.",
    },
    {
        "name": "items",
        "description": "Manage items. So _fancy_ they have their own docs.",
        "externalDocs": {
            "description": "Items external docs",
            "url": "https://fastapi.tiangolo.com/",
        },
    },
]

@router.on_event("startup")
async def startup_event():
    templates.env.filters["date"] = formatarData


@router.post("/novousuario", tags=["users"], summary="Cadastrar um novo Usuário")
async def postUsuario(
    nome: str = Form(),
    senha: str = Form(),
):
    UsuarioRepo.inserir(Usuario(0, nome, senha))
    return RedirectResponse("/", status_code=status.HTTP_303_SEE_OTHER)

@router.get("/usuarios", response_class=JSONResponse, summary="Exibir todos os Usuários")
async def getUsuarios(request: Request):
    """
    Faça exibir todos os projetos inseridos no banco de dados.
    """
    projetos = UsuarioRepo.getAll()
    return {"projetos": projetos}
