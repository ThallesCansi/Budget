print("Options Menu")
print("-"*30)
print("1. https://aplicacaoweb.budgetapp.repl.co/signUp-signIn")


option = 5
while option != 0:
    option = int(input("Options: "))
    if (option == 1):
        import os
<<<<<<< HEAD
        os.system("uvicorn mainWeb:app --reload")
=======
        os.system("uvicorn mainWeb:app --reload ")
>>>>>>> b608de8f364dadbc036b468eef6fe38efb750943
