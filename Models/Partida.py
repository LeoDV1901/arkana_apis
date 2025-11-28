from datetime import datetime

class Partida:
    def __init__(self, data):
        # Lista de IDs de los jugadores que participaron en la partida
        # Por defecto una lista vacía si no se envía
        self.id_jugadores = data.get("id_jugadores", [])

        # Resultado de la partida (ganador, puntajes, etc.)
        # Se define como un diccionario flexible
        self.resultado = data.get("resultado", {})

        # Fecha en la que se jugó la partida
        # Si no se proporciona, se usa la fecha actual en UTC
        self.fecha = data.get("fecha", datetime.utcnow())

        # Lista de cartas usadas en la partida
        # Generalmente contiene IDs de cartas o estadísticas asociadas
        self.cartas_usadas = data.get("cartas_usadas", [])

        # Modo de juego seleccionado (por ejemplo: clásico, ranked, torneo)
        self.modo = data.get("modo")
