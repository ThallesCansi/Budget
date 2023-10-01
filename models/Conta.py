from dataclasses import dataclass


@dataclass
class Conta:
    id: int
    idUsuario: int
    titulo: str
    saldo: float
    meta: str | None = None
