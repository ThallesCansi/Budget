from pydantic import BaseModel
from datetime import date

from models.Conta import Conta
from models.Usuario import Usuario
from models.Dependente import Dependente

class Transacao(BaseModel):
    idTransacao: int
    usuario: Usuario
    conta: Conta
    dependente: Dependente
    descricao: str
    data: date
    valor: float
    tipo: str
