from flask import jsonify
from Extensions import mongo


def obtener_estadisticas_globales():
    """
    Devuelve TODOS los documentos generados por Spark.
    """
    datos = list(mongo.db.estadisticas_globales.find({}, {"_id": 0}))
    return jsonify({"ok": True, "data": datos})


def obtener_ultima_estadistica_global():
    """
    Devuelve el documento más reciente según fecha_generado.
    """
    dato = mongo.db.estadisticas_globales.find_one(
        {},
        {"_id": 0},
        sort=[("fecha_generado", -1)]
    )

    if not dato:
        return jsonify({"ok": False, "msg": "No hay datos generados por Spark."}), 404

    return jsonify({"ok": True, "data": dato})
