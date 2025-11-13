"""Daily Reports Page Boundary - Handles HTTP interface for daily reports"""

from flask import Blueprint, request, jsonify
from datetime import datetime
from src.entity import Role
from src.controller.auth.auth_middleware import require_role
from src.controller.platform.get_daily_reports_controller import GetDailyReportsController

daily_reports_page = Blueprint('daily_reports', __name__, url_prefix='/api/platform/reports')


@daily_reports_page.route('/daily', methods=['GET'])
@require_role(Role.PLATFORM_MANAGEMENT)
def get_daily():
    """Get daily report for a specific date"""
    try:
        report_date = request.args.get('date', datetime.now().strftime('%Y-%m-%d'))
        controller = GetDailyReportsController(report_date)
        response, status = controller.execute()
        return jsonify(response), status
    except Exception as exc:
        return jsonify({
            "success": False,
            "message": str(exc)
        }), 500
