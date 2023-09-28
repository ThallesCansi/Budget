from fastapi.templating import Jinja2Templates
from fastapi.responses import JSONResponse, RedirectResponse, HTMLResponse
from models.Usuario import Usuario
from repositories.ContaRepo import ContaRepo
from repositories.UsuarioRepo import UsuarioRepo


from fastapi import APIRouter, Depends, Form, Query, Request, status
from fastapi.templating import Jinja2Templates
from util.seguranca import gerar_token, validar_usuario_logado, verificar_senha

from util.templateFilters import formatarData


router = APIRouter()

templates = Jinja2Templates(directory="templates")


@router.on_event("startup")
async def startup_event():
    templates.env.filters["date"] = formatarData


@router.get("/")
async def getIndex(request: Request):
    return templates.TemplateResponse(
        "main/index.html", { "request": request,}
    )

@router.get("/entrar", tags=["Usuário"], summary="Ir para a página de acesso ao sistema.", response_class=HTMLResponse)
async def getEntrar(request: Request, logado: bool = Depends(validar_usuario_logado)):
    if logado:
        return RedirectResponse("/dashboard", status.HTTP_302_FOUND)
    else:
        return templates.TemplateResponse("usuario/entrar.html", {"request": request})


@router.post("/entrar", tags=["Usuário"], summary="Entrar no sistema através de e-mail e senha.", response_class=HTMLResponse)
async def postEntrar(
    request: Request, 
    usuario: Usuario = Depends(validar_usuario_logado),
    email: str = Form(""), 
    senha: str = Form(""),
    returnUrl: str = Query("/entrar"),
    ):

    # normalização de dados
    email = email.strip().lower()
    senha = senha.strip()

    hash_senha_bd = UsuarioRepo.obterSenhaDeEmail(email)
    if hash_senha_bd:
        if verificar_senha(senha, hash_senha_bd):
            token = gerar_token()
            UsuarioRepo.alterarToken(email, token)
            response = RedirectResponse(returnUrl, status.HTTP_302_FOUND)
            response.set_cookie(key="auth_token", value=token, max_age=1800, httponly=True)
            return response
        else:
            raise Exception(
                "Não foi possível alterar o token do usuário no banco de dados."
            )

@router.get("/sair")
async def getSair(
    request: Request, usuario: Usuario = Depends(validar_usuario_logado)
):   
    if (usuario):
        UsuarioRepo.alterarToken(usuario.email, "") 
    response = RedirectResponse("/entrar", status.HTTP_302_FOUND)
    response.set_cookie(
        key="auth_token", value="", httponly=True, expires="1970-01-01T00:00:00Z"
    )    
    return response


@router.get("/transacoes")
async def getTrans(request: Request):
    mensagem = "Transações"
    usuario = ""
    pagina = "/transacoes"
    return templates.TemplateResponse(
        "transacoes/transacoes.html", { "request": request,
                            "mensagem":mensagem,
                            "usuario": usuario,
                            "pagina": pagina,
                          }
    )

@router.get("/carteira")
async def getTrans(request: Request):
    mensagem = "Carteira"
    usuario = ""
    pagina = "/carteira"
    return templates.TemplateResponse(
        "conta/carteira.html", { "request": request,
                            "mensagem":mensagem,
                            "usuario": usuario,
                            "pagina": pagina,
                          }
    )

@router.get("/metas")
async def getTrans(request: Request):
    mensagem = "Metas"
    usuario = ""
    pagina = "/metas"
    return templates.TemplateResponse(
        "metas/metas.html", { "request": request,
                            "mensagem":mensagem,
                            "usuario": usuario,
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
        "main/configuracoes.html", { "request": request,
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