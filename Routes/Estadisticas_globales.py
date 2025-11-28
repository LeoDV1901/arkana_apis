from flask import Blueprint
from Controllers.EstadisticasGlobales import (
    obtener_estadisticas_globales,
    obtener_ultima_estadistica_global
)

# Blueprint que agrupa todas las rutas relacionadas con las
# estadísticas globales generadas por Spark.
# Se registrará en app.py con el prefijo /SparkResultados
estadisticasG_bp = Blueprint("estadisticas_globales", __name__)

# ============================================================
#   GET /SparkResultados
#   Obtiene TODOS los documentos de estadísticas globales
# ============================================================
estadisticasG_bp.get("")(obtener_estadisticas_globales)

# ============================================================
#   GET /SparkResultados/ultimas
#   Obtiene ÚNICAMENTE el último documento generado por Spark
# ============================================================
estadisticasG_bp.get("/ultimas")(obtener_ultima_estadistica_global)
