from typing import List
from Database import Database
from Transaction import Transaction

class TransactionRepo:
    @classmethod
    def createTable(cls):
        sql = """
                CREATE TABLE IF NOT EXISTS transactions
            (
                idTransaction INTEGER PRIMARY KEY AUTOINCREMENT,
                idUser INTEGER,
                idCategory INTEGER,
                idAccount INTEGER,
                idDependent INTEGER,
                description TEXT,
                date DATE,
                value REAL,
                typeIorE TEXT,
                FOREIGN KEY(idUser) REFERENCES user(idUser),
                FOREIGN KEY(idCategory) REFERENCES category(idCategory),
                FOREIGN KEY(idAccount) REFERENCES account(idAccount),
                FOREIGN KEY(idDependent) REFERENCES dependent(idDependent)
            )
              """
        conn = Database.createConnection()
        cursor = conn.cursor()
        tableCreated = (cursor.execute(sql).rowcount > 0)
        conn.commit()
        conn.close()
        return tableCreated
    
    @classmethod
    def insert(cls, transaction: Transaction) -> Transaction:  
        sql = """
                INSERT INTO transactions (idDependent, description, date, value, typeIorE)
                VALUES (?, ?, ?, ?, ?)
              """
        conn = Database.createConnection()
        cursor = conn.cursor()
        result = cursor.execute (sql, (transaction.idDependent, transaction.description, transaction.date, transaction.value, transaction.typeIorE))
        if (result.rowcount > 0):
            transaction.idTransaction = result.lastrowid   
        conn.commit()
        conn.close()
        return transaction
    
    # @classmethod
    # def update(cls, transaction: Transaction) -> Transaction:
    #     sql = "UPDATE transactions WHERE idTransaction=?"
    #     conn = Database.createConnection()
    #     cursor = conn.cursor()
    #     result = cursor.execute(sql, (transaction.idCategory, transaction.idAccount, transaction.idDependent, transaction.description, transaction.date, transaction.value))
    #     if (result.rowcount > 0):
    #         conn.commit()
    #         conn.close()
    #         return transaction
    #     else:
    #         conn.close()
    #         return None
    
    @classmethod
    def delete(cls, idTransaction: int) -> bool:
        sql="DELETE FROM transactions WHERE idTransaction=?"
        conn = Database.createConnection()
        cursor = conn.cursor()
        result = cursor.execute(sql, (idTransaction, ))
        if (result.rowcount > 0):
            conn.commit()
            conn.close()
            return True
        else:
            conn.close()
            return False

    @classmethod
    def getAll(cls) ->List[Transaction]:
        sql = "SELECT t.idTransaction, t.idUser, c.name, t.idAccount, d.name, t.description, t.date, t.value, t.typeIorE FROM transactions t INNER JOIN dependent d ON d.idDependent = t.idDependent INNER JOIN category c ON c.idCategory = t.idCategory"
        conn = Database.createConnection()
        cursor = conn.cursor()
        result = cursor.execute(sql).fetchall()
        objects = [Transaction(*x) for x in result]
        conn.commit()
        conn.close()
        return objects

    @classmethod
    def getOne(cls, idTransaction: int) -> Transaction:
        sql = "SELECT description FROM transactions WHERE idTransaction=?"
        conn = Database.createConnection()
        cursor = conn.cursor()
        result = cursor.execute(sql, (idTransaction, )).fetchone()
        object = Transaction(*result)
        conn.commit()
        conn.close()
        return object

