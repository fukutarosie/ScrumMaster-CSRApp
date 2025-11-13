-- ============================================================================
-- SHORTLIST TABLE IMPROVEMENTS - SQL MIGRATION SCRIPT
-- ============================================================================
-- Purpose: Address concerns identified in SHORTLIST_ANALYSIS.md
-- Execute these changes on your Supabase database
-- ============================================================================

-- IMPORTANT: Review and test these changes in a development environment first!
-- Some changes may require data migration or could cause constraints violations.

-- ============================================================================
-- 1. ADD UNIQUE CONSTRAINT - Prevent Duplicate Shortlist Entries
-- ============================================================================
-- PRIORITY: HIGH
-- CONCERN: Race conditions could create duplicate (csr_user_id, request_id) entries
-- IMPACT: Prevents data integrity issues

DO $$ 
BEGIN
    -- Check if constraint already exists
    IF NOT EXISTS (
        SELECT 1 FROM pg_constraint 
        WHERE conname = 'unique_csr_request'
    ) THEN
        -- Add unique constraint
        ALTER TABLE shortlist
        ADD CONSTRAINT unique_csr_request UNIQUE (csr_user_id, request_id);
        
        RAISE NOTICE 'Added unique constraint: unique_csr_request';
    ELSE
        RAISE NOTICE 'Constraint unique_csr_request already exists';
    END IF;
END $$;

-- ============================================================================
-- 2. RENAME COLUMN - volunteered_hours to volunteer_rating
-- ============================================================================
-- PRIORITY: CRITICAL
-- CONCERN: "volunteered_hours" is misleading - it stores a rating (1-5), not hours
-- IMPACT: Improves code clarity, prevents confusion
-- NOTE: This is a BREAKING CHANGE - requires code updates

-- OPTION A: Rename column (RECOMMENDED but requires code changes)
/*
DO $$ 
BEGIN
    IF EXISTS (
        SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'shortlist' AND column_name = 'volunteered_hours'
    ) THEN
        ALTER TABLE shortlist
        RENAME COLUMN volunteered_hours TO volunteer_rating;
        
        RAISE NOTICE 'Renamed volunteered_hours to volunteer_rating';
    ELSE
        RAISE NOTICE 'Column volunteered_hours does not exist (may already be renamed)';
    END IF;
END $$;

-- Add comment to clarify the column purpose
COMMENT ON COLUMN shortlist.volunteer_rating IS 'PIN user rating of CSR performance (1-5 scale, supports decimals like 4.5)';
*/

-- OPTION B: Keep column name but add comment (NO CODE CHANGES REQUIRED)
COMMENT ON COLUMN shortlist.volunteered_hours IS 'PIN user rating of CSR performance (1-5 scale, supports decimals like 4.5). NOTE: Despite the name, this is NOT hours worked - it is a rating.';

-- ============================================================================
-- 3. ADD AUDIT TRAIL COLUMNS
-- ============================================================================
-- PRIORITY: MEDIUM
-- CONCERN: Missing information about who completed the request and when statuses changed
-- IMPACT: Improves audit trail, useful for debugging and analytics

-- 3a. Add completed_by_user_id column
DO $$ 
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'shortlist' AND column_name = 'completed_by_user_id'
    ) THEN
        ALTER TABLE shortlist
        ADD COLUMN completed_by_user_id INTEGER REFERENCES users(id);
        
        COMMENT ON COLUMN shortlist.completed_by_user_id IS 'User ID who marked this as completed (usually the PIN user)';
        
        RAISE NOTICE 'Added column: completed_by_user_id';
    ELSE
        RAISE NOTICE 'Column completed_by_user_id already exists';
    END IF;
END $$;

-- 3b. Add in_progress_at timestamp
DO $$ 
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'shortlist' AND column_name = 'in_progress_at'
    ) THEN
        ALTER TABLE shortlist
        ADD COLUMN in_progress_at TIMESTAMP;
        
        COMMENT ON COLUMN shortlist.in_progress_at IS 'Timestamp when status changed to IN_PROGRESS (CSR started work)';
        
        RAISE NOTICE 'Added column: in_progress_at';
    ELSE
        RAISE NOTICE 'Column in_progress_at already exists';
    END IF;
END $$;

-- 3c. Add declined_at timestamp
DO $$ 
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'shortlist' AND column_name = 'declined_at'
    ) THEN
        ALTER TABLE shortlist
        ADD COLUMN declined_at TIMESTAMP;
        
        COMMENT ON COLUMN shortlist.declined_at IS 'Timestamp when CSR withdrew/declined the opportunity';
        
        RAISE NOTICE 'Added column: declined_at';
    ELSE
        RAISE NOTICE 'Column declined_at already exists';
    END IF;
END $$;

-- ============================================================================
-- 4. ADD CHECK CONSTRAINTS FOR DATA VALIDATION
-- ============================================================================
-- PRIORITY: MEDIUM
-- CONCERN: No database-level validation for rating values
-- IMPACT: Prevents invalid data (e.g., rating of 10 or -1)

