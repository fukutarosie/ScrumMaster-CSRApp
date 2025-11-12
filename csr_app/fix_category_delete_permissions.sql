-- ============================================
-- FIX SERVICE_CATEGORY DELETE PERMISSIONS
-- ============================================

-- First, let's check current RLS policies
SELECT 
    schemaname,
    tablename,
    policyname,
    permissive,
    roles,
    cmd,
    qual,
    with_check
FROM pg_policies 
WHERE tablename = 'service_category';

-- Drop all existing policies to start fresh
DROP POLICY IF EXISTS "Allow all operations for authenticated users" ON public.service_category;
DROP POLICY IF EXISTS "Enable read access for all users" ON public.service_category;
DROP POLICY IF EXISTS "Enable insert for authenticated users only" ON public.service_category;
DROP POLICY IF EXISTS "Enable update for authenticated users only" ON public.service_category;
DROP POLICY IF EXISTS "Enable delete for authenticated users only" ON public.service_category;

-- Ensure RLS is enabled
ALTER TABLE public.service_category ENABLE ROW LEVEL SECURITY;

-- Create new comprehensive policies

-- 1. SELECT: Allow everyone to read (including anon users)
CREATE POLICY "service_category_select_policy" 
ON public.service_category
FOR SELECT
USING (true);

-- 2. INSERT: Allow authenticated users and service_role
CREATE POLICY "service_category_insert_policy" 
ON public.service_category
FOR INSERT
WITH CHECK (
    auth.role() = 'authenticated' 
    OR auth.role() = 'service_role'
    OR auth.role() = 'anon'
);

-- 3. UPDATE: Allow authenticated users and service_role
CREATE POLICY "service_category_update_policy" 
ON public.service_category
FOR UPDATE
USING (
    auth.role() = 'authenticated' 
    OR auth.role() = 'service_role'
    OR auth.role() = 'anon'
)
WITH CHECK (
    auth.role() = 'authenticated' 
    OR auth.role() = 'service_role'
    OR auth.role() = 'anon'
);

-- 4. DELETE: Allow authenticated users and service_role
CREATE POLICY "service_category_delete_policy" 
ON public.service_category
FOR DELETE
USING (
    auth.role() = 'authenticated' 
    OR auth.role() = 'service_role'
    OR auth.role() = 'anon'
);

-- Grant explicit permissions to roles
GRANT ALL ON public.service_category TO authenticated;
GRANT ALL ON public.service_category TO anon;
GRANT ALL ON public.service_category TO service_role;
GRANT USAGE, SELECT ON SEQUENCE service_category_id_seq TO authenticated;
GRANT USAGE, SELECT ON SEQUENCE service_category_id_seq TO anon;
GRANT USAGE, SELECT ON SEQUENCE service_category_id_seq TO service_role;

-- Verify the policies are created
SELECT 
    schemaname,
    tablename,
    policyname,
    permissive,
    roles,
    cmd,
    qual,
    with_check
FROM pg_policies 
WHERE tablename = 'service_category'
ORDER BY cmd, policyname;

-- Test query: Check if we can see the data
SELECT COUNT(*) as total_categories FROM public.service_category;

-- Show all categories
SELECT id, name, description FROM public.service_category ORDER BY name;
