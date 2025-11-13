"""
Activate User Profile Controller - TRUE OOP Implementation
"""

from typing import Dict, Tuple, Optional
from src.entity import User


class ActivateUserProfileController:
    """
    Activate User Profile Controller - TRUE OOP
    Reactivates a suspended user account.
    
    Usage:
        controller = ActivateUserProfileController(user_id)
        response, status = controller.execute()
    """
    
    def __init__(self, user_id: int):
        """Initialize controller"""
        self.user_id = user_id
        self.user: Optional[User] = None
    
    def execute(self) -> Tuple[Dict, int]:
        """Execute user profile reactivation"""
        # Load user from database
        self.user = User.find(self.user_id)
        if not self.user:
            return {
                'success': False,
                'message': 'User profile not found'
            }, 404
        
        # Check if already active
        if self.user.is_active:
            return {
                'success': False,
                'message': 'User profile is already active'
            }, 400
        
        # Activate (instance method - sets is_active to True)
        if self.user.activate():
            return {
                'success': True,
                'message': f'User profile for {self.user.username} has been reactivated successfully'
            }, 200
        
        return {
            'success': False,
            'message': 'Failed to activate user profile'
        }, 400

