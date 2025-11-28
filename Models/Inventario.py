from datetime import datetime

class Inventario:
    def __init__(self, data):
        # ID del usuario dueño del ítem en inventario
        self.id_usuario = data.get("id_usuario")

        # ID de la carta asociada (si aplica)
        self.id_carta = data.get("id_carta")

        # ID del chip NFC vinculado (si aplica)
        self.id_nfc = data.get("id_nfc")

        # Cantidad de unidades de esta carta o ítem
        # Por defecto, se asigna 1
        self.cantidad = data.get("cantidad", 1)

        # Fecha en que el usuario obtuvo este ítem
        # Si no se especifica, se usa la fecha actual (UTC)
        self.fecha_obtencion = data.get("fecha_obtencion", datetime.utcnow())
