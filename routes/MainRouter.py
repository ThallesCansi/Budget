from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from util.templateFilters import formatarData


router = APIRouter()

templates = Jinja2Templates(directory="templates")


@router.on_event("startup")
async def startup_event():
    templates.env.filters["date"] = formatarData


@router.get("/dashboard")
async def getIndex(request: Request):
    titulo = "Bom dia, Thalles"
    pagina = "/dashboard"
    return templates.TemplateResponse(
        "dashboard.html", { "request": request,
                            "titulo": titulo,
                            "pagina": pagina,
                          }
    )

@router.get("/configuracoes")
async def getIndex(request: Request):
    titulo = "Configurações"
    pagina = "/configuracoes"
    return templates.TemplateResponse(
        "configuracoes.html", { "request": request,
                            "titulo": titulo,
                             "pagina": pagina, }
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