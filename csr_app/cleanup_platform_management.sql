-- ============================================================================
-- Platform Management Database Cleanup
-- ============================================================================
-- This script removes the mistakenly created service_category table
-- Platform Management now uses the existing service_types table instead
-- ============================================================================

-- Drop the unused service_category table
-- This table was created by mistake during Platform Management implementation
-- The correct table to use is service_types (which PINs already use)
DROP TABLE IF EXISTS public.service_category CASCADE;

-- ============================================================================
-- Verification Queries (Run these after cleanup to verify)
-- ============================================================================

-- 1. Verify service_types table exists and has data
-- This should return all service types that PINs can use
SELECT 
    id,
    service_name,
    created_at
FROM public.service_types 
ORDER BY service_name;

-- 2. Verify service_category table no longer exists
-- This query should return an error: "relation does not exist"
-- If it returns data, the cleanup was not successful
-- SELECT * FROM public.service_category;

-- ============================================================================
-- Expected Results After Cleanup
-- ============================================================================
-- ✅ service_types table exists with current service types
-- ✅ service_category table does not exist
-- ✅ Platform Management can manage service_types entries
-- ✅ PINs continue to use service_types when creating requests
-- ============================================================================
