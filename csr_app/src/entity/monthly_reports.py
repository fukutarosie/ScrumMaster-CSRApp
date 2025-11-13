"""
MonthlyReports Entity Class - TRUE OOP Implementation
Aggregates and retrieves monthly activity reports
"""

from typing import Dict, List, Optional
from datetime import datetime
from calendar import monthrange
from .supabase_config import get_supabase, execute_with_retry


class MonthlyReports:
    """
    MonthlyReports Entity - TRUE OOP Implementation
    
    This class aggregates monthly statistics from various tables
    
    Usage:
        report = MonthlyReports.get_by_month('2025-01')
    """
    
    def __init__(self, report_data: Optional[Dict] = None):
        """
        Initialize a MonthlyReports instance
        
        Args:
            report_data: Initialize with existing report data
        """
        self.month: Optional[str] = None
        self.month_start_date: Optional[str] = None
        self.month_end_date: Optional[str] = None
        self.total_requests: int = 0
        self.total_matches: int = 0
        self.total_new_users: int = 0
        self.total_active_users: int = 0
        self.total_categories: int = 0
        self.weekly_breakdown: List[Dict] = []
        
        if report_data:
            self._load_from_dict(report_data)
    
    def _load_from_dict(self, data: Dict) -> None:
        """Populate instance variables from dictionary"""
        self.month = data.get('month')
        self.month_start_date = data.get('month_start_date')
        self.month_end_date = data.get('month_end_date')
        self.total_requests = data.get('total_requests', 0)
        self.total_matches = data.get('total_matches', 0)
        self.total_new_users = data.get('total_new_users', 0)
        self.total_active_users = data.get('total_active_users', 0)
        self.total_categories = data.get('total_categories', 0)
        self.weekly_breakdown = data.get('weekly_breakdown', [])
    
    def to_dict(self) -> Dict:
        """
        Convert report object to dictionary
        
        Returns:
            Dictionary representation of report
        """
        return {
            'month': self.month,
            'month_start_date': self.month_start_date,
            'month_end_date': self.month_end_date,
            'total_requests': self.total_requests,
            'total_matches': self.total_matches,
            'total_new_users': self.total_new_users,
            'total_active_users': self.total_active_users,
            'total_categories': self.total_categories,
            'weekly_breakdown': self.weekly_breakdown
        }
    
    @classmethod
    def get_by_month(cls, month: str) -> Optional['MonthlyReports']:
        """
        Factory method to get monthly report for a specific month
        
        Args:
            month: Month in YYYY-MM format
            
        Returns:
            MonthlyReports object with aggregated data
        """
        supabase = get_supabase()
        
        year, month_num = map(int, month.split('-'))
        last_day = monthrange(year, month_num)[1]
        
        report = cls()
        report.month = month
        report.month_start_date = f"{month}-01"
        report.month_end_date = f"{month}-{last_day:02d}"
        
        start_datetime = f"{report.month_start_date}T00:00:00"
        end_datetime = f"{report.month_end_date}T23:59:59"
        
        try:
            result = execute_with_retry(
                lambda: supabase.table('pin_request')
                .select('id', count='exact')
                .gte('created_at', start_datetime)
                .lte('created_at', end_datetime)
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
                .gte('created_at', start_datetime)
                .lte('created_at', end_datetime)
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
                .gte('created_at', start_datetime)
                .lte('created_at', end_datetime)
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
                lambda: supabase.table('service_types')
                .select('id', count='exact')
                .execute()
            )
            report.total_categories = result.count if result else 0
        except Exception as e:
            print(f"[WARNING] Failed to get category count: {str(e)}")
            report.total_categories = 0
        
        return report
