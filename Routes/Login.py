from flask import Blueprint
from Controllers.AuthController import AuthController

auth_routes = Blueprint("auth_routes", __name__)

auth_routes.route("/login", methods=["POST"])(AuthController.login)
