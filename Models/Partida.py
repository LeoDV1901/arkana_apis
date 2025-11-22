from datetime import datetime

class Partida:
    def __init__(self, data):
        self.id_jugadores = data.get("id_jugadores", [])
        self.resultado = data.get("resultado", {})
        self.fecha = data.get("fecha", datetime.utcnow())
        self.cartas_usadas = data.get("cartas_usadas", [])
        self.modo = data.get("modo")
