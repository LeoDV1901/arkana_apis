from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from flask_migrate import Migrate
import os
from dotenv import load_dotenv

# Carga las variables definidas en el archivo .env
# Esto permite acceder a DATABASE_URL u otras claves de configuración
load_dotenv()

# Instancias globales de SQLAlchemy y Migrate.
# Aún no están vinculadas a la aplicación Flask hasta init_app().
db = SQLAlchemy()
migrate = Migrate()

def init_app(app):
    """
    Inicializa la configuración de la base de datos y
    enlaza SQLAlchemy y Flask-Migrate con la aplicación Flask.
    """

    # Obtiene la URL de la base de datos desde las variables de entorno.
    # Ejemplo en .env:
    # DATABASE_URL=postgresql://usuario:password@localhost:5432/mi_bd
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')

    # Desactiva el seguimiento de modificaciones para evitar
    # sobrecarga de memoria y advertencias innecesarias.
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Inicializa la instancia de SQLAlchemy con la app Flask ya configurada.
    db.init_app(app)

    # Inicializa flask-migrate, que permite manejar migraciones con Alembic.
    migrate.init_app(app, db)
