"""Create Category Page Boundary - Handles HTTP interface for category creation"""

from flask import Blueprint, request, jsonify
from src.entity import Role
from src.controller.auth.auth_middleware import require_role
from src.controller.platform.create_service_category_controller import CreateServiceCategoryController

create_category_page = Blueprint('create_category', __name__, url_prefix='/api/platform/categories')


@create_category_page.route('', methods=['POST'])
@require_role(Role.PLATFORM_MANAGEMENT)
def create():
    """Create a new service category"""
    try:
        payload = request.get_json()
        controller = CreateServiceCategoryController(payload)
        response, status = controller.execute()
        return jsonify(response), status
    except Exception as exc:
        return jsonify({
            "success": False,
            "message": str(exc)
        }), 500
