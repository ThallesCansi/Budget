from typing import List
from Database import Database
from Category import Category

class CategoryRepo:
    @classmethod
    def createTable(cls):
        sql = """
                CREATE TABLE IF NOT EXISTS category 
            (
                idCategory INTEGER PRIMARY KEY AUTOINCREMENT,
                idUser INTEGER,
                name TEXT NOT NULL,
                limitMoney DECIMAL NOT NULL,
                colorTag TEXT NOT NULL,
                icon BLOB NOT NULL,
                typeIorE BINARY NOT NULL,
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
    def insert(cls, category: Category) -> Category:
        sql = """
                INSERT INTO category (name, limitMoney, colorTag, icon, typeIorE)
                VALUES (?, ?, ?, ?, ?)
              """
        conn = Database.createConnection()
        cursor = conn.cursor()
        result = cursor.execute (sql, (category.name, category.limit, category.colorTag, category.icon, category.typeIorE))
        if (result.rowcount > 0):
            category.idCategory = result.lastrowid
        conn.commit()
        conn.close()
        return category
    
    @classmethod
    def update(cls, category: Category) -> Category:
        sql = "UPDATE category SET name=?, limitMoney=?, colorTag=?, icon=?, typeIorE=? WHERE idCategory=?"
        conn = Database.createConnection()
        cursor = conn.cursor()
        result = cursor.execute(sql, (category.name, category.limit, category.colorTag, category.icon, category.typeIorE, category.idCategory))
        if (result.rowcount > 0):
            conn.commit()
            conn.close()
            return category
        else:
            conn.close()
            return None
    
    @classmethod
    def delete(cls, idCategory: int) -> bool:
        sql="DELETE FROM category WHERE idCategory=?"
        conn = Database.createConnection()
        cursor = conn.cursor()
        result = cursor.execute(sql, (idCategory, ))
        if (result.rowcount > 0):
            conn.commit()
            conn.close()
            return True
        else:
            conn.close()
            return False

    @classmethod
    def getAll(cls) ->List[Category]:
        sql = "SELECT idCategory, idUser, name, limitMoney, colorTag, icon, typeIorE FROM category"
        conn = Database.createConnection()
        cursor = conn.cursor()
        result = cursor.execute(sql).fetchall()
        objects = [Category(*x) for x in result]
        conn.commit()
        conn.close()
        return objects

    @classmethod
    def getOne(cls, idCategory: int) -> Category:
        sql = "SELECT idCategory, idUser, name, limitMoney, colorTag, icon, typeIorE from category WHERE idCategory=?"
        conn = Database.createConnection()
        cursor = conn.cursor()
        result = cursor.execute(sql, (idCategory, )).fetchone()
        object = Category(*result)
        conn.commit()
        conn.close()
        return object

