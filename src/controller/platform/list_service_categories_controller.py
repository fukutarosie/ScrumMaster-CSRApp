"""
List Service Categories Controller - TRUE OOP Implementation
Orchestrates fetching and filtering categories
"""

from typing import Tuple, Dict, List
from src.entity.service_category import ServiceCategory
from src.utils.helpers import ResponseHelpers


class ListServiceCategoriesController:
    """
    List Service Categories Controller - TRUE OOP
    
    Usage:
        controller = ListServiceCategoriesController(filters)
        response, status = controller.execute()
    """
    
    def __init__(self, filters: Dict = None):
        """
        Initialize controller with optional filters
        
        Args:
            filters: Optional filters for pagination, sorting, etc.
        """
        self.filters = filters or {}
        self.categories: List[ServiceCategory] = []
    
    def fetch_categories(self) -> None:
        """
        Fetch all categories from database
        """
        self.categories = ServiceCategory.find_all()
    
    def execute(self) -> Tuple[Dict, int]:
        """
        Execute category listing process
        
        Returns:
            Tuple of (response_dict, status_code)
        """
        try:
            self.fetch_categories()
            
            categories_data = [category.to_dict() for category in self.categories]
            
            return ResponseHelpers.success_response(
                data={
                    'categories': categories_data,
                    'total': len(categories_data)
                },
                message='Categories retrieved successfully',
                status_code=200
            )
            
        except Exception as e:
            import traceback
            print(f"[ERROR] List categories error: {str(e)}")
            print(f"[ERROR] Traceback: {traceback.format_exc()}")
            return ResponseHelpers.error_response(
                message='An unexpected error occurred while fetching categories. Please try again.',
                error_code='SERVER_ERROR',
                status_code=500
            )
