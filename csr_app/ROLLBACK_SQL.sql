-- ============================================================================
-- ROLLBACK SCRIPT (EMERGENCY USE ONLY)
-- ============================================================================
-- Run this ONLY if something goes wrong during migration
-- This reverts all table names back to plural
-- ============================================================================

-- ⚠️ WARNING: Only run this if you need to undo the rename!

-- Rollback renames in REVERSE order
ALTER TABLE request RENAME TO requests;
ALTER TABLE "user" RENAME TO users;
ALTER TABLE role RENAME TO roles;
ALTER TABLE service_type RENAME TO service_types;

-- Verify rollback
SELECT tablename 
FROM pg_tables 
WHERE schemaname = 'public' 
  AND tablename IN ('users', 'roles', 'requests', 'service_types')
ORDER BY tablename;

-- ============================================================================
-- If data is corrupted (unlikely), restore from backup:
-- ============================================================================
-- DROP TABLE users CASCADE;
-- CREATE TABLE users AS SELECT * FROM backup_schema.users;
-- 
-- DROP TABLE roles CASCADE;
-- CREATE TABLE roles AS SELECT * FROM backup_schema.roles;
-- 
-- DROP TABLE requests CASCADE;
-- CREATE TABLE requests AS SELECT * FROM backup_schema.requests;
-- 
-- DROP TABLE service_types CASCADE;
-- CREATE TABLE service_types AS SELECT * FROM backup_schema.service_types;
--
-- Then recreate foreign keys manually (see original schema)
-- ============================================================================

