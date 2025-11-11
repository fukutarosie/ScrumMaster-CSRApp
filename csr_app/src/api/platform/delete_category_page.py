"""Delete Category Page Boundary - Handles HTTP interface for category deletion"""

from flask import Blueprint, jsonify
from src.entity import Role
from src.controller.auth.auth_middleware import require_role
from src.controller.platform.delete_service_category_controller import DeleteServiceCategoryController

delete_category_page = Blueprint('delete_category', __name__, url_prefix='/api/platform/categories')


@delete_category_page.route('/<int:category_id>', methods=['DELETE'])
@require_role(Role.PLATFORM_MANAGEMENT)
def delete(category_id):
    """Delete a service category"""
    try:
        controller = DeleteServiceCategoryController(category_id)
        response, status = controller.execute()
        return jsonify(response), status
    except Exception as exc:
        return jsonify({
            "success": False,
            "message": str(exc)
        }), 500
