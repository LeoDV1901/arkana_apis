from datetime import datetime

class Usuario:
    def __init__(self, data):
        # Nombre público del usuario dentro del sistema
        self.nickname = data.get("nickname")

        # Correo electrónico del usuario (usado para login y notificaciones)
        self.correo = data.get("correo")

        # Contraseña del usuario (debería almacenarse hasheada en la BD)
        self.contraseña = data.get("contraseña")

        # Número telefónico del usuario
        self.telefono = data.get("telefono")

        # Fecha en la que el usuario se registró
        # Si no se envía, se asigna la fecha actual (UTC)
        self.fecha_registro = data.get("fecha_registro", datetime.utcnow())

        # Fecha y hora del último inicio de sesión registrado
        self.ultimo_login = data.get("ultimo_login")

        # Estado de la cuenta: activo, suspendido, eliminado, etc.
        self.estado_cuenta = data.get("estado_cuenta", "activo")

        # Rol del usuario dentro del sistema: jugador, administrador, etc.
        self.rol = data.get("rol", "jugador")
