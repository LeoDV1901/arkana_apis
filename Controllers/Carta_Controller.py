from flask import request, jsonify
from bson import ObjectId
from datetime import datetime
from Models.Carta import Carta
from Extensions import mongo


class CartaController:

    @staticmethod
    def crear():
        data = request.json

        # Si el front manda fecha, eliminarla para no guardar strings
        if "fecha_creacion" in data:
            del data["fecha_creacion"]

        # Convertir datos en objeto Carta
        carta = Carta(data).__dict__

        # Guardar fecha CREACIÓN como datetime real
        carta["fecha_creacion"] = datetime.utcnow()

        mongo.db.cartas.insert_one(carta)
        return jsonify({"msg": "Carta creada"}), 200

    @staticmethod
    def obtener_todas():
        cartas = list(mongo.db.cartas.find())

        for c in cartas:
            c["_id"] = str(c["_id"])

            # Convertir datetime → ISO
            if isinstance(c.get("fecha_creacion"), datetime):
                c["fecha_creacion"] = c["fecha_creacion"].isoformat()

        return jsonify(cartas), 200

    @staticmethod
    def obtener(id):
        c = mongo.db.cartas.find_one({"_id": ObjectId(id)})
        if not c:
            return jsonify({"error": "Carta no encontrada"}), 404

        c["_id"] = str(c["_id"])

        if isinstance(c.get("fecha_creacion"), datetime):
            c["fecha_creacion"] = c["fecha_creacion"].isoformat()

        return jsonify(c), 200

    @staticmethod
    def actualizar(id):
        data = request.json

        # Evitar error si mandan _id
        data.pop("_id", None)

        # Evitar que manden fecha como string
        if "fecha_creacion" in data:
            del data["fecha_creacion"]

        mongo.db.cartas.update_one({"_id": ObjectId(id)}, {"$set": data})
        return jsonify({"msg": "Carta actualizada"}), 200

    @staticmethod
    def eliminar(id):
        mongo.db.cartas.delete_one({"_id": ObjectId(id)})
        return jsonify({"msg": "Carta eliminada"}), 200