-- 4a. Validate volunteer_rating range (1.0 to 5.0)
DO $$ 
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM pg_constraint 
        WHERE conname = 'check_volunteer_rating_range'
    ) THEN
        ALTER TABLE shortlist
        ADD CONSTRAINT check_volunteer_rating_range 
        CHECK (volunteered_hours IS NULL OR (volunteered_hours >= 1.0 AND volunteered_hours <= 5.0));
        
        RAISE NOTICE 'Added check constraint: check_volunteer_rating_range';
    ELSE
        RAISE NOTICE 'Constraint check_volunteer_rating_range already exists';
    END IF;
END $$;

-- 4b. Validate status values
DO $$ 
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM pg_constraint 
        WHERE conname = 'check_shortlist_status'
    ) THEN
        ALTER TABLE shortlist
        ADD CONSTRAINT check_shortlist_status 
        CHECK (status IN ('SHORTLISTED', 'IN_PROGRESS', 'COMPLETED', 'DECLINED'));
        
        RAISE NOTICE 'Added check constraint: check_shortlist_status';
    ELSE
        RAISE NOTICE 'Constraint check_shortlist_status already exists';
    END IF;
END $$;

-- ============================================================================
-- 5. ADD INDEXES FOR PERFORMANCE
-- ============================================================================
-- PRIORITY: HIGH
-- CONCERN: Queries on status and csr_user_id are common but may not have indexes
-- IMPACT: Improves query performance, especially as data grows

-- 5a. Index on csr_user_id (for quick lookup of CSR's shortlist)
DO $$ 
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM pg_indexes 
        WHERE indexname = 'idx_shortlist_csr_user_id'
    ) THEN
        CREATE INDEX idx_shortlist_csr_user_id ON shortlist(csr_user_id);
        RAISE NOTICE 'Created index: idx_shortlist_csr_user_id';
    ELSE
        RAISE NOTICE 'Index idx_shortlist_csr_user_id already exists';
    END IF;
END $$;

-- 5b. Index on request_id (for quick lookup of CSR assignments per request)
DO $$ 
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM pg_indexes 
        WHERE indexname = 'idx_shortlist_request_id'
    ) THEN
        CREATE INDEX idx_shortlist_request_id ON shortlist(request_id);
        RAISE NOTICE 'Created index: idx_shortlist_request_id';
    ELSE
        RAISE NOTICE 'Index idx_shortlist_request_id already exists';
    END IF;
END $$;

-- 5c. Composite index on (csr_user_id, status) for filtered queries
DO $$ 
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM pg_indexes 
        WHERE indexname = 'idx_shortlist_csr_status'
    ) THEN
        CREATE INDEX idx_shortlist_csr_status ON shortlist(csr_user_id, status);
        RAISE NOTICE 'Created index: idx_shortlist_csr_status';
    ELSE
        RAISE NOTICE 'Index idx_shortlist_csr_status already exists';
    END IF;
END $$;

-- 5d. Index on status (for counting requests by status)
DO $$ 
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM pg_indexes 
        WHERE indexname = 'idx_shortlist_status'
    ) THEN
        CREATE INDEX idx_shortlist_status ON shortlist(status);
        RAISE NOTICE 'Created index: idx_shortlist_status';
    ELSE
        RAISE NOTICE 'Index idx_shortlist_status already exists';
    END IF;
END $$;

-- ============================================================================
-- 6. CREATE TRIGGER TO AUTO-UPDATE in_progress_at
-- ============================================================================
-- PRIORITY: LOW
-- CONCERN: Automate timestamp updates when status changes
-- IMPACT: Ensures timestamps are accurate without relying on application code

-- 6a. Create trigger function
CREATE OR REPLACE FUNCTION update_shortlist_timestamps()
RETURNS TRIGGER AS $$
BEGIN
    -- When status changes to IN_PROGRESS, set in_progress_at
    IF NEW.status = 'IN_PROGRESS' AND (OLD.status IS NULL OR OLD.status != 'IN_PROGRESS') THEN
        NEW.in_progress_at = NOW();
    END IF;
    
    -- When status changes to DECLINED, set declined_at
    IF NEW.status = 'DECLINED' AND (OLD.status IS NULL OR OLD.status != 'DECLINED') THEN
        NEW.declined_at = NOW();
    END IF;
    
    -- Always update updated_at
    NEW.updated_at = NOW();
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- 6b. Create trigger
DO $$ 
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM pg_trigger 
        WHERE tgname = 'trigger_shortlist_timestamps'
    ) THEN
        CREATE TRIGGER trigger_shortlist_timestamps
        BEFORE UPDATE ON shortlist
        FOR EACH ROW
        EXECUTE FUNCTION update_shortlist_timestamps();
        
        RAISE NOTICE 'Created trigger: trigger_shortlist_timestamps';
    ELSE
        RAISE NOTICE 'Trigger trigger_shortlist_timestamps already exists';
    END IF;
END $$;

-- ============================================================================
-- 7. ADD TABLE COMMENTS FOR DOCUMENTATION
-- ============================================================================
COMMENT ON TABLE shortlist IS 'Tracks CSR Rep shortlist items and assignments. Lifecycle: SHORTLISTED -> IN_PROGRESS -> COMPLETED (or DECLINED)';

