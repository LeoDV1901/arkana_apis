from flask import jsonify
from Controllers.Spark import EstadisticasService

class EstadisticasController:

    @staticmethod
    def generar():
        """
        Controlador encargado de solicitar la generación de estadísticas globales.

        Flujo:
        1. Llama al servicio EstadisticasService, que ejecuta el proceso en Spark.
        2. Spark genera estadísticas y devuelve una respuesta (generalmente un dict).
        3. El controlador regresa esa información como JSON.
        """
        
        # Llamada al servicio que ejecuta el proceso en Spark
        data = EstadisticasService.generar_estadisticas_spark()

        # Se retorna la respuesta con status 200
        return jsonify(data), 200
