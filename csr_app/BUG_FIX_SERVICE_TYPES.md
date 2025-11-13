# Bug Fix: Service Types 500 Error

**Date**: November 12, 2025  
**Status**: ✅ FIXED

## Problem

The `/api/requests/service-types` endpoint was returning **500 Internal Server Error**.

### Error Details
- **Endpoint**: `GET /api/requests/service-types`
- **Status Code**: 500
- **Root Cause**: Database table name mismatch

### Terminal Evidence
```
127.0.0.1 - - [12/Nov/2025 15:29:53] "GET /api/requests/service-types HTTP/1.1" 500 -
```

### Database Error
```
postgrest.exceptions.APIError: {'code': 'PGRST205', 'details': None, 
'hint': "Perhaps you meant the table 'public.service_types'", 
'message': "Could not find the table 'public.service_type' in the schema cache"}
```

## Root Cause

During the database table rename migration (plural → singular), the code was updated to use `service_type` (singular), but the actual database table remained `service_types` (plural).

**Files affected**:
- `csr_app/src/entity/request.py` (2 occurrences)

## Solution

Updated all references in `request.py` from `service_type` to `service_types`:

### Changes Made

1. **Line 196** - Fixed `validate_service_type()` method:
   ```python
   # Before
   lambda: supabase.table('service_type')
   
   # After
   lambda: supabase.table('service_types')
   ```

2. **Line 664** - Fixed `get_service_types()` method:
   ```python
   # Before
   lambda: supabase.table('service_type')
       .select('*')
       .execute()
   
   # After
   lambda: supabase.table('service_types')
       .select('*')
       .order('service_name')  # Also added ordering
       .execute()
   ```

## Testing

### Before Fix
```bash
GET /api/requests/service-types → 500 Error
```

### After Fix
```bash
GET /api/requests/service-types → 200 OK
Response: {
  "success": true,
  "data": [11 service types],
  "message": "Service types retrieved successfully"
}
```

### Sample Data Retrieved
- Companionship Visit
- Environment
- Errands
- Grocery Shopping
- Meal Delivery
- Medical Escort
- Pet Care
- Technology Support
- Transportation
- And more...

## Impact

This fix resolves:
- ✅ CSR browse page can now load service type filters
- ✅ PIN request creation form can load service types dropdown
- ✅ No more 500 errors on dashboard load
- ✅ Frontend can display service type categories properly

## Files Modified
- `csr_app/src/entity/request.py`

## Related Issues
- User account view fix (all users now show active/inactive status correctly)
- Controller: `ViewAllUserAccountsController` now uses `User.all(include_inactive=True)`

