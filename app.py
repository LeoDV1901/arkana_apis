from flask import Flask
from Extensions import mongo
import certifi
from flask_cors import CORS
from flask import send_from_directory

# Se crea la instancia principal de la aplicación Flask
app = Flask(__name__)

# -------------------------------------------------------
# Configuración de conexión a MongoDB (MongoDB Atlas)
# -------------------------------------------------------
app.config["MONGO_URI"] = (
    "mongodb+srv://marcosj9807_db_user:GQ3MEg7vIKovKO0z@arkana."
    "ge1yf3l.mongodb.net/arkana?retryWrites=true&w=majority&appName=Spark"
)

# Se especifica el archivo de certificados de confianza
app.config["MONGO_TLSCAFILE"] = certifi.where()

# Inicializa la extensión PyMongo con la configuración previa
mongo.init_app(app)

# -------------------------------------------------------
# Configuración de CORS
# -------------------------------------------------------
# Se habilita CORS para permitir peticiones desde cualquier origen.
# Esto es útil para frontend separado (React, Angular, etc.) que consuma la API.
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

# -------------------------------------------------------
# Rutas base y archivos estáticos
# -------------------------------------------------------
@app.route('/favicon.ico')
def favicon():
    # Devuelve un icono desde la carpeta static para evitar errores 404 del navegador
    return send_from_directory('static', 'api.ico')

@app.route("/")
def home():
    # Ruta principal de prueba para verificar que el servidor funciona
    return "Hola mundo desde Python API"

# -------------------------------------------------------
# Importación de blueprints
# Cada módulo define un grupo de rutas relacionadas.
# -------------------------------------------------------
from Routes.User import usuario_bp
from Routes.Carta import carta_bp
from Routes.Carta_nfc_routes import carta_nfc_bp
from Routes.Inventario import inventario_bp
from Routes.Partida import partida_bp
from Routes.Sancion import sancion_bp
from Routes.Login import auth_routes
from Routes.SparkStarts import sparks_bp
from Routes.routes_estadisticas import estadisticas_bp
from Routes.Estadisticas_globales import estadisticasG_bp
from Routes.Regresiones import regresion_bp
from Routes.RegresionM import regresion_multiple_bp

# -------------------------------------------------------
# Registro de blueprints con prefijos
# -------------------------------------------------------
app.register_blueprint(usuario_bp, url_prefix="/usuarios")
app.register_blueprint(carta_bp, url_prefix="/cartas")
app.register_blueprint(carta_nfc_bp, url_prefix="/cartas_nfc")
app.register_blueprint(inventario_bp, url_prefix="/inventario")
app.register_blueprint(partida_bp, url_prefix="/partidas")
app.register_blueprint(sancion_bp, url_prefix="/sanciones")
app.register_blueprint(auth_routes, url_prefix="/login")
app.register_blueprint(estadisticas_bp, url_prefix="/estadisticas")
app.register_blueprint(sparks_bp, url_prefix="/arrancarSpark")
app.register_blueprint(estadisticasG_bp, url_prefix="/SparkResultados")
app.register_blueprint(regresion_bp, url_prefix="/regresion")
app.register_blueprint(regresion_multiple_bp, url_prefix="/regresionM")

# -------------------------------------------------------
# Ejecutar el servidor
# -------------------------------------------------------
if __name__ == "__main__":
    # debug=True habilita recarga automática y mensajes detallados
    # use_reloader=False evita lanzar dos instancias del servidor en Windows
    app.run(debug=True, use_reloader=False)
