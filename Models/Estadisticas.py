from datetime import datetime

class Estadistica:
    def __init__(self, data):
        # ID del usuario al que pertenecen estas estadísticas
        self.id_usuario = data.get("id_usuario")

        # Total de partidas ganadas por el usuario
        self.partidas_ganadas = data.get("partidas_ganadas", 0)

        # Total de partidas perdidas por el usuario
        self.partidas_perdidas = data.get("partidas_perdidas", 0)

        # Número total de cartas usadas por el usuario
        self.cartas_usadas = data.get("cartas_usadas", 0)

        # Ranking general del usuario dentro del juego
        self.ranking = data.get("ranking", 0)

        # Fecha de la última actualización de las estadísticas
        # Si no se proporciona, se usa la fecha actual en UTC
        self.fecha_actualizacion = data.get("fecha_actualizacion", datetime.utcnow())
