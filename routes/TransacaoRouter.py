from fastapi import APIRouter, Depends, Form, HTTPException, Query, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from models.Transacao import Transacao
from models.Usuario import Usuario
from repositories.TransacaoRepo import TransacaoRepo
from repositories.UsuarioRepo import UsuarioRepo
from util.seguranca import validar_usuario_logado
from util.templateFilters import formatar_data
from util.validators import *

router = APIRouter(prefix="/transacao")

templates = Jinja2Templates(directory="templates")


@router.on_event("startup")
async def startup_event():
    templates.env.filters["date"] = formatar_data


@router.get(
    "/listagem",
    tags=["Transações"],
    summary="Exibir a listagem das transações da tabela.",
    response_class=HTMLResponse,
)
async def getListagem(
    request: Request,
    mensagem="Transações",
    pagina = "/transacoes",
    usuario: Usuario = Depends(validar_usuario_logado),
):
    if usuario:
        transacoes = TransacaoRepo.obterTransacaoPorUsuario(usuario.id)
        receita = TransacaoRepo.obterReceita(usuario.id)
        despesa = TransacaoRepo.obterDespesa(usuario.id)
        saldo = TransacaoRepo.obterSaldo(usuario.id)
        return templates.TemplateResponse(
            "transacoes/transacoes.html",
            {
                "request": request,
                "transacoes": transacoes,
                "receita": receita,
                "despesa": despesa,
                "saldo": saldo,
                "mensagem": mensagem,
                "pagina": pagina,
                "usuario": usuario,
            },
        )
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)




@router.post(
    "/adicionar",
    tags=["Transação"],
    summary="Adicionar uma transação à tabela para um usuário do sistema.",
    response_class=HTMLResponse,
)
async def postReceita(
    request: Request,
    descricao: str = Form(""),
    valor: float = Form(""),
    idConta: str = Form(""),
    idDependente: str = Form(""),
    data: str = Form(""),
    idCategoria: str = Form(),
    forma_pagamento: str = Form(""),
    tipo: str = Query(...),
    usuario: Usuario = Depends(validar_usuario_logado),
):
    if usuario:
        descricao = descricao.strip()

        erros = {}

        is_not_empty(descricao, "descricao", erros)
        is_size_between(descricao, "descricao", 4, 64, erros)

        is_not_none(valor, "valor", erros)

        is_not_empty(idConta, "conta", erros)

        is_not_empty(idDependente, "dependente", erros)

        is_not_empty(formatar_data(data), "data", erros)
        is_date(formatar_data(data), "data", erros)

        is_not_empty(idCategoria, "categoria", erros)

        is_not_empty(forma_pagamento, "forma_pagamento", erros)

        if tipo == "Receita":
            valor = abs(float(valor))
        else:
            valor == float(-valor)

        if len(erros) > 0:
            print(erros)
            valores = {}
            valores["descricao"] = descricao
            valores["valor"] = valor
            valores["idConta"] = idConta
            valores["idDependente"] = idDependente
            valores["data"] = data
            valores["idCategoria"] = idCategoria
            valores["forma_pagamento"] = forma_pagamento
            return templates.TemplateResponse(
                "usuario/dashboard.html",
                {
                    "request": request,
                    "usuario": usuario,
                    "erros": erros,
                    "valores": valores,
                },
            )

        TransacaoRepo.inserir(
            Transacao(
                0,
                idConta,
                idCategoria,
                idDependente,
                usuario.id,
                descricao,
                data,
                valor,
                forma_pagamento,
                tipo,
            )
        )
        return RedirectResponse("/dashboard", status_code=status.HTTP_303_SEE_OTHER)
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
