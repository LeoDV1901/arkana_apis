from flask import request, jsonify
from bson import ObjectId
from Extensions import mongo
from Models.Carta_nfc import CartaNFC

class CartaNFCController:

    @staticmethod
    def crear():
        data = request.json

        # Validar campos obligatorios
        faltantes = [campo for campo in ["id_chip", "id_carta", "propietario_actual"]
                     if campo not in data or data[campo] in [None, ""]]

        if faltantes:
            return jsonify({"error": f"Faltan campos obligatorios: {', '.join(faltantes)}"}), 400

        # Crear objeto del modelo y convertir a dict para Mongo
        nfc = CartaNFC(data).to_dict()

        # Guardar en Mongo
        result = mongo.db.cartas_nfc.insert_one(nfc)

        return jsonify({
            "msg": "Carta NFC creada correctamente",
            "id": str(result.inserted_id)
        }), 201

    @staticmethod
    def obtener_todas():
        cards = list(mongo.db.cartas_nfc.find())

        # Convertir _id a string
        for c in cards:
            c["_id"] = str(c["_id"])

        return jsonify(cards)

    @staticmethod
    def obtener(id):
        try:
            c = mongo.db.cartas_nfc.find_one({"_id": ObjectId(id)})
        except:
            return jsonify({"error": "ID inválido"}), 400

        if not c:
            return jsonify({"error": "No encontrada"}), 404

        c["_id"] = str(c["_id"])
        return jsonify(c)

    @staticmethod
    def actualizar(id):
        data = request.json

        # No permitir modificar _id o fecha_creacion
        data.pop("_id", None)
        data.pop("fecha_creacion", None)

        mongo.db.cartas_nfc.update_one(
            {"_id": ObjectId(id)},
            {"$set": data}
        )

        return jsonify({"msg": "Actualizado correctamente"})

    @staticmethod
    def eliminar(id):
        mongo.db.cartas_nfc.delete_one({"_id": ObjectId(id)})
        return jsonify({"msg": "Eliminado"})
