from typing import Annotated
from fastapi import FastAPI, Form, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn

from repositories.ContaRepo import ContaRepo
from repositories.UsuarioRepo import UsuarioRepo

from routes.MainRouter import router as mainRouter
from routes.UsuarioRouter import router as UsuarioRouter
from routes.ContaRouter import router as ContaRouter


UsuarioRepo.criarTabela()
ContaRepo.criarTabela()

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

## Conta *Não implementado*

- Inserir novas contas
- Consultar todos as contas
- Consultar os dados de uma única conta
- Alterar os dados de uma conta *Está retornando um erro*
- Excluir alguma conta
- Excluir todas as contas

## Categoria *Não implementado*

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

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)

# ! Vai sumir tudo que está daqui pra baixo.

# monta um diretório para servir de templates de páginas
templates = Jinja2Templates(directory="templates")


@app.get("/formReceita", response_class=HTMLResponse)
async def getHome(request: Request):
    activeDash = "active"
    titulo = "Formulário"
    return templates.TemplateResponse(
        "formReceita.html",
        {"request": request, "activeDash": activeDash, "titulo": titulo},
    )


@app.get("/formDespesa", response_class=HTMLResponse)
async def getHome(request: Request):
    activeDash = "active"
    titulo = "Formulário"
    return templates.TemplateResponse(
        "formDespesa.html",
        {"request": request, "activeDash": activeDash, "titulo": titulo},
    )


@app.get("/formCartao", response_class=HTMLResponse)
async def getHome(request: Request):
    return templates.TemplateResponse("formCartao.html", {"request": request})


@app.get("/formMeta", response_class=HTMLResponse)
async def getHome(request: Request):
    return templates.TemplateResponse("formMeta.html", {"request": request})


@app.get("/base", response_class=HTMLResponse)
async def getHome(request: Request):
    return templates.TemplateResponse("base.html", {"request": request})


@app.post("/criarConta", response_class=HTMLResponse)
async def postCriarConta(
    titulo: Annotated[str, Form()],
    saldo: Annotated[str, Form()],
    meta: Annotated[str, Form()],
):
    ContaRepo.inserir(titulo, saldo, meta)
    return RedirectResponse(status_code=status.HTTP_303_SEE_OTHER)


# # rota para login e cadastro
# @app.get("/signUp-signIn", response_class=HTMLResponse)
# async def getLogin(request: Request):
#     return templates.TemplateResponse("signUp-signIn.html",
#                                       {"request": request})


# #cadastro de usuário
# @app.post("/dashboard")
# async def postCadastrarUsuario(name: Annotated[str, Form()],
#                                email: Annotated[str, Form()],
#                                password: Annotated[str, Form()]):
#     UserRepo.insert(User(0, name, email, None, password, None, None, None))


# # rota para recuperar senha
# @app.get("/recuperarSenha", response_class=HTMLResponse)
# async def getRecuperar(request: Request):
#     return templates.TemplateResponse("recuperarSenha.html",
#                                       {"request": request})


# rota para dashboard
@app.get("/dashboard", response_class=HTMLResponse)
async def getDashboard(request: Request):
    activeDash = "active"
    titulo = "Bom dia, Ricardo"

    # TransactionDb = TransactionRepo.getAll()
    # dependentsDb = DependentRepo.getAll()
    # categoryDb = CategoryRepo.getAll()
    # accountDb = AccountRepo.getAll()

    # receita = 0
    # despesa = 0
    # lista_categoria_despesa = []
    # for t in TransactionDb:
    #     if t.typeIorE == "Receita":
    #         receita += t.value
    #         t.value = format_currency(t.value, 'BRL', locale='pt_BR')
    #     else:
    #         despesa += t.value
    #         lista_categoria_despesa.append(t.idCategory)
    #         t.value = format_currency(t.value, 'BRL', locale='pt_BR')
    # saldo = receita - despesa

    # receita = format_currency(receita, 'BRL', locale='pt_BR')
    # saldo = format_currency(saldo, 'BRL', locale='pt_BR')
    # despesa = format_currency(despesa, 'BRL', locale='pt_BR')

    return templates.TemplateResponse(
        "dashboard.html",
        {
            "request": request,
            "titulo": titulo,
            "activeDash": activeDash,
            # "transactions": TransactionDb,
            # "dependents": dependentsDb,
            # "categories": categoryDb,
            # "account": accountDb,
            # "saldo": saldo,
            # "receita": receita,
            # "despesa": despesa,
            # "lista_despesa": lista_categoria_despesa
        },
    )


# rota para transações
@app.get("/transacoes", response_class=HTMLResponse)
async def getTransacoes(request: Request):
    activeTran = "active"
    titulo = "Transações"

    # TransactionDb = TransactionRepo.getAll()
    # qtdeTransacoes = len(TransactionDb)

    # receita = 0
    # despesa = 0
    # for t in TransactionDb:
    #     date_string = t.date
    #     date_object = datetime.strptime(date_string, "%Y-%m-%d")
    #     date_formated = date_object.strftime("%d/%m/%Y")
    #     t.date = date_formated

    #     if t.typeIorE == "Receita":
    #         receita += t.value
    #         t.value = format_currency(t.value, 'BRL', locale='pt_BR')
    #     else:
    #         despesa += t.value
    #         t.value = format_currency(t.value, 'BRL', locale='pt_BR')
    # saldo = receita - despesa

    # receita = format_currency(receita, 'BRL', locale='pt_BR')
    # saldo = format_currency(saldo, 'BRL', locale='pt_BR')
    # despesa = format_currency(despesa, 'BRL', locale='pt_BR')

    return templates.TemplateResponse(
        "transacoes.html",
        {
            "request": request,
            "titulo": titulo,
            "activeTran": activeTran,
            # "transactions": TransactionDb,
            # "qtdeTransacoes": qtdeTransacoes,
            # "receita": receita,
            # "despesa": despesa,
            # "saldo": saldo
        },
    )


