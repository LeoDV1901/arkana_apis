from flask import request, jsonify
from bson import ObjectId
from db import mongo
from Models.Carta_nfc import CartaNFC

class CartaNFCController:

    @staticmethod
    def crear():
        data = request.json
        card = CartaNFC(data).__dict__
        mongo.db.cartas_nfc.insert_one(card)
        return jsonify({"msg": "Carta NFC creada"}), 201

    @staticmethod
    def obtener_todas():
        cards = list(mongo.db.cartas_nfc.find())
        for c in cards:
            c["_id"] = str(c["_id"])
        return jsonify(cards)

    @staticmethod
    def obtener(id):
        c = mongo.db.cartas_nfc.find_one({"_id": ObjectId(id)})
        if not c:
            return jsonify({"error": "No encontrada"}), 404
        c["_id"] = str(c["_id"])
        return jsonify(c)

    @staticmethod
    def actualizar(id):
        data = request.json
        mongo.db.cartas_nfc.update_one({"_id": ObjectId(id)}, {"$set": data})
        return jsonify({"msg": "Actualizado"})

    @staticmethod
    def eliminar(id):
        mongo.db.cartas_nfc.delete_one({"_id": ObjectId(id)})
        return jsonify({"msg": "Eliminado"})
