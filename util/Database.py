import sqlite3


class Database:
    @classmethod
    def criarConexao(cls):
        conn = sqlite3.connect("database.db")
        return conn
