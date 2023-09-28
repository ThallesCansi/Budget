import secrets
import bcrypt
from fastapi import Request
from models.Usuario import Usuario
from repositories.UsuarioRepo import UsuarioRepo

def validar_usuario_logado(request: Request) -> Usuario | bool:
    try:
        token = request.cookies["auth_token"]
        if token.strip() == "":
            return None
        usuario = UsuarioRepo.obterUsuarioPorToken(token)
        return usuario
    except KeyError:
        return None

def obter_hash_senha(senha: str) -> str:
    hashed = bcrypt.hashpw(senha.encode(), bcrypt.gensalt())
    return hashed.decode()

def verificar_senha(senha: str, hash_senha: str) -> bool:
    try:
        return bcrypt.checkpw(senha.encode(), hash_senha.encode())
    except ValueError:
        return False

def gerar_token(tamanho: int = 32) -> str:
    return secrets.token_hex(tamanho)
