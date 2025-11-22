from flask import Blueprint
from Controllers.Carta_Controller import CartaController

carta_bp = Blueprint("cartas", __name__)

carta_bp.post("/")(CartaController.crear)
carta_bp.get("/")(CartaController.obtener_todas)
carta_bp.get("/<id>")(CartaController.obtener)
carta_bp.put("/<id>")(CartaController.actualizar)
carta_bp.delete("/<id>")(CartaController.eliminar)
