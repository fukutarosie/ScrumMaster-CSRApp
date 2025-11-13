"""
Get Completed Matches Controller - TRUE OOP Implementation
"""

from typing import Dict, Tuple
from datetime import datetime
from src.entity.request import Request
from src.entity.shortlist import Shortlist
from src.entity import User
from src.utils.helpers import ResponseHelpers


class GetCompletedMatchesController:
    """
    Get Completed Matches Controller - TRUE OOP
    
    Usage:
        controller = GetCompletedMatchesController(auth_token, start_date, end_date, page, limit)
        response, status = controller.execute()
    """
    
    def __init__(self, auth_token: str, start_date: str = None, end_date: str = None,
                 page_str: str = None, limit_str: str = None, service_type: str = None):
        """Initialize controller"""
        self.auth_token = auth_token
        self.start_date = start_date
        self.end_date = end_date
        self.page_str = page_str
        self.limit_str = limit_str
        self.service_type = service_type.lower() if service_type else None
        self.user = None
        self.requests = []
    
    def authenticate_user(self) -> bool:
        """Authenticate user from token"""
        self.user = User.verify_token(self.auth_token)
        return self.user is not None
    
    def parse_pagination(self) -> Tuple[int, int]:
        """Parse pagination parameters"""
        try:
            page = int(self.page_str) if self.page_str else 1
            limit = int(self.limit_str) if self.limit_str else 10
        except:
            page = 1
            limit = 10
        return page, limit
    
    def execute(self) -> Tuple[Dict, int]:
        """Execute completed matches retrieval"""
        try:
            # Authenticate
            if not self.authenticate_user():
                return (ResponseHelpers.error_response('Invalid or expired token', 401), 401)
            
            # Get fulfilled requests for this PIN user
            self.requests = Request.by_pin_user(self.user.id)
            self.requests = [r for r in self.requests if r.status == Request.STATUS_FULFILLED]
            
            print(f"[DEBUG] Total fulfilled requests: {len(self.requests)}")
            print(f"[DEBUG] Date filters - start: {self.start_date}, end: {self.end_date}, service: {self.service_type}")
            
            # Apply date filters
            if self.start_date:
                before_filter = len(self.requests)
                self.requests = [
                    r for r in self.requests
                    if self._is_on_or_after(r.fulfilled_at, self.start_date)
                ]
                print(f"[DEBUG] Start date filter: {before_filter} -> {len(self.requests)} requests")
            if self.end_date:
                before_filter = len(self.requests)
                self.requests = [
                    r for r in self.requests
                    if self._is_on_or_before(r.fulfilled_at, self.end_date)
                ]
                print(f"[DEBUG] End date filter: {before_filter} -> {len(self.requests)} requests")
            
            # Apply service type filter
            if self.service_type:
                self.requests = [
                    r for r in self.requests
                    if (r.service_type or '').lower() == self.service_type
                ]
            
            # Parse pagination
            page, limit = self.parse_pagination()
            
            # Apply pagination
            start = (page - 1) * limit
            end = start + limit
            paginated_requests = self.requests[start:end]
            
            # Convert to dictionaries
            requests_data = []
            print(f"[DEBUG] Processing {len(paginated_requests)} paginated requests")
            
            for req in paginated_requests:
                try:
                    req_dict = req.to_dict()
                    print(f"[DEBUG] Processing request {req.id}, status: {req.status}")
                    
                    # Get assignment/match info
                    try:
                        assignment = Shortlist.active_assignment_for_request(req.id)
                        if assignment:
                            print(f"[DEBUG] Found assignment for request {req.id}, status: {assignment.status}")
                            req_dict['assignment_status'] = assignment.status
                            try:
                                assignment_dict = assignment.to_assignment_dict()
                                req_dict['active_assignment'] = assignment_dict
                                # IMPORTANT: Frontend expects 'matched_csr' as an array
                                req_dict['matched_csr'] = [assignment_dict]
                                print(f"[DEBUG] Assignment dict created for request {req.id}")
                                print(f"[DEBUG] matched_csr data: {req_dict['matched_csr']}")
                            except Exception as e:
                                print(f"[WARNING] Failed to get assignment dict for request {req.id}: {str(e)}")
                                import traceback
                                traceback.print_exc()
                                req_dict['active_assignment'] = None
                                req_dict['matched_csr'] = []
                        else:
                            print(f"[DEBUG] No assignment found for request {req.id}")
                            req_dict['assignment_status'] = None
                            req_dict['active_assignment'] = None
                            req_dict['matched_csr'] = []
                    except Exception as e:
                        print(f"[WARNING] Failed to get assignment for request {req.id}: {str(e)}")
                        import traceback
                        traceback.print_exc()
                        req_dict['assignment_status'] = None
                        req_dict['active_assignment'] = None
                        req_dict['matched_csr'] = []
                    
                    requests_data.append(req_dict)
                    print(f"[DEBUG] Successfully processed request {req.id}")
                    
                except Exception as e:
                    print(f"[ERROR] Failed to process request {req.id}: {str(e)}")
                    import traceback
                    traceback.print_exc()
                    # Skip this request but continue with others
                    continue
            
            # Build pagination info
            pagination = {
                'page': page,
                'limit': limit,
                'total': len(self.requests),
                'pages': (len(self.requests) + limit - 1) // limit
            }
            
            # Prepare response data with pagination
            response_data = {
                'success': True,
                'message': 'Completed matches retrieved successfully',
                'data': requests_data,
                'pagination': pagination
            }
            
            return (response_data, 200)
            
        except Exception as e:
            print(f"[ERROR] Get completed matches failed: {str(e)}")
            import traceback
            traceback.print_exc()
            return (ResponseHelpers.error_response('Internal server error'), 500)

    def _parse_date(self, date_str: str) -> datetime:
        """Parse ISO datetime string or date string safely"""
        if not date_str:
            return None
        try:
            # Handle ISO datetime (e.g., "2025-11-10T15:30:00" or "2025-11-10T15:30:00Z")
            cleaned = date_str.replace('Z', '+00:00')
            return datetime.fromisoformat(cleaned)
        except Exception:
            try:
                # Handle date only (e.g., "2025-11-10")
                return datetime.strptime(date_str, '%Y-%m-%d')
            except Exception as e:
                print(f"[ERROR] Failed to parse date '{date_str}': {str(e)}")
                return None

    def _is_on_or_after(self, date_str: str, start_date_str: str) -> bool:
        """Check if date is on or after start date"""
        if not date_str:
            print(f"[WARNING] fulfilled_at is None/empty for comparison")
            return True  # Include requests without fulfilled_at date
        date_val = self._parse_date(date_str)
        start_val = self._parse_date(start_date_str)
        if not date_val or not start_val:
            print(f"[DEBUG] Date parsing failed - fulfilled_at: {date_str}, start_date: {start_date_str}")
            return True  # Include if date parsing fails
        result = date_val.date() >= start_val.date()
        return result

    def _is_on_or_before(self, date_str: str, end_date_str: str) -> bool:
        """Check if date is on or before end date"""
        if not date_str:
            print(f"[WARNING] fulfilled_at is None/empty for comparison")
            return True  # Include requests without fulfilled_at date
        date_val = self._parse_date(date_str)
        end_val = self._parse_date(end_date_str)
        if not date_val or not end_val:
            print(f"[DEBUG] Date parsing failed - fulfilled_at: {date_str}, end_date: {end_date_str}")
            return True  # Include if date parsing fails
        result = date_val.date() <= end_val.date()
        return result
