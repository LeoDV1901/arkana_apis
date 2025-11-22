from datetime import datetime

class Estadistica:
    def __init__(self, data):
        self.id_usuario = data.get("id_usuario")
        self.partidas_ganadas = data.get("partidas_ganadas", 0)
        self.partidas_perdidas = data.get("partidas_perdidas", 0)
        self.cartas_usadas = data.get("cartas_usadas", 0)
        self.ranking = data.get("ranking", 0)
        self.fecha_actualizacion = data.get("fecha_actualizacion", datetime.utcnow())
