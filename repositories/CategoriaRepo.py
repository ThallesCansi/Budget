from typing import List


from models.Categoria import Categoria
from util.Database import Database


class CategoriaRepo:
    @classmethod
    def criarTabela(cls):
        sql = """CREATE TABLE IF NOT EXISTS categoria (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                idUsuario INTEGER NOT NULL,
                nome TEXT NOT NULL,
                CONSTRAINT fkUsuarioCategoria FOREIGN KEY(idUsuario) REFERENCES usuario(id)
            )"""
        conexao = Database.criarConexao()
        cursor = conexao.cursor()
        tabelaCriada = cursor.execute(sql).rowcount > 0
        conexao.commit()
        conexao.close()
        return tabelaCriada

    @classmethod
    def inserir(cls, categoria: Categoria) -> Categoria:
        sql = "INSERT INTO categoria (nome, idUsuario) values (?, ?)"
        conexao = Database.criarConexao()
        cursor = conexao.cursor()
        resultado = cursor.execute(sql, (categoria.nome, categoria.idUsuario))
        if resultado.rowcount > 0:
            categoria.id = resultado.lastrowid
        conexao.commit()
        conexao.close()
        return categoria

    @classmethod
    def alterar(cls, categoria: Categoria) -> Categoria:
        sql = "UPDATE categoria SET nome=? WHERE id=?"
        conexao = Database.criarConexao()
        cursor = conexao.cursor()
        resultado = cursor.execute(
            sql,
            (
                categoria.nome,
                categoria.id,
            ),
        )
        if resultado.rowcount > 0:
            conexao.commit()
            conexao.close()
            return categoria
        else:
            conexao.close()
            return None

    @classmethod
    def excluir(cls, id: int) -> bool:
        sql = "DELETE FROM categoria WHERE id=?"
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
    def obterTodos(cls) -> List[Categoria]:
        sql = "SELECT * FROM categoria"
        conexao = Database.criarConexao()
        cursor = conexao.cursor()
        resultado = cursor.execute(sql).fetchall()
        objetos = [Categoria(*x) for x in resultado]
        conexao.commit()
        conexao.close()
        return objetos

    @classmethod
    def obterPorId(cls, id: int) -> Categoria:
        sql = "SELECT * FROM categoria WHERE id=?"
        conexao = Database.criarConexao()
        cursor = conexao.cursor()
        resultado = cursor.execute(sql, (id,)).fetchone()
        objeto = Categoria(*resultado)
        conexao.commit()
        conexao.close()
        return objeto

    @classmethod
    def obterCategoriaPorUsuario(cls, idUsuario: int) -> list[Categoria]:
        sql = "SELECT * FROM categoria WHERE idUsuario=?"
        conexao = Database.criarConexao()
        cursor = conexao.cursor()
        try:
            resultado = cursor.execute(sql, (idUsuario,)).fetchall()
            if resultado:
                objeto = [Categoria(*x) for x in resultado]
            else:
                objeto = None
        except Exception as e: 
            objeto = e
        conexao.commit()
        conexao.close()
        return objeto
