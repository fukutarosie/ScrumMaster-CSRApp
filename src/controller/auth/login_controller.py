from typing import Dict, Tuple, List
from src.entity import User, Role
from src.utils.validators import Validators
from src.utils.sanitizers import Sanitizers
from src.utils.helpers import TokenHelpers, RequestHelpers, ResponseHelpers


class LoginController:
    """
    Login Controller - Handles authentication logic
    Usage:
        controller = LoginController(request_data)
        response, status = controller.execute()
    """
    
    def __init__(self, request_data: Dict):
        """
        Initialize controller with request data
        
        Args:
            request_data: Login data from HTTP request
        """
        # Instance variables (object state - data in memory)
        self.request_data = request_data
        self.user = None  # Will hold User object
        self.errors: List[str] = []
        self.sanitized_data: Dict = {}
    
    # ============================================================================
    # VALIDATION METHODS (Instance methods)
    # ============================================================================
    
    def validate_request_data(self) -> bool:
        """
        Validate request data
        
        Returns:
            True if valid, False otherwise (errors stored in self.errors)
        """
        if not self.request_data:
            self.errors.append('Request body is required')
            return False
        
        # Validate required fields
        is_valid, error_msg, missing = RequestHelpers.validate_required_fields(
            self.request_data, ['username', 'password', 'role_name']
        )
        if not is_valid:
            self.errors.append(error_msg)
            return False
        
        # Sanitize input data
        self.sanitized_data = {
            'username': Sanitizers.sanitize_username(self.request_data.get('username', '')),
            'password': self.request_data.get('password', ''),  # Don't modify password
            'role_name': Sanitizers.sanitize_string(self.request_data.get('role_name', ''))
        }
        
        # Validate username format
        is_valid, error_msg = Validators.validate_username(self.sanitized_data['username'])
        if not is_valid:
            self.errors.append(error_msg)
            return False
        
        # Validate password format
        is_valid, error_msg = Validators.validate_password(self.sanitized_data['password'])
        if not is_valid:
            self.errors.append(error_msg)
            return False
        
        return True
    
    def authenticate_user(self) -> bool:
        """
        Authenticate user using User.authenticate factory method
        
        Returns:
            True if authenticated, False otherwise
        """
        self.user = User.authenticate(
            username=self.sanitized_data['username'],
            password=self.sanitized_data['password'],
            role_name=self.sanitized_data['role_name']
        )
        
        if not self.user:
            self.errors.append('Invalid credentials or user role mismatch')
            return False
        
        return True

    def execute(self) -> Tuple[Dict, int]:
        """
        Execute login process
        
        This is the main method that orchestrates the entire process:
        1. Validate request data
        2. Authenticate user (returns User object)
        3. Generate session token
        4. Return response with user data and token
        
        Returns:
            Tuple of (response_dict, status_code)
        """
        try:
            # Step 1: Validate request data
            if not self.validate_request_data():
                return ResponseHelpers.error_response(
                    message='; '.join(self.errors),
                    error_code='VALIDATION_ERROR',
                    status_code=400
                )
            
            # Step 2: Authenticate user (returns User object)
            if not self.authenticate_user():
                return ResponseHelpers.error_response(
                    message='; '.join(self.errors),
                    error_code='AUTH_FAILED',
                    status_code=401
                )
            
            # Step 3: Generate session token
            token = self.user.generate_session_token()
            
            # Prepare role information with consistent naming
            role_info = None
            if self.user.roles:
                role_data = self.user.roles
                role_info = {
                    'id': role_data.get('id', self.user.role_id),
                    'name': role_data.get('role_name'),
                    'role_name': role_data.get('role_name'),
                    'code': role_data.get('role_code'),
                    'role_code': role_data.get('role_code'),
                    'description': role_data.get('description'),
                    'dashboard_route': role_data.get('dashboard_route')
                }
            else:
                try:
                    role = Role.find(self.user.role_id)
                    if role:
                        role_info = {
                            'id': role.id,
                            'name': role.role_name,
                            'role_name': role.role_name,
                            'code': role.role_code,
                            'role_code': role.role_code,
                            'description': role.description,
                            'dashboard_route': role.dashboard_route
                        }
                except Exception:
                    role_info = None
            
            # Step 4: Return success response
            response_data = {
                'token': token,
                'user': {
                    'id': self.user.id,
                    'username': self.user.username,
                    'full_name': self.user.full_name,
                    'email': self.user.email,
                    'role_id': self.user.role_id,
                    'role': role_info
                }
            }
            
            return ResponseHelpers.success_response(
                data=response_data,
                message='Login successful',
                status_code=200
            )
            
        except Exception as e:
            import traceback
            print(f"[ERROR] Login error: {str(e)}")
            print(f"[ERROR] Traceback: {traceback.format_exc()}")
            return ResponseHelpers.error_response(
                message='An unexpected error occurred during login',
                error_code='SERVER_ERROR',
                status_code=500
            )
