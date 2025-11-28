from flask import Blueprint
from Controllers.Inventario_Controller import InventarioController

# Blueprint que agrupa todas las rutas relacionadas
# con el inventario de cartas de los usuarios.
# Se registrará en app.py con el prefijo /inventario
inventario_bp = Blueprint("inventario", __name__)

# ============================================================
#   POST /inventario/
#   Agrega un nuevo ítem al inventario de un usuario
# ============================================================
inventario_bp.post("/")(InventarioController.agregar)

# ============================================================
#   GET /inventario/<id_usuario>
#   Obtiene todos los ítems del inventario del usuario indicado
# ============================================================
inventario_bp.get("/<id_usuario>")(InventarioController.obtener_por_usuario)

# ============================================================
#   DELETE /inventario/item/<id>
#   Elimina un ítem del inventario por su ID
# ============================================================
inventario_bp.delete("/item/<id>")(InventarioController.eliminar)
