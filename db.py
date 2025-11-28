from flask_pymongo import PyMongo

# Inicializa la instancia de PyMongo sin configuración.
# La configuración (MONGO_URI, opciones de conexión, etc.)
# debe proporcionarse más adelante en la aplicación Flask
# mediante app.config, antes de llamar a mongo.init_app(app).
mongo = PyMongo()
