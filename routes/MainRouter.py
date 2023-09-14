from fastapi import APIRouter
from fastapi.templating import Jinja2Templates

from utils.templateFilters import formatarData


router = APIRouter()

templates = Jinja2Templates(directory="templates")


@router.on_event("startup")
async def startup_event():
    templates.env.filters["date"] = formatarData


@router.get("/")
async def root():
    return "<h1>Hello, FastAPI.</h1>"
