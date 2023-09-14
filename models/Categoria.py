from datetime import date
from typing import Optional
from pydantic import BaseModel

from models.Usuario import Usuario

class Categoria(BaseModel):
    idCategoria: int
    usuario: Usuario
    nome: str
    limite: float
    cor: str
    tipo: str
