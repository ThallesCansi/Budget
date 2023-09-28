from typing import List


from models.Meta import Meta
from util.Database import Database

class MetaRepo:
    @classmethod
    def criarTabela(cls):
        sql = """CREATE TABLE IF NOT EXISTS meta(
            idMeta INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario INTEGER,
            nome TEXT NOT NULL,
            valor DECIMAL,
            valorinicial DECIMAL,
            data DATE,
            descricao TEXT NOT NULL,
            cor TEXT,
            FOREIGN KEY(usuario) REFERENCES user(usuario))"""
        conexao = Database.criarConexao()
        cursor = conexao.cursor()
        tabelaCriada = cursor.execute(sql).rowcount > 0
        
        conexao.commit()
        conexao.close()
        return tabelaCriada

    @classmethod
    def inserir(cls, meta: Meta) -> Meta:
        sql = """INSERT INTO meta (nome, valor, valorinicial, data, descricao, cor)
            values (?, ?, ?, ?, ?, ?)"""
        conexao = Database.criarConexao()
        cursor = conexao.cursor()
        resultado = cursor.execute(
            sql, (Meta.nome, Meta.valor, Meta.valorinicial, Meta.data, Meta.descricao, Meta.cor)
        )
        if resultado.rowcount > 0:
            meta.idMeta = resultado.lastrowid
        conexao.commit()
        conexao.close()
        return meta

    @classmethod
    def alterar(cls, meta: Meta) -> Meta:
        sql = "UPDATE meta SET nome=?, valor=?, valorinicial=?, data=?, descricao=?, cor=? WHERE idMeta=?"
        conexao = Database.criarConexao()
        cursor = conexao.cursor()
        resultado = cursor.execute(
            sql, (Meta.nome, Meta.valor, Meta.valorinicial, Meta.data, Meta.descricao, Meta.cor, Meta.idMeta)
        )
        if resultado.rowcount > 0:
            conexao.commit()
            conexao.close()
            return meta
        else:
            conexao.close()
            return None

    @classmethod
    def excluir(cls, idMeta: int) -> bool:
        sql = "DELETE FROM meta WHERE idMeta=?"
        conexao = Database.criarConexao()
        cursor = conexao.cursor()
        resultado = cursor.execute(sql, (idMeta,))
        if resultado.rowcount > 0:
            conexao.commit()
            conexao.close()
            return True
        else:
            conexao.close()
            return False

    @classmethod
    def limparTabela(cls) -> bool:
        sql = "DELETE FROM meta"
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
    def obterTodos(cls) -> List[Meta]:
        sql = "SELECT idMeta, usuario, nome, valor, valorinicial, data, descricao cor FROM meta"
        conexao = Database.criarConexao()
        cursor = conexao.cursor()
        resultado = cursor.execute(sql).fetchall()
        objetos = [Meta(*x) for x in resultado]
        conexao.commit()
        conexao.close()
        return objetos

    @classmethod
    def obterPorId(cls, idMeta: int) -> Meta:
        sql = "SELECT idMeta, usuario, nome, valor, valorinicial, data, descricao, cor FROM meta WHERE idMeta=?"
        conexao = Database.criarConexao()
        cursor = conexao.cursor()
        resultado = cursor.execute(sql, (idMeta,)).fetchone()
        objeto = Meta(*resultado)
        conexao.commit()
        conexao.close()
        return objeto