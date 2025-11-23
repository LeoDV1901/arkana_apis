class UsuarioLogin:
    def __init__(self, data):
        self.correo = data.get("correo")
        self.contraseña = data.get("contraseña")

    def validar_password(self, contraseña_guardada):
        # Comparación directa de texto plano
        return self.contraseña == contraseña_guardada
