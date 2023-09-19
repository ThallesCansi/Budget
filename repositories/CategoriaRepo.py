from typing import List

from util.Database import Database
from models.Categoria import Categoria


class CategoriaRepo:
    @classmethod
    def criarTabela(cls):
        sql = """CREATE TABLE IF NOT EXISTS categoria(
            idCategoria INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario INTEGER,
            nome TEXT NOT NULL,
            limite DECIMAL,
            cor TEXT,
            tipo TEXT,
            FOREIGN KEY(usuario) REFERENCES user(usuario))"""
        conexao = Database.criarConexao()
        cursor = conexao.cursor()
        tabelaCriada = cursor.execute(sql).rowcount > 0
        conexao.commit()
        conexao.close()
        return tabelaCriada

    @classmethod
    def inserir(cls, categoria: Categoria) -> Categoria:
        sql = """INSERT INTO categoria (nome, limite, cor, tipo)
            values (?, ?, ?, ?)"""
        conexao = Database.criarConexao()
        cursor = conexao.cursor()
        resultado = cursor.execute(
            sql, (categoria.nome, categoria.limite, categoria.cor, categoria.tipo)
        )
        if resultado.rowcount > 0:
            categoria.idCategoria = resultado.lastrowid
        conexao.commit()
        conexao.close()
        return categoria

    @classmethod
    def alterar(cls, categoria: Categoria) -> Categoria:
        sql = "UPDATE categoria SET nome=?, limite=?, cor=?, tipo=? WHERE idCategoria=?"
        conexao = Database.criarConexao()
        cursor = conexao.cursor()
        resultado = cursor.execute(
            sql, (categoria.nome, categoria.limite, categoria.cor, categoria.tipo, categoria.idCategoria)
        )
        if resultado.rowcount > 0:
            conexao.commit()
            conexao.close()
            return categoria
        else:
            conexao.close()
            return None

    @classmethod
    def excluir(cls, idCategoria: int) -> bool:
        sql = "DELETE FROM categoria WHERE idCategoria=?"
        conexao = Database.criarConexao()
        cursor = conexao.cursor()
        resultado = cursor.execute(sql, (idCategoria,))
        if resultado.rowcount > 0:
            conexao.commit()
            conexao.close()
            return True
        else:
            conexao.close()
            return False

    @classmethod
    def limparTabela(cls) -> bool:
        sql = "DELETE FROM categoria"
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
    def obterTodos(cls) -> List[Categoria]:
        sql = "SELECT idCategoria, usuario, nome, limite, cor, tipo FROM categoria"
        conexao = Database.criarConexao()
        cursor = conexao.cursor()
        resultado = cursor.execute(sql).fetchall()
        objetos = [Categoria(*x) for x in resultado]
        conexao.commit()
        conexao.close()
        return objetos

    @classmethod
    def obterPorId(cls, idCategoria: int) -> Categoria:
        sql = "SELECT idCategoria, usuario, nome, limite, cor, tipo FROM categoria WHERE idCategoria=?"
        conexao = Database.criarConexao()
        cursor = conexao.cursor()
        resultado = cursor.execute(sql, (idCategoria,)).fetchone()
        objeto = Categoria(*resultado)
        conexao.commit()
        conexao.close()
        return objeto
