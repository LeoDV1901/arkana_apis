from datetime import datetime

class CartaNFC:
    def __init__(self, data: dict):
        # IDs normalizados a string si vienen, sino None
        self.id_chip = str(data.get("id_chip")) if data.get("id_chip") is not None else None
        self.id_carta = str(data.get("id_carta")) if data.get("id_carta") is not None else None
        self.propietario_actual = str(data.get("propietario_actual")) if data.get("propietario_actual") is not None else None

        # Si la data trae fecha_creacion la usamos (p. ej. al leer de la DB).
        # Si no viene, la creamos ahora.
        fc = data.get("fecha_creacion")
        if isinstance(fc, datetime):
            self.fecha_creacion = fc
        elif isinstance(fc, str):
            # intentar parse simple ISO (siempre que la envíes como ISO)
            try:
                self.fecha_creacion = datetime.fromisoformat(fc)
            except Exception:
                self.fecha_creacion = datetime.utcnow()
        else:
            self.fecha_creacion = datetime.utcnow()

    def to_dict(self) -> dict:
        """Serializa para insertar/actualizar en la DB (fecha en ISO)."""
        return {
            "id_chip": self.id_chip,
            "id_carta": self.id_carta,
            "propietario_actual": self.propietario_actual,
            "fecha_creacion": self.fecha_creacion.isoformat()
        }

    def validate(self) -> (bool, str):
        """Validación mínima; devuelve (ok, mensaje)."""
        if not self.id_chip:
            return False, "id_chip es requerido"
        if not self.id_carta:
            return False, "id_carta es requerido"
        if not self.propietario_actual:
            return False, "propietario_actual es requerido"
        return True, "ok"
