"""
View User Profile Controller - TRUE OOP Implementation
"""

from typing import Dict, Tuple
from src.entity import Role

# View All User Profiles Controller 
class ViewAllUserProfilesController:
    """
    View All User Profiles Controller - TRUE OOP
    
    Usage:
        controller = ViewAllUserProfilesController()
        response, status = controller.execute()
    """
    
    def execute(self) -> Tuple[Dict, int]:
        """Execute profiles retrieval"""

        # Call the Role Entity factory method to get all profiles
        # This is a factory method because it returns a list of Role objects
        profiles = Role.all()  
        profiles_data = [profile.to_dict() for profile in profiles]
        
        return {
            'success': True,
            'data': profiles_data,
            'count': len(profiles_data)
        }, 200

# View ONE User Profile Controller 
# NOT INCLUDED IN DIAGRAM DOCUMENTATION
class ViewOneUserProfileController:
    """
    View One User Profile Controller - TRUE OOP
    
    Usage:
        controller = ViewOneUserProfileController(profile_id)
        response, status = controller.execute()
    """
    
    def __init__(self, profile_id: int):
        """Initialize controller"""
        self.profile_id = profile_id
        self.profile = None
    
    def execute(self) -> Tuple[Dict, int]:
        """Execute profile retrieval"""
        self.profile = Role.find(self.profile_id)  
        if not self.profile:
            return {
                'success': False,
                'message': 'User profile not found'
            }, 404
        
        return {
            'success': True,
            'data': self.profile.to_dict()
        }, 200
