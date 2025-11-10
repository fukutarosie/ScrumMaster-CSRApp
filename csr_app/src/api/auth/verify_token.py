"""Verify Token Boundary - Handles HTTP interface for token verification"""

from flask import Blueprint, request, jsonify
from src.controller.auth.verify_token_controller import VerifyTokenController

verify_token_boundary = Blueprint('verify_token', __name__, url_prefix='/api/auth')

# Verify session token by METHOD: GET
@verify_token_boundary.route('/verify', methods=['GET'])
def verify():
    """Verify session token endpoint"""
    try:
        token = request.headers.get('Authorization', '').replace('Bearer ', '')
        # Create controller object, call instance method
        controller = VerifyTokenController(token)
        response, status = controller.execute()
        return jsonify(response), status
    except Exception as exc:
        return jsonify({
            "success": False,
            "message": str(exc)
        }), 500

