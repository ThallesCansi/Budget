from typing import Annotated
from fastapi import FastAPI, Request, Form, status
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
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

# rota para /Entrar
@app.get("/base", response_class=HTMLResponse)
async def getHome(request: Request):
    return templates.TemplateResponse("base.html", {"request": request})

@app.get("/signUp-signIn", response_class=HTMLResponse)
async def getLogin(request: Request):
    return templates.TemplateResponse("signUp-signIn.html", {"request": request})

@app.get("/recuperarSenha", response_class=HTMLResponse)
async def getRecuperar(request: Request):
    return templates.TemplateResponse("recuperarSenha.html", {"request": request})

@app.get("/dashboard", response_class=HTMLResponse)
async def getDashboard(request: Request):
    activeDash= "sidebar-active"
    titulo = "Bom dia, Ricardo"
    return templates.TemplateResponse("dashboard.html", {"request": request, "titulo":titulo, "activeDash": activeDash})


@app.get("/transacoes", response_class=HTMLResponse)
async def getTransacoes(request: Request):
    activeTran= "sidebar-active"
    titulo = "Transações"
    
    TransactionDb = TransactionRepo.getAll()
    
    qtdeTransacoes = len(TransactionDb)

    return templates.TemplateResponse("transacoes.html", {"request": request, "titulo": titulo, "transactions": TransactionDb, "activeTran": activeTran, "qtdeTransacoes": qtdeTransacoes})


@app.get("/carteira", response_class=HTMLResponse)
async def getCarteira(request: Request):
    activeCart= "sidebar-active"
    titulo = "Carteira"
    return templates.TemplateResponse("carteira.html", {"request": request, "titulo":titulo, "activeCart": activeCart})

@app.get("/metas", response_class=HTMLResponse)
async def getMetas(request: Request):
    activeMeta= "sidebar-active"
    titulo = "Metas"
    return templates.TemplateResponse("metas.html", {"request": request, "titulo":titulo, "activeMeta": activeMeta})

@app.get("/configuracoes", response_class=HTMLResponse)
async def getConfig(request: Request):
    activeConfig= "sidebar-active"
    titulo = "Configurações"
    return templates.TemplateResponse("configuracoes.html", {"request": request, "titulo":titulo, "activeConfig": activeConfig})



@app.get("/teste", response_class=HTMLResponse)
async def getTeste(request: Request):
    return templates.TemplateResponse("teste.html", {"request": request})


@app.post("/dashboard")
async def postCadastrarProduto(
    name: Annotated[str, Form()], 
    email: Annotated[str, Form()], 
    birth: Annotated[str, Form()],
    password: Annotated[str, Form()],
    phone: Annotated[str, Form()],
    state: Annotated[str, Form()],
    city: Annotated[str, Form()]):
    UserRepo.insert(User (0, name, email, birth, password, phone, state, city))

@app.post("/cadastrarReceita")
async def postCadastrarReceita(
    description: Annotated[str, Form()], 
    value: Annotated[str, Form()], 
    idConta: Annotated[str, Form()],
    idMembro: Annotated[str, Form()],
    date: Annotated[str, Form()],
    idCategoria: Annotated[str, Form()],
    payment: Annotated[str, Form()]):
    TransactionRepo.insert(Transaction (2, 2, idCategoria, idConta, idMembro, description, date, value, payment))

@app.post("/cadastrarDependente")
async def postCadastrarDependente( 
    name: Annotated[str, Form()],
    description: Annotated[str, Form()]):
    DependentRepo.insert(Dependent (1, 1, name, description, "red"))

# Terminar o Banco de Cartão
@app.post("/cadastrarCartao")
async def postCadastrarCartao(
    description: Annotated[str, Form()], 
    value: Annotated[str, Form()], 
    idConta: Annotated[str, Form()],
    idMembro: Annotated[str, Form()],
    date: Annotated[str, Form()],
    idCategoria: Annotated[str, Form()],
    payment: Annotated[str, Form()]):
    TransactionRepo.insert(Transaction (2, 2, idCategoria, idConta, idMembro, description, date, value, payment))