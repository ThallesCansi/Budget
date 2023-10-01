from dataclasses import dataclass

from models.Usuario import Usuario


@dataclass
class Categoria:
    id: int
    idUsuario: Usuario
    nome: str
