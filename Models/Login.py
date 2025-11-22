from werkzeug.security import check_password_hash

class UsuarioLogin:
    def __init__(self, data):
        self.email = data.get("email")
        self.password = data.get("password")

    def validar_password(self, hashed_password):
        return check_password_hash(hashed_password, self.password)
