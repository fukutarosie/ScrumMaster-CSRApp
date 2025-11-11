"""GetShortlist Boundary - HTTP layer for retrieving CSR shortlist"""

from flask import Blueprint, request, jsonify
from src.controller.shortlist.get_shortlist_controller import GetShortlistController
from src.controller.auth.auth_middleware import require_role

get_shortlist_boundary = Blueprint(
    'get_shortlist',
    __name__,
    url_prefix='/api/shortlist'
)

@get_shortlist_boundary.route('', methods=['GET'])
@require_role('CSR Rep')
def get_shortlist():
    """Get CSR's shortlist with optional filters"""
    auth_token = request.headers.get('Authorization', '').replace('Bearer ', '')
    status = request.args.get('status', '').strip() or None
    page = request.args.get('page', '1')
    limit = request.args.get('limit', '10')
    start_date = request.args.get('start_date', '').strip() or None
    end_date = request.args.get('end_date', '').strip() or None
    service_type = request.args.get('service_type', '').strip() or None
    
    # Controller currently exposes a static method interface
    response, status_code = GetShortlistController.get_shortlist(
        auth_token=auth_token,
        status_filter=status,
        page_str=page,
        limit_str=limit
    )
    return jsonify(response), status_code
