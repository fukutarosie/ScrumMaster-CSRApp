-- ============================================================================
-- ESSENTIAL DATABASE UPDATES - Quick Start
-- ============================================================================
-- These are the CRITICAL updates that should be applied immediately
-- Execute in Supabase SQL Editor: https://supabase.com/dashboard/project/_/sql
-- ============================================================================

-- ============================================================================
-- 1. ADD UNIQUE CONSTRAINT (HIGHEST PRIORITY)
-- ============================================================================
-- Prevents duplicate shortlist entries from race conditions

ALTER TABLE shortlist
ADD CONSTRAINT unique_csr_request UNIQUE (csr_user_id, request_id);

-- ============================================================================
-- 2. ADD COLUMN COMMENT (CRITICAL - No Code Changes Needed)
-- ============================================================================
-- Clarifies that volunteered_hours is actually a rating, not hours

COMMENT ON COLUMN shortlist.volunteered_hours IS 'PIN user rating of CSR performance (1-5 scale, supports decimals like 4.5). NOTE: Despite the name, this is NOT hours worked - it is a rating.';

-- ============================================================================
-- 3. ADD CHECK CONSTRAINT FOR RATING RANGE
-- ============================================================================
-- Ensures rating values are between 1.0 and 5.0

ALTER TABLE shortlist
ADD CONSTRAINT check_volunteer_rating_range 
CHECK (volunteered_hours IS NULL OR (volunteered_hours >= 1.0 AND volunteered_hours <= 5.0));

-- ============================================================================
-- 4. ADD ESSENTIAL INDEXES FOR PERFORMANCE
-- ============================================================================
-- These improve query performance significantly

-- Index for CSR's shortlist queries
CREATE INDEX IF NOT EXISTS idx_shortlist_csr_user_id ON shortlist(csr_user_id);

-- Index for request assignment lookups
CREATE INDEX IF NOT EXISTS idx_shortlist_request_id ON shortlist(request_id);

-- Composite index for filtered queries (most common use case)
CREATE INDEX IF NOT EXISTS idx_shortlist_csr_status ON shortlist(csr_user_id, status);

-- ============================================================================
-- 5. VERIFY INSTALLATION
-- ============================================================================
-- Check that everything was created successfully

SELECT 
    'unique_csr_request' as constraint_name,
    CASE WHEN EXISTS (
        SELECT 1 FROM pg_constraint WHERE conname = 'unique_csr_request'
    ) THEN '✅ Installed' ELSE '❌ Missing' END as status
UNION ALL
SELECT 
    'check_volunteer_rating_range',
    CASE WHEN EXISTS (
        SELECT 1 FROM pg_constraint WHERE conname = 'check_volunteer_rating_range'
    ) THEN '✅ Installed' ELSE '❌ Missing' END
UNION ALL
SELECT 
    'idx_shortlist_csr_user_id',
    CASE WHEN EXISTS (
        SELECT 1 FROM pg_indexes WHERE indexname = 'idx_shortlist_csr_user_id'
    ) THEN '✅ Installed' ELSE '❌ Missing' END
UNION ALL
SELECT 
    'idx_shortlist_request_id',
    CASE WHEN EXISTS (
        SELECT 1 FROM pg_indexes WHERE indexname = 'idx_shortlist_request_id'
    ) THEN '✅ Installed' ELSE '❌ Missing' END
UNION ALL
SELECT 
    'idx_shortlist_csr_status',
    CASE WHEN EXISTS (
        SELECT 1 FROM pg_indexes WHERE indexname = 'idx_shortlist_csr_status'
    ) THEN '✅ Installed' ELSE '❌ Missing' END;

-- ============================================================================
-- DONE! ✅
-- ============================================================================
-- These changes require NO code modifications in your Python/JavaScript code
-- Your application will continue to work exactly as before, but with:
-- - Data integrity protection (no duplicates)
-- - Better performance (indexes)
-- - Data validation (rating range)
-- - Clear documentation (column comment)
-- ============================================================================

