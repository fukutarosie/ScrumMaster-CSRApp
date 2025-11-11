"""
Get Shortlist Controller - CSR views their shortlist (Control Layer)
"""

from src.entity.shortlist import Shortlist
from src.entity import User
from src.utils.helpers import ResponseHelpers

class GetShortlistController:
    """
    Get CSR's shortlist with filters and pagination
    """
    
    @staticmethod
    def get_shortlist(auth_token, status_filter, page_str, limit_str):
        """
        Get CSR's shortlist with filters
        
        Returns: (response_dict, status_code)
        """
        try:
            # Verify token and get user (entity object)
            user = User.verify_token(auth_token)
            if not user:
                return (ResponseHelpers.error_response('Invalid or expired token', 401), 401)
            
            csr_user_id = user.id

            # If frontend does not provide a status filter, fetch ALL items
            # The frontend will handle filtering by tabs
            # Only apply filter if explicitly provided
            if status_filter and status_filter.strip():
                status_filter = status_filter.strip()
            else:
                status_filter = None
            
            # Parse pagination
            try:
                page = int(page_str) if page_str else 1
                limit = int(limit_str) if limit_str else 50
            except:
                page = 1
                limit = 50
            
            # Calculate offset from page number
            offset = (page - 1) * limit
            
            # Query shortlist entries with database-level pagination
            shortlist_entries = Shortlist.search(
                csr_user_id=csr_user_id,
                status=status_filter,
                limit=limit,
                offset=offset
            )
            shortlist_items = [entry.to_dict() for entry in shortlist_entries]
            
            print(f"[DEBUG] Shortlist controller - User ID: {csr_user_id}, Status filter: '{status_filter if status_filter else 'ALL'}', Items found: {len(shortlist_items)}")
            if shortlist_items:
                print(f"[DEBUG] Sample item statuses: {[item['status'] for item in shortlist_items[:3]]}")
            
            # Return response
            return (ResponseHelpers.success_response(
                data=shortlist_items,
                message='Shortlist retrieved successfully'
            ), 200)
            
        except Exception as e:
            print(f"[ERROR] Get shortlist failed: {str(e)}")
            import traceback
            traceback.print_exc()
            return (ResponseHelpers.error_response('Internal server error'), 500)
