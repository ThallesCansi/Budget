from babel.dates import format_datetime, get_month_names
from datetime import datetime
from fastapi import APIRouter, Depends, Form, Path, Request, status
from fastapi.responses import JSONResponse, RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates

from models.Usuario import Usuario
from repositories.UsuarioRepo import UsuarioRepo
from utils.seguranca import gerar_token, validar_usuario_logado
from utils.templateFilters import formatarData


router = APIRouter()

templates = Jinja2Templates(directory="templates")


@router.on_event("startup")
async def startup_event():
    templates.env.filters["date"] = formatarData


@router.get("/entrar", tags=["Usuário"], summary="Ir para a página de acesso ao sistema.", response_class=HTMLResponse)
async def getEntrar(request: Request, logado: bool = Depends(validar_usuario_logado)):
    if logado:
        return RedirectResponse("/dashboard", status.HTTP_302_FOUND)
    else:
        return templates.TemplateResponse("usuario/entrar.html", {"request": request})


@router.post("/entrar", tags=["Usuário"], summary="Entrar no sistema através de e-mail e senha.", response_class=HTMLResponse)
async def postEntrar(request: Request, email: str = Form(...), senha: str = Form(...)):
    usuario = UsuarioRepo.obterPorEmail(email)
    if usuario:
        if email != usuario.email or senha != usuario.senha:
            mensagem_erro_entrar = "E-mail ou senha inválidos. Tente novamente."
            return templates.TemplateResponse("usuario/entrar.html", {"request": request, "mensagem_erro_entrar": mensagem_erro_entrar})
        else:
            token = gerar_token()
            UsuarioRepo.inserirToken(email, token)
            response = RedirectResponse("/dashboard", status.HTTP_302_FOUND)
            response.set_cookie(key="auth_token", value=token, max_age=1800, httponly=True)
            return response
    else:
        mensagem_erro_entrar = "Parece que você ainda não se cadastrou no Budget."
        return templates.TemplateResponse("usuario/entrar.html", {"request": request, "mensagem_erro_entrar": mensagem_erro_entrar})


@router.post("/novousuario", tags=["Usuário"], summary="Inserir um novo usuário ao sistema.", response_class=HTMLResponse)
async def postNovoUsuario(request: Request, nome: str = Form(...), email: str = Form(...), senha: str = Form()):
    usuario = UsuarioRepo.obterPorEmail(email)
    if usuario:
        mensagem_erro_cadastrar = "Este e-mail já está em uso."
        return templates.TemplateResponse("usuario/entrar.html", {"request": request, "mensagem_erro_cadastrar": mensagem_erro_cadastrar})
    else:
        UsuarioRepo.inserir(Usuario(0, nome, email, senha))
        token = gerar_token()
        UsuarioRepo.inserirToken(email, token)
        response = RedirectResponse("/dashboard", status.HTTP_302_FOUND)
        response.set_cookie(key="auth_token", value=token, max_age=1800, httponly=True)
        return response


@router.get("/dashboard", tags=["Usuário"], summary="Visualizar o dashboard do sistema.", response_class=HTMLResponse)
async def getDashboard(request: Request, logado: bool = Depends(validar_usuario_logado)):
    pagina = "/dashboard"
    hora = datetime.now().hour
    if 6 <= hora <= 12:
        mensagem = "Bom dia, "
    elif hora <= 18:
        mensagem = "Boa tarde, "
    else:
        mensagem = "Boa noite, "
        
    if logado:
        token = request.cookies.values().mapping["auth_token"]
        usuario = UsuarioRepo.obterPorToken(token)
        data_hora = format_datetime(datetime.now(), format="short", locale='pt_BR').title()
        meses = get_month_names("wide", locale="pt_BR")
        return templates.TemplateResponse("usuario/dashboard.html", {"request": request, "mensagem": mensagem, "pagina": pagina, "usuario": usuario, "data_hora": data_hora, "meses": meses})
    else:
        return RedirectResponse("/entrar", status.HTTP_302_FOUND)

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
    "/atualizarusuario",
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
