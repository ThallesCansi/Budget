from typing import List

from util.Database import Database
from models.Meta import Meta

class MetaRepo:
    @classmethod
    def criarTabela(cls):
        sql = """CREATE TABLE IF NOT EXISTS meta(
            idMeta INTEGER PRIMARY KEY AUTOINCREMENT,
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