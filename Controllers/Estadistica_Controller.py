from flask import request, jsonify
from bson import ObjectId
from Extensions import mongo  # Se usa solo este, el otro estaba duplicado
from Models.Estadisticas import Estadistica


class EstadisticaController:

    @staticmethod
    def crear():
        data = request.json

        # Validación simple
        if not data:
            return jsonify({"error": "No se enviaron datos"}), 400

        # Crear modelo
        e = Estadistica(data).__dict__

        # Guardar en Mongo
        mongo.db.estadisticas.insert_one(e)

        return jsonify({"msg": "Estadística creada"}), 201

    @staticmethod
    def obtener_por_usuario(id_usuario):
        est = mongo.db.estadisticas.find_one({"id_usuario": id_usuario})

        if not est:
            return jsonify({"error": "No encontrado"}), 404

        # Convertir ID
        est["_id"] = str(est["_id"])

        return jsonify(est), 200

    @staticmethod
    def actualizar(id_usuario):
        data = request.json

        if not data:
            return jsonify({"error": "No se enviaron datos"}), 400

        result = mongo.db.estadisticas.update_one(
            {"id_usuario": id_usuario},
            {"$set": data}
        )

        if result.matched_count == 0:
            return jsonify({"error": "Usuario no encontrado"}), 404

        return jsonify({"msg": "Estadística actualizada"}), 200
