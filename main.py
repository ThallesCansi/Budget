print("Options Menu")
print("-"*30)
print("1. Database Transactions")
print("2. Database Category")
print("3. Rodar Uvicorn")


option = 5
while option != 0:
    option = int(input("Options: "))
    if (option == 1 ):
        from mainTerminalTransaction import showMenu
        showMenu()
        
    elif (option == 2):
        from mainTerminalCategory import showMenu
        showMenu()
        
    elif (option == 3):
        import os
        os.system("uvicorn mainWeb:app --reload")
        
    






