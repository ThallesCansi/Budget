import json
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import uvicorn

from repositories.CategoriaRepo import CategoriaRepo
from repositories.ContaRepo import ContaRepo
from repositories.DependenteRepo import DependenteRepo
from repositories.TransacaoRepo import TransacaoRepo
from repositories.UsuarioRepo import UsuarioRepo
from routes.CategoriaRouter import router as CategoriaRouter
from routes.ContaRouter import router as ContaRouter
from routes.DependenteRouter import router as DependenteRouter
from routes.MainRouter import router as mainRouter
from routes.TransacaoRouter import router as TransacaoRouter
from routes.UsuarioRouter import router as UsuarioRouter
from util.exceptionHandler import configurar as configurarExcecoes

ContaRepo.criarTabela()
CategoriaRepo.criarTabela()
DependenteRepo.criarTabela()
TransacaoRepo.criarTabela()
UsuarioRepo.criarTabela()

with open("project_info.json", "r", encoding="utf-8") as project_info_file:
    project_info = json.load(project_info_file)

app = FastAPI(
    title=project_info["title"],
    description=project_info["description"],
    version=project_info["version"],
    contact=project_info["contact"],
    license_info=project_info["license"],
    openapi_tags=project_info["tags_metadata"],
)

configurarExcecoes(app)

app.mount("/static", StaticFiles(directory="static", html=True), name="static")

app.include_router(mainRouter)
app.include_router(ContaRouter)
app.include_router(CategoriaRouter)
app.include_router(DependenteRouter)
app.include_router(TransacaoRouter)
app.include_router(UsuarioRouter)

if __name__ == "__main__":
    uvicorn.run(app="main:app", reload=True)
