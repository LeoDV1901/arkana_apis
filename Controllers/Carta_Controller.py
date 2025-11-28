from flask import request, jsonify
from bson import ObjectId
from datetime import datetime
from Models.Carta import Carta
from Extensions import mongo


class CartaController:

    @staticmethod
    def crear():
        data = request.json  # Datos enviados por el cliente

        # Si el cliente envía fecha_creacion, la eliminamos para evitar guardar un string
        if "fecha_creacion" in data:
            del data["fecha_creacion"]

        # Crear objeto Carta basado en el modelo y convertirlo a diccionario
        carta = Carta(data).__dict__

        # Establecer fecha de creación real usando datetime UTC
        carta["fecha_creacion"] = datetime.utcnow()

        # Insertar en la colección "cartas"
        mongo.db.cartas.insert_one(carta)

        return jsonify({"msg": "Carta creada"}), 200

    @staticmethod
    def obtener_todas():
        # Obtener todas las cartas desde MongoDB
        cartas = list(mongo.db.cartas.find())

        for c in cartas:
            # Convertir ObjectId a string para que sea serializable a JSON
            c["_id"] = str(c["_id"])

            # Si fecha_creacion es un datetime, convertirlo a ISO8601
            if isinstance(c.get("fecha_creacion"), datetime):
                c["fecha_creacion"] = c["fecha_creacion"].isoformat()

        return jsonify(cartas), 200

    @staticmethod
    def obtener(id):
        # Buscar una carta por su ID
        c = mongo.db.cartas.find_one({"_id": ObjectId(id)})

        # Si no existe, retornamos error
        if not c:
            return jsonify({"error": "Carta no encontrada"}), 404

        # Convertir ObjectId a string
        c["_id"] = str(c["_id"])

        # Convertir fecha a ISO si es necesario
        if isinstance(c.get("fecha_creacion"), datetime):
            c["fecha_creacion"] = c["fecha_creacion"].isoformat()

        return jsonify(c), 200

    @staticmethod
    def actualizar(id):
        data = request.json  # Datos enviados por el cliente

        # Eliminar _id para evitar conflicto, ya que no puede actualizarse
        data.pop("_id", None)

        # Eliminar fecha si el frontend la envía como string
        if "fecha_creacion" in data:
            del data["fecha_creacion"]

        # Actualizar los campos enviados
        mongo.db.cartas.update_one(
            {"_id": ObjectId(id)},
            {"$set": data}
        )

        return jsonify({"msg": "Carta actualizada"}), 200

    @staticmethod
    def eliminar(id):
        # Eliminar documento por su ID
        mongo.db.cartas.delete_one({"_id": ObjectId(id)})
        return jsonify({"msg": "Carta eliminada"}), 200
