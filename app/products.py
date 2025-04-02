from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt
from bson.objectid import ObjectId
from app.config import db, CACHE_CONFIG
from flask_caching import Cache
import json


product_bp = Blueprint('product', __name__)


cache = Cache()



@product_bp.before_app_request
def setup_cache():
    cache.init_app(current_app, config=CACHE_CONFIG)  # Initialize with Flask app

# -------------------------------
# 🔹 GET ALL PRODUCTS (CACHED)
# -------------------------------
@product_bp.route('/products', methods=['GET'])
def get_products():
    cached_data = cache.get("products")
    if cached_data:
        return jsonify(json.loads(cached_data.decode('utf-8')))

    products = list(db.products.find({}, {"_id": 1, "category": 1, "name": 1, "price": 1, "stock": 1, "image": 1}))
    
    for product in products:
        product["_id"] = str(product["_id"])

    cache.set("products", json.dumps(products), timeout=300)
    return jsonify(products)

# -------------------------------
# 🔹 GET SINGLE PRODUCT
# -------------------------------
@product_bp.route('/products/<string:product_id>', methods=['GET'])
def get_product(product_id):
    product = db.products.find_one({"_id": ObjectId(product_id)}, {"_id": 0})
    if not product:
        return jsonify({"error": "Product not found"}), 404
    return jsonify(product)

# -------------------------------
# 🔹 ADD PRODUCT (Admin Only)
# -------------------------------
@product_bp.route('/products', methods=['POST'])
@jwt_required()
def add_product():
    claims = get_jwt()
    if claims.get("role", "") not in ["admin"]:
        return jsonify({"error": "Unauthorized"}), 403

    data = request.get_json()
    required_fields = ["name", "category", "stock", "price", "image"]
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 400

    db.products.insert_one(data)
    cache.delete("products")
    return jsonify({"message": "Product added successfully!"}), 201

# -------------------------------
# 🔹 UPDATE PRODUCT (Admin Only)
# -------------------------------
@product_bp.route('/products/<string:product_id>', methods=['PUT'])
@jwt_required()
def update_product(product_id):
    claims = get_jwt()
    if claims.get("role", "") not in ["admin"]:
        return jsonify({"error": "Unauthorized"}), 403

    data = request.get_json()
    result = db.products.update_one({"_id": ObjectId(product_id)}, {"$set": data})
    
    if result.matched_count == 0:
        return jsonify({"error": "Product not found"}), 404

    cache.delete("products")
    return jsonify({"message": "Product updated successfully!"})

# -------------------------------
# 🔹 DELETE PRODUCT (Admin Only)
# -------------------------------
@product_bp.route('/products/<string:product_id>', methods=['DELETE'])
@jwt_required()
def delete_product(product_id):
    claims = get_jwt()
    if claims.get("role", "") not in ["admin"]:
        return jsonify({"error": "Unauthorized"}), 403

    result = db.products.delete_one({"_id": ObjectId(product_id)})
    if result.deleted_count == 0:
        return jsonify({"error": "Product not found"}), 404

    cache.delete("products")
    return jsonify({"message": "Product deleted successfully!"})
