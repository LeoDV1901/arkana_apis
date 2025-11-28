from datetime import datetime

class Carta:
    def __init__(self, data):
        # Nombre de la carta (obligatorio)
        self.nombre = data.get("nombre")

        # Breve descripción o historia de la carta
        self.descripcion = data.get("descripcion")

        # Tipo de carta (ejemplo: ataque, defensa, soporte, especial)
        self.tipo = data.get("tipo")

        # Rareza de la carta (común, rara, épica, legendaria, etc.)
        self.rareza = data.get("rareza")

        # Atributos principales de la carta
        self.vida = data.get("vida")          # Cantidad de vida o resistencia
        self.daño = data.get("daño")          # Daño base de la carta
        self.velocidad = data.get("velocidad")# Velocidad de ejecución/ataque
        self.mana = data.get("mana")          # Costo de uso

        # Fecha en que se creó la carta
        # Si no se especifica, se asigna automáticamente la fecha actual en UTC
        self.fecha_creacion = data.get("fecha_creacion", datetime.utcnow())

        # URL de la ilustración asociada a la carta (imagen)
        self.ilustracion_url = data.get("ilustracion_url")
