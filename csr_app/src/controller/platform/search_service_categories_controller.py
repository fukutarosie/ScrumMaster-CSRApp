"""
Search Service Categories Controller - TRUE OOP Implementation
Orchestrates searching categories by keyword
"""

from typing import Tuple, Dict, List
from src.entity.service_category import ServiceCategory
from src.utils.helpers import ResponseHelpers


class SearchServiceCategoriesController:
    """
    Search Service Categories Controller - TRUE OOP
    
    Usage:
        controller = SearchServiceCategoriesController(keyword)
        response, status = controller.execute()
    """
    
    def __init__(self, keyword: str):
        """
        Initialize controller with search keyword
        
        Args:
            keyword: Search keyword
        """
        self.keyword = keyword.strip() if keyword else ""
        self.categories: List[ServiceCategory] = []
        self.errors: List[str] = []
    
    def validate_keyword(self) -> bool:
        """
        Validate search keyword
        
        Returns:
            True if valid, False otherwise
        """
        if not self.keyword:
            self.errors.append("Search keyword is required")
            return False
        
        if len(self.keyword) < 2:
            self.errors.append("Search keyword must be at least 2 characters")
            return False
        
        return True
    
    def search_categories(self) -> None:
        """
        Search categories by keyword
        """
        self.categories = ServiceCategory.search_by_keyword(self.keyword)
    
    def execute(self) -> Tuple[Dict, int]:
        """
        Execute category search process
        
        Returns:
            Tuple of (response_dict, status_code)
        """
        try:
            if not self.validate_keyword():
                return ResponseHelpers.error_response(
                    message='; '.join(self.errors),
                    error_code='VALIDATION_ERROR',
                    status_code=400
                )
            
            self.search_categories()
            
            categories_data = [category.to_dict() for category in self.categories]
            
            return ResponseHelpers.success_response(
                data={
                    'categories': categories_data,
                    'total': len(categories_data),
                    'keyword': self.keyword
                },
                message='Categories search completed successfully',
                status_code=200
            )
            
        except Exception as e:
            import traceback
            print(f"[ERROR] Search categories error: {str(e)}")
            print(f"[ERROR] Traceback: {traceback.format_exc()}")
            return ResponseHelpers.error_response(
                message='An unexpected error occurred while searching categories. Please try again.',
                error_code='SERVER_ERROR',
                status_code=500
            )
