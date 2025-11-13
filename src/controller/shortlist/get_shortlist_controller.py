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

            # If frontend does not provide a status filter, default to SHORTLISTED
            # to show the CSR their active shortlist items first.
            if not status_filter:
                status_filter = Shortlist.STATUS_SHORTLISTED
            
            # Parse pagination
            try:
                page = int(page_str) if page_str else 1
                limit = int(limit_str) if limit_str else 50
            except:
                page = 1
                limit = 50
            
            # Calculate offset from page number
            offset = (page - 1) * limit
            
            # Query shortlist entries (entity returns objects). Entity doesn't support pagination directly,
            # so we fetch filtered results and slice in-memory for now.
            shortlist_entries = Shortlist.search(
                csr_user_id=csr_user_id,
                status=status_filter
            )
            paged_entries = shortlist_entries[offset: offset + limit] if shortlist_entries else []
            shortlist_items = []
            
            for entry in paged_entries:
                item_dict = entry.to_dict()
                # Enrich with active assignment info if request data exists
                if item_dict.get('requests') and entry.request_id:
                    active_assignment = Shortlist.active_assignment_for_request(entry.request_id)
                    if active_assignment:
                        # Add active_assignment to the request data
                        item_dict['requests']['active_assignment'] = {
                            'id': active_assignment.id,
                            'csr_user_id': active_assignment.csr_user_id,
                            'status': active_assignment.status
                        }
                        # Also add to 'request' key for consistency
                        if item_dict.get('request'):
                            item_dict['request']['active_assignment'] = item_dict['requests']['active_assignment']
                shortlist_items.append(item_dict)
            
            print(f"[DEBUG] Shortlist controller - User ID: {csr_user_id}, Status filter: {status_filter}, Items found: {len(shortlist_items)}")
            if shortlist_items:
                print(f"[DEBUG] First item: {shortlist_items[0]}")
            
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
