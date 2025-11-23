from flask import request, jsonify
from bson import ObjectId
from db import mongo
from Models.Sancion import Sancion
from Extensions import mongo

class SancionController:

    @staticmethod
    def crear():
        data = request.json
        sancion = Sancion(data).__dict__
        mongo.db.sanciones.insert_one(sancion)
        return jsonify({"msg": "Sanción aplicada"}), 201

    @staticmethod
    def obtener_por_usuario(id_usuario):
        sanciones = list(mongo.db.sanciones.find({"id_usuario": id_usuario}))
        for s in sanciones:
            s["_id"] = str(s["_id"])
        return jsonify(sanciones)

    @staticmethod
    def eliminar(id):
        mongo.db.sanciones.delete_one({"_id": ObjectId(id)})
        return jsonify({"msg": "Sanción eliminada"})
