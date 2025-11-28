from datetime import datetime

class Sancion:
    def __init__(self, data):
        # ID del usuario al que se le aplica la sanción
        self.id_usuario = data.get("id_usuario")

        # Tipo de sanción: advertencia, suspensión, bloqueo, etc.
        self.tipo = data.get("tipo")

        # Motivo detallado de la sanción
        self.motivo = data.get("motivo")

        # Fecha en que inicia la sanción
        # Si no se recibe, se asigna la fecha actual (UTC)
        self.fecha_inicio = data.get("fecha_inicio", datetime.utcnow())

        # Fecha en que termina la sanción, opcional según el tipo
        self.fecha_fin = data.get("fecha_fin")

        # Identificador de quien aplicó la sanción (admin)
        self.aplicada_por = data.get("aplicada_por")
