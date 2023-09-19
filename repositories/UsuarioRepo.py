from typing import List

from models.Usuario import Usuario
from util.Database import Database


class UsuarioRepo:
    @classmethod
    def criarTabela(cls):
        sql = """
                CREATE TABLE IF NOT EXISTS usuario
            (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome INTEGER,
                senha TEXT NOT NULL
            )
                """
        conn = Database.createConnection()
        cursor = conn.cursor()
        tableCreated = cursor.execute(sql).rowcount > 0
        conn.commit()
        conn.close()
        return tableCreated

    @classmethod
    def inserir(cls, usuario: Usuario) -> Usuario:
        sql = """
                INSERT INTO usuario (nome, senha)
                VALUES (?, ?)
              """
        conn = Database.createConnection()
        cursor = conn.cursor()
        result = cursor.execute(sql, (usuario.nome, usuario.senha))
        if result.rowcount > 0:
            usuario.id = result.lastrowid
        conn.commit()
        conn.close()
        return usuario

    @classmethod
    def alterar(cls, usuario: Usuario) -> Usuario:
        sql = "UPDATE usuario SET nome=?, senha=? WHERE id=?"
        conn = Database.createConnection()
        cursor = conn.cursor()
        result = cursor.execute(sql, (usuario.nome, usuario.senha, usuario.id))
        if result.rowcount > 0:
            conn.commit()
            conn.close()
            return usuario
        else:
            conn.close()
            return None

    @classmethod
    def excluir(cls, id: int) -> bool:
        sql = "DELETE FROM usuario WHERE id=?"
        conn = Database.createConnection()
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
        sql = "DELETE FROM usuario"
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
    def obterTodos(cls) -> List[Usuario]:
        sql = "SELECT id, nome, senha FROM usuario"
        conn = Database.createConnection()
        cursor = conn.cursor()
        result = cursor.execute(sql).fetchall()
        objects = [Usuario(*x) for x in result]
        conn.commit()
        conn.close()
        return objects

    @classmethod
    def obterPorId(cls, id: int) -> Usuario:
        sql = "SELECT id, nome, senha FROM usuario WHERE id=?"
        conn = Database.createConnection()
        cursor = conn.cursor()
        result = cursor.execute(sql, (id,)).fetchone()
        object = Usuario(*result)
        conn.commit()
        conn.close()
        return object
