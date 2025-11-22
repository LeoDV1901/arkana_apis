from flask import request, jsonify
from bson import ObjectId
from db import mongo
from Models.Estadisticas import Estadistica

class EstadisticaController:

    @staticmethod
    def crear():
        data = request.json
        e = Estadistica(data).__dict__
        mongo.db.estadisticas.insert_one(e)
        return jsonify({"msg": "Estadística creada"}), 201

    @staticmethod
    def obtener_por_usuario(id_usuario):
        est = mongo.db.estadisticas.find_one({"id_usuario": id_usuario})
        if not est:
            return jsonify({"error": "No encontrado"}), 404
        est["_id"] = str(est["_id"])
        return jsonify(est)

    @staticmethod
    def actualizar(id_usuario):
        data = request.json
        mongo.db.estadisticas.update_one({"id_usuario": id_usuario}, {"$set": data})
        return jsonify({"msg": "Estadística actualizada"})
