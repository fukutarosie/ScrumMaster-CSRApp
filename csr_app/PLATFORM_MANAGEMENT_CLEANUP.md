# Platform Management - Database Cleanup Instructions

## Overview
Platform Management was initially implemented with a new `service_category` table, but this was incorrect. The system already has a `service_types` table that PINs use when creating requests. Platform Management should manage these existing service types, not create a separate table.

## Changes Made

### 1. Entity Layer (`src/entity/service_category.py`)
- **Changed table reference**: `service_category` → `service_types`
- **Changed field names**: 
  - `name` → `service_name`
  - Removed `description` field (not in service_types table)
  - Removed `updated_at` field (not in service_types table)
- **Updated all methods** to work with the existing `service_types` table structure

### 2. Controller Layer
Updated all Platform Management controllers:
- `create_service_category_controller.py` - Now creates entries in `service_types`
- `update_service_category_controller.py` - Now updates entries in `service_types`
- `delete_service_category_controller.py` - Now deletes entries from `service_types`
- `list_service_categories_controller.py` - Now lists entries from `service_types`
- `search_service_categories_controller.py` - Now searches entries in `service_types`

All controllers now use `service_name` field instead of `name` and no longer reference `description`.

### 3. API Layer
No changes needed - API pages were already generic and don't hardcode field names.

## Database Cleanup Required

### Tables to Drop
The following table was mistakenly created and should be removed:
- `service_category`

### SQL Cleanup Statement

Execute this SQL statement in your Supabase SQL Editor to remove the unused table:

```sql
-- Drop the mistakenly created service_category table
DROP TABLE IF EXISTS public.service_category CASCADE;
```

**IMPORTANT**: Run this SQL statement in Supabase SQL Editor:
1. Go to your Supabase project dashboard
2. Navigate to SQL Editor
3. Create a new query
4. Paste the SQL statement above
5. Execute the query

### Verification Query

After cleanup, verify that only the correct table exists:

```sql
-- Verify service_types table exists and has data
SELECT * FROM public.service_types ORDER BY service_name;

-- Verify service_category table no longer exists (should return error)
SELECT * FROM public.service_category;
```

## Existing Service Types Table Structure

The `service_types` table that Platform Management now manages has the following structure:

```sql
CREATE TABLE public.service_types (
    id BIGSERIAL PRIMARY KEY,
    service_name TEXT NOT NULL UNIQUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

### Current Service Types in Database
The following service types are currently available (created by PINs):
- Companionship Visit
- Grocery Shopping
- Meal Delivery
- Transportation
- Home Maintenance
- Technology Help
- Medical Escort
- Reading/Writing Help
- Pet Care
- Errands

## API Changes for Frontend

### Request/Response Field Changes

**OLD (Incorrect)**:
```json
{
  "name": "Environmental Conservation",
  "description": "Activities related to environmental protection"
}
```

**NEW (Correct)**:
```json
{
  "service_name": "Environmental Conservation"
}
```

### API Endpoints (No Change)
All endpoints remain the same:
- `POST /api/platform/categories` - Create service type
- `GET /api/platform/categories` - List all service types
- `GET /api/platform/categories/<id>` - Get specific service type
- `PUT /api/platform/categories/<id>` - Update service type
- `DELETE /api/platform/categories/<id>` - Delete service type
- `GET /api/platform/categories/search?keyword=<keyword>` - Search service types

### Updated Request Examples

**Create Service Type**:
```bash
POST /api/platform/categories
{
  "service_name": "Pet Care"
}
```

**Update Service Type**:
```bash
PUT /api/platform/categories/1
{
  "service_name": "Pet Care and Walking"
}
```

**Response Format**:
```json
{
  "success": true,
  "message": "Service category created successfully",
  "data": {
    "id": 1,
    "service_name": "Pet Care",
    "created_at": "2024-01-15T10:30:00Z"
  }
}
```

## Files Modified

1. `csr_app/src/entity/service_category.py` - Updated to use `service_types` table
2. `csr_app/src/controller/platform/create_service_category_controller.py` - Updated field names
3. `csr_app/src/controller/platform/update_service_category_controller.py` - Updated field names
4. `csr_app/src/controller/platform/delete_service_category_controller.py` - No changes needed
5. `csr_app/src/controller/platform/list_service_categories_controller.py` - No changes needed
6. `csr_app/src/controller/platform/search_service_categories_controller.py` - No changes needed
7. `csr_app/src/entity/daily_reports.py` - Updated to use `service_types` table
8. `csr_app/src/entity/weekly_reports.py` - Updated to use `service_types` table
9. `csr_app/src/entity/monthly_reports.py` - Updated to use `service_types` table

## Impact on Other Components

### PIN Request Creation
- PINs already use the `service_types` table when creating requests
- The `requests` table has a `service_type` field that references service names from `service_types`
- Platform Management can now manage the service types that PINs see and use

### CSR Request Filtering
- CSRs filter requests by `service_type`
- Platform Management changes to service types will be immediately reflected in CSR filtering options

## Testing Checklist

After applying these changes, test the following:

- [ ] Platform Management can view all existing service types
- [ ] Platform Management can create new service types
- [ ] Platform Management can update existing service types
- [ ] Platform Management can delete service types (that aren't in use)
- [ ] Platform Management can search service types
- [ ] PINs can see updated service types when creating requests
- [ ] CSRs can filter by updated service types
- [ ] No references to `service_category` table remain in code
- [ ] SQL cleanup statement executed successfully

## Files Modified

1. `csr_app/src/entity/service_category.py` - Updated to use `service_types` table
2. `csr_app/src/controller/platform/create_service_category_controller.py` - Updated field names
3. `csr_app/src/controller/platform/update_service_category_controller.py` - Updated field names
4. `csr_app/src/controller/platform/delete_service_category_controller.py` - No changes needed
5. `csr_app/src/controller/platform/list_service_categories_controller.py` - No changes needed
6. `csr_app/src/controller/platform/search_service_categories_controller.py` - No changes needed

## Summary

✅ **Correct Implementation**: Platform Management now manages the existing `service_types` table that PINs use
❌ **Removed**: Mistaken `service_category` table that was created separately
🔧 **Field Changes**: `name` → `service_name`, removed `description` field
📊 **Database**: Execute SQL cleanup statement to drop unused `service_category` table
