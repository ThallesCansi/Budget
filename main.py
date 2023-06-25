print("Options Menu")
print("-"*30)
print("1. Database User")
print("2. Database Category")
print("3. Rodar Uvicorn")


option = 5
while option != 0:
    option = int(input("Options: "))
    if (option == 1 ):
        from mainTerminalUser import showMenu
        showMenu()
        
    elif (option == 2):
        from mainTerminalCategory import showMenu
        showMenu()
        
    elif (option == 3):
        import os
        os.system("uvicorn mainWeb:app --reload --host=0.0.0.0 --port=5000")
        
    






