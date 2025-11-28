from flask import Blueprint
from Controllers.Sancion_Controller import SancionController

# Blueprint para agrupar todas las rutas relacionadas con sanciones.
# Se registrará en app.py con el prefijo /sanciones
sancion_bp = Blueprint("sanciones", __name__)

# -------------------------------------------------------
# Rutas del módulo de sanciones
# -------------------------------------------------------

# Crear una nueva sanción
sancion_bp.post("/")(SancionController.crear)

# Obtener todas las sanciones asociadas a un usuario específico
sancion_bp.get("/<id_usuario>")(SancionController.obtener_por_usuario)

# Eliminar una sanción por su ID
sancion_bp.delete("/<id>")(SancionController.eliminar)
