from flask import request, jsonify
from bson import ObjectId
from db import mongo
from Models.Carta import Carta
from Extensions import mongo

class CartaController:

    @staticmethod
    def crear():
        data = request.json
        carta = Carta(data).__dict__
        mongo.db.cartas.insert_one(carta)
        return jsonify({"msg": "Carta creada"}), 200

    @staticmethod
    def obtener_todas():
        cartas = list(mongo.db.cartas.find())
        for c in cartas:
            c["_id"] = str(c["_id"])
        return jsonify(cartas)

    @staticmethod
    def obtener(id):
        c = mongo.db.cartas.find_one({"_id": ObjectId(id)})
        if not c:
            return jsonify({"error": "Carta no encontrada"}), 404
        c["_id"] = str(c["_id"])
        return jsonify(c)

    @staticmethod
    def actualizar(id):
        data = request.json
        mongo.db.cartas.update_one({"_id": ObjectId(id)}, {"$set": data})
        return jsonify({"msg": "Carta actualizada"})

    @staticmethod
    def eliminar(id):
        mongo.db.cartas.delete_one({"_id": ObjectId(id)})
        return jsonify({"msg": "Carta eliminada"})
