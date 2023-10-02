from typing import List

from models.Transacao import Transacao
from util.Database import Database


class TransacaoRepo:
    @classmethod
    def criarTabela(cls):
        sql = """CREATE TABLE IF NOT EXISTS transacao (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                idConta INT NOT NULL,
                idCategoria INT NOT NULL,
                idDependente INT NOT NULL,
                idUsuario INT NOT NULL,
                descricao TEXT NOT NULL,
                data DATE NOT NULL,
                valor DECIMAL NOT NULL,
                forma_pagamento TEXT NOT NULL,
                tipo TEXT NOT NULL,
                CONSTRAINT fkContaTransacao FOREIGN KEY(idConta) REFERENCES conta(id),
                CONSTRAINT fkCategoriaTransacao FOREIGN KEY(idCategoria) REFERENCES categoria(id),
                CONSTRAINT fkDependenteTransacao FOREIGN KEY(idDependente) REFERENCES dependente(id),
                CONSTRAINT fkUsuarioTransacao FOREIGN KEY(idUsuario) REFERENCES usuario(id)
            );"""
        conexao = Database.criarConexao()
        cursor = conexao.cursor()
        tabelaCriada = cursor.execute(sql).rowcount > 0
        conexao.commit()
        conexao.close()
        return tabelaCriada

    @classmethod
    def inserir(cls, transacao: Transacao) -> Transacao:
        sql = "INSERT INTO transacao (idConta, idCategoria, idDependente, idUsuario, descricao, data, valor, forma_pagamento, tipo) values (?, ?, ?, ?, ?, ?, ?, ?, ?);"
        conexao = Database.criarConexao()
        cursor = conexao.cursor()
        resultado = cursor.execute(
            sql,
            (
                transacao.idConta,
                transacao.idCategoria,
                transacao.idDependente,
                transacao.idUsuario,
                transacao.descricao,
                transacao.data,
                transacao.valor,
                transacao.forma_pagamento,
                transacao.tipo,
            ),
        )
        if resultado.rowcount > 0:
            transacao.id = resultado.lastrowid
        conexao.commit()
        conexao.close()
        return transacao

    @classmethod
    def alterar(cls, transacao: Transacao) -> Transacao:
        sql = "UPDATE transacao SET idConta=?, idCategoria=?, idDependente=?, descricao=?, data=?, valor=?, forma_pagamento=?, tipo=? WHERE id=?;"
        conexao = Database.criarConexao()
        cursor = conexao.cursor()
        resultado = cursor.execute(
            sql,
            (
                transacao.idConta,
                transacao.idCategoria,
                transacao.idDependente,
                transacao.idUsuario,
                transacao.descricao,
                transacao.data,
                transacao.valor,
                transacao.forma_pagamento,
                transacao.tipo,
            ),
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
        sql = "DELETE FROM transacao WHERE id=?;"
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
    def obterTransacaoPorUsuario(cls, idUsuario: int) -> Transacao:
        sql = """SELECT
                    t.id as id_transacao,
                    t.descricao AS descricao_transacao,
                    t.data,
                    t.valor,
                    t.forma_pagamento,
                    t.tipo,
                    c.nome AS nome_categoria,
                    co.nome AS nome_conta,
                    d.nome AS nome_dependente
                FROM transacao t
                INNER JOIN categoria c ON t.idCategoria = c.id
                INNER JOIN conta co ON t.idConta = co.id
                LEFT JOIN dependente d ON t.idDependente = d.id
                WHERE t.idUsuario = ?;
                """
        conexao = Database.criarConexao()
        cursor = conexao.cursor()
        resultado = cursor.execute(sql, (idUsuario,)).fetchall()
        objetos = [
            Transacao(
                id=x[0],
                descricao=x[1],
                data=x[2],
                valor=x[3],
                forma_pagamento=x[4],
                tipo=x[5],
                nomeCategoria=x[6],
                nomeConta=x[7],
                nomeDependente=x[8],
            )
            for x in resultado
        ]
        conexao.commit()
        conexao.close()
        return objetos

    @classmethod
    def obterReceita(cls, idUsuario: int) -> str:
        sql = """SELECT
                    SUM(CASE WHEN t.tipo = 'Receita' AND t.valor > 0 THEN t.valor ELSE 0 END) AS soma_receitas_positivas
                FROM transacao t
                WHERE t.idUsuario = ?;
                """
        conexao = Database.criarConexao()
        cursor = conexao.cursor()
        resultado = cursor.execute(sql, (idUsuario,)).fetchone()
        conexao.commit()
        conexao.close()
        return resultado[0]

    @classmethod
    def obterDespesa(cls, idUsuario: int) -> float:
        sql = """SELECT
                    SUM(CASE WHEN t.tipo = 'Despesa' AND t.valor < 0 THEN t.valor ELSE 0 END) AS soma_receitas_positivas
                FROM transacao t
                WHERE t.idUsuario = ?;
                """
        conexao = Database.criarConexao()
        cursor = conexao.cursor()
        resultado = cursor.execute(sql, (idUsuario,)).fetchone()
        conexao.commit()
        conexao.close()
        return resultado[0]

    @classmethod
    def obterSaldo(cls, idUsuario: int) -> float:
        sql = """SELECT
                    SUM(t.valor) AS soma_total_valores
                FROM transacao t
                INNER JOIN categoria c ON t.idCategoria = c.id
                INNER JOIN conta co ON t.idConta = co.id
                LEFT JOIN dependente d ON t.idDependente = d.id
                WHERE t.idUsuario = ?;
                """
        conexao = Database.criarConexao()
        cursor = conexao.cursor()
        resultado = cursor.execute(sql, (idUsuario,)).fetchone()
        conexao.commit()
        conexao.close()
        return resultado[0]
