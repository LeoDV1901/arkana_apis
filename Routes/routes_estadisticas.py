from flask import Blueprint, jsonify
from Extensions import mongo

# Blueprint encargado de las rutas relacionadas con estadísticas globales.
# Se registrará en app.py con el prefijo /estadisticas
estadisticas_bp = Blueprint("estadisticas", __name__)

@estadisticas_bp.route("/", methods=["GET"])
def obtener_estadisticas():
    """
    Obtiene un documento con las estadísticas globales generadas por Spark.
    Busca el registro más reciente en la colección 'estadisticas_globales'.
    Se excluye el campo _id para evitar problemas de serialización en JSON.
    """

    # Recupera un documento (find_one toma cualquiera si no se especifica orden)
    datos = mongo.db.estadisticas_globales.find_one({}, {"_id": 0})

    # Si no existen datos, se responde un mensaje por defecto
    return jsonify(datos or {"mensaje": "No hay estadísticas generadas"})
