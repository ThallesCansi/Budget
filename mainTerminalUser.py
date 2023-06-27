from typing import List
from User import User
from UserRepo import UserRepo
import os
import time
import replit

if UserRepo.createTable():
    print("Table 'user' created.")


def showMenu():
    replit.clear()
    print("Options Menu")
    print("-"*30)
    print("1. List User")
    print("2. Insert User")
    print("0. Close")


def showUserTable(users: List[User]):
    print("USERS".center(19, "-"))
    print("-"*19)
    print("ID".center(6), "NAME".ljust(12))
    print("-"*19)
    for u in users:
        print(f"{str(u.idUser).zfill(2).center(6)} {str(u.name).ljust(12)}")


def insertUser():
    print("USER INSERTION".center(19, "-"))
    print("-"*19)
    name = input("Type the name: ")
    email = input("Type the email: ")
    birth = input("Type the birth: ")
    password = input("Type the password: ")
    phone = input("Type the phone number: ")
    state = input("Type the state state: ")
    city = input("Type the city: ")
    user = User(0, name, email, birth, password, phone, state, city)
    processedUser = UserRepo.insert(user)
    if (processedUser.id > 0):
        print("User inserted successfully!")
    else:
        print("User could not be inserted.")

def processOption(option):
    replit.clear()
    if (option == 1):
        users = UserRepo.getAll()
        showUserTable(users)
    elif (option == 2):
        insertUser()

    time.sleep(3)


option = -1
while (option != 0):
    showMenu()
    option = int(input("Your Option: "))
    processOption(option)
