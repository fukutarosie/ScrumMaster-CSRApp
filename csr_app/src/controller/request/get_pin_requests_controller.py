"""
Get PIN Requests Controller - TRUE OOP Implementation
"""

from typing import Dict, Tuple
from src.entity.request import Request
from src.entity.shortlist import Shortlist
from src.entity import User
from src.utils.helpers import ResponseHelpers, PaginationHelpers


class GetPINRequestsController:
    """
    Get PIN Requests Controller - TRUE OOP
    
    Usage:
        controller = GetPINRequestsController(auth_token, status_param, service_type, page, limit)
        response, status = controller.execute()
    """
    
    def __init__(self, auth_token: str, status_param: str = None, service_type: str = None, 
                 page_str: str = None, limit_str: str = None):
        """Initialize controller"""
        self.auth_token = auth_token
        self.status_param = status_param
        self.service_type = service_type
        self.page_str = page_str
        self.limit_str = limit_str
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
        """Execute request retrieval"""
        try:
            # Authenticate
            if not self.authenticate_user():
                return (ResponseHelpers.error_response('Invalid or expired token', 401), 401)
            
            # Get requests for this PIN user
            self.requests = Request.by_pin_user(self.user.id)
            
            # Apply filters
            if self.status_param:
                status_param_upper = self.status_param.upper()
                
                if status_param_upper == 'IN_PROGRESS':
                    # IN_PROGRESS: Request is ACTIVE and has a shortlist entry with IN_PROGRESS status
                    print(f"[DEBUG] Filtering for IN_PROGRESS requests")
                    print(f"[DEBUG] Total requests before filter: {len(self.requests)}")
                    in_progress_requests = []
                    for req in self.requests:
                        if req.status == Request.STATUS_ACTIVE:
                            assignment = Shortlist.active_assignment_for_request(req.id)
                            print(f"[DEBUG] Request {req.id} - Status: {req.status}, Assignment: {assignment.status if assignment else 'None'}")
                            if assignment and assignment.status == Shortlist.STATUS_IN_PROGRESS:
                                in_progress_requests.append(req)
                                print(f"[DEBUG] ✅ Request {req.id} added to IN_PROGRESS list")
                    self.requests = in_progress_requests
                    print(f"[DEBUG] Total IN_PROGRESS requests: {len(self.requests)}")
                    
                elif status_param_upper == Request.STATUS_FULFILLED:
                    # Include legacy 'COMPLETED' status for fulfilled tab
                    allowed_statuses = {Request.STATUS_FULFILLED, 'COMPLETED'}
                    self.requests = [r for r in self.requests if (r.status or '').upper() in allowed_statuses]
                else:
                    # Normal status filter
                    allowed_statuses = {status_param_upper}
                    self.requests = [r for r in self.requests if (r.status or '').upper() in allowed_statuses]
                    
            if self.service_type:
                self.requests = [r for r in self.requests if r.service_type == self.service_type]
            
            # Parse pagination
            page, limit = self.parse_pagination()
            
            # Apply pagination
            start = (page - 1) * limit
            end = start + limit
            paginated_requests = self.requests[start:end]
            
            # Convert to dictionaries and add assignment status
            requests_data = []
            for req in paginated_requests:
                req_dict = req.to_dict()
                # Add assignment status for all requests
                assignment = Shortlist.active_assignment_for_request(req.id)
                if assignment:
                    req_dict['assignment_status'] = assignment.status
                    req_dict['active_assignment'] = assignment.to_assignment_dict()
                else:
                    req_dict['assignment_status'] = None
                    req_dict['active_assignment'] = None
                requests_data.append(req_dict)
            
            # Build pagination info
            pagination = {
                'page': page,
                'limit': limit,
                'total': len(self.requests),
                'pages': (len(self.requests) + limit - 1) // limit
            }
            
            return (ResponseHelpers.success_response(
                data=requests_data,
                message='Requests retrieved successfully',
                pagination=pagination
            ), 200)
            
        except Exception as e:
            print(f"[ERROR] Get PIN requests failed: {str(e)}")
            return (ResponseHelpers.error_response('Internal server error'), 500)
