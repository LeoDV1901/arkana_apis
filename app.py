from flask import Flask
from Extensions import mongo
import certifi
from flask_cors import CORS


app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb+srv://marcosj9807_db_user:GQ3MEg7vIKovKO0z@arkana.ge1yf3l.mongodb.net/arkana?retryWrites=true&w=majority&appName=Spark"

app.config["MONGO_TLSCAFILE"] = certifi.where()
mongo.init_app(app)

# Rutas
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

app.register_blueprint(usuario_bp, url_prefix="/usuarios")
app.register_blueprint(carta_bp, url_prefix="/cartas")
app.register_blueprint(carta_nfc_bp, url_prefix="/cartas_nfc")
app.register_blueprint(inventario_bp, url_prefix="/inventario")
app.register_blueprint(partida_bp, url_prefix="/partidas")
app.register_blueprint(sancion_bp, url_prefix="/sanciones")
app.register_blueprint(auth_routes,url_prefix="/login")
app.register_blueprint(estadisticas_bp, url_prefix="/estadisticas")
app.register_blueprint(sparks_bp, url_prefix="/arrancarSpark")
app.register_blueprint(estadisticasG_bp, url_prefix="/SparkResultados")
app.register_blueprint(regresion_bp, url_prefix="/regresion")
app.register_blueprint(regresion_multiple_bp, url_prefix="/regresionM")

CORS(app, supports_credentials=True)
CORS(app, resources={r"/*": {"origins": "*"}}, methods=["GET","POST","OPTIONS"])

if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)