from flask import Blueprint, jsonify
from Extensions import mongo

estadisticas_bp = Blueprint("estadisticas", __name__)

@estadisticas_bp.route("/", methods=["GET"])
def obtener_estadisticas():
    datos = mongo.db.estadisticas_globales.find_one({}, {"_id": 0})
    return jsonify(datos or {"mensaje": "No hay estadísticas generadas"})
