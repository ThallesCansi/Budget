import sqlite3


class Database:
    @classmethod
    def createConnection(cls):
        conn = sqlite3.connect("database.db")
        return conn
