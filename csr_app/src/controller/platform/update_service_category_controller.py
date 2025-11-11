"""
Update Service Category Controller - TRUE OOP Implementation
Holds request data in memory and orchestrates category update
"""

from typing import Tuple, Dict, List
from src.entity.service_category import ServiceCategory
from src.utils.helpers import RequestHelpers, ResponseHelpers


class UpdateServiceCategoryController:
    """
    Update Service Category Controller - TRUE OOP
    
    Usage:
        controller = UpdateServiceCategoryController(category_id, request_data)
        response, status = controller.execute()
    """
    
    def __init__(self, category_id: int, request_data: Dict):
        """
        Initialize controller with category ID and request data
        
        Args:
            category_id: ID of category to update
            request_data: Updated category data from HTTP request
        """
        self.category_id = category_id
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
        
        name = self.request_data.get('name', '').strip()
        if name:
            if len(name) < 2:
                self.errors.append('Category name must be at least 2 characters')
            if len(name) > 100:
                self.errors.append('Category name must not exceed 100 characters')
        
        description = self.request_data.get('description', '')
        if description and len(description) > 500:
            self.errors.append('Category description must not exceed 500 characters')
        
        return len(self.errors) == 0
    
    def sanitize_data(self) -> None:
        """
        Sanitize input data and store in self.sanitized_data
        """
        self.sanitized_data = {}
        if 'name' in self.request_data:
            self.sanitized_data['name'] = self.request_data.get('name', '').strip()
        if 'description' in self.request_data:
            self.sanitized_data['description'] = self.request_data.get('description', '').strip() if self.request_data.get('description') else None
    
    def load_category(self) -> bool:
        """
        Load existing category from database
        
        Returns:
            True if found, False otherwise
        """
        self.category = ServiceCategory.find_by_id(self.category_id)
        if not self.category:
            self.errors.append(f"Category with ID {self.category_id} not found")
            return False
        return True
    
    def update_category_object(self) -> None:
        """
        Update ServiceCategory object with sanitized data
        """
        if 'name' in self.sanitized_data:
            self.category.name = self.sanitized_data['name']
        if 'description' in self.sanitized_data:
            self.category.description = self.sanitized_data['description']
    
    def execute(self) -> Tuple[Dict, int]:
        """
        Execute category update process
        
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
            
            if not self.load_category():
                return ResponseHelpers.error_response(
                    message='; '.join(self.errors),
                    error_code='NOT_FOUND',
                    status_code=404
                )
            
            self.sanitize_data()
            self.update_category_object()
            
            try:
                self.category.save()
            except ValueError as e:
                error_msg = str(e)
                
                if 'already exists' in error_msg.lower():
                    return ResponseHelpers.error_response(
                        message=error_msg,
                        error_code='CATEGORY_EXISTS',
                        status_code=409,
                        details={'field': 'name'}
                    )
                else:
                    return ResponseHelpers.error_response(
                        message=error_msg,
                        error_code='VALIDATION_ERROR',
                        status_code=400
                    )
            
            return ResponseHelpers.success_response(
                data=self.category.to_dict(),
                message='Service category updated successfully',
                status_code=200
            )
            
        except Exception as e:
            import traceback
            print(f"[ERROR] Update category error: {str(e)}")
            print(f"[ERROR] Traceback: {traceback.format_exc()}")
            return ResponseHelpers.error_response(
                message='An unexpected error occurred while updating service category. Please try again.',
                error_code='SERVER_ERROR',
                status_code=500
            )
