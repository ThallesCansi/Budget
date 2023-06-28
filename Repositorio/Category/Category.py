class Category:
    def __init__(self, idCategory, idUser, name, limit, colorTag, icon, typeIorE):
        self.idCategory = idCategory
        self.idUser = idUser 
        self.name = name
        self.limit = limit
        self.colorTag = colorTag
        self.icon = icon
        self.typeIorE = typeIorE
    
    def __str__(self):
        text = f"""
        ID Category: {self.idCategory}
        ID User: {self.idUser}
        Name: {self.name}
        Limit: {self.limit}
        Color Tag: {self.colorTag}
        Icon: {self.icon}
        Type - Income or Expense: {self.typeIorE}
        """
        return text.strip()
        