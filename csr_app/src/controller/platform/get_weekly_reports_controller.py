"""
Get Weekly Reports Controller - TRUE OOP Implementation
Orchestrates fetching weekly reports
"""

from typing import Tuple, Dict
from datetime import datetime, timedelta
from src.entity.weekly_reports import WeeklyReports
from src.utils.helpers import ResponseHelpers


class GetWeeklyReportsController:
    """
    Get Weekly Reports Controller - TRUE OOP
    
    Usage:
        controller = GetWeeklyReportsController(start_date)
        response, status = controller.execute()
    """
    
    def __init__(self, start_date: str = None):
        """
        Initialize controller with week start date
        
        Args:
            start_date: Week start date in YYYY-MM-DD format (defaults to current week Monday)
        """
        if start_date:
            self.start_date = start_date
        else:
            today = datetime.now()
            monday = today - timedelta(days=today.weekday())
            self.start_date = monday.strftime('%Y-%m-%d')
        
        self.report = None
        self.errors = []
    
    def validate_date(self) -> bool:
        """
        Validate date format
        
        Returns:
            True if valid, False otherwise
        """
        try:
            datetime.strptime(self.start_date, '%Y-%m-%d')
            return True
        except ValueError:
            self.errors.append("Invalid date format. Expected YYYY-MM-DD")
            return False
    
    def fetch_report(self) -> None:
        """
        Fetch weekly report for the specified week
        """
        self.report = WeeklyReports.get_by_week(self.start_date)
    
    def execute(self) -> Tuple[Dict, int]:
        """
        Execute weekly report retrieval process
        
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
                message='Weekly report retrieved successfully',
                status_code=200
            )
            
        except Exception as e:
            import traceback
            print(f"[ERROR] Get weekly report error: {str(e)}")
            print(f"[ERROR] Traceback: {traceback.format_exc()}")
            return ResponseHelpers.error_response(
                message='An unexpected error occurred while fetching weekly report. Please try again.',
                error_code='SERVER_ERROR',
                status_code=500
            )
