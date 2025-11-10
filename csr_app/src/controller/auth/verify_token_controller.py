"""
Verify Token Controller - TRUE OOP Implementation
Handles token verification process
"""

from typing import Dict, Tuple, List
from src.entity import User
from src.utils.helpers import ResponseHelpers


class VerifyTokenController:
    """
    Verify Token Controller - TRUE OOP
    
    This controller verifies JWT tokens and returns user information.
    
    Usage:
        controller = VerifyTokenController(auth_token)
        response, status = controller.execute()
    """
    
    def __init__(self, auth_token: str):
        """
        Initialize controller with auth token
        
        Args:
            auth_token: JWT authentication token
        """
        self.auth_token = auth_token
        self.user = None
        self.errors: List[str] = []
    
    def execute(self) -> Tuple[Dict, int]:
        """
        Execute token verification process
        
        Returns:
            Tuple of (response_dict, status_code)
        """
        try:
            # Verify token and get user
            self.user = User.verify_token(self.auth_token)
            if not self.user:
                return ResponseHelpers.error_response(
                    message='Invalid or expired token',
                    error_code='INVALID_TOKEN',
                    status_code=401
                )
            
            # Return success response with user data
            response_data = {
                'user': {
                    'id': self.user.id,
                    'username': self.user.username,
                    'full_name': self.user.full_name,
                    'email': self.user.email,
                    'role_id': self.user.role_id,
                    'role': self.user.roles if self.user.roles else None
                }
            }
            
            return ResponseHelpers.success_response(
                data=response_data,
                message='Token is valid',
                status_code=200
            )
            
        except Exception as e:
            print(f"[ERROR] Verify token error: {str(e)}")
            return ResponseHelpers.error_response(
                message='An unexpected error occurred during token verification',
                error_code='SERVER_ERROR',
                status_code=500
            )

