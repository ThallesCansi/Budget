from typing import List

from util.Database import Database
from models.Conta import Conta


class ContaRepo:
    @classmethod
    def criarTabela(cls):
        sql = """
                CREATE TABLE IF NOT EXISTS conta
            (
                idConta INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario INTEGER,
                titulo TEXT NOT NULL,
                saldo DECIMAL NOT NULL,
                meta TEXT,
                FOREIGN KEY(usuario) REFERENCES user(usuario)
            )
                """
        conn = Database.createConnection()
        cursor = conn.cursor()
        tableCreated = (cursor.execute(sql).rowcount > 0)
        conn.commit()
        conn.close()
        return tableCreated

    @classmethod
    def inserir(cls, conta: Conta) -> Conta:
        sql = """
                INSERT INTO conta (titulo, saldo, meta)
                VALUES (?, ?, ?)
              """
        conn = Database.createConnection()
        cursor = conn.cursor()
        result = cursor.execute(
            sql, (conta.titulo, conta.saldo, conta.meta))
        if (result.rowcount > 0):
            conta.idConta = result.lastrowid
        conn.commit()
        conn.close()
        return conta

    @classmethod
    def atualizar(cls, conta: Conta) -> Conta:
        sql = "UPDATE conta SET titulo=?, saldo=?, meta=? WHERE idConta=?"
        conn = Database.createConnection()
        cursor = conn.cursor()
        result = cursor.execute(
            sql, (conta.titulo, conta.saldo, conta.meta, conta.idConta))
        if (result.rowcount > 0):
            conn.commit()
            conn.close()
            return conta
        else:
            conn.close()
            return None

    @classmethod
    def excluir(cls, idConta: int) -> bool:
        sql = "DELETE FROM conta WHERE idconta=?"
        conn = Database.createConnection()
        cursor = conn.cursor()
        result = cursor.execute(sql, (idConta, ))
        if (result.rowcount > 0):
            conn.commit()
            conn.close()
            return True
        else:
            conn.close()
            return False

    @classmethod
    def getAll(cls) -> List[Conta]:
        sql = "SELECT idConta, usuario, titulo, salado, meta FROM conta"
        conn = Database.createConnection()
        cursor = conn.cursor()
        result = cursor.execute(sql).fetchall()
        objects = [Conta(*x) for x in result]
        conn.commit()
        conn.close()
        return objects

    @classmethod
    def getOne(cls, idconta: int) -> Conta:
        sql = "SELECT idConta, usuario, titulo, salado, meta FROM conta WHERE idConta=?"
        conn = Database.createConnection()
        cursor = conn.cursor()
        result = cursor.execute(sql, (idconta, )).fetchone()
        object = Conta(*result)
        conn.commit()
        conn.close()
        return object
