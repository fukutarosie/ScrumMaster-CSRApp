"""
ServiceCategory Entity Class - TRUE OOP Implementation
Manages service types from the existing 'service_types' table
"""

from typing import Dict, List, Optional
from datetime import datetime
from .supabase_config import get_supabase, execute_with_retry


class ServiceCategory:
    """
    ServiceCategory Entity - TRUE OOP Implementation

    This class manages the existing 'service_types' table that PINs use
    when creating requests. Platform Management can now manage these
    service types that are already in use by the system.

    This class implements proper OOP:
    - Objects hold data in memory (instance variables)
    - Instance methods do the actual work (not wrappers)
    - Factory methods (class methods) for querying
    - No static methods for business logic

    Usage:
        category = ServiceCategory()
        category.service_name = 'Environmental Conservation'
        category.save()

        category = ServiceCategory.find_by_id(1)
        category.service_name = 'Updated name'
        category.save()
    """

    def __init__(self, category_id: Optional[int] = None, category_data: Optional[Dict] = None):
        """
        Initialize a ServiceCategory instance

        Args:
            category_id: Load existing category from database by ID
            category_data: Initialize with existing category data

        Example:
            category = ServiceCategory(category_id=1)
            category = ServiceCategory(category_data={'id': 1, 'service_name': 'Education', ...})
            category = ServiceCategory()
        """
        self.id: Optional[int] = None
        self.service_name: Optional[str] = None
        self.created_at: Optional[str] = None

        if category_id is not None:
            self._load_from_id(category_id)
        elif category_data is not None:
            self._load_from_dict(category_data)

    def _load_from_id(self, category_id: int) -> None:
        """Load category data from database by ID (private method)"""
        supabase = get_supabase()
        result = execute_with_retry(
            lambda: supabase.table('service_types')
            .select('*')
            .eq('id', category_id)
            .execute()
        )
        if result and result.data:
            self._load_from_dict(result.data[0])

    def _load_from_dict(self, data: Dict) -> None:
        """Populate instance variables from dictionary (private method)"""
        self.id = data.get('id')
        self.service_name = data.get('service_name')
        self.created_at = data.get('created_at')

    def validate(self) -> tuple[bool, List[str]]:
        """
        Validate category object state

        Returns:
            Tuple of (is_valid, list_of_errors)
        """
        errors = []

        if not self.service_name or len(self.service_name.strip()) < 2:
            errors.append('Service name must be at least 2 characters')

        if self.service_name and len(self.service_name) > 100:
            errors.append('Service name must not exceed 100 characters')

        return len(errors) == 0, errors

    def check_uniqueness(self) -> tuple[bool, Optional[str]]:
        """
        Check if service name already exists

        Returns:
            Tuple of (is_unique, error_message)
        """
        supabase = get_supabase()

        query = supabase.table('service_types').select('id').eq('service_name', self.service_name)
        if self.id:
            query = query.neq('id', self.id)
        result = execute_with_retry(lambda: query.execute())
        if result and result.data:
            return False, f"Service name '{self.service_name}' already exists"

        return True, None

    def save(self) -> bool:
        """
        Save category to database (create or update)
        Instance method that DOES THE ACTUAL WORK

        Returns:
            True if successful

        Raises:
            ValueError: If validation fails
        """
        is_valid, errors = self.validate()
        if not is_valid:
            raise ValueError('; '.join(errors))

        is_unique, error = self.check_uniqueness()
        if not is_unique:
            raise ValueError(error)

        supabase = get_supabase()

        if self.id:
            update_data = {
                'service_name': self.service_name
            }

            result = execute_with_retry(
                lambda: supabase.table('service_types')
                .update(update_data)
                .eq('id', self.id)
                .execute()
            )
        else:
            insert_data = {
                'service_name': self.service_name
            }

            result = execute_with_retry(
                lambda: supabase.table('service_types')
                .insert(insert_data)
                .execute()
            )

            if result and result.data:
                self.id = result.data[0]['id']
                self.created_at = result.data[0]['created_at']

        return True

    def delete(self) -> bool:
        """
        Delete this category from database

        Returns:
            True if successful

        Raises:
            ValueError: If category has no ID
        """
        if not self.id:
            raise ValueError('Cannot delete service type without ID')

        supabase = get_supabase()

        print(f"[DEBUG] Attempting to delete service type with ID: {self.id}")

        try:
            result = execute_with_retry(
                lambda: supabase.table('service_types')
                .delete()
                .eq('id', self.id)
                .execute()
            )

            print(f"[DEBUG] Delete result: {result}")
            print(f"[DEBUG] Delete result.data: {result.data if result else 'None'}")

            if result and result.data:
                print(f"[DEBUG] Successfully deleted service type ID: {self.id}")
                return True
            else:
                print(f"[DEBUG] Delete returned no data for service type ID: {self.id}")
                return False

        except Exception as e:
            print(f"[ERROR] Failed to delete service type ID {self.id}: {str(e)}")
            import traceback
            print(f"[ERROR] Traceback: {traceback.format_exc()}")
            raise

    def to_dict(self) -> Dict:
        """
        Convert category object to dictionary

        Returns:
            Dictionary representation of category
        """
        return {
            'id': self.id,
            'service_name': self.service_name,
            'created_at': self.created_at
        }

    @classmethod
    def find_by_id(cls, category_id: int) -> Optional['ServiceCategory']:
        """
        Factory method to find category by ID

        Args:
            category_id: Category ID to search for

        Returns:
            ServiceCategory object or None if not found
        """
        supabase = get_supabase()
        result = execute_with_retry(
            lambda: supabase.table('service_types')
            .select('*')
            .eq('id', category_id)
            .execute()
        )

        if result and result.data:
            return cls(category_data=result.data[0])
        return None

    @classmethod
    def find_by_name(cls, name: str) -> Optional['ServiceCategory']:
        """
        Factory method to find category by service name

        Args:
            name: Service name to search for

        Returns:
            ServiceCategory object or None if not found
        """
        supabase = get_supabase()
        result = execute_with_retry(
            lambda: supabase.table('service_types')
            .select('*')
            .eq('service_name', name)
            .execute()
        )

        if result and result.data:
            return cls(category_data=result.data[0])
        return None

    @classmethod
    def find_all(cls) -> List['ServiceCategory']:
        """
        Factory method to get all categories

        Returns:
            List of ServiceCategory objects
        """
        supabase = get_supabase()
        result = execute_with_retry(
            lambda: supabase.table('service_types')
            .select('*')
            .order('service_name')
            .execute()
        )

        if result and result.data:
            return [cls(category_data=data) for data in result.data]
        return []

    @classmethod
    def search_by_keyword(cls, keyword: str) -> List['ServiceCategory']:
        """
        Factory method to search categories by keyword

        Args:
            keyword: Search keyword to match against service name

        Returns:
            List of ServiceCategory objects matching the keyword
        """
        supabase = get_supabase()

        search_pattern = f"%{keyword}%"

        result = execute_with_retry(
            lambda: supabase.table('service_types')
            .select('*')
            .ilike('service_name', search_pattern)
            .execute()
        )

        if result and result.data:
            return [cls(category_data=data) for data in result.data]
        return []
