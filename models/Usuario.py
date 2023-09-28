from dataclasses import dataclass
from typing import Optional


@dataclass
class Usuario:
    id: int
    nome: str
    email: str
    senha:  Optional[str] = ""
    token: Optional[str] = ""
