from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from repositories.ContaRepo import ContaRepo
from utils.templateFilters import formatarData


router = APIRouter()

templates = Jinja2Templates(directory="templates")


@router.on_event("startup")
async def startup_event():
    templates.env.filters["date"] = formatarData


@router.get("/")
async def getIndex(request: Request):
    return templates.TemplateResponse(
        "signUp-signIn.html", { "request": request,}
    )

@router.get("/recuperarSenha")
async def getRecuperar(request: Request):
    return templates.TemplateResponse(
        "recuperarSenha.html", { "request": request,}
    )


@router.get("/dashboard")
async def getDash(request: Request):
    titulo = "Bom dia, Thalles"
    pagina = "/dashboard"
    return templates.TemplateResponse(
        "dashboard.html", { "request": request,
                            "titulo": titulo,
                            "pagina": pagina,
                          }
    )

@router.get("/transacoes")
async def getTrans(request: Request):
    titulo = "Transações"
    pagina = "/transacoes"
    return templates.TemplateResponse(
        "transacoes.html", { "request": request,
                            "titulo": titulo,
                            "pagina": pagina,
                          }
    )

@router.get("/configuracoes")
async def getConfig(request: Request):
    titulo = "Configurações"
    pagina = "/configuracoes"
    contas = ContaRepo.obterTodos()
    return templates.TemplateResponse(
        "configuracoes.html", { "request": request,
                            "titulo": titulo,
                             "pagina": pagina, 
                             "contas": contas,}
    )


@router.get("/formCategoria")
async def getIndex(request: Request):
    titulo = "Conta"
    activeConfig = "active"
    return templates.TemplateResponse(
        "formCategoria.html", { "request": request,
                            "titulo": titulo,
                             "activeConfig": activeConfig, }
    )