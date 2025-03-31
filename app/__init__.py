from flask import Flask
from flask_jwt_extended import JWTManager
from app.config import JWT_SECRET_KEY
from app.routes import register_routes

def create_app():
    app = Flask(__name__)
    app.config['JWT_SECRET_KEY'] = JWT_SECRET_KEY

    JWTManager(app)

    register_routes(app)

    return app
