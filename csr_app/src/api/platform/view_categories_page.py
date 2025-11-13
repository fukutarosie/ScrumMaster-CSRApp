"""View Categories Page Boundary - Handles HTTP interface for listing categories"""

from flask import Blueprint, request, jsonify
from src.entity import Role
from src.controller.auth.auth_middleware import require_role
from src.controller.platform.list_service_categories_controller import ListServiceCategoriesController

# URL prefix pluralized to /api/platform/categories
view_categories_page = Blueprint('view_categories', __name__, url_prefix='/api/platform/categories')


@view_categories_page.route('', methods=['GET'])
@require_role(Role.PLATFORM_MANAGEMENT)
def list_categories():
    """Get all service categories"""
    try:
        filters = request.args.to_dict()
        controller = ListServiceCategoriesController(filters)
        response, status = controller.execute()
        return jsonify(response), status
    except Exception as exc:
        return jsonify({
            "success": False,
            "message": str(exc)
        }), 500
