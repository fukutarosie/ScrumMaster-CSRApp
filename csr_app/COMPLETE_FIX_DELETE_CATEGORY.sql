-- ============================================
-- COMPLETE FIX FOR SERVICE_CATEGORY DELETE ISSUE
-- Run this script in Supabase SQL Editor
-- ============================================

-- Step 1: Check current state
SELECT 'Current RLS Policies:' as info;
SELECT 
    policyname,
    cmd,
    qual,
    with_check
FROM pg_policies 
WHERE tablename = 'service_category';

-- Step 2: Check for foreign key constraints
SELECT 'Foreign Key Constraints:' as info;
SELECT
    tc.constraint_name, 
    tc.table_name, 
    kcu.column_name,
    ccu.table_name AS foreign_table_name,
    rc.delete_rule
FROM information_schema.table_constraints AS tc 
JOIN information_schema.key_column_usage AS kcu
    ON tc.constraint_name = kcu.constraint_name
JOIN information_schema.constraint_column_usage AS ccu
    ON ccu.constraint_name = tc.constraint_name
JOIN information_schema.referential_constraints AS rc
    ON rc.constraint_name = tc.constraint_name
WHERE tc.constraint_type = 'FOREIGN KEY' 
    AND ccu.table_name = 'service_category';

-- Step 3: Drop all existing RLS policies
DROP POLICY IF EXISTS "Allow all operations for authenticated users" ON public.service_category;
DROP POLICY IF EXISTS "Enable read access for all users" ON public.service_category;
DROP POLICY IF EXISTS "Enable insert for authenticated users only" ON public.service_category;
DROP POLICY IF EXISTS "Enable update for authenticated users only" ON public.service_category;
DROP POLICY IF EXISTS "Enable delete for authenticated users only" ON public.service_category;
DROP POLICY IF EXISTS "service_category_select_policy" ON public.service_category;
DROP POLICY IF EXISTS "service_category_insert_policy" ON public.service_category;
DROP POLICY IF EXISTS "service_category_update_policy" ON public.service_category;
DROP POLICY IF EXISTS "service_category_delete_policy" ON public.service_category;

-- Step 4: Ensure RLS is enabled
ALTER TABLE public.service_category ENABLE ROW LEVEL SECURITY;

-- Step 5: Create permissive policies that allow all operations
-- These policies use 'true' which means they allow the operation for everyone

CREATE POLICY "service_category_select_all" 
ON public.service_category
FOR SELECT
USING (true);

CREATE POLICY "service_category_insert_all" 
ON public.service_category
FOR INSERT
WITH CHECK (true);

CREATE POLICY "service_category_update_all" 
ON public.service_category
FOR UPDATE
USING (true)
WITH CHECK (true);

CREATE POLICY "service_category_delete_all" 
ON public.service_category
FOR DELETE
USING (true);

-- Step 6: Grant explicit permissions
GRANT ALL ON public.service_category TO authenticated;
GRANT ALL ON public.service_category TO anon;
GRANT ALL ON public.service_category TO service_role;
GRANT ALL ON public.service_category TO postgres;

-- Grant sequence permissions
GRANT USAGE, SELECT ON SEQUENCE service_category_id_seq TO authenticated;
GRANT USAGE, SELECT ON SEQUENCE service_category_id_seq TO anon;
GRANT USAGE, SELECT ON SEQUENCE service_category_id_seq TO service_role;

-- Step 7: Verify the setup
SELECT 'New RLS Policies:' as info;
SELECT 
    policyname,
    cmd,
    permissive,
    roles,
    qual,
    with_check
FROM pg_policies 
WHERE tablename = 'service_category'
ORDER BY cmd;

-- Step 8: Test data access
SELECT 'Total Categories:' as info, COUNT(*) as count FROM public.service_category;
SELECT 'Sample Categories:' as info;
SELECT id, name, LEFT(description, 50) as description FROM public.service_category LIMIT 5;

-- Step 9: Test delete (optional - uncomment to test)
-- This will attempt to delete a test category if it exists
-- DO $$
-- DECLARE
--     test_id INTEGER;
-- BEGIN
--     -- Insert a test category
--     INSERT INTO public.service_category (name, description)
--     VALUES ('TEST_DELETE', 'Test category for deletion')
--     RETURNING id INTO test_id;
--     
--     RAISE NOTICE 'Created test category with ID: %', test_id;
--     
--     -- Try to delete it
--     DELETE FROM public.service_category WHERE id = test_id;
--     
--     -- Check if it was deleted
--     IF NOT EXISTS (SELECT 1 FROM public.service_category WHERE id = test_id) THEN
--         RAISE NOTICE 'Test category successfully deleted!';
--     ELSE
--         RAISE NOTICE 'Test category was NOT deleted - there is still an issue';
--     END IF;
-- END $$;

SELECT 'Setup complete! Try deleting a category from the frontend now.' as info;
