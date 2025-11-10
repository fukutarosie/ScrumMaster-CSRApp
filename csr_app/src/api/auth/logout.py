"""Logout Boundary - Handles HTTP interface for logout"""

from flask import Blueprint, request, jsonify
from src.entity import User

logout_boundary = Blueprint('logout', __name__, url_prefix='/api/auth')

# User logout by METHOD: POST
@logout_boundary.route('/logout', methods=['POST'])
def logout():
    """
    User logout endpoint
    
    Logout is primarily client-side (removing token from localStorage).
    This endpoint validates the token and returns success.
    """
    try:
        token = request.headers.get('Authorization', '').replace('Bearer ', '')
        
        # Verify token is valid
        user = User.verify_token(token)
        if not user:
            return jsonify({
                "success": False,
                "message": "Invalid or expired token"
            }), 401
        
        # Client-side will remove the token from localStorage
        return jsonify({
            "success": True,
            "message": "Logout successful"
        }), 200
        
    except Exception as exc:
        return jsonify({
            "success": False,
            "message": str(exc)
        }), 500

