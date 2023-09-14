from typing import List
from Repositorio.Database import Database
from Repositorio.Dependent.Dependent import Dependent

class DependentRepo:
    @classmethod
    def createTable(cls):
        sql = """
                CREATE TABLE IF NOT EXISTS dependent
            (
                idDependent INTEGER PRIMARY KEY AUTOINCREMENT,
                idUser INTEGER,
                name TEXT NOT NULL,
                description TEXT NOT NULL,
                colorTag TEXT NOT NULL,
                FOREIGN KEY(idUser) REFERENCES user(idUser)
            )
              """
        conn = Database.createConnection()
        cursor = conn.cursor()
        tableCreated = (cursor.execute(sql).rowcount > 0)
        conn.commit()
        conn.close()
        return tableCreated
    
    @classmethod
    def insert(cls, dependent: Dependent) -> Dependent:
        sql = """
                INSERT INTO dependent (name, description, colorTag)
                VALUES (?, ?, ?)
              """
        conn = Database.createConnection()
        cursor = conn.cursor()
        result = cursor.execute (sql, (dependent.name, dependent.description, dependent.colorTag))
        if (result.rowcount > 0):
            dependent.idDependent = result.lastrowid
        conn.commit()
        conn.close()
        return dependent
    
    @classmethod
    def update(cls, dependent: Dependent) -> Dependent:
        sql = "UPDATE dependent SET name=?, description=?, colorTag=? WHERE idDependent=?"
        conn = Database.createConnection()
        cursor = conn.cursor()
        result = cursor.execute(sql, (dependent.name, dependent.description, dependent.colorTag, dependent.idDependent))
        if (result.rowcount > 0):
            conn.commit()
            conn.close()
            return dependent
        else:
            conn.close()
            return None
    
    @classmethod
    def delete(cls, idDependent: int) -> bool:
        sql="DELETE FROM dependent WHERE idDependent=?"
        conn = Database.createConnection()
        cursor = conn.cursor()
        result = cursor.execute(sql, (idDependent, ))
        if (result.rowcount > 0):
            conn.commit()
            conn.close()
            return True
        else:
            conn.close()
            return False

    @classmethod
    def getAll(cls) ->List[Dependent]:
        sql = "SELECT idDependent, idUser, name, description, colorTag FROM dependent"
        conn = Database.createConnection()
        cursor = conn.cursor()
        result = cursor.execute(sql).fetchall()
        objects = [Dependent(*x) for x in result]
        conn.commit()
        conn.close()
        return objects

    @classmethod
    def getOne(cls, idDependent: int) -> Dependent:
        sql = "SELECT idDependent, idUser, name, description, colorTag FROM dependent WHERE idDependent=?"
        conn = Database.createConnection()
        cursor = conn.cursor()
        result = cursor.execute(sql, (idDependent, )).fetchone()
        object = Dependent(*result)
        conn.commit()
        conn.close()
        return object

