-- ============================================================================
-- STEP 2: RENAME TABLES FROM PLURAL TO SINGULAR
-- ============================================================================
-- Run this AFTER STEP_1_BACKUP_SQL.sql completes successfully
-- ORDER MATTERS! We rename in a specific sequence to preserve foreign keys
-- ============================================================================

-- ============================================================================
-- IMPORTANT: Rename order to avoid FK constraint conflicts
-- ============================================================================
-- 1. service_types (no FK dependencies)
-- 2. roles (no FK dependencies)  
-- 3. users (depends on roles)
-- 4. requests (depends on users)
-- ============================================================================

-- Step 1: Rename service_types (independent table)
ALTER TABLE service_types RENAME TO service_type;

-- Step 2: Rename roles (independent table)
ALTER TABLE roles RENAME TO role;

-- Step 3: Rename users (depends on role)
-- Note: "user" is a reserved word in PostgreSQL, so we quote it
-- But in Python/Supabase client, you use it WITHOUT quotes: supabase.table('user')
ALTER TABLE users RENAME TO "user";

-- Step 4: Rename requests (depends on user)
ALTER TABLE requests RENAME TO request;

-- ============================================================================
-- NOTE: These tables are ALREADY SINGULAR - no changes needed:
-- - shortlist
-- - request_status_history
-- ============================================================================

-- ============================================================================
-- ✅ SUCCESS MESSAGE
-- ============================================================================
-- Tables have been renamed! PostgreSQL automatically updates:
-- ✅ Indexes
-- ✅ Constraints
-- ✅ Foreign key references
--
-- Next: Run STEP_3_VERIFY_SQL.sql to confirm everything worked
-- ============================================================================

