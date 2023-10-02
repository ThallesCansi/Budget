from typing import List


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
                meta TEXT,
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
                INSERT INTO conta (idUsuario, nome, saldo, meta)
                VALUES (?, ?, ?, ?)
              """
        conn = Database.criarConexao()
        cursor = conn.cursor()
        result = cursor.execute(
            sql, (conta.idUsuario, conta.nome, conta.saldo, conta.meta)
        )
        if result.rowcount > 0:
            conta.id = result.lastrowid
        conn.commit()
        conn.close()
        return conta

    @classmethod
    def alterar(cls, conta: Conta) -> Conta:
        sql = "UPDATE conta SET nome=?, saldo=?, meta=? WHERE id=?"
        conn = Database.criarConexao()
        cursor = conn.cursor()
        result = cursor.execute(sql, (conta.nome, conta.saldo, conta.meta, conta.id))
        if result.rowcount > 0:
            conn.commit()
            conn.close()
            return conta
        else:
            conn.close()
            return None

    @classmethod
    def excluir(cls, id: int) -> bool:
        sql = "DELETE FROM conta WHERE id=?"
        conn = Database.criarConexao()
        cursor = conn.cursor()
        result = cursor.execute(sql, (id,))
        if result.rowcount > 0:
            conn.commit()
            conn.close()
            return True
        else:
            conn.close()
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
        sql = "SELECT id, idUsuario, nome, saldo, meta FROM conta"
        conn = Database.criarConexao()
        cursor = conn.cursor()
        result = cursor.execute(sql).fetchall()
        objects = [Conta(*x) for x in result]
        conn.commit()
        conn.close()
        return objects

    @classmethod
    def obterPorId(cls, id: int) -> Conta:
        sql = "SELECT id, idUsuario, nome, saldo, meta FROM conta WHERE id=?"
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
