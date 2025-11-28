from flask import Blueprint
from Controllers.User_Controller import UsuarioController

# Se crea el Blueprint para agrupar todas las rutas relacionadas con usuarios.
# Este blueprint será registrado en app.py con el prefijo /usuarios
usuario_bp = Blueprint("usuarios", __name__)

# -------------------------------------------------------
# Rutas para el manejo de usuarios
# -------------------------------------------------------

# Crea un nuevo usuario
usuario_bp.post("")(UsuarioController.crear_usuario)

# Obtiene la lista completa de usuarios
usuario_bp.get("/")(UsuarioController.obtener_usuarios)

# Obtiene los datos de un usuario específico por su ID
usuario_bp.get("/<id>")(UsuarioController.obtener_usuario)

# Actualiza la información de un usuario mediante su ID
usuario_bp.put("/<id>")(UsuarioController.actualizar_usuario)

# Elimina un usuario según su ID
usuario_bp.delete("/<id>")(UsuarioController.eliminar_usuario)
