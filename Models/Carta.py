from datetime import datetime

class Carta:
    def __init__(self, data):
        self.nombre = data.get("nombre")
        self.descripcion = data.get("descripcion")
        self.tipo = data.get("tipo")
        self.rareza = data.get("rareza")
        self.vida = data.get("vida")
        self.daño = data.get("daño")
        self.velocidad = data.get("velocidad")
        self.mana = data.get("mana")
        self.fecha_creacion = data.get("fecha_creacion", datetime.utcnow())
        self.ilustracion_url = data.get("ilustracion_url")
