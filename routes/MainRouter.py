from fastapi.templating import Jinja2Templates
from fastapi.responses import JSONResponse, RedirectResponse, HTMLResponse
from models.Usuario import Usuario
from repositories.ContaRepo import ContaRepo
from repositories.UsuarioRepo import UsuarioRepo


from fastapi import APIRouter, Depends, Form, HTTPException, Query, Request, status
from fastapi.templating import Jinja2Templates
from util.seguranca import gerar_token, validar_usuario_logado, verificar_senha

from util.templateFilters import formatar_data
from util.validators import *

router = APIRouter()

templates = Jinja2Templates(directory="templates")


@router.on_event("startup")
async def startup_event():
    templates.env.filters["date"] = formatar_data


@router.get("/")
async def getIndex(request: Request):
    return templates.TemplateResponse(
        "main/index.html",
        {
            "request": request,
        },
    )


@router.get(
    "/entrar",
    tags=["Usuário"],
    summary="Ir para a página de acesso ao sistema.",
    response_class=HTMLResponse,
)
async def getEntrar(request: Request, logado: bool = Depends(validar_usuario_logado)):
    if logado:
        return RedirectResponse("/dashboard", status.HTTP_302_FOUND)
    else:
        return templates.TemplateResponse("usuario/entrar.html", {"request": request})


@router.post(
    "/entrar",
    tags=["Usuário"],
    summary="Entrar no sistema através de e-mail e senha.",
    response_class=HTMLResponse,
)
async def postEntrar(
    request: Request,
    usuario: Usuario = Depends(validar_usuario_logado),
    emailLogin: str = Form(""),
    senhaLogin: str = Form(""),
    returnUrl: str = Query("/dashboard"),
):
    # normalização de dados
    emailLogin = emailLogin.strip().lower()
    senhaLogin = senhaLogin.strip()

    # validação de dados
    erros = {}
    # validação do campo email
    is_not_empty(emailLogin, "emailLogin", erros)
    is_email(emailLogin, "emailLogin", erros)
    # validação do campo senha
    is_not_empty(senhaLogin, "senhaLogin", erros)

    # só checa a senha no BD se os dados forem válidos
    if len(erros) == 0:
        hash_senha_bd = UsuarioRepo.obterSenhaDeEmail(emailLogin)
        if hash_senha_bd:
            if verificar_senha(senhaLogin, hash_senha_bd):
                token = gerar_token()
                if UsuarioRepo.alterarToken(emailLogin, token):
                    response = RedirectResponse(returnUrl, status.HTTP_302_FOUND)
                    response.set_cookie(
                        key="auth_token", value=token, max_age=1800, httponly=True
                    )
                    return response
                else:
                    raise Exception(
                        "Não foi possível alterar o token do usuário no banco de dados."
                    )
            else:
                add_error("senhaLogin", "Senha não confere.", erros)
        else:
            add_error("emailLogin", "Usuário não cadastrado.", erros)

    # se tem algum erro, mostra o formulário novamente
    if len(erros) > 0:
        valores = {}
        valores["emailLogin"] = emailLogin
        return templates.TemplateResponse(
            "usuario/entrar.html",
            {
                "request": request,
                "usuario": usuario,
                "erros": erros,
                "valores": valores,
            },
        )


@router.get("/sair")
async def getSair(request: Request, usuario: Usuario = Depends(validar_usuario_logado)):
    if usuario:
        UsuarioRepo.alterarToken(usuario.email, "")
        response = RedirectResponse("/entrar", status.HTTP_302_FOUND)
        response.set_cookie(
            key="auth_token", value="", httponly=True, expires="1970-01-01T00:00:00Z"
        )
        return response
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)


@router.get("/carteira")
async def getTrans(request: Request, usuario: Usuario = Depends(validar_usuario_logado)):
    if usuario:
        mensagem = "Carteira"
        usuario = ""
        pagina = "/carteira"
        return templates.TemplateResponse(
            "conta/carteira.html",
            {
                "request": request,
                "mensagem": mensagem,
                "usuario": usuario,
                "pagina": pagina,
            },
        )
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)


@router.get("/metas")
async def getTrans(request: Request, usuario: Usuario = Depends(validar_usuario_logado)):
    if usuario:
        mensagem = "Metas"
        usuario = ""
        pagina = "/metas"
        return templates.TemplateResponse(
            "metas/metas.html",
            {
                "request": request,
                "mensagem": mensagem,
                "usuario": usuario,
                "pagina": pagina,
            },
        )
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)


@router.get("/configuracoes")
async def getConfig(request: Request, usuario: Usuario = Depends(validar_usuario_logado)):
    if usuario:
        mensagem = "Configurações"
        pagina = "/configuracoes"
        contas = ContaRepo.obterContaPorUsuario(usuario.id)
        return templates.TemplateResponse(
            "main/configuracoes.html",
            {
                "request": request,
                "mensagem": mensagem,
                "usuario": usuario,
                "pagina": pagina,
                "contas": contas,
            },
        )
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)


@router.get("/dependentes")
async def getIndex(request: Request, usuario: Usuario = Depends(validar_usuario_logado)):
    if usuario:
        mensagem = "Dependentes"
        usuario = ""
        pagina = "/configuracoes"
        return templates.TemplateResponse(
            "/dependentes/dependente.html",
            {
                "request": request,
                "pagina": pagina,
                "mensagem": mensagem,
                "usuario": usuario,
            },
        )
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
