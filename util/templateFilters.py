def formatarData(dataStr: str) -> str:
    if dataStr is None:
        return ""
    ano, mes, dia = dataStr.split("-")
    return f"{dia}/{mes}/{ano}"
