from flask import jsonify, request
from Models.User import Usuario
from bson import ObjectId
from Extensions import mongo
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

class UsuarioController:

    # ======================================================
    # 🔹 CREAR USUARIO
    # ======================================================
    @staticmethod
    def crear_usuario():
        data = request.get_json(force=True)

        # Validación mínima
        obligatorios = ["nickname", "correo", "contraseña"]
        faltantes = [c for c in obligatorios if not data.get(c)]

        if faltantes:
            return jsonify({"error": f"Faltan campos: {', '.join(faltantes)}"}), 400

        # Verificar duplicados
        if mongo.db.usuarios.find_one({"correo": data["correo"]}):
            return jsonify({"error": "El correo ya está registrado"}), 409

        if mongo.db.usuarios.find_one({"nickname": data["nickname"]}):
            return jsonify({"error": "El nickname ya está en uso"}), 409

        # Convertir objeto Usuario
        nuevo = Usuario(data).__dict__

        # 🔐 HASH PASSWORD
        nuevo["contraseña"] = generate_password_hash(data["contraseña"])

        # 🔥 FECHAS AUTOMÁTICAS
        fecha_actual = datetime.utcnow()
        nuevo["fecha_registro"] = fecha_actual
        nuevo["ultimo_login"] = fecha_actual

        # 🚫 Eliminar id si viene desde React
        nuevo.pop("id", None)

        mongo.db.usuarios.insert_one(nuevo)
        return jsonify({"msg": "Usuario creado"}), 201


    # ======================================================
    # 🔹 OBTENER TODOS
    # ======================================================
    @staticmethod
    def obtener_usuarios():
        usuarios = list(mongo.db.usuarios.find())

        for u in usuarios:
            u["_id"] = str(u["_id"])

            # Normalizar fechas
            for campo in ["fecha_registro", "ultimo_login"]:
                if campo in u and isinstance(u[campo], datetime):
                    u[campo] = u[campo].isoformat()

        return jsonify(usuarios), 200


    # ======================================================
    # 🔹 OBTENER POR ID
    # ======================================================
    @staticmethod
    def obtener_usuario(id):
        if not ObjectId.is_valid(id):
            return jsonify({"error": "ID inválido"}), 400

        usuario = mongo.db.usuarios.find_one({"_id": ObjectId(id)})

        if not usuario:
            return jsonify({"error": "No encontrado"}), 404

        usuario["_id"] = str(usuario["_id"])

        for campo in ["fecha_registro", "ultimo_login"]:
            if campo in usuario and isinstance(usuario[campo], datetime):
                usuario[campo] = usuario[campo].isoformat()

        return jsonify(usuario), 200


    # ======================================================
    # 🔹 ACTUALIZAR USUARIO
    # ======================================================
    @staticmethod
    def actualizar_usuario(id):
        if not ObjectId.is_valid(id):
            return jsonify({"error": "ID inválido"}), 400

        data = request.get_json(force=True)

        # 🚫 Nunca permitir que React envíe id
        data.pop("id", None)

        # 🚫 No permitir modificar fechas importantes
        data.pop("fecha_registro", None)
        data.pop("ultimo_login", None)

        # 🔐 Si modifica contraseña → hashear
        if "contraseña" in data and data["contraseña"]:
            data["contraseña"] = generate_password_hash(data["contraseña"])

        resultado = mongo.db.usuarios.update_one(
            {"_id": ObjectId(id)},
            {"$set": data}
        )

        if resultado.matched_count == 0:
            return jsonify({"error": "No encontrado"}), 404

        return jsonify({"msg": "Actualizado"}), 200


    # ======================================================
    # 🔹 ELIMINAR USUARIO
    # ======================================================
    @staticmethod
    def eliminar_usuario(id):
        if not ObjectId.is_valid(id):
            return jsonify({"error": "ID inválido"}), 400

        resultado = mongo.db.usuarios.delete_one({"_id": ObjectId(id)})

        if resultado.deleted_count == 0:
            return jsonify({"error": "No encontrado"}), 404

        return jsonify({"msg": "Eliminado"}), 200
