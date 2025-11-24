from flask import Blueprint, jsonify
import subprocess

sparks_bp = Blueprint("spark", __name__)

@sparks_bp.route("", methods=["POST"])
def generar_estadisticas():
    try:
        subprocess.Popen(["python", "spark_job.py"])
        return jsonify({"mensaje": "Proceso Spark iniciado"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
