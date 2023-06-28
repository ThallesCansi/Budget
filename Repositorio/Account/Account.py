class Account:
    def __init__(self, idAccount, idUser, title, balance, goal):
        self.idAccount = idAccount
        self.idUser = idUser
        self.title = title
        self.balance = balance
        self.goal = goal
   
    def __str__(self):
        text = f"""
        ID Account: {self.idAccount}
        ID User: {self.idUser}
        Title: {self.title}
        Balance: {self.balance}
        Goal: {self.goal}
        """
        return text.strip()