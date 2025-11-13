"""Monthly Reports Page Boundary - Handles HTTP interface for monthly reports"""

from flask import Blueprint, request, jsonify
from datetime import datetime
from src.entity import Role
from src.controller.auth.auth_middleware import require_role
from src.controller.platform.get_monthly_reports_controller import GetMonthlyReportsController

monthly_reports_page = Blueprint('monthly_reports', __name__, url_prefix='/api/platform/reports')


@monthly_reports_page.route('/monthly', methods=['GET'])
@require_role(Role.PLATFORM_MANAGEMENT)
def get_monthly():
    """Get monthly report for a specific month"""
    try:
        month = request.args.get('month', datetime.now().strftime('%Y-%m'))
        controller = GetMonthlyReportsController(month)
        response, status = controller.execute()
        return jsonify(response), status
    except Exception as exc:
        return jsonify({
            "success": False,
            "message": str(exc)
        }), 500
