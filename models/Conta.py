from dataclasses import asdict, dataclass

from models.Usuario import Usuario


@dataclass
class Conta:
    idConta: int
    usuario: Usuario
    titulo: str
    saldo: float
    meta: str | None = None
