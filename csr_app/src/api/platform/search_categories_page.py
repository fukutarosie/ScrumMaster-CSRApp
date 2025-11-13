"""Search Categories Page Boundary - Handles HTTP interface for searching categories"""

from flask import Blueprint, request, jsonify
from src.entity import Role
from src.controller.auth.auth_middleware import require_role
from src.controller.platform.search_service_categories_controller import SearchServiceCategoriesController

search_categories_page = Blueprint('search_categories', __name__, url_prefix='/api/platform/categories')


@search_categories_page.route('/search', methods=['GET'])
@require_role(Role.PLATFORM_MANAGEMENT)
def search():
    """Search service categories by keyword"""
    try:
        keyword = request.args.get('keyword', '')
        controller = SearchServiceCategoriesController(keyword)
        response, status = controller.execute()
        return jsonify(response), status
    except Exception as exc:
        return jsonify({
            "success": False,
            "message": str(exc)
        }), 500
