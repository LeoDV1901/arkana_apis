from datetime import datetime

class Inventario:
    def __init__(self, data):
        self.id_usuario = data.get("id_usuario")
        self.id_carta = data.get("id_carta")
        self.id_nfc = data.get("id_nfc")
        self.cantidad = data.get("cantidad", 1)
        self.fecha_obtencion = data.get("fecha_obtencion", datetime.utcnow())
