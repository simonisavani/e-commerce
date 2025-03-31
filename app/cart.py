from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from bson.objectid import ObjectId
from app.config import db

cart_bp = Blueprint('cart', __name__)

@cart_bp.route('/cart', methods=['POST'])
@jwt_required()
def add_to_cart():
    user_id = str(get_jwt_identity())  # Get user ID from JWT
    data = request.get_json()

    # Validate required fields
    if not data or "product_id" not in data or "quantity" not in data:
        return jsonify({"error": "Missing product_id or quantity"}), 400

    try:
        product_id = ObjectId(data["product_id"])  # Convert product_id to ObjectId
    except:
        return jsonify({"error": "Invalid product_id"}), 400

    # Check if product exists
    product = db.products.find_one({"_id": product_id})
    if not product:
        return jsonify({"error": "Product not found"}), 404

    db.cart.insert_one({
        "user_id": user_id, 
        "product_id": str(product_id), 
        "quantity": data["quantity"]
    })

    return jsonify({"message": "Added to cart!"}), 201


@cart_bp.route('/cart', methods=['GET'])
@jwt_required()
def get_cart():
    user_id = str(get_jwt_identity())  
    cart_items = list(db.cart.find({"user_id": user_id}, {"_id": 1, "product_id": 1, "quantity": 1}))

    # Convert `_id` to string
    for item in cart_items:
        item["_id"] = str(item["_id"])

    return jsonify(cart_items)


@cart_bp.route('/cart/<cart_id>', methods=['DELETE'])
@jwt_required()
def remove_from_cart(cart_id):
    user_id = str(get_jwt_identity())  

    try:
        cart_object_id = ObjectId(cart_id)  # Convert cart_id to ObjectId
    except:
        return jsonify({"error": "Invalid cart_id"}), 400

    result = db.cart.delete_one({"_id": cart_object_id, "user_id": user_id})

    if result.deleted_count == 0:
        return jsonify({"error": "Item not found in cart"}), 404

    return jsonify({"message": "Item removed from cart"}), 200
