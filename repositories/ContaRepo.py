from typing import List, Tuple


from models.Conta import Conta
from util.Database import Database


class ContaRepo:
    @classmethod
    def criarTabela(cls):
        sql = """CREATE TABLE IF NOT EXISTS conta (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                idUsuario INTEGER,
                nome TEXT NOT NULL,
                saldo DECIMAL NOT NULL,
                descricao TEXT,
                FOREIGN KEY(idUsuario) REFERENCES usuario(id)
            )"""
        conn = Database.criarConexao()
        cursor = conn.cursor()
        tableCreated = cursor.execute(sql).rowcount > 0
        conn.commit()
        conn.close()
        return tableCreated

    @classmethod
    def inserir(cls, conta: Conta) -> Conta:
        sql = """
                INSERT INTO conta (idUsuario, nome, saldo, descricao)
                VALUES (?, ?, ?, ?)
              """
        conn = Database.criarConexao()
        cursor = conn.cursor()
        result = cursor.execute(
            sql, (conta.idUsuario, conta.nome, conta.saldo, conta.descricao)
        )
        if result.rowcount > 0:
            conta.id = result.lastrowid
        conn.commit()
        conn.close()
        return conta

    @classmethod
    def alterar(cls, conta: Conta) -> Conta:
        sql = "UPDATE conta SET nome=?, saldo=?, descricao=? WHERE id=?"
        conn = Database.criarConexao()
        cursor = conn.cursor()
        result = cursor.execute(sql, (conta.nome, conta.saldo, conta.descricao, conta.id))
        if result.rowcount > 0:
            conn.commit()
            conn.close()
            return conta
        else:
            conn.close()
            return None

    @classmethod
    def excluirContaTransacoes(cls, id: int) -> bool:
        sql = """DELETE FROM transacao
                WHERE idConta = ?;
                """
        conexao = Database.criarConexao()
        cursor = conexao.cursor()
        result = cursor.execute(sql, (id,))

        if result.rowcount > 0:
            conexao.commit()
            conexao.close()
        else:
            conexao.close()

        sql = """DELETE FROM conta
                WHERE id = ?;
                """
        conexao = Database.criarConexao()
        cursor = conexao.cursor()
        result = cursor.execute(sql, (id,))

        if result.rowcount > 0:
            conexao.commit()
            conexao.close()
            return True
        else:
            conexao.close()
            return False

    @classmethod
    def limparTabela(cls) -> bool:
        sql = "DELETE FROM conta"
        conexao = Database.criarConexao()
        cursor = conexao.cursor()
        resultado = cursor.execute(sql)
        if resultado.rowcount > 0:
            conexao.commit()
            conexao.close()
            return True
        else:
            conexao.close()
            return False

    @classmethod
    def obterTodos(cls) -> List[Conta]:
        sql = "SELECT id, idUsuario, nome, saldo, descricao FROM conta"
        conn = Database.criarConexao()
        cursor = conn.cursor()
        result = cursor.execute(sql).fetchall()
        objects = [Conta(*x) for x in result]
        conn.commit()
        conn.close()
        return objects

    @classmethod
    def obterPorId(cls, id: int) -> Conta:
        sql = "SELECT id, idUsuario, nome, saldo, descricao FROM conta WHERE id=?"
        conn = Database.criarConexao()
        cursor = conn.cursor()
        result = cursor.execute(sql, (id,)).fetchone()
        object = Conta(*result)
        conn.commit()
        conn.close()
        return object

    @classmethod
    def obterContaPorUsuario(cls, idUsuario: int) -> list[Conta]:
        sql = "SELECT * FROM conta WHERE idUsuario=?"
        conexao = Database.criarConexao()
        cursor = conexao.cursor()
        try:
            resultado = cursor.execute(sql, (idUsuario,)).fetchall()
            if resultado:
                objeto = [Conta(*x) for x in resultado]
            else:
                objeto = []
        except Exception as e:
            objeto = e
        conexao.commit()
        conexao.close()
        return objeto

    @classmethod
    def obterSaldoContas(cls, idUsuario: int) -> List[Tuple[int, float]]:
        sql = """SELECT 
                    c.id AS id_conta,
                    COALESCE(c.saldo, 0) + COALESCE(SUM(t.valor), 0) AS saldo_atualizado
                FROM conta c
                LEFT JOIN transacao t ON c.id = t.idConta AND t.idUsuario = ?
                WHERE c.idUsuario = ?
                GROUP BY c.id, c.saldo;
            """
        conexao = Database.criarConexao()
        cursor = conexao.cursor()
        try:
            cursor.execute(sql, (idUsuario, idUsuario))
            resultados = cursor.fetchall()
            saldo_contas = [(row[0], row[1]) for row in resultados]
        except Exception as e:
            saldo_contas = []
        conexao.close()
        return saldo_contas

    @classmethod
    def verificarTransacoesConta(cls, id) -> bool:
        sql = """SELECT COUNT(*) AS total_transacoes
                FROM transacao
                WHERE idConta = ?;
                """
        conexao = Database.criarConexao()
        cursor = conexao.cursor()
        resultado = cursor.execute(sql, (id, )).fetchone()
        conexao.close
        if resultado[0] == 0:
            return False
        else:
            return True