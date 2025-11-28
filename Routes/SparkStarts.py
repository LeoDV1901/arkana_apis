from flask import Blueprint, jsonify
import subprocess

# Blueprint encargado de manejar las rutas relacionadas con la ejecución de Spark.
# En app.py será registrado con un prefijo, por ejemplo: /arrancarSpark
sparks_bp = Blueprint("spark", __name__)

@sparks_bp.route("", methods=["POST"])
def generar_estadisticas():
    """
    Inicia un proceso independiente que ejecuta el archivo spark_job.py.
    Esto permite que Spark se ejecute fuera del hilo principal de Flask,
    evitando que la API se quede bloqueada mientras Spark procesa información.
    """
    try:
        # Ejecuta spark_job.py como un proceso separado.
        # Popen no espera el resultado; simplemente dispara el proceso y continúa.
        subprocess.Popen(["python", "spark_job.py"])

        return jsonify({"mensaje": "Proceso Spark iniciado"}), 200

    except Exception as e:
        # En caso de error durante el arranque del proceso, se devuelve un JSON descriptivo.
        return jsonify({"error": str(e)}), 500
