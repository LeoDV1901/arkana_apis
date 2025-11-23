from flask import jsonify
from Controllers.Spark import EstadisticasService

class EstadisticasController:

    @staticmethod
    def generar():
        data = EstadisticasService.generar_estadisticas_spark()
        return jsonify(data), 200
