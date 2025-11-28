from flask import Blueprint
from Controllers.Carta_nfc_Controller import CartaNFCController

# Blueprint para agrupar todas las rutas relacionadas
# con las cartas NFC dentro del sistema.
# En app.py se registrará con el prefijo /cartas_nfc
carta_nfc_bp = Blueprint("cartas_nfc", __name__)

# ============================================================
#   POST /cartas_nfc
#   Crea una nueva carta NFC
# ============================================================
carta_nfc_bp.post("")(CartaNFCController.crear)

# ============================================================
#   GET /cartas_nfc/
#   Obtiene todas las cartas NFC registradas
# ============================================================
carta_nfc_bp.get("/")(CartaNFCController.obtener_todas)

# ============================================================
#   GET /cartas_nfc/<id>
#   Obtiene los datos de una carta NFC por su ID
# ============================================================
carta_nfc_bp.get("/<id>")(CartaNFCController.obtener)

# ============================================================
#   PUT /cartas_nfc/<id>
#   Actualiza una carta NFC por su ID
# ============================================================
carta_nfc_bp.put("/<id>")(CartaNFCController.actualizar)

# ============================================================
#   DELETE /cartas_nfc/<id>
#   Elimina una carta NFC por su ID
# ============================================================
carta_nfc_bp.delete("/<id>")(CartaNFCController.eliminar)
