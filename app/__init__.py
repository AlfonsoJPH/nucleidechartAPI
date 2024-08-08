from flask import Flask
from app.routes import api

def create_app():
    app = Flask(__name__)

    # Configuración de la aplicación
    app.config.from_object('app.config.Config')

    # Registro de blueprints
    app.register_blueprint(api)

    return app
