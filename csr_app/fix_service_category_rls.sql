-- ============================================
-- FIX SERVICE_CATEGORY TABLE AND RLS POLICIES
-- ============================================

-- Ensure the table exists with correct structure
CREATE TABLE IF NOT EXISTS public.service_category (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL UNIQUE,
    description TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create index for better search performance
CREATE INDEX IF NOT EXISTS idx_service_category_name ON public.service_category(name);
CREATE INDEX IF NOT EXISTS idx_service_category_description ON public.service_category USING gin(to_tsvector('english', description));

-- Enable RLS
ALTER TABLE public.service_category ENABLE ROW LEVEL SECURITY;

-- Drop all existing policies
DROP POLICY IF EXISTS "Allow all operations for authenticated users" ON public.service_category;
DROP POLICY IF EXISTS "Enable read access for all users" ON public.service_category;
DROP POLICY IF EXISTS "Enable insert for authenticated users only" ON public.service_category;
DROP POLICY IF EXISTS "Enable update for authenticated users only" ON public.service_category;
DROP POLICY IF EXISTS "Enable delete for authenticated users only" ON public.service_category;

-- Create comprehensive RLS policies

-- Allow SELECT for all authenticated users (including anon key)
CREATE POLICY "Enable read access for all users" 
ON public.service_category
FOR SELECT
USING (true);

-- Allow INSERT for authenticated users
CREATE POLICY "Enable insert for authenticated users only" 
ON public.service_category
FOR INSERT
WITH CHECK (auth.role() = 'authenticated' OR auth.role() = 'service_role');

-- Allow UPDATE for authenticated users
CREATE POLICY "Enable update for authenticated users only" 
ON public.service_category
FOR UPDATE
USING (auth.role() = 'authenticated' OR auth.role() = 'service_role')
WITH CHECK (auth.role() = 'authenticated' OR auth.role() = 'service_role');

-- Allow DELETE for authenticated users
CREATE POLICY "Enable delete for authenticated users only" 
ON public.service_category
FOR DELETE
USING (auth.role() = 'authenticated' OR auth.role() = 'service_role');

-- Insert default service categories if they don't exist
INSERT INTO public.service_category (name, description) VALUES
    ('Technology', 'Technology-related services and support'),
    ('Healthcare', 'Healthcare and medical services'),
    ('Education', 'Educational services and training'),
    ('Finance', 'Financial services and consulting'),
    ('Legal', 'Legal services and consultation'),
    ('Transportation', 'Transportation and logistics services'),
    ('Home Services', 'Home maintenance and repair services'),
    ('Food & Beverage', 'Food delivery and catering services'),
    ('Entertainment', 'Entertainment and event services'),
    ('Professional Services', 'Professional consulting and advisory services')
ON CONFLICT (name) DO NOTHING;

-- Grant necessary permissions to authenticated role
GRANT SELECT ON public.service_category TO authenticated;
GRANT SELECT ON public.service_category TO anon;
GRANT INSERT, UPDATE, DELETE ON public.service_category TO authenticated;
GRANT USAGE, SELECT ON SEQUENCE service_category_id_seq TO authenticated;

-- Verify the setup
SELECT 
    schemaname,
    tablename,
    rowsecurity as "RLS Enabled"
FROM pg_tables 
WHERE tablename = 'service_category';

-- Show all policies
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

-- Show sample data
SELECT id, name, description FROM public.service_category LIMIT 5;
