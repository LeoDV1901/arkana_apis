from flask import Blueprint
from Controllers.Partida_Controller import PartidaController

# Blueprint que agrupa las rutas relacionadas con partidas.
# Se registrará en app.py con el prefijo /partidas
partida_bp = Blueprint("partidas", __name__)

# ============================================================
#   POST /partidas
#   Crea una nueva partida
# ============================================================
partida_bp.post("")(PartidaController.crear)

# ============================================================
#   GET /partidas/
#   Obtiene todas las partidas registradas
# ============================================================
partida_bp.get("/")(PartidaController.obtener_todas)

# ============================================================
#   GET /partidas/<id>
#   Obtiene una partida por su ID
# ============================================================
partida_bp.get("/<id>")(PartidaController.obtener)
