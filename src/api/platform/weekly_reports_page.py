"""Weekly Reports Page Boundary - Handles HTTP interface for weekly reports"""

from flask import Blueprint, request, jsonify
from datetime import datetime, timedelta
from src.entity import Role
from src.controller.auth.auth_middleware import require_role
from src.controller.platform.get_weekly_reports_controller import GetWeeklyReportsController

weekly_reports_page = Blueprint('weekly_reports', __name__, url_prefix='/api/platform/reports')


@weekly_reports_page.route('/weekly', methods=['GET'])
@require_role(Role.PLATFORM_MANAGEMENT)
def get_weekly():
    """Get weekly report for a specific week"""
    try:
        start_date = request.args.get('start_date')
        if not start_date:
            today = datetime.now()
            monday = today - timedelta(days=today.weekday())
            start_date = monday.strftime('%Y-%m-%d')
        
        controller = GetWeeklyReportsController(start_date)
        response, status = controller.execute()
        return jsonify(response), status
    except Exception as exc:
        return jsonify({
            "success": False,
            "message": str(exc)
        }), 500
