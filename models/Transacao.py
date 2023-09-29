from datetime import date
from dataclasses import dataclass

@dataclass
class Transacao():
    id: int
    conta: str | None = None
    dependente: str | None = None
    categoria: str | None = None
    descricao: str | None = None
    data: date | None = None
    valor: float | None = None
    forma_pagamento: str | None = None
    tipo: str | None = None
