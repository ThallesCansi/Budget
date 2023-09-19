from dataclasses import dataclass

from models.Usuario import Usuario


@dataclass
class Categoria:
    idCategoria: int
    usuario: Usuario
    nome: str
    limite: float | None = None
    cor: str | None = None
    tipo: str | None = None
