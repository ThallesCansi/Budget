from typing import List
from Repositorio.Database import Database
from Repositorio.Account.Account import Account

class AccountRepo:
    @classmethod
    def createTable(cls):
        sql = """
                CREATE TABLE IF NOT EXISTS account
            (
                idAccount INTEGER PRIMARY KEY AUTOINCREMENT,
                idUser INTEGER,
                title TEXT NOT NULL,
                balance DECIMAL NOT NULL,
                goal TEXT,
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
    def insert(cls, account: Account) -> Account:  
        sql = """
                INSERT INTO account (title, balance, goal)
                VALUES (?, ?, ?)
              """
        conn = Database.createConnection()
        cursor = conn.cursor()
        result = cursor.execute (sql, (account.title, account.balance, account.goal))
        if (result.rowcount > 0):
            account.idAccount = result.lastrowid   
        conn.commit()
        conn.close()
        return account
    
    @classmethod
    def update(cls, account: Account) -> Account:  
        sql = "UPDATE account SET title=?, balance=?, goal=? WHERE idAccount=?"
        conn = Database.createConnection()
        cursor = conn.cursor()
        result = cursor.execute(sql, (account.title, account.balance, account.goal, account.idAccount))
        if (result.rowcount > 0):
            conn.commit()
            conn.close()
            return account
        else:
            conn.close()
            return None
    
    @classmethod
    def delete(cls, idAccount: int) -> bool:
        sql="DELETE FROM account WHERE idAccount=?"
        conn = Database.createConnection()
        cursor = conn.cursor()
        result = cursor.execute(sql, (idAccount, ))
        if (result.rowcount > 0):
            conn.commit()
            conn.close()
            return True
        else:
            conn.close()
            return False

    @classmethod
    def getAll(cls) ->List[Account]:
        sql = "SELECT idAccount, idUser, title, balance, goal FROM account a"
        conn = Database.createConnection()
        cursor = conn.cursor()
        result = cursor.execute(sql).fetchall()
        objects = [Account(*x) for x in result]
        conn.commit()
        conn.close()
        return objects

    @classmethod
    def getOne(cls, idAccount: int) -> Account:
        sql = "SELECT idAccount, idUser, title, balance, goal FROM account WHERE idAccount=?"
        conn = Database.createConnection()
        cursor = conn.cursor()
        result = cursor.execute(sql, (idAccount, )).fetchone()
        object = Account(*result)
        conn.commit()
        conn.close()
        return object

