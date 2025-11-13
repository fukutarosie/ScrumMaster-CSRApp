"""
Get Daily Reports Controller - TRUE OOP Implementation
Orchestrates fetching daily reports
"""

from typing import Tuple, Dict
from datetime import datetime
from src.entity.daily_reports import DailyReports
from src.utils.helpers import ResponseHelpers


class GetDailyReportsController:
    """
    Get Daily Reports Controller - TRUE OOP
    
    Usage:
        controller = GetDailyReportsController(date)
        response, status = controller.execute()
    """
    
    def __init__(self, report_date: str = None):
        """
        Initialize controller with report date
        
        Args:
            report_date: Date in YYYY-MM-DD format (defaults to today)
        """
        self.report_date = report_date or datetime.now().strftime('%Y-%m-%d')
        self.report = None
        self.errors = []
    
    def validate_date(self) -> bool:
        """
        Validate date format
        
        Returns:
            True if valid, False otherwise
        """
        try:
            datetime.strptime(self.report_date, '%Y-%m-%d')
            return True
        except ValueError:
            self.errors.append("Invalid date format. Expected YYYY-MM-DD")
            return False
    
    def fetch_report(self) -> None:
        """
        Fetch daily report for the specified date
        """
        self.report = DailyReports.get_by_date(self.report_date)
    
    def execute(self) -> Tuple[Dict, int]:
        """
        Execute daily report retrieval process
        
        Returns:
            Tuple of (response_dict, status_code)
        """
        try:
            if not self.validate_date():
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
                message='Daily report retrieved successfully',
                status_code=200
            )
            
        except Exception as e:
            import traceback
            print(f"[ERROR] Get daily report error: {str(e)}")
            print(f"[ERROR] Traceback: {traceback.format_exc()}")
            return ResponseHelpers.error_response(
                message='An unexpected error occurred while fetching daily report. Please try again.',
                error_code='SERVER_ERROR',
                status_code=500
            )
