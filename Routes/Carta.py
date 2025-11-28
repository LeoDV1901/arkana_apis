from flask import Blueprint
from Controllers.Carta_Controller import CartaController

# Blueprint que agrupa todas las rutas relacionadas con las cartas
# Se registrará en app.py con el prefijo /cartas
carta_bp = Blueprint("cartas", __name__)

# ============================================================
#   POST /cartas
#   Crea una nueva carta
# ============================================================
carta_bp.post("")(CartaController.crear)

# ============================================================
#   GET /cartas/
#   Obtiene todas las cartas registradas
# ============================================================
carta_bp.get("/")(CartaController.obtener_todas)

# ============================================================
#   GET /cartas/<id>
#   Obtiene la información de una carta específica
# ============================================================
carta_bp.get("/<id>")(CartaController.obtener)

# ============================================================
#   PUT /cartas/<id>
#   Actualiza una carta existente por su ID
# ============================================================
carta_bp.put("/<id>")(CartaController.actualizar)

# ============================================================
#   DELETE /cartas/<id>
#   Elimina una carta por su ID
# ============================================================
carta_bp.delete("/<id>")(CartaController.eliminar)
