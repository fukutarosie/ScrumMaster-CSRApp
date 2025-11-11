"""
WeeklyReports Entity Class - TRUE OOP Implementation
Aggregates and retrieves weekly activity reports
"""

from typing import Dict, List, Optional
from datetime import datetime, timedelta
from .supabase_config import get_supabase, execute_with_retry


class WeeklyReports:
    """
    WeeklyReports Entity - TRUE OOP Implementation
    
    This class aggregates weekly statistics from various tables
    
    Usage:
        report = WeeklyReports.get_by_week('2025-01-13')
    """
    
    def __init__(self, report_data: Optional[Dict] = None):
        """
        Initialize a WeeklyReports instance
        
        Args:
            report_data: Initialize with existing report data
        """
        self.week_start_date: Optional[str] = None
        self.week_end_date: Optional[str] = None
        self.total_requests: int = 0
        self.total_matches: int = 0
        self.total_new_users: int = 0
        self.total_active_users: int = 0
        self.total_categories: int = 0
        self.daily_breakdown: List[Dict] = []
        
        if report_data:
            self._load_from_dict(report_data)
    
    def _load_from_dict(self, data: Dict) -> None:
        """Populate instance variables from dictionary"""
        self.week_start_date = data.get('week_start_date')
        self.week_end_date = data.get('week_end_date')
        self.total_requests = data.get('total_requests', 0)
        self.total_matches = data.get('total_matches', 0)
        self.total_new_users = data.get('total_new_users', 0)
        self.total_active_users = data.get('total_active_users', 0)
        self.total_categories = data.get('total_categories', 0)
        self.daily_breakdown = data.get('daily_breakdown', [])
    
    def to_dict(self) -> Dict:
        """
        Convert report object to dictionary
        
        Returns:
            Dictionary representation of report
        """
        return {
            'week_start_date': self.week_start_date,
            'week_end_date': self.week_end_date,
            'total_requests': self.total_requests,
            'total_matches': self.total_matches,
            'total_new_users': self.total_new_users,
            'total_active_users': self.total_active_users,
            'total_categories': self.total_categories,
            'daily_breakdown': self.daily_breakdown
        }
    
    @classmethod
    def get_by_week(cls, start_date: str) -> Optional['WeeklyReports']:
        """
        Factory method to get weekly report starting from a specific date
        
        Args:
            start_date: Week start date in YYYY-MM-DD format (typically Monday)
            
        Returns:
            WeeklyReports object with aggregated data
        """
        supabase = get_supabase()
        
        start = datetime.strptime(start_date, '%Y-%m-%d')
        end = start + timedelta(days=6)
        
        report = cls()
        report.week_start_date = start.strftime('%Y-%m-%d')
        report.week_end_date = end.strftime('%Y-%m-%d')
        
        start_datetime = f"{report.week_start_date}T00:00:00"
        end_datetime = f"{report.week_end_date}T23:59:59"
        
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
                lambda: supabase.table('service_category')
                .select('id', count='exact')
                .execute()
            )
            report.total_categories = result.count if result else 0
        except Exception as e:
            print(f"[WARNING] Failed to get category count: {str(e)}")
            report.total_categories = 0
        
        return report
