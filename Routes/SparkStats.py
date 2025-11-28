from flask import Blueprint, jsonify
from Controllers.SparkStatsController import EstadisticasController

# Se crea el Blueprint que agrupa las rutas relacionadas con estadísticas vía Spark.
# Este blueprint se registrará en app.py con el prefijo configurado (por ejemplo: /arrancarSpark)
spark_bp = Blueprint("spark_bp", __name__)

# -------------------------------------------------------
# Ruta para iniciar la generación de estadísticas con Spark
# -------------------------------------------------------
@spark_bp.route("", methods=["POST"])
def generar():
    """
    Llama al controlador encargado de ejecutar el proceso de Spark.
    La función generar() en el controlador debe devolver un JSON con
    el resultado o un mensaje de estado.
    """
    return EstadisticasController.generar()
