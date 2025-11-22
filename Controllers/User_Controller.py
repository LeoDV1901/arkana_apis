from flask import jsonify, request
from Models.User import Usuario
from bson import ObjectId
from Extensions import mongo

class UsuarioController:

    @staticmethod
    def crear_usuario():
        data = request.json
        nuevo = Usuario(data).__dict__
        mongo.db.usuarios.insert_one(nuevo)
        return jsonify({"msg": "Usuario creado"}), 201

    @staticmethod
    def obtener_usuarios():
        usuarios = list(mongo.db.usuarios.find())
        for u in usuarios:
            u["_id"] = str(u["_id"])
        return jsonify(usuarios), 200

    @staticmethod
    def obtener_usuario(id):
        usuario = mongo.db.usuarios.find_one({"_id": ObjectId(id)})
        if not usuario:
            return jsonify({"error": "No encontrado"}), 404
        
        usuario["_id"] = str(usuario["_id"])
        return jsonify(usuario), 200

    @staticmethod
    def actualizar_usuario(id):
        data = request.json
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
