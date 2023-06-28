class Transaction:
    def __init__(self, idTransaction, idUser, idCategory, idAccount, idDependent, description, date, value, typeIorE):
        self.idTransaction = idTransaction
        self.idUser = idUser
        self.idCategory = idCategory
        self.idAccount = idAccount
        self.idDependent = idDependent
        self.description = description
        self.date = date
        self.value = value 
        self.typeIorE = typeIorE
   
    def __str__(self):
        text = f"""
        ID Transaction: {self.idTransaction}
        ID User: {self.idUser}
        ID Category: {self.idCategory}
        ID Account: {self.idAccount}
        ID Dependent: {self.idDependent}
        Description: {self.description}
        Date: {self.date}
        Value: {self.value}
        Type Income or Expense: {self.typeIorE}
        """
        return text.strip()