from dataclasses import dataclass


@dataclass
class Conta:
    id: int
    idUsuario: int
    nome: str
    saldo: float
    meta: str | None = None
