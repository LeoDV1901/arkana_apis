from flask import request, jsonify
from bson import ObjectId
from db import mongo
from Models.Partida import Partida
from Extensions import mongo

class PartidaController:

    @staticmethod
    def crear():
        data = request.json
        partida = Partida(data).__dict__
        mongo.db.partidas.insert_one(partida)
        return jsonify({"msg": "Partida registrada"}), 201

    @staticmethod
    def obtener_todas():
        partidas = list(mongo.db.partidas.find())
        for p in partidas:
            p["_id"] = str(p["_id"])
        return jsonify(partidas)

    @staticmethod
    def obtener(id):
        p = mongo.db.partidas.find_one({"_id": ObjectId(id)})
        if not p:
            return jsonify({"error": "No encontrada"}), 404
        p["_id"] = str(p["_id"])
        return jsonify(p)
