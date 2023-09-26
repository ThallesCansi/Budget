from fastapi import APIRouter, Form, Path, Request, status
from fastapi.responses import JSONResponse, RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates

from models.Usuario import Usuario
from repositories.UsuarioRepo import UsuarioRepo
from utils.templateFilters import formatarData


router = APIRouter()

templates = Jinja2Templates(directory="templates")


@router.on_event("startup")
async def startup_event():
    templates.env.filters["date"] = formatarData


@router.get("/entrar", tags=["Usuário"], summary="Ir para a página de acesso ao sistema.", response_class=HTMLResponse)
async def getEntrar(request: Request): # ! COLOCAR A DEPENDÊNCIA PARA VERIFICAR SE JÁ ESTÁ LOGADO
    return templates.TemplateResponse("entrar.html", {"request": request})


@router.post("/entrar", tags=["Usuário"], summary="Entrar no sistema através de e-mail e senha.", response_class=HTMLResponse)
async def postEntrar(request: Request, email: str = Form(...), senha: str = Form(...)):
    usuario = UsuarioRepo.obterPorEmail(email) # ! CRIAR FUNÇÃO PARA PESQUISAR O USUÁRIO COM BASE NO E-MAIL DELE DO FORMULÁRIO
    if usuario == []:
        mensagem_erro = "Parece que você ainda não se cadastrou no Budget."
        return templates.TemplateResponse("participante/entrar.html", {"request": request, "mensagem_erro": mensagem_erro})
    else:
        if email != usuario.email or senha != usuario.senha:
            mensagem_erro = "E-mail ou senha inválidos. Tente novamente."
            return templates.TemplateResponse("participante/entrar.html", {"request": request, "mensagem_erro": mensagem_erro})
        else:
            return RedirectResponse("/dashboard", status.HTTP_302_FOUND)




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
