from fastapi import APIRouter, Form, Path
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates

from models.Categoria import Categoria
from models.Usuario import Usuario
from repositories.CategoriaRepo import CategoriaRepo
from util.templateFilters import formatarData



router = APIRouter()

templates = Jinja2Templates(directory="templates")


@router.on_event("startup")
async def startup_event():
    templates.env.filters["date"] = formatarData


@router.post(
    "/novacategoria",
    tags=["Categoria"],
    summary="Nova categoria",
    response_class=JSONResponse,
)
async def postNovaCategoria(
    nome: str = Form(),
    limite: float | None = Form(None),
    cor: str | None = Form(None),
    tipo: str | None = Form(None),
):
    CategoriaRepo.inserir(Categoria(0, Usuario, nome, limite, cor, tipo))
    return {"nome": nome, "limite": limite, "cor": cor, "tipo": tipo}


@router.get(
    "/categorias",
    tags=["Categoria"],
    summary="Consultar categorias",
    response_class=JSONResponse,
)
async def getCategorias():
    categorias = CategoriaRepo.obterTodos()
    return {"categorias": categorias}


@router.get(
    "/categoria/{id}",
    tags=["Categoria"],
    summary="Consultar uma única categoria",
    response_class=JSONResponse,
)
async def getCategoria(id: int = Path(...)):
    categoria = CategoriaRepo.obterPorId(id)
    return {"categoria": categoria}


@router.put(
    "/atualizarcategoria",
    tags=["Categoria"],
    summary="Atualizar categoria",
    response_class=JSONResponse,
)
async def putAtualizarCategoria(
    id: int = Form(),
    nome: str = Form(),
    limite: str | None = Form(None),
    cor: str | None = Form(None),
    tipo: str | None = Form(None),
):
    categoriaAtualizada = CategoriaRepo.alterar(Categoria(id, Categoria, nome, limite, cor, tipo))
    return {"categoriaAtualizada": categoriaAtualizada}


@router.delete(
    "/excluircategoria",
    tags=["Categoria"],
    summary="Excluir categoria",
    response_class=JSONResponse,
)
async def deleteExcluirCategoria(id: int = Form()):
    categoria = CategoriaRepo.excluir(id)
    return {"categoria": categoria}


@router.delete(
    "/excluircategorias",
    tags=["Categoria"],
    summary="Excluir todas as categorias",
    response_class=JSONResponse,
)
async def deleteExcluirCategorias():
    categorias = CategoriaRepo.limparTabela()
    return {"categorias": categorias}
