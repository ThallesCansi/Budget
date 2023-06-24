from typing import List
from Category import Category
from CategoryRepo import CategoryRepo
import os
import time

if CategoryRepo.createTable():
    print("Table 'category' created.")

def showMenu():
    os.system("cls")  
    print("Options Menu")
    print("-"*30)
    print("1. List Category")
    print("2. Insert Category")
    print("3. Update Category")
    print("4. Delete Category")
    print("5. Category Details")
    print("0. Close")


def showCategoryTable(categories: List[Category]):
    print("CATEGORIES".center(19, "-"))
    print("-"*19)
    print("ID".center(6), "NAME".ljust(12))
    print("-"*19)
    for c in categories:
        print(f"{str(c.idCategory).zfill(2).center(6)} {str(c.name).ljust(12)}")

def insertCategory():
    print("CATEGORY INSERTION".center(19, "-"))
    print("-"*19)
    name = input("Type the name: ")
    limit = float(input("Type the limit money: "))
    colorTag = input("Type the color tag: ")
    icon = input("Aattach icon: ")
    typeIorE = input("Type I: income or E: expense: ")
    category = Category(0, 0, name, limit, colorTag, icon, typeIorE)
    processedCategory= CategoryRepo.insert(category)
    if (processedCategory.idCategory > 0):
        print("Category inserted successfully!")
    else:
        print("Category could not be inserted.")

def updateCategory():
    print("CATEGORY UPDATING".center(19, "-"))
    print("-"*19)    
    idCategory = input("Type the category id: ") 

    category = CategoryRepo.getOne(idCategory)
    idUser = category.idUser

    name = input(f"Type the name ({category.name}): ")
    limit = input(f"Type the limit money ({category.limit}): ")
    colorTag = input(f"Type the color tag ({category.colorTag}): ")
    icon = input(f"Aattach icon ({category.icon}): ")
    typeIorE = input(f"Type the type of category (I: income or E: expense) ({category.typeIorE}): ")

    name = name.strip() if name.strip() != "" else category.name
    limit = limit.strip() if limit.strip() != "" else category.limit
    colorTag = colorTag.strip() if colorTag.strip() != "" else category.colorTag
    icon = icon.strip() if icon.strip() != "" else category.icon
    typeIorE = typeIorE.strip() if typeIorE.strip() != "" else category.typeIorE

    modifiedCategory = Category(idCategory, idUser, name, float(limit), colorTag, icon, typeIorE)
    processedCategory = CategoryRepo.update(modifiedCategory)
    if (processedCategory != None):
        print("Category updated successfully!")
    else: 
        print("Category could not be updated.")


def deleteCategory():
    print('CATEGORY DELETION'.center(19, "-"))
    print("-"*19)    
    id = input("Type the Category id: ")
    
    category = CategoryRepo.getOne(id)
    confirmation = input(f"Do you really wanna exclude category {category.name}? (Y/N)")

    if (confirmation.upper() == "Y"):
        if CategoryRepo.delete(id):    
            print("Category deleted successfully!")
        else: 
            print("Category could not be deleted.")
    else:
        print("Operation cancelled.")

def showCategoryDetails():
    print("CATEGORY DETAILS".center(19, "-"))
    print("-"*19)    
    id = input("Type the category id: ")
    
    category = CategoryRepo.getOne(id)
    print(f"Id: {category.idCategory}")
    print(f"Id User: {category.idUser}")
    print(f"Name: {category.name}")
    print(f"Limit Money: {category.limit}")
    print(f"Color Tag: {category.colorTag}")
    print(f"Icon: {category.icon}")
    print(f"Type I or E (Income or Expense): {category.typeIorE}")
    
def processOption(option):
    os.system("cls")
    if (option == 1):
        categories = CategoryRepo.getAll()
        showCategoryTable(categories)
    elif (option == 2):
        insertCategory()
    elif (option == 3):
        updateCategory()
    elif (option == 4):
        deleteCategory()
    elif (option == 5):
        showCategoryDetails()


    time.sleep(3)

option = -1
while (option != 6):
    showMenu()
    option = int(input("Your Option: "))
    processOption(option)