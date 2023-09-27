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
    mensagem = "Configurações"
    usuario = ""
    pagina = "/configuracoes"
    contas = ContaRepo.obterTodos()
    return templates.TemplateResponse(
        "configuracoes.html", { "request": request,
                            "mensagem": mensagem,
                            "usuario": usuario,
                             "pagina": pagina, 
                             "contas": contas,}
    )


@router.get("/dependentes")
async def getIndex(request: Request):
    mensagem = "Dependentes"
    usuario = ""
    pagina = "/configuracoes"
    return templates.TemplateResponse(
        "/dependentes/dependente.html", { "request": request,
                            "pagina": pagina,
                            "mensagem": mensagem,
                            "usuario": usuario, }
    )