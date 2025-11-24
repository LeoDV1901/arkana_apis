from flask import jsonify, request
from Models.User import Usuario
from bson import ObjectId
from Extensions import mongo
from datetime import datetime

class UsuarioController:

    @staticmethod
    def crear_usuario():
        data = request.get_json(force=True)

        # Convertimos el request en objeto Usuario
        nuevo = Usuario(data).__dict__

        # 🔥 AGREGAR FECHAS AUTOMÁTICAS 🔥
        fecha_actual = datetime.utcnow().isoformat()
        nuevo["fecha_registro"] = fecha_actual
        nuevo["ultimo_login"] = fecha_actual

        # 🚫 Eliminar "id" si viene desde React
        nuevo.pop("id", None)

        mongo.db.usuarios.insert_one(nuevo)
        return jsonify({"msg": "Usuario creado"}), 200


    @staticmethod
    def obtener_usuarios():
        usuarios = list(mongo.db.usuarios.find())
        
        for u in usuarios:
            u["_id"] = str(u["_id"])

            # Convertir fechas a string si vienen como datetime
            if "fecha_registro" in u and isinstance(u["fecha_registro"], datetime):
                u["fecha_registro"] = u["fecha_registro"].isoformat()

            if "ultimo_login" in u and isinstance(u["ultimo_login"], datetime):
                u["ultimo_login"] = u["ultimo_login"].isoformat()

        return jsonify(usuarios), 200


    @staticmethod
    def obtener_usuario(id):
        usuario = mongo.db.usuarios.find_one({"_id": ObjectId(id)})
        if not usuario:
            return jsonify({"error": "No encontrado"}), 404
        
        usuario["_id"] = str(usuario["_id"])

        if "fecha_registro" in usuario and isinstance(usuario["fecha_registro"], datetime):
            usuario["fecha_registro"] = usuario["fecha_registro"].isoformat()

        if "ultimo_login" in usuario and isinstance(usuario["ultimo_login"], datetime):
            usuario["ultimo_login"] = usuario["ultimo_login"].isoformat()

        return jsonify(usuario), 200


    @staticmethod
    def actualizar_usuario(id):
        data = request.json.copy()

        # 🚫 Nunca permitir que React envíe id al update
        if "id" in data:
            del data["id"]

        # 🚫 Evitar que estas fechas se modifiquen por error
        data.pop("fecha_registro", None)
        data.pop("ultimo_login", None)

        resultado = mongo.db.usuarios.update_one(
            {"_id": ObjectId(id)}, 
            {"$set": data}
        )

        if resultado.matched_count == 0:
            return jsonify({"error": "No encontrado"}), 404
        
        return jsonify({"msg": "Actualizado"}), 200


    @staticmethod
    def eliminar_usuario(id):
        resultado = mongo.db.usuarios.delete_one({"_id": ObjectId(id)})

        if resultado.deleted_count == 0:
            return jsonify({"error": "No encontrado"}), 404

        return jsonify({"msg": "Eliminado"}), 200
