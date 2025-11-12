"""
ServiceCategory Entity Class - TRUE OOP Implementation
Holds service category data in memory and performs operations on itself
"""

from typing import Dict, List, Optional
from datetime import datetime
from .supabase_config import get_supabase, execute_with_retry


class ServiceCategory:
    """
    ServiceCategory Entity - TRUE OOP Implementation

    This class implements proper OOP:
    - Objects hold data in memory (instance variables)
    - Instance methods do the actual work (not wrappers)
    - Factory methods (class methods) for querying
    - No static methods for business logic

    Usage:
        category = ServiceCategory()
        category.name = 'Environmental Conservation'
        category.description = 'Activities related to environmental protection'
        category.save()

        category = ServiceCategory.find_by_id(1)
        category.description = 'Updated description'
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
            category = ServiceCategory(category_data={'id': 1, 'name': 'Education', ...})
            category = ServiceCategory()
        """
        self.id: Optional[int] = None
        self.name: Optional[str] = None
        self.description: Optional[str] = None
        self.created_at: Optional[str] = None
        self.updated_at: Optional[str] = None

        if category_id is not None:
            self._load_from_id(category_id)
        elif category_data is not None:
            self._load_from_dict(category_data)

    def _load_from_id(self, category_id: int) -> None:
        """Load category data from database by ID (private method)"""
        supabase = get_supabase()
        result = execute_with_retry(
            lambda: supabase.table('service_category')
            .select('*')
            .eq('id', category_id)
            .execute()
        )
        if result and result.data:
            self._load_from_dict(result.data[0])

    def _load_from_dict(self, data: Dict) -> None:
        """Populate instance variables from dictionary (private method)"""
        self.id = data.get('id')
        self.name = data.get('name')
        self.description = data.get('description')
        self.created_at = data.get('created_at')
        self.updated_at = data.get('updated_at')

    def validate(self) -> tuple[bool, List[str]]:
        """
        Validate category object state

        Returns:
            Tuple of (is_valid, list_of_errors)
        """
        errors = []

        if not self.name or len(self.name.strip()) < 2:
            errors.append('Category name must be at least 2 characters')

        if self.name and len(self.name) > 100:
            errors.append('Category name must not exceed 100 characters')

        if self.description and len(self.description) > 500:
            errors.append('Category description must not exceed 500 characters')

        return len(errors) == 0, errors

    def check_uniqueness(self) -> tuple[bool, Optional[str]]:
        """
        Check if category name already exists

        Returns:
            Tuple of (is_unique, error_message)
        """
        supabase = get_supabase()

        query = supabase.table('service_category').select('id').eq('name', self.name)
        if self.id:
            query = query.neq('id', self.id)
        result = execute_with_retry(lambda: query.execute())
        if result and result.data:
            return False, f"Category name '{self.name}' already exists"

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
                'name': self.name,
                'description': self.description,
                'updated_at': datetime.utcnow().isoformat()
            }

            result = execute_with_retry(
                lambda: supabase.table('service_category')
                .update(update_data)
                .eq('id', self.id)
                .execute()
            )
        else:
            insert_data = {
                'name': self.name,
                'description': self.description or ''
            }

            result = execute_with_retry(
                lambda: supabase.table('service_category')
                .insert(insert_data)
                .execute()
            )

            if result and result.data:
                self.id = result.data[0]['id']
                self.created_at = result.data[0]['created_at']
                self.updated_at = result.data[0].get('updated_at')

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
            raise ValueError('Cannot delete category without ID')

        supabase = get_supabase()
        result = execute_with_retry(
            lambda: supabase.table('service_category')
            .delete()
            .eq('id', self.id)
            .execute()
        )

        return bool(result and result.data)

    def to_dict(self) -> Dict:
        """
        Convert category object to dictionary

        Returns:
            Dictionary representation of category
        """
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'created_at': self.created_at,
            'updated_at': self.updated_at
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
            lambda: supabase.table('service_category')
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
        Factory method to find category by name

        Args:
            name: Category name to search for

        Returns:
            ServiceCategory object or None if not found
        """
        supabase = get_supabase()
        result = execute_with_retry(
            lambda: supabase.table('service_category')
            .select('*')
            .eq('name', name)
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
            lambda: supabase.table('service_category')
            .select('*')
            .order('name')
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
            keyword: Search keyword to match against name or description

        Returns:
            List of ServiceCategory objects matching the keyword
        """
        supabase = get_supabase()

        search_pattern = f"%{keyword}%"

        result = execute_with_retry(
            lambda: supabase.table('service_category')
            .select('*')
            .or_(f'name.ilike."{search_pattern}",description.ilike."{search_pattern}"')
            .order('name')
            .execute()
        )

        if result and result.data:
            return [cls(category_data=data) for data in result.data]
        return []
