from babel.dates import format_datetime, get_month_names
from datetime import datetime
from fastapi import APIRouter, Depends, Form, HTTPException, Request, status
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from models.Transacao import Transacao

from models.Usuario import Usuario
from repositories.TransacaoRepo import TransacaoRepo
from repositories.UsuarioRepo import UsuarioRepo
from util.seguranca import gerar_token, obter_hash_senha, validar_usuario_logado
from util.templateFilters import capitalizar_nome_proprio, formatarData
from util.validators import *


router = APIRouter()

templates = Jinja2Templates(directory="templates")


@router.on_event("startup")
async def startup_event():
    templates.env.filters["date"] = formatarData


@router.post(
    "/novousuario",
    tags=["Usuário"],
    summary="Inserir um novo usuário ao sistema.",
    response_class=HTMLResponse,
)
async def postNovoUsuario(
    request: Request,
    usuario: Usuario = Depends(validar_usuario_logado),
    nome: str = Form(""),
    email: str = Form(""),
    senha: str = Form(""),
    confirmarSenha: str = Form(""),
    termoUso: str = Form(""),
):
    nome = capitalizar_nome_proprio(nome).strip()

    email = email.lower().strip()

    senha = senha.strip()

    confirmarSenha = confirmarSenha.strip()

    erros = {}

    is_not_empty(nome, "nome", erros)
    is_person_fullname(nome, "nome", erros)

    is_not_empty(email, "email", erros)
    if is_email(email, "email", erros):
        if UsuarioRepo.emailExiste(email):
            add_error("email", "Já existe um aluno cadastrado com este e-mail.", erros)

    is_not_empty(senha, "senha", erros)
    is_password(senha, "senha", erros)

    is_not_empty(confirmarSenha, "confirmarSenha", erros)
    is_matching_fields(confirmarSenha, "confirmarSenha", senha, "Senha", erros)

    is_not_none(termoUso, "termoUso", erros)

    if len(erros) > 0:
        valores = {}
        valores["nome"] = nome
        valores["email"] = email.lower()
        return templates.TemplateResponse(
            "usuario/entrar.html",
            {
                "request": request,
                "usuario": usuario,
                "erros": erros,
                "valores": valores,
            },
        )

    UsuarioRepo.inserir(
        Usuario(
            id=0,
            nome=nome,
            email=email,
            senha=obter_hash_senha(senha),
        )
    )
    token = gerar_token()
    UsuarioRepo.alterarToken(email, token)
    response = RedirectResponse("/dashboard", status.HTTP_302_FOUND)
    response.set_cookie(key="auth_token", value=token, max_age=1800, httponly=True)
    return response


@router.get(
    "/dashboard",
    tags=["Usuário"],
    summary="Visualizar o dashboard do sistema.",
    response_class=HTMLResponse,
)
async def getDashboard(
    request: Request, usuario: Usuario = Depends(validar_usuario_logado)
):
    pagina = "/dashboard"
    hora = datetime.now().hour
    if 6 <= hora <= 12:
        mensagem = "Bom dia, "
    elif hora <= 18:
        mensagem = "Boa tarde, "
    else:
        mensagem = "Boa noite, "

    if usuario:
        usuario = UsuarioRepo.obterPorId(usuario.id)
        if usuario:
            data_hora = format_datetime(
                datetime.now(), format="short", locale="pt_BR"
            ).title()
            meses = get_month_names("wide", locale="pt_BR")
            return templates.TemplateResponse(
                "usuario/dashboard.html",
                {
                    "request": request,
                    "usuario": usuario,
                    "mensagem": mensagem,
                    "pagina": pagina,
                    "data_hora": data_hora,
                    "meses": meses,
                },
            )
        else:
            return RedirectResponse("/entrar", status_code=status.HTTP_303_SEE_OTHER)
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)


@router.get("/recuperarSenha")
async def getRecuperar(request: Request):
    return templates.TemplateResponse(
        "usuario/recuperarSenha.html",
        {
            "request": request,
        },
    )


@router.post(
    "/receita",
    tags=["Usuário"],
    summary="Adicionar uma receita",
    response_class=HTMLResponse,
)
async def postReceita(
    request: Request,
    descricao: str = Form(""),
    valor: float = Form(""),
    conta: str = "Inter",
    dependente: str = "Nenhum",
    data: str = Form(""),
    categoria: str = "Venda",
    forma_pagamento: str = "PIX",
    usuario: Usuario = Depends(validar_usuario_logado),
):
    if usuario:
        TransacaoRepo.inserir(
            Transacao(0, 1, 1, 1, 1, descricao, data, valor, forma_pagamento, "Receita")
        )
        return RedirectResponse("/dashboard", status_code=status.HTTP_303_SEE_OTHER)
