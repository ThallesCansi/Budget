from typing import List
from Transaction import Transaction
from TransactionRepo import TransactionRepo
import os
import time

if TransactionRepo.createTable():
    print("Table 'Transaction' created.")

def showMenu():
    os.system("cls")  
    print("Options Menu")
    print("-"*30)
    print("1. List Transactions")
    print("2. Insert Transaction")
    print("3. Update Transaction")
    print("4. Delete Transaction")
    print("5. Transaction Details")
    print("0. Close")


def showTransactionTable(transactions: List[Transaction]):
    print("TRANSACTIONS".center(19, "-"))
    print("-"*19)
    print("DESCRIPTION".center(6), "VALUE".ljust(12))
    print("-"*19)
    for t in transactions:
        print(f"{str(t.description).zfill(2).center(6)} {str(t.value).ljust(12)}")

def insertTransaction():
    print("TRANSACTION INSERTION".center(19, "-"))
    print("-"*19)
    description = input("Type the description: ")
    date = input("Type the date: ")
    value = float(input("Type the value: "))
    # typeIorE = input("Type the value: ")
    transaction = Transaction(0, 0, 0, 0, 0, description, date, value, 0)
    processedTransaction = TransactionRepo.insert(transaction)
    if (processedTransaction.idTransaction > 0):
        print("Transaction inserted successfully!")
    else:
        print("Transaction could not be inserted.")

def updateTransaction():
    print("TRANSACTION UPDATING".center(19, "-"))
    print("-"*19)    
    idTransaction = input("Type the transaction id: ")

    transaction = TransactionRepo.getOne(idTransaction)
    idUser = transaction.idUser
    idCategory = transaction.idCategory
    idAccount = transaction.idAccount
    idDependent = transaction.idDependent
    
    description = input(f"Type the description ({transaction.description}): ")
    date = input(f"Type the date ({transaction.date}): ")
    value = input(f"Type the value ({transaction.value}): ")

    description = description.strip() if description.strip() != "" else transaction.description
    date = date.strip() if date.strip() != "" else transaction.date
    value = value.strip() if value.strip() != "" else transaction.value

    modifiedTransaction = Transaction(idTransaction, idUser, idCategory, idAccount, idDependent, description, date, value)
    processedTransaction = TransactionRepo.update(modifiedTransaction)
    if (processedTransaction != None):
        print("Transaction updated successfully!")
    else: 
        print("Transaction could not be updated.")


def deleteTransaction():
    print('TRANSACTION  DELETION'.center(19, "-"))
    print("-"*19)    
    id = input("Type the transaction id: ")
    
    transaction = TransactionRepo.getOne(id)
    confirmation = input(f"Do you really wanna exclude transaction {transaction.description}?  (Y/N): ")

    if (confirmation.upper() == "Y"):
        if TransactionRepo.delete(id):    
            print("Transaction deleted successfully!")
        else: 
            print("Transaction could not be deleted.")
    else:
        print("Operation cancelled.")

def showTransactionDetails():
    print("TRANSACTION DETAILS".center(19, "-"))
    print("-"*19)    
    id = input("Type the transaction id: ")
    
    transaction = TransactionRepo.getOne(id)
    print(f"ID Transaction: {transaction.idTransaction}")
    print(f"ID User: {transaction.idUser}")
    print(f"ID Category: {transaction.idCategory}")
    print(f"ID Account: {transaction.idAccount}")
    print(f"ID Dependent: {transaction.idDependent}")
    print(f"Description: {transaction.description}")
    print(f"Data: {transaction.date}")
    print(f"Value: {transaction.value}")
    print(f"Income or Expense: {transaction.typeIorE}")

def processOption(option):
    os.system("cls")
    if (option == 1):
        transactions = TransactionRepo.getAll()
        showTransactionTable(transactions)
    elif (option == 2):
        insertTransaction()
    elif (option == 3):
        updateTransaction()
    elif (option == 4):
        deleteTransaction()
    elif (option == 5):
        showTransactionDetails()

    time.sleep(3)

option = -1
while (option != 6):
    showMenu()
    option = int(input("Your Option: "))
    processOption(option)