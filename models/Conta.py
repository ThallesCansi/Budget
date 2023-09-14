from pydantic import BaseModel

from models.Usuario import Usuario


class Conta(BaseModel):
    idConta: int
    usuario: Usuario
    titulo: str
    saldo: float
    meta: str
