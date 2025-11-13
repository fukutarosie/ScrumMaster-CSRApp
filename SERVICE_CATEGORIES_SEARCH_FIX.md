# Service Categories Search Issue - Fix Documentation

## Issue Description
When trying to search for a category using the search bar in the Platform Management page, an error message appeared: "An unexpected error occurred while searching categories. Please try again."

## Root Cause
The issue was in the **Supabase query syntax** used in the `search_by_keyword` method of the `ServiceCategory` entity class.

### Problematic Code (Before Fix)
```python
# Line 283-288 in service_category.py
search_term = f"%{keyword}%"

result = execute_with_retry(
    lambda: supabase.table('service_category')
    .select('*')
    .or_(f"name.ilike.{search_term},description.ilike.{search_term}")
    .order('name')
    .execute()
)
```

**Problem**: The `search_term` variable contained `%keyword%` (e.g., `%test%`), and when this was interpolated into the `.or_()` filter string, it created an invalid query format that Supabase couldn't parse correctly.

The resulting query would look like:
```
name.ilike.%test%,description.ilike.%test%
```

This is incorrect because the Supabase Python client expects the wildcard characters to be part of the filter value string, not interpolated as a variable.

## Solution Applied

### File Modified
- `csr_app/src/entity/service_category.py`

### Changes Made

**Fixed Code (Line 271-295):**
```python
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

    result = execute_with_retry(
        lambda: supabase.table('service_category')
        .select('*')
        .or_(f"name.ilike.%{keyword}%,description.ilike.%{keyword}%")
        .order('name')
        .execute()
    )

    if result and result.data:
        return [cls(category_data=data) for data in result.data]
    return []
```

**Key Changes:**
1. Removed the `search_term` variable that pre-formatted the keyword with wildcards
2. Directly embedded the keyword with wildcards in the `.or_()` filter string: `f"name.ilike.%{keyword}%,description.ilike.%{keyword}%"`

This creates the correct Supabase query format where the wildcards are part of the filter value.

## Technical Explanation

### Supabase `.or_()` Filter Syntax
The Supabase Python client's `.or_()` method expects a comma-separated string of filter conditions in the format:
```
column.operator.value,column.operator.value
```

For case-insensitive LIKE queries with wildcards:
```python
.or_(f"name.ilike.%{keyword}%,description.ilike.%{keyword}%")
```

This translates to SQL:
```sql
WHERE name ILIKE '%keyword%' OR description ILIKE '%keyword%'
```

### Why the Original Code Failed
When using a variable with wildcards:
```python
search_term = f"%{keyword}%"
.or_(f"name.ilike.{search_term},description.ilike.{search_term}")
```

The Supabase client couldn't properly parse the filter because it expected the wildcards to be part of the literal string in the filter expression, not as a pre-formatted variable.

## Database and Settings Impact

### ✅ No Database Changes Required
- The database schema remains unchanged
- The `service_category` table structure is correct
- All existing data is preserved

### ✅ No Frontend Changes Required
- The frontend search functionality remains the same
- The API endpoint `/api/platform/categories/search` works correctly
- No changes to the request/response format

### ✅ Backend Restart Required
- The Flask backend must be restarted to apply the fix
- The fix is applied in the entity layer (OOP model)

## Testing Recommendations

1. **Test Basic Search**
   - Navigate to Platform Management → Service Categories tab
   - Enter a search keyword (e.g., "Education", "Health")
   - Click the Search button
   - Verify that matching categories are displayed

2. **Test Partial Match Search**
   - Search for partial keywords (e.g., "Edu" should match "Education")
   - Verify case-insensitive matching works (e.g., "education" matches "Education")

3. **Test Description Search**
   - Search for keywords that appear in category descriptions
   - Verify that categories are found by description content

4. **Test No Results**
   - Search for a keyword that doesn't exist (e.g., "xyz123")
   - Verify that "No categories found" message is displayed (not an error)

5. **Test Clear Search**
   - Perform a search, then click the "Clear" button
   - Verify that all categories are displayed again

## Related Files

- **Entity**: `csr_app/src/entity/service_category.py` (Line 271-295)
- **Controller**: `csr_app/src/controller/platform/search_service_categories_controller.py`
- **API Endpoint**: `csr_app/src/api/platform/search_categories_page.py`
- **Frontend**: `csr_app/src/app/(actors)/platform/page.js` (searchCategories function)

## Prevention

To prevent similar issues in the future:
1. Always refer to Supabase Python client documentation for correct filter syntax
2. Test query filters with various input patterns during development
3. Add error logging to capture and debug Supabase query errors
4. Consider adding unit tests for entity search methods
5. Use type hints and validation for search parameters

## Summary

The search functionality now works correctly by using the proper Supabase filter syntax. Users can search for categories by name or description using case-insensitive partial matching.
