from flask import Blueprint
from Controllers.Estadistica_Controller import EstadisticaController

# Blueprint que agrupa todas las rutas relacionadas
# con las estadísticas individuales de cada usuario.
# Este blueprint se registrará en app.py con el prefijo /estadisticas
estadistica_bp = Blueprint("estadisticas", __name__)

# ============================================================
#   POST /estadisticas/
#   Crea un registro de estadísticas para un usuario
# ============================================================
estadistica_bp.post("/")(EstadisticaController.crear)

# ============================================================
#   GET /estadisticas/<id_usuario>
#   Obtiene las estadísticas del usuario indicado por su ID
# ============================================================
estadistica_bp.get("/<id_usuario>")(EstadisticaController.obtener_por_usuario)

# ============================================================
#   PUT /estadisticas/<id_usuario>
#   Actualiza las estadísticas del usuario indicado
# ============================================================
estadistica_bp.put("/<id_usuario>")(EstadisticaController.actualizar)
