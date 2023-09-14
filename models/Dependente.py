from pydantic import BaseModel

from models.Usuario import Usuario

class Dependente(BaseModel):
    idDependente: int
    usuario: Usuario
    nome: str
    descricao: str
    cor: str
