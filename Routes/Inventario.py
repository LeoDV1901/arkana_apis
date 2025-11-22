from flask import Blueprint
from Controllers.Inventario_Controller import InventarioController

inventario_bp = Blueprint("inventario", __name__)

inventario_bp.post("/")(InventarioController.agregar)
inventario_bp.get("/<id_usuario>")(InventarioController.obtener_por_usuario)
inventario_bp.delete("/item/<id>")(InventarioController.eliminar)
