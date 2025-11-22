from flask import Blueprint
from Controllers.Sancion_Controller import SancionController

sancion_bp = Blueprint("sanciones", __name__)

sancion_bp.post("/")(SancionController.crear)
sancion_bp.get("/<id_usuario>")(SancionController.obtener_por_usuario)
sancion_bp.delete("/<id>")(SancionController.eliminar)
