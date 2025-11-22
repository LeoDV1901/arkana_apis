from datetime import datetime

class Sancion:
    def __init__(self, data):
        self.id_usuario = data.get("id_usuario")
        self.tipo = data.get("tipo")
        self.motivo = data.get("motivo")
        self.fecha_inicio = data.get("fecha_inicio", datetime.utcnow())
        self.fecha_fin = data.get("fecha_fin")
        self.aplicada_por = data.get("aplicada_por")
