from flask import Flask
from Extensions import mongo
import certifi

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
from Routes.Estadisticas import estadistica_bp
from Routes.Login import auth_routes
from Routes.SparkStats import spark_bp 

app.register_blueprint(usuario_bp, url_prefix="/usuarios")
app.register_blueprint(carta_bp, url_prefix="/cartas")
app.register_blueprint(carta_nfc_bp, url_prefix="/cartas_nfc")
app.register_blueprint(inventario_bp, url_prefix="/inventario")
app.register_blueprint(partida_bp, url_prefix="/partidas")
app.register_blueprint(sancion_bp, url_prefix="/sanciones")
app.register_blueprint(estadistica_bp, url_prefix="/estadisticas")
app.register_blueprint(auth_routes,url_prefix="/Login")
app.register_blueprint(spark_bp, url_prefix="/spark")

if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)

