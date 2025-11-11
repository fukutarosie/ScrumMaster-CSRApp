-- ============================================================================
-- STEP 3: VERIFY DATABASE CHANGES
-- ============================================================================
-- Run this AFTER STEP_2_RENAME_SQL.sql completes
-- This confirms all tables were renamed correctly and data is intact
-- ============================================================================

-- ============================================================================
-- CHECK 1: Verify all new table names exist
-- ============================================================================
SELECT tablename 
FROM pg_tables 
WHERE schemaname = 'public' 
  AND tablename IN ('user', 'role', 'request', 'shortlist', 'request_status_history', 'service_type')
ORDER BY tablename;

-- Expected output: 6 rows
-- request
-- request_status_history
-- role
-- service_type
-- shortlist
-- user

-- ============================================================================
-- CHECK 2: Verify row counts match backups
-- ============================================================================
SELECT 
    'user' as table_name, 
    COUNT(*) as row_count,
    (SELECT COUNT(*) FROM backup_schema.users) as backup_count
FROM "user"

UNION ALL

SELECT 
    'role', 
    COUNT(*),
    (SELECT COUNT(*) FROM backup_schema.roles)
FROM role

UNION ALL

SELECT 
    'request', 
    COUNT(*),
    (SELECT COUNT(*) FROM backup_schema.requests)
FROM request

UNION ALL

SELECT 
    'service_type', 
    COUNT(*),
    (SELECT COUNT(*) FROM backup_schema.service_types)
FROM service_type

UNION ALL

SELECT 
    'shortlist', 
    COUNT(*),
    NULL  -- No backup needed (already singular)
FROM shortlist

UNION ALL

SELECT 
    'request_status_history', 
    COUNT(*),
    NULL  -- No backup needed (already singular)
FROM request_status_history;

-- ✅ If row_count = backup_count for each table, data is intact!

-- ============================================================================
-- CHECK 3: Verify foreign key constraints are intact
-- ============================================================================
SELECT 
    tc.table_name as "Table", 
    kcu.column_name as "Column",
    ccu.table_name as "References Table",
    ccu.column_name as "References Column"
FROM information_schema.table_constraints AS tc 
JOIN information_schema.key_column_usage AS kcu
    ON tc.constraint_name = kcu.constraint_name
    AND tc.table_schema = kcu.table_schema
JOIN information_schema.constraint_column_usage AS ccu
    ON ccu.constraint_name = tc.constraint_name
    AND ccu.table_schema = tc.table_schema
WHERE tc.constraint_type = 'FOREIGN KEY'
  AND tc.table_schema = 'public'
ORDER BY tc.table_name;

-- Expected foreign keys:
-- user.role_id -> role.id
-- request.pin_user_id -> user.id
-- shortlist.csr_user_id -> user.id
-- shortlist.request_id -> request.id
-- request_status_history.request_id -> request.id
-- request_status_history.changed_by -> user.id (if exists)

-- ============================================================================
-- CHECK 4: Test a simple query on each renamed table
-- ============================================================================

-- Test user table (note: quotes needed in SQL, but not in Python)
SELECT id, username, email FROM "user" LIMIT 3;

-- Test role table
SELECT id, role_name, role_code FROM role LIMIT 3;

-- Test request table
SELECT id, title, status FROM request LIMIT 3;

-- Test service_type table
SELECT * FROM service_type LIMIT 3;

-- Test joins still work
SELECT 
    u.username,
    r.role_name
FROM "user" u
JOIN role r ON u.role_id = r.id
LIMIT 3;

-- Test shortlist with request join
SELECT 
    s.id,
    s.status,
    req.title
FROM shortlist s
JOIN request req ON s.request_id = req.id
LIMIT 3;

-- ============================================================================
-- ✅ SUCCESS CHECKLIST
-- ============================================================================
-- [ ] CHECK 1: All 6 table names appear (user, role, request, etc.)
-- [ ] CHECK 2: All row counts match backup counts
-- [ ] CHECK 3: All foreign keys are listed correctly
-- [ ] CHECK 4: All SELECT queries return data without errors
--
-- If ALL checks pass, database migration is COMPLETE! ✅
-- Next: Let me know, and I'll update the Python code automatically
-- ============================================================================

