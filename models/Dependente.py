from dataclasses import dataclass

from models.Usuario import Usuario


@dataclass
class Dependente:
    id: int
    idUsuario: Usuario
    nome: str
