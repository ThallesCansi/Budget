print("Options Menu")
print("-"*30)
print("1. https://aplicacaoweb.budgetapp.repl.co/signUp-signIn")


option = 5
while option != 0:
    option = int(input("Options: "))
    if (option == 1):
        import os
        os.system("uvicorn mainWeb:app --reload --host=0.0.0.0 --port=5000")