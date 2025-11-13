"""
Get Monthly Reports Controller - TRUE OOP Implementation
Orchestrates fetching monthly reports
"""

from typing import Tuple, Dict
from datetime import datetime
from src.entity.monthly_reports import MonthlyReports
from src.utils.helpers import ResponseHelpers


class GetMonthlyReportsController:
    """
    Get Monthly Reports Controller - TRUE OOP
    
    Usage:
        controller = GetMonthlyReportsController(month)
        response, status = controller.execute()
    """
    
    def __init__(self, month: str = None):
        """
        Initialize controller with month
        
        Args:
            month: Month in YYYY-MM format (defaults to current month)
        """
        self.month = month or datetime.now().strftime('%Y-%m')
        self.report = None
        self.errors = []
    
    def validate_month(self) -> bool:
        """
        Validate month format
        
        Returns:
            True if valid, False otherwise
        """
        try:
            datetime.strptime(self.month, '%Y-%m')
            return True
        except ValueError:
            self.errors.append("Invalid month format. Expected YYYY-MM")
            return False
    
    def fetch_report(self) -> None:
        """
        Fetch monthly report for the specified month
        """
        self.report = MonthlyReports.get_by_month(self.month)
    
    def execute(self) -> Tuple[Dict, int]:
        """
        Execute monthly report retrieval process
        
        Returns:
            Tuple of (response_dict, status_code)
        """
        try:
            if not self.validate_month():
                return ResponseHelpers.error_response(
                    message='; '.join(self.errors),
                    error_code='VALIDATION_ERROR',
                    status_code=400
                )
            
            self.fetch_report()
            
            if not self.report:
                return ResponseHelpers.error_response(
                    message='Report not found',
                    error_code='NOT_FOUND',
                    status_code=404
                )
            
            return ResponseHelpers.success_response(
                data=self.report.to_dict(),
                message='Monthly report retrieved successfully',
                status_code=200
            )
            
        except Exception as e:
            import traceback
            print(f"[ERROR] Get monthly report error: {str(e)}")
            print(f"[ERROR] Traceback: {traceback.format_exc()}")
            return ResponseHelpers.error_response(
                message='An unexpected error occurred while fetching monthly report. Please try again.',
                error_code='SERVER_ERROR',
                status_code=500
            )
