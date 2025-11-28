from flask import Blueprint
from Controllers.AuthController import AuthController

# Blueprint para agrupar las rutas de autenticación.
# Se registra en app.py con el prefijo /login
auth_routes = Blueprint("auth_routes", __name__)

# ============================================================
#   POST /login
#   Endpoint encargado de validar credenciales y generar token
# ============================================================
auth_routes.route("/login", methods=["POST"])(AuthController.login)
