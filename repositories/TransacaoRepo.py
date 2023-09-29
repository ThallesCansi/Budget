from typing import List

from models.Transacao import Transacao
from util.Database import Database


class TransacaoRepo:
    @classmethod
    def criarTabela(cls):
        sql = """
            CREATE TABLE IF NOT EXISTS transacao (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            descricao TEXT NOT NULL,
            valor DECIMAL NOT NULL,
            conta TEXT NOT NULL,
            dependente TEXT NOT NULL,
            data DATE NOT NULL,
            categoria TEXT NOT NULL,
            forma_pagamento TEXT NOT NULL"""
        conexao = Database.criarConexao()
        cursor = conexao.cursor()
        tabelaCriada = cursor.execute(sql).rowcount > 0
        conexao.commit()
        conexao.close()
        return tabelaCriada

    @classmethod
    def inserir(cls, transacao: Transacao) -> Transacao:
        sql = """INSERT INTO transacao (descricao, valor, conta, dependente, data, categoria, forma_pagamento)
            values (?, ?, ?, ?, ?, ?, ?)"""
        conexao = Database.criarConexao()
        cursor = conexao.cursor()
        resultado = cursor.execute(
            sql, (transacao.descricao, transacao.valor, transacao.conta, transacao.dependente,
                  transacao.data, transacao.categoria, transacao.forma_pagamento)
        )
        if resultado.rowcount > 0:
            transacao.id = resultado.lastrowid
        conexao.commit()
        conexao.close()
        return transacao

    @classmethod
    def alterar(cls, transacao: Transacao) -> Transacao:
        sql = "UPDATE transacao SET descricao=?, valor=?, conta=?, dependente=?, data=?, categoria=?, forma_pagamento=? WHERE id=?"
        conexao = Database.criarConexao()
        cursor = conexao.cursor()
        resultado = cursor.execute(
            sql, (transacao.descricao, transacao.valor, transacao.conta, transacao.dependente,
                  transacao.data, transacao.categoria, transacao.forma_pagamento, transacao.id)
        )
        if resultado.rowcount > 0:
            conexao.commit()
            conexao.close()
            return transacao
        else:
            conexao.close()
            return None

    @classmethod
    def excluir(cls, id: int) -> bool:
        sql = "DELETE FROM transacao WHERE id=?"
        conexao = Database.criarConexao()
        cursor = conexao.cursor()
        resultado = cursor.execute(sql, (id,))
        if resultado.rowcount > 0:
            conexao.commit()
            conexao.close()
            return True
        else:
            conexao.close()
            return False

    @classmethod
    def obterTodos(cls) -> List[Transacao]:
        sql = "SELECT * FROM transacao"
        conexao = Database.criarConexao()
        cursor = conexao.cursor()
        resultado = cursor.execute(sql).fetchall()
        objetos = [Transacao(*x) for x in resultado]
        conexao.commit()
        conexao.close()
        return objetos

    @classmethod
    def obterPorId(cls, id: int) -> Transacao:
        sql = "SELECT * FROM transacao WHERE id=?"
        conexao = Database.criarConexao()
        cursor = conexao.cursor()
        resultado = cursor.execute(sql, (id,)).fetchone()
        objeto = Transacao(*resultado)
        conexao.commit()
        conexao.close()
        return objeto