# #Excluir transação
# @app.post("/excluirTransacao")
# async def postExcluirTransacao(idTransaction: Annotated[str, Form()]):
#     TransactionRepo.delete(idTransaction)
#     return RedirectResponse("/transacoes",
#                             status_code=status.HTTP_303_SEE_OTHER)


# #Excluir Categoria
# @app.post("/excluirCategoria")
# async def postExcluirCategoria(idCategory: Annotated[str, Form()]):
#     CategoryRepo.delete(idCategory)
#     return RedirectResponse("/configuracoes",
#                             status_code=status.HTTP_303_SEE_OTHER)


# #Excluir Conta
# @app.post("/excluirConta")
# async def postExcluirCategoria(idAccount: Annotated[str, Form()]):
#     AccountRepo.delete(idAccount)
#     return RedirectResponse("/configuracoes",
#                             status_code=status.HTTP_303_SEE_OTHER)


# rota para carteira
@app.get("/carteira", response_class=HTMLResponse)
async def getCarteira(request: Request):
    activeCart = "active"
    titulo = "Carteira"
    return templates.TemplateResponse(
        "carteira.html",
        {"request": request, "titulo": titulo, "activeCart": activeCart},
    )


# # rota para metas
# @app.get("/metas", response_class=HTMLResponse)
# async def getMetas(request: Request):
#     activeMeta = "sidebar-active"
#     titulo = "Metas"
#     return templates.TemplateResponse("metas.html", {
#         "request": request,
#         "titulo": titulo,
#         "activeMeta": activeMeta
#     })


# # rota para configurações
# @app.get("/configuracoes", response_class=HTMLResponse)
# async def getConfig(request: Request):
#     activeConfig = "sidebar-active"
#     titulo = "Configurações"

#     categoryDb = CategoryRepo.getAll()

#     accountDb = AccountRepo.getAll()

#     return templates.TemplateResponse(
#         "configuracoes.html", {
#             "request": request,
#             "titulo": titulo,
#             "activeConfig": activeConfig,
#             "categories": categoryDb,
#             "account": accountDb
#         })


# # Formulários do dashboard
# @app.post("/cadastrarReceita")
# async def postCadastrarReceita(
#         request: Request, description: Annotated[str, Form()],
#         value: Annotated[str, Form()], idAccount: Annotated[str, Form()],
#         idMembro: Annotated[str, Form()], date: Annotated[str, Form()],
#         idCategoria: Annotated[str, Form()],
#         payment: Annotated[str, Form()]):  # não tem na tabela
#     TransactionRepo.createTable()
#     TransactionRepo.insert(
#         Transaction(0, 1, idCategoria, idAccount, idMembro, description, date,
#                     value, "Receita"))
#     return RedirectResponse("/transacoes",
#                             status_code=status.HTTP_303_SEE_OTHER)


# @app.post("/cadastrarDespesa")
# async def postCadastrarDespesa(
#         request: Request, description: Annotated[str, Form()],
#         value: Annotated[str, Form()], idAccount: Annotated[str, Form()],
#         idMembro: Annotated[str, Form()], date: Annotated[str, Form()],
#         idCategoria: Annotated[str, Form()],
#         payment: Annotated[str, Form()]):  # não tem na tabela
#     TransactionRepo.createTable()
#     TransactionRepo.insert(
#         Transaction(0, 1, idCategoria, idAccount, idMembro, description, date,
#                     value, "Despesa"))
#     return RedirectResponse("/transacoes",
#                             status_code=status.HTTP_303_SEE_OTHER)


# # formulários de configurações
# @app.post("/cadastrarDependente")
# async def postCadastrarDependente(name: Annotated[str, Form()],
#                                   description: Annotated[str, Form()]):
#     DependentRepo.insert(Dependent(0, 1, name, description, "red"))
#     return RedirectResponse("/configuracoes",
#                             status_code=status.HTTP_303_SEE_OTHER)


# @app.post("/cadastrarCategoria")
# async def postCadastrarCategoria(name: Annotated[str, Form()]):
#     CategoryRepo.insert(Category(0, 1, name, 0, "red", 0, True))
#     return RedirectResponse("/configuracoes",
#                             status_code=status.HTTP_303_SEE_OTHER)


# @app.post("/cadastrarConta")
# async def postCadastrarCartao(title: Annotated[str, Form()],
#                               balance: Annotated[str, Form()],
#                               goal: Annotated[str, Form()]):
#     AccountRepo.createTable()
#     AccountRepo.insert(Account(0, 1, title, balance, goal))
#     return RedirectResponse("/configuracoes",
#                             status_code=status.HTTP_303_SEE_OTHER)
