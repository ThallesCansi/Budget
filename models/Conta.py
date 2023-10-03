from dataclasses import dataclass


@dataclass
class Conta:
    id: int
    idUsuario: int
    nome: str
    saldo: float
    descricao: str | None = None
