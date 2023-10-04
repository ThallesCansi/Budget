from dataclasses import dataclass


@dataclass
class Categoria:
    id: int
    idUsuario: int | None = None
    nome: str | None = None
    tipo: str | None = None
