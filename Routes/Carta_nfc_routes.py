from flask import Blueprint
from Controllers.Carta_nfc_Controller import CartaNFCController

carta_nfc_bp = Blueprint("cartas_nfc", __name__)

carta_nfc_bp.post("")(CartaNFCController.crear)
carta_nfc_bp.get("/")(CartaNFCController.obtener_todas)
carta_nfc_bp.get("/<id>")(CartaNFCController.obtener)
carta_nfc_bp.put("/<id>")(CartaNFCController.actualizar)
carta_nfc_bp.delete("/<id>")(CartaNFCController.eliminar)
