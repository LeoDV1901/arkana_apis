from datetime import datetime

class Usuario:
    def __init__(self, data):
        self.nickname = data.get("nickname")
        self.correo = data.get("correo")
        self.contraseña_hash = data.get("contraseña_hash")
        self.telefono = data.get("telefono")
        self.fecha_registro = data.get("fecha_registro", datetime.utcnow())
        self.ultimo_login = data.get("ultimo_login")
        self.estado_cuenta = data.get("estado_cuenta", "activo")
        self.rol = data.get("rol", "jugador")
