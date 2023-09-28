def formatarData(dataStr: str) -> str:
    if dataStr is None:
        return ""
    ano, mes, dia = dataStr.split("-")
    return f"{dia}/{mes}/{ano}"


def capitalizar_nome_proprio(nome: str) -> str:
    nome = nome.lower()
    ignoradas = ['de', 'da', 'do', 'di', 'das', 'com', 'dos']    
    palavras = nome.split()    
    palavras_capitalizadas = [
        palavra.capitalize() if palavra.lower() not in ignoradas else palavra.lower()
        for palavra in palavras
    ]
    return ' '.join(palavras_capitalizadas)