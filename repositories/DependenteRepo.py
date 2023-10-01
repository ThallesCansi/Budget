from models.Dependente import Dependente
from util.Database import Database


class DependenteRepo:
    @classmethod
    def criarTabela(cls):
        sql = """CREATE TABLE IF NOT EXISTS dependente (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                idUsuario INTEGER,
                nome TEXT NOT NULL,
                CONSTRAINT fkUsuarioDependente FOREIGN KEY(idUsuario) REFERENCES usuario(id)
            )"""
        conn = Database.criarConexao()
        cursor = conn.cursor()
        tableCreated = cursor.execute(sql).rowcount > 0
        conn.commit()
        conn.close()
        return tableCreated

    @classmethod
    def inserir(cls, dependente: Dependente) -> Dependente:
        sql = "INSERT INTO dependente (idUsuario, nome) VALUES (?, ?)"
        conn = Database.criarConexao()
        cursor = conn.cursor()
        result = cursor.execute(sql, (dependente.idUsuario, dependente.nome))
        if result.rowcount > 0:
            dependente.id = result.lastrowid
        conn.commit()
        conn.close()
        return dependente
