from flask import request, jsonify
from bson import ObjectId
from Extensions import mongo
from Models.Carta_nfc import CartaNFC


class CartaNFCController:

    @staticmethod
    def crear():
        data = request.json  # Datos enviados por el cliente en formato JSON

        # Lista de campos obligatorios que deben estar presentes
        faltantes = [
            campo for campo in ["id_chip", "id_carta", "propietario_actual"]
            if campo not in data or data[campo] in [None, ""]
        ]

        # Si falta alguno, retornamos error
        if faltantes:
            return jsonify({"error": f"Faltan campos obligatorios: {', '.join(faltantes)}"}), 400

        # Crear instancia del modelo y convertir a diccionario para guardar en MongoDB
        nfc = CartaNFC(data).to_dict()

        # Insertar el documento en la colección "cartas_nfc"
        result = mongo.db.cartas_nfc.insert_one(nfc)

        # Respuesta con el ID generado por Mongo
        return jsonify({
            "msg": "Carta NFC creada correctamente",
            "id": str(result.inserted_id)
        }), 201

    @staticmethod
    def obtener_todas():
        # Obtener todas las cartas NFC de la colección
        cards = list(mongo.db.cartas_nfc.find())

        # Convertir ObjectId a string para que sea serializable a JSON
        for c in cards:
            c["_id"] = str(c["_id"])

        return jsonify(cards)

    @staticmethod
    def obtener(id):
        try:
            # Buscar carta por ID
            c = mongo.db.cartas_nfc.find_one({"_id": ObjectId(id)})
        except:
            # Si el ID no es válido (ej. no tiene formato de ObjectId)
            return jsonify({"error": "ID inválido"}), 400

        # Si no existe la carta
        if not c:
            return jsonify({"error": "No encontrada"}), 404

        # Convertir ObjectId a string
        c["_id"] = str(c["_id"])

        return jsonify(c)

    @staticmethod
    def actualizar(id):
        data = request.json  # Datos a actualizar

        # Proteger campos que no deben ser modificados
        data.pop("_id", None)
        data.pop("fecha_creacion", None)

        # Actualizar documento en MongoDB
        mongo.db.cartas_nfc.update_one(
            {"_id": ObjectId(id)},   # Filtro por ID
            {"$set": data}           # Campos a modificar
        )

        return jsonify({"msg": "Actualizado correctamente"})

    @staticmethod
    def eliminar(id):
        # Eliminar documento por ID
        mongo.db.cartas_nfc.delete_one({"_id": ObjectId(id)})
        return jsonify({"msg": "Eliminado"})
