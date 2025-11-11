-- ============================================================================
-- STEP 1: BACKUP EXISTING TABLES
-- ============================================================================
-- Run this FIRST in Supabase SQL Editor
-- This creates a safety backup of all tables before renaming
-- ============================================================================

-- Create backup schema if it doesn't exist
CREATE SCHEMA IF NOT EXISTS backup_schema;

-- Backup all tables that will be renamed
CREATE TABLE IF NOT EXISTS backup_schema.users AS SELECT * FROM users;
CREATE TABLE IF NOT EXISTS backup_schema.roles AS SELECT * FROM roles;
CREATE TABLE IF NOT EXISTS backup_schema.requests AS SELECT * FROM requests;
CREATE TABLE IF NOT EXISTS backup_schema.service_types AS SELECT * FROM service_types;

-- Verify backups were created
SELECT 
    'backup_schema.users' as backup_table, 
    COUNT(*) as row_count 
FROM backup_schema.users

UNION ALL

SELECT 
    'backup_schema.roles', 
    COUNT(*) 
FROM backup_schema.roles

UNION ALL

SELECT 
    'backup_schema.requests', 
    COUNT(*) 
FROM backup_schema.requests

UNION ALL

SELECT 
    'backup_schema.service_types', 
    COUNT(*) 
FROM backup_schema.service_types;

-- ============================================================================
-- ✅ SUCCESS MESSAGE
-- ============================================================================
-- If you see row counts above matching your original tables, backups are ready!
-- Next: Run STEP_2_RENAME_SQL.sql
-- ============================================================================

