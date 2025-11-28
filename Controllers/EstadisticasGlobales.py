from flask import jsonify
from Extensions import mongo


def obtener_estadisticas_globales():
    """
    Obtiene TODOS los documentos generados por Spark desde la colección
    'estadisticas_globales'.

    - No se devuelve el campo "_id" porque no es serializable como JSON.
    - Regresa un arreglo con todas las estadísticas almacenadas.
    """
    datos = list(
        mongo.db.estadisticas_globales.find(
            {},          # sin filtro
            {"_id": 0}   # excluir _id del resultado
        )
    )

    return jsonify({
        "ok": True,
        "data": datos
    })


def obtener_ultima_estadistica_global():
    """
    Obtiene SOLO el documento más reciente generado por Spark.
    Esto se define usando el campo 'fecha_generado' en orden descendente.

    - Si no hay datos, devuelve un mensaje con status 404.
    - Si existe, retorna el último documento sin el campo _id.
    """
    dato = mongo.db.estadisticas_globales.find_one(
        {},
        {"_id": 0},          # excluir _id
        sort=[("fecha_generado", -1)]  # ordenar DESC por fecha_generado
    )

    if not dato:
        return jsonify({
            "ok": False,
            "msg": "No hay datos generados por Spark."
        }), 404

    return jsonify({
        "ok": True,
        "data": dato
    })
