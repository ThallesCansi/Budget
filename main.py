import json
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
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

app.mount("/static", StaticFiles(directory="static", html=True), name="static")

app.include_router(mainRouter)
app.include_router(UsuarioRouter)
app.include_router(ContaRouter)
app.include_router(CategoriaRouter)

if __name__ == "__main__":
    uvicorn.run(app="main:app", reload=True)
