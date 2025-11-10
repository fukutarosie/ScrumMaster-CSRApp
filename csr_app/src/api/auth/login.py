"""Login Boundary - Handles HTTP interface for user login"""

from flask import Blueprint, request, jsonify
from src.controller.auth.login_controller import LoginController

login_boundary = Blueprint('login', __name__, url_prefix='/api/auth')

# User login by METHOD: POST
@login_boundary.route('/login', methods=['POST'])
def login():
    """User login endpoint"""
    try:
        payload = request.get_json()
        # TRUE OOP: Create controller object, call instance method
        controller = LoginController(payload)
        response, status = controller.execute()
        return jsonify(response), status
    except Exception as exc:
        return jsonify({
            "success": False,
            "message": str(exc)
        }), 500
