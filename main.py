from typing import Annotated
from fastapi import FastAPI, Form, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn

from repositories.ContaRepo import ContaRepo
from repositories.UsuarioRepo import UsuarioRepo
from repositories.CategoriaRepo import CategoriaRepo

from routes.MainRouter import router as mainRouter
from routes.UsuarioRouter import router as UsuarioRouter
from routes.ContaRouter import router as ContaRouter
from routes.CategoriaRouter import router as CategoriaRouter


UsuarioRepo.criarTabela()
ContaRepo.criarTabela()
CategoriaRepo.criarTabela()

description = """
# Budget - Realizando o controle de suas finanças. 💸

## Usuário

Esta sessão é responsável por realizar todos os controles que envolve os usuários do sistema.

- Inserir novos usuários
- Consultar todos os usuários
- Consultar os dados de um único usuário
- Alterar os dados de um usuário
- Excluir algum usuário
- Excluir todos os usuários

## Conta

- Inserir novas contas
- Consultar todos as contas
- Consultar os dados de uma única conta
- Alterar os dados de uma conta *Está retornando um erro mas funciona*
- Excluir alguma conta
- Excluir todas as contas

## Categoria

- Inserir novas categorias
- Consultar todos as categorias
- Consultar os dados de uma única categoria
- Alterar os dados de uma categorias
- Excluir alguma categoria
- Excluir todas as categorias

## Dependente *Não implementado*

## Transação *Não implementado*
"""

contact = {
    "name": "Thalles Cansi",
    "e-mail": "thalles_cansi@hotmail.com",
}

license = {
    "name": "Apache 2.0",
    "identifier": "MIT",
}

tags_metadata = [
    {
        "name": "Usuário",
        "description": "Operações com os Usuários",
    },
    {
        "name": "Conta",
        "description": "Operações com as Contas",
    },
    {
        "name": "Categoria",
        "description": "Operações com as Categorias",
    },
]

app = FastAPI(
    title="Budget",
    description=description,
    version="2.0.0",
    contact=contact,
    license_info=license,
    openapi_tags=tags_metadata,
)

app.mount("/static", StaticFiles(directory="static", html=True), name="static")

app.include_router(mainRouter)
app.include_router(UsuarioRouter)
app.include_router(ContaRouter)
app.include_router(CategoriaRouter)

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True, host="0.0.0.0", port=80)


