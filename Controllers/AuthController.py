from flask import jsonify, request
from Extensions import mongo
from Models.Login import UsuarioLogin
from Models.User import Usuario  # si lo necesitas
from bson import ObjectId
from werkzeug.security import check_password_hash

class AuthController:

    @staticmethod
    def login():
        data = request.json

        # Validación de campos
        if not data.get("email") or not data.get("password"):
            return jsonify({"error": "Email y contraseña son requeridos"}), 400

        login_user = UsuarioLogin(data)

        # Buscar usuario por email
        usuario = mongo.db.usuarios.find_one({"email": login_user.email})
        if not usuario:
            return jsonify({"error": "Credenciales incorrectas"}), 401

        # Verificar contraseña
        if not login_user.validar_password(usuario["password"]):
            return jsonify({"error": "Credenciales incorrectas"}), 401

        usuario["_id"] = str(usuario["_id"])

        return jsonify({
            "msg": "Login exitoso",
            "usuario": {
                "id": usuario["_id"],
                "email": usuario["email"],
                "nombre": usuario.get("nombre")
            }
        }), 200
