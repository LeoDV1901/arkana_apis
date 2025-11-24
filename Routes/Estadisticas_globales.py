from flask import Blueprint
from Controllers.EstadisticasGlobales import (
    obtener_estadisticas_globales,
    obtener_ultima_estadistica_global
)

estadisticasG_bp = Blueprint("estadisticas_globales", __name__)

# Ruta para obtener TODAS las estadísticas generadas
estadisticasG_bp.get("")(obtener_estadisticas_globales)

# Ruta para obtener SOLO el último documento
estadisticasG_bp.get("/ultimas")(obtener_ultima_estadistica_global)
