from typing import Annotated
from fastapi import FastAPI, Request, Form, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from CategoryRepo import CategoryRepo
from User import User
from UserRepo import UserRepo
from TransactionRepo import TransactionRepo
from Transaction import Transaction
from DependentRepo import DependentRepo
from Dependent import Dependent

# habilita a aplicação a responder por resquisições HTTP
app = FastAPI()

# monta um diretório para servir arquivos estáticos via HTTP
app.mount("/static", StaticFiles(directory="static", html=True), name="static")

# monta um diretório para servir de templates de páginas
templates = Jinja2Templates(directory="templates")


@app.get("/base", response_class=HTMLResponse)
async def getHome(request: Request):
    return templates.TemplateResponse("base.html", {"request": request})

# rota para login e cadastro


@app.get("/signUp-signIn", response_class=HTMLResponse)
async def getLogin(request: Request):
    return templates.TemplateResponse("signUp-signIn.html", {"request": request})

# rota para recuperar senha


@app.get("/recuperarSenha", response_class=HTMLResponse)
async def getRecuperar(request: Request):
    return templates.TemplateResponse("recuperarSenha.html", {"request": request})

# rota para dashboard


@app.get("/dashboard", response_class=HTMLResponse)
async def getDashboard(request: Request):
    activeDash = "sidebar-active"
    titulo = "Bom dia, Ricardo"
    dependentsDb = DependentRepo.getAll()
    categoryDb = CategoryRepo.getAll()
    return templates.TemplateResponse("dashboard.html", {"request": request, "titulo": titulo, "activeDash": activeDash, "dependents": dependentsDb, "categories": categoryDb})

# rota para transações


@app.get("/transacoes", response_class=HTMLResponse)
async def getTransacoes(request: Request):
    activeTran = "sidebar-active"
    titulo = "Transações"

    TransactionDb = TransactionRepo.getAll()

    qtdeTransacoes = len(TransactionDb)

    return templates.TemplateResponse("transacoes.html", {"request": request, "titulo": titulo, "transactions": TransactionDb, "activeTran": activeTran, "qtdeTransacoes": qtdeTransacoes})

# rota para carteira


@app.get("/carteira", response_class=HTMLResponse)
async def getCarteira(request: Request):
    activeCart = "sidebar-active"
    titulo = "Carteira"
    return templates.TemplateResponse("carteira.html", {"request": request, "titulo": titulo, "activeCart": activeCart})

# rota para metas


@app.get("/metas", response_class=HTMLResponse)
async def getMetas(request: Request):
    activeMeta = "sidebar-active"
    titulo = "Metas"
    return templates.TemplateResponse("metas.html", {"request": request, "titulo": titulo, "activeMeta": activeMeta})

# rota para configurações


@app.get("/configuracoes", response_class=HTMLResponse)
async def getConfig(request: Request):
    activeConfig = "sidebar-active"
    titulo = "Configurações"
    return templates.TemplateResponse("configuracoes.html", {"request": request, "titulo": titulo, "activeConfig": activeConfig})

# Formulários do dashboard


@app.post("/cadastrarReceita")
async def postCadastrarReceita(request: Request,
                               description: Annotated[str, Form()],
                               value: Annotated[str, Form()],
                               idConta: Annotated[str, Form()],
                               idMembro: Annotated[str, Form()],
                               date: Annotated[str, Form()],
                               idCategoria: Annotated[str, Form()],
                               payment: Annotated[str, Form()]):  # não tem na tabela
    TransactionRepo.createTable()
    TransactionRepo.insert(Transaction(
        0, 0, idCategoria, idConta, idMembro, description, date, value, "Receita"))
    return RedirectResponse("/transacoes", status_code=status.HTTP_303_SEE_OTHER)


@app.post("/cadastrarDespesa")
async def postCadastrarDespesa(
        description: Annotated[str, Form()],
        value: Annotated[str, Form()],
        idConta: Annotated[str, Form()],
        idMembro: Annotated[str, Form()],
        date: Annotated[str, Form()],
        idCategoria: Annotated[str, Form()],
        payment: Annotated[str, Form()]):  # não tem na tabela
    TransactionRepo.insert(Transaction(
        2, 2, idCategoria, idConta, idMembro, description, date, value, "Despesa"))
    return RedirectResponse("/transacoes", status_code=status.HTTP_303_SEE_OTHER)

# formulários de configurações


@app.post("/cadastrarDependente")
async def postCadastrarDependente(
        name: Annotated[str, Form()],
        description: Annotated[str, Form()]):
    DependentRepo.insert(Dependent(1, 1, name, description, "red"))
    return RedirectResponse("/configuracoes", status_code=status.HTTP_303_SEE_OTHER)


@app.get("/dependentes", response_class=HTMLResponse)
async def getDependente(request: Request):
    return templates.TemplateResponse("configuracoes.html", {"request": request})


@app.post("/dashboard")
async def postCadastrarUsuario(
        name: Annotated[str, Form()],
        email: Annotated[str, Form()],
        password: Annotated[str, Form()]):
    UserRepo.insert(User(0, name, email, None, password, None, None, None))

# Terminar o Banco de Cartão
# @app.post("/cadastrarCartao")
# async def postCadastrarCartao(
#     description: Annotated[str, Form()],
#     value: Annotated[str, Form()],
#     idConta: Annotated[str, Form()],
#     idMembro: Annotated[str, Form()],
#     date: Annotated[str, Form()],
#     idCategoria: Annotated[str, Form()],
#     payment: Annotated[str, Form()]):
#     TransactionRepo.insert(Transaction (2, 2, idCategoria, idConta, idMembro, description, date, value, payment))
