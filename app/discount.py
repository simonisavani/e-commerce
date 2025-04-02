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

    if not data or "code" not in data:
        return jsonify({"error": "Coupon code is required"}), 400

    coupon = db.coupons.find_one({"code": data['code']})

    if not coupon:
        return jsonify({"error": "Invalid or non-existent coupon"}), 400

    # Ensure expiry date is a datetime object
    expiry_date = coupon.get("expiry")
    if isinstance(expiry_date, str):
        try:
            expiry_date = datetime.strptime(expiry_date, "%Y-%m-%d")  # Convert string to datetime
        except ValueError:
            return jsonify({"error": "Invalid expiry date format in database"}), 500  # Internal server error

    if expiry_date and expiry_date < datetime.utcnow():
        return jsonify({"error": "Coupon expired"}), 400

    coupon_id_str = str(coupon["_id"])  # Convert ObjectId to string

    # Check if the coupon has one-time use restriction
    if coupon.get("one_time_use", False):
        used_coupon = db.used_coupons.find_one({"user_id": user_id, "coupon_id": coupon_id_str})
        if used_coupon:
            return jsonify({"error": "Coupon already used"}), 400

        # Mark coupon as used
        db.used_coupons.insert_one({
            "user_id": user_id,
            "coupon_id": coupon_id_str,
            "used_at": datetime.utcnow()
        })

    return jsonify({"discount": coupon.get("discount", 0)}), 200
