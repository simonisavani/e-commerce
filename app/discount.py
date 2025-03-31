from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime
from bson.objectid import ObjectId
from app.config import db

discount_bp = Blueprint('discount', __name__)

@discount_bp.route('/coupon', methods=['POST'])
@jwt_required()
def apply_coupon():
    user_id = str(get_jwt_identity())  # Get logged-in user ID
    data = request.get_json()

    if "code" not in data:
        return jsonify({"error": "Coupon code is required"}), 400

    coupon = db.coupons.find_one({"code": data['code']})

    if not coupon:
        return jsonify({"error": "Invalid coupon"}), 400

    # Ensure expiry is stored as DateTime in MongoDB
    if isinstance(coupon["expiry"], str):
        expiry_date = datetime.strptime(coupon['expiry'], "%Y-%m-%d")  # Convert string to datetime
    else:
        expiry_date = coupon["expiry"]

    if expiry_date < datetime.utcnow():
        return jsonify({"error": "Coupon expired"}), 400

    # Check if coupon has usage restrictions
    coupon_id_str = str(coupon["_id"])  # Convert ObjectId to string
    if coupon.get("one_time_use", False):
        if db.used_coupons.find_one({"user_id": user_id, "coupon_id": coupon_id_str}):
            return jsonify({"error": "Coupon already used"}), 400

        # Mark coupon as used
        db.used_coupons.insert_one({"user_id": user_id, "coupon_id": coupon_id_str, "used_at": datetime.utcnow()})

    return jsonify({"discount": coupon['discount']}), 200
