# from flask import Blueprint, request, jsonify
# from flask_jwt_extended import jwt_required, get_jwt_identity
# from bson.objectid import ObjectId
# from datetime import datetime
# from app.config import db
# from app.tasks import send_order_notification

# order_bp = Blueprint('order', __name__)

# # -------------------------------
# # 🔹 PLACE ORDER
# # -------------------------------
# @order_bp.route('/order', methods=['POST'])
# # @jwt_required()
# # @app.route("/api/order", methods=["POST"])
# @jwt_required()
# def place_order():
#     user_id = get_jwt_identity()

#     # Fetch user's cart
#     cart_items = list(db.cart.find({"user_id": user_id}))
#     if not cart_items:
#         return jsonify({"error": "Your cart is empty"}), 400

#     unavailable_products = []
#     order_items = []

#     for item in cart_items:
#         product_id = str(item["product_id"])
#         product = db.products.find_one({"_id": ObjectId(product_id)})

#         if not product:
#             unavailable_products.append(product_id)
#             continue

#         order_items.append({
#             "product_id": product_id,
#             "quantity": item["quantity"],
#             "price": product["price"]
#         })

#     if unavailable_products:
#         return jsonify({
#             "error": "Some products in the cart are no longer available",
#             "missing_products": unavailable_products
#         }), 400

#     # If all items are valid, proceed with order creation
#     order_data = {
#         "user_id": user_id,
#         "items": order_items,
#         "status": "Pending",
#         "created_at": datetime.utcnow()
#     }
#     db.orders.insert_one(order_data)

#     # Clear the user's cart after order is placed
#     db.cart.delete_many({"user_id": user_id})

#     return jsonify({"message": "Order placed successfully"}), 201

# # def place_order():
# #     user_id = str(get_jwt_identity())  # Get user ID as a string
# #     cart_items = list(db.cart.find({"user_id": user_id}))

# #     if not cart_items:
# #         return jsonify({"error": "Cart is empty"}), 400

# #     # Ensure products exist in DB
# #     product_ids = [ObjectId(item["product_id"]) for item in cart_items if "product_id" in item]
# #     existing_products = list(db.products.find({"_id": {"$in": product_ids}}, {"_id": 1}))

# #     if len(existing_products) != len(product_ids):
# #         return jsonify({"error": "Some products in the cart are no longer available"}), 400

# #     # Remove `_id` field from cart items
# #     for item in cart_items:
# #         item.pop("_id", None)

# #     order = {
# #         "user_id": user_id,
# #         "items": cart_items,
# #         "status": "Pending",
# #         "created_at": datetime.utcnow()
# #     }

# #     order_id = db.orders.insert_one(order).inserted_id  # Insert order and get its ID

# #     # Clear the user's cart
# #     db.cart.delete_many({"user_id": user_id})

# #     # Trigger Celery task (passing order details)
# #     send_order_notification.delay(user_id, str(order_id), cart_items)

# #     return jsonify({"message": "Order placed!", "order_id": str(order_id)}), 201

# # -------------------------------
# # 🔹 TRACK ORDER
# # -------------------------------
# @order_bp.route('/order/<string:order_id>', methods=['GET'])
# @jwt_required()
# def track_order(order_id):
#     try:
#         order_object_id = ObjectId(order_id)  # Convert to ObjectId
#     except:
#         return jsonify({"error": "Invalid order ID"}), 400

#     order = db.orders.find_one({"_id": order_object_id})

#     if not order:
#         return jsonify({"error": "Order not found"}), 404

#     # Convert `_id` to string for JSON response
#     order["order_id"] = str(order.pop("_id"))
    
#     return jsonify(order)
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from bson.objectid import ObjectId
from datetime import datetime
from app.config import db  # Ensure you have a config.py where MongoDB is initialized

order_bp = Blueprint('order', __name__)

# ---------------------------------
# 🛒 PLACE AN ORDER
# ---------------------------------
@order_bp.route('/order', methods=['POST'])
@jwt_required()
def place_order():
    user_id = get_jwt_identity()

    # Fetch user's cart
    cart_items = list(db.cart.find({"user_id": user_id}))
    if not cart_items:
        return jsonify({"error": "Your cart is empty"}), 400

    unavailable_products = []
    order_items = []

    for item in cart_items:
        product_id = str(item["product_id"])
        product = db.products.find_one({"_id": ObjectId(product_id)})

        if not product:
            unavailable_products.append(product_id)
            continue

        order_items.append({
            "product_id": product_id,
            "quantity": item["quantity"],
            "price": product["price"]
        })

    if unavailable_products:
        return jsonify({
            "error": "Some products in the cart are no longer available",
            "missing_products": unavailable_products
        }), 400

    # Create order in database
    order_data = {
        "user_id": user_id,
        "items": order_items,
        "status": "Pending",  # Status: Pending, Shipped, Delivered, Cancelled
        "created_at": datetime.utcnow()
    }
    
    result = db.orders.insert_one(order_data)
    order_id = str(result.inserted_id)

    # Clear user's cart after placing an order
    db.cart.delete_many({"user_id": user_id})

    return jsonify({"message": "Order placed successfully", "order_id": order_id}), 201

# ---------------------------------
# 🔎 TRACK ORDER BY ID
# ---------------------------------
@order_bp.route('/order/<string:order_id>', methods=['GET'])
@jwt_required()
def track_order(order_id):
    try:
        order_object_id = ObjectId(order_id)
    except:
        return jsonify({"error": "Invalid order ID"}), 400

    order = db.orders.find_one({"_id": order_object_id})

    if not order:
        return jsonify({"error": "Order not found"}), 404

    order["order_id"] = str(order.pop("_id"))  # Convert `_id` to string
    return jsonify(order), 200

# ---------------------------------
# ❌ CANCEL ORDER
# ---------------------------------
@order_bp.route('/order/<string:order_id>/cancel', methods=['POST'])
@jwt_required()
def cancel_order(order_id):
    user_id = get_jwt_identity()

    try:
        order_object_id = ObjectId(order_id)
    except:
        return jsonify({"error": "Invalid order ID"}), 400

    order = db.orders.find_one({"_id": order_object_id, "user_id": user_id})

    if not order:
        return jsonify({"error": "Order not found"}), 404

    if order["status"] in ["Shipped", "Delivered"]:
        return jsonify({"error": "Cannot cancel an order that is already shipped or delivered"}), 400

    db.orders.update_one({"_id": order_object_id}, {"$set": {"status": "Cancelled"}})
    return jsonify({"message": "Order cancelled successfully"}), 200

# ---------------------------------
# 📋 LIST ALL ORDERS FOR USER
# ---------------------------------
@order_bp.route('/orders', methods=['GET'])
@jwt_required()
def list_orders():
    user_id = get_jwt_identity()
    orders = list(db.orders.find({"user_id": user_id}))

    for order in orders:
        order["order_id"] = str(order.pop("_id"))  # Convert `_id` to string

    return jsonify(orders), 200

