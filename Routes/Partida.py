from flask import Blueprint
from Controllers.Partida_Controller import PartidaController

partida_bp = Blueprint("partidas", __name__)

partida_bp.post("")(PartidaController.crear)
partida_bp.get("/")(PartidaController.obtener_todas)
partida_bp.get("/<id>")(PartidaController.obtener)
