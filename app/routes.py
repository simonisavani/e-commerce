from flask import Blueprint

from app.auth import auth_bp
from app.products import product_bp
from app.cart import cart_bp
from app.orders import order_bp
from app.discount import discount_bp

main_bp = Blueprint('main', __name__)

def register_routes(app):
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(product_bp, url_prefix="/api")
    app.register_blueprint(cart_bp, url_prefix="/api")
    app.register_blueprint(order_bp, url_prefix="/api")
    app.register_blueprint(discount_bp, url_prefix="/api")