COMMENT ON COLUMN shortlist.id IS 'Primary key';
COMMENT ON COLUMN shortlist.csr_user_id IS 'CSR Rep who shortlisted/is working on the request';
COMMENT ON COLUMN shortlist.request_id IS 'The PIN request being worked on';
COMMENT ON COLUMN shortlist.status IS 'Current status: SHORTLISTED, IN_PROGRESS, COMPLETED, or DECLINED';
COMMENT ON COLUMN shortlist.notes IS 'CSR notes about the request (optional)';
COMMENT ON COLUMN shortlist.completion_date IS 'Date when marked as COMPLETED';
COMMENT ON COLUMN shortlist.feedback_from_pin IS 'Feedback from PIN user about CSR performance (optional)';
COMMENT ON COLUMN shortlist.shortlisted_at IS 'Timestamp when CSR added to their shortlist';
COMMENT ON COLUMN shortlist.updated_at IS 'Last updated timestamp';

-- ============================================================================
-- 8. DATA CLEANUP (OPTIONAL) - Remove Duplicates if They Exist
-- ============================================================================
-- WARNING: Only run this if you have duplicate entries
-- This will keep the OLDEST entry for each (csr_user_id, request_id) pair

/*
-- First, check if duplicates exist
SELECT csr_user_id, request_id, COUNT(*) as duplicate_count
FROM shortlist
GROUP BY csr_user_id, request_id
HAVING COUNT(*) > 1;

-- If duplicates exist, delete them (keeping the oldest entry)
DELETE FROM shortlist
WHERE id NOT IN (
    SELECT MIN(id)
    FROM shortlist
    GROUP BY csr_user_id, request_id
);
*/

-- ============================================================================
-- 9. VERIFY CHANGES
-- ============================================================================
-- Run these queries to verify the changes were applied successfully

-- Check constraints
SELECT conname, contype, pg_get_constraintdef(oid)
FROM pg_constraint
WHERE conrelid = 'shortlist'::regclass;

-- Check indexes
SELECT indexname, indexdef
FROM pg_indexes
WHERE tablename = 'shortlist';

-- Check columns
SELECT column_name, data_type, column_default, is_nullable
FROM information_schema.columns
WHERE table_name = 'shortlist'
ORDER BY ordinal_position;

-- Check triggers
SELECT tgname, tgtype, tgenabled, pg_get_triggerdef(oid)
FROM pg_trigger
WHERE tgrelid = 'shortlist'::regclass;

-- ============================================================================
-- ROLLBACK SCRIPT (Emergency Use Only)
-- ============================================================================
-- Save this section separately - use only if you need to undo changes

/*
-- Remove unique constraint
ALTER TABLE shortlist DROP CONSTRAINT IF EXISTS unique_csr_request;

-- Remove check constraints
ALTER TABLE shortlist DROP CONSTRAINT IF EXISTS check_volunteer_rating_range;
ALTER TABLE shortlist DROP CONSTRAINT IF EXISTS check_shortlist_status;

-- Remove new columns
ALTER TABLE shortlist DROP COLUMN IF EXISTS completed_by_user_id;
ALTER TABLE shortlist DROP COLUMN IF EXISTS in_progress_at;
ALTER TABLE shortlist DROP COLUMN IF EXISTS declined_at;

-- Remove indexes
DROP INDEX IF EXISTS idx_shortlist_csr_user_id;
DROP INDEX IF EXISTS idx_shortlist_request_id;
DROP INDEX IF EXISTS idx_shortlist_csr_status;
DROP INDEX IF EXISTS idx_shortlist_status;

-- Remove trigger
DROP TRIGGER IF EXISTS trigger_shortlist_timestamps ON shortlist;
DROP FUNCTION IF EXISTS update_shortlist_timestamps();

-- Revert column rename (if you used OPTION A)
ALTER TABLE shortlist RENAME COLUMN volunteer_rating TO volunteered_hours;
*/

-- ============================================================================
-- SUMMARY OF CHANGES
-- ============================================================================
/*
APPLIED CHANGES:
✅ 1. Added unique constraint on (csr_user_id, request_id)
✅ 2. Added comment to volunteered_hours column (or renamed to volunteer_rating)
✅ 3. Added completed_by_user_id, in_progress_at, declined_at columns
✅ 4. Added check constraints for rating range and status values
✅ 5. Added performance indexes
✅ 6. Created trigger to auto-update timestamps
✅ 7. Added table and column documentation

IMPACT:
- Data integrity: Prevents duplicates
- Performance: Faster queries with indexes
- Audit trail: New timestamp columns
- Validation: Check constraints prevent bad data
- Documentation: Comments clarify purpose

BREAKING CHANGES:
- If you rename volunteered_hours to volunteer_rating, you MUST update Python code
- Unique constraint may fail if duplicates exist (run cleanup first)

NEXT STEPS FOR CODE:
1. If you renamed the column, update Python entity (src/entity/shortlist.py)
2. Update controller stats to use "average_rating" instead of "total_hours"
3. Test all shortlist-related endpoints
4. Update frontend to handle new fields if needed
*/

