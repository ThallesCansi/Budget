from datetime import date
from dataclasses import dataclass

@dataclass
class Transacao():
    id: int
    idConta: int | None = None
    idCategoria: int | None = None
    idDependente: int | None = None
    idUsuario: int | None = None
    descricao: str | None = None
    data: date | None = None
    valor: float | None = None
    forma_pagamento: str | None = None
    tipo: str | None = None
    nomeConta: str | None = None
    nomeCategoria: str | None = None
    nomeDependente: str | None = None
