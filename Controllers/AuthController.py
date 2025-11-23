from flask import jsonify, request
from Extensions import mongo
from Models.Login import UsuarioLogin

class AuthController:

    @staticmethod
    def login():
        data = request.json

        # Validación de campos
        if not data.get("correo") or not data.get("contraseña"):
            return jsonify({"error": "Correo y contraseña son requeridos"}), 400

        login_user = UsuarioLogin(data)

        # Buscar usuario por correo
        usuario = mongo.db.usuarios.find_one({"correo": login_user.correo})
        if not usuario:
            return jsonify({"error": "Credenciales incorrectas"}), 401

        # Verificar contraseña (texto plano)
        if not login_user.validar_password(usuario["contraseña"]):
            return jsonify({"error": "Credenciales incorrectas"}), 401

        usuario["_id"] = str(usuario["_id"])

        return jsonify({
            "msg": "Login exitoso",
            "usuario": {
                "id": usuario["_id"],
                "correo": usuario["correo"],
                "nickname": usuario.get("nickname")
            }
        }), 200
