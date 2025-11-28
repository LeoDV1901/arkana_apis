from datetime import datetime

class CartaNFC:
    def __init__(self, data: dict):
        """
        Representa una carta física NFC vinculada a una carta digital.
        Se asegura que los campos esenciales existan y estén normalizados.
        """

        # Normalizar ID como string sin espacios
        self.id_chip = self._normalize_string(data.get("id_chip"))
        self.id_carta = self._normalize_string(data.get("id_carta"))
        self.propietario_actual = self._normalize_string(data.get("propietario_actual"))

        # Manejo de fecha
        fc = data.get("fecha_creacion")
        self.fecha_creacion = self._parse_datetime(fc)

    # ---------------------------------------
    # MÉTODOS PRIVADOS
    # ---------------------------------------

    def _normalize_string(self, value):
        """Convierte valores a string limpiando espacios; retorna None si viene vacío."""
        if value is None:
            return None
        value = str(value).strip()
        return value if value else None

    def _parse_datetime(self, value):
        """Convierte una fecha en datetime; si falla, usa ahora."""
        if isinstance(value, datetime):
            return value

        if isinstance(value, str):
            try:
                return datetime.fromisoformat(value)
            except Exception:
                pass

        return datetime.utcnow()

    # ---------------------------------------
    # MÉTODOS PÚBLICOS
    # ---------------------------------------

    def to_dict(self) -> dict:
        """Serializa el objeto para guardarlo en MongoDB."""
        return {
            "id_chip": self.id_chip,
            "id_carta": self.id_carta,
            "propietario_actual": self.propietario_actual,
            "fecha_creacion": self.fecha_creacion.isoformat()
        }

    def validate(self) -> (bool, str):
        """Validación mínima; devuelve (ok, mensaje)."""
        if not self.id_chip:
            return False, "El campo 'id_chip' es obligatorio."
        if not self.id_carta:
            return False, "El campo 'id_carta' es obligatorio."
        if not self.propietario_actual:
            return False, "El campo 'propietario_actual' es obligatorio."

        return True, "ok"
