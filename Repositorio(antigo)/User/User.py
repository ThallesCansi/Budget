class User:
    def __init__(self, idUser, name, email, birth, password, phone, state, city):
        self.idUser = idUser
        self.name = name
        self.email = email
        self.birth = birth
        self.password = password
        self.phone = phone
        self.state = state
        self.city = city

    def __str__(self):
        text = f"""
        ID User: {self.id}
        Name: {self.name}
        Email: {self.email}
        Birth: {self.birth}
        Password: {self.password}
        Phone: {self.phone}
        State: {self.state}
        City: {self.city}
        """
        return text.strip()
        