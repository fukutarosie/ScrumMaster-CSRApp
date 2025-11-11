"""
DailyReports Entity Class - TRUE OOP Implementation
Aggregates and retrieves daily activity reports
"""

from typing import Dict, List, Optional
from datetime import datetime, date
from .supabase_config import get_supabase, execute_with_retry


class DailyReports:
    """
    DailyReports Entity - TRUE OOP Implementation
    
    This class aggregates daily statistics from various tables
    
    Usage:
        reports = DailyReports.get_by_date('2025-01-15')
        report = DailyReports.get_summary_for_date('2025-01-15')
    """
    
    def __init__(self, report_data: Optional[Dict] = None):
        """
        Initialize a DailyReports instance
        
        Args:
            report_data: Initialize with existing report data
        """
        self.report_date: Optional[str] = None
        self.total_requests: int = 0
        self.total_matches: int = 0
        self.total_new_users: int = 0
        self.total_active_users: int = 0
        self.total_categories: int = 0
        
        if report_data:
            self._load_from_dict(report_data)
    
    def _load_from_dict(self, data: Dict) -> None:
        """Populate instance variables from dictionary"""
        self.report_date = data.get('report_date')
        self.total_requests = data.get('total_requests', 0)
        self.total_matches = data.get('total_matches', 0)
        self.total_new_users = data.get('total_new_users', 0)
        self.total_active_users = data.get('total_active_users', 0)
        self.total_categories = data.get('total_categories', 0)
    
    def to_dict(self) -> Dict:
        """
        Convert report object to dictionary
        
        Returns:
            Dictionary representation of report
        """
        return {
            'report_date': self.report_date,
            'total_requests': self.total_requests,
            'total_matches': self.total_matches,
            'total_new_users': self.total_new_users,
            'total_active_users': self.total_active_users,
            'total_categories': self.total_categories
        }
    
    @classmethod
    def get_by_date(cls, report_date: str) -> Optional['DailyReports']:
        """
        Factory method to get daily report for a specific date
        
        Args:
            report_date: Date in YYYY-MM-DD format
            
        Returns:
            DailyReports object with aggregated data
        """
        supabase = get_supabase()
        
        report = cls()
        report.report_date = report_date
        
        try:
            result = execute_with_retry(
                lambda: supabase.table('pin_request')
                .select('id', count='exact')
                .gte('created_at', f"{report_date}T00:00:00")
                .lt('created_at', f"{report_date}T23:59:59")
                .execute()
            )
            report.total_requests = result.count if result else 0
        except Exception as e:
            print(f"[WARNING] Failed to get request count: {str(e)}")
            report.total_requests = 0
        
        try:
            result = execute_with_retry(
                lambda: supabase.table('shortlist')
                .select('id', count='exact')
                .eq('status', 'matched')
                .gte('created_at', f"{report_date}T00:00:00")
                .lt('created_at', f"{report_date}T23:59:59")
                .execute()
            )
            report.total_matches = result.count if result else 0
        except Exception as e:
            print(f"[WARNING] Failed to get match count: {str(e)}")
            report.total_matches = 0
        
        try:
            result = execute_with_retry(
                lambda: supabase.table('user')
                .select('id', count='exact')
                .gte('created_at', f"{report_date}T00:00:00")
                .lt('created_at', f"{report_date}T23:59:59")
                .execute()
            )
            report.total_new_users = result.count if result else 0
        except Exception as e:
            print(f"[WARNING] Failed to get new user count: {str(e)}")
            report.total_new_users = 0
        
        try:
            result = execute_with_retry(
                lambda: supabase.table('user')
                .select('id', count='exact')
                .eq('is_active', True)
                .execute()
            )
            report.total_active_users = result.count if result else 0
        except Exception as e:
            print(f"[WARNING] Failed to get active user count: {str(e)}")
            report.total_active_users = 0
        
        try:
            result = execute_with_retry(
                lambda: supabase.table('service_category')
                .select('id', count='exact')
                .execute()
            )
            report.total_categories = result.count if result else 0
        except Exception as e:
            print(f"[WARNING] Failed to get category count: {str(e)}")
            report.total_categories = 0
        
        return report
    
    @classmethod
    def get_date_range(cls, start_date: str, end_date: str) -> List['DailyReports']:
        """
        Factory method to get daily reports for a date range
        
        Args:
            start_date: Start date in YYYY-MM-DD format
            end_date: End date in YYYY-MM-DD format
            
        Returns:
            List of DailyReports objects
        """
        from datetime import timedelta
        
        start = datetime.strptime(start_date, '%Y-%m-%d').date()
        end = datetime.strptime(end_date, '%Y-%m-%d').date()
        
        reports = []
        current = start
        while current <= end:
            report = cls.get_by_date(current.strftime('%Y-%m-%d'))
            if report:
                reports.append(report)
            current += timedelta(days=1)
        
        return reports
