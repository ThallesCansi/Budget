from typing import List
from Dependent import Dependent
from DependentRepo import DependentRepo
import os
import time
import replit

if DependentRepo.createTable():
    print("Table 'dependent' created.")

def showMenu():
    replit.clear()  
    print("Options Menu")
    print("-"*30)
    print("1. List Dependent")
    print("2. Insert Dependent")
    print("3. Update Dependent")
    print("4. Delete Dependent")
    print("5. Dependent Details")
    print("0. Close")


def showDependentTable(dependents: List[Dependent]):
    print("DEPENDENTS".center(19, "-"))
    print("-"*19)
    print("ID".center(6), "NAME".ljust(12))
    print("-"*19)
    for d in dependents:
        print(f"{str(d.idDependent).zfill(2).center(6)} {str(d.name).ljust(12)}")

def insertDependent():
    print("DEPENDENT INSERTION".center(19, "-"))
    print("-"*19)
    name = input("Type the name: ")
    description = input("Type the description: ")
    colorTag = input("Type the color tag: ")
    dependent = Dependent(0, 0, name, description, colorTag)
    processedDependent= DependentRepo.insert(dependent)
    if (processedDependent.idDependent > 0):
        print("Dependent inserted successfully!")
    else:
        print("Dependent could not be inserted.")

def updateDependent():
    print("DEPENDENT UPDATING".center(19, "-"))
    print("-"*19)    
    idDependent = input("Type the dependent id: ")

    dependent = DependentRepo.getOne(idDependent)
    idUser = dependent.idUser

    name = input(f"Type the name ({dependent.name}): ")
    description = input(f"Type the description ({dependent.description}): ")
    colorTag = input(f"Type the color tag ({dependent.colorTag}): ")

    name = name.strip() if name.strip() != "" else dependent.name
    description = description.strip() if description.strip() != "" else dependent.description
    colorTag = colorTag.strip() if colorTag.strip() != "" else dependent.colorTag

    modifiedDependent = Dependent(idDependent, idUser, name, description, colorTag)
    processedDependent = DependentRepo.update(modifiedDependent)
    if (processedDependent != None):
        print("Dependent updated successfully!")
    else: 
        print("Dependent could not be updated.")


def deleteDependent():
    print('DEPENDENT  DELETION'.center(19, "-"))
    print("-"*19)    
    id = input("Type the dependent id: ")
    
    dependent = DependentRepo.getOne(id)
    confirmation = input(f"Do you really wanna exclude dependent {dependent.name}?  (Y/N): ")

    if (confirmation.upper() == "Y"):
        if DependentRepo.delete(id):    
            print("Dependent deleted successfully!")
        else: 
            print("Dependent could not be deleted.")
    else:
        print("Operation cancelled.")

def showDependentDetails():
    print("DEPENDENT DETAILS".center(19, "-"))
    print("-"*19)    
    id = input("Type the dependent id: ")
    
    dependent = DependentRepo.getOne(id)
    print(f"Id: {dependent.idDependent}")
    print(f"Id User: {dependent.idUser}")
    print(f"Name: {dependent.name}")
    print(f"Description: {dependent.description}")
    print(f"Color Tag: {dependent.colorTag}")

def processOption(option):
    replit.clear()
    if (option == 1):
        dependents = DependentRepo.getAll()
        showDependentTable(dependents)
    elif (option == 2):
        insertDependent()
    elif (option == 3):
        updateDependent()
    elif (option == 4):
        deleteDependent()
    elif (option == 5):
        showDependentDetails()

    time.sleep(3)

option = -1
while (option != 6):
    showMenu()
    option = int(input("Your Option: "))
    processOption(option)