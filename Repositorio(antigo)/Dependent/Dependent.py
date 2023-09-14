class Dependent:
    def __init__(self, idDependent, idUser, name, description, colorTag):
        self.idDependent = idDependent
        self.idUser = idUser 
        self.name = name
        self.description = description
        self.colorTag = colorTag
    
    def __str__(self):
        text = f"""
        ID Dependent: {self.idDependent}
        ID User: {self.idUser}
        Name: {self.name}
        Description: {self.description}
        Color Tag: {self.colorTag}
        """
        return text.strip()