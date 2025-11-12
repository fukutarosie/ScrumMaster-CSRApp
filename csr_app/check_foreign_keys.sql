-- ============================================
-- CHECK FOR FOREIGN KEY CONSTRAINTS
-- ============================================

-- Check if any tables reference service_category
SELECT
    tc.table_schema, 
    tc.constraint_name, 
    tc.table_name, 
    kcu.column_name,
    ccu.table_schema AS foreign_table_schema,
    ccu.table_name AS foreign_table_name,
    ccu.column_name AS foreign_column_name,
    rc.update_rule,
    rc.delete_rule
FROM information_schema.table_constraints AS tc 
JOIN information_schema.key_column_usage AS kcu
    ON tc.constraint_name = kcu.constraint_name
    AND tc.table_schema = kcu.table_schema
JOIN information_schema.constraint_column_usage AS ccu
    ON ccu.constraint_name = tc.constraint_name
    AND ccu.table_schema = tc.table_schema
JOIN information_schema.referential_constraints AS rc
    ON rc.constraint_name = tc.constraint_name
WHERE tc.constraint_type = 'FOREIGN KEY' 
    AND ccu.table_name = 'service_category';

-- If there are foreign key constraints, we need to handle them
-- Option 1: Add CASCADE delete
-- Option 2: Check for dependent records before deleting

-- Check if there are any dependent records (example for common tables)
-- Uncomment and modify based on your actual schema

-- SELECT 'csr_requests' as table_name, COUNT(*) as dependent_records
-- FROM csr_requests 
-- WHERE category_id IN (SELECT id FROM service_category);

-- SELECT 'services' as table_name, COUNT(*) as dependent_records
-- FROM services 
-- WHERE category_id IN (SELECT id FROM service_category);
