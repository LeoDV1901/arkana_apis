from flask import Blueprint
from Controllers.Estadistica_Controller import EstadisticaController

estadistica_bp = Blueprint("estadisticas", __name__)

estadistica_bp.post("/")(EstadisticaController.crear)
estadistica_bp.get("/<id_usuario>")(EstadisticaController.obtener_por_usuario)
estadistica_bp.put("/<id_usuario>")(EstadisticaController.actualizar)
