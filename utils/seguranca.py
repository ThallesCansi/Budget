from fastapi import Request
import secrets


def validar_usuario_logado(request: Request) -> bool:
    try:
        token = request.cookies["auth_token"]
        if token == False:
            return False
    except KeyError:
        return False

    return True


def gerar_token(tamanho: int = 32) -> str:
    return secrets.token_hex(tamanho)
