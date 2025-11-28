class UsuarioLogin:
    def __init__(self, data):
        # Correo ingresado por el usuario al iniciar sesión
        self.correo = data.get("correo")

        self.contraseña = data.get("contraseña")

    def validar_password(self, contraseña_guardada):
        """
        Valida la contraseña ingresada contra la almacenada.

        Actualmente es una comparación en texto plano.
        Para un entorno real, esto debe sustituirse por una 
        comparación con hash (bcrypt, werkzeug.security, etc.).
        """
        return self.contraseña == contraseña_guardada
