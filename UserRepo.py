from typing import List
from Database import Database
from User import User


class UserRepo:
    @classmethod
    def createTable(cls):
        sql = """
            CREATE TABLE IF NOT EXISTS user (
            idUser INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            birth TEXT,
            password TEXT NOT NULL,
            phone TEXT,
            state TEXT,
            city TEXT)
        """
        conn = Database.createConnection()
        cursor = conn.cursor()
        tableCreated = (cursor.execute(sql).rowcount > 0)
        conn.commit()
        conn.close()
        return tableCreated

    @classmethod
    def insert(cls, user: User) -> User:
        sql = "INSERT INTO user (name, email, birth, password, phone, state, city) VALUES (?, ?, ?, ?, ?, ?, ?)"
        conn = Database.createConnection()
        cursor = conn.cursor()
        result = cursor.execute(
            sql, (user.name, user.email, user.birth, user.password, user.phone, user.state, user.city))
        if (result.rowcount > 0):
            user.id = result.lastrowid
        conn.commit()
        conn.close()
        return user

    @classmethod
    def update(cls, user: User) -> User:
        sql = "UPDATE user SET name=?, email=?, birth=?, password=?, phone=?, state=?, city=? WHERE idUser=?"
        conn = Database.createConnection()
        cursor = conn.cursor()
        result = cursor.execute(
            sql, (user.name, user.email, user.birth, user.password, user.phone, user.state, user.city))
        if (result.rowcount > 0):
            conn.commit()
            conn.close()
            return user
        else:
            conn.close()
            return None

    @classmethod
    def delete(cls, idUser: int) -> bool:
        sql = "DELETE FROM user WHERE idUser=?"
        conn = Database.createConnection()
        cursor = conn.cursor()
        result = cursor.execute(sql, (idUser, ))
        if (result.rowcount > 0):
            conn.commit()
            conn.close()
            return True
        else:
            conn.close()
            return False

    @classmethod
    def getAll(cls) -> List[User]:
        sql = "SELECT idUser, name, email, birth, password, phone, state, city FROM user"
        conn = Database.createConnection()
        cursor = conn.cursor()
        result = cursor.execute(sql).fetchall()
        objects = [User(*x) for x in result]
        return objects

    @classmethod
    def getOne(cls, idUser: int) -> User:
        sql = "SELECT idUser, name, email, birth, password, phone, state, city FROM user WHERE idUser=?"
        conn = Database.createConnection()
        cursor = conn.cursor()
        result = cursor.execute(sql, (idUser, )).fetchone()
        object = User(*result)
        return object

    @classmethod
    def getAllOrderedByNameAsc(cls) -> List[User]:
        sql = "SELECT idUser, name, email, birth, password, phone, state, city FROM user ORDER BY name ASC"
        conn = Database.createConnection()
        cursor = conn.cursor()
        result = cursor.execute(sql).fetchall()
        objects = [User(*x) for x in result]
        return objects
