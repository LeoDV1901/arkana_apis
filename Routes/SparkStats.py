from flask import Blueprint, jsonify
from Controllers.SparkStatsController import EstadisticasController

spark_bp = Blueprint("spark_bp", __name__)

@spark_bp.route("", methods=["POST"])
def generar():
    return EstadisticasController.generar()
