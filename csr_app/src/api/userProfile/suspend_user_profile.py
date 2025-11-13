"""Suspend/Activate User Profile Boundary - Handles HTTP interface for user profile suspension"""

from flask import Blueprint, jsonify
from src.entity import Role
from src.controller.auth.auth_middleware import require_role
from src.controller.userProfile.suspend_user_profile_controller import SuspendUserProfileController
from src.controller.userProfile.activate_user_profile_controller import ActivateUserProfileController

suspend_user_profile_boundary = Blueprint('suspend_user_profile', __name__, url_prefix='/api/userProfile')


@suspend_user_profile_boundary.route('/<int:user_id>/suspend', methods=['PUT'])
@require_role(Role.USER_ADMIN)
def suspend_user_profile(user_id):
    """Suspend (deactivate) a user profile"""
    try:
        controller = SuspendUserProfileController(user_id)
        response, status = controller.execute()
        return jsonify(response), status
    except Exception as exc:
        return jsonify({
            'success': False,
            'message': str(exc)
        }), 500


@suspend_user_profile_boundary.route('/<int:user_id>/activate', methods=['PUT'])
@require_role(Role.USER_ADMIN)
def activate_user_profile(user_id):
    """Activate (reactivate) a suspended user profile"""
    try:
        controller = ActivateUserProfileController(user_id)
        response, status = controller.execute()
        return jsonify(response), status
    except Exception as exc:
        return jsonify({
            'success': False,
            'message': str(exc)
        }), 500
