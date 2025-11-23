from flask import Blueprint
from Controllers.User_Controller import UsuarioController

usuario_bp = Blueprint("usuarios", __name__)

usuario_bp.post("")(UsuarioController.crear_usuario)
usuario_bp.get("/")(UsuarioController.obtener_usuarios)
usuario_bp.get("/<id>")(UsuarioController.obtener_usuario)
usuario_bp.put("/<id>")(UsuarioController.actualizar_usuario)
usuario_bp.delete("/<id>")(UsuarioController.eliminar_usuario)
