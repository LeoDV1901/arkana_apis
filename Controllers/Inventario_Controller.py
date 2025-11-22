from flask import request, jsonify
from bson import ObjectId
from db import mongo
from Models.Inventario import Inventario

class InventarioController:

    @staticmethod
    def agregar():
        data = request.json
        inv = Inventario(data).__dict__
        mongo.db.inventario.insert_one(inv)
        return jsonify({"msg": "Carta agregada al inventario"}), 201

    @staticmethod
    def obtener_por_usuario(id_usuario):
        items = list(mongo.db.inventario.find({"id_usuario": id_usuario}))
        for item in items:
            item["_id"] = str(item["_id"])
        return jsonify(items)

    @staticmethod
    def eliminar(id):
        mongo.db.inventario.delete_one({"_id": ObjectId(id)})
        return jsonify({"msg": "Eliminado del inventario"})
