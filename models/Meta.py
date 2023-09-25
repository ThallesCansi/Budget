from dataclasses import dataclass
from datetime import date

from models.Usuario import Usuario


@dataclass
class Meta:
    idMeta: int
    usuario: Usuario
    nome: str
    valor: float | None = None
    valorinicial: float | None = None
    data: date | None = None
    descricao: str | None = None
    cor: str | None = None
