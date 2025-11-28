from flask import jsonify, request
from Extensions import mongo
from Models.Login import UsuarioLogin


class AuthController:

    @staticmethod
    def login():
        # Obtener datos enviados por el cliente (correo y contraseña)
        data = request.json

        # Validar que se reciban los campos obligatorios
        if not data.get("correo") or not data.get("contraseña"):
            return jsonify({"error": "Correo y contraseña son requeridos"}), 400

        # Crear un objeto del modelo UsuarioLogin
        login_user = UsuarioLogin(data)

        # Buscar un usuario en MongoDB usando el correo proporcionado
        usuario = mongo.db.usuarios.find_one({"correo": login_user.correo})

        # Si no existe, las credenciales están mal
        if not usuario:
            return jsonify({"error": "Credenciales incorrectas"}), 401

        # Validar la contraseña (comparación texto plano o método definido)
        if not login_user.validar_password(usuario["contraseña"]):
            return jsonify({"error": "Credenciales incorrectas"}), 401

        # Convertir ObjectId a string para que pueda enviarse en JSON
        usuario["_id"] = str(usuario["_id"])

        # Respuesta de login exitoso
        return jsonify({
            "msg": "Login exitoso",
            "usuario": {
                "id": usuario["_id"],
                "correo": usuario["correo"],
                "nickname": usuario.get("nickname")  # Puede no existir
            }
        }), 200
