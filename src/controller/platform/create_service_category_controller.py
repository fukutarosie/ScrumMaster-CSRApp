"""
Create Service Category Controller - TRUE OOP Implementation
Holds request data in memory and orchestrates category creation
"""

from typing import Tuple, Dict, List
from src.entity.service_category import ServiceCategory
from src.utils.helpers import RequestHelpers, ResponseHelpers


class CreateServiceCategoryController:
    """
    Create Service Category Controller - TRUE OOP
    
    This controller holds request data in memory and orchestrates category creation.
    It demonstrates proper OOP:
    - Has instance variables (data in memory)
    - Uses instance methods
    - Creates ServiceCategory objects and calls their instance methods
    
    Usage:
        controller = CreateServiceCategoryController(request_data)
        response, status = controller.execute()
    """
    
    def __init__(self, request_data: Dict):
        """
        Initialize controller with request data
        
        Args:
            request_data: Category data from HTTP request
        """
        self.request_data = request_data
        self.category = None
        self.errors: List[str] = []
        self.sanitized_data: Dict = {}
    
    def validate_request_data(self) -> bool:
        """
        Validate request data

        Returns:
            True if valid, False otherwise (errors stored in self.errors)
        """
        if not self.request_data:
            self.errors.append("Request body is required")
            return False

        required_fields = ['service_name']
        is_valid, error_msg, missing_fields = RequestHelpers.validate_required_fields(
            self.request_data, required_fields
        )
        if not is_valid:
            if missing_fields:
                self.errors.append(f"Missing required fields: {', '.join(missing_fields)}")
            else:
                self.errors.append(error_msg)
            return False

        service_name = self.request_data.get('service_name', '').strip()
        if not service_name or len(service_name) < 2:
            self.errors.append('Service name must be at least 2 characters')

        if len(service_name) > 100:
            self.errors.append('Service name must not exceed 100 characters')

        return len(self.errors) == 0

    def sanitize_data(self) -> None:
        """
        Sanitize input data and store in self.sanitized_data
        """
        self.sanitized_data = {
            'service_name': self.request_data.get('service_name', '').strip()
        }

    def create_category_object(self) -> None:
        """
        Create ServiceCategory object from sanitized data
        Stores ServiceCategory object in self.category (data in memory)
        """
        self.category = ServiceCategory()

        self.category.service_name = self.sanitized_data['service_name']
    
    def execute(self) -> Tuple[Dict, int]:
        """
        Execute category creation process
        
        This is the main method that orchestrates the entire process:
        1. Validate request data
        2. Sanitize data
        3. Create ServiceCategory object (holds data in memory)
        4. Save ServiceCategory object (ServiceCategory does the actual database work)
        5. Return response
        
        Returns:
            Tuple of (response_dict, status_code)
        """
        try:
            if not self.validate_request_data():
                return ResponseHelpers.error_response(
                    message='; '.join(self.errors),
                    error_code='VALIDATION_ERROR',
                    status_code=400
                )
            
            self.sanitize_data()
            
            self.create_category_object()
            
            try:
                self.category.save()
            except ValueError as e:
                error_msg = str(e)
                
                if 'already exists' in error_msg.lower():
                    return ResponseHelpers.error_response(
                        message=error_msg,
                        error_code='CATEGORY_EXISTS',
                        status_code=409,
                        details={'field': 'service_name'}
                    )
                else:
                    return ResponseHelpers.error_response(
                        message=error_msg,
                        error_code='VALIDATION_ERROR',
                        status_code=400
                    )
            
            return ResponseHelpers.success_response(
                data=self.category.to_dict(),
                message='Service category created successfully',
                status_code=201
            )
            
        except Exception as e:
            import traceback
            print(f"[ERROR] Create category error: {str(e)}")
            print(f"[ERROR] Traceback: {traceback.format_exc()}")
            return ResponseHelpers.error_response(
                message='An unexpected error occurred while creating service category. Please try again.',
                error_code='SERVER_ERROR',
                status_code=500
            )
