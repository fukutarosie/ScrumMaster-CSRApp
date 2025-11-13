"""
Delete Service Category Controller - TRUE OOP Implementation
Orchestrates category deletion
"""

from typing import Tuple, Dict, List
from src.entity.service_category import ServiceCategory
from src.utils.helpers import ResponseHelpers


class DeleteServiceCategoryController:
    """
    Delete Service Category Controller - TRUE OOP
    
    Usage:
        controller = DeleteServiceCategoryController(category_id)
        response, status = controller.execute()
    """
    
    def __init__(self, category_id: int):
        """
        Initialize controller with category ID
        
        Args:
            category_id: ID of category to delete
        """
        self.category_id = category_id
        self.category = None
        self.errors: List[str] = []
    
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
    
    def execute(self) -> Tuple[Dict, int]:
        """
        Execute category deletion process
        
        Returns:
            Tuple of (response_dict, status_code)
        """
        try:
            if not self.load_category():
                return ResponseHelpers.error_response(
                    message='; '.join(self.errors),
                    error_code='NOT_FOUND',
                    status_code=404
                )
            
            try:
                self.category.delete()
            except ValueError as e:
                return ResponseHelpers.error_response(
                    message=str(e),
                    error_code='DELETE_ERROR',
                    status_code=400
                )
            
            return ResponseHelpers.success_response(
                data={'id': self.category_id},
                message='Service category deleted successfully',
                status_code=200
            )
            
        except Exception as e:
            import traceback
            print(f"[ERROR] Delete category error: {str(e)}")
            print(f"[ERROR] Traceback: {traceback.format_exc()}")
            return ResponseHelpers.error_response(
                message='An unexpected error occurred while deleting service category. Please try again.',
                error_code='SERVER_ERROR',
                status_code=500
            )
