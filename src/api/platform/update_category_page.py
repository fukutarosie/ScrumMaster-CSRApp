"""Update Category Page Boundary - Handles HTTP interface for category update"""

from flask import Blueprint, request, jsonify
from src.entity import Role
from src.controller.auth.auth_middleware import require_role
from src.controller.platform.update_service_category_controller import UpdateServiceCategoryController

update_category_page = Blueprint('update_category', __name__, url_prefix='/api/platform/categories')


@update_category_page.route('/<int:category_id>', methods=['PUT'])
@require_role(Role.PLATFORM_MANAGEMENT)
def update(category_id):
    """Update an existing service category"""
    try:
        payload = request.get_json()
        controller = UpdateServiceCategoryController(category_id, payload)
        response, status = controller.execute()
        return jsonify(response), status
    except Exception as exc:
        return jsonify({
            "success": False,
            "message": str(exc)
        }), 500
